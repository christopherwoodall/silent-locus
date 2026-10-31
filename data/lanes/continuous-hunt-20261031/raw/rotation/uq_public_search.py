#!/usr/bin/env python3
"""Public urlquery search-page parser (no login, no htmx API).

Fetches https://urlquery.net/search/reports?q=QUERY (follows the 307 from
/search), parses result rows: submitted datetime, report id, submitted URL.
The old /api/htmx/search/ endpoint now 404s (verified 2026-10-31), so this
replaces uq_htmx_curl.py for the public path.
Output JSON: {"query","fetched_at","rows":[{date,report_id,url,report_url}]}
"""
import html as htmlmod
import json
import re
import subprocess
import sys
import urllib.parse
from datetime import datetime, timezone

ROW = re.compile(
    r'<time datetime="([^"]+)">.*?</time></td><td class="report-source">'
    r'<a[^>]*href="/report/([a-f0-9-]{36})"[^>]*>([^<]{1,500})</a>',
    re.S,
)


def fetch(query):
    url = "https://urlquery.net/search/reports?q=" + urllib.parse.quote(query)
    cmd = ["curl", "-sS", "-L", "-m", "60", url,
           "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
           "-H", "Accept: text/html"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=70)
    if p.returncode != 0:
        raise RuntimeError(f"curl failed rc={p.returncode}: {p.stderr.strip()[:200]}")
    return p.stdout


def main():
    query = sys.argv[1]
    page = fetch(query)
    rows = []
    seen = set()
    for date, rid, url in ROW.findall(page):
        if rid in seen:
            continue
        seen.add(rid)
        rows.append({"date": date, "report_id": rid,
                     "url": htmlmod.unescape(url.strip()),
                     "report_url": f"https://urlquery.net/report/{rid}"})
    out = {"query": query,
           "fetched_at": datetime.now(timezone.utc).isoformat(),
           "rows": rows}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
