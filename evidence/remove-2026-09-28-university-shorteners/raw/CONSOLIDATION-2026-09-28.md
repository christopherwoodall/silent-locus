# Consolidation — university-shorteners family (2026-09-28, workstream A)

## Decision: ONE index for the shortener family

Batches 1 and 2 of the shortener sweep are the same dataset family
(public YOURLS per-link stats pages, canonical shared schema from
`notes/gems-es-mapping.json`), so both JSONL files now ingest into a
single index **`university-shorteners`**. Batch provenance is preserved
per-doc in `event.dataset` (multi-field `.keyword` present) and in
`labels.shortener.*`:

| Source file (untouched on disk) | event.dataset | docs |
|---|---|---|
| `data/university-shorteners/university-shorteners.jsonl` | `university-shorteners` | 7 |
| `data/university-shorteners-batch2/university-shorteners-batch2.jsonl` | `university-shorteners-batch2` | 1 |

Live `_count` on `university-shorteners` = **8** (buckets: 7 + 1).
Doc IDs are deterministic: `yourls:<instance>:<slug>` — re-runs overwrite,
no duplicates. Zero top-level fields outside the canonical mapping;
`event.dataset.keyword` aggregation verified.

## Retired

- Index `university-shorteners-batch2` was deleted after the verified
  consolidate (no Kibana saved objects referenced it; grep of
  `kibana-exports/` clean). The batch-2 dataset dir on disk is untouched:
  `university-shorteners-batch2.jsonl`, `PROVENANCE.md`, `SHA256SUMS`,
  `progress.log`, evidence files all intact.
- The old per-batch ingest scripts
  (`scripts/es_ingest_university_shorteners.py`,
  `scripts/es_ingest_university_shorteners_batch2.py`) are kept as history;
  the canonical path is now
  `scripts/es_ingest_university_shorteners_consolidated.py`.

## Kept separate (by design)

- **`pxweb-national-stats`** (12 docs, `record_kind=stats_api_target`): a
  stats-API task-target family, not a shortener-stats family. Rebuilt
  2026-09-28 with deterministic IDs
  (`stats:<sha256(record_kind|matched_string|source_url)[:16]>`) via the
  rewritten `scripts/es_ingest_pxweb.py` — the old revision used
  auto-generated ES IDs (re-ingest would have duplicated) and carried a dead
  `load()` path; both fixed. Live `_count` = 12, no field drift.
- **`uoft-shorteners`**: lane O recorded clean negatives only (login walls,
  SEO-spam slugs) — no ES index, per the lane's verification bar. Nothing
  to consolidate.

## Re-verify commands

```
python3 scripts/es_ingest_university_shorteners_consolidated.py --verify
python3 scripts/es_ingest_pxweb.py --verify
```

## Addendum 2026-09-28 17:55Z — batch3 consolidated, count 15

Commit d559942 folded batch-3 (go.uvm.edu, 3 docs, `event.dataset=university-shorteners-batch3`)
into `university-shorteners` and retired index `university-shorteners-batch3` (404 verified).
Live `_count` = **15** (11 + 3 + 1). The C3 gap-recovery progress.log entry (11:40Z) predates
that merge, hence its "index now 12 docs" line — stale, not wrong at write time.
`scripts/es_ingest_university_shorteners_consolidated.py` is the canonical ingest: it now
reads all three JSONL sources and asserts 15 with the three-bucket breakdown (`--verify` green).
