# 2026-06-04-admin-deletions: dse wiki [Admin1] admin-deletion recurrence sweep (5,217 delete events, 2026-06-04 -> 2026-07-14)

Lane R (admin-deletion recurrence check), built 2026-09-28, ingested into
Factum 2026-10-10 (batch `d71a22ef05e2418c99e84697aa2aac31`, 5,248 records).

## What this lane holds

- `events.jsonl` — 5,217 wiki page-deletion events on the dse wiki
  (2026-06-04T10:53:40Z → 2026-07-14T13:56:54Z). Every event: actor
  `[Admin1]`, ip16 `2.202`, change_summary "Seite gelöscht." (page deleted).
- `rollup.jsonl` — 26 per-day `admin_cleanup_burst` summary docs, one per
  active deletion day, with burst sessions and page-name grammar families.
- `raw/` — upstream captures: `hits.jsonl` (the 5,217 raw delete records),
  `admin-deletions-rollup.jsonl`, `per-day-stats.json`,
  `STAGED-UNWIND-2026-09-28.md`.
- `PROVENANCE.md` — collection method, selection, ES cross-check.
- `INGEST_NOTES.md` — Factum record mapping and validation for this ingest.
- `build_factum_bundle.py` — the script that built the ingest bundle.

## Factum records

- 1 `source` (collusion-wiki corpus), 2 `artifact` (events.jsonl,
  rollup.jsonl as git references), 2 `dataset.snapshot` observations.
- 5,217 `dataset.record` observations, one per delete event, tagged
  `{"lane":"2026-06-04-admin-deletions"}`, grade OBSERVED.
- 26 `dataset.record` observations for the per-day rollup docs
  (`record_subset: per-day-rollup`), grade INFERENCE (derived summaries).

No `in_lane` edges were submitted at ingest; edge building is a later pass.

Legacy directory (ingested, safe for later removal):
`evidence/remove-2026-06-04-admin-deletions/`.
