#!/usr/bin/env python3
"""SCRATCH (temp/): Phase 2 reference patches for R1/R2/R3 moves.
Applies exact old->new path string replacements in the scripts each worker
identified. Prints every change. Run from repo root.
"""
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)

# (script, [(old, new), ...]) — exact strings as they appear in the file
PATCHES = {
    # R1: collusion-wiki raw layer
    "scripts/extract_wiki_proxy_urls.py": [
        ('collusion-wiki/revisions.jsonl.gz', 'collusion-wiki/raw/revisions.jsonl.gz'),
        ('collusion-wiki/links.jsonl.gz', 'collusion-wiki/raw/links.jsonl.gz'),
        ('collusion-wiki/records.jsonl.gz', 'collusion-wiki/raw/records.jsonl.gz'),
    ],
    "scripts/es_ingest_powerbi.py": [
        ('/data/collusion-wiki/records.jsonl', '/data/collusion-wiki/raw/records.jsonl'),
        ('/data/collusion-wiki/revisions.jsonl', '/data/collusion-wiki/raw/revisions.jsonl'),
    ],
    # R1: cors-bwa-proxy -> aggregates + raw
    "scripts/es_ingest_cors_bwa.py": [
        ('data/cors-bwa-proxy', 'data/aggregates/cors-bwa-proxy'),
        ('bwa_targets.jsonl', 'raw/bwa_targets.jsonl'),
        ('ladder_edges.jsonl', 'raw/ladder_edges.jsonl'),
    ],
    "scripts/cors_bwa_other_hosts.py": [
        ('data/cors-bwa-proxy', 'data/aggregates/cors-bwa-proxy'),
    ],
    "scripts/cors_bwa_collect.py": [
        ('data/cors-bwa-proxy', 'data/aggregates/cors-bwa-proxy'),
    ],
    "scripts/cors_bwa_ladders.py": [
        ('data/cors-bwa-proxy', 'data/aggregates/cors-bwa-proxy'),
        ('bwa_targets.jsonl', 'raw/bwa_targets.jsonl'),
        ('ladder_edges.jsonl', 'raw/ladder_edges.jsonl'),
    ],
    "scripts/cors_bwa_analyze.py": [
        ('data/cors-bwa-proxy', 'data/aggregates/cors-bwa-proxy'),
        ('bwa_targets.jsonl', 'raw/bwa_targets.jsonl'),
        ('ladder_edges.jsonl', 'raw/ladder_edges.jsonl'),
    ],
    # R2: paste archives
    "scripts/es_ingest_paste_archive.py": [
        ('{D}/k4be.pl/metadata.jsonl', '{D}/raw/k4be.pl/metadata.jsonl'),
        ('{D}/anna.fyi/titles.jsonl', '{D}/raw/anna.fyi/titles.jsonl'),
        ('{D}/infinitypaste.club/metadata.jsonl', '{D}/raw/infinitypaste.club/metadata.jsonl'),
    ],
    "scripts/es_ingest_paste.py": [
        ('PDIR + "/manifest.jsonl"', 'PDIR + "/raw/manifest.jsonl"'),
    ],
    "scripts/es_ingest_ludism.py": [
        ('PDIR + "/manifest.jsonl"', 'PDIR + "/raw/manifest.jsonl"'),
    ],
    "scripts/ludism_manifest.py": [
        ('DDIR + "/manifest.jsonl"', 'DDIR + "/raw/manifest.jsonl"'),
    ],
    # R3: boards/scans/misc
    "scripts/es_ingest_public_board.py": [
        ('data/public-board/notes.jsonl', 'data/public-board/raw/notes.jsonl'),
        ('/data/public-board/notes.jsonl', '/data/public-board/raw/notes.jsonl'),
        ('"notes.jsonl"', '"raw/notes.jsonl"'),
    ],
    "scripts/es_ingest_rmn_history.py": [
        ('slug_evolution.jsonl', 'raw/slug_evolution.jsonl'),
    ],
    "scripts/sweep_july7.py": [
        ('july7-wave/diffend_sweep_results_july7.jsonl', 'july7-wave/raw/diffend_sweep_results_july7.jsonl'),
        ('/diffend_sweep_results_july7.jsonl', '/raw/diffend_sweep_results_july7.jsonl'),
    ],
    "scripts/es_upsert_july7_resweep.py": [
        ('diffend_sweep_results_july7.jsonl', 'raw/diffend_sweep_results_july7.jsonl'),
        ('diffend_sweep_resweep_july7.jsonl', 'raw/diffend_sweep_resweep_july7.jsonl'),
    ],
    "scripts/es_ingest_july7.py": [
        ('diffend_sweep_results_july7.jsonl', 'raw/diffend_sweep_results_july7.jsonl'),
    ],
    "scripts/diffend_sweep_resweep_july7.py": [
        ('diffend_sweep_results_july7.jsonl', 'raw/diffend_sweep_results_july7.jsonl'),
        ('diffend_sweep_resweep_july7.jsonl', 'raw/diffend_sweep_resweep_july7.jsonl'),
    ],
    "scripts/es_unwind_admin_deletions.py": [
        ('admin-deletions/hits.jsonl', 'admin-deletions/raw/hits.jsonl'),
        ('staged_rollup/admin-deletions-rollup.jsonl', 'raw/admin-deletions-rollup.jsonl'),
    ],
    "scripts/es_unwind_university_shorteners.py": [
        ('staged_primary/', 'raw/staged_primary/'),
        ('staged_rollup/', 'raw/staged_rollup/'),
    ],
}

# tantive-space: dir-iteration patterns (messages.jsonl/threads.jsonl under
# the collection dir) need manual inspection — handled separately.

total = 0
for path, pairs in PATCHES.items():
    if not os.path.exists(path):
        print(f"MISSING SCRIPT: {path}")
        continue
    src = open(path).read()
    out = src
    applied = []
    for old, new in pairs:
        if old in out:
            out = out.replace(old, new)
            applied.append(old)
    if out != src:
        open(path, "w").write(out)
        total += 1
        print(f"patched {path}: {len(applied)} replacements")
        for a in applied:
            print(f"    {a}")
    else:
        print(f"NO MATCH in {path} — inspect manually")
print(f"\n{total} scripts patched")
