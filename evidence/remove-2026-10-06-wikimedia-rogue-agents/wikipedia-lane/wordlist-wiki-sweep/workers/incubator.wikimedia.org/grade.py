#!/usr/bin/env python3
"""Join hits-literal.json with revfetch-<pageid>.json and print a grading table.

Grades suggested automatically, verified by the worker before writing FINDINGS.md:
  - known-incident: revid in the marker-index set (or term-hit on incident page)
  - incident-shaped-new: ~2026-* / disposable-looking user, sandbox/test page,
    machine markers, NOT in incident set
  - organic: docs, discussions, established users, human pages
  - noise: degenerate matches (already filtered to literal-only by analyze.py)
"""
import json, os, re, sys
from collections import defaultdict

SWEEP = "raw/incubator.wikimedia.org"
KNOWN = {7226103,7226104,7226105,7226108,7226111,7226107,7226109,7226110,
 30732655,1238390511,8370994,8370995,741399,741400,612932,612933,612931,
 8370989,1356314507,1356419247,744412,613856,1233683454,10891416,747327,
 744271,741405,1353498400,744270,744272,1213503714,1213503789,1213513506,
 1353492663,1213399057}

def looks_temp(user):
    return bool(re.match(r"^~2026-\d+$", user or "")) or \
           bool(re.match(r"^(Temp|Test|test)[-_]?\w*\d{3,}$", user or "", re.I))

def main():
    recs = json.load(open(os.path.join(SWEEP, "hits-literal.json")))
    by_page = defaultdict(list)
    for r in recs:
        by_page[r["pageid"]].append(r)
    rows = []
    for pid, rs in by_page.items():
        p = os.path.join(SWEEP, f"revfetch-{pid}.json")
        if not os.path.exists(p):
            rows.append((pid, "MISSING-FETCH", rs[0]["title"], "", "", "", ""))
            continue
        d = json.load(open(p))
        page = list(d["response"]["query"]["pages"].values())[0]
        revs = page.get("revisions", [])
        if not revs:
            rows.append((pid, "no-revisions", page.get("title"), "", "", "", ""))
            continue
        rev = revs[0]
        revid = rev.get("revid")
        user = rev.get("user", "")
        grade = "organic"
        if revid in KNOWN:
            grade = "known-incident"
        elif looks_temp(user) or re.search(r"[Ss]andbox|[Tt]est", rs[0]["title"]):
            grade = "incident-shaped-NEW?"
        rows.append((pid, grade, revid, page.get("title"), user, rev.get("timestamp",""),
                     (rev.get("comment") or "")[:120], ";".join(t["term"] for t in rs)))
    for pid, grade, revid, title, user, ts, comment, terms in sorted(rows, key=lambda x: (x[1], str(x[3]))):
        print(f"[{grade}] {title} (pageid={pid}, revid={revid})")
        print(f"    user={user} ts={ts} comment={comment}")
        print(f"    terms: {terms}")
        print(f"    diff: https://incubator.wikimedia.org/w/index.php?diff={revid}")
        print()
    print(f"\n{len(rows)} pages")

if __name__ == "__main__":
    main()
