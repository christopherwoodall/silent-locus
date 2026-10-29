# Diffend temporal version-date sweep of 3,025 RubyGems names

3,027 probe rows from the 2026-09-28/29 Diffend sweep of 3,025 RubyGems gem
names. Each name was queried against my.diffend.io to capture version dates.

Result: 2,251 names in Diffend with version dates (HTTP 200), 756 not in
Diffend (302 to gems index), 18 connection failures, 2 targeted-check probe
failures. 3 gems have out-of-window version dates (outside
2026-05-05–2026-07-07): lambethcalcqzewgt, test_gem_kangaroo, wanproxyq.

## Factum ingest

Ingested 2026-10-10 as 3,027 `infra.package` observations (ecosystem:
rubygems) in 7 batches. Lane tag: `2026-09-29-gem-temporal-pivot`.
Factum lane id: `lane_10c1ccbe64a44ba48c0b1782e52ad8c6`.

- `events.jsonl` — source rows (3,027 lines, verified against SHA256SUMS).
- `raw/run-logs/` — sweep progress logs.
- `PROVENANCE.md` — full acquisition history, including the SHA256SUMS
  staleness note for the two run logs.
- `INGEST_NOTES.md` — ingest mapping decisions.

## Terms

- **Diffend**: gem security scanner at my.diffend.io.
- **temporal sweep**: version-date capture across a gem name list.
- **out-of-window**: version date outside the target window
  2026-05-05–2026-07-07.
