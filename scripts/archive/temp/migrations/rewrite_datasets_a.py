#!/usr/bin/env python3
"""Rewrite event.dataset in event JSONL files for collections whose slug sorts A-M.

Scope rule: from temp/dataset_targets.json, take keys whose slug part
(basename minus leading YYYY-MM-DD- date prefix) sorts < "n". Covers both
data/<dir>/ and data/aggregates/<dir>/ parents.

Idempotent: re-run leaves files unchanged (dataset already == target).
"""
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
DATA = os.path.join(ROOT, "data")
AGG = os.path.join(DATA, "aggregates")
MAP_PATH = os.path.join(os.path.dirname(__file__), "dataset_targets.json")
REPORT_PATH = os.path.join(os.path.dirname(__file__), "rewrite_datasets_a_report.json")

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")

# Per-file exception: this file gets the rollup dataset value.
EXCEPTION_DIR = "2026-06-04-admin-deletions"
EXCEPTION_FILE = "admin-deletions-rollup-flat.jsonl"
EXCEPTION_VALUE = "2026-06-04-admin-deletions-rollup"


def slug_of(basename):
    return DATE_RE.sub("", basename)


def my_keys(targets):
    return {k: v for k, v in targets.items() if slug_of(k) < "n"}


def event_files(dirpath):
    out = []
    for dirpath2, _dirs, files in os.walk(dirpath):
        rel = os.path.relpath(dirpath2, dirpath)
        if "raw" in rel.split(os.sep):
            continue
        for f in sorted(files):
            if f.endswith(".jsonl"):
                out.append(os.path.join(dirpath2, f))
    return sorted(out)


def rewrite_file(path, target):
    """Rewrite event.dataset per line. Returns (before_wc, after_wc, old_counter, changed)."""
    old_counter = Counter()
    tmp_path = path + ".rewrite_tmp"
    before_wc = 0
    after_wc = 0
    missing_event = 0
    with open(path, "r", encoding="utf-8") as fin, \
         open(tmp_path, "w", encoding="utf-8") as fout:
        for line in fin:
            before_wc += 1
            stripped = line.strip()
            if not stripped:
                fout.write(line)
                after_wc += 1
                continue
            rec = json.loads(stripped)
            ev = rec.get("event")
            if ev is None:
                ev = {}
                rec["event"] = ev
                missing_event += 1
            old_val = ev.get("dataset")
            old_counter[str(old_val)] += 1
            ev["dataset"] = target
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
            after_wc += 1
    if before_wc != after_wc:
        os.remove(tmp_path)
        raise RuntimeError(f"line count mismatch in {path}: {before_wc} vs {after_wc}")
    os.replace(tmp_path, path)
    return before_wc, after_wc, old_counter, missing_event


def main():
    with open(MAP_PATH, encoding="utf-8") as f:
        targets = json.load(f)
    mine = my_keys(targets)
    report = {}
    for key in sorted(mine):
        target = mine[key]
        found = False
        for parent in (DATA, AGG):
            d = os.path.join(parent, key)
            if not os.path.isdir(d):
                continue
            found = True
            dir_report = {"target": target, "parent": os.path.relpath(parent, ROOT),
                          "files": {}}
            for fp in event_files(d):
                t = target
                if key == EXCEPTION_DIR and os.path.basename(fp) == EXCEPTION_FILE:
                    t = EXCEPTION_VALUE
                bw, aw, oldc, mev = rewrite_file(fp, t)
                dir_report["files"][os.path.relpath(fp, d)] = {
                    "target_used": t,
                    "lines_before": bw,
                    "lines_after": aw,
                    "old_dataset_values": dict(oldc),
                    "missing_event_dict": mev,
                }
            report[key] = dir_report
        if not found:
            report[key] = {"error": "directory not found under data/ or data/aggregates/"}
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1, ensure_ascii=False)
    print(json.dumps(report, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
