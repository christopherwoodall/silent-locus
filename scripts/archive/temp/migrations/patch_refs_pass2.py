#!/usr/bin/env python3
"""SCRATCH (temp/): Wave A pass 2 — catch path references pass 1 missed:
BASE + "/data/<file>" and os.path.join(BASE, "data", "<file>") styles,
plus docstring prose mentions. Prints every change.

Run from repo root:  python3 temp/patch_refs_pass2.py
"""
import glob
import os
import re

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
os.chdir(REPO)

FILES = {
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

# longest names first; match /data/<f> and bare 'data/<f>' at word boundary,
# but never when already prefixed by a directory (e.g. data/overlap-analysis/)
pairs = []
for dest, names in FILES.items():
    for n in sorted(names, key=len, reverse=True):
        pairs.append((n, dest))

changed = {}
for path in sorted(glob.glob("scripts/*.py")):
    src = open(path).read()
    out = src
    for name, dest in pairs:
        # /data/<name> not preceded by an existing subdir hop
        out = re.sub(r'(?<![\w/-])/data/' + re.escape(name) + r'(?![\w.-])',
                     "/" + dest + "/" + name, out)
        # bare data/<name> at start of string/after quote/whitespace
        out = re.sub(r'(?<![\w/.-])data/' + re.escape(name) + r'(?![\w.-])',
                     dest + "/" + name, out)
    if out != src:
        open(path, "w").write(out)
        diff = sorted({name for name, _ in pairs
                       if re.search(re.escape(name), src)
                       and (dest + "/" + name) in out and ("/data/" + name) in src
                       or re.search(r'(?<![\w/.-])data/' + re.escape(name) + r'(?![\w.-])', src)})
        changed[path] = diff

for p, names in changed.items():
    print(f"patched {p}: {', '.join(names)}")
print(f"\n{len(changed)} scripts patched in pass 2")
