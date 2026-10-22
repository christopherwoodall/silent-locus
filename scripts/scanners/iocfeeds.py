#!/usr/bin/env python3
"""Lane 14 — third-party IOC feed scanner: AlienVault OTX (keyless),
URLhaus, ThreatFox.

What this module does: asks AlienVault OTX whether anyone else has
reported OUR watched infrastructure (the 4 Counsel-confirmed malicious
Cairn panel IPs, Tier-1 agent-infra domains, Tier-5 C2-like domains).
A third-party pulse referencing our infrastructure is SECONDARY
corroboration — or a warning that an IP has a prior malicious history.

Feed status (verified 2026-10-22):
  - OTX: GET /api/v1/indicators/{type}/{value}/general is KEYLESS
    (200, real pulse data). The pulse subscription/listing endpoints
    (/api/v1/pulses/...) need a free OTX API key — not wired, no
    account created.
  - URLhaus: REQUIRES Auth-Key (free abuse.ch account). The community
    API moved behind auth.abuse.ch login; unauthenticated calls return
    HTTP 401 as of 2026-10-22. Feed disabled in config; account
    creation not authorized.
  - ThreatFox: same abuse.ch Auth-Key requirement (401 without
    auth_key as of 2026-10-22). Feed disabled in config.

Each OTX hit = one pulse (not previously seen) referencing a watched
indicator. Confidence is capped LOW and grade is SECONDARY: these are
other people's reports, not our bytes. A hit we independently verify
becomes PRIMARY through the normal review path.

State: scripts/scanners/state/iocfeeds_seen.json maps
"<type>:<value>" -> [seen pulse IDs]. Pulses older than
max_pulse_age_days are recorded but not emitted (first-run baseline
would otherwise surface years-old history as "new").

Passive only. GET requests to otx.alienvault.com. Polite spacing
(request_spacing_seconds, default 3). HTTP 429 = hard stop.

IP-classification note (standing rule): every IPv4 indicator hit gets
attach_ip_classification() via _common — cloud/known-host status is a
priority indicator.

Usage:
    iocfeeds.py [--dry-run] [--since-hours 24] [--json]

Indicator watchlist comes from
~/workspace/silent-locus/scripts/swarm-infra-config.json ("iocfeeds"
block, "otx_indicators").
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
    parse_args, emit, report_error,
)

LANE = "iocfeeds"
OTX_BASE = "https://otx.alienvault.com/api/v1/indicators"
STATE_PATH = os.path.expanduser(
    "~/workspace/silent-locus/scripts/scanners/state/iocfeeds_seen.json")


def _otx_get(ind_type: str, value: str) -> tuple[int, dict | None]:
    """Keyless OTX indicator lookup. Returns (status, parsed JSON)."""
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
    """OTX '2026-09-14T00:05:58.709000' -> age in days. None if unparseable."""
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
                    max_age_days: float, spacing: float,
                    config: dict, dry_run: bool) -> list:
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
        # Hard stop per standing rule.
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
        # Record everything seen; emit only fresh, in-window pulses.
        if pid not in seen_ids:
            seen_ids.add(pid)
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

    Returns list of factum-ready hit dicts. seen_ids is accepted for
    orchestrator contract compatibility but this lane keeps its own
    per-indicator pulse-ID state file (ids, not a flat set), so the
    shared set is only marked, never read.
    """
    cfg = load_config()
    block = cfg.get("iocfeeds", {})
    feeds = block.get("feeds", {})

    if not block.get("enabled", True):
        print("[iocfeeds] disabled in config", file=sys.stderr)
        return []
    if not feeds.get("otx", {}).get("enabled", True):
        print("[iocfeeds] OTX feed disabled in config", file=sys.stderr)
        return []
    for name in ("urlhaus", "threatfox"):
        f = feeds.get(name, {})
        if f.get("enabled") and f.get("needs_key"):
            report_error("iocfeeds", "NeedsKey",
                         f"{name} enabled but requires an auth key",
                         {"feed": name})
            print(f"[iocfeeds] {name}: enabled but needs_key — skipping",
                  file=sys.stderr)

    indicators = block.get("otx_indicators", [])
    spacing = float(block.get("request_spacing_seconds", 3))
    max_age_days = float(block.get("max_pulse_age_days", 90))
    collected_at = utcnow_iso()
    seen = _load_seen()

    hits = []
    for ind in indicators:
        try:
            hits.extend(scan_indicator(ind, seen, collected_at,
                                        max_age_days, spacing, cfg,
                                        dry_run))
        except RuntimeError:
            raise  # 429 hard stop propagates
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
    args = parse_args("Lane 14 — third-party IOC feed scanner "
                      "(OTX keyless; URLhaus/ThreatFox need keys)")
    try:
        hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    except RuntimeError as e:
        print(f"[iocfeeds] {e}", file=sys.stderr)
        sys.exit(2)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
