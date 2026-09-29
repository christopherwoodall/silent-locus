# 2026-09-27-rmn-re-linktable — provenance

RMN RE link-table index collection. Docs are built by
`scripts/es_ingest_rmnre.py` from raw sources in
`data/2026-09-27-rmn-re/raw/` (link table capture + decoded JSON) and
`data/aggregates/2025-09-26-cors-bwa-proxy/raw/`.

- 2026-09-29: materialized as a physical collection dir
  (`events.jsonl` via the builder's `--dump` mode) under the canonical
  layout; previously a virtual registry entry with no directory.
