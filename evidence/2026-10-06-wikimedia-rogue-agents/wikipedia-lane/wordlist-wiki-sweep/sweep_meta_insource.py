#!/usr/bin/env python3
"""meta.wikimedia.org wordlist insource sweep + sandbox comment grep.
1,148 terms, paced >=5.5s between requests. Caches every response."""
import json, os, time, datetime, urllib.request, urllib.parse, urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "raw", "meta.wikimedia.org")
os.makedirs(RAW, exist_ok=True)
API = "https://meta.wikimedia.org/w/api.php"
UA = "silent-locus-wordlist-wiki-sweep/1.0 (research; meta.wikimedia.org only)"

def api_get(params, timeout=60):
    q = urllib.parse.urlencode(params)
    req = urllib.request.Request(API + "?" + q, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return -1, None

def main():
    terms = json.load(open(os.path.join(BASE, "search-terms.json")))["terms"]
    log = open(os.path.join(RAW, "RUNLOG.tsv"), "a", buffering=1)
    done = set()
    try:
        for line in open(os.path.join(RAW, "RUNLOG.tsv")):
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 6:
                done.add(int(parts[0]))
    except FileNotFoundError:
        pass
    if not done:
        log.write("n\tterm\ttimestamp_utc\thttp_status\thit_count\terror\n")

    for n, t in enumerate(terms):
        if n in done:
            continue
        term = t["term"]
        srsearch = 'insource:"%s"' % term
        status, data = -1, None
        err = ""
        for attempt in range(3):
            t0 = time.time()
            status, data = api_get({
                "action": "query", "list": "search",
                "srsearch": srsearch, "srlimit": 50,
                "srnamespace": "*", "format": "json",
                "formatversion": "2",
            })
            elapsed = time.time() - t0
            if status == 200 and data is not None:
                break
            err = "attempt%d status=%s" % (attempt + 1, status)
            time.sleep(10 * (attempt + 1))
        else:
            pass
        hits = 0
        if data and isinstance(data, dict) and "query" in data:
            hits = len(data["query"].get("search", []))
            data["_meta"] = {"n": n, "term": term, "srsearch": srsearch,
                             "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                             "http_status": status}
            with open(os.path.join(RAW, "insource-%d.json" % n), "w") as f:
                json.dump(data, f)
        else:
            with open(os.path.join(RAW, "insource-%d.json" % n), "w") as f:
                json.dump({"_meta": {"n": n, "term": term, "srsearch": srsearch,
                                     "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                     "http_status": status, "error": err}}, f)
        ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
        log.write("%d\t%s\t%s\t%d\t%d\t%s\n" % (n, term.replace("\t", " "), ts, status, hits, err))
        time.sleep(max(0, 5.5 - (time.time() - t0)))
    log.close()

    # Sandbox revision comments
    status, data = api_get({
        "action": "query", "prop": "revisions",
        "titles": "Meta:Sandbox",
        "rvprop": "ids|timestamp|user|comment|tags",
        "rvlimit": 200, "format": "json", "formatversion": "2",
    })
    if data:
        with open(os.path.join(RAW, "sandbox-comments-meta.json"), "w") as f:
            json.dump({"retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                       "http_status": status, "data": data}, f)
    print("DONE insource sweep + sandbox comments")

if __name__ == "__main__":
    main()
