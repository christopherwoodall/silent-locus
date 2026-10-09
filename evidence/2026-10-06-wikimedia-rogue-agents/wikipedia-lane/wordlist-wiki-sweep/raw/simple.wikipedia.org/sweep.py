#!/usr/bin/env python3
"""simple.wikipedia.org insource: sweep worker. Caches EVERY response (hits and zeros)."""
import json, time, urllib.parse, urllib.request, datetime, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
TERMS = json.load(open(os.path.join(BASE, "..", "..", "search-terms.json")))["terms"]
WIKI = "simple.wikipedia.org"
UA = {"User-Agent": "silent-locus-wordlist-sweep/1.0 (research; contact: swarmtracers)"}

log = open(os.path.join(BASE, "run_log.tsv"), "a", buffering=1)
if os.path.getsize(log.name if hasattr(log,'name') else '') == 0:
    pass

def done_indices():
    s = set()
    for fn in os.listdir(BASE):
        if fn.startswith("insource-") and fn.endswith(".json"):
            try: s.add(int(fn[len("insource-"):-len(".json")]))
            except ValueError: pass
    return s

done = done_indices()
print(f"resuming: {len(done)}/{len(TERMS)} done", flush=True)

for i, t in enumerate(TERMS):
    if i in done:
        continue
    term = t["term"]
    q = f'insource:"{term}"'
    url = ("https://" + WIKI + "/w/api.php?action=query&list=search"
           "&srlimit=50&srnamespace=*&format=json&srsearch=" + urllib.parse.quote(q))
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            status = r.status
            body = r.read().decode("utf-8", "replace")
    except Exception as e:
        status = f"ERR:{type(e).__name__}"
        body = json.dumps({"error": str(e)})
    try:
        j = json.loads(body)
        hits = len(j.get("query", {}).get("search", []))
        total = j.get("query", {}).get("searchinfo", {}).get("totalhits", hits)
    except Exception:
        hits, total = -1, -1
    with open(os.path.join(BASE, f"insource-{i}.json"), "w") as f:
        f.write(body)
    log.write(f"{i}\t{term}\t{t['category']}\t{ts}\t{status}\t{hits}\t{total}\n")
    if hits and hits > 0:
        print(f"[{i}] HIT({total}) {t['category']} :: {term[:80]}", flush=True)
    time.sleep(5.2)

log.close()
print("SWEEP COMPLETE", flush=True)
