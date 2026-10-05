#!/usr/bin/env python3
"""SCRATCH (temp/): Wave A moves — loose data/ files into collection dirs
and patch every scripts/*.py path reference. Prints a full change log.

Run from repo root:  python3 temp/move_loose_files.py
"""
import glob
import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)

MOVES = {
    "data/overlap-analysis": [
        "matches-f1f2.jsonl", "matches-f3.jsonl",
        "matches-f4f7f8f10f11f12.jsonl", "matches-f5f6.jsonl",
        "overlap-matches.jsonl", "wiki_ioc_pivots.jsonl",
        "wiki_paste_links.jsonl", "wiki_gem_bridge.json",
        "wiki_ioc_pivot_summary.json", "wiki_shortener_detail.json",
        "jsonhero_doc_links.jsonl",
    ],
    "data/rubygems-goimport-campaign": [
        "gem-graph-edges.jsonl", "gem-graph-edges.jsonl.pre-bulk",
        "gem-graph-nodes.jsonl", "gem-graph-nodes.jsonl.pre-bulk",
        "gem-ioc-hits.jsonl", "gem-ioc-hits.jsonl.pre-bulk",
        "gem-ioc-log.jsonl", "gem-ioc-log.jsonl.pre-bulk",
        "gem-iocs-2026-09-27.jsonl", "gem-june18-wayback.jsonl",
        "gem-pins-batch1.txt", "gem-pins-batch2.txt",
        "gem-pins-batch3.txt", "gem-pins-batch4.txt",
        "gem-pins-diffend.txt", "gemstuffer-jfrog-2026-09-27.csv",
    ],
}

log = []

# 1) moves
for dest_dir, files in MOVES.items():
    os.makedirs(dest_dir, exist_ok=True)
    for f in files:
        src = os.path.join("data", f)
        dst = os.path.join(dest_dir, f)
        if not os.path.exists(src):
            log.append(f"MISSING SOURCE (skipped): {src}")
            continue
        if os.path.exists(dst):
            log.append(f"TARGET EXISTS (skipped): {dst}")
            continue
        shutil.move(src, dst)
        log.append(f"mv {src} -> {dst}")

# 2) path patches in scripts/*.py (exact string, longest first so
#    e.g. gem-ioc-log.jsonl beats gem-ioc-log variants)
pairs = []
for dest_dir, files in MOVES.items():
    for f in sorted(files, key=len, reverse=True):
        pairs.append((f"data/{f}", f"{dest_dir}/{f}"))

patched = {}
for path in sorted(glob.glob("scripts/*.py")):
    src = open(path).read()
    out = src
    for old, new in pairs:
        out = out.replace(f'"{old}"', f'"{new}"').replace(f"'{old}'", f"'{new}'")
    if out != src:
        open(path, "w").write(out)
        hits = [old for old, _ in pairs if f'"{old}"' in src or f"'{old}'" in src]
        patched[path] = hits
        log.append(f"patched {path}: {', '.join(hits)}")

print("\n".join(log))
print(f"\n{sum(1 for l in log if l.startswith('mv '))} moved, "
      f"{len(patched)} scripts patched")
if any("skipped" in l.lower() for l in log):
    sys.exit(1)
