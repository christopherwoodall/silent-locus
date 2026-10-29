# Provenance — processed RubyGems unpacked corpus

Lane: `processed-gems`.
Legacy dir: `evidence/processed/gems/` (moved to
`data/lanes/processed-gems/raw/` on ingest, 2026-10-11).

## What this dataset is

537 unpacked RubyGems trees (directories), a strict subset of the 618 `.gem`
files in `evidence/raw/gems/` (81 raw gems were never unpacked). Contents:
641 `.rb` payload files, gemspecs, READMEs, 28 nested `.gem` files bundled
inside the trees (e.g. `wandsproxylol-0.0.5.gem`).

## Dedup verdict (2026-10-11)

All 565 unique gem names from `evidence/raw/gems` are already in Factum
(Diffend sweep lanes: 2026-05-11-osv, gem-temporal-pivot, gem83-reconciliation,
gem-negative-lanes). The unpacked trees add no new package entities, so no
1:1 per-gem re-ingest was done — that would duplicate entity coverage.

The novel content is the file bytes: payload sources retained under `raw/`
for forensics. A payload-URL scan of the 641 `.rb` files surfaced only
localhost/test URLs; the campaign's real exfil endpoints are already recorded
on the existing package records.

## Factum ingest (2026-10-11)

- 1 `source` (unpacked corpus).
- 1 `run` (unpack census: 537/618 unpacked, 28 nested gems, file-type census,
  payload URL top-10).
- 1 `claim` (entity coverage: 565/565 names already in Factum; bytes retained).
- No schema changes needed. Bundle: `ingest-processed-gems-20261011`.
