#!/usr/bin/env python3
"""Next-verticals hunt driver: paced htmx queries, raw JSON saved per query."""
import subprocess, time, json, os, sys

UQ = os.path.expanduser("~/workspace/skills/urlquery/bin/uq_htmx.py")
OUTDIR = os.path.expanduser(
    "~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/mimic/raw")
os.makedirs(OUTDIR, exist_ok=True)

QUERIES = [
    ("nv_01_dated_20261005", "uqscan=20261005"),   # today's dated tags catch-all
    ("nv_02_dated_20261006", "uqscan=20261006"),   # tomorrow's dated tags (expect empty)
    ("nv_03_school", "uqscan=school"),
    ("nv_04_school20261005", "uqscan=school20261005"),
    ("nv_05_gov", "uqscan=gov"),
    ("nv_06_gov20261005", "uqscan=gov20261005"),
    ("nv_07_mall", "uqscan=mall"),
    ("nv_08_mall20261005", "uqscan=mall20261005"),
    ("nv_09_scenic", "uqscan=scenic"),
    ("nv_10_pharmacy", "uqscan=pharmacy"),
    ("nv_11_bank", "uqscan=bank"),
    ("nv_12_estate", "uqscan=estate"),
    ("nv_13_hongkong", "uqscan=hongkong"),
    ("nv_14_macau", "uqscan=macau"),
    ("nv_15_taiwan", "uqscan=taiwan"),
    ("nv_16_taipei", "uqscan=taipei"),
    ("nv_17_uqid", "uqid="),
    ("nv_18_uqt", "uqt="),
    ("nv_19_uqv", "uqv="),
    ("nv_20_srcmanual", "src=manual"),
    ("nv_21_hospital_known", "uqscan=hospital"),  # known family, calibration
    ("nv_22_food_known", "uqscan=food"),          # known family, calibration
    ("nv_23_xuexiao", "uqscan=xuexiao"),          # pinyin bonus: schools
    ("nv_24_zhengwu", "uqscan=zhengwu"),          # pinyin bonus: gov-service
]

PACING = 7  # seconds between invocations (>5s required)

for i, (slug, q) in enumerate(QUERIES):
    out = os.path.join(OUTDIR, slug + ".json")
    if os.path.exists(out) and os.path.getsize(out) > 2:
        print(f"[{i+1}/{len(QUERIES)}] {slug}: cached, skipping", flush=True)
        continue
    print(f"[{i+1}/{len(QUERIES)}] {slug}: querying...", flush=True)
    cmd = [sys.executable, UQ, "search", "--query", q, "--limit", "30", "--delay", "5"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        payload = r.stdout if r.stdout.strip() else json.dumps(
            {"error": r.stderr.strip()[-500:], "query": q})
        with open(out, "w") as f:
            f.write(payload)
    except Exception as e:
        with open(out, "w") as f:
            f.write(json.dumps({"error": str(e), "query": q}))
    time.sleep(PACING)

print("DONE", flush=True)
