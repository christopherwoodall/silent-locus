#!/usr/bin/env python3
"""Lane 1: urlquery.net scanner for Chinese Amap agent-fleet tradecraft.

Passive-only watch over urlquery.net for NEW fleet reports.

What it does:
  1. Runs a small set of urlquery API searches over a 24h date window
     (tag grammar x Amap targeting, Amap/gaode domains, httpbin /base64/
     payloads, webhook.site + ntfy.sh exfil patterns, pre-prod Amap hosts).
  2. Scores every returned report LOCALLY by indicator conjunction --
     a report becomes a hit only when >= 2 indicator families co-occur
     (single-family matches never emit; see FALSE-POSITIVES-urlquery.md).
  3. Emits factum-ready hit dicts (grade PRIMARY: we polled the API
     ourselves and scored the returned rows).

Transport: the authenticated api.urlquery.net search endpoint via the
installed urlquery skill CLI (~/workspace/skills/urlquery/bin/uq.py),
which handles the Secure Vault surrogate credential. The keyless htmx
search endpoint is NOT used for the primary scan: per the skill docs,
htmx search silently misses known-live records (weak negatives), so it
cannot carry a "new reports" watch. The API search is 429-throttled;
we keep the query count small (~11) and space calls ~3s apart.

Contract:
    scan(since_hours=24, seen_ids=None, dry_run=False) -> list[dict]

CLI:
    urlquery.py [--since-hours N] [--dry-run] [--json]

Notes:
  - The known fleet submitter id (akbkyowd9geqr98) is documented in
    config but CANNOT be a live detection rule: the urlquery report API
    exposes no submitter field (verified 2026-10-14). Kept for context.
  - `q` in urlquery search syntax matches submitted URLs (never page
    content). Space = implicit AND (established pattern in
    scripts/swarm-infra-crawler.py).
"""
from __future__ import annotations

import datetime
import json
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _common as C
from ip_classifier import classify_ip

LANE = "urlquery-amap-watch"
UQ_CLI = os.path.expanduser("~/workspace/skills/urlquery/bin/uq.py")
IP_CACHE_PATH = os.path.expanduser(
    "~/workspace/silent-locus/scripts/scanners/state/ip_asn_cache.json")
DELAY = 3.0  # polite spacing; API is 429-throttled
LIMIT_PER_QUERY = 30
HIT_THRESHOLD = 3  # minimum combined indicator weight

# Indicator regexes applied LOCALLY to (submitted URL + tags + final title).
# weight: tag grammar is weak alone (benign scanners use it too), the
# targeting/payload/exfil families are the discriminating signal.
# COUNSEL FIXES (2026-10-14):
#  - linguist H1: label_grammar tightened (was matching plain "researchers")
#  - adversarial: label_grammar CUT as emission driver (weight 0) -- labels
#    are claims, not evidence; thousands of honest agents collide
#  - cryptologist: uqtag= added (was in config but missing from regex)
INDICATORS = [
    ("tag_grammar", 1, re.compile(r"(uqscan=|uqframe=|uqtag=|cachebust=1|[?&]uq=)")),
    ("amap_target", 2, re.compile(r"(amap\.com|gaode\.com)", re.IGNORECASE)),
    ("preprod_host", 1, re.compile(r"pre-amap-pc-ssr\.amap\.com", re.IGNORECASE)),
    ("httpbin_base64", 2,
     re.compile(r"httpbin\.org/base64/[A-Za-z0-9+/=]{40,}")),
    ("webhook_site", 1,
     re.compile(r"webhook\.site/[a-f0-9]{8}-[a-f0-9-]{27}")),
    ("ntfy_amapdata", 2, re.compile(r"ntfy\.sh/amapdata[-\w]*")),
    # A6 2026-10-20: zz= is the OAI-launcher marker; weight 3 drives emission
    # on its own so the query family is not screened-but-silent.
    ("zz_launcher", 3, re.compile(r"(?<![a-z0-9_])zz=")),
    # weight 0: logged for context but NEVER drives emission alone
    ("label_grammar", 0,
     re.compile(r"(claude20\d{6,}|\bresearch[-_][a-z0-9]{4,}\b)", re.IGNORECASE)),
    # cryptologist: flag non-standard Via proxy labels (the hysandbox-ats
    # method). Partial: only fires when row carries header data; full
    # implementation needs per-report detail fetch (TODO).
    ("via_anomaly", 2,
     re.compile(r"via[:\s]+[^\n]*?(sandbox|ats|proxy-[a-z0-9]{4,})", re.IGNORECASE)),
]

