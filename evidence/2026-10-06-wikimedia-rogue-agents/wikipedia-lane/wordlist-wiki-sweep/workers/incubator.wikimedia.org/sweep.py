#!/usr/bin/env python3
"""Wordlist-wiki-sweep worker for incubator.wikimedia.org.

For each of 1,148 terms: insource:"<term>" via MediaWiki API list=search,
srlimit=50, srnamespace=*, paced >=5s. Caches EVERY response (hits and zeros).
Also pulls 200 most recent revisions of Incubator:Sandbox and greps edit
comments case-insensitively for all terms.

Usage: run from the wordlist-wiki-sweep/ dir. Run log: raw/incubator.wikimedia.org/RUNLOG.jsonl
"""
import json, os, subprocess, sys, time, urllib.parse, datetime, re

API = "https://incubator.wikimedia.org/w/api.php"
OUTDIR = "raw/incubator.wikimedia.org"
os.makedirs(OUTDIR, exist_ok=True)
RUNLOG = os.path.join(OUTDIR, "RUNLOG.jsonl")
PACE = 5.2  # seconds between request starts

KNOWN_INCIDENT_OLDIDS = {
    7226103, 7226104, 7226105, 7226108, 7226111, 7226107, 7226109, 7226110,
    30732655, 1238390511, 8370994, 8370995, 741399, 741400, 612932, 612933,
    612931, 8370989, 1356314507, 1356419247, 744412, 613856, 1233683454,
    10891416, 747327, 744271, 741405, 1353498400, 744270, 744272, 1213503714,
    1213503789, 1213513506, 1353492663, 1213399057,
}

def curl_json(url):
    """GET via curl; returns (http_status, parsed_or_raw_body)."""
    for attempt in (1, 2):
        p = subprocess.run(
            ["curl", "-sS", "--max-time", "60", "-w", "\n%{http_code}",
             "--compressed", "-A", "silent-locus-wordlist-sweep/1.0 (contact via edit summary)",
             url],
            capture_output=True, text=True)
        body, _, code = p.stdout.rpartition("\n")
        try:
            status = int(code.strip())
        except ValueError:
            status = 0
        if status == 200:
            try:
                return status, json.loads(body)
            except json.JSONDecodeError:
                return status, {"_raw_unparseable": body[:2000]}
        time.sleep(15)
    return status, {"_error": "non-200 after retry", "_stdout_tail": p.stdout[-500:]}

def search_insource(term):
    params = {"action": "query", "list": "search",
              "srsearch": 'insource:"%s"' % term,
              "srlimit": "50", "srnamespace": "*", "format": "json"}
    return curl_json(API + "?" + urllib.parse.urlencode(params))

def log(entry):
    with open(RUNLOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def main():
    terms = json.load(open("search-terms.json"))["terms"]
    start_n = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    end_n = int(sys.argv[2]) if len(sys.argv) > 2 else len(terms)
    print(f"sweeping terms [{start_n}:{end_n}) of {len(terms)}", flush=True)
    last = 0.0
    for n in range(start_n, end_n):
        t = terms[n]
        term, cat = t["term"], t["category"]
        out = os.path.join(OUTDIR, f"insource-{n:04d}.json")
        if os.path.exists(out) and os.path.getsize(out) > 0:
            # resume: skip already-done
            try:
                d = json.load(open(out))
                hits = d.get("query", {}).get("searchinfo", {}).get("totalhits", -1)
                log({"n": n, "term": term, "category": cat, "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                     "http": 200, "hits": hits, "note": "resumed-skip"})
                continue
            except Exception:
                pass
        wait = PACE - (time.time() - last)
        if wait > 0:
            time.sleep(wait)
        last = time.time()
        status, data = search_insource(term)
        with open(out, "w") as f:
            json.dump({"term": term, "category": cat, "url": "insource:" + term,
                       "response": data}, f, ensure_ascii=False)
        hits = -1
        if isinstance(data, dict):
            hits = data.get("query", {}).get("searchinfo", {}).get("totalhits", -1)
        log({"n": n, "term": term, "category": cat,
             "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
             "http": status, "hits": hits})
        if n % 50 == 49:
            print(f"  ...{n+1} done, last term={term!r} hits={hits}", flush=True)
    print("done", flush=True)

if __name__ == "__main__":
    main()
