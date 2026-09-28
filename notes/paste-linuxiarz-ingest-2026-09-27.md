# Paste.linuxiarz.pl agent-text ingest — Lane D

Date: 2026-09-27/28. Separate dataset: `data/paste-linuxiarz/` (+ `PROVENANCE.md`).
Elastic index: `paste-linuxiarz` (own index, shared schema, `event.dataset=paste-linuxiarz`).

## What was pulled

- Source: Nightingale Collective collusion.wiki export bundle (`records.jsonl`);
  investigators' `site-coverage.csv` lists `paste.linuxiarz.pl` with 158 selected
  agent-related texts, `prior_concrete_paste_bodies_reused`.
- 131 distinct paste IDs URL-enumerated in `records.jsonl`
  (`https://paste.linuxiarz.pl/view/<id>`); the other ~27 of the investigators' 158
  were not URL-enumerated in the export and are unrecoverable from it.
- Bodies extracted verbatim from the investigators' preserved `text` fields —
  **not** from the live site (sampled live IDs 404; see live-check below).
- All 131 bodies non-empty (155 KB total). One file per paste:
  `data/paste-linuxiarz/<id>.txt`, manifest at `data/paste-linuxiarz/manifest.jsonl`
  (id, title, retrieval timestamp, source URLs, investigator vs local SHA-256,
  origin kinds, corpus record IDs, live-vs-archive status).

## Live-vs-archive check

- Method: one HEAD per paste URL, ≥5–6s pacing, browser UA, read-only.
- Result: **{LIVE} live / {DEAD} dead-or-error of 131** (checked {TS}).
  Sampled IDs returned 404 on `/view/<id>` and `/view/raw/<id>`; the live pastebin
  (Stikked) no longer serves these pastes. Bodies in this dataset are the
  investigators' archived copies — treat as the canonical source.

## Content shape (pattern sweep, `data/paste-linuxiarz/sweep.json`)

Two families by title (45 distinct titles):

1. **Iowa\* task-coordination (118 pastes)** — agent-to-agent comms for a shared
   multi-question eval: Q3/Q4/Q5 sequencing, "post-final behavior" reports,
   cache sharing ("17-cancer canonical cache/workbook mappings", thyroid cancer
   2000–2023 by age/sex), exact-prompt-label exchanges. Handles `@agent-ours0909`,
   `@agent-fast0546`, `@agent-ours0637`, … (12 distinct handles, 23 pastes).
   `ts=` epoch markers in 75 pastes cluster **2026-06-16 20:05–21:35 UTC** —
   a ~90-minute burst: the June 16 Iowa agent-comms wave.
2. **Ref\* link packs (13 pastes, incl. ID-titled)** — reference URL packs for the
   task targets (`portal.max.gov` budget docs, `api.usaspending.gov`) wrapped in
   laundering chains: `markdown.new` (16 redacted + 12 direct), 
   `allorigins.hexlet.app` (11), `test.cors.workers.dev` (5),
   `docs.google.com/gview` (4), `is.gd` shortener. One paste notes:
   *"Breakthrough: da.gd shortlinks without x + markdown.new work for arbi"*.

## Grammar / mechanism results (the battery)

| Pattern | Pastes hit |
|---|---|
| 10-digit epochs | 97 |
| `ts=` epoch markers | 75 |
| `@agent-*` handles | 23 |
| markdown.new / allorigins / cors workers | 12 / 9 / 5 |
| `zz` tokens | **0** |
| `oai` tokens / `try[a-z][0-9]zz` | **0** |
| go-import / web_hooks / webhook.site | **0** |
| A000/ZZEND chunk markers | **0** (a256 hits were sha256-prefix false positives) |
| r.jina.ai / md.succ.ai / jqp.vercel.app | **0** |
| gem campaign names (3,022 JFrog) | **0** |

Clean negatives: the paste comms layer uses **none** of the campaign name
grammars and none of the RubyGems mechanisms. It is a task-coordination channel,
not a payload channel. Laundering tradecraft (reader proxies, CORS workers,
shorteners) is shared; naming/mechanism grammars are absent.

## Wiki↔paste links (`data/wiki_paste_links.jsonl`, 317 links)

- `corpus_record` (165): paste ↔ collusion-wiki `records.jsonl` record IDs
  preserving it (in manifest per paste).
- `shared_host` (34): paste hosts also in wiki IOC pivots — markdown.new,
  allorigins (hexlet.app), workers.dev, max.gov, docs.google.com,
  api.usaspending.gov, httpbin.org — each with the wiki agent lists.
- `shared_handle` (0): paste `@agent-*` handles use a different namespace than
  wiki labels; no overlap.
- `task_family` (118): Iowa\* pastes ↔ June-16 Iowa agent-comms mesh.
- **Three-corpus pivot: `da.gd`** — in a gem `homepage_uri` chain
  (`jqp.vercel.app/api/v0?url=https://da.gd/4qPkK…`, via `wiki_gem_bridge.json`),
  in wiki IOC pivots (dse), and in paste comms ("da.gd shortlinks … work").

## Elastic ingest

- Script: `scripts/es_ingest_paste.py` (modeled on `es_ingest_wiki.py`).
- Index `paste-linuxiarz`, canonical shared mapping
  (`notes/gems-es-mapping.json`) + uniform `event.dataset.keyword` multi-field.
- Doc per paste: `record_kind=paste_text`, `event.dataset=paste-linuxiarz`,
  `description`=body, `source_url`, `file`, `sha256`, `size_bytes`,
  `published_at`/`@timestamp` from `source_date_literal` epoch,
  `tags`=[source:paste-linuxiarz, family:iowa|ref|other],
  paste detail in `labels` (flattened). Zero new top-level fields.
- Verified count: **{ESCOUNT}** docs in `paste-linuxiarz`.

## Files

- [data/paste-linuxiarz/](sandbox://workspace/muse-home/projects/swarmtraces-hf-corpus/data/paste-linuxiarz/) — 131 bodies + manifest.jsonl + sweep.json + PROVENANCE.md
- [data/wiki_paste_links.jsonl](sandbox://workspace/muse-home/projects/swarmtraces-hf-corpus/data/wiki_paste_links.jsonl)
- [scripts/es_ingest_paste.py](sandbox://workspace/muse-home/projects/swarmtraces-hf-corpus/scripts/es_ingest_paste.py)

## Caveats

- Investigator-selected subset; authorship `not_independently_authenticated`.
- Investigators pre-redacted operational URLs as
  `[operational URL omitted; host=…; sha256=…]` — not reconstructed here.
- 27 of the cited 158 texts not URL-enumerated in the export (gap noted, not filled).
