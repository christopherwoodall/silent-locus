# PROVENANCE — 2026-10-01 oai-tag / arquivo.pt / markdown.new sweep (lane 4/4)

## Task
BigSexyWarlock69-ordered collection on the Transluce us-canada-gov pivots.
See `~/workspace/silent-locus/notes/transluce-us-canada-gov-2026-10-01.md`.

## Build
- Build script (single-collection convention): `sweep_indicators.py` in THIS dir.
- Run: `python3 sweep_indicators.py` (streams the three frozen exports read-only).

## Sources (all READ-ONLY; nothing modified, nothing merged)
| alias | path | records scanned |
|---|---|---|
| frozen:urlquery-incidents | `~/workspace/muse-home/projects/swarmtraces-hf-corpus/elastic-exports/urlquery-incidents-20260928T022324Z.jsonl.gz` | 51,643 |
| frozen:collusion-wiki | `.../collusion-wiki-20260928T025051Z.jsonl.gz` | 80,434 |
| frozen:rubygems-goimport | `.../rubygems-goimport-campaign-20260928T022324Z.jsonl.gz` | 6,619 |
| transluce-dataset | `~/workspace/transluce-urlquery/urlquery-agent-activity-2026-09-22-v5/all-reports.csv` | 38,160 rows |

Note: the elastic-exports cited in the grading note ARE on disk (found in the
old `swarmtraces-hf-corpus` archive repo). No live API queries were needed.
Sidecar labeling rule: every event carries `source` = `frozen:<alias>` or
`transluce-dataset`; frozen data was never altered.

## Outputs (annotated sidecar, this dir only)
- `events.jsonl` — 96,353 annotated events; fields: source, record_id,
  event_time (full timestamp), indicator_count, indicators[], evidence{},
  url/report links, tags, labels_note. Ranked by indicator_count desc.
  25,699 events fire 2+ indicators (steering: these outrank lone-oai hits).
- `sweep_summary.json` — per-indicator counts per source + score histogram.
- `timeline.json` — per-hit timeline records + per-minute bursts (>=8 hits).
- `temporal_overlaps.md` — hit-days inside known windows; >=2-source days.

## Marker verdicts (verified against bytes)
- **oai_prefix**: frozen urlquery 4 hits = ALL FALSE POSITIVES —
  `OAItest7z645xgm` httpbin probe (May 14), `OAIJS1782002787694412133`
  httpbun probe title (Jun 21), `persistent.oaistatic.com` ChatGPT asset
  domain (Jul 1), `utm_oaid` ad param (Jul 30).
  **Zero genuine Transluce-style oai* agent tags in the frozen urlquery corpus.**
  collusion-wiki 2,026 oai hits = genuine DSE-grammar labels
  (e.g. `dse~OAIFlatheadBridgeTestMay24X@45`, `grammar:oai` tags), wiki-side,
  agent-authored. rubygems 632 = oai gem names (existing watchlist surface).
- **arquivo_pt**: urlquery 1 = scan OF arquivo.pt homepage (2026-09-25),
  NOT relay use. collusion-wiki 8 = Nightingale investigation notes
  documenting our own DataUSA bundle reproduction (Jun 16-17).
  **Zero agent relay-use of arquivo.pt anywhere in our vantage.**
- **markdown_new**: urlquery 11 = 7 tinyurl-chain scans (May 11-13) + 4
  agent-use: `markdown.new/r.jina.ai/...` chains (May 14 datastudio,
  May 17 alexandria.ucsb.edu), `markdown.new/api?url=api.datausa.io`
  (Sep 24, our own reproduction), `markdown.new/https://api.datausa.io/...`
  (May 27). collusion-wiki 2,628 = wiki revisions documenting agent
  markdown.new relay use, Jun-18 burst incl.
  `https://markdown.new/https://www.sec.gov/files/county.json` — same
  MAX.gov/SEC pairing Transluce reports, co-occurring with oai_prefix,
  zz_label, epoch nonces, uniq= nonce params (9-indicator hits, Jun 18).
- **webhook_deaddrop (A000/ZZEND)**: 0 standalone-token hits in the frozen
  exports after false-positive tightening (initial hits were `a000` inside
  UUIDs/sha hex runs). The verified May-12 A000/ZZEND markers live in raw
  gem payload bytes, NOT in these elastic exports — exports cannot answer
  this indicator; do not cite this zero as absence.
- **github_remote_cache_zz**: 0 everywhere (frozen exports).
- **go_import**: 0 urlquery / wiki; 1,867 rubygems (the campaign corpus itself).
- **disposable_email**: 0 everywhere.
- **transluce-dataset**: 9 hits, all epoch_nonce FPs (10-digit ids in
  why_included text). 0 oai/arquivo/markdown markers.
