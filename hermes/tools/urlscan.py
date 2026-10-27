#!/usr/bin/env python3
"""urlscan.io scanner (Hermes port of lane 6).

Searches urlscan.io's public anonymous search API for fleet
fingerprints: getPoiInfo-shaped URLs, Amap/gaode domains, the
`uqscan=` / `uqframe=` tag markers, and the `hysandbox` proxy
marker.

API: https://urlscan.io/api/v1/search/?q=<query>&size=100
Anonymous limits (grounded 2026-10-04): results cover only the
last 30 days, leading-wildcard searches are blocked (403), and
full result bodies need a login. Verdicts rest on search metadata
only: URL, title, scan date.

Grade rule: urlscan hits are other people's scan metadata, so
they grade SECONDARY, always. No per-query override can ever
upgrade third-party metadata to PRIMARY. A scan record shows
that someone asked urlscan to scan a URL. It does not show
who asked, or why.

Port changes vs the source:
- Config: tools/config.json, resolved relative to this file.
  Queries come from its "urlscan" block.
- IP classification uses the vendored _common classifier
  (exact-IP and watchlist-CIDR tiers only; no live ASN lookup).
- State: none. Dedup uses the caller's seen_ids set.
- Captures: none in this module; hits carry the result URL.

Rate limit: about 1 request per 2 s between queries.

Usage: urlscan.py [--dry-run] [--since-hours 24] [--json]
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
    is_new, mark_seen, parse_args, emit, attach_ip_classification,
    scanner_enabled,
)

LANE = "urlscan"
SEARCH_BASE = "https://urlscan.io/api/v1/search/"
RESULT_PAGE = "https://urlscan.io/result/"
RARE_MARKERS = ("uqscan=", "uqframe=", "hysandbox")


def _search(query: str, size: int) -> tuple[int, dict | None]:
    url = (f"{SEARCH_BASE}?q={urllib.parse.quote(query, safe='')}"
           f"&size={size}")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        print(f"[urlscan] query {query!r} failed: {type(e).__name__}: {e}",
              file=sys.stderr)
        return -1, None


def _parse_date(iso: str) -> datetime.datetime | None:
    try:
        return datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except Exception:
        return None


def _match_fields(result: dict, indicators: list) -> tuple[list, list]:
    """Return (url-field matches, title-field matches), tracked
    separately. A title-only match is weaker than a URL match."""
    url_hay, title_hay = [], []
    for section in ("page", "task"):
        sec = result.get(section) or {}
        for field, hay in (("url", url_hay), ("title", title_hay)):
            v = sec.get(field)
            if v:
                hay.append(str(v).lower())
    url_matched = [i for i in indicators
                   if any(i.lower() in h for h in url_hay)]
    title_matched = [i for i in indicators
                     if any(i.lower() in h for h in title_hay)]
    return url_matched, title_matched


def _match_indicators(result: dict, indicators: list) -> list:
    url_matched, title_matched = _match_fields(result, indicators)
    out = list(url_matched)
    for i in title_matched:
        if i not in out:
            out.append(i)
    return out


def _cap(confidence: str, cap: str | None) -> str:
    if not cap:
        return confidence
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    if rank.get(confidence, 3) < rank.get(cap, 3):
        return cap
    return confidence


def scan_query(cfg_query: dict, cfg: dict, cutoff: datetime.datetime,
               seen_ids, collected_at: str, size: int,
               dry_run: bool = False) -> list:
    q = cfg_query["q"]
    indicators = cfg_query.get("indicators", [])
    label = cfg_query.get("label", q)
    hits = []
    if dry_run:
        # Port fix vs the source (whose dry-run still queried):
        # a dry run prints the plan and makes no network call.
        print(f"[dry-run] urlscan query: {label} (q={q!r})",
              file=sys.stderr)
        return hits
    status, data = _search(q, size)
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
            continue
        matched = _match_indicators(r, indicators)
        if not matched:
            continue
        url_matched, _title_matched = _match_fields(r, indicators)
        rare = any(m.lower() in RARE_MARKERS for m in matched)
        confidence = "HIGH" if (rare or len(matched) >= 2) else "MEDIUM"
        if not url_matched:
            # Title-only match: cap at MEDIUM, whatever the
            # marker rarity. The title field is weaker evidence.
            confidence = _cap(confidence, "MEDIUM")
        confidence = _cap(confidence, cfg_query.get("confidence_cap"))
        block_cap = (cfg.get("scanners", {}).get("urlscan", {})
                     .get("confidence_cap"))
        confidence = _cap(confidence, block_cap)
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
                    "time_basis": "upstream scan time",
                    "scan_uuid": uuid,
                    "page_url": page_url,
                    "page_title": title,
                    "page_domain": page.get("domain"),
                    "page_ip": page.get("ip"),
                    "page_asn_provider_context_unvalidated":
                        page.get("asn"),
                    "page_asn_note": "unvalidated provider "
                        "context, never a tier input",
                    "screenshot_url": r.get("screenshot"),
                    "result_api_url": r.get("result"),
                },
                grade="SECONDARY",
            ),
            page.get("ip"), cfg,
        ))
        mark_seen(seen_ids, key)
    return hits


def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False):
    if not dry_run and not scanner_enabled("urlscan"):
        print("[urlscan] live scan refused: urlscan.enabled is not "
              "true in config.json (module ships disabled)",
              file=sys.stderr)
        raise SystemExit(2)
    cfg = load_config()
    if seen_ids is None:
        seen_ids = set()
    block = cfg.get("scanners", {}).get("urlscan", {})
    queries = block.get("queries", [])
    skipped = [q.get("q") for q in queries if not q.get("enabled", False)]
    queries = [q for q in queries if q.get("enabled", False)]
    collected_at = utcnow_iso()
    cutoff = (datetime.datetime.now(datetime.timezone.utc)
              - datetime.timedelta(hours=since_hours))
    delay = float(block.get("rate_limit_seconds", 2))
    size = int(block.get("size", 100))
    if dry_run:
        print(f"[dry-run] urlscan: {len(queries)} queries planned "
              f"(window: last {since_hours}h)", file=sys.stderr)
        for cq in queries:
            print(f"  q={cq['q']!r} indicators={cq.get('indicators')}",
                  file=sys.stderr)
        for q in skipped:
            print(f"  (disabled) {q!r}", file=sys.stderr)
    hits = []
    for i, cq in enumerate(queries):
        if i > 0 and not dry_run:
            time.sleep(delay)
        try:
            hits.extend(scan_query(cq, cfg, cutoff, seen_ids,
                                   collected_at, size, dry_run))
        except Exception as e:
            print(f"[urlscan] query {cq.get('q')!r} failed: "
                  f"{type(e).__name__}: {e}", file=sys.stderr)
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    hits.sort(key=lambda h: (rank.get(h["confidence"], 3), h["summary"]))
    return hits


def main():
    args = parse_args("urlscan.io scanner (Hermes port)")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
