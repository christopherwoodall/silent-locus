#!/usr/bin/env python3
"""Retry throttled queries from collect_gapfill.py with long backoff (30s).
Appends new uniques into raw/window_gapfill.json."""
import json, subprocess, time, sys, os

BASE = os.path.expanduser("~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/new-fleets")
RAW = os.path.join(BASE, "raw")
CLI = os.path.expanduser("~/workspace/skills/urlquery/bin/uq_htmx.py")
OUT = os.path.join(RAW, "window_gapfill.json")

existing = json.load(open(OUT))
seen = {r["report_id"] for r in existing}
print(f"starting with {len(existing)} reports")

queries = ["jmail.world", "webhook.site", "wasmer.app", "replit.app", "appwrite.network",
           "museum", "ngrok", "harness", "cachedview.nl", "batch=", ".shop"]
added = 0
for q in queries:
    print(f"retry: {q}", flush=True)
    ok = False
    for attempt in range(3):
        try:
            p = subprocess.run([sys.executable, CLI, "search", "--query", q, "--limit", "50"],
                               capture_output=True, text=True, timeout=120)
            d = json.loads(p.stdout)
            for r in d.get("reports", []):
                if r.get("report_id") not in seen:
                    seen.add(r["report_id"]); existing.append(r); added += 1
            ok = True
            print(f"  ok, +{added} total new", flush=True)
            break
        except Exception as e:
            print(f"  attempt {attempt+1} failed: {e}", flush=True)
            time.sleep(45)
    if not ok:
        print(f"  GAVE UP: {q}", flush=True)
    time.sleep(30)

json.dump(existing, open(OUT, "w"), indent=1)
print(f"DONE: +{added} new, {len(existing)} total -> {OUT}")
