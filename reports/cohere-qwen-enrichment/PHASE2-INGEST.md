# Phase-2 ingest note — Cohere Qwen enrichment entities

- Batch: `data/records/6d4bfbca983342ccaa7cd7a935e8a185/` — 195 records:
  1 run, 2 sources, 1 dataset.snapshot observation, 135 infra.ioc
  observations, 56 claim records.
- Idempotency key: `cohere-qwen-enrichment-phase2`. Actor: `agent:cohere-qwen-phase2`.
  Lane tag `cohere-qwen-enrichment` on every record.
- Source: `entities.json` (335 rows, verifier VERIFIED-WITH-GAPS, gaps closed)
  + `ioc-list.md` (124 IOCs). All 124 ioc-list entries are contained in
  entities values, so ioc-list was treated as a view only and NOT
  double-ingested.
- Reconciliation (335 rows in, 191 kept, 144 dropped):
  - Kept: 135 indicator rows as infra.ioc + 56 descriptive rows as claims.
  - Dropped, within-batch duplicate (82): same sanitized value in both
    lanes (linguist + cryptologist) or repeated across types; first
    occurrence kept.
  - Dropped, token/query value withheld (3): a 32-hex resource id, an
    `Expires` param value, and an `sv` param value. Values are NOT recorded
    anywhere in this note, the batch, or the commit, per the signed-URL rule.
  - Dropped, corpus overlap (59): term already present verbatim in exported
    records (examples: sanmaohe host + URL, routify-file-proxy-sg host,
    PROBE_PAYLOAD_ABC123, /tmp/put_probe, cohere.com, huggingface.co).
- Mapping: DOMAIN/url_host -> category domain; URL/url -> url-pattern with
  the query string stripped (2 rows sanitized); IP -> ip; TOOL_CALL -> marker;
  all other indicator types -> other. Status active for OBSERVED rows,
  candidate for INFERENCE/UPSTREAM rows. Descriptive types (product, model,
  publisher, dataset, task, tool, benchmark, timestamp, count_claim,
  OSS_REGION, COMMAND, FLAG_SEQUENCE) -> claim records with property
  "entity", subject + cites to the enrichment corpus snapshot observation,
  basis = the row's entities.json grade. Grades were never upgraded; every
  record carries its row grade in tags.
- Signed-URL rule: zero query strings, signatures, tokens, or key values in
  the batch (grep verified: no `Signature=`, `OSSAccessKeyId`, `Expires=`,
  `sv=` substrings; no `?` in any ioc term). Raw files were never modified.
- Export + verify --blobs after ingest: ok=true, verified=true, pending=0.
  Corpus total after export: 208,568 records (208,360 + 13 hunt + 195
  enrichment). The 1,737 missing artifacts in verify output are corpus-wide
  pre-existing local-only bytes; this batch carries no file artifacts.
- Not pushed by this worker. Parent pushes and verifies.
