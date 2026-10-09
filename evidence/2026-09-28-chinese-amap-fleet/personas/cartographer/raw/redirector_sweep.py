#!/usr/bin/env python3
"""TARGET-CLASS HUNT sweep: phishing-redirector farms + scam infra via urlquery htmx endpoint.
Paced at 1 request per ~6s. Dumps JSON per query into the raw dir for offline clustering.
Usage: python3 redirector_sweep.py
"""
import json, subprocess, sys, time, os

BIN = "/home/hatch/workspace/skills/urlquery/bin/uq_htmx.py"
OUT = "/home/hatch/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/cartographer/raw"

QUERIES = [
    # archive-oracle / fetch-proxy usage (jmail auditor signature)
    ("cachedview.nl", 100),
    ("archive.ph", 100),
    ("webcache.googleusercontent", 50),
    # auditor probe phrases: known phishing-kit URLs used as search probes
    ("followlike", 60),
    ("livetraffic", 60),
    ("refer=", 60),
    ("seekers+of+decay", 60),
    # namespace-walk grammar of forum/drive audits
    ("thread/", 100),
    ("drive/", 100),
    # scam-shop networks
    (".shop", 100),
    (".store", 100),
    # redirector-kit TTP phrases
    ("vol1-efta", 60),
    ("efta", 60),
    # forum/drive farm candidates: common redirector-kit hosts? keep broad
    ("/search?q=", 60),
]

def run(query, limit):
    cmd = [sys.executable, BIN, "search", "--query", query, "--limit", str(limit), "--delay", "0"]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        out = p.stdout.strip()
        if out.startswith("[") or out.startswith("{"):
            return json.loads(out)
        return {"raw": out, "stderr": p.stderr[-500:]}
    except Exception as e:
        return {"error": str(e)}

os.makedirs(OUT, exist_ok=True)
manifest = {}
for i, (q, lim) in enumerate(QUERIES):
    print(f"[{i+1}/{len(QUERIES)}] query={q!r} limit={lim}", flush=True)
    res = run(q, lim)
    fn = f"q_{q.replace('/', '_').replace('.', '_').replace('=', '_').replace('+', '_')}.json"
    path = os.path.join(OUT, fn)
    with open(path, "w") as f:
        json.dump(res, f, indent=1)
    n = len(res) if isinstance(res, list) else "?"
    print(f"  -> {fn}: {n} records", flush=True)
    manifest[q] = {"file": fn, "count": n}
    if i < len(QUERIES) - 1:
        time.sleep(6)

with open(os.path.join(OUT, "sweep_manifest.json"), "w") as f:
    json.dump({"date": "2026-10-04/05", "queries": manifest}, f, indent=1)
print("DONE")
