# Dir triage — worker W7 (2026-09-29)

Read-only survey of the four top-level `data/` support dirs, plus build notes.
Nothing moved, renamed, or restructured.

## (a) Survey

### data/aggregates/ — 4 dated dirs (analysis outputs, not raw captures)
- `2025-09-26-cors-bwa-proxy/` (16 files: PROVENANCE.md, SHA256SUMS, raw/) —
  night-watch lane: `*.cors.bwa.workers.dev` proxy-primitive records pulled from
  the project's Elastic Cloud deployment; ES index `cors-bwa-proxy` (154 docs).
  PROVENANCE still says "**Dataset:** `data/cors-bwa-proxy/`" though no such
  top-level dir exists — stale/planned reference.
- `2026-05-26-proxy-primitives/` (3 files: PROVENANCE.md, SHA256SUMS, events.jsonl) —
  Lane F toolkit-hunt sweep of longcat's 207-domain proxy primitives
  (pure.md, api.cors.lol, corsmirror.com, gview) across hunt corpora.
- `2026-09-28-gem83-reconciliation/` (7 files: PROVENANCE.md, SHA256SUMS, raw/) —
  Lane E: independent reconstruction of the 83-gem June-18 GemStuffer segment,
  cross-referenced against three project sources.
- `2026-09-29-overlap-analysis/` (8 files: PROVENANCE.md, SHA256SUMS, events.jsonl, raw/) —
  support collection of cross-corpus overlap/pivot analysis outputs
  (F1/F2 marker matches etc.); explicitly NOT loaded to Elasticsearch.

### data/processed/ — 1 entry
- `gems/` (964 subdirs, one per `<name>-<version>`) — extracted contents of the
  reconstructed GemStuffer `.gem` tarballs (`a.gemspec`, `evil.rb`, `lib/`, …);
  derived build artifact of `data/raw/gems/`. (Spot-peek: one dir contained a
  nested second `.gem` file — extraction captured inner archives.)

### data/site-captures/ — 33 per-site dirs
- One dir per agent-board/venue host (`bboard.ai`, `swarmmemo.com`,
  `agenttavern.dev`, …). Each holds `surface_capture.json`
  (url, http_status, retrieved_at_utc, sha256, bytes, content_preview) plus a
  `_body.txt`; most targets are `/llms.txt`. Uniform shape, no events.jsonl,
  no per-site PROVENANCE.

### data/raw/ — 5 entries (corpus roots + gem tarballs)
- `MANIFEST.json` (11 keys) — publication manifest for the SwarmTraces HF
  redacted dataset (article 2026-09-25, "over 80,000 reassembled attack payloads"
  claimed; observed 189,579 records).
- `redacted.jsonl.gz` (~15 MB) — the 189,579-record redacted SwarmTraces dataset
  itself (91,037 payload + 23,008 response + 75,534 recovered_text).
- `swarmtraces_provenance.json` — dataset-level provenance record.
- `gems/` (618 `.gem` files) — reconstructed GemStuffer tarballs (our own
  collection per the 2026-09-27 provenance correction; kept separate from
  SwarmTraces).
- `gems-excluded/` (4 `.gem` files, e.g. `rgscan_s4_*`) — tarballs excluded
  from the corpus, reason not recorded in the filename.

## Decision-needed items (for Christopher)

1. **aggregates/ vs data/ layering.** `aggregates/` dirs use the dated-dataset
   shape (PROVENANCE.md + SHA256SUMS + raw/, two with events.jsonl) but sit
   outside the `data/YYYY-MM-DD-<slug>/` convention and the ES ingest path.
   Is `aggregates/` a permanent support layer, or staging for promotion into
   dated dataset dirs? Related: `2025-09-26-cors-bwa-proxy` and
   `2026-09-28-gem83-reconciliation` have `raw/` but no `events.jsonl` —
   normalize them, or leave as analysis-only?
2. **data/raw/ corpus-root placement.** The SwarmTraces redacted corpus
   (`redacted.jsonl.gz` + MANIFEST + provenance) lives at `data/raw/` while
   every other dataset is a dated dir. Intentional canonical home, or should it
   move under a dated dataset dir? Same question for `raw/gems/` vs the dated
   rubygems dataset dir (tarballs in one place, dataset records in another).
3. **site-captures/ normalization candidate.** 33 uniform captures, no event
   records. One record per capture (`surface_capture.json` + body) would fit a
   future sweep — or leave as support material. Your call.
4. **processed/gems/ retention.** 964 extracted dirs duplicate `raw/gems/`
   tarballs in unpacked form. Keep as build artifact, or drop as redundant?
5. **Stale dataset reference.** `aggregates/2025-09-26-cors-bwa-proxy/PROVENANCE.md`
   names `data/cors-bwa-proxy/` as the dataset location; no such dir exists.

## (b) New record_kinds

None. All three built dirs used existing registry kinds:
`artifact_observation` (jsonhero-docs), `venue_probe` (ludism-wikis),
`relay_paste` (paste-linuxiarz). No registry additions needed.

## (c) BLOCKED dirs

None. All three assigned dirs built cleanly:
- `2026-09-28-jsonhero-docs`: 12 records (commit 3491944)
- `2026-09-28-ludism-wikis`: 29 records (commit ad189cb)
- `2026-05-26-paste-linuxiarz`: 131 records (commit 31c3bb2)

Verification per dir: `scripts/validate_schema.py` exit 0 (172 records, 0
violations); `sha256sum -c SHA256SUMS` all-OK from inside each dir;
3-row spot-checks against raw by hand; fingerprint function proved against the
`TheNacken/python-cors-proxy` reference before building.
