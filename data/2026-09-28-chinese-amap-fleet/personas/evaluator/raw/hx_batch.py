#!/usr/bin/env python3
"""Batch htmx search harness for the scoredrop lane (lane 4).
Uses curl (robust to IncompleteRead flakiness), <=1 req/5s, retries with backoff.
Saves all results to JSON for verification.
"""
import json
import re
import subprocess
import sys
import time
import urllib.parse
import html as htmlmod

BASE = "https://urlquery.net"
DELAY = 5.5  # seconds between requests (task says <=1 req/5s)

def fetch(path, current_url, retries=3):
    for attempt in range(retries):
        cmd = [
            "curl", "-s", "--max-time", "90",
            "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "-H", "HX-Request: true",
            "-H", f"HX-Current-URL: {current_url}",
            BASE + path,
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        body = r.stdout
        if body and "/report/" in body:
            return body
        wait = 8 * (attempt + 1)
        print(f"  [retry {attempt+1}] empty/bad response, sleeping {wait}s", file=sys.stderr)
        time.sleep(wait)
    return ""

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
    for rep, d in zip(reports, dates):
        rep["date"] = d.replace(" ", "T") + ":00Z"
    return reports

def search(query, limit=24, offset=0):
    qs = urllib.parse.urlencode({"q": query, "limit": limit, "offset": offset})
    current = f"{BASE}/search?q={urllib.parse.quote(query)}"
    html = fetch(f"/api/htmx/search/?{qs}", current)
    return parse_reports(html)

def main():
    queries = []
    domains = ["webhook.site", "ntfy.sh", "0x0.st", "paste.rs", "rentry.co"]
    keywords = ["accuracy", "pass@1", "resolved", "score", "f1", "exact_match", "task_complete"]
    for d in domains:
        for k in keywords:
            queries.append(f"{d} {k}")
    # Also: dead-drop domain alone (baseline) for the top ones, low limit
    # (phase 2 queries passed via CLI args)
    if len(sys.argv) > 1:
        queries = sys.argv[1:]
    out = {}
    for i, q in enumerate(queries):
        print(f"[{i+1}/{len(queries)}] q={q!r}", file=sys.stderr)
        reps = search(q)
        out[q] = reps
        print(f"  -> {len(reps)} reports", file=sys.stderr)
        if i < len(queries) - 1:
            time.sleep(DELAY)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
