#!/usr/bin/env python3
"""urlquery htmx API CLI (undocumented public endpoint, no auth needed).

Mirrors uq.py's search interface but hits the website's htmx endpoint,
which is rate-limited separately from api.urlquery.net.

Usage:
    uq_htmx.py search --query QUERY [--limit N] [--offset N]

Outputs JSON: {"reports": [{"report_id","url","ip","country","date"}...]}.
Be polite: sleep between calls; the site will throttle aggressive use.
"""
import argparse
import html as htmlmod
import json
import re
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://urlquery.net"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "HX-Request": "true",
    "Accept": "text/html",
}


def fetch(path, current_url):
    h = dict(HEADERS)
    h["HX-Current-URL"] = current_url
    req = urllib.request.Request(BASE + path, headers=h)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", "replace")


def parse_reports(page_html):
    reports = []
    # each row has href="/report/<id>" ... >submitted-url</a>
    rows = re.findall(
        r'href="/report/([a-f0-9-]{8,36})"[^>]*>([^<]{1,300})</a>', page_html
    )
    seen = set()
    for rid, url in rows:
        if rid in seen:
            continue
        seen.add(rid)
        reports.append({
            "report_id": rid,
            "url": htmlmod.unescape(url.strip()),
        })
    # dates appear as "2026-10-04 20:12" in row order
    dates = re.findall(r'(20\d\d-\d\d-\d\d \d\d:\d\d)', page_html)
    for r, d in zip(reports, dates):
        r["date"] = d.replace(" ", "T") + ":00Z"
    return reports


def search(query, limit=24, offset=0, delay=3):
    all_reports = []
    per_page = min(limit, 24)
    fetched = 0
    while fetched < limit:
        n = min(per_page, limit - fetched)
        qs = urllib.parse.urlencode({"q": query, "limit": n, "offset": offset + fetched})
        current = f"{BASE}/search?q={urllib.parse.quote(query)}"
        page_html = fetch(f"/api/htmx/search/?{qs}", current)
        batch = parse_reports(page_html)
        if not batch:
            break
        all_reports.extend(batch)
        fetched += len(batch)
        if len(batch) < n:
            break
        time.sleep(delay)
    return {"reports": all_reports[:limit], "query": query}


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("--query", required=True)
    s.add_argument("--limit", type=int, default=24)
    s.add_argument("--offset", type=int, default=0)
    s.add_argument("--delay", type=float, default=3)
    a = ap.parse_args()
    if a.cmd == "search":
        print(json.dumps(search(a.query, a.limit, a.offset, a.delay)))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
