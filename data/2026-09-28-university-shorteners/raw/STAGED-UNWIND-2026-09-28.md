# Staged unwind — university-shorteners (workstream E, 2026-09-28)

## Violation
Primary index `university-shorteners` holds 16 docs; 5 of them are
`yourls_stats_detail` docs that each collapse N per-URL referrer rows into one
doc (740 / 57 / 285 / 77 / 28 = 1,187 rows), plus 305 daily traffic points
buried in slug-level summary docs. Standing rule: PRIMARY INDEXES HOLD
EXPLICIT EVENTS ONLY — rollups go in `<index>-rollup`.

## Staged payloads (this directory tree)
- `staged_primary/university-shorteners_explicit.jsonl` — 1,520 docs,
  regenerated from the canonical explicit-event dataset
  (`data/university-shorteners-events/university-shorteners-events.jsonl`)
  with top-level `_id = labels.event_id`:
  - 1,188 `yourls_referrer_url` docs (one per observed referrer-URL row;
    keep-all policy — genuine duplicate (host, URL) observations preserved,
    disambiguated by `:dupN` event_id suffixes).
  - 308 `yourls_daily_hits` docs (one per (slug, date, series) point).
  - 13 `yourls_country_hits` docs.
  - 11 `yourls_stats_page` docs.
  All carry `event.dataset=university-shorteners`, `@timestamp`, `record_kind`.
  (The earlier 1,492-doc staging was an incomplete build from the pre-rebuild
  evidence files — missing 1 referrer row, 3 daily points, and the 13 country
  + 11 stats-page records entirely. Corrected 2026-09-28.)
  sha256: 07a5586d10f0f08b8dc2ea51deadf5cb0a73c66bde91075fe05276de15cb9090
- `staged_rollup/university-shorteners-rollup.jsonl` — the 16 current
  slug-summary docs, exported read-only from the live index with original
  `_id`s (`yourls:<instance>:<slug>`), to be MOVED into
  `university-shorteners-rollup`.
  sha256: 9f402045df10f9d02c1380394268295c972343543ff877580069e8c216be1b14

## Coordination
No shortener re-explosion lane is running (checked 2026-09-28 ~18:20 UTC:
no subagent, no process, no uncommitted shortener work beyond workstream B's
committed 16-doc state). This unwind owns the university-shorteners re-explosion.

## Execution (blocked until the write pause lifts)
`scripts/es_unwind_university_shorteners.py --execute` refuses to run while
`notes/ELASTIC_WRITE_PAUSE` exists. Sequence when resumed:
1. Create `university-shorteners-rollup` (canonical mapping), bulk 16 docs,
   verify _count=16.
2. Bulk 1,520 explicit docs into `university-shorteners`, verify interim 1536.
3. Bulk-delete the 16 rollup _ids from `university-shorteners`,
   verify primary _count=1520, rollup _count=16.
4. Verify `event.dataset.keyword` on both indexes.

Nothing has been written to the cloud cluster by this staging work.
