# schemas/event-dirs.md

Hunt event directories under `data/`, named `<YYYY-MM-DD>-<slug>/`.
Name starts with the EVENT date, not the analysis date.

## Required files

- `README.md` — what the event is, in ASD-STE100 (short sentences,
  simple words, terms defined on first use).
- `PROVENANCE.md` — collection record: what, source, retrieval
  time/method, what changed between pulls, what failed.
- `SHA256SUMS` — hashes of the captured files.
- `raw/` — unedited captured evidence.
- `events.jsonl` — observations, one JSON object per line in the common
  envelope: `@timestamp`, `event{}`, `record_kind`, `fingerprint`
  (SHA-256 hex of the dataset's documented identity string per
  PROVENANCE.md), `labels{}`. Findings go in lane docs, not the JSONL.

## Optional lane files

- `METHODOLOGY.md`, `LESSONS.md` — how the lane was worked, what was
  learned.
- `FINDINGS.md`, `*-REPORT.md`, `writeup-*.md` — analysis with graded
  claims (OBSERVED / INFERENCE / UPSTREAM).
- `PERSONA_MANIFEST.md`, `personas/` — multi-persona review sections.
- Lane scripts live in the event dir; multi-event parsers go in
  top-level `scripts/`.
- Sub-lanes get subdirs (`full-sweep/`, `infra-sweep/`, `live-monitor/`,
  `harness-logs/`, `cachedview/`, …).

## Example

`data/2026-09-28-chinese-amap-fleet/`: README, PROVENANCE,
SHA256SUMS, events.jsonl, METHODOLOGY, LESSONS, SSLIP-REPORT,
PERSONA_MANIFEST, personas/, raw/, plus ~20 sub-lane dirs.
