# 2026-06-19-rmn-re-linktable — provenance

RMN RE link-table index collection. Docs were built by
`es_ingest_rmnre.py` (now co-located in this dir) from raw sources in
`data/2016-12-28-rmn-re/raw/` (link table capture + decoded JSON) and
`data/aggregates/2025-09-26-cors-bwa-proxy/raw/`.

- 2026-09-29: materialized as a physical collection dir
  (`events.jsonl` via the builder's `--dump` mode) under the canonical
  layout; previously a virtual registry entry with no directory.
- **Builder location:** the historical build script `es_ingest_rmnre.py`
  (moved here from `scripts/` 2026-09-29 per the single-collection
  convention) reads `data/2016-12-28-rmn-re/raw/link_table_decoded_2026-09-27.json`;
  note the 1-row `events.jsonl` below was materialized from the aggregates
  JSONL, not from a fresh run of this builder.

## Materialization 2026-09-29 (worker W1)

The earlier note above claimed a `--dump` materialization that did not
exist; this dir was a PROVENANCE.md alone. Materialized now from the only
physical dump on disk:

- **Source:** `data/aggregates/2025-09-26-cors-bwa-proxy/raw/rmn-re-linktable.jsonl`
  — a single ES doc (`_index: rmn-re-linktable`, `record_kind: shortlink`,
  `_id: rmn:masscounty1781813461d`).
- **events.jsonl:** 1 row, shared event schema (`@timestamp`,
  `event.dataset=2026-06-19-rmn-re-linktable`, `record_kind=shortlink`,
  `fingerprint`, flat `labels`, `source_url`). Labels keep the ES doc's
  label keys verbatim plus `link.slug`/`link.target`;
  `labels.timestamp_source = "es:_source.@timestamp"`.
- **Fingerprint:** `sha256(slug)` = the same identity-string recipe as
  `data/2016-12-28-rmn-re/` — recomputed there first and reproduced its
  row exactly (`sha256("gmb")=b87a098f…`) before writing this one
  (`sha256("masscounty1781813461d")=66411d6b…`).
- **No rollup.jsonl:** a single row has no genuine aggregate layer, so no
  rollup was built (documented here instead).
- **SHA256SUMS** regenerated in this dir covering all files.

## 2026-09-29: ingest script co-located (hunt convention)
- `es_ingest_rmnre.py` moved from `scripts/` into this directory per
  Christopher's single-collection convention; transforms
  `data/2016-12-28-rmn-re/raw/link_table_decoded_2026-09-27.json` into
  shared-schema docs (real transform, not a pure loader).
- `REPO_ROOT` in the script adjusted (repo root is now three levels up).
  Offline verification: `python3 -m py_compile` clean.
- `scripts/local_es_manifest.json` via_script entry repointed here.
- SHA256SUMS regenerated (script file + updated PROVENANCE added to coverage).

## 2026-09-29: date-prefix correction (worker)
Dir renamed `data/2026-09-27-rmn-re-linktable` → `data/2026-06-19-rmn-re-linktable`
per the date-prefix convention (prefix = first real event date): the single
event's `@timestamp` is `2026-06-19T00:11:00Z` (corroborated by the source ES
doc `_source.@timestamp` in `data/aggregates/2025-09-26-cors-bwa-proxy/raw/rmn-re-linktable.jsonl`).
Updated: `event.dataset` in `events.jsonl`, `INDEX`/`event.dataset` in
`es_ingest_rmnre.py`, refs in `schema/collections.json`,
`scripts/local_es_manifest.json`, `scripts/cors_bwa_analyze.py`,
`scripts/cors_bwa_collect.py`, README collection table, `temp/index_map.json`.
`SRC` repointed to the sibling `data/2016-12-28-rmn-re/raw/` after its
own date-prefix correction (2026-09-27 → 2016-12-28, first event 2016-12-28).

## Historical loader relocation (2026-09-30)

Preserved `es_ingest_rmnre.py` at `raw/scripts/legacy/es_ingest_rmnre.py` as a historical, optional Elasticsearch loader; it is not an active collection event builder. Its local path resolution now targets the same collection and repository inputs from the archived location. No source evidence, `events.jsonl`, or `rollup.jsonl` was changed; no network or ES actions were run. The SHA256SUMS entry records the relocated script bytes.
