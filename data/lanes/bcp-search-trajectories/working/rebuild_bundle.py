#!/usr/bin/env python3
"""Rebuild the BCP bundle, retrying file writes through EPERM waves."""
import subprocess
import sys
import time
import os

LANE_DIR = "/home/hatch/workspace/silent-locus/data/lanes/bcp-search-trajectories"
BUNDLE = os.path.join(LANE_DIR, "bundle-bcp-search.json")
REPORT = os.path.join(LANE_DIR, "build-report.json")

# Run the builder
p = subprocess.run(
    [sys.executable, os.path.join(LANE_DIR, "build_bundle.py")],
    capture_output=True, cwd=LANE_DIR,
)
if p.returncode != 0:
    print("BUILDER FAILED", p.returncode)
    print(p.stderr[:1000].decode(errors="replace"))
    sys.exit(1)

print(f"builder OK: bundle {len(p.stdout)} bytes, report {len(p.stderr)} bytes")

# Write files with retry through EPERM waves
for attempt in range(30):
    try:
        with open(BUNDLE, "wb") as fh:
            fh.write(p.stdout)
        with open(REPORT, "wb") as fh:
            fh.write(p.stderr)
        # Verify
        assert os.path.getsize(BUNDLE) == len(p.stdout)
        assert os.path.getsize(REPORT) == len(p.stderr)
        print(f"WRITE OK on attempt {attempt + 1}")
        sys.exit(0)
    except PermissionError as e:
        print(f"attempt {attempt + 1}: EPERM, retrying in 60s")
        time.sleep(60)

print("WRITE FAILED after 30 attempts")
sys.exit(3)
