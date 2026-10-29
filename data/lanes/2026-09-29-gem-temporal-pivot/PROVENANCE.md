# PROVENANCE — data/2026-09-29-gem-temporal-pivot/

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

`raw/run-logs/diffend_temporal_sweep.stdout.log` moved in from the former undated stub (the file PROVENANCE already listed as the sweep
stdout, left behind by the canonical-layout migration). Contents verified: two
progress-marker lines from the 2026-09-28 Diffend 3,025-name sweep
(`total 3025, done 0, todo 3025`; `0/3025 ... oow_hits=0`). Stub dir removed after
the move; no other stub content existed.

## 2026-09-29 — resume checkpoint (interrupted)
Diffend temporal sweep resumed via `scripts/diffend_temporal_sweep_resume.py`: 1,548/3,000 items probed (events 27 → 1,575 rows, `record_kind=diffend_probe`), progress logged in `raw/run-logs/diffend_temporal_sweep_resume.stdout.log` (last: 1500/3000 at 10:54:54Z). Worker interrupted by a runtime restart drain before committing; no data loss — events and log intact. Resume from item ~1,573 using the same script; it checkpoints in the log.

## 2026-09-29 — Diffend temporal sweep COMPLETE (3,025/3,025 names)

Final leg ran 10:58Z–12:03Z via `scripts/diffend_temporal_sweep_resume.py` (re-run
from the 9a6bc06 checkpoint; checkpoint = events.jsonl itself, dedupe by
gem.name). 1,452 items probed, 0 fetch failures (`DONE oow_hits=2 fetch_fail=0`).
Progress in raw/run-logs/diffend_temporal_sweep_resume.stdout.log; five batch
commits (10729d6, 5dc81fc, a13d2c3, 608f9e4, c243a36).

Final tally (ground truth from events.jsonl):

- 3,027 rows, 3,025 distinct gem names (`record_kind=diffend_probe`); the 2
  extra rows are historical duplicates that predate this leg (names present in
  both phase-1 and the first resume leg) — left untouched.
- In Diffend with version dates captured (HTTP 200): 2,251
- Not in Diffend (302 → gems index): 756
- Fetch negatives, recorded honestly, no refetch: 16 "Remote end closed
  connection without response" (2026-09-28 burst run), 2 curl "000" connect
  failures (slnstep8275, slnstep8300), 2 phase-1 targeted-check probe-failed rows.
- Out-of-window version dates (outside 2026-05-05–2026-07-07): 3 gems —
  lambethcalcqzewgt, test_gem_kangaroo, wanproxyq.

Caveat: `labels.out_of_window` / `labels.versions` are JSON-encoded strings on
resume-leg rows but native lists on the 27 phase-1 rows (backfill_w3.py).
validate_schema.py passes (it does not enforce the flat-labels rule on these);
parse defensively with a str-or-list check.

All fetches were read-only HTTPS GETs against my.diffend.io (stock browser UA,
~1.5s pace, no auth, no submissions, no invented IDs).

Build script relocated per repo convention (single-collection build scripts
live in the event dir): scripts/diffend_temporal_sweep_resume.py → ./ (renamed to build_diffend_temporal_sweep.py 2026-09-29 to match the `^(es_ingest|build)_.*\.py` root-layout convention)

## 2026-10-10 — SHA256SUMS staleness note (ingest agent)

`sha256sum -c SHA256SUMS` reports FAILED for
`raw/run-logs/diffend_temporal_sweep.stdout.log` and
`raw/run-logs/diffend_temporal_sweep_resume.stdout.log`.
Root cause: SHA256SUMS was captured before the resumed final leg finished
(2026-09-29 10:58Z–12:03Z); the logs legitimately grew as the sweep
completed. Current log content matches the documented final state
(`2026-09-29T12:03:04+00:00 DONE oow_hits=2 fetch_fail=0`; earlier leg logged
oow_hits=1, total 3 out-of-window gems, matching the events.jsonl tally).
`events.jsonl`, the build script, and this file verify OK. Checksums left as
recorded (historical); do not "fix" them by re-hashing without noting the
date gap.
