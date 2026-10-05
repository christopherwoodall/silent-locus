#!/usr/bin/env python3
"""SCRATCH (temp/): Phase 2 reference patches for R5 renames + R2 tantive
dir-iteration scripts + the two manual cases from the R1-R3 pass.
Exact-string replacements only; prints every change. Run from repo root.
"""
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)

PATCHES = {
    # manual leftovers from R1-R3 pass
    "scripts/es_ingest_public_board.py": [
        ('{D}/notes.jsonl', '{D}/raw/notes.jsonl'),
    ],
    "scripts/sweep_july7.py": [
        ('OUTDIR, "diffend_sweep_results_july7.jsonl"',
         'OUTDIR, "raw", "diffend_sweep_results_july7.jsonl"'),
    ],
    # R2 tantive dir-iteration (messages.jsonl / threads.jsonl moved to raw/)
    "scripts/es_ingest_tantive.py": [
        ('("messages.jsonl", "threads.jsonl")', '("raw/messages.jsonl", "raw/threads.jsonl")'),
    ],
    "scripts/tantive_pull.py": [
        ('"threads.jsonl"', '"raw/threads.jsonl"'),
        ('"messages.jsonl"', '"raw/messages.jsonl"'),
    ],
    "scripts/tantive_sweep.py": [
        ('"messages.jsonl"', '"raw/messages.jsonl"'),
        ('"threads.jsonl"', '"raw/threads.jsonl"'),
    ],
    # R5 rename references
    "scripts/fix_iowa_timestamps_pastebin_fp_2026_09_28.py": [
        ('data/pastebin-cluster-sweep/sweep.jsonl',
         'data/pastebin-cluster-sweep/pastebin-cluster-sweep.jsonl'),
    ],
    "scripts/backfill_schema_2026_09_28.py": [
        ('data/pastebin-cluster-sweep/sweep.jsonl',
         'data/pastebin-cluster-sweep/pastebin-cluster-sweep.jsonl'),
        ('data/webhook-deaddrops/webhook-deaddrop-hits-2026-09-27.jsonl',
         'data/webhook-deaddrops/webhook-deaddrops.jsonl'),
        ('data/admin-deletions/staged_primary/admin-deletions_explicit.jsonl',
         'data/admin-deletions/admin-deletions-explicit.jsonl'),
        ('data/admin-deletions/staged_rollup/admin-deletions-rollup-flat.jsonl',
         'data/admin-deletions/admin-deletions-rollup-flat.jsonl'),
    ],
    "scripts/es_ingest_webhook_deaddrops.py": [
        ('webhook-deaddrop-hits-2026-09-27.jsonl', 'webhook-deaddrops.jsonl'),
    ],
    "scripts/es_ingest_pxweb.py": [
        ('pxweb-national-stats/hits.jsonl', 'pxweb-national-stats/pxweb-national-stats.jsonl'),
    ],
    "scripts/es_unwind_admin_deletions.py": [
        ('staged_primary/admin-deletions_explicit.jsonl', 'admin-deletions-explicit.jsonl'),
    ],
    "scripts/diffend_targeted_check.py": [
        ('gem-temporal-pivot/diffend_targeted_check.jsonl',
         'gem-temporal-pivot/gem-temporal-pivot-diffend-targeted-check.jsonl'),
        ('"diffend_targeted_check.jsonl"', '"gem-temporal-pivot-diffend-targeted-check.jsonl"'),
    ],
    "scripts/diffend_temporal_sweep.py": [
        ('gem-temporal-pivot/diffend_temporal_sweep.jsonl',
         'gem-temporal-pivot/gem-temporal-pivot-diffend-temporal-sweep.jsonl'),
        ('"diffend_temporal_sweep.jsonl"', '"gem-temporal-pivot-diffend-temporal-sweep.jsonl"'),
    ],
    "scripts/july7_forensics_extract.py": [
        ('payload-reconstructions.jsonl', 'july7-gem-forensics-payload-reconstructions.jsonl'),
    ],
    "scripts/sweep_proxy_primitives.py": [
        ('osv/diffend_sweep_results.jsonl', 'osv/osv-diffend-sweep-results.jsonl'),
        ('"diffend_sweep_results.jsonl"', '"osv-diffend-sweep-results.jsonl"'),
    ],
    "scripts/gem83_reconciliation_build.py": [
        ('diffend_sweep_results_retry.jsonl', 'osv-diffend-sweep-results-retry.jsonl'),
        ('diffend_sweep_results.jsonl', 'osv-diffend-sweep-results.jsonl'),
    ],
    "scripts/diffend_sweep_retry.py": [
        ('diffend_sweep_results_retry.jsonl', 'osv-diffend-sweep-results-retry.jsonl'),
        ('diffend_sweep_results.jsonl', 'osv-diffend-sweep-results.jsonl'),
    ],
    "scripts/diffend_sweep.py": [
        ('"diffend_sweep_results.jsonl"', '"osv-diffend-sweep-results.jsonl"'),
        ('data/osv/diffend_sweep_results.jsonl', 'data/osv/osv-diffend-sweep-results.jsonl'),
    ],
    "scripts/diffend_merge_final.py": [
        ('diffend_sweep_results_retry.jsonl', 'osv-diffend-sweep-results-retry.jsonl'),
        ('diffend_sweep_results.jsonl', 'osv-diffend-sweep-results.jsonl'),
    ],
}

total, misses = 0, []
for path, pairs in PATCHES.items():
    if not os.path.exists(path):
        misses.append(f"MISSING SCRIPT: {path}")
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
    for old, _ in pairs:
        if old not in src:
            misses.append(f"{path}: no match for {old!r}")
print(f"\n{total} scripts patched")
for m in misses:
    print("MISS:", m)
