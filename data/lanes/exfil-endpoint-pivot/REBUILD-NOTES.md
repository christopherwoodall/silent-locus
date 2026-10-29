# REBUILD-NOTES — exfil-endpoint-pivot

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
- `events.jsonl`: 2 records fixed — `labels.local_saved_copy` `data/separate-eval-test/sources/jfrog-gemstuffer-post.html` -> `evidence/2026-09-29-separate-eval-test/raw/sources/jfrog-gemstuffer-post.html` (target verified).
- `PROVENANCE.md`: 5 refs fixed (separate-eval-test HTML, paste corpora dirs, aggregates events.jsonl — all `data/` -> `evidence/`).
- Ambiguity: PROVENANCE.md line 38 cites sibling `data/2026-07-07-xss-ssti-census/events.jsonl` (122 payloads). The mechanical correction does not verify (`evidence/remove-2026-07-07-xss-ssti-census/` is empty); the file actually lives at `data/lanes/xss-ssti-census/events.jsonl` (122 records match). Left untouched; ingest worker to resolve.
