#!/usr/bin/env python3
"""insource: vocab sweep across 9 wikis. Paced >=5.5s per request."""
import json, time, urllib.parse, urllib.request, datetime, os

RAW = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/vocab-sweep/raw")
os.makedirs(RAW, exist_ok=True)

WIKIS = [
    "en.wikipedia.org", "simple.wikipedia.org", "test.wikipedia.org",
    "test2.wikipedia.org", "www.mediawiki.org", "commons.wikimedia.org",
    "incubator.wikimedia.org", "meta.wikimedia.org", "bg.wikipedia.org",
]
PHRASES = [
    "Temporary technical sandbox initialization",
    "testing external link",
    "sandbox test link",
    "Sandbox link test",
    "clear sandbox",
    "OCR test",
]
UA = {"User-Agent": "silent-locus-vocab-sweep/1.0 (research; contact via repo)"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

results = {}
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
n = 0
for wiki in WIKIS:
    for phrase in PHRASES:
        n += 1
        q = urllib.parse.quote(f'insource:"{phrase}"')
        url = (f"https://{wiki}/w/api.php?action=query&list=search&srsearch={q}"
               f"&srlimit=50&srnamespace=*&format=json&formatversion=2")
        try:
            d = get(url)
            hits = d.get("query", {}).get("search", [])
            info = d.get("query", {}).get("searchinfo", {})
            entry = {
                "wiki": wiki, "phrase": phrase, "url": url,
                "total_hits": info.get("totalhits"),
                "returned": len(hits),
                "hits": [{"ns": h.get("ns"), "title": h.get("title"),
                          "pageid": h.get("pageid"), "timestamp": h.get("timestamp"),
                          "snippet": h.get("snippet")} for h in hits],
            }
        except Exception as e:
            entry = {"wiki": wiki, "phrase": phrase, "url": url, "error": str(e)}
        fn = f"{RAW}/insource-{wiki}-{n:02d}.json"
        json.dump(entry, open(fn, "w"), indent=1)
        results.setdefault(phrase, []).append({"wiki": wiki, "total": entry.get("total_hits"),
                                               "returned": entry.get("returned", 0),
                                               "error": entry.get("error")})
        time.sleep(5.5)

summary = {"started_utc": started, "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "method": "MediaWiki API list=search insource:, srlimit=50, srnamespace=*, paced >=5.5s",
           "per_phrase": results}
json.dump(summary, open(f"{RAW}/SUMMARY.json", "w"), indent=1)
print(json.dumps({p: {r["wiki"]: r["total"] for r in rs} for p, rs in results.items()}, indent=1))
