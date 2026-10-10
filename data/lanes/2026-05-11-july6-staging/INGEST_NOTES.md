# INGEST_NOTES — 2026-05-11-july6-staging

## Mapping decisions

Legacy `record_kind` -> Factum `claim.property` (verbatim value), one claim per
legacy event (11 total):

| legacy kind | count | claim basis |
|---|---|---|
| staging_signal | 3 (2 delete-burst + 1 venue-preclaim) | OBSERVED |
| null_read | 5 | OBSERVED |
| comparator | 3 | INFERENCE |

- Claim `note` = legacy `description`, byte-identical (validator-checked).
- Claim `value` = structured object: legacy_doc_id, legacy_record_kind,
  legacy_fingerprint, full `labels` (verbatim), observer, source_url, @timestamp.
- Claim `subject` = the sweep run record (@run); `cites` = @run. Claims cannot
  cite `source` records (schema target-kinds restriction); the source record
  carries the locator `data/lanes/2026-05-11-july6-staging/events.jsonl`.
- Run: `run_kind=sweep`, tool=july6-staging-sweep, coverage scanned=11/total=11/complete=true. No started/ended — not documented, not invented.
- The 3 staging_signal claims carry `value.interpretation_status` = superseded
  2026-09-28: the July 5-6 admin deletion sweep is mid-campaign hygiene, NOT a
  pre-run staging modality (PROVENANCE closure, notes/admin-deletions-2026-09-28.md).

## Dedup

`match --text <term> --mode fuzzy` for july6-staging, delete-burst-2026-07-05,
admin_cleanup_burst, no_agent_wiki_writes, forward_dated_page_names,
comparator-may-11, 2026-05-11-july6-staging, null-read-gem-registry,
staging-sweep — all zero matches. In-batch fingerprints unique.

## Batch

Batch 4f13ae9d2e454a75848aacc75d4e3dda: 11 claims + 1 run + 1 source + 13
in_lane edges (top-level lane set on bundle). `verify --blobs` ok.
