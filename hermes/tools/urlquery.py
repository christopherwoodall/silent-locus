#!/usr/bin/env python3
"""urlquery scanner (Hermes port of lane 1).

Passive watch over urlquery.net for new agent-fleet reports.

What it does:
1. Runs urlquery API searches over a date window (tag grammar,
   Amap/gaode targeting, httpbin /base64/ payloads, webhook.site
   and ntfy.sh exfil shapes, pre-prod hosts, zz= launcher marker).
2. Scores each returned report LOCALLY by indicator weight. A
   report becomes a hit only at weight 3 or more. Weight-0
   indicators never drive emission.
3. Emits hit dicts, grade SECONDARY: it polls other people's
   submissions. Polling an API ourselves does not make someone
   else's submission our own observation. Confidence is capped
   at MEDIUM.

Port changes vs the source:
- Transport: the source used a vault-backed CLI. This port calls
  the urlquery search API directly with a key read at run time
  from the env var named in config (api_key_env). No key set
  means no network call: every query is skipped with a warning.
  No secret value is stored anywhere.
- Config: tools/config.json, resolved relative to this file.
  The known submitter id from the source config is NOT carried
  over: the report API exposes no submitter field, so it cannot
  be a live rule, and this profile never tracks submitter identity.
- State: none. Dedup uses the caller's seen_ids set.
- `q` matches submitted URLs AND page content. Local scoring
  uses submitted URL, final URL, tags, and title only. Never
  trust the raw API hit count: a `zz=` search also matches
  country_code "zz" rows, and a bare `ntfy` search returns
  page-content noise.

Usage: urlquery.py [--dry-run] [--since-hours 24] [--json]
"""
from __future__ import annotations

import datetime
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C

LANE = "urlquery"


def _date_filter(since_hours: float) -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    since = now - datetime.timedelta(hours=since_hours)
    return f"date:[{since.strftime('%Y-%m-%d')} TO {now.strftime('%Y-%m-%d')}]"


def _search(block: dict, api_key: str, query: str,
            limit: int) -> list:
    """One urlquery API search. Returns report rows; [] on failure."""
    base = block.get("api_base", "https://api.urlquery.net/v1")
    url = f"{base}/search?{urllib.parse.urlencode({'q': query, 'limit': limit})}"
    req = urllib.request.Request(url, headers={
        "User-Agent": C.USER_AGENT,
        "Authorization": f"Bearer {api_key}",
    })
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"  [warn] urlquery search HTTP {e.code}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"  [warn] urlquery search failed: {type(e).__name__}: {e}",
              file=sys.stderr)
        return []
    if not isinstance(data, dict):
        return []
    return data.get("reports") or []


def _submitted_url(row: dict) -> str:
    su = (row.get("submit") or {}).get("url") or {}
    schema, addr = su.get("schema", "http"), su.get("addr", "")
    return f"{schema}://{addr}" if addr else ""


def _score_row(row: dict, indicators: list) -> tuple[list, int]:
    tags = row.get("tags") or []
    final = row.get("final") or {}
    final_url = ((final.get("url") or {}).get("addr")) or ""
    final_title = final.get("title") or ""
    haystack = "\n".join([_submitted_url(row), final_url, final_title,
                          " ".join(tags)])
    matched, weight = [], 0
    for name, w, rx in indicators:
        if rx.search(haystack):
            matched.append(name)
            weight += w
    return matched, weight


def _confidence(weight: int) -> str:
    # Capped at MEDIUM: this scanner polls other people's
    # submissions, so no hit may claim HIGH confidence.
    return "MEDIUM"


def _cap(confidence: str, cap: str | None) -> str:
    if not cap:
        return confidence
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    if rank.get(confidence, 3) < rank.get(cap, 3):
        return cap
    return confidence


