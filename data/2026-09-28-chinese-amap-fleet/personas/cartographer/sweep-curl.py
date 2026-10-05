#!/usr/bin/env python3
"""Curl-based fallback for urlquery htmx search — same parse logic as uq_htmx.py,
but fetches pages via curl (survives flaky egress where urllib IncompleteReads)."""
import html as htmlmod
import json
import re
import subprocess
import sys
import time
import urllib.parse

BASE = "https://urlquery.net"
HEADERS = [
    "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "HX-Request: true",
    "Accept: text/html",
]


def fetch(path, current_url):
    qs = urllib.parse.urlencode({
        "q": sys.argv[1], "limit": "24", "offset": "0"})  # placeholder, unused
    cmd = ["curl", "-sS", "--max-time", "45"] + sum(
        (["-H", h] for h in HEADERS + [f"HX-Current-URL: {current_url}"]), []) + \
        [BASE + path]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:200])
    return r.stdout


def parse_reports(page_html):
    reports = []
    rows = re.findall(
        r'href="/report/([a-f0-9-]{8,36})"[^>]*>([^<]{1,300})</a>', page_html)
    seen = set()
    for rid, url in rows:
        if rid in seen:
            continue
        seen.add(rid)
        reports.append({
            "report_id": rid,
            "url": htmlmod.unescape(url.strip()),
        })
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


if __name__ == "__main__":
    q, lim = sys.argv[1], int(sys.argv[2])
    print(json.dumps(search(q, lim)))
    sys.stdout.flush()