- Low-precision indicators (broad regexes, use indicator_count>=2 to filter):
  file_suffix_antibot, double_slash_path, exposed_key_in_url, epoch_nonce.

## Temporal findings (timestamps first-class, steering)
- collusion-wiki **2026-06-18T20:09–20:10**: 636+665 hits/min (wiki-swarm
  revision storm; oai+zz+markdown+uniq+epoch co-occurring) — lands on the
  BEA/DoE/SEC incident window (Jun 16-18). Jun 16/17/18 hit-days:
  8,611 / 4,591 / 19,515 across sources.
- rubygems **2026-05-12T02:47**: 166 hits/min burst — same date as the
  verified A000/ZZEND webhook-marker wave (all three sources active May 12).
- urlquery **2026-05-11 08:54–09:03**: sustained ~50 hits/min
  (jina/allorigins + file-suffix antibot pairs — the zz-tag swarm season).
- Nov-2025 origin window: 2 urlquery hits (da.gd shortener probes, Nov 17/24),
  thin single-indicator relay activity — earliest relay-use signal in vantage.
- LAC days: May 28 (166 urlquery + 813 wiki), Jun 9 (103 + 18) — wiki-heavy.
- 58 days have annotated hits in >=2 sources (see temporal_overlaps.md).

## Rules compliance
- Read-only on frozen sources: exports opened with gzip streaming, never
  written. Hits are sidecar annotations only (no merge into frozen datasets).
- No invented IDs: every event carries source record _id / report_id / event_id.
- Retry dedupe: this event dir is new; zero pre-existing rows. Re-runs of
  sweep_indicators.py regenerate the sidecar deterministically.
- Agents/infrastructure only; no human/operator attribution attempted.
- SHA256SUMS covers all outputs in this dir (build script included).

## Aggregation into Factum (2026-10-10, BigSexyWarlock69-approved)

96,353 annotated events are NOT ingested 1:1. They are aggregated to
20 Factum records:

- 1 run record (`lane_aggregation`, tool `oai-tag-sweep-aggregate` v1):
  coverage 96,353 annotated events from 138,696 frozen records
  (urlquery-incidents 51,643; collusion-wiki 80,434; rubygems-goimport
  6,619) plus 38,160 Transluce dataset rows (9 hits).
- 1 source record: locator `data/lanes/oai-tag-sweep/events.jsonl`.
- 15 `intel.behavior` observations, one per fired indicator
  (`category` = indicator name). Each carries: pattern definition, verbatim
  marker verdicts from this file, per-source prevalence, first/last seen
  dates, and 2-3 verbatim exemplar evidence snippets from the sweep sidecar.
- 3 OBSERVED claims on the run: sweep_coverage, multi_indicator_rate
  (25,699 events with 2+ indicators = 26.7%; 58 days with hits in 2+
  sources), temporal_distribution (event span 2025-03-04..2026-09-27;
  1,665 burst minutes with >= 8 hits; largest 2026-06-18T20:10Z, 665
  collusion-wiki hits).

Method (`data/lanes/oai-tag-sweep/aggregate.py`, retained):

1. Stream `events.jsonl`; count hits per indicator per source.
2. Independently cross-check totals against `sweep_summary.json`:
   total events (96,353), per-indicator per-source counts, and the
   2+ indicator rate (25,699). All match; assertion failure aborts.
3. Exemplars: rank candidate events per indicator by `indicator_count`
   desc, dedupe identical snippets, then round-robin across sources for
   source diversity (max 3).
4. Bundle builder `data/lanes/oai-tag-sweep/build_factum_bundle.py`
   emits the 20-record bundle (idempotency key
   `oai-tag-sweep-aggregate-v1`); every record carries
   `tags.lane = "oai-tag-sweep"`.

Pre-ingest dedup (2026-10-10): no `intel.behavior` taxonomy for these
indicators existed (only 4 unrelated categories: restriction-circumvention,
software-flaw-exploitation, unauthorized-form-submission,
url-shortener-abuse). Disk scan of all exported `data/records/*/records.jsonl`
plus `data/.local/pending`: `oai_prefix`, `epoch_nonce`, `markdown_new`
exist as `infra.ioc` marker terms in lane `2026-09-05-termina-digital`
(different record type, different lane; kept and annotated via
`tags.also_observed_in_lane`). No duplicate submitted. (Live `match`
queries were unusable during this ingest: lock contention, then a stale
index, then a sibling worker's staged symlink at
`data/lanes/openai-agent-traces/events.jsonl` tripping the store SYMLINK
guard on every command.)

Taxonomy doc: `docs/taxonomy/indicator-taxonomy.md`.
