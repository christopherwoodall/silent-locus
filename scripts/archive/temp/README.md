# Archived `temp/` scripts and artifacts

These files were preserved from the former repository-root `temp/` workspace.
They record one-off collection/layout/dataset migration work and wave builder
or backfill work; neither directory is an active pipeline. Original usage
strings mentioning `temp/` describe the historical invocation, not the
current location. In particular, many scripts write or delete data and must
not be executed without separately reviewing their historical inputs and
side effects. Map/report/log contents were moved unchanged as provenance.

Every basename below had the old path `temp/<basename>`; its new path is
`scripts/archive/temp/<group>/<basename>`, except maintenance tools, which
are now `scripts/maintenance/<basename>`. `temp/README.md` remains in place.

| Group | Basenames |
| --- | --- |
| `builders/` | `backfill_w1.py`, `backfill_w2.py`, `backfill_w3.py`, `backfill_w4.py`, `backfill_w6.py`, `build_events_w3_dse_wiki.py`, `build_events_w3_gems.py`, `build_events_w3_hf.py`, `build_events_w3_jsonhero_archive.py`, `build_events_w3_thecolony.py`, `build_w4.py` |
| `migrations/` | `concat_5cols.py`, `concat_dockerhub.py`, `concat_overlap.py`, `dataset_targets.json`, `date_fallbacks.json`, `date_map.json`, `failing_files.txt`, `failing_files_after.txt`, `index_map.json`, `layout_sweep.py`, `layout_sweep_report.json`, `move_loose_files.py`, `patch_refs_pass2.py`, `phase2_layout_patch.py`, `phase2_patch_r123.py`, `phase2_patch_r4.py`, `phase2_patch_r5.py`, `phase4_dated_refs.py`, `rewrite_a_run1.log`, `rewrite_a_run2.log`, `rewrite_datasets_a.py`, `rewrite_datasets_a_report.json`, `rewrite_datasets_b.py`, `rewrite_datasets_b_report.json`, `slug_map.json`, `slug_map_meta.json` |
| `scripts/maintenance/` | `audit_collections.py`, `checksum_sweep.py` |

The Python scripts whose repository root used to depend on their location
now resolve the root from their new location. Migration scripts that consume
maps/reports or produce reports resolve those artifacts beside themselves in
`migrations/`. Backfills retain their `--check` (non-writing) branch; their
historical dataset paths may no longer exist. No builder or migration was
executed during this move; the checksum sweep was **not** run.

References outside these owned directories still mentioning old paths:
`schema/README.md` (`temp/backfill_w1..w4.py`),
`notes/dir-triage-W3.md` (five `temp/build_events_w3_*.py` paths),
`notes/dir-triage-W4.md` (`temp/build_w4.py`), and
`notes/hf-hygiene-scan-2026-09-29.md` (`temp/build_w4.py:6`).
These historical documents were deliberately not edited.
