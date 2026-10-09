#!/usr/bin/env python3
"""Gap-fill collection for new-fleets hunt: urlquery submissions window from ~04:00 UTC 2026-10-05 onward.
Resume script: collects into raw/window_gapfill.json. Polite: 6s between requests."""
import json, subprocess, time, sys, os

BASE = os.path.expanduser("~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/new-fleets")
RAW = os.path.join(BASE, "raw")
CLI = os.path.expanduser("~/workspace/skills/urlquery/bin/uq_htmx.py")
OUT = os.path.join(RAW, "window_gapfill.json")
SLEEP = 6

queries = [
    ("http", 0), ("http", 50), ("http", 100), ("http", 150),
    "webhook.site", "ngrok", "eval", "harness", "appwrite.network",
    "jmail.world", "nonce=", "task=", "batch=", "museum", "cachedview.nl",
    "wasmer.app", "replit.app", "ovou.com", ".shop",
]
allr = []
seen = set()

def run(q, offset=None):
    cmd = [sys.executable, CLI, "search", "--query", q, "--limit", "50", "--delay", "0"]
    if offset:
        cmd += ["--offset", str(offset)]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        d = json.loads(p.stdout)
        return d.get("reports", [])
    except Exception as e:
        print(f"  ERR {q}@{offset}: {e}", flush=True)
        return None

n_fail = 0
for item in queries:
    if isinstance(item, tuple):
        q, off = item
    else:
        q, off = item, None
    print(f"query: {q} offset={off}", flush=True)
    reps = run(q, off)
    if reps is None:
        n_fail += 1
        continue
    for r in reps:
        rid = r.get("report_id")
        if rid and rid not in seen:
            seen.add(rid)
            allr.append(r)
    print(f"  -> total unique so far: {len(allr)}", flush=True)
    time.sleep(SLEEP)

with open(OUT, "w") as f:
    json.dump(allr, f, indent=1)
print(f"DONE: {len(allr)} unique reports -> {OUT}, failures={n_fail}")
