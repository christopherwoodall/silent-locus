#!/usr/bin/env python3
"""Concatenate 42 dockerhub-trojan-images-*.jsonl files into events.jsonl.

- Sorted-filename order.
- Each record gets labels.file_origin = <old basename> (create labels if missing; report).
- Output written via temp file + os.replace.
- After verification, delete the 42 source files (content 100% preserved).
"""
import json
import os
import sys
import random

DIR = "/mnt/c/Users/chris/Desktop/projects/silent-locus/data/2026-09-28-dockerhub-trojan-images"
OUT = os.path.join(DIR, "events.jsonl")
TMP = OUT + ".tmp"

def main():
    sources = sorted(
        f for f in os.listdir(DIR)
        if f.startswith("dockerhub-trojan-images-") and f.endswith(".jsonl")
    )
    print(f"source files: {len(sources)}")
    for f in sources:
        print(f"  {f}")
    assert len(sources) == 42, f"expected 42 sources, got {len(sources)}"

    total = 0
    per_file = {}
    missing_labels = []
    with open(TMP, "w", encoding="utf-8") as out:
        for fname in sources:
            n = 0
            with open(os.path.join(DIR, fname), encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    rec = json.loads(line)
                    if "labels" not in rec or not isinstance(rec["labels"], dict):
                        rec.setdefault("labels", {})
                        missing_labels.append((fname, n))
                    rec["labels"]["file_origin"] = fname
                    out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    n += 1
            per_file[fname] = n
            total += n
    os.replace(TMP, OUT)

    # verification
    expected = 42318
    with open(OUT, encoding="utf-8") as fh:
        out_lines = sum(1 for _ in fh)
    print(f"input total: {total}, expected: {expected}, output lines: {out_lines}")
    assert total == expected == out_lines, "line count mismatch"

    # spot-check 3 random records
    with open(OUT, encoding="utf-8") as fh:
        lines = fh.readlines()
    for i in random.sample(range(len(lines)), 3):
        rec = json.loads(lines[i])
        print(f"spot-check line {i}: labels.file_origin={rec['labels'].get('file_origin')}")

    if missing_labels:
        print(f"WARNING: {len(missing_labels)} records missing labels (created): {missing_labels[:5]}")
    else:
        print("no records missing labels object")

    # delete sources only after successful verification
    for fname in sources:
        os.remove(os.path.join(DIR, fname))
    print("deleted 42 source files")

if __name__ == "__main__":
    main()
