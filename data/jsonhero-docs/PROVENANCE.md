# PROVENANCE — data/jsonhero-docs/

Separate dataset: the 17 jsonhero.io shared documents the wiki agent swarms used
as collaborative state (found by recon lane F). Kept out of `data/collusion-wiki/`
by design.

## Sources

| File | Source | Retrieved |
|---|---|---|
| `<docid>.json` (11 files) | `GET https://jsonhero.io/j/<docid>.json` — the docs were published to jsonhero.io's unauthenticated public document API; fetched read-only, paced ≥3s, browser UA | 2026-09-28 |
| `manifest.json` | Retrieval log: doc id, source URL, HTTP status, live/dead, SHA-256, byte size, corpus URL-occurrence count | 2026-09-28 |
| `../jsonhero_doc_links.jsonl` | Cross-reference: 2,273 wiki-revision → doc URL links, extracted read-only from `data/collusion-wiki/revisions.jsonl` (fields: doc_id, view, path_param, wiki, agent_label, page_key, rev_id, rev_time) | 2026-09-28 |

## Method

- Doc ID list from `../jsonhero/usage_patterns.json` (17 unique IDs, 2,398 corpus URL occurrences).
- Fetch: urllib first (IncompleteRead failures on larger bodies — egress-proxy
  streaming artifact), then curl — 11/17 live, 6/17 HTTP 500 "Unexpected Server
  Error" (recorded dead; all 6 are referenced in June-2026 wiki revisions, so
  they were live during the campaign and died since).
- Dedupe: 7 docs byte-identical (SEC regCF county dataset), 2 byte-identical
  (county GeoJSON) — kept all, dedupe group recorded in manifest labels.
- Inspection: key inventory, `?path=` deep-link resolution check, IOC battery
  (jina/md.succ.ai/jqp/webhook/shortener/go-import/img-beacon — zero hits).

## Cascade attempt (no data retrieved)

- `https://www.sec.gov/files/county.json` (the upstream source cited inside doc
  `KwQ0rn8weoBu`) — HTTP 403 bot-block from this network. Not retried
  aggressively. The agents fetched it via reader proxies (jqp/md.succ.ai),
  which is exactly why the proxy layer exists.

## Limitations

- Agent labels in the corpus are publisher-redacted; wiki↔doc links carry
  redacted handles only.
- No operator identity pursued; agents/infrastructure only.

## Keep-all + annotate

No records dropped. Dead docs are kept as manifest entries (not silently
omitted). Byte-identical re-posts are kept as separate files with a shared
dedupe-group label.
