# Provenance — collusion-manifest

Manifest sidecar for the `collusion-wiki` collection.

## Source
- **Publisher:** Nightingale Collective (https://rubyhack.ai/), via the
  collusion.wiki data export at https://collusion.wiki/explorer/download —
  the investigators' mirror of the agent-occupied German wikis (dse on
  prowiki.org; probier and fractal on wikiservice.at).
- **Retrieved:** 2026-09-28 as part of the collusion-wiki lane-22 download
  (all 11 export files SHA-256 verified against the publisher's published
  checksums at ingest time; see `evidence/2026-05-17-collusion-wiki/PROVENANCE.md`).

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
- `evidence/2026-05-17-collusion-wiki/PROVENANCE.md` — sibling collection's provenance
  (same download event).

## Schema backfill 2026-09-29 (normalization sweep, worker W4)

- Built `events.jsonl`: 111 records — 110 `coverage_gap` (one per evidence/remove-2026-09-03-collusion-manifest/raw/coverage-gaps.csv row; new record_kind, see triage note) and 1 `artifact_observation` (evidence/remove-2026-09-03-collusion-manifest/raw/manifest.json itself).
- Fingerprint identity strings: `coverage-gap:<site>|<host>` for rows; `collusion-manifest:db_sha256=<db_sha256>` for the manifest.
- @timestamp: no per-row dates in the CSV -> manifest.generated_at 2026-09-03T03:42:36Z for all; labels.timestamp_source=`manifest.generated_at`.
- `rollup.jsonl`: 7 rows, one per gap category (record_kind `coverage_gap`, event.dataset `2026-09-03-collusion-manifest-rollup`): site/host counts, gaps-remaining counts, saved-response and distinct-text totals. Fingerprint identity: `coverage-gap-rollup:<category>`.
- Regenerated `SHA256SUMS` (events.jsonl + rollup.jsonl + raw/**).

## Date-prefix audit 2026-09-29 (worker W5)

Dir renamed `2026-05-01-collusion-manifest` -> `2026-09-03-collusion-manifest`.
All 118 event records carry @timestamp 2026-09-03 (the export manifest's
`generated_at`); the old 2026-05-01 prefix was the export's revision
write-date *cut* (`revision.write_date >= 2026-05-01`), not an event date.
Per schema/collections.md (prefix = first event), the correct prefix is
2026-09-03. `event.dataset` updated in events.jsonl / rollup.jsonl
(`...-rollup` suffix preserved); SHA256SUMS regenerated.
