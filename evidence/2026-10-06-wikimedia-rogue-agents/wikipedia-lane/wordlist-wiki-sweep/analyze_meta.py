#!/usr/bin/env python3
"""Summarize meta.wikimedia.org wordlist insource sweep + sandbox comment grep."""
import json, os, glob

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "raw", "meta.wikimedia.org")
KNOWN = {7226103, 7226104, 7226105, 7226108, 7226111, 7226107, 7226109,
         7226110, 30732655, 1238390511, 8370994, 8370995, 741399, 741400,
         612932, 612933, 612931, 8370989, 1356314507, 1356419247, 744412,
         613856, 1233683454, 10891416, 747327, 744271, 741405, 1353498400,
         744270, 744272, 1213503714, 1213503789, 1213513506, 1353492663,
         1213399057}

terms = json.load(open(os.path.join(BASE, "search-terms.json")))["terms"]
summary = {"total_terms": len(terms), "terms_searched": 0, "errors": 0,
           "by_category": {}, "hits": []}

for n, t in enumerate(terms):
    cat = t["category"]
    summary["by_category"].setdefault(cat, {"searched": 0, "zero": 0, "hits": 0, "terms_with_hits": []})
    summary["by_category"][cat]["searched"] += 1
    p = os.path.join(RAW, "insource-%d.json" % n)
    if not os.path.exists(p):
        summary["errors"] += 1
        continue
    d = json.load(open(p))
    summary["terms_searched"] += 1
    hits = []
    if "query" in d:
        hits = d["query"].get("search", [])
    if not hits:
        summary["by_category"][cat]["zero"] += 1
        continue
    summary["by_category"][cat]["hits"] += len(hits)
    summary["by_category"][cat]["terms_with_hits"].append(t["term"])
    entry = {"n": n, "term": t["term"], "category": cat, "count": len(hits),
             "results": [{"title": h.get("title"), "ns": h.get("ns"),
                          "pageid": h.get("pageid"), "timestamp": h.get("timestamp"),
                          "snippet": h.get("snippet")} for h in hits]}
    summary["hits"].append(entry)

with open(os.path.join(RAW, "SUMMARY.json"), "w") as f:
    json.dump(summary, f, indent=1)

# Sandbox comment grep
sb = json.load(open(os.path.join(RAW, "sandbox-comments-meta.json")))["data"]
revs = sb["query"]["pages"][0]["revisions"]
matches = []
for rv in revs:
    comment = (rv.get("comment") or "")
    for n, t in enumerate(terms):
        if t["term"].lower() in comment.lower():
            matches.append({"n": n, "term": t["term"], "category": t["category"],
                            "revid": rv.get("revid"), "user": rv.get("user"),
                            "timestamp": rv.get("timestamp"), "comment": comment,
                            "tags": rv.get("tags")})
sb_out = {"revisions_scanned": len(revs), "matches": matches}
with open(os.path.join(RAW, "sandbox-comments-SUMMARY.json"), "w") as f:
    json.dump(sb_out, f, indent=1)

print("terms_searched=%d/%d errors=%d terms_with_hits=%d" %
      (summary["terms_searched"], summary["total_terms"], summary["errors"], len(summary["hits"])))
for cat, c in summary["by_category"].items():
    print("  %s: searched=%d zero=%d terms_with_hits=%d hits=%d" %
          (cat, c["searched"], c["zero"], len(c["terms_with_hits"]), c["hits"]))
print("sandbox comment matches: %d" % len(matches))
