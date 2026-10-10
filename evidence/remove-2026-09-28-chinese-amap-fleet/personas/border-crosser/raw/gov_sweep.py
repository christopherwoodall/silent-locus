#!/usr/bin/env python3
"""BORDER-CROSSER gov-domain sweep via curl (python egress broken on this VM).

Hits urlquery htmx search endpoint with >=6s politeness delay between calls.
Saves one JSON file per domain query under raw/htmx/.
Usage: python3 gov_sweep.py [domain ...]
"""
import json, os, re, subprocess, sys, time, html as htmlmod, urllib.parse

BASE = "https://urlquery.net"
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "htmx")
HEADERS = [
    "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "-H", "HX-Request: true",
    "-H", "Accept: text/html",
]

def fetch(query, limit, offset):
    qs = urllib.parse.urlencode({"q": query, "limit": limit, "offset": offset})
    current = f"{BASE}/search?q={urllib.parse.quote(query)}"
    url = f"{BASE}/api/htmx/search/?{qs}"
    cmd = ["curl", "-s", "--max-time", "50"] + HEADERS + ["-H", f"HX-Current-URL: {current}", url]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.stdout

def parse_reports(page_html):
    reports = []
    rows = re.findall(r'href="/report/([a-f0-9-]{8,36})"[^>]*>([^<]{1,300})</a>', page_html)
    seen = set()
    for rid, url in rows:
        if rid in seen: continue
        seen.add(rid)
        reports.append({"report_id": rid, "url": htmlmod.unescape(url.strip())})
    dates = re.findall(r'(20\d\d-\d\d-\d\d \d\d:\d\d)', page_html)
    for r, d in zip(reports, dates):
        r["date"] = d.replace(" ", "T") + ":00Z"
    return reports

def search(query, limit=48, delay=6):
    out = []
    fetched = 0
    while fetched < limit:
        n = min(24, limit - fetched)
        html = fetch(query, n, fetched)
        if not html:
            return out, "EMPTY"
        batch = parse_reports(html)
        if not batch:
            # endpoint may return an empty page when done; check for obvious error
            if "rate" in html.lower() or "throttl" in html.lower():
                return out, "THROTTLE?"
            return out, "DONE?" if fetched else "NOPARSE"
        out.extend(batch)
        fetched += len(batch)
        if len(batch) < n: break
        time.sleep(delay)
    return out, "OK"

DOMAINS = sys.argv[1:] or ["go.jp","gov.br","gov.in","gouv.fr","gov.za","gov.uk","gov.tw","gov.kr","gov.sg","gov.my","gov.th","gov.vn","gov.tr","gov.ae","gov.sa","gov.eg","gov.mx","gov.ar","gov.co"]

os.makedirs(OUTDIR, exist_ok=True)
summary = {}
for i, d in enumerate(DOMAINS):
    q = f"url.domain:{d}"
    reports, status = search(q, limit=48, delay=6)
    fp = os.path.join(OUTDIR, d.replace(".", "_") + ".json")
    with open(fp, "w") as f:
        json.dump({"query": q, "status": status, "reports": reports}, f, indent=1)
    summary[d] = {"status": status, "count": len(reports)}
    print(f"{d}: {status} n={len(reports)}", flush=True)
    if i < len(DOMAINS) - 1:
        time.sleep(6)
with open(os.path.join(OUTDIR, "_summary.json"), "w") as f:
    json.dump(summary, f, indent=1)
print("summary:", json.dumps(summary))
