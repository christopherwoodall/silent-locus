#!/usr/bin/env python3
"""Third-party IOC feed scanner (Hermes port of lane 14).

Asks AlienVault OTX whether anyone else has reported our watched
infrastructure (Counsel-confirmed malicious panel IPs, Tier-1
agent-infra domains, Tier-5 C2-like domains). A third-party pulse
is SECONDARY corroboration, or a warning that an IP has a prior
malicious history. Confidence is capped LOW.

Feed status (verified 2026-10-22):
- OTX: GET /api/v1/indicators/{type}/{value}/general is KEYLESS.
  Pulse listing needs a key; not wired, no account created.
- URLhaus: needs an abuse.ch Auth-Key (401 without one).
  Disabled. Account creation is not authorized.
- ThreatFox: same abuse.ch Auth-Key requirement. Disabled.

Each OTX hit is one pulse (not previously seen) that references
a watched indicator. Pulses older than max_pulse_age_days are
recorded but not emitted, so a first run does not surface
years-old history as "new".

State: hermes/workspace/state/iocfeeds_seen.json, mapping
"<type>:<value>" to seen pulse IDs.

Passive only. GET to otx.alienvault.com. HTTP 429 is a hard stop.

Port changes vs the source: config from tools/config.json;
state under hermes/workspace/state/; no silent-locus paths.
The whole scanner ships disabled in this profile (source had
iocfeeds/otx enabled); the runner gate enforces that.

Usage: iocfeeds.py [--dry-run] [--since-hours 24] [--json]
"""
from __future__ import annotations

import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    USER_AGENT, load_config, make_hit, utcnow_iso,
    is_new, mark_seen, attach_ip_classification,
    parse_args, emit, report_error, STATE_DIR, scanner_enabled,
)

LANE = "iocfeeds"
OTX_BASE = "https://otx.alienvault.com/api/v1/indicators"
STATE_PATH = os.path.join(STATE_DIR, "iocfeeds_seen.json")


def _otx_get(ind_type: str, value: str) -> tuple[int, dict | None]:
    url = (f"{OTX_BASE}/{ind_type}/"
           f"{urllib.parse.quote(value, safe='')}/general")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        print(f"[iocfeeds] OTX request failed for {value}: "
              f"{type(e).__name__}: {e}", file=sys.stderr)
        return -1, None


def _load_seen() -> dict:
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def _save_seen(seen: dict) -> None:
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(seen, f, indent=1, ensure_ascii=False, sort_keys=True)
    os.rename(tmp, STATE_PATH)


def _pulse_age_days(created: str) -> float | None:
    try:
        ts = created.replace("Z", "+00:00")
        dt = datetime.datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        now = datetime.datetime.now(datetime.timezone.utc)
        return (now - dt).total_seconds() / 86400.0
    except Exception:
        return None


def scan_indicator(ind: dict, seen: dict, collected_at: str,
                    max_age_days: float, config: dict,
                    dry_run: bool, seed_only: bool = False) -> list:
    ind_type = ind.get("type", "")
    value = ind.get("value", "")
    label = ind.get("label", value)
    key = f"{ind_type}:{value}"
    hits = []
    if dry_run:
        print(f"[dry-run] iocfeeds OTX lookup: {ind_type} {value} "
              f"({label})", file=sys.stderr)
        return hits
    status, data = _otx_get(ind_type, value)
    if status == 429:
        report_error("iocfeeds", "RateLimited",
                     "OTX returned 429; aborting run",
                     {"indicator": key})
        raise RuntimeError("OTX 429: hard stop")
    if status != 200 or not data:
        print(f"[iocfeeds] {key}: HTTP {status} (skipped)",
              file=sys.stderr)
        report_error("iocfeeds", "FetchFailed",
                     f"OTX lookup returned HTTP {status}",
                     {"indicator": key})
        return hits
    seen_ids = set(seen.get(key, []))
    pulses = (data.get("pulse_info") or {}).get("pulses") or []
    print(f"[iocfeeds] {key}: {len(pulses)} pulses total",
          file=sys.stderr)
    for p in pulses:
        pid = str(p.get("id", ""))
        if not pid:
            continue
        created = p.get("created") or ""
        age = _pulse_age_days(created)
        if pid not in seen_ids:
            seen_ids.add(pid)
            if seed_only:
                # First run: seed the baseline, emit nothing.
                # No first-run backlog is reported as "new".
                continue
            if age is None or age > max_age_days:
                continue
            name = (p.get("name") or "")[:160]
            desc = ((p.get("description") or "").replace("\n", " "))[:200]
            hit = make_hit(
                lane=LANE,
                source_url=(f"https://otx.alienvault.com/pulse/{pid}"),
                indicators_matched=[value, label],
                confidence="LOW",
                summary=(f"[iocfeeds] OTX pulse {pid} references {value} "
                         f"({label}): {name} [{created[:10]}]"),
                provenance={
                    "method": "OTX keyless indicator lookup",
                    "endpoint": f"/api/v1/indicators/{ind_type}/"
                                f"{value}/general",
                    "indicator": key,
                    "pulse_id": pid,
                    "pulse_name": name,
                    "pulse_created": created,
                    "pulse_description": desc,
                    "retrieved_at": collected_at,
                },
                observed_at=utcnow_iso(),
                extra={
                    "indicator_type": ind_type,
                    "indicator_value": value,
                    "indicator_label": label,
                    "pulse_id": pid,
                    "pulse_created": created,
                },
                grade="SECONDARY",
            )
            if ind_type == "IPv4":
                hit = attach_ip_classification(hit, value, config)
            hits.append(hit)
    seen[key] = sorted(seen_ids)
    return hits


