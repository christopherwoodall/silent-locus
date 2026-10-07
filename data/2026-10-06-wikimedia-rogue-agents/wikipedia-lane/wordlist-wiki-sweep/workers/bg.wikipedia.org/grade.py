#!/usr/bin/env python3
"""Grade insource: hits for bg.wikipedia.org wordlist sweep.
Stage 1: collect all terms with totalhits>0 -> hits-summary.json
Stage 2: for each distinct hit page, fetch latest 3 revisions
         (user, timestamp, comment, tags) -> page-revs.json
Output pre-graded JSON; human (caller) applies final grades.
"""
import json, os, subprocess, time, urllib.parse, re

BASE_DIR = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/wordlist-wiki-sweep")
RAWDIR = os.path.join(BASE_DIR, "raw", "bg.wikipedia.org")
API = "https://bg.wikipedia.org/w/api.php"
UA = "silent-locus-wordlist-sweep/1.0 (academic research)"

KNOWN_INCIDENT = {7226103, 7226104, 7226105, 7226108, 7226111, 7226107,
    7226109, 7226110, 30732655, 1238390511, 8370994, 8370995, 741399,
    741400, 612932, 612933, 612931, 8370989, 1356314507, 1356419247,
    744412, 613856, 1233683454, 10891416, 747327, 744271, 741405,
    1353498400, 744270, 744272, 1213503714, 1213503789, 1213513506,
    1353492663, 1213399057}

terms = json.load(open(os.path.join(BASE_DIR, "search-terms.json")))["terms"]

# ---- Stage 1: gather hits ----
hits = []          # (n, term, category, totalhits, [results])
non200 = []
zero_count = 0
for n, t in enumerate(terms):
    p = os.path.join(RAWDIR, f"insource-{n}.json")
    if not os.path.exists(p):
        print(f"WARNING: missing insource-{n}.json ({t['term'][:40]})")
        continue
    d = json.load(open(p))
    if d.get("http_status") != 200:
        non200.append({"n": n, "term": t["term"], "http_status": d.get("http_status")})
        continue
    th = d.get("totalhits")
    if th and th > 0:
        res = d["response"].get("query", {}).get("search", [])
        hits.append({"n": n, "term": t["term"], "category": t["category"],
                     "totalhits": th,
                     "results": [{"ns": r["ns"], "title": r["title"],
                                  "pageid": r["pageid"],
                                  "snippet": r.get("snippet", "")[:300]} for r in res]})
    else:
        zero_count += 1

print(f"terms: {len(terms)} | cached-missing: {len(terms)-zero_count-len(hits)-len(non200)} | "
      f"zeros: {zero_count} | non-200: {len(non200)} | hit-terms: {len(hits)}")
json.dump({"hits": hits, "non200": non200, "zeros": zero_count},
          open(os.path.join(RAWDIR, "hits-summary.json"), "w"), ensure_ascii=False, indent=1)

# ---- Stage 2: revision metadata for each distinct hit page ----
def api(params):
    q = urllib.parse.urlencode(params)
    for att in range(3):
        p = subprocess.run(["curl", "-sS", "--max-time", "60", "-A", UA, API + "?" + q],
                           capture_output=True, text=True)
        if p.returncode == 0 and p.stdout:
            try:
                return json.loads(p.stdout)
            except Exception:
                pass
        time.sleep(10 * (att + 1))
    return None

seen = {}
for h in hits:
    for r in h["results"]:
        seen.setdefault(r["pageid"], r["title"])

page_revs = {}
titles = list(seen.values())
# batch 20 titles per request
for i in range(0, len(titles), 20):
    batch = titles[i:i+20]
    d = api({"action": "query", "prop": "revisions", "titles": "|".join(batch),
             "rvlimit": 3, "rvprop": "ids|timestamp|user|comment|tags", "format": "json"})
    if not d:
        print("API FAIL on batch", i); continue
    for pg in d.get("query", {}).get("pages", {}).values():
        page_revs[str(pg["pageid"])] = {
            "pageid": pg["pageid"], "ns": pg["ns"], "title": pg["title"],
            "revisions": pg.get("revisions", [])}
    time.sleep(1.0)
    if i % 100 == 0:
        print(f"rev batches: {i}/{len(titles)}", flush=True)

json.dump(page_revs, open(os.path.join(RAWDIR, "page-revs.json"), "w"),
          ensure_ascii=False, indent=1)

# ---- Stage 3: heuristic pre-grade ----
temp_re = re.compile(r"^~2026-\d+$")
graded = []
for h in hits:
    pages = []
    for r in h["results"]:
        pr = page_revs.get(str(r["pageid"]), {})
        revs = pr.get("revisions", [])
        users = [x.get("user", "?") for x in revs]
        sandboxy = any(k in r["title"].lower() for k in
                       ["пясъчник", "sandbox", "тест", "test"])
        tempish = any(temp_re.match(u or "") for u in users)
        known = any(x.get("revid") in KNOWN_INCIDENT for x in revs)
        if known:
            pre = "known-incident?"
        elif tempish and sandboxy:
            pre = "INCIDENT-SHAPED-CANDIDATE"
        elif tempish:
            pre = "temp-user-check"
        else:
            pre = "likely-organic-or-noise"
        pages.append({"title": r["title"], "ns": r["ns"], "pageid": r["pageid"],
                      "snippet": r["snippet"], "recent_users": users,
                      "recent_revids": [x.get("revid") for x in revs],
                      "recent_ts": [x.get("timestamp") for x in revs],
                      "sandboxy": sandboxy, "tempish": tempish, "pre_grade": pre})
    graded.append({"term": h["term"], "category": h["category"],
                   "totalhits": h["totalhits"], "shown": len(h["results"]),
                   "pages": pages})

json.dump(graded, open(os.path.join(RAWDIR, "pre-graded.json"), "w"),
          ensure_ascii=False, indent=1)
n_cand = sum(1 for g in graded for p in g["pages"] if "CANDIDATE" in p["pre_grade"] or "check" in p["pre_grade"] or "known" in p["pre_grade"])
print(f"distinct hit pages: {len(seen)} | pre-graded terms: {len(graded)} | "
      f"flagged pages for manual review: {n_cand}")
for g in graded:
    for p in g["pages"]:
        if "CANDIDATE" in p["pre_grade"] or "check" in p["pre_grade"] or "known" in p["pre_grade"]:
            print("FLAG:", g["term"][:50], "|", p["title"], "|", p["pre_grade"], "|", p["recent_users"])
print("GRADE STAGE DONE")