def _make_hit(row: dict, matched: list, weight: int, rule: str,
              query: str, scanned_at: str, config: dict) -> dict:
    report_id = row["report_id"]
    ip = row.get("ip") or {}
    final = row.get("final") or {}
    block_cap = (config.get("scanners", {}).get("urlquery", {})
                 .get("confidence_cap"))
    hit = C.make_hit(
        lane=LANE,
        observed_at=row.get("date") or scanned_at,
        source_url=f"https://urlquery.net/report/{report_id}",
        indicators_matched=matched,
        confidence=_cap(_confidence(weight), block_cap),
        summary=(f"urlquery report {report_id[:8]}: "
                 f"{len(matched)} indicators ({', '.join(matched)}) "
                 f"weight={weight} on {_submitted_url(row)[:80]}"),
        provenance={
            "method": "urlquery api search (key from env var)",
            "query": query,
            "rule": rule,
            "indicator_weight": weight,
            "scanned_at": scanned_at,
        },
        grade="SECONDARY",
        extra={
            "report_id": report_id,
            "submitted_url": _submitted_url(row),
            "report_date": row.get("date"),
            "target_ip": ip.get("addr"),
            "target_asn_provider_context_unvalidated": ip.get("asn"),
            "target_asn_note": "unvalidated provider context, "
                "never a tier input",
            "target_country": ip.get("country"),
            "final_title": final.get("title"),
            "report_tags": row.get("tags") or [],
        },
    )
    return C.attach_ip_classification(hit, ip.get("addr"), config)


def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False):
    if not dry_run and not C.scanner_enabled("urlquery"):
        print("[urlquery] live scan refused: urlquery.enabled is "
              "not true in config.json (module ships disabled)",
              file=sys.stderr)
        raise SystemExit(2)
    hits = []
    config = C.load_config()
    block = config.get("scanners", {}).get("urlquery", {})
    families = block.get("query_families", [])
    indicators = []
    for ind in block.get("indicators", []):
        try:
            indicators.append((ind["name"], int(ind["weight"]),
                               re.compile(ind["regex"], re.IGNORECASE)))
        except (KeyError, re.error, ValueError) as e:
            print(f"  [warn] bad indicator {ind}: {e}", file=sys.stderr)
    threshold = int(block.get("hit_threshold_weight", 3))
    delay = float(block.get("rate_limit_seconds", 3))
    limit = int(block.get("limit_per_query", 30))
    datef = _date_filter(since_hours)
    scanned_at = C.utcnow_iso()

    if dry_run:
        print("[dry-run] urlquery scan plan")
        print(f"  window: last {since_hours}h -> {datef}")
        for fam in families:
            print(f"  WOULD search: [{fam.get('family')}] "
                  f"{fam.get('query')} {datef} (rule: {fam.get('rule')})")
        for name, w, rx in indicators:
            print(f"    {name:14s} w={w}  {rx.pattern}")
        return hits

    api_key = C.resolve_env(block.get("api_key_env"))
    if not api_key:
        print("[urlquery] no API key env var set "
              f"({block.get('api_key_env')}); skipping all queries, "
              "no network calls made", file=sys.stderr)
        return hits

    seen_reports = set()
    for fam in families:
        query = f"{fam.get('query')} {datef}"
        rows = _search(block, api_key, query, limit)
        time.sleep(delay)
        for row in rows:
            rid = row.get("report_id")
            if not rid or rid in seen_reports:
                continue
            seen_reports.add(rid)
            matched, weight = _score_row(row, indicators)
            if weight < threshold:
                continue
            key = f"urlquery:{rid}"
            if C.is_new(seen_ids, key):
                C.mark_seen(seen_ids, key)
                hits.append(_make_hit(row, matched, weight,
                                     fam.get("rule", ""), query,
                                     scanned_at, config))
    hits.sort(key=lambda h: (-h["provenance"]["indicator_weight"],
                            h["observed_at"]))
    print(f"lane-1: {len(seen_reports)} reports screened, "
          f"{len(hits)} hits", file=sys.stderr)
    return hits


def main():
    args = C.parse_args("urlquery.net agent-fleet watch (Hermes port)")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    C.emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
