# Ingest notes — 2026-09-27-swarmtraces-verification

Ingest date: 2026-10-09 (UTC 2026-10-10). Worker: agent:lane-ingest-2026-09-27-swarmtraces-verification.
Factum batch: 4b7e2c8b27604e09b0aff3ad2b76492a (exported as data/records/2710b44489a1454c97547e90cb16e0e6).

## What was ingested

5 legacy `finding` records from evidence/2026-09-27-swarmtraces-verification/events.jsonl
(now data/lanes/2026-09-27-swarmtraces-verification/). Submitted as:

- 1 `source` record (the legacy events.jsonl).
- 1 `run` record (ref audit-run, run_kind corpus_audit): the 2026-09-27
  measured audit pass by notes-farm-2026-09-29 over swarmtraces
  redacted.jsonl.gz, 189,579 rows scanned, coverage complete.
- 1 `artifact` record (storage git): raw/verification-2026-09-27.md, the
  audit note. Bytes in data/blobs.
- 5 `claim` records (basis OBSERVED), one per finding: corpus_record_counts,
  record_field_stats, redaction_marker_counts, parentage_topology,
  cite_token_semantics. Each cites the run and the artifact.

## Mapping rules

Use plain words. Short sentences.

- Each legacy finding becomes one claim. The `description` field is kept
  byte-identical in `body.note`. The measurement numbers move into
  `body.value` as typed integers, taken from the `labels` map, not from
  memory. Key names keep the legacy label names with dots changed to
  underscores where needed (e.g. redacted.destination is kept verbatim as
  a JSON key).
- Legacy metadata moves into tags: `legacy_fingerprint` (the finding's own
  fingerprint), `legacy_record_kind: finding`, `confidence: confirmed`
  (verbatim from source), `timestamp_source: note:publication_date`,
  `observer: notes-farm-2026-09-29`. Lane tag on every record.
- Grade: all five are OBSERVED. The source note says every figure was
  re-measured from the corpus bytes. No interpretation was ingested.
- No edges were created. Edge building is a separate pass.

## Checks done

- Dedup: 5 distinctive key terms (R0189579, 44799675,
  "swarmtraces record counts", "redacted.destination",
  "parent_id null on all payloads") returned not_found against the corpus.
  The aggregate lanes gem83-reconciliation and overlap-analysis analyze
  cross-corpus overlap, not this corpus's structure — no overlap.
- Post-submit check: all 5 claims verified — notes byte-identical to the
  legacy descriptions, value integers match the legacy labels,
  fingerprints resolve to the 5 legacy events, subject and cites are
  resolved record IDs (run_37c9cc60d7eb4bbb81d92a4b15f770d2,
  artifact_6b7ac251e28d4a9ca56130a515947034), lane tag on every record,
  no reserved tag keys.
- `export` and `verify --blobs` passed. 8 new records (883 total).

## Builder

Factum `add --input` on a hand-built JSON bundle (no builder script kept).

## Gotchas hit and fixed

- Claim subject/cites may only reference kind observation, sighting,
  artifact, claim, or run. The first bundle used the `source` record as
  subject and was rejected with REFERENCE_TYPE. Fix: subject = the `run`
  record, cites = run + artifact.
- `run.started` must be an ISO date-time string
  ("2026-09-27T00:00:00Z"), not {"date": "2026-09-27"}. Validation
  rejected the object form.
