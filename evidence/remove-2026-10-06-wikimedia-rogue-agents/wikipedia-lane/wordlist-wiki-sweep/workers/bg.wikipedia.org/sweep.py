#!/usr/bin/env python3
"""Wordlist wiki sweep worker — bg.wikipedia.org.
insource:"<term>" exact-phrase content search via MediaWiki API,
paced >=5.5s between requests. Caches EVERY response (hits AND zeros).
Run log: run-log.jsonl (term, category, ts_utc, http_status, totalhits).
Resumable: skips n already cached.
"""
import json, os, subprocess, sys, time, urllib.parse, datetime

BASE_DIR = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/wordlist-wiki-sweep")
TERMS_FILE = os.path.join(BASE_DIR, "search-terms.json")
RAWDIR = os.path.join(BASE_DIR, "raw", "bg.wikipedia.org")
RUNLOG = os.path.join(RAWDIR, "run-log.jsonl")
API = "https://bg.wikipedia.org/w/api.php"
UA = "silent-locus-wordlist-sweep/1.0 (academic research; bg.wikipedia.org worker)"
PACE = 5.5  # seconds between request starts (min)

os.makedirs(RAWDIR, exist_ok=True)

with open(TERMS_FILE) as f:
    terms = json.load(f)["terms"]
print(f"loaded {len(terms)} terms", flush=True)

# discover already-cached
done = set()
if os.path.exists(RUNLOG):
    with open(RUNLOG) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                done.add(json.loads(line)["n"])
            except Exception:
                pass
print(f"already cached: {len(done)}", flush=True)

def search_term(term):
    sr = 'insource:"%s"' % term
    q = urllib.parse.urlencode({
        "action": "query", "list": "search", "srsearch": sr,
        "srlimit": 50, "srnamespace": "*", "format": "json",
    })
    url = API + "?" + q
    for attempt in range(3):
        p = subprocess.run(
            ["curl", "-sS", "--max-time", "60", "-A", UA, url],
            capture_output=True, text=True)
        body = p.stdout
        if p.returncode == 0 and body:
            try:
                data = json.loads(body)
                si = data.get("query", {}).get("searchinfo", {})
                return 200, data, si.get("totalhits")
            except Exception as e:
                return 200, {"_raw_parse_error": str(e), "_raw_head": body[:2000]}, None
        time.sleep(10 * (attempt + 1))
    return 599, {"_error": "curl failed", "_stderr": p.stderr[:500]}, None

with open(RUNLOG, "a") as log:
    for n, t in enumerate(terms):
        if n in done:
            continue
        t0 = time.time()
        ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        status, data, totalhits = search_term(t["term"])
        path = os.path.join(RAWDIR, f"insource-{n}.json")
        with open(path, "w") as f:
            json.dump({"term": t["term"], "category": t["category"], "ts_utc": ts,
                       "http_status": status, "totalhits": totalhits,
                       "response": data}, f, ensure_ascii=False)
        log.write(json.dumps({"n": n, "term": t["term"], "category": t["category"],
                              "ts_utc": ts, "http_status": status,
                              "totalhits": totalhits}) + "\n")
        log.flush()
        if n % 50 == 0:
            print(f"[{n}/{len(terms)}] {t['term'][:40]!r} hits={totalhits}", flush=True)
        elapsed = time.time() - t0
        if elapsed < PACE:
            time.sleep(PACE - elapsed)

print("SWEEP COMPLETE", flush=True)
