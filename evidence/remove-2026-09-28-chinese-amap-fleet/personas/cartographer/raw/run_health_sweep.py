#!/usr/bin/env python3
"""Cartographer lane sweep: 14 paced urlquery htmx queries on health portals.
Saves JSON to health-portals-json/<n>_<name>.json. >=5s between HTTP calls,
8s between queries, 3x retry with 60s backoff.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

BIN = Path.home() / "workspace/skills/urlquery/bin/uq_htmx_curl.py"
OUT = (
    Path.home()
    / "workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/cartographer/raw/health-portals-json"
)
OUT.mkdir(parents=True, exist_ok=True)

QUERIES = [
    ("01_tableau-health-department", "tableau health department", 50),
    ("02_tableau-asthma", "tableau asthma", 40),
    ("03_department-of-health-tableau", "department of health tableau", 40),
    ("04_wonder-cdc", "wonder.cdc.gov", 50),
    ("05_data-cdc", "data.cdc.gov", 40),
    ("06_healthdata-gov", "healthdata.gov", 40),
    ("07_powerbi-health", "powerbi health", 40),
    ("08_powerbi-health-department", "app.powerbi.com health department", 40),
    ("09_nhs-uk-data", "nhs.uk data", 40),
    ("10_digital-nhs-uk", "digital.nhs.uk", 40),
    ("11_provider-directory", "provider directory", 40),
    ("12_hospital-compare", "hospital compare", 30),
    ("13_public-health-dashboard", "public health dashboard", 40),
    ("14_county-health-data", "county health data", 40),
]


def run_query(name, query, limit):
    dest = OUT / f"{name}.json"
    for attempt in range(3):
        try:
            p = subprocess.run(
                [sys.executable, str(BIN), "search", "--query", query,
                 "--limit", str(limit), "--delay", "5"],
                capture_output=True, text=True, timeout=1200,
            )
            if p.returncode != 0:
                raise RuntimeError(p.stderr.strip()[:300])
            data = json.loads(p.stdout)
            dest.write_text(json.dumps(data, indent=1))
            print(f"OK {name}: {len(data.get('reports', []))} reports -> {dest.name}")
            return True
        except Exception as e:
            print(f"RETRY {name} attempt {attempt+1}: {e}", flush=True)
            time.sleep(60)
    print(f"FAIL {name} after 3 attempts")
    return False


def main():
    ok = fail = 0
    for i, (name, query, limit) in enumerate(QUERIES):
        if run_query(name, query, limit):
            ok += 1
        else:
            fail += 1
        if i < len(QUERIES) - 1:
            time.sleep(8)
    print(f"DONE: {ok} ok, {fail} failed")


if __name__ == "__main__":
    main()
