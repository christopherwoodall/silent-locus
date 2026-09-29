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
