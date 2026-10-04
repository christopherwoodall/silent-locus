#!/usr/bin/env python3
"""Nonce-grammar incident discovery sweep via Wayback CDX — PATH-SCOPED.

INVERTED HUNT: sweep for the toolkit's cache-buster grammar across .gov hosts.

Method: path-scoped prefix queries (url=<host>/<path> + matchType=prefix +
urlkey regex filter) are ~50x cheaper than domain-wide regex scans (1s vs
60s+ and no 504s). Covers the path shapes of all known incidents:
  /api/* (DoE /api/v1.0, BEA /api), /files/* (SEC county.json),
  /ajax/* (LAC), /data/*, /search/*.

Read-only. Polite: 1.5s pacing per shard, 3 shards, 120s timeout.
Idempotent via query log.
"""
import json, time, urllib.parse, urllib.request, urllib.error, os
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"; LOGS.mkdir(exist_ok=True)
QLOG = LOGS / "nonce-query-log-path.jsonl"
HITS = LOGS / "nonce-hits-path.jsonl"

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

FROM, TO = "20260601", "20260801"   # incident window (all 4 known: May 28-Jun 21)

GRAMMARS = {
    "zzoai":   r".*zz=oai[0-9]+.*",
    "zzbulk":  r".*zzbulk.*",
    "x0dec":   r".*x=0\.[0-9]{10,}.*",
    "freshx":  r".*fresh=x.*",
    "prepnum": r".*prep[0-9]{4,}.*",
    "cbdec":   r".*cb=0\.[0-9]{10,}.*",
}

PATHS = ["api", "files", "data", "ajax", "search"]

HOSTS = [
    "civilrightsdata.ed.gov", "www.sec.gov", "sec.gov", "apps.bea.gov",
    "bea.gov", "census.gov", "www.census.gov", "kansasmemory.gov",
    "bac-lac.gc.ca", "recherche-collection-search.bac-lac.canada.ca",
    "data.nysed.gov", "wonder.cdc.gov", "portal.max.gov",
    "ed.gov", "www.ed.gov", "nces.ed.gov", "data.gov", "api.data.gov",
    "whitehouse.gov", "justice.gov", "cdc.gov", "www.cdc.gov", "nih.gov",
    "nasa.gov", "noaa.gov", "weather.gov", "irs.gov", "ssa.gov", "va.gov",
    "state.gov", "dhs.gov", "commerce.gov", "treasury.gov", "labor.gov",
    "energy.gov", "usda.gov", "doi.gov", "dot.gov", "hud.gov", "epa.gov",
    "nps.gov", "fbi.gov", "bls.gov", "fhfa.gov", "canada.ca", "gc.ca",
]

def done_queries():
    s = set()
    if QLOG.exists():
        for line in QLOG.open():
            try: s.add(json.loads(line)["qkey"])
            except Exception: pass
    return s

def cdx(host, path, grex):
    f = urllib.parse.quote(grex, safe="")
    url = (f"http://web.archive.org/cdx/search/cdx?url={host}/{path}"
           f"&matchType=prefix&from={FROM}&to={TO}&filter=urlkey:{f}"
           f"&collapse=urlkey&output=json&limit=20000")
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            body = r.read()
        if r.status != 200:
            return {"http": r.status, "rows": None}
        d = json.loads(body)
        return {"http": 200, "rows": d[1:] if len(d) > 1 else []}
    except urllib.error.HTTPError as e:
        return {"http": e.code, "rows": None}
    except Exception as e:
        return {"http": -1, "rows": None, "err": str(e)[:120]}

def main():
    shard = int(os.environ.get("SHARD", "0"))
    nshards = int(os.environ.get("NSHARDS", "1"))
    combos = [(h, p) for h in HOSTS for p in PATHS]
    combos = [c for i, c in enumerate(combos) if i % nshards == shard]
    print(f"shard {shard}/{nshards}: {len(combos)} host-path combos", flush=True)
    done = done_queries()
    bursts = defaultdict(list)
    for host, path in combos:
        for gname, grex in GRAMMARS.items():
            qkey = f"{host}/{path}|{gname}"
            if qkey in done:
                continue
            res = cdx(host, path, grex)
            rec = {"qkey": qkey, "host": host, "path": path, "grammar": gname,
                   "http": res["http"],
                   "n": len(res["rows"]) if res["rows"] is not None else None,
                   "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
            with QLOG.open("a") as f:
                f.write(json.dumps(rec) + "\n")
            if res["rows"]:
                for row in res["rows"]:
                    ts, orig = row[1], row[2]
                    bursts[(host, path, ts[:8])].append(orig)
                    with HITS.open("a") as f:
                        f.write(json.dumps({"host": host, "path": path,
                                            "grammar": gname, "ts": ts,
                                            "url": orig}) + "\n")
                print(f"HIT {host}/{path} {gname}: {len(res['rows'])} rows", flush=True)
            time.sleep(1.5)
    print("\n=== BURSTS (>=10 hits, one host+path+day) ===", flush=True)
    for (host, path, day), urls in sorted(bursts.items(), key=lambda kv: -len(kv[1])):
        if len(urls) >= 10:
            print(f"{len(urls):5d}  {host}/{path}  {day}  e.g. {urls[0][:90]}", flush=True)

if __name__ == "__main__":
    main()
