#!/usr/bin/env python3
"""Wordlist insource sweep worker for commons.wikimedia.org.

For EVERY term in search-terms.json, runs:
  action=query&list=search&srsearch=insource:"<term>"&srlimit=50&srnamespace=*&format=json
paced >=5.5s between requests. Caches EVERY response (hits AND zeros) in
raw/commons.wikimedia.org/insource-<n>.json with a TSV run log
(term, timestamp, http status, hit count). Resumable: skips indexes already cached.

Also pulls the 200 most recent revisions of the wiki's main sandbox
(Project:Sandbox) for the comment grep pass.
"""
import json, time, urllib.request, urllib.parse, os, sys, datetime

WORK = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/wordlist-wiki-sweep")
RAW = os.path.join(WORK, "raw/commons.wikimedia.org")
os.makedirs(RAW, exist_ok=True)
LOG_PATH = os.path.join(RAW, "run-log.tsv")
SUMMARY_PATH = os.path.join(RAW, "SUMMARY.json")

BASE = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "MuseWordlistSweep/1.0 (silent-locus wikipedia-lane research, BigSexyWarlock69)"}
PACE = 5.5

def utcnow():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def api_get(params, retries=3):
    url = BASE + "?" + urllib.parse.urlencode(params)
    last_status, last_err = None, None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                last_status = r.status
                return r.status, json.loads(r.read().decode("utf-8")), url, None
        except urllib.error.HTTPError as e:
            last_status = e.code
            last_err = "HTTPError %s" % e.code
            body = ""
            try: body = e.read().decode("utf-8", "replace")[:500]
            except Exception: pass
            last_err += " " + body
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(30)
                continue
            return e.code, None, url, last_err
        except Exception as e:
            last_err = "%s: %s" % (type(e).__name__, e)
            time.sleep(10)
    return last_status, None, url, last_err

terms = json.load(open(os.path.join(WORK, "search-terms.json")))["terms"]
print("terms: %d" % len(terms), flush=True)

need_log_header = not os.path.exists(LOG_PATH)
log = open(LOG_PATH, "a")
if need_log_header:
    log.write("index\tterm\tcategory\ttimestamp_utc\thttp_status\thits\turl\n")

summary = []
done = 0
for i, t in enumerate(terms):
    fn = os.path.join(RAW, "insource-%d.json" % i)
    if os.path.exists(fn):
        try:
            d = json.load(open(fn))
            summary.append({"index": i, "term": t["term"], "category": t["category"],
                            "hits": d.get("hits"), "status": d.get("http_status"),
                            "timestamp": d.get("timestamp")})
        except Exception:
            pass
        continue
    term = t["term"]
    srsearch = 'insource:"%s"' % term
    params = {"action": "query", "list": "search", "srsearch": srsearch,
              "srlimit": 50, "srnamespace": "*", "format": "json", "formatversion": 2}
    status, data, url, err = api_get(params)
    hits = None
    if data and "query" in data and "searchinfo" in data["query"]:
        hits = data["query"]["searchinfo"].get("totalhits", 0)
    ts = utcnow()
    cache = {"index": i, "term": term, "category": t["category"], "timestamp": ts,
             "http_status": status, "hits": hits, "url": url, "error": err,
             "response": data}
    with open(fn, "w") as f:
        json.dump(cache, f)
    log.write("%d\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
        i, term.replace("\t", " "), t["category"], ts, status, hits, url))
    log.flush()
    summary.append({"index": i, "term": term, "category": t["category"],
                    "hits": hits, "status": status, "timestamp": ts})
    done += 1
    if done % 25 == 0:
        print("[%s] %d/%d done" % (ts, i + 1, len(terms)), flush=True)
    time.sleep(PACE)

log.close()

# SUMMARY
cat_hits = {}
total_hits_terms = 0
errors = 0
for s in summary:
    if s["status"] != 200:
        errors += 1
    h = s["hits"] or 0
    cat_hits.setdefault(s["category"], [0, 0])
    cat_hits[s["category"]][0] += 1
    if h > 0:
        cat_hits[s["category"]][1] += 1
        total_hits_terms += 1

summ = {"wiki": "commons.wikimedia.org", "built_utc": utcnow(),
        "terms_queried": len(terms), "cached": len(summary),
        "terms_with_hits": total_hits_terms, "non_200": errors,
        "per_category": {c: {"terms": v[0], "with_hits": v[1]} for c, v in cat_hits.items()},
        "results": summary}
json.dump(summ, open(SUMMARY_PATH, "w"), indent=1)
print("insource sweep done: %d terms, %d with hits, %d non-200" % (len(terms), total_hits_terms, errors), flush=True)

# Sandbox 200-rev pull
print("pulling sandbox revisions...", flush=True)
params = {"action": "query", "prop": "revisions", "titles": "Project:Sandbox",
          "rvprop": "ids|timestamp|user|comment|tags", "rvlimit": 200,
          "format": "json", "formatversion": 2, "redirects": 1}
status, data, url, err = api_get(params)
sb = {"timestamp": utcnow(), "http_status": status, "url": url, "error": err,
      "response": data}
json.dump(sb, open(os.path.join(RAW, "sandbox-revisions.json"), "w"))
print("sandbox revisions: status=%s" % status, flush=True)
