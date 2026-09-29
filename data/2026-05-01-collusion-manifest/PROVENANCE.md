# Provenance — collusion-manifest

Manifest sidecar for the `collusion-wiki` collection.

## Source
- **Publisher:** Nightingale Collective (https://rubyhack.ai/), via the
  collusion.wiki data export at https://collusion.wiki/explorer/download —
  the investigators' mirror of the agent-occupied German wikis (dse on
  prowiki.org; probier and fractal on wikiservice.at).
- **Retrieved:** 2026-09-28 as part of the collusion-wiki lane-22 download
  (all 11 export files SHA-256 verified against the publisher's published
  checksums at ingest time; see `data/collusion-wiki/PROVENANCE.md`).

## Files
- `manifest.json` — the export's own manifest as published: generation
  timestamp (`2026-09-03T03:42:36Z`), source-database SHA-256, the revision
  write-date cut (`revision.write_date >= 2026-05-01`), record counts
  (14,591 revisions / 4,579 pages / 3,103 labels) and per-wiki breakdowns
  (dse 13,403 revs / 3,908 pages; probier 1,013 / 601; fractal 169 / 68).
- `coverage-gaps.csv` — the publisher's coverage-gaps listing from the same
  export (known gaps in the investigator corpus).

## Why a separate collection
These two files describe the export itself (selection basis, cuts, counts,
known gaps) rather than carrying agent content, so they are registered as a
`support`-class sidecar (`index: null` — nothing loads them to ES) alongside
the canonical `collusion-wiki` data.

## Note sources
- `notes/gem-hunt-collusion-wiki-2026-09-27.md` — lane 22 sweep report:
  export file inventory, checksum verification, per-wiki counts, revision
  cut, IP/username redaction policy.
- `notes/collusion-wiki-schema-2026-09-27.md` — schema/structure of the
  collusion.wiki export.
- `data/collusion-wiki/PROVENANCE.md` — sibling collection's provenance
  (same download event).
