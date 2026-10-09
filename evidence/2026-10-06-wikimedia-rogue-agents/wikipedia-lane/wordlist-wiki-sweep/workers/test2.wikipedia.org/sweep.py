#!/usr/bin/env python3
"""test2.wikipedia.org wordlist sweep worker.
For each of the 1,148 terms: insource: exact-phrase search via MediaWiki API,
paced >=5s between requests. Caches EVERY response (hits AND zeros).
Also pulls the 200 most recent Project:Sandbox revisions for comment grepping.
"""
import json, os, re, subprocess, sys, time, urllib.parse
from datetime import datetime, timezone

WIKI = "test2.wikipedia.org"
BASE = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/wordlist-wiki-sweep")
RAW = os.path.join(BASE, "raw", WIKI)
TERMS_FILE = os.path.join(BASE, "search-terms.json")
PACE = 5.5  # seconds between requests (>=5s per brief)

KNOWN_OLDIDS = {
    7226103, 7226104, 7226105, 7226108, 7226111, 7226107, 7226109, 7226110,
    30732655, 1238390511, 8370994, 8370995, 741399, 741400, 612932, 612933,
    612931, 8370989, 1356314507, 1356419247, 744412, 613856, 1233683454,
    10891416, 747327, 744271, 741405, 1353498400, 744270, 744272, 1213503714,
    1213503789, 1213513506, 1353492663, 1213399057,
}

REGEX_TERMS = {
    'oai[0-9]+': 'insource:/oai[0-9]+/',
    'zz=oai[0-9]+': 'insource:/zz=oai[0-9]+/',
    'prep[0-9]{17,} as query-param key': 'insource:/prep[0-9]{17,}/',
}

def build_srsearch(term):
    if term in REGEX_TERMS:
        return REGEX_TERMS[term]
    if '"' in term:
        # regex-escape the whole literal so embedded quotes are safe
        return 'insource:/' + re.escape(term) + '/'
    return 'insource:"' + term + '"'

def api_get(params, retries=4):
    qs = urllib.parse.urlencode(params)
    url = f"https://{WIKI}/w/api.php?{qs}"
    last = None
    for attempt in range(retries):
        try:
            r = subprocess.run(
                ["curl", "-sS", "--max-time", 45,
                 "-H", "User-Agent: silent-locus-wordlist-sweep/1.0 (research; test2.wikipedia.org worker)",
                 "-w", "\n%{http_code}", url],
                capture_output=True, text=True, timeout=60)
            out = r.stdout.rsplit("\n", 1)
            body, code = (out[0], out[1]) if len(out) == 2 else (r.stdout, "000")
            if code == "200":
                return int(code), json.loads(body)
            last = (code, body[:300])
        except Exception as e:
            last = ("EXC", str(e)[:300])
        time.sleep(10 + attempt * 10)
    return (int(last[0]) if str(last[0]).isdigit() else 0), last[1]

def main():
    os.makedirs(RAW, exist_ok=True)
    terms = json.load(open(TERMS_FILE))["terms"]
    log_path = os.path.join(RAW, "run-log.jsonl")
    summary = {"wiki": WIKI, "started_utc": datetime.now(timezone.utc).isoformat(),
               "terms_total": len(terms), "requests": [], "errors": 0}
    print(f"[test2] {len(terms)} terms, pacing {PACE}s", flush=True)
    logf = open(log_path, "w")
    for i, t in enumerate(terms):
        term, cat = t["term"], t["category"]
        sr = build_srsearch(term)
        code, data = api_get({
            "action": "query", "list": "search", "srsearch": sr,
            "srlimit": 50, "srnamespace": "*", "format": "json",
        })
        ts = datetime.now(timezone.utc).isoformat()
        if code != 200:
            summary["errors"] += 1
            hits = data if isinstance(data, list) else []
            rec = {"n": i, "term": term, "category": cat, "timestamp": ts,
                   "http": code, "totalhits": -1, "note": "request failed",
                   "raw_file": None}
        else:
            totalhits = data["query"]["searchinfo"]["totalhits"]
            hits = [{"pageid": h["pageid"], "ns": h["ns"], "title": h["title"],
                     "timestamp": h["timestamp"], "size": h.get("size")}
                    for h in data["query"]["search"]]
            fn = f"insource-{i:04d}.json"
            with open(os.path.join(RAW, fn), "w") as f:
                json.dump({"n": i, "term": term, "category": cat, "srsearch": sr,
                           "retrieved_utc": ts, "http": code,
                           "totalhits": totalhits, "results": hits}, f, indent=2)
            rec = {"n": i, "term": term, "category": cat, "timestamp": ts,
                   "http": code, "totalhits": totalhits, "raw_file": fn}
        logf.write(json.dumps(rec) + "\n"); logf.flush()
        summary["requests"].append(rec)
        if (i + 1) % 100 == 0:
            print(f"[test2] {i+1}/{len(terms)} done", flush=True)
        time.sleep(PACE)
    summary["finished_utc"] = datetime.now(timezone.utc).isoformat()
    json.dump(summary, open(os.path.join(RAW, "SUMMARY.json"), "w"), indent=2)
    logf.close()
    print("[test2] insource sweep complete; pulling Project:Sandbox revisions", flush=True)

    # --- Sandbox revisions: 200 most recent, for comment grepping ---
    code, data = api_get({
        "action": "query", "titles": "Project:Sandbox", "prop": "revisions",
        "rvlimit": 200, "rvprop": "ids|timestamp|user|comment|tags|flags",
        "rvslots": "main", "format": "json",
    })
    ts = datetime.now(timezone.utc).isoformat()
    sb_path = os.path.join(RAW, "sandbox-revisions.json")
    if code == 200:
        pages = data["query"]["pages"]
        revs = []
        for pid, p in pages.items():
            for r in p.get("revisions", []):
                revs.append(r)
        json.dump({"retrieved_utc": ts, "http": code, "title": "Project:Sandbox",
                   "rev_count": len(revs), "revisions": revs},
                  open(sb_path, "w"), indent=2)
        # comment grep: case-insensitive substring of every term
        lowered = [(r.get("revid"), (r.get("comment") or "")) for r in revs]
        matches = []
        for ti, t in enumerate(terms):
            needle = t["term"].lower()
            for revid, comment in lowered:
                if needle and needle in comment.lower():
                    matches.append({"term_index": ti, "term": t["term"],
                                    "category": t["category"], "revid": revid,
                                    "comment": comment})
        json.dump({"retrieved_utc": ts, "terms_searched": len(terms),
                   "sandbox_revs": len(revs), "matches": matches},
                  open(os.path.join(RAW, "sandbox-comment-grep.json"), "w"), indent=2)
        print(f"[test2] sandbox revs={len(revs)} comment-matches={len(matches)}", flush=True)
    else:
        json.dump({"retrieved_utc": ts, "http": code, "error": True},
                  open(sb_path, "w"))
        print(f"[test2] SANDBOX FETCH FAILED http={code}", flush=True)
    print("[test2] DONE", flush=True)

if __name__ == "__main__":
    main()
