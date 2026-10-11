#!/usr/bin/env python3
"""Independent validation of the 2026-10-11-hf-traj-tbench bundles.

Re-derives key numbers from the parquet bytes (not from the builder's
intermediate files) and checks bundle structural rules.
"""
import glob
import json
import os
import random
import re
from collections import Counter

import pyarrow.parquet as pq

LANE = "2026-10-11-hf-traj-tbench"
LANE_DIR = os.path.expanduser(f"~/workspace/silent-locus/data/lanes/{LANE}")
WORK = os.path.join(LANE_DIR, ".work")
RAW = os.path.expanduser(
    "~/workspace/silent-locus/evidence/hf-trajectories/raw/"
    "yoonholee-terminalbench-trajectories/data")
F0 = os.path.join(RAW, "train-00000-of-00002.parquet")
F1 = os.path.join(RAW, "train-00001-of-00002.parquet")

errors = []


def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        errors.append(msg)


def load_bundles():
    recs = []
    for p in sorted(glob.glob(os.path.join(WORK, "bundles", "*.json"))):
        b = json.load(open(p))
        assert b["bundle"] == 2, "bundle version"
        assert b["actor"], "actor required"
        assert b["idempotency_key"], "idempotency key required"
        recs.extend(b["records"])
    return recs


recs = load_bundles()
print(f"loaded {len(recs)} records from bundles")
obss = [r for r in recs if r["kind"] == "observation"]

# --- structural checks ---
for r in recs:
    tags = r.get("tags", {})
    if tags.get("lane") != LANE:
        check(False, f"lane tag missing/wrong on {r.get('ref')}")
        break
else:
    check(True, "every record carries tags.lane")

refs = [r["ref"] for r in recs]
# refs are bundle-local; uniqueness is required per bundle only
for p in sorted(glob.glob(os.path.join(WORK, "bundles", "*.json"))):
    brefs = [r["ref"] for r in json.load(open(p))["records"]]
    check(len(brefs) == len(set(brefs)),
          f"refs unique within {p.split('/')[-1]}")

REQ = {"type", "source", "observed_at", "time_basis", "files", "data"}
for r in obss:
    b = r["body"]
    if not REQ <= set(b):
        check(False, f"observation missing fields: {r['ref']}")
        break
    if len(r["ref"]) > 64:
        check(False, f"ref too long: {r['ref']}")
        break
else:
    check(True, "observation envelope complete, refs <= 64 chars")

# --- 1. matrix re-derivation ---
by_cat = Counter()
for r in obss:
    d = r["body"]["data"]
    if r["body"]["type"] == "intel.behavior":
        by_cat[d["category"]] += 1
    else:
        by_cat[r["body"]["type"] + "/" + d.get("category", "?")] += 1
print("by category:", dict(by_cat))

mx = [r for r in obss
      if r["body"]["type"] == "intel.behavior"
      and r["body"]["data"]["category"] == "harness-assignment"]
truth = Counter()
for path in (F0, F1):
    pf = pq.ParquetFile(path)
    for batch in pf.iter_batches(columns=["model", "agent"],
                                 batch_size=100000):
        df = batch.to_pandas()
        for m, a in zip(df["model"], df["agent"]):
            truth[(str(m), str(a))] += 1
check(len(mx) == len(truth) == 109,
      f"matrix record count {len(mx)} == distinct pairs {len(truth)}")

# spot-check 5 random pairs: description count == byte count
for p in random.sample(sorted(truth), 5):
    n = truth[p]
    hits = [r for r in mx
            if r["tags"]["model"] == p[0] and r["tags"]["harness"] == p[1]]
    ok = len(hits) == 1 and f"ran {n} " in hits[0]["body"]["data"]["description"]
    check(ok, f"matrix spot-check {p[0][:30]} x {p[1]} = {n}")

# --- 2. jina re-derivation ---
jr = [r for r in obss
      if r["body"]["data"].get("category") == "fetch-proxy-abuse"]
rows, occ = 0, 0
for rg in range(pq.ParquetFile(F1).num_row_groups):
    tbl = pq.ParquetFile(F1).read_row_group(rg, columns=["steps"])
    for s in tbl.column("steps").to_pylist():
        if not s or s == "null":
            continue
        c = s.lower().count("r.jina.ai")
        if c:
            rows += 1
            occ += c
check(len(jr) == rows == 20, f"jina rows {len(jr)} == byte rows {rows}")
print(f"byte r.jina.ai occurrences: {occ}")

# verbatim spot-check: pick a jina record that carries THOUGHT reasoning text,
# find that text in the raw bytes (raw steps are JSON-escaped, so compare
# the escaped form)
cands = [r for r in jr if "THOUGHT:" in r["body"]["data"]["description"]]
check(len(cands) > 0, f"{len(cands)} jina records carry THOUGHT reasoning")
sample = cands[0]
desc = sample["body"]["data"]["description"]
m = re.search(r"THOUGHT: (.+?)(?:\n\n```|\n*$)", desc, re.S)
thought = m.group(0) if m else None
found = False
if thought:
    escaped = json.dumps(thought)[1:-1]
    for rg in range(pq.ParquetFile(F1).num_row_groups):
        tbl = pq.ParquetFile(F1).read_row_group(rg, columns=["steps"])
        for s in tbl.column("steps").to_pylist():
            if s and escaped[:120] in s:
                found = True
                break
        if found:
            break
check(bool(thought) and found, "jina verbatim THOUGHT text present in raw bytes")

# --- 3. command profile re-derivation ---
cp = [r for r in obss
      if r["body"]["data"].get("category") == "shell-command-profile"]
models_in_steps = set()
pf = pq.ParquetFile(F1)
for batch in pf.iter_batches(columns=["model", "steps"], batch_size=20000):
    for row in batch.to_pylist():
        s = row["steps"]
        if s and s != "null":
            models_in_steps.add(str(row["model"]))
check(len(cp) == len(models_in_steps),
      f"cmd profiles {len(cp)} == models with steps {len(models_in_steps)}")
check(set(r["tags"]["model"] for r in cp) == models_in_steps,
      "cmd profile model set matches bytes")

# --- 4. URL re-derivation (spot check top term) ---
ur = [r for r in obss if r["body"]["type"] == "infra.ioc"]
terms = [r["body"]["data"]["term"] for r in ur]
check(len(terms) == len(set(terms)), "URL terms unique in batch")
check(all("\\" not in t and not re.search(r"\s", t) for t in terms),
      "no regex-artifact URLs submitted")
# recount the top term from bytes
top = max(ur, key=lambda r: int(r["tags"]["fetch_count"]))
tc = sum(1 for rg in range(pf.num_row_groups)
         for s in pf.read_row_group(rg, columns=["steps"])
         .column("steps").to_pylist()
         if s and s != "null" and top["body"]["data"]["term"] in s)
check(tc == int(top["tags"]["fetch_count"]),
      f"URL spot-check {top['body']['data']['term'][:50]} count {tc}")

print()
print("ERRORS:", len(errors))
for e in errors:
    print(" -", e)
raise SystemExit(1 if errors else 0)
