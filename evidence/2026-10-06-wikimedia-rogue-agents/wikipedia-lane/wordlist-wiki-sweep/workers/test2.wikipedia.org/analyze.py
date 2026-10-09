#!/usr/bin/env python3
"""Analyze test2 sweep raw data: per-category tally, hit enrichment, comment-grep report."""
import json, os, subprocess, time, urllib.parse
from datetime import datetime, timezone

WIKI = "test2.wikipedia.org"
BASE = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/wordlist-wiki-sweep")
RAW = os.path.join(BASE, "raw", WIKI)
OUT = os.path.join(BASE, "workers", WIKI)

KNOWN_OLDIDS = {
    7226103, 7226104, 7226105, 7226108, 7226111, 7226107, 7226109, 7226110,
    30732655, 1238390511, 8370994, 8370995, 741399, 741400, 612932, 612933,
    612931, 8370989, 1356314507, 1356419247, 744412, 613856, 1233683454,
    10891416, 747327, 744271, 741405, 1353498400, 744270, 744272, 1213503714,
    1213503789, 1213513506, 1353492663, 1213399057,
}

def api_get(params):
    qs = urllib.parse.urlencode(params)
    url = f"https://{WIKI}/w/api.php?{qs}"
    r = subprocess.run(
        ["curl", "-sS", "--max-time", 45,
         "-H", "User-Agent: silent-locus-wordlist-sweep/1.0 (research; test2 analysis)",
         url], capture_output=True, text=True, timeout=60)
    return json.loads(r.stdout)

def main():
    terms = json.load(open(os.path.join(BASE, "search-terms.json")))["terms"]
    log = [json.loads(l) for l in open(os.path.join(RAW, "run-log.jsonl"))]
    by_cat = {}
    for t in terms:
        by_cat.setdefault(t["category"], {"searched": 0, "hits": 0, "terms": []})
        by_cat[t["category"]]["searched"] += 1
    hit_terms = []
    for rec in log:
        c = by_cat[rec["category"]]
        if rec["totalhits"] and rec["totalhits"] > 0:
            c["hits"] += 1
            c["terms"].append({"n": rec["n"], "term": rec["term"],
                               "totalhits": rec["totalhits"], "raw_file": rec["raw_file"]})
            hit_terms.append(rec)
        elif rec["totalhits"] == -1:
            c.setdefault("errors", 0)
            c["errors"] += 1
    # enrich every hit page: latest revision metadata
    all_pageids = set()
    for rec in hit_terms:
        raw = json.load(open(os.path.join(RAW, rec["raw_file"])))
        for h in raw["results"]:
            all_pageids.add(str(h["pageid"]))
    all_pageids = list(all_pageids)
    print(f"[analyze] {len(hit_terms)} hit-terms, {len(all_pageids)} distinct pages to enrich", flush=True)
    page_meta = {}
    for i in range(0, len(all_pageids), 50):
        batch = all_pageids[i:i+50]
        d = api_get({"action": "query", "pageids": "|".join(batch),
                     "prop": "revisions", "rvprop": "ids|timestamp|user|comment|tags|flags",
                     "rvslots": "main", "format": "json"})
        for pid, p in d["query"]["pages"].items():
            rev = (p.get("revisions") or [{}])[0]
            page_meta[pid] = {"pageid": int(pid), "ns": p.get("ns"),
                              "title": p.get("title"),
                              "revid": rev.get("revid"),
                              "timestamp": rev.get("timestamp"),
                              "user": rev.get("user"),
                              "comment": rev.get("comment"),
                              "tags": rev.get("tags"),
                              "minor": rev.get("minor", False)}
        time.sleep(5.5)
    # attach enriched pages to hit terms
    for rec in hit_terms:
        raw = json.load(open(os.path.join(RAW, rec["raw_file"])))
        rec["pages"] = [page_meta.get(str(h["pageid"]),
                        {"pageid": h["pageid"], "title": h["title"], "note": "meta missing"})
                        for h in raw["results"]]
    # comment grep summary
    cg = json.load(open(os.path.join(RAW, "sandbox-comment-grep.json")))
    for m in cg.get("matches", []):
        m["known_incident"] = m["revid"] in KNOWN_OLDIDS
    analysis = {
        "analyzed_utc": datetime.now(timezone.utc).isoformat(),
        "terms_total": len(terms),
        "terms_with_hits": len(hit_terms),
        "terms_zero": len(terms) - len(hit_terms),
        "per_category": {k: {"searched": v["searched"], "hits": v["hits"],
                             "errors": v.get("errors", 0),
                             "terms": v["terms"]} for k, v in sorted(by_cat.items())},
        "hit_terms_enriched": hit_terms,
        "comment_grep": {"matches": cg.get("matches", []),
                         "sandbox_revs": cg.get("sandbox_revs"),
                         "retrieved_utc": cg.get("retrieved_utc")},
    }
    json.dump(analysis, open(os.path.join(OUT, "ANALYSIS.json"), "w"), indent=2)
    print("[analyze] wrote ANALYSIS.json", flush=True)
    # quick console tally
    for k, v in sorted(by_cat.items()):
        print(f"  {k}: {v['hits']}/{v['searched']} terms with hits", flush=True)
    print(f"  comment-grep matches: {len(cg.get('matches', []))}", flush=True)

if __name__ == "__main__":
    main()
