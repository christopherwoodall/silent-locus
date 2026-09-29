# Corpus schema — silent-locus

Machine-readable: [`record.schema.json`](record.schema.json) (JSON Schema draft
2020-12). Machine validation: `scripts/validate_schema.py` (stdlib only, no
dependencies). Run it before commit or ingest; it exits non-zero on any
violation.

## The one rule

Every JSONL record under `data/` is an **explicit event**. We do not
consolidate events. Rollups and joins live in support indexes, never in the
corpus files.

## Required fields

| Field | Meaning |
|---|---|
| `@timestamp` | Event time. UTC ISO-8601 with `Z`. Must parse. See fallback rule below. |
| `event.dataset` | Dataset slug, e.g. `collusion-wiki`. Doubles as the Elastic index/layer name. |
| `event.created` | When the pipeline created this record (UTC, `Z`). Not the event time. |
| `record_kind` | Snake-case record class (registry below). |
| `fingerprint` | SHA-256 hex of the dataset's documented identity string. |
| `labels` | All dataset-specific fields live here. Flat object, never nested. |

## Optional fields

`source_url`, `description`, `confidence` (`confirmed|high|medium|low` by
convention), `tags` (array of strings), `observer` (`{product, type, vendor}`),
`retrieved_at`, `retrieved_via`, `sha256`, `size_bytes`, `note`, `status`,
`matched_string`, `file` (relative path of the repo-local source artifact the
record was materialized from, e.g. `data/<collection>/raw/...`; complements
`source_url`, which is the upstream URL), `payloads` (array of embedded
per-item payload material: `{kind, content_type, content, encoding,
truncated, byte_size, sha256}`; complements `file`, which points at the full
repo-local artifact — embed small payloads fully, truncate large ones at a
documented cap with `truncated: true`). No other top-level keys are allowed.

## Timestamp rules

- All timestamps are UTC with `Z` suffix. Parseable or the record is invalid.
- `@timestamp` is the **event** time, not the pipeline time.
- When no event time is recoverable, use the documented sentinel
  `1970-01-01T00:00:00Z` **and** set
  `labels.timestamp_source = "fallback:no_recoverable_date"`. A missing event
  time must never silently become "now" (pipeline time); the sentinel is fixed,
  documented, and excludable from time-series analysis.
- When the timestamp is derived from a labels field, record the provenance:
  `labels.timestamp_source = "labels:<dotted.key>"` (e.g.
  `labels:published.at`).
- Date-like evidence that is *not* the event time stays in `labels`
  (e.g. `live_checked_at` prose, capture times) and is never promoted to
  `@timestamp` without proof of what it describes.

## Labels rules

- Dataset-specific fields go under `labels`, never at top level.
- Flat: values are strings, numbers, booleans, null, or arrays of scalars.
  No nested objects (ECS `labels` rule).
- Keys match `^[a-z0-9_.]+$`; dotted keys (`section.field`) namespace
  sub-structure, e.g. `published.at`, `gem.wave`.

## Fingerprint rules

- Always SHA-256 hex (64 chars). No MD5-era values.
- The identity string is dataset-specific and **must be documented in that
  dataset's PROVENANCE.md**, e.g. `venue + "|" + source_url`.
- Deterministic: same identity string always yields the same fingerprint.

## record_kind registry

Snake-case, one per record class. Enumerated 2026-09-28 against all
141,804 records in the 84 event files under `data/`: **100 kinds in use**,
all registered. Kinds newly added after the 2026-09-28 boundary backfill
carry a one-line description **(inferred)** from actual usage; kinds from
the previous registry are listed without change. Two 2026-09-29 additions
(`live_recheck`, `paste_text`) are produced by the collections' ES ingest
scripts as published index docs and are absent from the staged event
files, so they were missed by the event-file enumeration.

