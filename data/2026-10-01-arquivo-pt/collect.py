#!/usr/bin/env python3
"""Collection worker, lane 1/4: Arquivo.pt capture metadata for Transluce
us-canada-gov incident targets (notes/transluce-us-canada-gov-2026-10-01.md).

Pulls CDX capture metadata (timestamps, original URLs, status, digests)
for each incident target + padded window. Streams raw JSONL to raw/.
Modest rate: >=1.5s between requests, backoff on 429/503, hard stop on
explicit rejection. No full page bodies.

Run: python3 collect.py  (writes raw/<slug>.cdx.jsonl + collect.log.jsonl)
"""
import json, time, gzip, urllib.request, urllib.parse, urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
RAW.mkdir(exist_ok=True)
LOG = HERE / "collect.log.jsonl"

# slug, hosts (domain match), incident window, notes
TARGETS = [
    ("kansas-kansasmemory",  ["kansasmemory.gov"],              "2026-05-07", "2026-05-07", "36,578 captures per Transluce"),
    ("maryland-edstats",     ["msde.maryland.gov"],  # domain match covers reportcard.* too
                                                                          "2026-05-06", "2026-05-06", "295,912 captures; multiple hosts"),
    ("illinois-iquery",      ["iquery.illinois.gov"],           "2026-04-19", "2026-05-01", "251 captures; legacy IQuery portal"),
    ("lac-collectionsearch", ["bac-lac.gc.ca", "recherche-collection-search.bac-lac.canada.ca"],
                                                                          "2026-05-28", "2026-06-09", "899 requests May 28 + Jun 9; divorce records; payloads on the canada.ca frontend host"),
    ("doe-crdc",             ["civilrightsdata.ed.gov"],        "2026-06-17", "2026-06-17", "200,000+ requests; State_Id=1 OR 1=1 probe"),
    ("bea-api",              ["apps.bea.gov"],                  "2026-06-16", "2026-06-18", "3,005 captures; API-key registration"),
    ("omb-max",              ["portal.max.gov"],                "2026-05-25", "2026-05-27", "MAX.gov; Transluce evidence is urlquery-based"),
    ("navy-history",         ["history.navy.mil"],              "2026-04-23", "2026-05-18", "Apr 23-24 + May 18 probing"),
    ("doj-ojjdp",            ["ojjdp.ncjrs.gov", "ojjdp.ojp.gov"],
                                                                          "2026-05-30", "2026-05-31", "OJJDP arrest stats; encoded parent-dir"),
    ("sec",                  ["www.sec.gov"],                   "2026-06-18", "2026-06-18", "county.json; urlquery-corroborated cluster"),
    ("cdc-wonder",           ["wonder.cdc.gov"],                "2026-07-18", "2026-07-18", "WONDER form submission (probe=0)"),
    ("calaccess",            ["cal-access.sos.ca.gov"],         "2026-05-26", "2026-05-26", "CAL-ACCESS antibot bypass"),
    ("nysed-enrollment",     ["data.nysed.gov"],                "2026-05-17", "2026-05-17", "NY school-enrollment stats"),
    ("texas-dshs",           ["dshs.texas.gov"],                "2026-05-17", "2026-05-17", "Texas DSHS STI stats"),
]

PAD_DAYS = 7          # steering: flag captures outside reported windows
REQ_GAP = 1.6         # seconds between requests (<=1 req/sec rule)
TIMEOUT = 300
BACKOFFS = [30, 60, 180]

def log(obj):
    obj["logged_at"] = datetime.now(timezone.utc).isoformat()
    with LOG.open("a") as f:
        f.write(json.dumps(obj) + "\n")

def cdx_query(host, frm, to):
    # NOTE: Arquivo.pt CDX defaults to limit=100000 (verified 2026-10-01);
    # explicit high limit required for flood-scale windows. from/to accept
    # full timestamp precision (YYYYMMDDHHMMSS), enabling sub-day halving.
    params = urllib.parse.urlencode({
        "url": host, "matchType": "domain",
        "from": frm, "to": to, "output": "json",
        "limit": 2000000,
    })
    url = f"https://arquivo.pt/wayback/cdx?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "silent-locus-research/1.0 (research; arquivo.pt ToS educational use)"})
    return urllib.request.urlopen(req, timeout=TIMEOUT)

