# Elastic DB export — 2026-09-28

Full snapshot of the hunt's Elasticsearch indices, taken after the
`collusion-wiki` ingest stabilized (80,434 docs, stable across 5-min checks).

Cluster: agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud (Elastic Cloud, us-east-1)

| Index | Docs | File | Size | SHA-256 |
|---|---|---|---|---|
| rubygems-goimport-campaign | 6,619 | rubygems-goimport-campaign-20260928T022324Z.jsonl.gz | 284 KB | 439e7fcdcc7812203435ce794956f440cde12c0c84937adb80266829fd9125dc |
| urlquery-incidents | 51,643 | urlquery-incidents-20260928T022324Z.jsonl.gz | 8.5 MB | b46f0f3a7dc6f133618bcdf24bed3393f6985309598fa8764204bb5752d899dd |
| collusion-wiki | 80,434 | collusion-wiki-20260928T025051Z.jsonl.gz | 9.9 MB | 53f19bb1a7cd28ea4ea6d8460e46f150495b913211ef4b795baf00d569ade06a |

Export method: scroll API (`scripts/es_export.py`), read-only, `sort: ["_doc"]`.
Each line: `{"_id": ..., "_source": {...}}` (UTF-8 JSON, gzip).
Verification: `gunzip -t` clean on all files; 100 sampled lines per file parse
and carry `_id`/`_source`; exported doc count == live `_count` per index.

## Restore

1. Create the index with the canonical mapping from
   `../notes/gems-es-mapping.json` (shared schema, 56 properties).
2. Convert each line to `_bulk` action pairs:
   `{"index": {"_index": "<index>", "_id": "<_id>"}}` followed by the `_source` JSON.
3. `POST /_bulk` in batches (5–10 MB per request).

The `.meta.json` sidecar per file records expected vs exported counts and status.

## Pass 2 — 2026-09-28 ~03:13 UTC (full DB snapshot)

Re-exported all three pass-1 indices (fresh timestamps, pass-1 files untouched)
plus every index added since: `urlquery-hunt` (omitted from pass 1),
`paste-linuxiarz`, `paste-archive`, `jsonhero-docs`, `jsonhero-docs-archive`,
`rmn-re-history`, `rmn-re-linktable`. Complete `_cat/indices` listing taken
before export — no other indices exist on the cluster.

| Index | Docs | File | Size | SHA-256 |
|---|---|---|---|---|
| rubygems-goimport-campaign | 6,619 | rubygems-goimport-campaign-20260928T030726Z.jsonl.gz | 277 KB | 439e7fcdcc7812203435ce794956f440cde12c0c84937adb80266829fd9125dc |
| urlquery-incidents | 51,643 | urlquery-incidents-20260928T030741Z.jsonl.gz | 8.5 MB | a40b39c7824e9d4949c44369d6fb8fe1042ec48ccdf9e7ead012aa9f7ccaaf1a |
| collusion-wiki | 80,434 | collusion-wiki-20260928T030925Z.jsonl.gz | 9.4 MB | 53f19bb1a7cd28ea4ea6d8460e46f150495b913211ef4b795baf00d569ade06a |
| urlquery-hunt | 3,504 | urlquery-hunt-20260928T031202Z.jsonl.gz | 435 KB | 81fb1bc983111b837db9febb781b6f5d7f11abd5a93d630187d13ea6cda3b89c |
| paste-linuxiarz | 131 | paste-linuxiarz-20260928T031217Z.jsonl.gz | 46 KB | 20e0d9846515da063302da19a2698beedaa675872ee280769ad4677b5cee7dcd |
| paste-archive | 76 | paste-archive-20260928T031225Z.jsonl.gz | 7 KB | 3f7a9689d415789ef740c48a608ac7fbf8adf914e56dc415c6d6b5a5ee4089b7 |
| jsonhero-docs | 17 | jsonhero-docs-20260928T031237Z.jsonl.gz | 2 KB | 70a5da9e181b2697b3e23cb5c493ae50bbf7369b4b896225dc02aecfccf6742e |
| jsonhero-docs-archive | 6 | jsonhero-docs-archive-20260928T031247Z.jsonl.gz | 1 KB | 8bc03080a0ada91072ddf304215c0b2043670c891ad6fc45b7c1d1d27622ac2d |
| rmn-re-history | 764 | rmn-re-history-20260928T031256Z.jsonl.gz | 35 KB | d0e3b166809c973b4d1b0aac39aba8319210db75f4f3723ad5ad3aa9f27c2711 |
| rmn-re-linktable | 764 | rmn-re-linktable-20260928T031306Z.jsonl.gz | 43 KB | a38f72b9da7ca1a817dc81cc1fa4c2b37007a6ee542ad1f48bba9e67f57cde45 |

Pass-2 totals: **143,958 docs, ~19.7 MB** across all 10 indices.
Verification: `gunzip -t` clean on all files; sampled lines parse with
`_id`/`_source`; exported count == live `_count` per index. Note: `_cat/indices`
`docs.count` reads higher than `_count` on re-ingested indices (deleted segments
not yet merged) — `_count` is authoritative and matches every export.
