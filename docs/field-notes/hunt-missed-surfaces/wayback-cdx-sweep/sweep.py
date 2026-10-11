#!/usr/bin/env python3
"""Wayback CDX sweep for Transluce-incident URLs.

Why: skill-ladders found agent skills are archive-first BY INSTRUCTION, and
hemo-web-read teaches agents to CREATE captures via web.archive.org/save/.
If the agents touched Wayback, captures are timestamped evidence.

Read-only CDX queries only. NEVER submits save requests.
Idempotent: per-query results cached in state.json; reruns skip done queries.
Polite: 2s between requests, backoff on 429/503.

Outputs:
  data/cdx-log.jsonl          every CDX request (params, http, rows)
  data/in-window-captures.jsonl  captures with timestamp in Apr-Jul 2026
"""
import gzip, json, random, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
STATE = ROOT / "state.json"
LOG = DATA / "cdx-log.jsonl"
INWINDOW = DATA / "in-window-captures.jsonl"

UA = {"User-Agent": "silent-locus-hunt/1.0 (research CDX sweep; contact: hunt)"}
CDX = "https://web.archive.org/cdx/search/cdx"
FROM, TO = "20260401", "20260731"   # incident window Apr-Jul 2026
PACE = 2.0

REPO = Path(__file__).resolve().parents[3]  # ~/workspace/silent-locus
HOTLEADS = REPO / "collections/hunt-missed-surfaces/hot-leads/data"
ARQ_DOE = REPO / "data/2026-10-01-arquivo-pt/raw/doe-crdc.cdx.jsonl.gz"

PREFIX_QUERIES = [
    # NOTE: CDX quirk (verified 2026-10-03): url=<p>/* with matchType=prefix
    # returns []. Wildcard alone (no matchType) = prefix match. For
    # URL-prefix matching of an exact stem, use matchType=prefix WITHOUT *.
    ("doe-api-zzoai",
     "civilrightsdata.ed.gov/api/v1.0/*",
     {"filter": "original:.*zz=oai.*"}),
    ("doe-api-all",
     "civilrightsdata.ed.gov/api/v1.0/*",
     {"collapse": "urlkey", "limit": "50000"}),
    ("lac-ajax",
     "recherche-collection-search.bac-lac.canada.ca/ajax/*",
     {"collapse": "urlkey", "limit": "50000"}),
    ("bea-api",
     "apps.bea.gov/api/*",
     {"collapse": "urlkey", "limit": "50000"}),
    ("sec-county-json-prefix",
     "sec.gov/files/county.json",
     {"matchType": "prefix", "collapse": "urlkey", "limit": "50000"}),
]

EXACT_STATIC = [
    ("sec-county-json", "https://www.sec.gov/files/county.json"),
    ("sec-county-json-nosub", "https://sec.gov/files/county.json"),
]

def cdx_query(params, name):
    q = dict(params)
    q.setdefault("output", "json")
    q.setdefault("from", FROM)
    q.setdefault("to", TO)
    q.setdefault("fl", "timestamp,original,statuscode,digest,mimetype")
    url = CDX + "?" + urllib.parse.urlencode(q)
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r:
                body = r.read().decode("utf-8", errors="replace")
            rows = json.loads(body) if body.strip() else []
            rec = {"name": name, "params": params, "http": 200,
                   "rows": max(0, len(rows) - 1), "truncated": False}
            data = rows[1:] if rows else []
            return rec, data
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < 3:
                time.sleep(10 * (attempt + 1))
                continue
            rec = {"name": name, "params": params, "http": e.code,
                   "rows": 0, "error": f"HTTP {e.code}"}
            return rec, []
        except Exception as e:
            rec = {"name": name, "params": params, "http": -1,
                   "rows": 0, "error": str(e)[:200]}
            return rec, []
    rec = {"name": name, "params": params, "http": -1, "rows": 0,
           "error": "retries exhausted"}
    return rec, []

def record_capture(row, query_name):
    ts, orig, status, digest = (row + ["", "", "", ""])[:4]
    mime = row[4] if len(row) > 4 else ""
    if FROM + "000000" <= ts <= TO + "235959":
        rec = {"query": query_name, "timestamp": ts, "url": orig,
               "status": status, "digest": digest, "mime": mime}
        with INWINDOW.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        return True
    return False

def distinct_zzoai_urls():
    """Stream the Arquivo.pt DoE CDX, return sorted distinct zz=oai URLs."""
    seen = set()
    with gzip.open(ARQ_DOE, "rt") as f:
        for line in f:
            if "zz=oai" not in line:
                continue
            try:
                u = json.loads(line).get("url", "")
            except Exception:
                continue
            if "zz=oai" in u:
                seen.add(u)
    return sorted(seen)

def main():
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    state.setdefault("queries_done", {})
    inwin = 0

    def run(name, params):
        nonlocal inwin
        if state["queries_done"].get(name):
            print(f"skip {name} (done)")
            return
        rec, data = cdx_query(params, name)
        for row in data:
            if record_capture(row, name):
                inwin += 1
        rec["in_window"] = sum(1 for _ in open(INWINDOW)) if INWINDOW.exists() else 0
        state["queries_done"][name] = rec
        with LOG.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        STATE.write_text(json.dumps(state, indent=2))
        print(f"{name}: http={rec['http']} rows={rec['rows']} "
              f"in-window-so-far={rec['in_window']}")
        time.sleep(PACE)

    for name, url, extra in PREFIX_QUERIES:
        run(name, {"url": url, **extra})
    for name, url in EXACT_STATIC:
        run(name, {"url": url})

    # LAC 14 exact payload URLs
    lac = json.load(open(HOTLEADS / "lac-candidates.json"))["payload_urls"]
    for i, u in enumerate(lac):
        run(f"lac-exact-{i:02d}", {"url": u})

    # Random sample of 200 exact zz=oai DoE URLs
    zzoai = distinct_zzoai_urls()
    print(f"distinct zz=oai URLs in Arquivo.pt data: {len(zzoai)}")
    state["zzoai_distinct_arquivo"] = len(zzoai)
    rng = random.Random(20261003)
    sample = rng.sample(zzoai, min(200, len(zzoai)))
    state["sample_seed"] = 20261003
    state["sample_size"] = len(sample)
    STATE.write_text(json.dumps(state, indent=2))
    for i, u in enumerate(sample):
        run(f"doe-exact-{i:03d}", {"url": u})

    print(f"\nDONE. in-window captures total: "
          f"{sum(1 for _ in open(INWINDOW)) if INWINDOW.exists() else 0}")

if __name__ == "__main__":
    main()
