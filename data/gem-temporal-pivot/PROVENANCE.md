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
