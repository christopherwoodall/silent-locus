#!/usr/bin/env python3
"""SCRATCH (temp/): Phase 2 reference patches for R4 (aggregates moves,
rubygems raw layer, overlap-analysis raw+backfill). Two passes:
1) dir-prefix moves, 2) raw/ insertions for consumed files.
Prints every change. Run from repo root.
"""
import glob
import os

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
os.chdir(REPO)

PASS1 = [  # directory moves (order: longest first)
    ("data/overlap-analysis/", "data/aggregates/overlap-analysis/"),
    ("data/gem83-reconciliation", "data/aggregates/gem83-reconciliation"),
    ("data/proxy-primitives", "data/aggregates/proxy-primitives"),
    # rubygems raw layer: every data file moved under raw/
    ("data/rubygems-goimport-campaign/gem-", "data/rubygems-goimport-campaign/raw/gem-"),
    ("data/rubygems-goimport-campaign/gemstuffer-", "data/rubygems-goimport-campaign/raw/gemstuffer-"),
]
PASS2 = [  # raw/ insertions for script-consumed files (post-PASS1 strings)
    ('"/gem83-reconciliation.jsonl"', '"/raw/gem83-reconciliation.jsonl"'),
    ("'/gem83-reconciliation.jsonl'", "'/raw/gem83-reconciliation.jsonl'"),
    ('/gem83-reconciliation.jsonl"', '/raw/gem83-reconciliation.jsonl"'),
    ("overlap-analysis/wiki_ioc_pivots.jsonl", "overlap-analysis/raw/wiki_ioc_pivots.jsonl"),
    ("overlap-analysis/jsonhero_doc_links.jsonl", "overlap-analysis/raw/jsonhero_doc_links.jsonl"),
    # proxy-primitives event file rename
    ("proxy-primitives/hits.jsonl", "proxy-primitives/proxy-primitives.jsonl"),
    ('"hits.jsonl"', '"proxy-primitives.jsonl"'),  # only safe in the 3 proxy scripts, filtered below
]

PROXY_SCRIPTS = {"scripts/es_ingest_proxy_primitives.py",
                 "scripts/sweep_proxy_primitives.py",
                 "scripts/extract_wiki_proxy_urls.py"}

for path in sorted(glob.glob("scripts/*.py")):
    src = open(path).read()
    out = src
    for old, new in PASS1:
        out = out.replace(old, new)
    for old, new in PASS2:
        if old == '"hits.jsonl"' and path not in PROXY_SCRIPTS:
            continue
        out = out.replace(old, new)
    if out != src:
        open(path, "w").write(out)
        print(f"patched {path}")
print("done")
