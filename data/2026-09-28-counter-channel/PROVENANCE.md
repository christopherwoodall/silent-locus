# PROVENANCE — counter-channel snapshot

Lane L (2026-09-28). Read-only snapshot of the countapi.mileshilliard.com
agent counter channel documented in the thecolony.ai incident wiki.

## Method

- Named-key GETs only: `GET /api/v1/get/<key>`. No increments, no creates,
  no updates. Verified a nonexistent key returns 404 "Key not found"
  (no creation side-effect) before probing.
- Sibling enumeration: 12 read-only GETs (bare key + 11 suffix variants),
  all 404.
- `/api/v1/info/<key>` and `/api/v1/namespace/<ns>`: 404 (this countapi
  clone exposes no list/info endpoints).

## Result

| key | value | note |
|---|---|---|
| langr5backup4813_CA | 4 | unchanged from 2026-09-04 report |
| langr5backup4813_TX | 2 | unchanged from 2026-09-04 report |
| langr5backup4813_ZZ | 2 | documented-fake key now carries a value — channel being poked |

## Files

- `snapshot_2026-09-27.json` — values, HTTP statuses, probe results, comparison.

## Scope

Counters only. No attempt to attribute who incremented them.

## Closure 2026-09-28 (workstream D)

Naturally small: one read-only counter-channel snapshot of a single
countapi-clone namespace documented in the incident wiki. N=4 docs (3
counter_reading + 1 counter_probe) is the complete enumeration — the only 3
documented keys plus a sibling-enumeration probe (12 read-only GETs, all 404)
showing the host exposes no list/info endpoints to expand from. ES
`counter-channel` _count=4 verified. Nothing further to pull from this venue.

## Schema build 2026-09-29 (worker W6)

- `events.jsonl` built from `raw/snapshot_2026-09-27.json`: 4 rows
  (3 `counter_reading` + 1 `counter_probe`), matching the N=4 complete
  enumeration in the closure note above. Both kinds are new (not in the
  schema registry).
- Fingerprint identity strings: `countapi.mileshilliard.com|<counter key>`
  for readings; `countapi.mileshilliard.com|sibling_probe` for the probe.
- `@timestamp` = per-key `retrieved_at_utc` for readings
  (`labels:key.retrieved_at`); `snapshot_at_utc` for the probe
  (`labels:snapshot_at_utc`).
- `SHA256SUMS` regenerated covering every file in the directory.

## Rollup review 2026-09-29 (W8)

rollup: none — 4 rows (3 counter_reading + 1 counter_probe) are the complete
single-snapshot enumeration; no time series, no aggregate layer.

## Build-script relocation 2026-09-29 (ingest-script condensation)

- Moved `scripts/es_ingest_counter.py` into this collection dir per Christopher's build-script convention (single-collection build scripts live in the event directory).
- Path fixes in the moved script: `D` is now the script's own dir (self-locating); `REPO_ROOT` resolves three levels up for the mapping path.
- BUG FIX: `build_docs()` read `{D}/snapshot_2026-09-27.json` but the snapshot lives at `raw/snapshot_2026-09-27.json` — the old path never existed, so `--load` was broken; fixed to the `raw/` path.
- Verified offline (2026-09-29): `build_docs()` assembles 4 docs from disk (3 counter_reading, 1 counter_probe) with no network/ES access.
- ES ingest driver: `push_to_local_es.py --all` runs the path in `scripts/local_es_manifest.json` `via_script` for index `2026-09-28-counter-channel`; manifest entry updated to the new script location.

## Historical loader relocation (2026-09-30)

Preserved `es_ingest_counter.py` at `raw/scripts/legacy/es_ingest_counter.py` as a historical, optional Elasticsearch loader; it is not an active collection event builder. Its local path resolution now targets the same collection and repository inputs from the archived location. No source evidence, `events.jsonl`, or `rollup.jsonl` was changed; no network or ES actions were run. The SHA256SUMS entry records the relocated script bytes.
