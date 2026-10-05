#!/usr/bin/env python3
"""Patch script references after canonical-layout migration (renames + raw sweep)."""
import json, glob, os

rep = json.load(open(os.path.join(os.path.dirname(__file__), "layout_sweep_report.json")))
pairs = []  # (old, new)

for s in rep["renames"]:
    old, new = s.split(" -> ")
    pairs.append(("data/" + old, "data/" + new))
# overlap-analysis concat (this phase)
for fn in ["matches-f1f2.jsonl", "matches-f3.jsonl", "matches-f4f7f8f10f11f12.jsonl",
           "matches-f5f6.jsonl", "overlap-matches.jsonl", "wiki_paste_links.jsonl"]:
    pairs.append(("data/aggregates/2026-09-29-overlap-analysis/" + fn,
                  "data/aggregates/2026-09-29-overlap-analysis/events.jsonl"))
# 6 multi-file dirs handled by concat workers (event-file paths -> events.jsonl)
for s in rep["moved_files"]:
    old, new = s.split(" -> ")
    pairs.append((old, new))
for s in rep["moved_dirs"]:
    old, new = s.split(" -> ")
    pairs.append((old, new))          # prefix-style, applied to substrings
for s in rep["scripts_moved"]:
    old, new = s.split(" -> ")
    pairs.append((old, new))

pairs.sort(key=lambda p: -len(p[0]))
pairs = [(o, n) for o, n in pairs if o != n]
print(f"{len(pairs)} path mappings")

hits = {}
targets = sorted(glob.glob("scripts/*.py") + glob.glob("scripts/*.sh") + ["Makefile"])
for f in targets:
    src = open(f, encoding="utf-8", errors="replace").read()
    orig = src
    for old, new in pairs:
        if old in src:
            src = src.replace(old, new)
            hits.setdefault(f, []).append(old)
    if src != orig:
        open(f, "w").write(src)

for f, olds in sorted(hits.items()):
    print(f"{f}: {len(olds)} mappings")
