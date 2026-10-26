#!/usr/bin/env python3
"""urlscan crawl executor 2026-10-26. Anonymous API only, 1 req / 2s.
Idempotent: skips a query whose raw/search.json already parses."""
import hashlib, json, os, time, urllib.parse, urllib.request, urllib.error, datetime

BASE = os.path.expanduser("~/workspace/silent-locus/reports/urlscan-crawl-2026-10-26")
UA = "silent-locus-lane-scanner/1.0 (+hunt: chinese-amap-fleet)"
QUERIES = [
    ("getpoiinfo", "getPoiInfo"),
    ("uqscan-tag", "uqscan="),
    ("uqframe-tag", "uqframe="),
    ("proxy-marker", "hysandbox"),
    ("relay-jina-reader", "domain:r.jina.ai"),
    ("title-amap", 'page.title:"amap"'),
]

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def log(line):
    with open(os.path.join(BASE, "crawl-progress.log"), "a") as f:
        f.write(line + "\n")
    print(line, flush=True)

os.makedirs(os.path.join(BASE, "raw/screenshots"), exist_ok=True)
for i, (label, q) in enumerate(QUERIES):
    d = os.path.join(BASE, "raw", label)
    os.makedirs(d, exist_ok=True)
    out = os.path.join(d, "search.json")
    if os.path.exists(out):
        try:
            data = json.load(open(out))
            if isinstance(data, dict) and "total" in data and "results" in data:
                ts = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
                log(f"{ts} SKIP existing-complete label={label} query={q} total={data['total']} fetched={len(data['results'])}")
                continue
        except Exception:
            pass
    if i > 0:
        time.sleep(2.0)
    url = f"https://urlscan.io/api/v1/search/?q={urllib.parse.quote(q, safe='')}&size=100"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            status = resp.status
            body = resp.read()
    except urllib.error.HTTPError as e:
        log(f"{ts} label={label} query={q} HTTP={e.code} total=NA fetched=0 error=HTTPError")
        if e.code == 429:
            print("HARD STOP 429", flush=True)
            break
        continue
    except Exception as e:
        log(f"{ts} label={label} query={q} HTTP=-1 total=NA fetched=0 error={type(e).__name__}:{e}")
        continue
    with open(out, "wb") as f:
        f.write(body)
    try:
        data = json.loads(body)
        total, fetched = data.get("total"), len(data.get("results", []))
    except Exception:
        total, fetched = "unparsed", 0
    with open(os.path.join(d, ".PROVENANCE.txt"), "w") as f:
        f.write(f"source URL: {url}\nretrieval time (UTC): {ts}\nmethod: curl-equivalent anonymous GET via python urllib (same urlscan.io/api/v1/search endpoint, User-Agent silent-locus-lane-scanner/1.0)\nHTTP status: {status}\n")
    with open(out + ".sha256", "w") as f:
        f.write(f"{sha(out)}  search.json\n")
    with open(os.path.join(d, ".PROVENANCE.txt.sha256"), "w") as f:
        f.write(f"{sha(os.path.join(d, '.PROVENANCE.txt'))}  .PROVENANCE.txt\n")
    log(f"{ts} label={label} query={q} HTTP={status} total={total} fetched={fetched}")
print("DONE")
