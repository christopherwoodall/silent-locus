#!/usr/bin/env python3
"""Post-sweep analysis for the test.wikipedia.org wordlist sweep.

1. Reads run-log.jsonl + insource-*.json, builds per-category tallies.
2. For every nonzero term, fetches current revision details (content
   snippet, timestamp, user, comment, tags) for each hit page, paced >=5s.
3. Emits a JSON candidate list for manual grading + prints the tally.

Output: raw/test.wikipedia.org/grade-candidates.json
Do not commit. Do not touch main.
"""
import json, time, os, urllib.parse, urllib.request
from datetime import datetime, timezone
from collections import Counter, defaultdict

BASE = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/wordlist-wiki-sweep")
RAW = os.path.join(BASE, "raw", "test.wikipedia.org")

# Known incident oldids (54-set per LIFEVAL-WRITEUP.md marker index, task brief)
KNOWN = {7226103,7226104,7226105,7226108,7226111,7226107,7226109,7226110,
         30732655,1238390511,8370994,8370995,741399,741400,612932,612933,
         612931,8370989,1356314507,1356419247,744412,613856,1233683454,
         10891416,747327,744271,741405,1353498400,744270,744272,1213503714,
         1213503789,1213513506,1353492663,1213399057}

terms = json.load(open(os.path.join(BASE, "search-terms.json")))["terms"]
log = {}
for line in open(os.path.join(RAW, "run-log.jsonl")):
    line = line.strip()
    if line:
        e = json.loads(line)
        log[e["n"]] = e

assert len(log) == len(terms), f"run incomplete: {len(log)}/{len(terms)} logged"

UA = {"User-Agent": "silent-locus-wiki-hunt/1.0 (agent-incident research)"}
def api(params):
    url = "https://test.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

cat_terms = Counter()
cat_nonzero = Counter()
cat_hits = Counter()
nonzero = []  # (n, term, category, totalhits, [hits])
for n, t in enumerate(terms):
    e = log[n]
    cat_terms[t["category"]] += 1
    total = e.get("totalhits", -1)
    if total and total > 0:
        d = json.load(open(os.path.join(RAW, f"insource-{n}.json")))
        hits = d["query"]["search"]
        cat_nonzero[t["category"]] += 1
        cat_hits[t["category"]] += total
        nonzero.append((n, t["term"], t["category"], total, hits))

print("=== PER-CATEGORY TALLY ===")
for c in sorted(cat_terms):
    print(f"{c:18s} terms={cat_terms[c]:4d} nonzero_terms={cat_nonzero[c]:3d} totalhits={cat_hits[c]}")
print(f"{'TOTAL':18s} terms={len(terms):4d} nonzero_terms={len(nonzero):3d} totalhits={sum(cat_hits.values())}")

# collect unique pageids for revision detail fetch
pageids = {}
for n, term, cat, total, hits in nonzero:
    for h in hits:
        pageids[h["pageid"]] = (h["title"], h.get("ns"))

candidates = []
pids = list(pageids)
print(f"\n=== fetching revision details for {len(pids)} unique hit pages ===", flush=True)
revinfo = {}
for i in range(0, len(pids), 40):
    batch = pids[i:i+40]
    d = api({"action": "query", "format": "json", "formatversion": "2",
             "prop": "revisions", "pageids": "|".join(map(str, batch)),
             "rvprop": "ids|timestamp|user|comment|tags", "rvslots": "main",
             "rvlimit": "1"})
    for p in d["query"]["pages"]:
        revs = p.get("revisions", [])
        r = revs[0] if revs else {}
        revinfo[p["pageid"]] = {
            "title": p.get("title"), "ns": p.get("ns"),
            "revid": r.get("revid"), "parentid": r.get("parentid"),
            "user": r.get("user"), "timestamp": r.get("timestamp"),
            "comment": r.get("comment"), "tags": r.get("tags", []),
        }
    time.sleep(5.2)

for n, term, cat, total, hits in nonzero:
    pages = []
    for h in hits:
        ri = revinfo.get(h["pageid"], {})
        pages.append({
            "title": h["title"], "ns": h.get("ns"), "pageid": h["pageid"],
            "revid": ri.get("revid"), "user": ri.get("user"),
            "timestamp": ri.get("timestamp"), "comment": ri.get("comment"),
            "tags": ri.get("tags"),
            "diff": f"https://test.wikipedia.org/w/index.php?diff={ri.get('revid')}" if ri.get("revid") else None,
            "known_incident_oldid": (ri.get("revid") in KNOWN),
        })
    candidates.append({"n": n, "term": term, "category": cat,
                       "totalhits": total, "shown": len(hits), "pages": pages})

out = os.path.join(RAW, "grade-candidates.json")
json.dump({"generated_utc": datetime.now(timezone.utc).isoformat(),
           "candidates": candidates}, open(out, "w"), indent=1)
print(f"\nwrote {out} with {len(candidates)} nonzero terms", flush=True)
for c in candidates:
    print(f"\n--- [{c['category']}] n={c['n']} term={c['term']!r} totalhits={c['totalhits']} (showing {c['shown']})")
    for p in c["pages"]:
        print(f"    {p['title']} | revid={p['revid']} user={p['user']} ts={p['timestamp']} known={p['known_incident_oldid']}")
        print(f"      comment={p['comment']!r} tags={p['tags']}")
        print(f"      diff={p['diff']}")
