# Staged unwind — admin-deletions (workstream E, 2026-09-28)

## Violation
Primary index `admin-deletions` holds 26 per-day summary docs
(`record_kind=admin_cleanup_burst`); the 5,217 verbatim delete events in
`data/admin-deletions/hits.jsonl` were never indexed. Standing rule: PRIMARY
INDEXES HOLD EXPLICIT EVENTS ONLY — rollups go in `<index>-rollup`.

## Staged payloads (this directory tree)
- `staged_primary/admin-deletions_explicit.jsonl` — 5,217 docs, one per row of
  `hits.jsonl`. `_id` = the row's `event_id` (verified unique); `@timestamp` =
  row `time`; `event.dataset=admin-deletions`; `record_kind=delete_event`.
  sha256: 8a116db5a70778590d65b33af340f51b36ee1f1c8aa9ff91c951acfccb2ec829
- `staged_rollup/admin-deletions-rollup.jsonl` — the 26 current per-day docs,
  exported read-only from the live index with original `_id`s
  (`admin-deletions:YYYY-MM-DD`), to be MOVED into `admin-deletions-rollup`.
  sha256: 62b552fe294d32a8935d0dbb39f59d5672bdd06400e375cd1f9d4d54a8

## Execution (blocked until the write pause lifts)
`scripts/es_unwind_admin_deletions.py --execute` refuses to run while
`notes/ELASTIC_WRITE_PAUSE` exists. Sequence when resumed:
1. Create `admin-deletions-rollup` (canonical mapping notes/gems-es-mapping.json),
   bulk 26 rollup docs, verify _count=26.
2. Bulk 5,217 explicit docs into `admin-deletions` (deterministic _ids),
   verify interim _count=5243.
3. Bulk-delete the 26 rollup _ids from `admin-deletions`,
   verify primary _count=5217, rollup _count=26.
4. Verify `event.dataset.keyword` on both indexes.

Nothing has been written to the cloud cluster by this staging work.
