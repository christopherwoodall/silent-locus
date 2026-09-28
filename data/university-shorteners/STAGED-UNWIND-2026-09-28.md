# Staged unwind — university-shorteners (workstream E, 2026-09-28)

## Violation
Primary index `university-shorteners` holds 16 docs; 5 of them are
`yourls_stats_detail` docs that each collapse N per-URL referrer rows into one
doc (740 / 57 / 285 / 77 / 28 = 1,187 rows), plus 305 daily traffic points
buried in slug-level summary docs. Standing rule: PRIMARY INDEXES HOLD
EXPLICIT EVENTS ONLY — rollups go in `<index>-rollup`.

## Staged payloads (this directory tree)
- `staged_primary/university-shorteners_explicit.jsonl` — 1,492 docs:
  - 1,187 `shortener_referrer_row` docs (one per referrer-URL row in the
    `*_referrer_urls_daily_*.json` evidence files; keep-all policy — duplicate
    listings kept, disambiguated by occurrence suffix).
    `_id = yourlsref:<instance>:<slug>:<sha16(host|url)>#<occurrence>`.
  - 305 `shortener_daily_hits` docs (one per (slug, date, series) point;
    dates normalized to ISO `YYYY-MM-DD`).
    `_id = yourlsdaily:<instance>:<slug>:<series>:<date>`.
  All carry `event.dataset=university-shorteners`, `@timestamp`, `record_kind`.
  sha256: 7c10a86621330d6e83b9de4e590d388b10fc8a104e
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
2. Bulk 1,492 explicit docs into `university-shorteners`, verify interim 1508.
3. Bulk-delete the 16 rollup _ids from `university-shorteners`,
   verify primary _count=1492, rollup _count=16.
4. Verify `event.dataset.keyword` on both indexes.

Nothing has been written to the cloud cluster by this staging work.
