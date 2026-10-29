# PROVENANCE — gomod-hunt

Clean-negative Go module index lane (2026-09-27): swept 32,766 Go module
index pairs for campaign patterns (`zz`, probe-name grammars, go-import
laundering markers). Result: clean negative at pattern level — campaign
footprint remains RubyGems-only.

- Raw scripts + match files moved into this directory from
  `~/workspace/tmp-gomod/` on 2026-09-28 (night watch) so the material
  lives in the repo, not /tmp-adjacent scratch.
- Report: `notes/gem-hunt-gomodules-2026-09-27.md`
- SHA-256 manifest: `manifest.sha256`

## Schema backfill 2026-09-29

All eight `matches_N.jsonl` files transformed by `temp/backfill_w3.py`.

- record_kind: `gomod_proxy_match` (new kind; Go module proxy index entries
  matching the proxy-themed hunt).
- fingerprint: sha256 of `Path + "|" + Version`. NOTE: the source files
  contain exact duplicate rows (identical Path|Version|Timestamp, e.g. 190
  dup rows in matches_1); identical records deterministically share a
  fingerprint. Duplicates were preserved, not dropped (lossless rule).
- @timestamp: `Timestamp` (Go module index time, already UTC Z);
  `labels.timestamp_source = "labels:gomod.timestamp"`.
- Field renames into labels (label keys must be lowercase):
  `Path` -> `gomod.path`, `Version` -> `gomod.version`,
  `Timestamp` -> `gomod.timestamp`.
- event.dataset = `gomod-hunt`.

## Canonical layout migration (2026-09-29)

Concatenated 8 event shards (gomod-hunt-matches-1.jsonl, gomod-hunt-matches-2.jsonl, gomod-hunt-matches-3.jsonl, gomod-hunt-matches-4.jsonl, gomod-hunt-matches-5.jsonl, gomod-hunt-matches-6.jsonl, gomod-hunt-matches-7.jsonl, gomod-hunt-matches-8.jsonl) into `events.jsonl` in sorted-filename order (35014 records; count verified against inputs). Each record gained `labels.file_origin` = original shard basename; no other fields changed. Source shards removed after verification.

## Factum aggregation (2026-10-10)

Giant-lane aggregation into Factum. No 1:1 ingest of the 35,014 rows
(BigSexyWarlock69 approved aggregation).

- Input: `events.jsonl` here (sha256
  f6ff86f479deac07eb1441b0b80a26c1a6444b95f3e3733d8008eba6b5ec06f6),
  moved from `evidence/2026-05-05-gomod-hunt/` to `data/lanes/gomod-hunt/`
  along with `PROVENANCE.md`, `SHA256SUMS`, and `raw/`.
- Method: one `infra.ioc` observation per unique `labels."gomod.path"`
  (2,397 paths; case preserved). Distinct versions live in tags
  (`tags.versions`, `tags.version_count`); no per-version records.
  Each record carries `tags.match_count` (source rows for the path),
  `tags.pseudo_version_count`, `tags.has_pseudo_version`, and
  `{"lane":"gomod-hunt"}`.
- Also submitted: 1 source record (lane locator) and 1 run record
  documenting this aggregation, plus 7 OBSERVED summary claims:
  event volume (35,014), uniqueness (2,397 paths / 32,766 pairs),
  temporal spread (2026-05-05 to 2026-06-30), pseudo-version pattern
  (15,436 matches, 44.1%), top-5 path concentration (14.3%),
  third-party GitHub-proxying hosts (4,565 matches, 13.0%), and
  source duplicate rows (2,248 exact path|version|timestamp dupes
  preserved upstream; dedupe is path-level only).
- Builder: `build_gomod_bundle.py` (this directory) emits the bundle and
  runs an independent re-derivation validator over `events.jsonl`
  (asserts 35,014 / 2,397 / 32,766 / timestamp bounds / pseudo stats).
  Output bundle kept as `bundle.json`.
- Pre-ingest dedup: 30 sampled terms (5 most frequent + 25 random) matched
  against all exported Factum batches by exact substring — zero hits.
- Legacy directory renamed to `evidence/remove-2026-05-05-gomod-hunt/`
  (ingested, safe for later removal).
