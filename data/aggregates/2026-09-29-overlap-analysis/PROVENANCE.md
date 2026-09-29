# overlap-analysis — provenance

Support collection: cross-corpus overlap/pivot analysis outputs. Not loaded
to Elasticsearch (index: none).

| File | Produced by | Content |
|---|---|---|
| matches-f1f2.jsonl | scripts/extract_f1f2.py | F1/F2 marker matches against the corpus |
| matches-f3.jsonl | scripts/build_timeline_anchors.py | F3 timeline-anchor matches |
| matches-f4f7f8f10f11f12.jsonl | scripts/negative-sweep-f4f7f8f10f11f12.py | negative-sweep hits and misses |
| matches-f5f6.jsonl | scripts/extract_f5f6.py | F5/F6 marker matches |
| overlap-matches.jsonl | scripts/overlap-scan (see notes/) | cross-corpus overlap results |
| wiki_ioc_pivots.jsonl | scripts/wiki_ioc_pivot.py | IOC pivot rows across wiki/gems corpora |
| wiki_paste_links.jsonl | scripts/wiki_ioc_pivot.py | paste links referenced by the collusion wiki |
| wiki_gem_bridge.json | scripts/gem83_reconciliation_build.py | bridge between wiki and gem corpora |
| wiki_ioc_pivot_summary.json | scripts/wiki_ioc_pivot.py | aggregate pivot summary |
| wiki_shortener_detail.json | scripts/wiki_ioc_pivot.py | shortener IOC detail |
| jsonhero_doc_links.jsonl | scripts/wiki_ioc_pivot.py | jsonhero document link inventory |

Fingerprint identity strings: see "Aggregates move 2026-09-29" below
(supersedes the earlier "not applicable" note — the JSONL final outputs are
now schema events).

## Aggregates move 2026-09-29

Multi-source conglomerate collections now live under `data/aggregates/`.

- `data/overlap-analysis/` -> `data/aggregates/overlap-analysis/`
  (whole directory: PROVENANCE.md, SHA256SUMS, all JSONL/JSON files).

## Raw layer 2026-09-29

Script-consumed inputs moved to `raw/` keeping upstream names (exempt from
the event schema):

- `wiki_ioc_pivots.jsonl` -> `raw/wiki_ioc_pivots.jsonl`
  (read by `scripts/es_ingest_powerbi.py`, `scripts/extract_wiki_proxy_urls.py`,
  `scripts/sweep_proxy_primitives.py`).
- `jsonhero_doc_links.jsonl` -> `raw/jsonhero_doc_links.jsonl`
  (read by `scripts/es_ingest_jsonhero.py`,
  `scripts/es_ingest_jsonhero_archive.py`).

Non-JSONL files left at root: `wiki_gem_bridge.json`,
`wiki_ioc_pivot_summary.json`, `wiki_shortener_detail.json`.

## Schema backfill 2026-09-29

The six write-only, regenerable final outputs were backfilled in place onto
`schema/record.schema.json` via `temp/backfill_w6.py` (idempotent, stdlib
only, lossless — every original field survives; validated clean with
`scripts/validate_schema.py`; line counts before/after identical):

| File | Records | record_kind |
|---|---|---|
| matches-f1f2.jsonl | 25 | overlap_match |
| matches-f3.jsonl | 13 | overlap_match |
| matches-f4f7f8f10f11f12.jsonl | 72 | overlap_match |
| matches-f5f6.jsonl | 8,409 | overlap_match |
| overlap-matches.jsonl | 8,519 | overlap_match |
| wiki_paste_links.jsonl | 317 | paste_link |

Fingerprint identity strings (sha256 hex of):

- `overlap_match`: `overlap-analysis|overlap_match|<match_id>|<evidence-or-swarmtraces_evidence>`
  (`match_id` alone collides on the 537 exact-duplicate rows in
  matches-f5f6/overlap-matches; byte-identical rows intentionally share one
  fingerprint).
- `paste_link`: `overlap-analysis|paste_link|<link_type>|<paste_id>|<wiki_side>`
  (verified unique over all 317 rows).

Field handling:

- `event`: `{"dataset": "overlap-analysis", "created": <backfill run time UTC>}`.
- The pre-existing top-level `fingerprint` field was the hunt-finding FAMILY
  label (`F1`, `F3`, `F6`, `ntfy-topic`, ...), not a hash — moved to
  `labels.match.family`; the new top-level `fingerprint` is the sha256 above.
- No date fields exist in these records: sentinel
  `@timestamp = 1970-01-01T00:00:00Z` with
  `labels.timestamp_source = "fallback:no_recoverable_date"`.
- Remaining fields moved to `labels` (dotted): `match.id`, `match.kind`,
  `hunt.ioc`, `hunt.ioc_type`, `hunt.reference`, `swarmtraces.id`,
  `swarmtraces.payload_id`, `swarmtraces.field`, `swarmtraces.evidence`,
  `evidence`, `notes`, `link.type`, `paste.id`, `paste.title`, `wiki_side`,
  `wiki_agents`, `wiki_wikis`. `confidence` and `note` are canonical
  top-level and stayed in place.
