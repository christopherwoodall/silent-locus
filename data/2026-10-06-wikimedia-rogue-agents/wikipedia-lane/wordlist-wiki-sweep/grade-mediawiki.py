#!/usr/bin/env python3
"""Fetch revision metadata (user, timestamp, comment, tags) for candidate
insource hits on www.mediawiki.org, paced >=5.2s. Caches per-title JSON.
Candidates chosen from terms 0-321 local-namespace hits.
Usage: python3 grade-mediawiki.py  (reads workers/www.mediawiki.org/hitlist.json,
                                   grades candidates into workers/www.mediawiki.org/grades.json)
"""
import json, os, subprocess, time, urllib.parse
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "raw", "www.mediawiki.org")
WORK = os.path.join(BASE, "workers", "www.mediawiki.org")
GCACHE = os.path.join(WORK, "grade-cache")
os.makedirs(GCACHE, exist_ok=True)
UA = "silent-locus-wiki-sweep/1.0 (research; contact via repo)"
API = "https://www.mediawiki.org/w/api.php"
PACING = 5.2

terms = json.load(open(os.path.join(BASE, "search-terms.json")))["terms"]

def cached(n):
    p = os.path.join(RAW, f"insource-{n}.json")
    return json.load(open(p))

# (term_index, title, why)
CANDIDATES = [
    (7,  "Talk:XTools/ArticleInfo/Flow export", "0x0.st on talk page"),
    (7,  "MediaWiki talk:Gadget-UTCLiveClock.js", "0x0.st on gadget talk"),
    (42, "Arabic Wikimedia Technical Community/Projects", "api.ipify.org single hit"),
    (152,"Arabic Wikimedia Technical Community/Projects", "httpbin.org same page"),
    (152,"User:Harej/PublicSuffixList", "httpbin.org on user page"),
    (96, "Talk:WikiApiary", "crt.sh single hit"),
    (122,"MediaWiki on IRC", "dpaste.org"),
    (122,"Help talk:Templates", "dpaste.org"),
    (130,"Core Platform Team/Decisions Architecture Research Documentation/API router and rate limiting design proposal", "file.io single hit"),
    (74, "Reading/Web/Accessibility for reading/Reporting/en.wikipedia.org/Archive 2", "catbox.moe"),
    (74, "Talk:Reading/Web/Desktop Improvements/Archive8", "catbox.moe"),
    (149,"Outreachy/Round 7", "htmlpreview.github.io"),
    (149,"User:Niharika (usurped)/Bug Reporting System", "htmlpreview.github.io user page"),
    (292,"Hack-A-Ton DC", "is.gd"),
    (292,"Extension talk:Send2StatusNet", "is.gd"),
    (292,"MediaWiki:Spam-whitelist", "is.gd"),
    (140,"GitLab/2020 consultation", "go-import"),
    (61, "Manual:WebRequest.php/pt-br", "arquivo.pt on Manual"),
    (64, "Extension talk:Graph/Demo", "bea.gov"),
    (307,"Project:Support desk/Flow/2023/03", "localhost.run sample"),
    (307,"Project:Support desk/Flow/2019/05", "localhost.run sample"),
    (0,  "API:Holidays viewer", "${7*7} sample"),
    (0,  "Manual:Namespace", "${7*7} sample"),
    (308,"Extension:WikiHiero/Syntax/fr", "m47 sample"),
]

def fetch_rev(title):
    safe = "".join(c if c.isalnum() else "_" for c in title)[:80]
    cp = os.path.join(GCACHE, safe + ".json")
    if os.path.exists(cp):
        return json.load(open(cp))
    params = {"action": "query", "prop": "revisions", "titles": title,
              "rvprop": "ids|timestamp|user|comment|tags|userid",
              "rvlimit": "1", "format": "json", "formatversion": "2"}
    qs = "&".join(f"{k}={urllib.parse.quote(v, safe='')}" for k, v in params.items())
    t0 = time.time()
    r = subprocess.run(["curl", "-sS", "-m", "45", "-A", UA, API + "?" + qs],
                       capture_output=True, timeout=60)
    time.sleep(max(0, PACING - (time.time() - t0)))
    try:
        data = json.loads(r.stdout.decode("utf-8", "replace"))
    except Exception:
        data = {"_fetch_error": True}
    json.dump(data, open(cp, "w"), indent=1)
    return data

def snippet_for(n, title):
    d = cached(n)
    for pg in d.get("query", {}).get("search", []):
        if pg.get("title") == title:
            sn = (pg.get("snippet") or "")
            return sn[:400].replace("\n", " ")
    return ""

grades = []
for n, title, why in CANDIDATES:
    data = fetch_rev(title)
    pages = data.get("query", {}).get("pages", [{}])
    pg = pages[0]
    revs = pg.get("revisions", [{}])
    r = revs[0] if revs else {}
    grades.append({
        "n": n, "term": terms[n]["term"], "category": terms[n].get("category"),
        "title": title, "why": why,
        "revid": r.get("revid"), "timestamp": r.get("timestamp"),
        "user": r.get("user"), "userid": r.get("userid"),
        "comment": r.get("comment"), "tags": r.get("tags"),
        "snippet": snippet_for(n, title),
    })
    print(json.dumps({"n": n, "title": title, "user": r.get("user"),
                      "ts": r.get("timestamp"), "tags": r.get("tags")},
                     ensure_ascii=False)[:200], flush=True)

json.dump(grades, open(os.path.join(WORK, "grades.json"), "w"), indent=1, ensure_ascii=False)
print("wrote workers/www.mediawiki.org/grades.json", len(grades), "records")
