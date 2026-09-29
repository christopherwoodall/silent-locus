# PROVENANCE — data/gem-temporal-pivot/

Partial artifacts from the 2026-09-28 temporal-pivot hunt (see
`notes/gem-temporal-pivot-2026-09-28.md`; verdict: clean negative).

- `diffend_temporal_sweep.jsonl` — first 24 rows of the abandoned 3,025-name Diffend
  version-date sweep (checkpointed by gem name; resume by re-running
  `scripts/diffend_temporal_sweep.py`, which skips names already present). Most rows are
  connection-failure records: my.diffend.io closed connections on burst traffic from
  this environment on 2026-09-28.
- `diffend_temporal_sweep.stdout.log` — sweep stdout (progress markers).
- `diffend_targeted_check.jsonl` — targeted 13-name version-date check (July-7 family +
  distinctive May names); killed for the same endpoint reason after 2 failure rows
  (the aggregated `.json` was never written).

All fetches were read-only HTTPS GETs (no auth, no downloads, no submissions).
No credentials, no PII.

## Schema backfill 2026-09-29

Both JSONL files transformed by `temp/backfill_w3.py` onto the shared schema.

- record_kind: `diffend_probe` for both files (live diffend probes /
  negative-sweep observations of gem names).
- fingerprint: sha256 of `"diffend_targeted_check|" + name`
  (targeted_check) or `"diffend_temporal_sweep|" + name` (temporal_sweep).
- @timestamp: sentinel `1970-01-01T00:00:00Z`,
  `labels.timestamp_source = "fallback:no_recoverable_date"` (probe rows
  carry no date fields).
- Field moves: `name` -> `labels.gem.name`; all other fields to labels.
  `versions` (list of objects) and `out_of_window` are JSON-encoded strings
  in labels to satisfy the flat-labels rule (lossless; parse with
  `json.loads`). In `diffend_targeted_check.jsonl` the top-level `status`
  string (an HTTP error message) moved to labels, and a canonical
  `status = "probe-failed"` marker was set (both rows have `ok: false`).
- event.dataset = `gem-temporal-pivot` for both files.

## Canonical layout migration (2026-09-29)

Concatenated 2 event shards (gem-temporal-pivot-diffend-targeted-check.jsonl, gem-temporal-pivot-diffend-temporal-sweep.jsonl) into `events.jsonl` in sorted-filename order (27 records; count verified against inputs). Each record gained `labels.file_origin` = original shard basename; no other fields changed. Source shards removed after verification.

## Stub merge 2026-09-29

`raw/run-logs/diffend_temporal_sweep.stdout.log` moved in from the undated
`data/gem-temporal-pivot/` stub (the file PROVENANCE already listed as the sweep
stdout, left behind by the canonical-layout migration). Contents verified: two
progress-marker lines from the 2026-09-28 Diffend 3,025-name sweep
(`total 3025, done 0, todo 3025`; `0/3025 ... oow_hits=0`). Stub dir removed after
the move; no other stub content existed.
