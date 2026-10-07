#!/usr/bin/env python3
"""Wordlist-wiki-sweep worker for www.mediawiki.org.

For each of 1,148 search terms: MediaWiki API insource: exact-phrase search,
srlimit=50, srnamespace=*, paced >=5s. Caches every response (hits AND zeros)
in raw/www.mediawiki.org/insource-<n>.json with a JSONL run log.

Resume-safe: skips terms whose insource-<n>.json already exists.
"""
import json, os, subprocess, sys, time, urllib.parse
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "raw", "www.mediawiki.org")
LOG = os.path.join(RAW, "run-log.jsonl")
UA = "silent-locus-wiki-sweep/1.0 (research; contact via repo)"
PACING = 5.2  # seconds between request starts (>=5 per task)
API = "https://www.mediawiki.org/w/api.php"

os.makedirs(RAW, exist_ok=True)

with open(os.path.join(BASE, "search-terms.json")) as f:
    terms = json.load(f)["terms"]

# map term index -> existing outfile
done = set()
for fn in os.listdir(RAW):
    if fn.startswith("insource-") and fn.endswith(".json"):
        try:
            done.add(int(fn[len("insource-"):-len(".json")]))
        except ValueError:
            pass

log_f = open(LOG, "a")

total_hits = 0
new_hits = 0
start_all = time.time()
for n, t in enumerate(terms):
    out = os.path.join(RAW, f"insource-{n}.json")
    if n in done and os.path.exists(out):
        continue
    term = t["term"]
    # escape embedded double quotes for the insource:"..." phrase query
    phrase = term.replace('"', '\\"')
    srsearch = f'insource:"{phrase}"'
    params = {
        "action": "query", "list": "search", "srsearch": srsearch,
        "srlimit": "50", "srnamespace": "*", "format": "json",
        "formatversion": "2",
    }
    qs = "&".join(f"{k}={urllib.parse.quote(v, safe='')}" for k, v in params.items())
    url = API + "?" + qs
    ts = datetime.now(timezone.utc).isoformat()
    status, hit_count = -1, -1
    body = b""
    t0 = time.time()
    try:
        r = subprocess.run(
            ["curl", "-sS", "-m", "45", "-A", UA, "-w", "\n%{http_code}", url],
            capture_output=True, timeout=60)
        out_raw = r.stdout
        status = int(out_raw.rsplit(b"\n", 1)[-1].strip() or -1)
        body = out_raw.rsplit(b"\n", 1)[0]
        with open(out, "wb") as f:
            f.write(body)
        if status == 200:
            data = json.loads(body.decode("utf-8", "replace"))
            q = data.get("query", {})
            hit_count = int(q.get("searchinfo", {}).get("totalhits", -1))
            if hit_count > 0:
                new_hits += 1
                total_hits += hit_count
    except Exception as e:
        status = -2
        with open(out + ".error", "w") as f:
            f.write(f"{type(e).__name__}: {e}\n")
    rec = {"n": n, "term": term, "category": t.get("category", ""),
           "timestamp_utc": ts, "http_status": status, "hit_count": hit_count}
    log_f.write(json.dumps(rec) + "\n")
    log_f.flush()
    if hit_count and hit_count > 0:
        print(f"[{n}] HIT({hit_count}): {term!r}", flush=True)
    # pace: >=5s between request starts
    wait = PACING - (time.time() - t0)
    if wait > 0:
        time.sleep(wait)

log_f.close()
print(f"DONE: {len(terms)} terms, {new_hits} terms with hits, {total_hits} raw hit records, "
      f"elapsed {time.time()-start_all:.0f}s", flush=True)
