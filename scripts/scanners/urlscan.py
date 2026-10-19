#!/usr/bin/env python3
"""Lane 6 — urlscan.io scanner: Chinese Amap agent fleet.

Searches urlscan.io's public anonymous search API for fleet fingerprints:

  getPoiInfo-shaped URLs, Amap/gaode domains in page URLs, the fleet's
  `uqscan=` / `uqframe=` tag markers, and the `hysandbox` proxy marker.

API: https://urlscan.io/api/v1/search/?q=<query>&size=100
Anonymous limits (grounded 2026-10-04): results limited to the last
30 days, leading-wildcard searches blocked (403), full result bodies
require login — verdicts rest on search metadata (URL, title, date).
Screenshots are reachable anonymously: https://urlscan.io/screenshots/<uuid>.png

Prior sweep (2026-10-04) was an honest zero for every fleet fingerprint;
this module exists to catch NEW appearances (fleet pages newly submitted
to urlscan.io, or staging patterns moving off httpbun).

Passive only. Rate limit: ~1 request / 2 s between queries.

Standing rule: every recorded IP (page_ip from urlscan metadata) is
classified via ip_classifier and attached as hit["ip_classification"];
tier 1/2 hits get hit["priority"] = True.

Usage:
    urlscan.py [--dry-run] [--since-hours 24] [--json]

Queries come from ~/workspace/silent-locus/scripts/swarm-infra-config.json
("urlscan" block).
"""
from __future__ import annotations

import datetime
import os
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    USER_AGENT, load_config, make_hit, utcnow_iso,
    is_new, mark_seen, parse_args, emit, attach_ip_classification,
)
import urllib.request
import urllib.error
import json

LANE = "urlscan"
SEARCH_BASE = "https://urlscan.io/api/v1/search/"
RESULT_PAGE = "https://urlscan.io/result/"  # + uuid + /
REQUEST_DELAY = 2.0  # polite: ~1 request per 2 s
SIZE = 100  # one page per query; results are newest-first

# Indicators that, alone, make a hit HIGH confidence (rare fleet markers).
RARE_MARKERS = ("uqscan=", "uqframe=", "hysandbox")


def _search(query: str) -> tuple[int, dict | None]:
    url = (f"{SEARCH_BASE}?q={urllib.parse.quote(query, safe='')}"
           f"&size={SIZE}")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:  # network/DNS/proxy failure
        print(f"[urlscan] query {query!r} failed: {type(e).__name__}: {e}",
              file=sys.stderr)
        return -1, None


def _parse_date(iso: str) -> datetime.datetime | None:
    try:
        return datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except Exception:
        return None


def _match_indicators(result: dict, indicators: list) -> list:
    """Substring-match each indicator against URL/title fields (case-ins)."""
    haystacks = []
    for section in ("page", "task"):
        sec = result.get(section) or {}
        for field in ("url", "title"):
            v = sec.get(field)
            if v:
                haystacks.append(str(v).lower())
    matched = [i for i in indicators if any(i.lower() in h for h in haystacks)]
    return matched


def scan_query(cfg_query: dict, cfg: dict, cutoff: datetime.datetime,
               seen_ids, dry_run: bool, collected_at: str) -> list:
    q = cfg_query["q"]
    indicators = cfg_query.get("indicators", [])
    label = cfg_query.get("label", q)
    hits = []

    status, data = _search(q)
    if status != 200 or data is None:
        print(f"[urlscan] query {q!r}: HTTP {status}, skipped",
              file=sys.stderr)
        return hits

    total = data.get("total", 0)
    results = data.get("results", [])
    print(f"[urlscan] query {q!r}: {total} total, {len(results)} fetched",
          file=sys.stderr)

    for r in results:
        uuid = r.get("_id") or (r.get("task") or {}).get("uuid")
        if not uuid:
            continue
        key = f"urlscan:{uuid}"
        if not is_new(seen_ids, key):
            continue
        scan_date = _parse_date((r.get("task") or {}).get("time", ""))
        if scan_date is not None and scan_date < cutoff:
            continue  # older than the look-back window
        matched = _match_indicators(r, indicators)
        if not matched:
            continue
        rare = any(m.lower() in RARE_MARKERS for m in matched)
        confidence = "HIGH" if (rare or len(matched) >= 2) else "MEDIUM"
        # counsel: respect per-query confidence cap (adversarial DEMOTE)
        cap = cfg_query.get("confidence_cap")
        if cap:
            rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
            if rank.get(confidence, 3) < rank.get(cap, 3):
                confidence = cap
        page = r.get("page") or {}
        task = r.get("task") or {}
        page_url = page.get("url") or task.get("url") or ""
        title = page.get("title") or ""
        hits.append(attach_ip_classification(
            make_hit(
                lane=LANE,
                source_url=f"{RESULT_PAGE}{uuid}/",
                indicators_matched=matched + [f"query:{label}"],
                confidence=confidence,
                summary=f"[urlscan] {page_url[:120]} — {', '.join(matched)}"
                        + (f" [{title[:60]}]" if title else ""),
                provenance={
                    "method": "urlscan.io anonymous search API",
                    "query": q,
                    "scan_uuid": uuid,
                    "scan_time": task.get("time"),
                    "retrieved_at": collected_at,
                },
                observed_at=(task.get("time") or collected_at),
                extra={
                    "scan_uuid": uuid,
                    "page_url": page_url,
                    "page_title": title,
                    "page_domain": page.get("domain"),
                    "page_ip": page.get("ip"),
                    "page_asn": page.get("asn"),
                    "screenshot_url": r.get("screenshot"),
                    "result_api_url": r.get("result"),
                },
                grade="PRIMARY",
            ),
            page.get("ip"), cfg,
        ))
        mark_seen(seen_ids, key)
    return hits


def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False):
    """Run all urlscan queries. Returns list of factum-ready hit dicts."""
    cfg = load_config()
    if seen_ids is None:
        seen_ids = set()
    queries = cfg.get("urlscan", {}).get("queries", [])
    # counsel: skip disabled queries (adversarial CUT verdicts)
    queries = [q for q in queries if q.get("enabled", True)]
    if dry_run:
        queries = queries[:3]
    collected_at = utcnow_iso()
    cutoff = (datetime.datetime.now(datetime.timezone.utc)
              - datetime.timedelta(hours=since_hours))

    if dry_run:
        print(f"[dry-run] urlscan: {len(queries)} queries planned "
              f"(window: last {since_hours}h, cutoff {cutoff.isoformat()}):",
              file=sys.stderr)
        for cq in queries:
            print(f"  q={cq['q']!r} indicators={cq.get('indicators')}",
                  file=sys.stderr)

    hits = []
    for i, cq in enumerate(queries):
        if i > 0:
            time.sleep(REQUEST_DELAY)
        try:
            hits.extend(scan_query(cq, cfg, cutoff, seen_ids, dry_run,
                                   collected_at))
        except Exception as e:
            print(f"[urlscan] query {cq.get('q')!r} failed: "
                  f"{type(e).__name__}: {e}", file=sys.stderr)
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    hits.sort(key=lambda h: (rank.get(h["confidence"], 3), h["summary"]))
    return hits


def main():
    args = parse_args("Lane 6 — urlscan.io scanner (Chinese Amap fleet)")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
