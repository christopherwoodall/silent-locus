#!/usr/bin/env python3
"""urlquery htmx API CLI via curl (urllib hangs on this VM's egress proxy).

Same interface/output as uq_htmx.py:
    uq_htmx_curl.py search --query QUERY [--limit N] [--offset N] [--delay S]

Outputs JSON: {"reports": [{"report_id","url","date"}...], "query": QUERY}
"""
import argparse
import html as htmlmod
import json
import re
import subprocess
import sys
import time
import urllib.parse

BASE = "https://urlquery.net"


def fetch(path, current_url, timeout=60):
    cmd = [
        "curl", "-sS", "-m", str(timeout), BASE + path,
        "-H", "HX-Request: true",
        "-H", f"HX-Current-URL: {current_url}",
        "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "-H", "Accept: text/html",
    ]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 10)
    if p.returncode != 0:
        raise RuntimeError(f"curl failed rc={p.returncode}: {p.stderr.strip()[:200]}")
    return p.stdout


def parse_reports(page_html):
    reports = []
    rows = re.findall(
        r'href="/report/([a-f0-9-]{8,36})"[^>]*>([^<]{1,300})</a>', page_html
    )
    seen = set()
    for rid, url in rows:
        if rid in seen:
            continue
        seen.add(rid)
        reports.append({"report_id": rid, "url": htmlmod.unescape(url.strip())})
    dates = re.findall(r'(20\d\d-\d\d-\d\d \d\d:\d\d)', page_html)
    for r, d in zip(reports, dates):
        r["date"] = d.replace(" ", "T") + ":00Z"
    return reports


def search(query, limit=24, offset=0, delay=5):
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
    s.add_argument("--delay", type=float, default=5)
    a = ap.parse_args()
    if a.cmd == "search":
        print(json.dumps(search(a.query, a.limit, a.offset, a.delay)))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
