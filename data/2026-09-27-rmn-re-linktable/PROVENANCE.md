# 2026-09-27-rmn-re-linktable — provenance

RMN RE link-table index collection. Docs are built by
`scripts/es_ingest_rmnre.py` from raw sources in
`data/2026-09-27-rmn-re/raw/` (link table capture + decoded JSON) and
`data/aggregates/2025-09-26-cors-bwa-proxy/raw/`.

- 2026-09-29: materialized as a physical collection dir
  (`events.jsonl` via the builder's `--dump` mode) under the canonical
  layout; previously a virtual registry entry with no directory.

## Materialization 2026-09-29 (worker W1)

The earlier note above claimed a `--dump` materialization that did not
exist; this dir was a PROVENANCE.md alone. Materialized now from the only
physical dump on disk:

- **Source:** `data/aggregates/2025-09-26-cors-bwa-proxy/raw/rmn-re-linktable.jsonl`
  — a single ES doc (`_index: rmn-re-linktable`, `record_kind: shortlink`,
  `_id: rmn:masscounty1781813461d`).
- **events.jsonl:** 1 row, shared event schema (`@timestamp`,
  `event.dataset=2026-09-27-rmn-re-linktable`, `record_kind=shortlink`,
  `fingerprint`, flat `labels`, `source_url`). Labels keep the ES doc's
  label keys verbatim plus `link.slug`/`link.target`;
  `labels.timestamp_source = "es:_source.@timestamp"`.
- **Fingerprint:** `sha256(slug)` = the same identity-string recipe as
  `data/2026-09-27-rmn-re/` — recomputed there first and reproduced its
  row exactly (`sha256("gmb")=b87a098f…`) before writing this one
  (`sha256("masscounty1781813461d")=66411d6b…`).
- **No rollup.jsonl:** a single row has no genuine aggregate layer, so no
  rollup was built (documented here instead).
- **SHA256SUMS** regenerated in this dir covering all files.