def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False):
    """Check OTX for third-party pulses on watched indicators.

    seen_ids is accepted for contract compatibility. This lane
    keeps its own per-indicator pulse-ID state file, so the
    shared set is only marked, never read.
    """
    if not dry_run and not scanner_enabled("iocfeeds"):
        print("[iocfeeds] live scan refused: iocfeeds.enabled is "
              "not true in config.json (module ships disabled)",
              file=sys.stderr)
        raise SystemExit(2)
    cfg = load_config()
    block = cfg.get("scanners", {}).get("iocfeeds", {})
    feeds = block.get("feeds", {})
    for name in ("urlhaus", "threatfox"):
        f = feeds.get(name, {})
        if f.get("enabled") and f.get("needs_key"):
            report_error("iocfeeds", "NeedsKey",
                         f"{name} enabled but requires an auth key",
                         {"feed": name})
            print(f"[iocfeeds] {name}: enabled but needs_key — skipping",
                  file=sys.stderr)
    indicators = block.get("otx_indicators", [])
    spacing = float(block.get("rate_limit_seconds", 3))
    max_age_days = float(block.get("max_pulse_age_days", 90))
    collected_at = utcnow_iso()
    seen = _load_seen()
    # Feed-level gate: OTX lookups run only when the feed block
    # itself says enabled:true. A scanner-level enable alone
    # does not turn the feed on.
    otx_enabled = feeds.get("otx", {}).get("enabled", False) is True
    if not dry_run and not otx_enabled:
        print("[iocfeeds] OTX feed is disabled in config "
              "(feeds.otx.enabled is not true); skipping all OTX "
              "lookups, no network calls", file=sys.stderr)
        return []
    # Empty seen file means a first run: seed seen with all
    # current pulse IDs and emit nothing.
    seed_only = (not dry_run and not seen)
    if seed_only:
        print("[iocfeeds] empty seen file: seeding baseline from "
              "current pulses, emitting nothing this run",
              file=sys.stderr)
    hits = []
    for ind in indicators:
        try:
            hits.extend(scan_indicator(ind, seen, collected_at,
                                       max_age_days, cfg, dry_run,
                                       seed_only))
        except RuntimeError:
            # OTX 429: save seen state BEFORE re-raising, so
            # pulses already processed are neither lost nor
            # re-emitted as new on the next run.
            if not dry_run:
                _save_seen(seen)
            raise
        except Exception as e:
            print(f"[iocfeeds] indicator {ind.get('value')!r} failed: "
                  f"{type(e).__name__}: {e}", file=sys.stderr)
            report_error("iocfeeds", type(e).__name__, str(e),
                         {"indicator": ind.get("value")})
        if not dry_run:
            time.sleep(spacing)
    if not dry_run:
        _save_seen(seen)
    if seen_ids is not None:
        for h in hits:
            seen_ids.add(f"iocfeeds:{h.get('pulse_id')}")
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    hits.sort(key=lambda h: (rank.get(h["confidence"], 3), h["summary"]))
    return hits


def main():
    args = parse_args("Third-party IOC feed scanner (Hermes port)")
    try:
        hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    except RuntimeError as e:
        print(f"[iocfeeds] {e}", file=sys.stderr)
        sys.exit(2)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
