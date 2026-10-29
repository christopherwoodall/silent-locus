# REBUILD-NOTES — paste-ubuntu-cn

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
- `events.jsonl`: 1 record fixed (3 path refs) — `labels["sweep.external_ref_paths"][0]` and `labels["sweep.scopes"][0..1]`: `data/` -> `evidence/` (note: labels use flat dotted keys, not nested objects).
- `PROVENANCE.md`: 3 refs fixed (termina-digital wayback db, `raw/sample_decode_verification.txt`, chinese-amap-fleet XZ_KNOWLEDGE.md — all `data/` -> `evidence/`).
- Ambiguity (important): `evidence/2026-10-03-openai-agent-traces/events.jsonl` is a DANGLING symlink — target `../../openai-agent-traces/data/traces.jsonl` is absent in this checkout. The mechanical `data/` -> `evidence/` prefix was applied (the symlink path is the repo's canonical reference), but the bytes are not reachable through it here. Real data exists at `evidence/2026-10-03-openai-agent-traces/raw/traces.jsonl`. Ingest worker must resolve before following this ref.
