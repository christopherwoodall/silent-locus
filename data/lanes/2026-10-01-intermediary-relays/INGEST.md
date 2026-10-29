# INGEST — 2026-10-01-intermediary-relays into Factum

Ingest date: 2026-10-10. Corpus rebuild lane ingest.
Builder: `build_bundle.py`. Cleaner: `clean_bundle.py` (0 fixes needed).
Validator: `validate_bundle.py` — PASS (34/34 checks).

## Record mapping (legacy record_kind -> Factum type)

| legacy kind (count) | Factum type (count) | note |
|---|---|---|
| relay_score (17) | infra.proxy_instance (16) | api.cors.lol skipped: proxy_instance already in corpus (lane proxy-fresh-blood) |
| indicator_census (18) | infra.ioc (17) | term = the sweep_v3.py regex (the real searchable value, not the internal indicator name); category marker; status candidate. `allorigins` skipped: ioc already in corpus (lane 2026-09-05-termina-digital) |
| relay_mention_sample (3000) | infra.proxy_chain (part of 1101) | only lines carrying a concrete relay-invocation URL; 437 fragment-only lines (e.g. `"wrapper": "markdown.new"`) dropped from structured ingest, preserved in raw events.jsonl |
| relay_ts_sample (519) | infra.proxy_chain (part of 1101) | joined via link.slug to full shortener_link records in lane 2016-12-28-rmn-re; real @timestamps kept as observed_at |
| (live probes, PROVENANCE.md) | reachability.check (6) | 5 response + 1 blocked (r.jina.ai, sandbox fetch policy) |
| (sweep run) | run (1) | run_kind indicator_sweep, tool sweep_v3.py |
| (lane sources) | source (1) | locator data/lanes/2026-10-01-intermediary-relays/ |

Total submitted: 1142 records. Intra-batch dedup on (proxy_service,
target_url) merged mention/ts passes per the multi-pass rule (ts evidence
wins ties). 42 candidate chains collided with existing corpus
(proxy_service, target_url) pairs and were dropped. Zero retractions.

## Extraction notes

- Chain extraction runs on a JSON-unescape + triple percent-decode copy of
  the sample line: relay URLs are often URL-encoded inside wrapper-service
  query strings (jqp.vercel.app/api/v0?...&url=https%3A%2F%2Fmd.succ.ai%2F...).
  The decoded inner relay URL becomes target_url; the original verbatim
  line is kept in tags.verbatim.
- proxy_service is the leftmost relay host of the extracted URL; `chain`
  lists stacked relays in order (e.g. allorigins.hexlet.app ->
  markdown.new -> web.archive.org).
- mention-sample observed_at: inner record @timestamp when present and not
  1970-01-01, else the sweep execution date 2026-10-01 (tagged
  timestamp_source=fallback:dir_date_prefix). No invented event times.
- double_slash ioc: rg census recorded 0 lines/0 files (lookbehind
  unsupported); the Python pass hits are noted in tags.census_note.

## Dedup decisions (pre-ingest, against exported batches)

- api.cors.lol proxy_instance: exists (proxy-fresh-blood) -> skipped, noted.
- `allorigins` ioc term: exists (2026-09-05-termina-digital) -> skipped, noted.
- 42 chains: (proxy_service, target_url) already in corpus -> dropped.
- Corpus DB was lock-contended by a sibling worker; dedup ran against the
  immutable exported batches (data/records/*/records.jsonl) per the
  2026-10-10 AGENTS.md lesson.

## Files

- bundle.raw.json — builder output; bundle.json — cleaned (submitted);
  drop_log.json — skips/drops; cleaning_report.json — cleaner report.
- build_bundle.py, clean_bundle.py, validate_bundle.py — lane tooling.
- events.jsonl, sweep_*.json, sweep_*.txt, sweep_*.py, build_events.py,
  PROVENANCE.md, WRITEUP.md, SHA256SUMS — original lane artifacts (moved
  here from evidence/2026-10-01-intermediary-relays/).
