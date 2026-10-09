# REBUILD-NOTES — reverse-tunnels

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
- `events.jsonl`: 107 records fixed — `file` `data/2026-06-17-reverse-tunnels/raw/<name>` -> `evidence/remove-2026-06-17-reverse-tunnels/raw/<name>` (all 107 targets verified).
- `PROVENANCE.md`: 5 refs fixed (collusion-wiki revisions.jsonl, thecolony-ai wiki_incident_page.html, `raw/manifest.sha256` x2, `raw/run-logs/NOTE-htmx_search.pyc.md`).
- Ambiguities:
  - Line 143 says `es_ingest_reverse_tunnels.py` is co-located at `data/2026-06-17-reverse-tunnels/`; the mechanical correction does not verify. The script actually lives at `data/lanes/reverse-tunnels/es_ingest_reverse_tunnels.py`. Left untouched.
  - Lines 113/196 cite `raw/run-logs/htmx_search.cpython-312.pyc` as a re-added curated artifact, but the file is absent on disk (only `NOTE-htmx_search.pyc.md` and the progress log exist in `raw/run-logs/`). Doc/reality mismatch; left untouched for the ingest worker.
  - Lines 129/130/204/206 reference the pre-rename `data/2016-05-06-reverse-tunnels/` dir inside historical relocation notes. Left untouched (historical).
