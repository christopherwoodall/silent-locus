#!/usr/bin/env python3
"""Pull recent revision histories of main sandbox pages; grep comments for ngrams."""
import json, time, urllib.parse, urllib.request, datetime, os

RAW = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/ngram-sweep/raw")
os.makedirs(RAW, exist_ok=True)

SANDPITS = {
    "en.wikipedia.org": "Wikipedia:Sandbox",
    "simple.wikipedia.org": "Wikipedia:Sandbox",
    "test.wikipedia.org": "Wikipedia:Sandbox",
    "test2.wikipedia.org": "Wikipedia:Sandbox",
    "www.mediawiki.org": "Project:Sandbox",
    "commons.wikimedia.org": "Commons:Sandbox",
    "incubator.wikimedia.org": "Incubator:Sandbox",
    "meta.wikimedia.org": "Meta:Sandbox",
    "bg.wikipedia.org": "Уикипедия:Пясъчник",
}
NGRAMS = [
    "technical sandbox initialization",
    "sandbox initialization",
    "temporary technical",
    "lifeval temporary",
    "lifeval api",
    "temp-account test",
    "temp-account",
    "api temp-account",
    "external link test",
]
UA = {"User-Agent": "silent-locus-ngram-sweep/1.0 (research; contact via repo)"}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

out = {}
for wiki, page in SANDPITS.items():
    t = urllib.parse.quote(page.replace(" ", "_"), safe="")
    url = (f"https://{wiki}/w/api.php?action=query&prop=revisions&titles={t}"
           f"&rvprop=ids|timestamp|user|comment|tags&rvlimit=200&format=json&formatversion=2")
    try:
        d = get(url)
        pages = d.get("query", {}).get("pages", [])
        revs = pages[0].get("revisions", []) if pages else []
        matches = []
        for r in revs:
            c = (r.get("comment") or "").lower()
            hit = [p for p in NGRAMS if p in c]
            if hit:
                matches.append({"revid": r.get("revid"), "timestamp": r.get("timestamp"),
                                "user": r.get("user"), "comment": r.get("comment"),
                                "tags": r.get("tags"), "ngrams": hit,
                                "difflink": f"https://{wiki}/w/index.php?diff={r.get('revid')}"})
        entry = {"wiki": wiki, "page": page, "revs_scanned": len(revs), "comment_matches": matches}
    except Exception as e:
        entry = {"wiki": wiki, "page": page, "error": str(e)}
    json.dump(entry, open(f"{RAW}/sandbox-comments-{wiki}.json", "w"), indent=1)
    out[wiki] = {"scanned": entry.get("revs_scanned"), "matches": len(entry.get("comment_matches", [])),
                 "error": entry.get("error")}
    time.sleep(5.5)

json.dump({"finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "method": "prop=revisions rvlimit=200 per sandbox, comment substring match (case-insensitive)",
           "per_wiki": out}, open(f"{RAW}/sandbox-comments-SUMMARY.json", "w"), indent=1)
print(json.dumps(out, indent=1))