# Query families. Each gets " date:[YYYY-MM-DD TO YYYY-MM-DD]" appended.
# family -> (query, detection-rule-name)
QUERY_FAMILIES = [
    ("tag-grammar", "uqscan= amap", "tag x amap"),
    ("tag-grammar", "uqscan= gaode", "tag x gaode"),
    ("tag-grammar", "uqframe= amap", "tagframe x amap"),
    ("tag-grammar", "cachebust=1 amap", "cachebust x amap"),
    ("tag-grammar", "zz=", "zz launcher marker x 24h"),
    ("amap-targeting", "url.domain:amap.com", "amap domain"),
    ("amap-targeting", "url.domain:gaode.com", "gaode domain"),
    ("preprod", "pre-amap-pc-ssr", "pre-prod host"),
    ("payload", "httpbin.org/base64", "httpbin base64 payload"),
    ("exfil", "webhook.site amap", "webhook exfil x amap"),
    ("exfil", "webhook.site uqscan", "webhook exfil x tag"),
    ("exfil", "ntfy.sh/amapdata", "ntfy amapdata topic"),
]


def _date_filter(since_hours: float) -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    since = now - datetime.timedelta(hours=since_hours)
    return f"date:[{since.strftime('%Y-%m-%d')} TO {now.strftime('%Y-%m-%d')}]"


def _search(query: str, limit: int = LIMIT_PER_QUERY) -> list:
    """One urlquery API search. Returns report rows; [] on any failure."""
    proc = subprocess.run(
        [sys.executable, UQ_CLI, "search",
         "--query", query, "--limit", str(limit)],
        capture_output=True, text=True, timeout=180,
    )
    if proc.returncode != 0:
        print(f"  [warn] uq.py search failed: {proc.stderr[:200]}",
              file=sys.stderr)
        return []
    try:
        data = json.loads(proc.stdout)
    except (json.JSONDecodeError, AttributeError):
        print("  [warn] uq.py returned unparsable output", file=sys.stderr)
        return []
    # the API sometimes returns literal null (observed on /recent/) or
    # "reports": null -- both mean "no rows", not an error
    if not isinstance(data, dict):
        return []
    return data.get("reports") or []


def _submitted_url(row: dict) -> str:
    su = (row.get("submit") or {}).get("url") or {}
    schema, addr = su.get("schema", "http"), su.get("addr", "")
    return f"{schema}://{addr}" if addr else ""


def _score_row(row: dict) -> tuple[list, int]:
    """Score one search-result row. Returns (matched indicator names, weight)."""
    tags = row.get("tags") or []
    final = row.get("final") or {}
    final_url = ((final.get("url") or {}).get("addr")) or ""
    final_title = final.get("title") or ""
    haystack = "\n".join([_submitted_url(row), final_url, final_title,
                          " ".join(tags)])
    matched, weight = [], 0
    for name, w, rx in INDICATORS:
        if rx.search(haystack):
            matched.append(name)
            weight += w
    return matched, weight


def _confidence(weight: int) -> str:
    if weight >= 6:
        return "HIGH"
    return "MEDIUM"  # threshold 3..5


