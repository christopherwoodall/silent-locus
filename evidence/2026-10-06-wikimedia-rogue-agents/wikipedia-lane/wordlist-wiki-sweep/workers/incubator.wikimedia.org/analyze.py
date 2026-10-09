#!/usr/bin/env python3
"""Aggregate the insource sweep: runlog tally + literal-match filtering.

CirrusSearch mangles punctuation-only/glob terms (e.g. ${7*7} -> matches "7"),
so an API hit only counts as a REAL hit if at least one cached snippet
contains the literal term as a case-insensitive substring (searchmatch tags
stripped). Outputs hits-literal.json: per-term records needing revision fetch.
"""
import json, os, re, glob
from collections import Counter

SWEEP = "raw/incubator.wikimedia.org"

def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s or "")

def main():
    terms = json.load(open("search-terms.json"))["terms"]
    tally = Counter()            # category -> (raw_hits_terms, literal_hits_terms, total_raw_hits)
    raw_hits_terms = Counter()
    literal_hits_terms = Counter()
    total_raw_hits = Counter()
    literal_records = []
    degenerate = []

    for n, t in enumerate(terms):
        p = os.path.join(SWEEP, f"insource-{n:04d}.json")
        term, cat = t["term"], t["category"]
        try:
            d = json.load(open(p))
        except Exception:
            continue
        resp = d.get("response", {})
        total = resp.get("query", {}).get("searchinfo", {}).get("totalhits", 0)
        results = resp.get("query", {}).get("search", [])
        if total and total > 0:
            raw_hits_terms[cat] += 1
            total_raw_hits[cat] += total
        lit = [r for r in results
               if term.lower() in strip_tags(r.get("snippet", "")).lower()]
        if lit:
            literal_hits_terms[cat] += 1
            for r in lit:
                literal_records.append({
                    "n": n, "term": term, "category": cat,
                    "totalhits": total, "truncated": total > 50,
                    "ns": r.get("ns"), "title": r.get("title"),
                    "pageid": r.get("pageid"),
                    "snippet": strip_tags(r.get("snippet", ""))[:300],
                })
        elif total and total > 0:
            degenerate.append({"n": n, "term": term, "category": cat, "totalhits": total})

    out = {
        "raw_terms_with_any_api_hit": dict(raw_hits_terms),
        "terms_with_literal_snippet_match": dict(literal_hits_terms),
        "sum_totalhits_by_category": dict(total_raw_hits),
        "degenerate_query_terms": degenerate,
    }
    json.dump(out, open(os.path.join(SWEEP, "SUMMARY.json"), "w"), indent=2, ensure_ascii=False)
    json.dump(literal_records, open(os.path.join(SWEEP, "hits-literal.json"), "w"), indent=2, ensure_ascii=False)
    print(json.dumps(out, indent=2)[:3000])
    print(f"\nliteral hit records: {len(literal_records)} | degenerate terms: {len(degenerate)}")
    # distinct pages among literal hits
    pages = {(r["title"], r["pageid"]) for r in literal_records}
    print("distinct pages needing revision fetch:", len(pages))

if __name__ == "__main__":
    main()
