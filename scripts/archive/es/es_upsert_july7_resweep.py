#!/usr/bin/env python3
"""WORKSTREAM C2 — ES upsert for lane-J re-sweep rows.

Idempotent: upserts ONLY the rows written by
scripts/archive/collectors/diffend/diffend_sweep_resweep_july7.py
(rec['resweep_pass'] is True) into index july7-wave, using the deterministic
doc IDs july7:<name> from
data/2026-07-07-july7-wave/raw/scripts/legacy/es_ingest_july7.py's build_doc. Verified rows
from earlier passes are untouched.
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", ".."))
sys.path.insert(0, os.path.join(
    ROOT, "data", "2026-07-07-july7-wave", "raw", "scripts", "legacy"))
import es_ingest_july7 as base

SWEEP = os.path.join(
    ROOT, "data", "2026-07-07-july7-wave",
    "raw", "diffend_sweep_results_july7.jsonl")


def main():
    docs = {}
    names = []
    with open(SWEEP) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("resweep_pass"):
                docs["july7:%s" % rec["name"]] = base.build_doc(rec)
                names.append(rec["name"])
    print("upserting %d resweep docs" % len(docs), flush=True)
    ok, fail = base.bulk_load(docs)
    print("bulk ok=%d fail=%d" % (ok, fail), flush=True)
    total, found, july = base.verify()
    print("VERIFY: _count total=%d in_diffend=%d wave:july-7=%d" % (total, found, july))
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
