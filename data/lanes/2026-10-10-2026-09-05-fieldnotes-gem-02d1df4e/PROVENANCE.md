# Provenance — 2026-09-05-fieldnotes-gem ingest

## Original acquisition (2026-09-28, workstream D)

Read-only GETs of 4 URLs, 2026-09-28 03:22–03:25 UTC. The gem artifact
itself was never downloaded or installed. Full detail:
`data/lanes/2026-09-05-fieldnotes-gem/PROVENANCE.md`.

## Factum ingest (2026-10-10, Phase 3 Batch 5)

- Pre-ingest dedup: `match --text "fieldnotes" --mode fuzzy` →
  not_found; `match --text "public-board" --mode fuzzy` → not_found;
  `match --url "https://my.diffend.io/gems/fieldnotes"` → not_found.
  No duplicates in the corpus.
- Submitted as one bundle (`lane-ingest/2026-09-05-fieldnotes-gem/v1`):
  7 `files[]` (git storage) → 7 artifact records; 1 source, 2 runs,
  5 observations (1 `infra.package`, 4 `web.capture`), 4 claims.
- Factum auto-created 19 `in_lane` edges to
  `lane_8f87fa1067f742628a97517502d1df4e`.
- Batch `2710b44489a1454c97547e90cb16e0e6`:
  `data/records/2710b44489a1454c97547e90cb16e0e6/`.
- Blob bytes verified sha256-identical to raw files before the legacy
  files were removed.
- Legacy directory renamed to
  `evidence/remove-2026-09-05-fieldnotes-gem/` after its contents were
  moved to `data/lanes/2026-09-05-fieldnotes-gem/` (docs) and
  `data/blobs/sha256/` (capture bytes).
