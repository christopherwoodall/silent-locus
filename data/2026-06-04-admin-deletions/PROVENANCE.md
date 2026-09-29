# data/admin-deletions/ — provenance

Lane R (admin-deletion recurrence check), 2026-09-28. Follow-up to lane P's
open question: do the dse wiki admin's deletion sweeps recur before other runs?

## Source

`data/collusion-wiki/events.jsonl.gz` (19,913 events), filtered to
`event_type == "delete"`. No other transformation: `hits.jsonl` carries the
original event records verbatim (one JSON object per line, sorted by `time`).

## Selection

- All delete events in the corpus: **5,217 unique event_ids**
  (2026-06-04T10:53:40Z → 2026-07-14T13:56:54Z).
- Exact-duplicate event_ids: **0** (no dedup needed; checked).
- Invariants across all 5,217: actor `[Admin1]` ip16 `2.202`, wiki `dse`,
  `change_summary` "Seite gelöscht." (page deleted), `time_grade` `reqlog`.

## Cross-check

ES index `collusion-wiki`: 5,217 docs whose `_id` matches
`wiki:event:delete:*` — **exact per-day match with the JSONL counts on all 26
active days** (the 4 apparent extras on 06-19/06-21 were `revert` events whose
`_id` merely contains the string ":delete:"; excluded). Verification script
paged 2026-03-01..2026-07-15 in day chunks and compared `_id` sets directly.

## Derived files

- `hits.jsonl` — 5,217 delete events (full original records).
- `per-day-stats.json` — per active day: count, first/last timestamps,
  burst sessions (gaps > 60 min), top page-name grammar roots.
- ES index `admin-deletions` — 26 per-day summary docs built from the
  canonical shared schema (`notes/gems-es-mapping.json`), `event.dataset` =
  `admin-deletions`, `event.dataset.keyword` multi-field present at creation.

## Collection method

Read-only. No submissions, logins, or writes to any external venue.
Extraction script is idempotent (re-run `python3` filter over the same
`.gz`; resumable by re-writing `hits.jsonl`).

Retrieved: 2026-09-28. No external retrieval — corpus is local.

## Closure 2026-09-28 (workstream C)

Naturally small: 26 per-day summary docs built from the full 5,217 dse-wiki
admin deletion events (2026-06-04 → 2026-07-14); the raw 5,217 records are
preserved verbatim in hits.jsonl and matched exactly against the collusion-wiki
index per day. N=26 is bounded by the 26 active deletion days — no further
summaries are constructible. ES `admin-deletions` _count=26 verified,
schema-drift clean.

## Raw layer 2026-09-29

- `hits.jsonl` -> `raw/hits.jsonl` (upstream capture; referenced only in docstring of scripts/es_unwind_admin_deletions.py) and `staged_rollup/admin-deletions-rollup.jsonl` -> `raw/admin-deletions-rollup.jsonl` (transform intermediate; consumer: scripts/es_unwind_admin_deletions.py). Upstream names preserved; raw layer exempt from event schema. `staged_rollup/admin-deletions-rollup-flat.jsonl` and `staged_primary/admin-deletions_explicit.jsonl` are manifest-staged event files handled separately.

## Canonical layout migration (2026-09-29)

Renamed `admin-deletions-explicit.jsonl` -> `events.jsonl` and `admin-deletions-rollup-flat.jsonl` -> `rollup.jsonl`, contents unchanged (rollup records carry dataset `2026-06-04-admin-deletions-rollup`). No file_origin labels added (pure renames). NOTE: source basenames differed from the original migration spec (no date prefix); mapping adapted accordingly.
