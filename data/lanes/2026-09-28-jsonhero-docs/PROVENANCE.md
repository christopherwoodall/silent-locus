# PROVENANCE — data/2026-09-28-jsonhero-docs/

Separate dataset: the 17 jsonhero.io shared documents the wiki agent swarms used
as collaborative state (found by recon lane F). Kept out of `data/2026-05-17-collusion-wiki/`
by design.

## Sources

| File | Source | Retrieved |
|---|---|---|
| `<docid>.json` (11 files) | `GET https://jsonhero.io/j/<docid>.json` — the docs were published to jsonhero.io's unauthenticated public document API; fetched read-only, paced ≥3s, browser UA | 2026-09-28 |
| `manifest.json` | Retrieval log: doc id, source URL, HTTP status, live/dead, SHA-256, byte size, corpus URL-occurrence count | 2026-09-28 |
| `data/aggregates/2026-09-29-overlap-analysis/raw/jsonhero_doc_links.jsonl` | Cross-reference: 2,273 wiki-revision → doc URL links, extracted read-only from `data/2026-05-17-collusion-wiki/raw/revisions.jsonl` (fields: doc_id, view, path_param, wiki, agent_label, page_key, rev_id, rev_time) | 2026-09-28 |

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

## Closure 2026-09-28 (workstream C)

Expanded then closed: bounded retry of the 6 HTTP-500 docs recovered
`swJMw8b6VwDC` (now HTTP 200, 70,089 B, regCF county family — distinct from the
85,889 B dedupe group; body fetched, manifest updated, ingested — live docs
11->12). The remaining 5 still return HTTP 500; all were live in June 2026 per
wiki-revision citations and died since. N=17 docs = the complete 17-ID corpus
list from `../jsonhero/usage_patterns.json` (12 live + 5 dead) — the venue is
exhaustively enumerated. ES `jsonhero-docs` _count=17 verified, schema-drift
clean.

## Schema normalization 2026-09-29 (worker W7)

- Built `events.jsonl`: 12 records, one per live doc JSON in `raw/` (builder:
  `temp/build_events_w7.py`, repo root passed as argv[1]).
- record_kind: `artifact_observation` (existing registry kind; no new kinds introduced).
- Fingerprint identity string: `jsonhero-doc:<doc_id>` (sha256 hex of that string).
  Method verified against the reference: recomputing sha256("TheNacken/python-cors-proxy")
  reproduces data/2023-11-14-hfspace-proxies' fingerprint `14c645d9…efbe94` exactly.
- `@timestamp`: `2026-09-28T00:00:00Z` for all records
  (`labels.timestamp_source = "fallback:dir_date_prefix;manifest retrieved_at_utc partially
  redacted (02:5x:00Z)"`) — the manifest's retrieval timestamps carry a redacted digit
  and are not parseable, so no per-doc event time is recoverable.
- Body sha256 + byte_size verified per file against `manifest.json` at build time
  (all 12 match); verified values carried as top-level `sha256` / `size_bytes`.
- The 5 dead docs (HTTP 500, no body file) remain manifest-only per the keep-all policy —
  no event records created for them. `manifest.json`'s `file` field still carries the
  legacy pre-normalization path prefix; left as-is (raw is immutable).
- `SHA256SUMS` regenerated (sha256sum-style): `events.jsonl` + all `raw/` contents,
  verified with `sha256sum -c`.

## Rollup 2026-09-29 (W8)

Built `rollup.jsonl`: 5 rows x `doc_family_rollup` — the 12 doc artifacts
cluster by (first top-level key, byte size): `regCF_county_2019:85889` (7
docs), `regCF_county_2019:70089` (1), `copyright:10942` (2),
`2019_005_code:1472` (1), `unkeyed:634` (1). Labels: family key/size,
doc count, total bytes, member doc ids; `@timestamp` = dir-date fallback
2026-09-28T00:00:00Z (no per-doc event times recoverable). Fingerprint
identity string `2026-09-28-jsonhero-docs|doc-family|<family_key>`.
Builder: `temp/build_rollup_w8.py` (repo root passed as argv[1]); counts and
byte totals independently recomputed from events (12 docs). `scripts/validate_schema.py`:
0 violations. SHA256SUMS regenerated (15 entries, incl. rollup.jsonl);
`sha256sum -c` OK.

## 2026-09-29 — build scripts co-located per convention
Normalization-wave build scripts moved from `temp/` to the collection root
per the 2026-09-29 convention (single-collection build scripts live in the
collection dir; schema/collections.md). `temp/` removed. SHA256SUMS
regenerated; `sha256sum -c` green.

## Historical loader relocation (2026-09-30)

Preserved `es_ingest_jsonhero.py` at `raw/scripts/legacy/es_ingest_jsonhero.py` as a historical, optional Elasticsearch loader; it is not an active collection event builder. Its local path resolution now targets the same collection and repository inputs from the archived location. No source evidence, `events.jsonl`, or `rollup.jsonl` was changed; no network or ES actions were run. The SHA256SUMS entry records the relocated script bytes.
