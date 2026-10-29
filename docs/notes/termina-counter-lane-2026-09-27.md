# Lane L — termina.digital Wayback re-check + counter-channel snapshot (2026-09-28)

## TL;DR

- termina.digital `/db/` is gone live (404), but it was never on the main
  domain in the archive — the incident DB lives on **swarm.termina.digital**,
  and Wayback holds **115 captures** of it (2026-09-05 → 2026-09-18).
  **99 files recovered** — the full incident DB (incidents × campaigns ×
  clusters × venues × actors × trackers).
- The counter channel at **countapi.mileshilliard.com is still live**:
  `langr5backup4813_CA=4`, `_TX=2` (unchanged since 2026-09-04),
  `_ZZ=2` (documented-fake key now carries a value — the channel is being
  poked). 12 sibling-key probes all 404; the key family is exactly these 3.
- Both datasets in their own Elastic indices (`termina-digital`: 107 docs,
  `counter-channel`: 4 docs) under the shared canonical schema.

## termina.digital

### Recovery path

1. `termina.digital/db*` CDX → **zero captures**. The /db/ never lived on the
   main domain in archived form.
2. Blog pages were JS-rendered (empty HTML). The site's archived WASM binary
   (818,387 B, static strings extraction — no execution) embeds the full blog
   markdown; Swarmchasing I/II reveal the DB moved to the subdomain
   `swarm.termina.digital` (`/db/incident/dsewiki-2026-05.html` docket,
   `/db` front page, `swarm.termina.digital` map).
3. `swarm.termina.digital*` CDX (collapse=urlkey) → **115 rows**. Bulk-pulled
   all non-static assets: 99 files OK (7 wayback connection-drops recovered
   on retry; 3 permanent: bogus `/db/index.html)` CDX row, `/db/page/dse/`
   dir artifact, `/db/search.html?q=xinhai` 404-in-wayback).
4. Live probes: `swarm.termina.digital/` → 200 (WASM map app shell);
   `/db/` → 404; `/db/llms.txt` → 503 "public exports are temporarily
   unavailable". Wayback is the only source.
5. archive.today unreachable from this network (timeout) — Wayback-only.

### What's in the DB (schema v10, data through 2026-09-07T23:08)

- **6 incidents**: aisi-2026-07, artifactory-2026-05, dsewiki-2026-05,
  hf-2026-07, modal-2026-07, usemod-envelopes-2026-08.
- **11 clusters** (task families): aihw-pbs, bulgarian-nsi, datausa-cooks,
  datausa-sequence, ihme-health, iowa-cancer, oecd-equity, paste-qa-early,
  sec-county-json, texas-poverty, xinzhai-store.
- **7 campaigns**: artifactory-swarm, paste-qa-early, swarm-cohort,
  swarm-retrieval, usemod-fleet, visitors, xinzhai-2026-07.
- **17 venues**: anna-fyi, apchem, bitily, dse, 3× ludism wikis, 5× paste
  hosts (nervesocket, nosupamu, smirky, ubuntu-cn, wjake), **rmn-re**,
  usemod-org, 3× ws-dict wikis.
- **24 agent-handle actor pages** (dse), 13 dse wiki-page records, 3 trackers
  (thecolony, she-llac cross-site pack, ai-safety-lab).
- API documented at `/db/api/*.json` — **never captured by Wayback** (HTML
  only). `graph.json` and `search/index.json` recovered.

### Corpus diffs (independent corroboration)

- **rmn-re venue**: DB census 600 shortlink rows, June 2026 = 484 — our crawl
  found +484 June links and 764 total (Sept 28). DB: "106 of 123 /16s that
  created rmn.re shortlinks are /16s seen editing the wikis, covering 494 of
  540 links; top ones azure 20.x — the shortener and the wikis ran on the
  same networks." Independent confirmation of the shortener↔wiki IP linkage.
  DB also notes post-disclosure visitors (thecolony invitation 09-05,
  public-board llms.txt 09-06) in its census.
- **anna-fyi venue**: DB: 136 pastes lifetime, 60 in the NSI statistical
  reference series (2026-05-27). Our paste-archive: 55 anna.fyi pastes, 50
  templated NSI references. Close; DB census is the fuller number.
- **Actor pages** document the 2026-06-18 SEC county bridge event forensically:
  per-handle edit chains with proxy ladders
  (md.succ.ai → proxymule → urltomarkdown → allorigins).
- **she-llac tracker**: "friend of rowan; also the rubygems lead" — she-llac
  is the origin of the RubyGems go-import lead.
- **ai-safety-lab tracker**: "iowa-shortlinks: fifteen is.gd, **da.gd** and
  tinyurl links, all to the idph AnnualThyroidCancer csv" — da.gd appears
  here independently (our three-corpus pivot).

### Pattern battery (99 recovered pages)

zz-words 227 · oai-prefixed 581 · epoch nonces 1279 · md.succ.ai 94 ·
jqp 53 · allorigins 82 · proxymule 51 · r.jina.ai 9 · markdown.new 8 ·
webhook 4 · da.gd 7 · is.gd 12 · bitily 32 · rmn.re 18 · vanderbi.lt 8 ·
countapi 7 · go-import 0 · chunk markers 0 · gmail 0. The DB is dense with
the campaign toolkit; go-import/webhook/chunk-marker grammars absent from it
(mechanism boundary holds).

### Negatives

- `pub/datasets/agent-pastes-2026-09-08.tar.gz`: 503 live and in Wayback.
- Structured `/db/api/*.json`: never archived.

## Counter channel

- `langr5backup4813_CA=4`, `_TX=2` — unchanged since the 2026-09-04
  investigator report. `_ZZ=2` — the documented-fake key now carries a value.
- Sibling probe (read-only GET, 12 candidates incl. bare key and 10 state
  suffixes): all 404. No `/api/v1/info/` or `/api/v1/namespace/` endpoints
  on this countapi clone.

## Elastic

- `termina-digital`: 107 docs (99 wayback files + 5 aux captures + 3
  negatives), verified count + `event.dataset.keyword` + kind breakdown.
- `counter-channel`: 4 docs (3 readings + 1 probe), verified.
- Scripts: `scripts/es_ingest_termina.py`, `scripts/es_ingest_counter.py`
  (`--create/--load/--verify`). Note: `notes/gems-es-mapping.json`'s
  `index` key is the index NAME (string), not settings — create with
  `{"mappings": m["mappings"]}` only (same pattern as other ingest scripts).

## Files

- `data/termina-digital/` — wayback/ (99 files), wayback_manifest.json,
  CDX dumps, PROVENANCE.md, sweep.json, aux captures.
- `data/counter-channel/` — snapshot_2026-09-27.json, PROVENANCE.md.
