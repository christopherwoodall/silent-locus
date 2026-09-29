# PROVENANCE — proxy-primitives (Lane F sweep, 2026-09-27)

Lane F of the escaped-eval toolkit hunt. Sweeps longcat's 207-domain-audit
proxy primitives — `pure.md`, `api.cors.lol`, `corsmirror.com`, Google Docs
Viewer `gview` — across the hunt's own corpora, including URL-encoded
variants (`pure%2emd`, `pure%252emd`, double-encoded hosts).

## Sources swept

1. **Elastic `collusion-wiki` index (80,434 docs)** — read-only regexp on
   `matched_string`/`external_links` keyword fields + wildcard query_string
   on `note`/`meta_description`/`matched_string.text`, per primitive.
   RESULT: effectively blind. The ingest withheld raw URLs
   (`labels.url_withheld=true` on wiki_link docs), so pure.md/api.cors.lol/
   corsmirror return 0 even though the URLs exist in the source dumps.
   Only 21 gview hits (in notes/descriptions). The ES sweep is documented
   here for honesty; the local corpus is the authoritative source.
2. **Local `data/collusion-wiki/*.jsonl.gz`** — links (553 hits), revisions
   (first-seen timestamps), records (414 agent annotation rows; operational
   URLs omitted in-dump, host+sha256 survive), pages, events, shortener-logs.
3. **Local pivot products** — `wiki_ioc_pivots.jsonl` (829 structured IOC
   rows), `wiki_shortener_detail.json` (4), `wiki_ioc_pivot_summary.json` (3).
4. **Gem corpus** — `gem-ioc-log.jsonl`, `gem-ioc-hits.jsonl`,
   `gemstuffer-jfrog-2026-09-27.csv`, `gem-graph-*.jsonl`,
   `osv/diffend_sweep_results.jsonl`: **zero real proxy-primitive URLs**.
   Only matches are gem-name fragments `zjgview5`, `zrgview1`, `zrgview2`
   (zz-grammar names), flagged `record_kind=gem-name-fragment`, not proxy use.

## Output

- `hits.jsonl` — 1,522 hit records after exact-duplicate collapse.
  Fields: `primitive`, `source`, `matched_string`, `laundered_target`
  (best-effort parse of the wrapped URL; null when the source dump truncated
  the URL — e.g. `http://api.cors.lol/?url=https:%2`), `first_seen_effective`
  (earliest revision `write_date` containing the exact URL; null where the
  dump carries no timestamp), plus source-specific context
  (host/relation/wikis/agents/record_id).
- `progress.log` — run log.

## Known limitations

- `first_seen_effective` is a lower bound from the corpus snapshot, not the
  internet-wide first use.
- Some `links.jsonl.gz` URLs are truncated in the released dump; their
  laundered target is unrecoverable (marked null).
- The `collusion-wiki` ES index cannot corroborate URL content
  (url_withheld); do not cite ES counts as coverage.
- Agents/infrastructure only: no operator identity, registrant details, or
  person-focused attribution was collected or is present here.

## Reproduce

`python3 scripts/sweep_proxy_primitives.py` (ES + raw local grep) then
`python3 scripts/extract_wiki_proxy_urls.py` (structured wiki extraction,
merge, dedup). Both are idempotent; merge collapses exact duplicates only.

## Schema backfill 2026-09-29

Brought `hits.jsonl` (1,522 records) onto `schema/record.schema.json` via
`temp/backfill_w4.py` (idempotent, stdlib only).

- **event**: added `{"dataset": "proxy-primitives", "created": <backfill run
  time UTC>}` to every record (none existed).
- **record_kind**: existing values kept verbatim, except the two hyphenated
  values that violate `^[a-z0-9_]+$`: `corpus-hit` -> `corpus_hit` (3
  records) and `gem-name-fragment` -> `gem_name_fragment` (6 records);
  originals preserved under `labels.record_kind_original`. Remaining kinds:
  `wiki_link` (553), `wiki_record_annotation` (128), `wiki_ioc_pivot` (827),
  `wiki_shortener` (4), `wiki_revision` (1).
- **fingerprint**: identity string is `labels.hit_sha` — the sha256 hex
  precomputed by the source pipeline over the hit tuple, adopted verbatim as
  the fingerprint (verified unique over all 1,522 rows; no collisions).
- **@timestamp**: `labels.first_seen_effective` > `labels.first_seen` >
  `labels.time` (normalized to UTC Z; provenance recorded in
  `labels.timestamp_source = "labels:<field>"`). 1,127 of 1,522 records have
  no recoverable event time and carry the sentinel `1970-01-01T00:00:00Z`
  with `labels.timestamp_source = "fallback:no_recoverable_date"`.
- All other non-canonical top-level fields moved into `labels` unchanged
  (`primitive`, `source`, `host`, `relation`, `wikis`, `agents_sample`,
  `context`, `doc_id`, etc.). `matched_string`, `source_url`, `tags`, and the
  one pre-existing `labels` dict were kept in place. Lossless: no fields
  dropped.

## Aggregates move 2026-09-29

Multi-source conglomerate collections now live under `data/aggregates/`.

- `data/proxy-primitives/` -> `data/aggregates/proxy-primitives/`
  (whole directory: PROVENANCE.md, SHA256SUMS, hits.jsonl, progress.log).
- Event-file naming convention applied: `hits.jsonl` ->
  `proxy-primitives.jsonl` (1,522 records, contents unchanged; schema
  backfill from 2026-09-29 above still applies verbatim).
- SHA256SUMS not regenerated (orchestrator handles checksums/manifest
  references centrally).
