# Corpus schema — silent-locus

Machine-readable: [`record.schema.json`](record.schema.json) (JSON Schema draft
2020-12). Machine validation: `scripts/validate_schema.py` (stdlib only, no
dependencies). Run it before commit or ingest; it exits non-zero on any
violation.

## The one rule

Every JSONL record under `data/` is an **explicit event**. We do not
consolidate events. Rollups and joins live in support indexes, never in the
corpus files.

## Required fields

| Field | Meaning |
|---|---|
| `@timestamp` | Event time. UTC ISO-8601 with `Z`. Must parse. See fallback rule below. |
| `event.dataset` | Dataset slug, e.g. `collusion-wiki`. Doubles as the Elastic index/layer name. |
| `event.created` | When the pipeline created this record (UTC, `Z`). Not the event time. |
| `record_kind` | Snake-case record class (registry below). |
| `fingerprint` | SHA-256 hex of the dataset's documented identity string. |
| `labels` | All dataset-specific fields live here. Flat object, never nested. |

## Optional fields

`source_url`, `description`, `confidence` (`confirmed|high|medium|low` by
convention), `tags` (array of strings), `observer` (`{product, type, vendor}`),
`retrieved_at`, `retrieved_via`, `sha256`, `size_bytes`, `note`, `status`,
`matched_string`. No other top-level keys are allowed.

## Timestamp rules

- All timestamps are UTC with `Z` suffix. Parseable or the record is invalid.
- `@timestamp` is the **event** time, not the pipeline time.
- When no event time is recoverable, use the documented sentinel
  `1970-01-01T00:00:00Z` **and** set
  `labels.timestamp_source = "fallback:no_recoverable_date"`. A missing event
  time must never silently become "now" (pipeline time); the sentinel is fixed,
  documented, and excludable from time-series analysis.
- When the timestamp is derived from a labels field, record the provenance:
  `labels.timestamp_source = "labels:<dotted.key>"` (e.g.
  `labels:published.at`).
- Date-like evidence that is *not* the event time stays in `labels`
  (e.g. `live_checked_at` prose, capture times) and is never promoted to
  `@timestamp` without proof of what it describes.

## Labels rules

- Dataset-specific fields go under `labels`, never at top level.
- Flat: values are strings, numbers, booleans, null, or arrays of scalars.
  No nested objects (ECS `labels` rule).
- Keys match `^[a-z0-9_.]+$`; dotted keys (`section.field`) namespace
  sub-structure, e.g. `published.at`, `gem.wave`.

## Fingerprint rules

- Always SHA-256 hex (64 chars). No MD5-era values.
- The identity string is dataset-specific and **must be documented in that
  dataset's PROVENANCE.md**, e.g. `venue + "|" + source_url`.
- Deterministic: same identity string always yields the same fingerprint.

## record_kind registry

Snake-case, one per record class. Observed (2026-09-28):

`admin_cleanup_burst`, `corpus_grep_negative`, `delete_event`,
`diffend_harvest`, `download`, `extraction`, `file_drop_probe`, `graph_node`,
`marker_ambiguous`, `pastebin_probe`, `relay_paste`, `surface_negative`,
`sweep_negative`, `timeline_anchor`, `transfer_test_paste`, `venue_finding`,
`venue_probe`, `web_search_negative`, `webhook_deaddrop`,
`webhook_deaddrop_candidate`, `wiki_event`

New kinds are added by the dataset builder and recorded here.

## Layer naming

`event.dataset` is the layer name: one dataset, one Elastic index, one
`data/<slug>/` directory. Index names equal dataset slugs.

## Provenance

Every dataset directory carries `PROVENANCE.md` (source, method, identity
string for fingerprints, caveats) and `SHA256SUMS` (checksums of every file
in the directory, verified with `sha256sum -c`).

## Conformance status

The ten datasets rewritten by `scripts/backfill_schema_2026_09_28.py`
(2026-09-28) conform. Remaining corpus files predate the schema and are being
brought into conformance; `scripts/validate_schema.py` measures drift.
