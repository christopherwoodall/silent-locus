#!/usr/bin/env python3
"""One-shot gap-fill for wordlist wiki sweep.
Usage: gapfill.py <wiki-host>
Fetches only term indices missing as raw/<host>/insource-<n>.json.
Paces >=5.2s, 3 attempts, 60s timeout. Appends to run-log.csv.
"""
import csv, json, sys, time, re, urllib.request, urllib.parse, os
from datetime import datetime, timezone

BASE = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/wordlist-wiki-sweep")
UA = "wordlist-wiki-sweep/1.0 (research; IOC hunt; contact via repo)"

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
    have = set()
    for f in os.listdir(rawdir):
        m = re.match(r"insource-0*(\d+)\.json$", f)
        if not m:
            continue
        idx = int(m.group(1))
        # Only count new-format captures (with _sweep envelope). Old-format
        # files (zero-padded, no _sweep) may carry mangled-query hit counts
        # and must be re-fetched.
        try:
            with open(os.path.join(rawdir, f)) as fh:
                env = json.load(fh)
            if "_sweep" in env and env["_sweep"].get("n") == idx:
                have.add(idx)
        except Exception:
            pass
    remaining = sorted(set(range(len(terms))) - have)
    print(f"[{host}] {len(have)}/{len(terms)} have, {len(remaining)} to fetch", flush=True)
    logpath = os.path.join(rawdir, "run-log.csv")
    newlog = not os.path.exists(logpath)
    logf = open(logpath, "a", newline="")
    lw = csv.writer(logf)
    if newlog:
        lw.writerow(["n", "term", "timestamp_utc", "http_status", "totalhits", "error"])
    done_n = 0
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
        done_n += 1
        if done_n % 25 == 0 or done_n == len(remaining):
            print(f"[{host}] {done_n}/{len(remaining)} n={n} totalhits={totalhits} {t['term'][:40]}", flush=True)
        time.sleep(5.2)
    logf.close()
    print(f"[{host}] DONE", flush=True)

main()
