#!/usr/bin/env python3
"""insource: ngram sweep across 9 wikis. Paced >=5.5s per request."""
import json, time, urllib.parse, urllib.request, datetime, os

RAW = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/ngram-sweep/raw")
os.makedirs(RAW, exist_ok=True)

WIKIS = [
    "en.wikipedia.org", "simple.wikipedia.org", "test.wikipedia.org",
    "test2.wikipedia.org", "www.mediawiki.org", "commons.wikimedia.org",
    "incubator.wikimedia.org", "meta.wikimedia.org", "bg.wikipedia.org",
]
NGRAMS = [
    "technical sandbox initialization",
    "sandbox initialization",
    "temporary technical",
    "Lifeval temporary",
    "Lifeval API",
    "temp-account test",
    "temp-account",
    "API temp-account",
    "external link test",
]
UA = {"User-Agent": "silent-locus-ngram-sweep/1.0 (research; contact via repo)"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

results = {}
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
n = 0
for wiki in WIKIS:
    for ng in NGRAMS:
        n += 1
        q = urllib.parse.quote(f'insource:"{ng}"')
        url = (f"https://{wiki}/w/api.php?action=query&list=search&srsearch={q}"
               f"&srlimit=50&srnamespace=*&format=json&formatversion=2")
        try:
            d = get(url)
            hits = d.get("query", {}).get("search", [])
            info = d.get("query", {}).get("searchinfo", {})
            entry = {
                "wiki": wiki, "ngram": ng, "url": url,
                "total_hits": info.get("totalhits"),
                "returned": len(hits),
                "hits": [{"ns": h.get("ns"), "title": h.get("title"),
                          "pageid": h.get("pageid"), "timestamp": h.get("timestamp"),
                          "snippet": h.get("snippet")} for h in hits],
            }
        except Exception as e:
            entry = {"wiki": wiki, "ngram": ng, "url": url, "error": str(e)}
        json.dump(entry, open(f"{RAW}/insource-{wiki}-{n:02d}.json", "w"), indent=1)
        results.setdefault(ng, []).append({"wiki": wiki, "total": entry.get("total_hits"),
                                           "returned": entry.get("returned", 0),
                                           "error": entry.get("error")})
        time.sleep(5.5)

summary = {"started_utc": started, "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "method": "MediaWiki API list=search insource:, srlimit=50, srnamespace=*, paced >=5.5s",
           "per_ngram": results}
json.dump(summary, open(f"{RAW}/SUMMARY.json", "w"), indent=1)
print(json.dumps({p: {r["wiki"]: r["total"] for r in rs} for p, rs in results.items()}, indent=1))
