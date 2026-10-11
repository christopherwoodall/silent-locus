#!/usr/bin/env python3
"""Submit lane bundles with patient lock-contention retries.

Usage: submit_bundles.py [start_bundle]
Submits bundle-<start>..bundle-03, 90 attempts each with 60s sleeps.
Prints SUBMITTED <batch_id> per bundle. Idempotent: factum returns the
original IDs when an idempotency key is retried.
"""
import glob
import json
import subprocess
import sys
import time

LANE_DIR = "/home/hatch/workspace/silent-locus"
BUNDLES = ("/home/hatch/workspace/silent-locus/data/lanes/"
           "2026-10-11-hf-traj-tbench/.work/bundles")
PENDING = "/home/hatch/workspace/silent-locus/data/.local/pending"
FACTUM = ["uv", "run", "skills/factum/scripts/factum.py",
          "--repo", "."]
ENV = {"PATH": "/home/hatch/.local/bin:/usr/bin:/bin",
       "HOME": "/home/hatch"}
KEYS = {b: f"lane-ingest-2026-10-11-hf-traj-tbench-chunk{b:02d}-v1"
        for b in range(4)}


def already_pending(b):
    key = KEYS[b]
    for f in glob.glob(f"{PENDING}/*.json"):
        try:
            d = json.load(open(f))
        except Exception:
            continue
        if d.get("receipt", {}).get("key") == key:
            return d.get("batch_id")
    return None


start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
for b in range(start, 4):
    path = f"{BUNDLES}/bundle-{b:02d}.json"
    batch = already_pending(b)
    if batch:
        print(f"SUBMITTED bundle-{b:02d} (already pending) batch={batch}",
              flush=True)
        continue
    done = False
    for attempt in range(1, 91):
        try:
            p = subprocess.run(
                FACTUM + ["add", "--input", path],
                capture_output=True, text=True, cwd=LANE_DIR, env=ENV,
                timeout=1500)
            try:
                res = json.loads(p.stdout)
            except Exception:
                res = {}
        except subprocess.TimeoutExpired:
            batch = already_pending(b)
            if batch:
                print(f"SUBMITTED bundle-{b:02d} attempt={attempt} "
                      f"(recovered after timeout) batch={batch}", flush=True)
                done = True
                break
            print(f"bundle-{b:02d} attempt={attempt} TIMEOUT (not pending); "
                  f"retrying", flush=True)
            time.sleep(60)
            continue
        if res.get("ok") is True:
            batch = (res.get("result") or {}).get("batch_id") or \
                res.get("batch_id")
            print(f"SUBMITTED bundle-{b:02d} attempt={attempt} "
                  f"batch={batch}", flush=True)
            done = True
            break
        err = (res.get("error") or {}).get("code", "?")
        print(f"bundle-{b:02d} attempt={attempt} err={err} "
              f"stderr={p.stderr[:80]}", flush=True)
        time.sleep(60)
    if not done:
        print(f"FAILED bundle-{b:02d} after 90 attempts", flush=True)
        sys.exit(1)
print("ALL SUBMITTED", flush=True)
