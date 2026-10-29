# Ingest notes — swarmtraces-hf-dataset

Ingest date: 2026-10-10. Worker: agent:lane-ingest:swarmtraces-hf-dataset.

## What was ingested

Giant-lane aggregation of `evidence/raw/redacted.jsonl.gz` (189,579
records). No 1:1 ingest.

- 1 `source` record — dataset locator
  `https://swarmtraces.org/data/final/redacted.jsonl.gz` (+ sha256,
  retrieval date in tags).
- 1 `run` record (ref run, run_kind extraction) — the aggregation pass.
- 1 `dataset.snapshot` observation — dataset_uri, revision
  (sha256:...), coverage complete, row_count 189579.
- 37 `infra.ioc` observations — unique literal IOC values:
  6 domains, 20 URL prefixes (HF API, docker registry, Artifactory
  board, Slack), 8 tailscale stable build URLs, 10 zz-marker Artifactory
  full URLs, 1 IP (169.254.169.254). Record counts in tags (records
  containing the complete literal value). All tag values are strings.
- 5 `claim` records (basis OBSERVED) — artifactory board volume, flat
  chain topology (max depth 1), redaction-slot token cardinality, target
  surface summary, IMDSv2 token-request code. Subjects/cites are bundle
  @refs (bare strings); no claim cites a source record.

## Mapping rules

Use plain words. Short sentences.

- `term` is the exact observed value, never an internal ID. URLs that hit
  a redaction boundary (`[`, `REDACTED`, `CREDENTIAL`, `SERVICE`) are
  discarded — counted values are complete observed strings only.
- Observation `type` lives inside `body`, not at record level.
- `tags` values are all strings (record counts stringified).
- Every record carries `{"lane": "swarmtraces-hf-dataset"}`.
- Claims cite the run and the relevant IOC observations. The source
  record is linked via observation `body.source`, never cited.

## Dedup

- File-level grep over all committed `data/records/*/records.jsonl` for
  every candidate term + `match --text --mode fuzzy` spot queries.
- Skipped: the 5 verification-claim topics (record counts, field stats,
  redaction-marker occurrences, parentage topology, cite-token semantics)
  already in lane `2026-09-27-swarmtraces-verification`; redaction-slot
  placeholders as IOC terms (not concrete values); fragment IOCs that
  already exist as different values (noted as related in tags).
- Within-batch dedup by exact term.

## Checks done

- `validate_bundle.py`: independent re-derivation from bytes — all
  checks passed (counts, chain stats, slot cardinalities, snapshot,
  verbatim spot-checks, schema-shape rules).
- `export` + `verify --blobs` before commit.

## Builder

`build_bundle.py` (extractor) + `validate_bundle.py` (independent
validator), both kept in this lane dir. Bundle: `bundle.json`
(Factum bundle v2). Stats: `extraction-stats.json`.
