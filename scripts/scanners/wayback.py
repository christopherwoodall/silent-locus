#!/usr/bin/env python3
"""Lane 7 — Wayback CDX scanner: Chinese Amap agent fleet.

Queries the Wayback Machine CDX API for NEW captures of fleet
infrastructure:

  - *.hysandbox.tencent-cloud.com (fleet proxy cert domain, matchType=domain)
  - pre-amap-pc-ssr.amap.com (pre-prod SSR host, matchType=prefix)
  - amap-pc-ssr.amap.com/ssr/place/* (fleet POI page targets, prefix)
  - amap-pc-ssr.amap.com/ssr/api/getPoiInfo* (fleet API target, prefix)

CRITICAL (per TOOLS.md): the CDX endpoint is
  http://web.archive.org/cdx/search/cdx
port 80, NOT 443 (443 times out through the egress proxy).
matchType=prefix takes a BARE prefix (no trailing '*').
The backend is flaky: on failure retry with 45-90 s spacing.

Prior baseline (2026-10-04): 115 fleet-shaped captures in the fleet window
(83% POI-ID overlap with the 217 fleet targets, peak-day burst, parallel
timing, zero baseline Sep 1-7). This module watches for NEW captures since
the last run: only captures with a timestamp inside --since-hours are
reported.

Passive only. Only the CDX index is queried; no archived pages are
fetched.

IP-classification note (standing rule): CDX rows carry no IP addresses
(fields: urlkey, timestamp, original, statuscode, digest, mimetype), so
wayback hits record no IPs and attach no ip_classification. If an IP
field is ever added to these hits, it must be classified via
_common.attach_ip_classification before this module ships.

Usage:
    wayback.py [--dry-run] [--since-hours 24] [--json]

Targets come from ~/workspace/silent-locus/scripts/swarm-infra-config.json
("wayback" block).
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
    is_new, mark_seen, parse_args, emit,
)

LANE = "wayback"
CDX_BASE = "http://web.archive.org/cdx/search/cdx"  # port 80, NOT 443
FIELDS = "urlkey,timestamp,original,statuscode,digest,mimetype"
LIMIT = 2000
RETRY_SLEEPS = (60, 90)  # TOOLS.md: 45-90 s spacing on flaky-backend failures


def _cdx(params: dict) -> tuple[int, list | None]:
    query = urllib.parse.urlencode(params)
    url = f"{CDX_BASE}?{query}"
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


def _cdx_with_retry(params: dict, label: str) -> list | None:
    for attempt, sleep_s in enumerate([0] + list(RETRY_SLEEPS)):
        if sleep_s:
            print(f"[wayback] {label}: retrying in {sleep_s}s "
                  f"(attempt {attempt + 1})", file=sys.stderr)
            time.sleep(sleep_s)
        status, data = _cdx(params)
        if status == 200 and data is not None:
            return data
        print(f"[wayback] {label}: HTTP {status}", file=sys.stderr)
    print(f"[wayback] {label}: giving up after "
          f"{1 + len(RETRY_SLEEPS)} attempts", file=sys.stderr)
    return None


def _cdx_timestamp_to_iso(ts: str) -> str:
    """'20261014120000' -> '2026-10-14T12:00:00Z'."""
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


def scan_target(target: dict, from_ts: str, seen_ids, collected_at: str,
                dry_run: bool) -> list:
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
        "limit": str(LIMIT),
    }
    hits = []

    if dry_run:
        print(f"[dry-run] wayback target: {label} "
              f"(url={target['url']!r}, matchType={target.get('matchType')}, "
              f"from={from_ts})", file=sys.stderr)
        return hits

    data = _cdx_with_retry(params, label)
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
        # COUNSEL FIX (adversarial 2026-10-14): anti-bot telemetry rows are
        # CUT as hit emission -- ~92% of baseline rows, fired by the
        # crawler's own page loads. Emitting classified noise is the
        # definition of a noisy scanner. Skip them entirely.
        if any(t in original for t in
               ("_____tmd_____", "punishTextFetch", "page/feedback")):
            continue
        # COUNSEL FIX (adversarial 2026-10-14): presence-only captures
        # DEMOTED HIGH->MEDIUM. A capture proves the crawler saw the URL,
        # not who asked; the real signal was burst shape, not presence.
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
            grade="PRIMARY",
        ))
        mark_seen(seen_ids, key)
    return hits


def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False):
    """Query CDX for new captures. Returns list of factum-ready hit dicts."""
    cfg = load_config()
    if seen_ids is None:
        seen_ids = set()
    targets = cfg.get("wayback", {}).get("targets", [])
    collected_at = utcnow_iso()
    from_ts = _cutoff_cdx(since_hours)

    hits = []
    for t in targets:
        try:
            hits.extend(scan_target(t, from_ts, seen_ids, collected_at,
                                    dry_run))
        except Exception as e:
            print(f"[wayback] target {t.get('label')!r} failed: "
                  f"{type(e).__name__}: {e}", file=sys.stderr)
        if not dry_run:
            time.sleep(5)  # polite spacing between CDX queries
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    hits.sort(key=lambda h: (rank.get(h["confidence"], 3), h["summary"]))
    return hits


def main():
    args = parse_args("Lane 7 — Wayback CDX scanner (Chinese Amap fleet)")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
