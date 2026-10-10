# Ingest notes — oai-tag-sweep (aggregation)

## Record type

`intel.behavior` (urn:factum:intel:behavior:1), one observation per fired
indicator (15 of 18 defined; `webhook_deaddrop`, `github_remote_cache_zz`,
`disposable_email` fired zero times and have no records).
`category` is the indicator name (e.g. `oai_prefix`).
`description` carries the pattern definition, per-source prevalence,
first/last seen dates, the byte-verified marker verdicts from the lane
PROVENANCE.md, and 2-3 verbatim exemplar evidence snippets.
`provenance` = `2026-10-01-oai-tag-sweep`.

Per the task brief, `infra.ioc` is used only for concrete IOC values, not
indicator names, so no `infra.ioc` records were created here.

## Timestamps

Sweep rows carry real event times, but the submitted records are aggregates,
so per-row times are not recoverable into the aggregate shape.
`observed_at` = 2026-10-01 (the sweep run date per `sweep_summary.json`),
`time_basis` = `legacy_documented`. Per-indicator first-seen dates from the
event bytes are in `data.first_observed`. Severity is marker-presence
severity for a research sweep (minimal/low), not an impact assessment.

## Claims

Three OBSERVED claims on the run record: `sweep_coverage` (96,353 annotated
events from 138,696 frozen records + 38,160 Transluce rows), 
`multi_indicator_rate` (25,699 events with 2+ indicators, 26.7%; 58
overlap days), `temporal_distribution` (span 2025-03-04..2026-09-27; 1,665
burst minutes >= 8 hits; largest 2026-06-18T20:10Z with 665 collusion-wiki
hits). Claims cite the run record.

## Dedup

Pre-ingest check 2026-10-10: no `intel.behavior` taxonomy for these
indicators existed (4 unrelated categories only). `oai_prefix`,
`epoch_nonce`, `markdown_new` exist as `infra.ioc` marker terms in lane
`2026-09-05-termina-digital` (different record type, different lane);
annotated via `tags.also_observed_in_lane`, no duplicates submitted.
Disk scan covered all exported `data/records/*/records.jsonl` and
`data/.local/pending`. Live `match` was unusable (lock contention, stale
index, then a sibling's staged symlink tripping the SYMLINK guard).

## Overlap

The termina-digital lane holds per-sighting `infra.ioc` rows for three of
the same marker names. Those are distinct sightings in a different lane, so
both stand; the overlap is annotated in tags.

## Edges

No edges submitted during ingest. No `in_lane` edges exist.

## Batches

One bundle, idempotency key `oai-tag-sweep-aggregate-v1` (20 records).

## Validator

`data/lanes/oai-tag-sweep/aggregate.py` re-derives expectations from
`events.jsonl` independently of the sweep script: 1:1 row accounting
(96,353), per-indicator per-source counts cross-checked against
`sweep_summary.json`, 2+ indicator rate (25,699). All assertions pass.
Bundle payloads validated against the installed pack schemas; bundle-local
`@ref`s resolve.
