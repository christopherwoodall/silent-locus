#!/usr/bin/env python3
"""crt.sh certificate-transparency scanner (Hermes port of lane 8).

Monitors Certificate Transparency (via crt.sh) for NEW certs tied
to fleet proxy infrastructure:

- %.hysandbox.tencent-cloud.com (fleet proxy cert wildcard)
- %hy3% / %hy4% (Tencent Hunyuan model naming), kept only when
  'tencent' appears in the issuer name or the SAN list. The bare
  patterns are extremely noisy, and both ship disabled.

API: https://crt.sh/?q=<pattern>&output=json&exclude=expired
The known fleet cert (serial in config) is excluded and never
reported. Only certs newer than the look-back window (by crt.sh
entry_timestamp, else not_before) are reported.

crt.sh rate-limits hard (429 seen 2026-10-14 from shared egress).
This module sleeps 10 s between patterns and ABORTS the remaining
patterns on a 429. A 429 is a hard stop for this provider.

Passive only: only the public CT search index is queried.
crt.sh rows carry no IP, so no IP classification is attached.

Port changes vs the source: config from tools/config.json
(relative to this file); no silent-locus paths; no other change
to query or filter logic.

Usage: crtsh.py [--dry-run] [--since-hours 24] [--json]
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
    is_new, mark_seen, parse_args, emit, scanner_enabled,
)

LANE = "crtsh"
CRTSH_BASE = "https://crt.sh/"


class RateLimited(Exception):
    """crt.sh answered 429: hard stop for this provider in this run."""


def _query(pattern: str) -> tuple[int, list | None]:
    params = urllib.parse.urlencode(
        {"q": pattern, "output": "json", "exclude": "expired"})
    url = f"{CRTSH_BASE}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body) if body.strip() else []
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise RateLimited(f"crt.sh 429 for pattern {pattern!r}")
        return e.code, None
    except RateLimited:
        raise
    except Exception as e:
        print(f"[crtsh] pattern {pattern!r} failed: {type(e).__name__}: {e}",
              file=sys.stderr)
        return -1, None


def _parse_ts(ts: str) -> datetime.datetime | None:
    if not ts:
        return None
    try:
        dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        return dt
    except Exception:
        return None


def _issuer_or_san_tencent(cert: dict) -> bool:
    issuer = (cert.get("issuer_name") or "").lower()
    sans = (cert.get("name_value") or "").lower()
    return "tencent" in issuer or "tencent" in sans


def scan_pattern(pat: dict, cutoff: datetime.datetime, known_serial: str,
                 seen_ids, collected_at: str, dry_run: bool,
                 result_cap: int) -> list:
    pattern = pat["q"]
    label = pat.get("label", pattern)
    needs_tencent = bool(pat.get("issuer_filter"))
    indicators_base = pat.get("indicators", [pattern])
    hits = []
    if dry_run:
        print(f"[dry-run] crtsh pattern: {label} (q={pattern!r}, "
              f"issuer_filter={pat.get('issuer_filter')})", file=sys.stderr)
        return hits
    status, certs = _query(pattern)
    if status != 200 or certs is None:
        print(f"[crtsh] pattern {label!r}: HTTP {status}, skipped",
              file=sys.stderr)
        return hits
    if not isinstance(certs, list):
        print(f"[crtsh] pattern {label!r}: unexpected response shape",
              file=sys.stderr)
        return hits
    certs.sort(key=lambda c: (c.get("entry_timestamp") or ""), reverse=True)
    if len(certs) > result_cap:
        print(f"[crtsh] pattern {label!r}: {len(certs)} certs, "
              f"capped to newest {result_cap}", file=sys.stderr)
    else:
        print(f"[crtsh] pattern {label!r}: {len(certs)} certs",
              file=sys.stderr)
    for cert in certs[:result_cap]:
        serial = (cert.get("serial_number") or "").lower()
        if serial and serial == known_serial.lower():
            continue
        if needs_tencent and not _issuer_or_san_tencent(cert):
            continue
        cert_id = cert.get("id")
        key = f"crtsh:{cert_id}" if cert_id is not None else f"crtsh:{serial}"
        if not is_new(seen_ids, key):
            continue
        seen_at = (_parse_ts(cert.get("entry_timestamp"))
                   or _parse_ts(cert.get("not_before")))
        if seen_at is not None and seen_at < cutoff:
            continue
        sans = [s for s in (cert.get("name_value") or "").split("\n") if s]
        cn = cert.get("common_name") or ""
        # Exact match or suffix match only, never substring: a
        # substring match would fire on unrelated hostnames that
        # merely contain the marker string.
        direct_domain = any(
            s.lower() == "hysandbox.tencent-cloud.com"
            or s.lower().endswith(".hysandbox.tencent-cloud.com")
            for s in sans)
        indicators = list(indicators_base)
        if direct_domain:
            indicators.append("hysandbox.tencent-cloud.com SAN")
        if _issuer_or_san_tencent(cert):
            indicators.append("tencent-issuer-or-SAN")
        confidence = "HIGH" if direct_domain else "MEDIUM"
        observed = (cert.get("entry_timestamp") or cert.get("not_before")
                    or collected_at)
        hits.append(make_hit(
            lane=LANE,
            source_url=(f"{CRTSH_BASE}?id={cert_id}"
                        if cert_id is not None else CRTSH_BASE),
            indicators_matched=indicators,
            confidence=confidence,
            summary=f"[crtsh] {cn or (sans[0] if sans else '?')} — "
                    f"serial {serial or '?'} "
                    f"(not_before {cert.get('not_before')})",
            provenance={
                "method": "crt.sh Certificate Transparency search",
                "query": pattern,
                "pattern_label": label,
                "crtsh_id": cert_id,
                "serial_number": cert.get("serial_number"),
                "issuer": cert.get("issuer_name"),
                "not_before": cert.get("not_before"),
                "not_after": cert.get("not_after"),
                "entry_timestamp": cert.get("entry_timestamp"),
                "retrieved_at": collected_at,
            },
            observed_at=observed,
            extra={
                "serial": cert.get("serial_number"),
                "common_name": cn,
                "sans": sans,
                "issuer": cert.get("issuer_name"),
                "not_before": cert.get("not_before"),
                "not_after": cert.get("not_after"),
                "crtsh_id": cert_id,
                "pattern_label": label,
            },
            grade="SECONDARY",
        ))
        mark_seen(seen_ids, key)
    return hits


def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False):
    if not dry_run and not scanner_enabled("crtsh"):
        print("[crtsh] live scan refused: crtsh.enabled is not "
              "true in config.json (module ships disabled)",
              file=sys.stderr)
        raise SystemExit(2)
    cfg = load_config()
    if seen_ids is None:
        seen_ids = set()
    block = cfg.get("scanners", {}).get("crtsh", {})
    patterns = [p for p in block.get("patterns", [])
                if p.get("enabled", False)]
    known_serial = block.get("known_cert_serial", "")
    delay = float(block.get("rate_limit_seconds", 10))
    result_cap = int(block.get("result_cap", 500))
    collected_at = utcnow_iso()
    cutoff = (datetime.datetime.now(datetime.timezone.utc)
              - datetime.timedelta(hours=since_hours))
    if dry_run:
        print(f"[dry-run] crtsh: {len(patterns)} patterns planned "
              f"(window: last {since_hours}h)", file=sys.stderr)
    hits = []
    for i, pat in enumerate(patterns):
        if i > 0 and not dry_run:
            time.sleep(delay)
        try:
            hits.extend(scan_pattern(pat, cutoff, known_serial, seen_ids,
                                     collected_at, dry_run, result_cap))
        except RateLimited as e:
            print(f"[crtsh] {e} — aborting remaining patterns",
                  file=sys.stderr)
            break
        except Exception as e:
            print(f"[crtsh] pattern {pat.get('label')!r} failed: "
                  f"{type(e).__name__}: {e}", file=sys.stderr)
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    hits.sort(key=lambda h: (rank.get(h["confidence"], 3), h["summary"]))
    return hits


def main():
    args = parse_args("crt.sh certificate-transparency scanner "
                      "(Hermes port)")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
