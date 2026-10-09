#!/usr/bin/env python3
"""Wordlist insource: sweep worker for test.wikipedia.org.

One insource:"<term>" search per term (srlimit=50, srnamespace=*),
paced >=5.2s. Caches EVERY response (hits and zeros). Resumable via run-log.jsonl.
Do not commit. Do not touch main.
"""
import json, time, os, re, urllib.parse, urllib.request
from datetime import datetime, timezone

# NOTE (corrected 2026-10-07): CirrusSearch insource:"..." is a FULL-TEXT phrase
# search on the page-source index, NOT a regex (regex needs insource:/.../).
# Verified: escaped "\$\{7\*7\}" still returns 36,620 hits (tokens "7","7" in
# File: EXIF dumps) — escaping changes nothing in full-text mode. So keep the
# exact prior-sweep form: plain quoted phrase. Terms that tokenize to junk
# (e.g. "${7*7}") yield token-noise hits, graded as noise. The one term with
# a double quote has it stripped to avoid breaking the quoted-phrase syntax.
def phrase(term):
    return term.replace('"', '')

BASE = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/wordlist-wiki-sweep")
RAW = os.path.join(BASE, "raw", "test.wikipedia.org")
os.makedirs(RAW, exist_ok=True)
LOG = os.path.join(RAW, "run-log.jsonl")

terms = json.load(open(os.path.join(BASE, "search-terms.json")))["terms"]
print(f"[sweep] {len(terms)} terms, cache dir {RAW}", flush=True)

done = set()
if os.path.exists(LOG):
    with open(LOG) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                done.add(json.loads(line)["n"])
            except Exception:
                pass
print(f"[sweep] resuming: {len(done)} already logged", flush=True)

UA = {"User-Agent": "silent-locus-wiki-hunt/1.0 (agent-incident research; see https://security.wikimedia.org)"}

def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()

logf = open(LOG, "a")
t0 = time.time()
for n, t in enumerate(terms):
    if n in done:
        continue
    term = t["term"]
    sr = 'insource:"%s"' % phrase(term)  # plain quoted phrase, like prior sweeps
    t_req = time.time()
    url = ("https://test.wikipedia.org/w/api.php?action=query&list=search&srsearch="
           + urllib.parse.quote(sr)
           + "&srlimit=50&srnamespace=*&format=json")
    status, total, err = -1, -1, None
    for attempt in range(4):
        try:
            status, body = fetch(url)
            data = json.loads(body)
            total = data.get("query", {}).get("searchinfo", {}).get("totalhits", -1)
            with open(os.path.join(RAW, f"insource-{n}.json"), "wb") as fh:
                fh.write(body)
            break
        except Exception as e:
            err = "%r" % (e,)
            status = -2
            time.sleep(10 * (attempt + 1))
    logf.write(json.dumps({
        "n": n, "term": term, "category": t["category"],
        "ts_utc": datetime.now(timezone.utc).isoformat(),
        "http_status": status, "totalhits": total, "error": err,
    }) + "\n")
    logf.flush()
    if (len(done) + n + 1) % 50 == 0 or n == len(terms) - 1:
        el = time.time() - t0
        print(f"[sweep] n={n} done-this-run={n+1-len(done)} totalhits={total} elapsed={el/60:.1f}min", flush=True)
    # keep >=6s between request starts (task: >=5s between requests)
    gap = 6.0 - (time.time() - t_req)
    if gap > 0:
        time.sleep(gap)
logf.close()
print("[sweep] COMPLETE", flush=True)
