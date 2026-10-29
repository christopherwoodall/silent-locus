# REBUILD-NOTES — xss-ssti-census

Source-data fix pass, 2026-10-09 (Counsel 2 audit). These notes record what was fixed in the SOURCE files (events.jsonl, PROVENANCE.md) before the Factum rebuild, which process decisions the ingest worker must apply, and what was left ambiguous.

## Process decisions (Counsel 2 audit — apply at ingest)

1. **tantive-space**: use FULL verbatim bodies from `raw/` (not excerpts). Applies to tantive-space only.
2. **commonlog-scan**: full verbatim bodies from `raw/`. Applies to commonlog-scan only.
3. **xss-ssti-census**: `term` takes the value from `markers_present` / `text` (the actual marker values, not the internal R-IDs such as `R0002137`); `category` takes the value from `family`. Applies to xss-ssti-census only.
4. **Lane tags**: derive the `lane` tag from the lane directory name automatically during ingest. Do not hand-tag records.
5. **Epoch timestamps**: where no recoverable date exists, accept `fallback:no_recoverable_date`. Do not invent dates.
6. **july7-wave**: dedup intra-lane duplicate rows (e.g. `test_gem_kangaroo`) at ingest time, on gem name + version.

## Fix policy used in this pass (2026-10-09)

- `events.jsonl`: mechanical prefix corrections only. Every new path was verified to exist on disk before the edit.
- `PROVENANCE.md`: fixed only paths presented as *current* locations whose corrected target verifies on disk. Historical move notes (`A -> B` relocations, `pre-migration`, `previous`, `relocated from`, staging paths, `raw/-missing` markers) were left untouched so the provenance record stays faithful.
- `SHA256SUMS`: refreshed for `events.jsonl` / `PROVENANCE.md` where an entry existed.
- Fingerprints: recomputed only where the lane's documented fingerprint rule covers a changed field. Otherwise left as-is.
- Nothing was committed or pushed.

## Lane-specific fixes (2026-10-09)
- `events.jsonl`: 117 records fixed — `labels.source_ref`: `data/raw/redacted.jsonl.gz` -> `evidence/raw/redacted.jsonl.gz` (100 records; the `id=R...` suffix preserved), `data/gemstuffer-jfrog-2026-09-27.csv` -> `evidence/2025-03-04-rubygems-goimport-campaign/raw/gemstuffer-jfrog-2026-09-27.csv` (17 records; the `Package=... Versions=...` suffix preserved). 5 records with `source_ref` starting `hosted` are not file paths — untouched.
- Fingerprints untouched: the documented rule (sha256 of `payload_id`) does not cover `source_ref`; the top-level `sha256` field covers `labels.text` (verified), also untouched by this fix.
- `PROVENANCE.md`: 15 refs fixed (collection dir, gemstuffer CSV, `data/raw/redacted.jsonl.gz` x3, aggregates events.jsonl, paste corpora dirs, gem IOC corpus files).
- Decision 3 applies here: at ingest, `term` <- `markers_present` / `text` (the actual marker values, e.g. `packages.hub.ace-research.openai.org`), NOT the internal `payload_id` R-IDs; `category` <- `family`.
- Decision 5 applies: records carry `1970-01-01T00:00:00Z` with `fallback:no_recoverable_date`. Accept as-is.
- Ambiguities: none.
