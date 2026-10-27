#!/usr/bin/env python3
"""Wayback CDX scanner (Hermes port of lane 7).

Queries the Wayback Machine CDX API for NEW captures of fleet
infrastructure: the hysandbox proxy domain, the pre-prod Amap
host, fleet POI pages and the getPoiInfo API path, the jina
reader domain, and paste archives.

CRITICAL: the CDX endpoint is http://web.archive.org/cdx/search/cdx
(port 80, NOT 443: 443 times out through the egress proxy).
matchType=prefix takes a BARE prefix (no trailing '*').
The backend is flaky: on failure retry with 45-90 s spacing.

Only captures inside --since-hours are reported. Anti-bot
telemetry rows (_____tmd_____, punishTextFetch, page/feedback)
are skipped, not emitted: they are the crawler's own page loads,
not fleet signal. Presence-only captures grade MEDIUM at most:
a capture proves the crawler saw the URL, not who asked.

Passive only. Only the CDX index is queried. No archived page
is fetched. CDX rows carry no IP, so no IP classification.

Port changes vs the source: config from tools/config.json
(relative to this file); targets from its "wayback" block;
no silent-locus paths; no other change to query logic.

Usage: wayback.py [--dry-run] [--since-hours 24] [--json]
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

LANE = "wayback"
FIELDS = "urlkey,timestamp,original,statuscode,digest,mimetype"
TELEMETRY_MARKERS = ("_____tmd_____", "punishTextFetch", "page/feedback")


def _cdx(cdx_base: str, params: dict) -> tuple[int, list | None]:
    query = urllib.parse.urlencode(params)
    url = f"{cdx_base}?{query}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        print(f"[wayback] CDX request failed: {type(e).__name__}: {e}",
              file=sys.stderr)
        return -1, None


def _cdx_with_retry(cdx_base: str, params: dict, label: str,
                    retry_sleeps: list) -> list | None:
    for attempt, sleep_s in enumerate([0] + list(retry_sleeps)):
        if sleep_s:
            print(f"[wayback] {label}: retrying in {sleep_s}s "
                  f"(attempt {attempt + 1})", file=sys.stderr)
            time.sleep(sleep_s)
        status, data = _cdx(cdx_base, params)
        if status == 200 and data is not None:
            return data
        print(f"[wayback] {label}: HTTP {status}", file=sys.stderr)
    print(f"[wayback] {label}: giving up after "
          f"{1 + len(retry_sleeps)} attempts", file=sys.stderr)
    return None


def _cdx_timestamp_to_iso(ts: str) -> str:
    try:
        dt = datetime.datetime.strptime(ts[:14], "%Y%m%d%H%M%S")
        return dt.replace(tzinfo=datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return ts


def _cutoff_cdx(since_hours: float) -> str:
    dt = (datetime.datetime.now(datetime.timezone.utc)
          - datetime.timedelta(hours=since_hours))
    return dt.strftime("%Y%m%d%H%M%S")


def scan_target(block: dict, target: dict, from_ts: str, seen_ids,
                collected_at: str, dry_run: bool) -> list:
    label = target.get("label", target["url"])
    indicators = target.get("indicators", [target["url"]])
    params = {
        "url": target["url"],
        "matchType": target.get("matchType", "prefix"),
        "output": "json",
        "fl": FIELDS,
        "from": from_ts,
        "filter": "statuscode:200",
        "collapse": "urlkey",
        "limit": str(int(block.get("limit", 2000))),
    }
    hits = []
    if dry_run:
        print(f"[dry-run] wayback target: {label} "
              f"(url={target['url']!r}, matchType={target.get('matchType')}, "
              f"from={from_ts})", file=sys.stderr)
        return hits
    data = _cdx_with_retry(block.get("cdx_base", ""),
                           params, label,
                           block.get("retry_sleeps", [60, 90]))
    if data is None:
        return hits
    rows = data[1:] if data and isinstance(data[0], list) else data
    print(f"[wayback] {label}: {len(rows)} captures since {from_ts}",
          file=sys.stderr)
    for row in rows:
        if not isinstance(row, list) or len(row) < 5:
            continue
        urlkey, ts, original, statuscode, digest = row[:5]
        key = f"wayback:{urlkey}:{ts}"
        if not is_new(seen_ids, key):
            continue
        mimetype = row[5] if len(row) > 5 else ""
        observed = _cdx_timestamp_to_iso(ts)
        if any(t in original for t in TELEMETRY_MARKERS):
            continue
        hits.append(make_hit(
            lane=LANE,
            source_url=f"https://web.archive.org/web/{ts}id_/{original}",
            indicators_matched=list(indicators),
            confidence="MEDIUM",
            summary=f"[wayback] {original[:140]} — capture {observed}",
            provenance={
                "method": "Wayback Machine CDX API (port 80)",
                "target": target["url"],
                "matchType": target.get("matchType"),
                "capture_timestamp": ts,
                "statuscode": statuscode,
                "digest": digest,
                "retrieved_at": collected_at,
            },
            observed_at=observed,
            extra={
                "capture_url": original,
                "capture_timestamp": ts,
                "statuscode": statuscode,
                "digest": digest,
                "mimetype": mimetype,
                "target_label": label,
            },
            grade="SECONDARY",
        ))
        mark_seen(seen_ids, key)
    return hits


def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False):
    if not dry_run and not scanner_enabled("wayback"):
        print("[wayback] live scan refused: wayback.enabled is not "
              "true in config.json (module ships disabled)",
              file=sys.stderr)
        raise SystemExit(2)
    cfg = load_config()
    if seen_ids is None:
        seen_ids = set()
    block = cfg.get("scanners", {}).get("wayback", {})
    targets = block.get("targets", [])
    collected_at = utcnow_iso()
    from_ts = _cutoff_cdx(since_hours)
    delay = float(block.get("rate_limit_seconds", 5))
    hits = []
    for t in targets:
        try:
            hits.extend(scan_target(block, t, from_ts, seen_ids,
                                    collected_at, dry_run))
        except Exception as e:
            print(f"[wayback] target {t.get('label')!r} failed: "
                  f"{type(e).__name__}: {e}", file=sys.stderr)
        if not dry_run:
            time.sleep(delay)
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    hits.sort(key=lambda h: (rank.get(h["confidence"], 3), h["summary"]))
    return hits


def main():
    args = parse_args("Wayback CDX scanner (Hermes port)")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
