# REBUILD-NOTES — commonlog-scan

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
- `events.jsonl`: no changes (no stale paths).
- `PROVENANCE.md`: 2 refs fixed — `raw/stream.sse`, `raw/messages.json` -> `evidence/remove-2026-08-25-commonlog-scan/raw/...`.
- Decision 2 applies here: at ingest, pull FULL verbatim message bodies from `evidence/remove-2026-08-25-commonlog-scan/raw/messages.json` (note: `.json`, not `.jsonl`; raw capture is `raw/stream.sse`). Do not use excerpts.
- Ambiguity: PROVENANCE.md line 24 describes a historical builder move into `data/2026-08-25-commonlog-scan/build_dataset.py`. The mechanical correction does not verify on disk; the script now lives at `data/lanes/commonlog-scan/build_dataset.py`. Left untouched; ingest worker to resolve.
