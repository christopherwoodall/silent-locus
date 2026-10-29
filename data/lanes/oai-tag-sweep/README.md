# oai-tag-sweep lane (Factum copy)

Aggregation of the 2026-10-01 indicator sweep lane into Factum.
BigSexyWarlock69 approved aggregation (no 1:1 ingest of the 96,353 events).

## Contents

- `events.jsonl` — 96,353 annotated sweep events (full rows retained here).
- `timeline.json` — per-hit timeline records + per-minute bursts (>= 8 hits).
- `temporal_overlaps.md` — hit-days inside known windows; >= 2-source days.
- `sweep_summary.json` — per-indicator counts per source + score histogram.
- `sweep_indicators.py` — the original sweep build script (single-collection).
- `aggregate.py` — per-indicator aggregation (counts, exemplars, cross-check).
- `agg.json` — aggregation output consumed by the bundle builder.
- `build_factum_bundle.py` — builds the 20-record Factum bundle.
- `PROVENANCE.md` — sweep provenance + aggregation methodology.
- `SHA256SUMS` — file hashes.
- `INGEST_NOTES.md` — Factum ingest notes.

## Factum records (20)

1 run + 1 source + 15 `intel.behavior` (one per fired indicator, `category` =
indicator name) + 3 OBSERVED claims (coverage, multi-indicator rate,
temporal distribution). All tagged `{"lane": "oai-tag-sweep"}`.

Indicator taxonomy: `docs/taxonomy/indicator-taxonomy.md`.
