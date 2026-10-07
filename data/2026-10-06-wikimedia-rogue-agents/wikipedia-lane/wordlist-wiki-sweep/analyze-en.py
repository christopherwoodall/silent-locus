#!/usr/bin/env python3
"""Grade en.wikipedia.org wordlist-sweep hits. Reads raw/en.wikipedia.org/SUMMARY.json
+ insource-*.json, fetches latest-revision metadata for every hit page, emits a
hit table for manual grading. Does NOT commit anything."""
import json, time, urllib.parse, urllib.request
from datetime import datetime, timezone

BASE = "https://en.wikipedia.org/w/api.php"
UA = "wordlist-wiki-sweep/1.0 (research; en.wikipedia.org IOC hunt; contact via repo)"
WORKDIR = "/home/hatch/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/wordlist-wiki-sweep"
RAW = WORKDIR + "/raw/en.wikipedia.org"

KNOWN_EN = {"1353490694","1353490935","1353491551","1353492663","1353498400",
            "1353501383","1353507315","1353518652","1353543060","1356314507","1356419247"}

def api(params):
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

def main():
    summ = json.load(open(RAW + "/SUMMARY.json"))["terms"]
    hits = [s for s in summ if (s.get("totalhits") or 0) > 0 and not s.get("error")]
    print("hit terms: %d / %d" % (len(hits), len(summ)))
    pages = {}  # title -> {term hits, snippet}
    for s in hits:
        d = json.load(open("%s/insource-%d.json" % (RAW, s["n"])))
        for h in d["query"]["search"]:
            t = h["title"]
            pages.setdefault(t, {"terms": [], "snippets": [], "pageid": h["pageid"]})
            pages[t]["terms"].append((s["term"], s["category"]))
            pages[t]["snippets"].append(h.get("snippet",""))
    print("distinct hit pages: %d" % len(pages))
    # fetch latest revision metadata in batches of 50
    titles = list(pages)
    revmeta = {}
    for i in range(0, len(titles), 50):
        batch = titles[i:i+50]
        d = api({"action":"query","prop":"revisions","titles":"|".join(batch),
                 "rvlimit":1,"rvprop":"ids|timestamp|user|comment|tags|flags","format":"json"})
        for pid, p in d["query"]["pages"].items():
            rev = (p.get("revisions") or [{}])[0]
            revmeta[p["title"]] = {"pageid": p.get("pageid"), "ns": p.get("ns"),
                                   "revid": rev.get("revid"), "timestamp": rev.get("timestamp"),
                                   "user": rev.get("user"), "comment": rev.get("comment"),
                                   "tags": rev.get("tags")}
        time.sleep(1.0)
    table = []
    for t, info in sorted(pages.items()):
        rm = revmeta.get(t, {})
        known = str(rm.get("revid")) in KNOWN_EN
        table.append({"title": t, "ns": rm.get("ns"), "revid": rm.get("revid"),
                      "timestamp": rm.get("timestamp"), "user": rm.get("user"),
                      "comment": rm.get("comment"), "tags": rm.get("tags"),
                      "known_incident_revid": known,
                      "term_hits": [{"term": tm, "category": c} for tm, c in info["terms"]],
                      "snippets": info["snippets"][:3]})
    json.dump({"generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "known_incident_en_oldids": sorted(KNOWN_EN),
               "hit_pages": table},
              open(RAW + "/hit-table.json", "w"), indent=1)
    print("wrote hit-table.json with %d pages" % len(table))

if __name__ == "__main__":
    main()
