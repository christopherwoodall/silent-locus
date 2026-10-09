#!/usr/bin/env python3
"""PATTERN-HUNTER phase 3a: sweep insource:"Lifeval" across all incident wikis.
curl + 5.5s pacing. Bank raw JSON. Grade: OBSERVED."""
import json, os, subprocess, sys, time, urllib.parse

BASE = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents")
RAW = os.path.join(BASE, "workers/wikipedia-lane/pattern-hunter/raw")
UA = "silent-locus-pattern-hunter/1.0 (OSINT research; mailto:research@example.org)"
PACE = 5.5

HOSTS = ["en.wikipedia.org", "test.wikipedia.org", "test2.wikipedia.org",
         "www.mediawiki.org", "commons.wikimedia.org", "simple.wikipedia.org",
         "incubator.wikimedia.org", "meta.wikimedia.org", "bg.wikipedia.org",
         "en.wikibooks.org", "en.wikivoyage.org", "www.wikidata.org",
         "en.wikiversity.org", "en.wikisource.org", "en.wikinews.org",
         "en.wikiquote.org", "species.wikimedia.org", "strategy.wikimedia.org"]

def curl_json(url):
    time.sleep(PACE)
    out = subprocess.run(["curl", "-sS", "--max-time", "60", "-A", UA, url],
                         capture_output=True, text=True)
    if out.returncode != 0:
        print(f"CURL FAIL {url}: {out.stderr.strip()}", file=sys.stderr)
        return None
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError:
        print(f"JSON FAIL {url}: {out.stdout[:200]}", file=sys.stderr)
        return None

all_hits = []
for host in HOSTS:
    q = urllib.parse.quote('insource:"Lifeval"')
    url = (f"https://{host}/w/api.php?action=query&list=search&srsearch={q}"
           f"&srnamespace=*&srlimit=50&format=json&formatversion=2")
    data = curl_json(url)
    fn = os.path.join(RAW, f"search_lifeval_{host.replace('.', '_')}.json")
    with open(fn, "w") as f:
        json.dump({"provenance": {"source_url": url, "retrieved_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, "response": data}, f, indent=1)
    hits = (data or {}).get("query", {}).get("search", []) if data else None
    if hits is None:
        print(f"{host}: QUERY FAILED")
        continue
    print(f"{host}: {len(hits)} hits")
    for h in hits:
        all_hits.append({"host": host, "ns": h.get("ns"), "title": h.get("title"),
                         "pageid": h.get("pageid"), "wordcount": h.get("wordcount"),
                         "timestamp": h.get("timestamp"), "snippet": h.get("snippet")})

with open(os.path.join(BASE, "workers/wikipedia-lane/pattern-hunter/lifeval_hits.json"), "w") as f:
    json.dump(all_hits, f, indent=1)
print(f"TOTAL: {len(all_hits)} hits banked")
