#!/usr/bin/env python3
"""Analyze www.mediawiki.org wordlist-wiki-sweep insource results.

Reads all raw/www.mediawiki.org/insource-<n>.json + search-terms.json,
builds per-category hit tally, and writes workers/www.mediawiki.org/
analysis input: hitlist.json + SUMMARY.json.
"""
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "raw", "www.mediawiki.org")
WORK = os.path.join(BASE, "workers", "www.mediawiki.org")
os.makedirs(WORK, exist_ok=True)

terms = json.load(open(os.path.join(BASE, "search-terms.json")))["terms"]

def load_insource(n):
    p = os.path.join(RAW, f"insource-{n}.json")
    if not os.path.exists(p):
        return None
    try:
        data = json.load(open(p))
    except Exception:
        return {"_parse_error": True}
    return data.get("query", {}).get("searchinfo", {}).get("totalhits")

hitlist = []   # terms with >=1 hit: n, term, category, totalhits, titles
missing = []
for n, t in enumerate(terms):
    hits = load_insource(n)
    if hits is None:
        missing.append(n)
        continue
    if isinstance(hits, int) and hits > 0:
        p = os.path.join(RAW, f"insource-{n}.json")
        data = json.load(open(p))
        pages = data.get("query", {}).get("search", [])
        titles = [f"{pg.get('title','?')} (ns={pg.get('ns')})" for pg in pages]
        hitlist.append({"n": n, "term": t["term"], "category": t.get("category", ""),
                        "totalhits": hits, "returned": len(pages), "titles": titles})

# per-category tally
cats = {}
for t in terms:
    cats.setdefault(t.get("category", ""), {"terms": 0, "terms_with_hits": 0,
                                            "raw_hits": 0})
    cats[t.get("category", "")]["terms"] += 1
for h in hitlist:
    c = cats[h["category"]]
    c["terms_with_hits"] += 1
    c["raw_hits"] += h["totalhits"]

summary = {
    "wiki": "www.mediawiki.org",
    "terms_total": len(terms),
    "terms_collected": len(terms) - len(missing),
    "terms_missing": missing,
    "terms_with_hits": len(hitlist),
    "raw_hits_sum": sum(h["totalhits"] for h in hitlist),
    "per_category": cats,
}
json.dump(summary, open(os.path.join(RAW, "SUMMARY.json"), "w"), indent=1)
json.dump({"hits": hitlist}, open(os.path.join(WORK, "hitlist.json"), "w"), indent=1)

print(json.dumps(summary, indent=1))
print("\n== HITS ==")
for h in sorted(hitlist, key=lambda x: -x["totalhits"]):
    print(f"[{h['n']}] ({h['totalhits']}) [{h['category']}] {h['term']!r}")
    for t in h["titles"][:6]:
        print(f"      {t}")
    if h["returned"] > 6:
        print(f"      ... +{h['returned']-6} more (total {h['totalhits']})")
