# Wiki ingest lane — collusion.wiki as a first-class dataset (2026-09-27)

## What was done
1. **Re-downloaded all 11 Nightingale dumps** from
   https://collusion.wiki/explorer/download (lane 22's `/tmp/collusion/`
   copies were lost on a VM rebuild). All **11/11 SHA-256 checksums verify**
   against the publisher's list (`sha256sum -c SHA256SUMS` clean).
2. **Moved to permanent home**: `data/collusion-wiki/` (both `.gz` and
   expanded files; 94 MB total).
3. **Provenance**: `data/collusion-wiki/PROVENANCE.md` — source, retrieval
   date, verbatim hashes, export caveats (publisher-selected agent-related
   text, /16-truncated IPs, redacted usernames, write-date cut ≥ 2026-05-01).
   Keep-all + annotate policy followed: zero records dropped; derived
   annotations marked `labels.annotated_by=es_ingest_wiki`.
4. **Schema doc**: `notes/collusion-wiki-schema-2026-09-27.md` — every dump's
   fields plus the shared-schema mapping table and noted gaps.
5. **Bridge**: `data/wiki_gem_bridge.json` ingested as `record_kind=wiki_bridge`
   (79 docs) — joins the gem indices on shared `package`/`gem`/`wave` fields.
6. **Elastic**: new index **`collusion-wiki`**, created with the canonical
   shared mapping from `notes/gems-es-mapping.json` (no new top-level fields;
   wiki-specific detail in `labels` (flattened) + `tags`). Ingested
   incrementally per Christopher's order, count confirmed after each load.
7. **Dashboards**: 4 new Kibana dashboards (17 visualizations), data view
   `collusion-wiki*`, exported to `kibana-exports/` (timestamped NDJSON via
   the existing export script — coordinated with the export lane, no
   overwrites).

## Index contents (80,434 docs, all counts confirmed in-index)

| record_kind | docs | source |
|---|---|---|
| wiki_revision | 14,591 | revisions.jsonl (full bodies in `description`) |
| wiki_page | 4,579 | pages.jsonl |
| wiki_event | 19,913 | events.jsonl (save/delete/revert/probe) |
| wiki_link | 23,877 | links.jsonl |
| wiki_record | 13,703 | records.jsonl |
| wiki_label | 3,103 | labels.jsonl |
| wiki_shortener | 499 | shortener-logs.json (rmn.re) |
| wiki_other_page | 90 | other-wikis.json (8 pages) |
| wiki_bridge | 79 | wiki_gem_bridge.json |

## Corpus stats
- Per-wiki revisions: dse 13,403 / probier 1,013 / fractal 169 / dorfwiki 6;
  pages: dse 3,908 / probier 601 / fractal 68 / dorfwiki 2.
- Time span: revisions 2026-05-24 → 2026-07-02; events (incl. probes)
  2026-05-17 → 2026-07-14.
- Agent labels: 3,103 (3 human handles); IPs /16-truncated at source.
- Page name grammars: epoch10 501 / oai 225 / zz* 59 / 999 54;
  `try[a-z][0-9]zz` absent (RubyGems-only).
- Link hosts: wikiservice.at 8,723 / jqp.vercel.app 4,602 / api.datausa.io
  2,217 / sec.gov 1,648 / md.succ.ai 1,434; proxy families tagged
  (`proxy:jina|translate|hf-space|other`).
- Bridge: 79 June-18 gems, `wave=june-18`, `status=dead`; homepage hosts
  sec.gov 33 / r.jina.ai 18 / markdown.new 8 / allorigins 5 / …

## Schema conformance (per parent's correction)
Every wiki concept maps to an existing shared field
(`record_kind`, `@timestamp`, `event.dataset`, `observer`, `source_url`,
`description`, `note`, `authors`, `external_links`, `tags`, `labels`,
plus `gem`/`package`/`version`/`wave`/`status`/`meta_homepage`/`meta_summary`
on bridge docs). Gaps carried in `labels`, not extended: revision seq/RCS
path, /16 prefix, page_family, link relation/followed, record origin chain,
shortener clicks, time_grade/uncertainty provenance. Flattened `labels`
**does** support terms aggs (verified: `labels.wiki`, `labels.host`,
`labels.proxy_family` all aggregate) — dashboards use them.

## Bugs found and fixed during ingest
- `records.jsonl` `source_date_literal` is sometimes `"current"` or a bare
  epoch → normalized (epoch→ISO, "current"→no @timestamp, raw kept in
  `labels.source_date_literal_raw`); 3,954 records have no @timestamp.
- Terms-agg `include` is a **regex**, not a wildcard: `grammar:*` silently
  matched nothing → fixed to `grammar:.*`.
- Bridge host extraction missed the `[operational URL omitted; host=…]`
  placeholders → parse `host=` from the redaction note.

## Dashboards (Kibana, time range 2026-05-01 → 2026-07-20)
1. **Collusion Wiki — Activity** (`collusion-wiki-activity`): revisions over
   time by wiki; events over time by type; agent-name count; top agent labels.
2. **Collusion Wiki — Name grammars** (`collusion-wiki-grammars`): grammar-tagged
   revisions over time; grammar families on pages and on agent labels; notes.
3. **Collusion Wiki — Laundering chains** (`collusion-wiki-laundering`): proxy
   families in links; top link hosts; shortener target families; top keywords.
4. **Collusion Wiki — Gem bridge** (`collusion-wiki-gem-bridge`): bridge count;
   homepage proxy families/hosts; 79-gem table; bridge + mechanism-boundary notes.

Exports: `kibana-exports/dashboard-collusion-wiki-*-2026-09-28T024746Z.ndjson`
(+ all-dashboards bundle). Scripts: `scripts/es_ingest_wiki.py`
(`--only <type>` / `--all` / `--verify`), `scripts/build_wiki_dashboards.py`
(idempotent, fixed saved-object IDs).

## Scope
Agents/infrastructure only; no operator identity. The source export's /16
truncation and username redaction make person-level attribution impossible
by construction.