- `access_gap` — venue or resource that could not be probed, with reason and resolution status **(inferred)**
- `admin_cleanup_burst`
- `api_venue_target` — candidate data-API endpoint catalogued as a venue to probe **(inferred)**
- `archive_probe` — availability probe against archive.org (CDX, availability API, playback) **(inferred)**
- `artifact_observation`
- `board_note` — administrative note scraped from a public board surface **(inferred)**
- `board_post` — individual board post with swarm-marker verdict **(inferred)**
- `campaign_day_rollup` — per-day aggregate of a campaign dataset (graph nodes, gems, IOC counts) **(inferred)**
- `campaign_specimen`
- `comparator` — staging-lag comparator: dated staging pattern measured against a later run **(inferred)**
- `corpus_grep_negative`
- `corpus_hit`
- `counter_probe` — probe of a counter API (e.g. countapi) across candidate keys **(inferred)**
- `counter_reading` — single counter-channel key reading (value at retrieval time) **(inferred)**
- `coverage_gap` — coverage-gap assessment for a host: what prior evidence leaves unresolved **(inferred)**
- `cross_family_citation` — wiki pages linking one task family to another **(inferred)**
- `delete_event`
- `diffend_harvest`
- `diffend_probe`
- `diffend_wave_rollup` — per-wave rollup of a Diffend sweep (candidates, verified presence/absence) **(inferred)**
- `dns_probe` — DNS resolution check for candidate tunnel hostnames **(inferred)**
- `doc_family_rollup` — rollup of a recovered document family (doc count, byte totals) **(inferred)**
- `download`
- `eval_candidate`
- `exfil_identifier`
- `extraction`
- `file_drop_probe`
- `finding` — analyst/system finding distilled from a sweep, with legacy-fingerprint provenance **(inferred)**
- `forged_flag_ioc`
- `fork_day_rollup` — per-day rollup of repo forks (new + cumulative counts) **(inferred)**
- `forum_message` — forum/chat message row with swarm-marker verdict **(inferred)**
- `gem_name_fragment`
- `gist_scan_page` — one page of a public gist scan (scanned count, exploitgym hits) **(inferred)**
- `gomod_proxy_match`
- `graph_node`
- `issue_summary_rollup` — issue/PR activity summary over a window (open/closed, PRs) **(inferred)**
- `link_growth_rollup` — per-month growth curve of a shortener link table **(inferred)**
- `liveness_probe` — liveness probe of a relay surface (HTTP status, resolved IP) **(inferred)**
- `log_message` — single message row from a commonlog-style venue scan **(inferred)**
- `live_recheck` — later live re-verification of a paste collection's recoverability state, with a deterministic identity fingerprint **(inferred)**
- `marker_ambiguous`
- `null_read` — explicit negative: no agent activity found in a window/surface **(inferred)**
- `overlap_match` — single match between the hunt corpus and the SwarmTraces corpus **(inferred)**
- `paste_day_burst` — per-day burst summary of relay pastes (count, title tops, live-check status) **(inferred)**
- `paste_link` — link between a paste and its wiki-side surface **(inferred)**
- `paste_venue_rollup` — per-venue rollup of a paste archive (pastes, recovery, tradecraft battery) **(inferred)**
- `paste_text` — full text body of one recovered paste (sha256, size_bytes, source_url), an ES-side ingest doc **(inferred)**
- `pastebin_pivot_hit`
- `pastebin_probe`
- `pattern_sweep_rollup` — rollup of a corpus pattern sweep (pattern, hit counts, files) **(inferred)**
- `payload_reconstruction`
- `recovery_census` — census of archive-recovery attempts for dead documents (recovered vs not-archived) **(inferred)**
- `related_readme` — cached README of a related/fork-adjacent repo **(inferred)**
- `relay_paste`
- `repo_commit` — single GitHub commit record **(inferred)**
- `repo_commit_rollup` — per-repo commit rollup over a window, incl. breach-window overlap **(inferred)**
- `repo_fork` — single repo fork record **(inferred)**
- `repo_issue` — single issue/PR record **(inferred)**
- `repo_search_hit` — one hit from a GitHub repo code/description search **(inferred)**
- `repo_snapshot` — point-in-time repo metadata snapshot (stars, forks, open issues) **(inferred)**
- `room_rollup` — chat-room rollup (messages, threads, authors, time window) **(inferred)**
- `run_shape` — temporal shape of a task-family run (staging date, burst window) **(inferred)**
- `shortener_info_page` — front-page capture of a shortener instance (software/version) **(inferred)**
- `shortener_link` — one shortener link with its resolved chain, grammars and markers **(inferred)**
- `shortlink` — single shortlink row from a link table (target, chain, clicks) **(inferred)**
- `source_reference` — cited source body/URL reference behind a sweep claim **(inferred)**
- `staging_signal`
- `stats_api_target` — candidate stats-API endpoint recorded as a probe target **(inferred)**
- `surface_negative`
- `sweep_negative`
- `tag_liveness`
- `tag_listing`
- `target_probe_rollup` — per-target rollup of wiki probe attempts (proxies used, verdict) **(inferred)**
- `timeline_anchor`
- `transfer_test_paste`
- `tunnel_candidate` — candidate tunnel hostname (provider, embedded IP, evidence) **(inferred)**
- `urlquery_rollup` — rollup of a urlquery lane search (query, total hits, reports retrieved) **(inferred)**
- `venue_finding`
- `venue_probe`
- `verdict` — swarm-marker verdict row for a venue sweep **(inferred)**
- `wayback_capture`
- `web_search_negative`
- `webhook_deaddrop`
- `webhook_deaddrop_candidate`
- `wiki_event`
- `wiki_ioc_pivot`
- `wiki_link`
- `wiki_page_snapshot` — current-state snapshot of a wiki page (body length, SHA) **(inferred)**
- `wiki_poverty_links_page` — worldpoverty task-family wiki page capture (country links) **(inferred)**
- `wiki_record_annotation`
- `wiki_revision`
- `wiki_shortener`
- `wiki_wpc_sequence_page` — worldpoverty sequence page capture (signed/write chain) **(inferred)**
- `worldpoverty_slug` — shortlink slug row for the worldpoverty task family **(inferred)**
- `xss_ssti_payload`
- `yourls_country_hits` — YOURLS stats row: hits by country **(inferred)**
- `yourls_daily_hits` — YOURLS stats row: daily hit-series point **(inferred)**
- `yourls_referrer_url` — YOURLS stats row: one referrer URL with hit count **(inferred)**
- `yourls_stats_detail` — full-detail YOURLS stats-page capture (decimated daily series, referrer rows) **(inferred)**
- `yourls_stats_page`

New kinds are added by the dataset builder and recorded here.

## Layer naming

`event.dataset` is the layer name: one dataset, one Elastic index, one
`data/YYYY-MM-DD-<slug>/` directory (date = first event, see
`collections.md`). Index names equal dataset slugs (date prefix
included).

## Provenance

Every dataset directory carries `PROVENANCE.md` (source, method, identity
string for fingerprints, caveats) and `SHA256SUMS` (checksums of every file
in the directory, verified with `sha256sum -c`).

## Conformance status

The ten datasets rewritten by `scripts/backfill_schema_2026_09_28.py`
(2026-09-28) conform. A second pass (2026-09-29, `temp/backfill_w1..w4.py`)
brought every file loaded directly by the ingest path
(`scripts/local_es_manifest.json` staged files, 74 files) into conformance.
46 non-staged files (raw transform inputs, e.g. collusion-wiki source tables
and `*/raw/` snapshots) still predate the schema and are next in line;
`scripts/validate_schema.py` measures drift.