def _classify_ip(target_ip: str | None, config: dict) -> dict | None:
    """Standing rule: every IP recorded on a hit gets classified.

    Returns the classify_ip dict, or None when there is no IP to
    classify. Classifier errors degrade to tier-4 UNKNOWN, never crash
    the scan."""
    if not target_ip:
        return None
    try:
        return classify_ip(target_ip, config, IP_CACHE_PATH)
    except Exception as e:  # noqa: BLE001 - degrade, don't crash
        print(f"  [warn] ip classification failed for {target_ip}: {e}",
              file=sys.stderr)
        return {"ip": target_ip, "tier": 4, "label": "UNKNOWN",
                "detail": f"classifier error: {e}", "asn": None,
                "org": None, "country": None, "city": None,
                "swarm_linked": False}


def _make_hit(row: dict, matched: list, weight: int,
              rule: str, query: str, scanned_at: str, config: dict) -> dict:
    report_id = row["report_id"]
    ip = row.get("ip") or {}
    final = row.get("final") or {}
    summary = (f"urlquery report {report_id[:8]}: "
               f"{len(matched)} indicators ({', '.join(matched)}) "
               f"weight={weight} on {_submitted_url(row)[:80]}")
    hit = C.make_hit(
        lane=LANE,
        observed_at=row.get("date") or scanned_at,
        source_url=f"https://urlquery.net/report/{report_id}",
        indicators_matched=matched,
        confidence=_confidence(weight),
        summary=summary,
        provenance={
            "method": "urlquery api search (authenticated, via uq.py)",
            "query": query,
            "rule": rule,
            "indicator_weight": weight,
            "scanned_at": scanned_at,
        },
        grade="PRIMARY",
        extra={
            "report_id": report_id,
            "submitted_url": _submitted_url(row),
            "report_date": row.get("date"),
            "target_ip": ip.get("addr"),
            "target_asn": ip.get("asn"),
            "target_country": ip.get("country"),
            "final_title": final.get("title"),
            "submitter_tags": row.get("tags") or [],
        },
    )
    ip_class = _classify_ip(ip.get("addr"), config)
    if ip_class:
        hit["ip_classification"] = ip_class
        # A cloud IP where you don't expect one is signal: flag it.
        if ip_class.get("tier") in (1, 2):
            hit["priority"] = True
    return hit


def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False):
    """Run the lane-1 urlquery watch.

    since_hours: look-back window (default 24). date filter is day-granular.
    seen_ids: optional set for dedup (keys "urlquery:<report_id>").
    dry_run: print what WOULD be queried; hit no network.
    """
    hits = []
    datef = _date_filter(since_hours)
    scanned_at = C.utcnow_iso()
    config = C.load_config()  # for ip_classifier

    if dry_run:
        print("[dry-run] urlquery.net lane-1 scan plan")
        print(f"  window: last {since_hours}h -> {datef}")
        for family, q, rule in QUERY_FAMILIES:
            print(f"  WOULD search: [{family}] {q} {datef}  (rule: {rule})")
        print("  indicator regexes (local scoring, hit threshold "
              f"weight>={HIT_THRESHOLD}):")
        for name, w, rx in INDICATORS:
            print(f"    {name:14s} w={w}  {rx.pattern}")
        return hits

    seen_reports = set()
    for family, q, rule in QUERY_FAMILIES:
        query = f"{q} {datef}"
        rows = _search(query)
        time.sleep(DELAY)
        for row in rows:
            rid = row.get("report_id")
            if not rid or rid in seen_reports:
                continue
            seen_reports.add(rid)
            matched, weight = _score_row(row)
            if weight < HIT_THRESHOLD:
                continue
            key = f"urlquery:{rid}"
            if C.is_new(seen_ids, key):
                C.mark_seen(seen_ids, key)
                hits.append(_make_hit(row, matched, weight, rule,
                                     query, scanned_at, config))

    hits.sort(key=lambda h: (-h["provenance"]["indicator_weight"],
                            h["observed_at"]))
    print(f"lane-1: {len(seen_reports)} reports screened, "
          f"{len(hits)} hits", file=sys.stderr)
    return hits


def main():
    args = C.parse_args("Lane 1: urlquery.net Amap fleet watch")
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    C.emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