def fetch_day_chunks(host, frm_dt, to_dt):
    """Fallback: one query per day if a wide query times out."""
    day = frm_dt
    chunks = []
    while day <= to_dt:
        d = day.strftime("%Y%m%d")
        chunks.append((d, d))
        day += timedelta(days=1)
    return chunks

def fetch_window(host, frm, to, out):
    """One CDX query; returns record count. Raises on failure."""
    for attempt in range(1 + len(BACKOFFS)):
        try:
            time.sleep(REQ_GAP)
            t0 = time.time()
            resp = cdx_query(host, frm, to)
            n = 0
            with gzip.open(str(out), "at", encoding="utf-8") as f:
                for line in resp:
                    line = line.strip()
                    if line:
                        f.write(line.decode("utf-8", "replace") + "\n")
                        n += 1
            dt = time.time() - t0
            log({"event": "query_ok", "host": host, "from": frm, "to": to,
                 "records": n, "seconds": round(dt, 1), "http": resp.status,
                 "attempt": attempt + 1})
            return n
        except urllib.error.HTTPError as e:
            log({"event": "http_error", "host": host, "from": frm, "to": to,
                 "http": e.code, "attempt": attempt + 1})
            if e.code in (429, 503):
                if attempt < len(BACKOFFS):
                    time.sleep(BACKOFFS[attempt]); continue
                log({"event": "hard_stop_rate_limit", "host": host})
            raise
        except Exception as e:
            log({"event": "fetch_error", "host": host, "from": frm, "to": to,
                 "error": f"{type(e).__name__}: {e}", "attempt": attempt + 1})
            if attempt < len(BACKOFFS):
                time.sleep(BACKOFFS[attempt])
                continue
            raise

def halve(frm, to):
    # frm/to are YYYYMMDDHHMMSS; split at midpoint, keep 1-second gap
    a = datetime.strptime(frm, "%Y%m%d%H%M%S")
    b = datetime.strptime(to, "%Y%m%d%H%M%S")
    mid = a + (b - a) / 2
    return ((frm, (mid - timedelta(seconds=1)).strftime("%Y%m%d%H%M%S")),
            (mid.strftime("%Y%m%d%H%M%S"), to))

def collect_target(slug, hosts, wfrom, wto):
    wfrom_dt = datetime.strptime(wfrom, "%Y-%m-%d")
    wto_dt = datetime.strptime(wto, "%Y-%m-%d")
    pfrom = (wfrom_dt - timedelta(days=PAD_DAYS)).strftime("%Y%m%d") + "000000"
    pto = (wto_dt + timedelta(days=PAD_DAYS)).strftime("%Y%m%d") + "235959"
    out = RAW / f"{slug}.cdx.jsonl.gz"
    total = 0
    for host in hosts:
        queue = [(pfrom, pto)]
        while queue:
            frm, to = queue.pop(0)
            try:
                total += fetch_window(host, frm, to, out)
            except Exception as e:
                span_h = (datetime.strptime(to, "%Y%m%d%H%M%S")
                          - datetime.strptime(frm, "%Y%m%d%H%M%S")).total_seconds() / 3600
                if span_h > 1.5:
                    w1, w2 = halve(frm, to)
                    queue.extend([w1, w2])
                    log({"event": "window_split", "slug": slug, "host": host,
                         "from": frm, "to": to, "into": [w1, w2]})
                else:
                    log({"event": "window_failed", "slug": slug, "host": host,
                         "from": frm, "to": to, "error": f"{type(e).__name__}: {e}"})
    log({"event": "target_done", "slug": slug, "total_records": total,
         "incident_window": [wfrom, wto], "padded_window": [pfrom, pto]})

def main():
    done = set()
    try:
        for line in LOG.open():
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("event") == "target_done":
                done.add(d.get("slug"))
    except FileNotFoundError:
        pass
    log({"event": "run_start", "utc": datetime.now(timezone.utc).isoformat(),
         "pad_days": PAD_DAYS, "req_gap": REQ_GAP, "skipped": sorted(done)})
    for slug, hosts, wfrom, wto, note in TARGETS:
        if slug in done:
            continue
        log({"event": "target_start", "slug": slug, "hosts": hosts, "note": note})
        collect_target(slug, hosts, wfrom, wto)
    log({"event": "run_done"})

if __name__ == "__main__":
    main()
