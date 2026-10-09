#!/usr/bin/env python3
"""Egress-waiter: polls proxy egress every 180s (max 12 tries), then runs the
jmail.world htmx re-query once egress recovers. Writes FLAG_UP when done."""
import subprocess, sys, time, os

RAW = "/home/hatch/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/ghost-hunter/raw"
FLAG = os.path.join(RAW, "EGRESS_UP.flag")
LOG = os.path.join(RAW, "egress_watcher.log")

def log(msg):
    line = time.strftime("%Y-%m-%d %H:%M:%S") + " " + msg
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def egress_ok():
    try:
        r = subprocess.run(
            ["curl", "-s", "-m", "12", "-o", "/dev/null", "-w", "%{http_code}",
             "https://urlquery.net/"],
            capture_output=True, text=True, timeout=30)
        return r.stdout.strip() == "200"
    except Exception:
        return False

for attempt in range(1, 13):
    if egress_ok():
        log(f"EGRESS UP on attempt {attempt}")
        # run jmail.world re-query (polite single request)
        try:
            r = subprocess.run(
                ["python3", "/home/hatch/workspace/skills/urlquery/bin/uq_htmx.py",
                 "search", "--query", "jmail.world", "--limit", "100"],
                capture_output=True, text=True, timeout=180)
            with open(os.path.join(RAW, "jmail_world_resumed.json"), "w") as f:
                f.write(r.stdout if r.returncode == 0 else r.stderr)
            log(f"jmail.world re-query rc={r.returncode} bytes={len(r.stdout)}")
        except Exception as e:
            log(f"re-query failed: {e}")
        open(FLAG, "w").write(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        sys.exit(0)
    log(f"attempt {attempt}/12: egress still down")
    time.sleep(180)

log("EGRESS STILL DOWN after 12 attempts (~36min); giving up")
