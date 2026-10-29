# REBUILD-NOTES — university-shorteners

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
- `events.jsonl`: 1,591 records fixed — `file` prefixes: `data/2026-09-28-university-shorteners/` -> `evidence/2026-09-28-university-shorteners/` (1,546), `data/2026-09-28-university-shorteners-batch2/` -> `evidence/...-batch2/` (5), `data/2026-09-28-university-shorteners-batch3/` -> `evidence/...-batch3/` (16), `data/2026-05-12-university-shorteners-events/` -> `evidence/remove-2026-05-12-university-shorteners-events/` (24). All targets verified on disk.
- `PROVENANCE.md`: 19 refs fixed (same four prefix rules; bare `raw/wayback/` refs resolved to the May-12 collection or the 2026-09-28 collection per section context — lines 115/141/166/198; line 69 keeps its `{a,b}` brace expansion, both expansions verified).
- Ambiguities: line 58 (`pre-migration data/university-shorteners[-batchN]/...`) and line 114 (docstring staging path) are explicitly historical — left untouched.
