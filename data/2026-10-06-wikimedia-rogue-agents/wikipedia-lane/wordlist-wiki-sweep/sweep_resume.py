#!/usr/bin/env python3
"""Resume-capable wordlist wiki sweep for one wiki host.
Skips term indices already in raw/<wiki>/run-log.csv. Paces >=5.2s.
Usage: sweep_resume.py <wiki-host>   (e.g. en.wikipedia.org)
"""
import csv, json, sys, time, urllib.request, urllib.parse, os
from datetime import datetime, timezone

BASE = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/wordlist-wiki-sweep")
UA = "wordlist-wiki-sweep/1.0 (research; IOC hunt; contact via repo)"

# Terms whose insource: PHRASE query is mangled by CirrusSearch (special chars
# degrade to wildcards / giant false-positive sets). Searched instead as
# insource: REGEX with the srsearch value given here (already URL-shaped).
SPECIAL_REGEX = {
    "${7*7}": r"insource:/\$\{7\*7\}/",
    "oai[0-9]+": r"insource:/oai[0-9]+/",
    "zz=oai[0-9]+": r"insource:/zz=oai[0-9]+/",
}

def build_srsearch(term):
    if term in SPECIAL_REGEX:
        return SPECIAL_REGEX[term]
    t = term.replace('"', '\\"')
    return f'insource:"{t}"'

def main():
    host = sys.argv[1]
    rawdir = os.path.join(BASE, "raw", host)
    os.makedirs(rawdir, exist_ok=True)
    terms = json.load(open(os.path.join(BASE, "search-terms.json")))["terms"]
    logpath = os.path.join(rawdir, "run-log.csv")
    done = set()
    if os.path.exists(logpath):
        with open(logpath) as f:
            for row in csv.DictReader(f):
                done.add(int(row["n"]))
    remaining = [n for n in range(len(terms)) if n not in done]
    print(f"[{host}] {len(done)}/{len(terms)} done, {len(remaining)} remaining", flush=True)
    logf = open(logpath, "a", newline="")
    lw = csv.writer(logf)
    if not done:
        lw.writerow(["n", "term", "timestamp_utc", "http_status", "totalhits", "error"])
    for n in remaining:
        t = terms[n]
        srsearch = build_srsearch(t["term"])
        q = urllib.parse.quote(srsearch)
        url = f"https://{host}/w/api.php?action=query&list=search&srsearch={q}&srlimit=50&srnamespace=*&format=json&formatversion=2"
        status, totalhits, err, body = None, None, "", None
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=60) as r:
                    status = r.status
                    body = r.read().decode("utf-8", "replace")
                d = json.loads(body)
                totalhits = d.get("query", {}).get("searchinfo", {}).get("totalhits")
                break
            except Exception as e:
                err = f"{type(e).__name__}: {e}"[:200]
                time.sleep(10)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if body is not None:
            env = {"_sweep": {"n": n, "term": t["term"], "category": t["category"],
                              "fetched_utc": ts, "http_status": status},
                   "response": json.loads(body)}
            with open(os.path.join(rawdir, f"insource-{n}.json"), "w") as f:
                json.dump(env, f)
        lw.writerow([n, t["term"], ts, status or "", totalhits if totalhits is not None else "", err])
        logf.flush()
        if n % 25 == 0:
            print(f"[{host}] n={n} totalhits={totalhits} {t['term'][:40]}", flush=True)
        time.sleep(5.2)
    logf.close()
    print(f"[{host}] DONE", flush=True)

main()
