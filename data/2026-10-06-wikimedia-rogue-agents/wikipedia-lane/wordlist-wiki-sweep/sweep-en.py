#!/usr/bin/env python3
"""Wordlist wiki sweep worker: en.wikipedia.org insource: search over all 1,148 terms.
Paced >=5.2s between requests. Caches EVERY response (hits and zeros).
Run log: raw/en.wikipedia.org/run-log.csv. Summary: raw/en.wikipedia.org/SUMMARY.json.
Does NOT commit anything. Launched by the en.wikipedia.org sweep worker 2026-10-06.
"""
import csv, json, time, urllib.parse, urllib.request
from datetime import datetime, timezone

BASE = "https://en.wikipedia.org/w/api.php"
UA = "wordlist-wiki-sweep/1.0 (research; en.wikipedia.org IOC hunt; contact via repo)"
WORKDIR = "/home/hatch/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/wordlist-wiki-sweep"
RAW = WORKDIR + "/raw/en.wikipedia.org"

def fetch(term, retries=3):
    # escape literal double-quotes so the insource:"..." phrase stays intact
    phrase = term.replace('"', '\\"')
    srsearch = 'insource:"%s"' % phrase
    params = {
        "action": "query", "list": "search", "srsearch": srsearch,
        "srlimit": "50", "srnamespace": "*", "format": "json",
    }
    url = BASE + "?" + urllib.parse.urlencode(params)
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp:
                status = resp.status
                body = resp.read()
                return status, body, None
        except Exception as e:
            last_err = repr(e)
            time.sleep(10)
    return 0, b"", last_err

def main():
    terms = json.load(open(WORKDIR + "/search-terms.json"))["terms"]
    log_path = RAW + "/run-log.csv"
    summary = []
    with open(log_path, "w", newline="") as lf:
        w = csv.writer(lf)
        w.writerow(["n", "term", "timestamp_utc", "http_status", "totalhits", "error"])
        for n, t in enumerate(terms):
            term = t["term"]
            ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            status, body, err = fetch(term)
            totalhits = None
            if status == 200 and body:
                try:
                    d = json.loads(body)
                    totalhits = d["query"]["searchinfo"]["totalhits"]
                    hits = d["query"]["search"]
                    d["_sweep"] = {"n": n, "term": term, "category": t["category"],
                                   "fetched_utc": ts, "http_status": status}
                    body = json.dumps(d, indent=1).encode()
                except Exception as e:
                    err = (err or "") + " parse:" + repr(e)
                    status = 0
            out = "%s/insource-%d.json" % (RAW, n)
            with open(out, "wb") as f:
                f.write(body if body else b"{}")
            w.writerow([n, term, ts, status, totalhits, err or ""])
            lf.flush()
            summary.append({"n": n, "term": term, "category": t["category"],
                            "totalhits": totalhits, "http_status": status, "error": err})
            if (n + 1) % 50 == 0:
                print("done %d/%d" % (n + 1, len(terms)), flush=True)
            time.sleep(5.2)
    json.dump({"completed_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "terms": summary},
              open(RAW + "/SUMMARY.json", "w"), indent=1)
    print("SWEEP COMPLETE: %d terms" % len(terms))

if __name__ == "__main__":
    main()
