# swarmtraces-hf-dataset lane

Giant-lane aggregation of the SwarmTraces July-2026 "OpenAI agents hacked
Hugging Face" redacted dataset (`evidence/raw/redacted.jsonl.gz`, 189,579
records). No 1:1 ingest.

## Contents

- `bundle.json` — Factum bundle v2: 1 source, 1 run, 1 dataset.snapshot,
  37 infra.ioc observations, 5 OBSERVED claims (45 records).
- `build_bundle.py` — extractor (single streaming pass).
- `validate_bundle.py` — independent validator (re-derivation from bytes).
- `extraction-stats.json` — measured numbers.
- `PROVENANCE.md`, `INGEST_NOTES.md` — method and dedup decisions.

## Related lanes

- `2026-09-27-swarmtraces-verification` — 5 structural claims on the same
  corpus (record counts, field stats, marker occurrences, parentage,
  cite tokens). This lane adds only new measures and edges to those.
