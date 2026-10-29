# 2026-09-12-jsonhero-docs-archive

Factum lane for the Wayback archive-recovery census of dead jsonhero.io
shared docs (Phase 3 Batch 5).

## What this lane holds

Six jsonhero.io shared docs returned HTTP 500 on the live site in
2026-09-28. The docs were referenced in June-2026 wiki revisions. A
Wayback CDX census on 2026-09-28 recovered one doc and confirmed five
had zero captures.

- One doc recovered: `swJMw8b6VwDC`. Wayback capture
  2026-09-12T07:50:05Z (HTTP 200). The doc is an older vintage of the SEC
  Regulation Crowdfunding county dataset. Its title shows it was made
  from a 2025-01-13 Wayback capture of `https://www.sec.gov/files/county.json`.
- Five docs not archived: `S5R1RRn64PLh`, `aB94pTzmWvtl`, `qDhAiEHyjXYi`,
  `wANOlosoW5YN`, `1vaGknk7ajC4`. These verdicts are Wayback-only
  (archive.today was unreachable from the collection network). They are
  graded medium confidence, not absence.

## Factum records

- 1 `web.capture` observation (the recovered doc).
- 5 `reachability.check` observations (the not-archived verdicts).
- 1 `dataset.snapshot` observation (the recovery census: 6 docs,
  1 recovered, 5 not archived).
- 7 `source` records (one per observation).
- Batch: `data/records/3aa6166778c14ca3a16b31706164a846/`.
- Lane tag: `{"lane": "2026-09-12-jsonhero-docs-archive"}`.
- Lane record: `lane_6a54cef9f2494cdaa6e8199de887b319`.

## Source material

Legacy directory (renamed after ingest):
`evidence/remove-2026-09-12-jsonhero-docs-archive/`. It holds `events.jsonl`
(6 rows), `rollup.jsonl` (recovery census), `PROVENANCE.md` (copied here as
`legacy-PROVENANCE.md`), `SHA256SUMS`, and `raw/` (the raw Wayback capture
HTML, the extracted payload JSON, and the legacy ES loader).
