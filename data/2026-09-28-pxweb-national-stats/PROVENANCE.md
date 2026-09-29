# PROVENANCE — Lane N: national-statistics-API task targets

**Lane:** N (2026-09-28 night watch) — "Vietnam PX-Web / national-stats APIs as agent task targets"
**Dataset dir:** `data/2026-09-28-pxweb-national-stats/` (project-relative)
**Collector:** hunt night-watch agent (read-only research; no submissions, logins, or target enumeration beyond public docs roots)

## Sources (all read-only, existing corpora + live public docs surfaces)
1. `data/2026-09-27-rmn-re/raw/link_table_decoded_2026-09-27.json` (764 slugs) — 4 agent-created rmn.re shortlinks to the UK ONS Cantabular API (`api.beta.ons.gov.uk/v1/datasets/TS030*`), click counts 44/36/33/30. Ingested in ES index `rmn-re-linktable`.
2. `data/2026-05-17-collusion-wiki/raw/links.jsonl` + ES `collusion-wiki` index — DataUSA tesseract API mentions (1,914 `data.jsonrecords` calls), US Census Bureau API mentions (125 docs, 94 `api.census.gov`), Statistics Iceland PX-Web table URL (`px.hagstofa.is`) from `paste.probyte.ee/view/e48589b5` ("Links for research").
3. `data/aggregates/2026-05-26-proxy-primitives/events.jsonl` + ES `proxy-primitives` index — 3 pure.md-laundered `api.datausa.io/tesseract/data.csv` (ipeds_admissions cube) hits from lane-f wiki IOC pivots (6 dse-wiki Clark-family agents).
4. `data/2026-09-28-university-shorteners/raw/goto-unm-edu/7t6-o_stats_2026-09-28.txt` — `pxweb.nso.gov.vn` (Vietnam General Statistics Office PX-Web) as HTTP referrer on the goto.unm.edu/7t6-o+ stats page (proxied via jqp/pure.md/md.succ.ai/r.jina.ai; peak 2026-06-18).
5. Live read-only HEAD/GET probes of public documented API roots only (docs surfaces, no user-content enumeration): `https://api.beta.ons.gov.uk/` (200 JSON), `https://api.datausa.io/` (302 → public Tesseract docs UI at /ui/), `https://px.hagstofa.is/pxen/` (302 → live public PxWeb UI "PxWeb - Select database").

## Schema
Canonical shared schema: `notes/gems-es-mapping.json` (`record_kind: stats_api_target`; detail in `labels` (flattened) + `tags`; `event.dataset.keyword` multi-field declared at index creation). Zero top-level fields beyond the mapping.

## Selection basis
Task-or-exchange signal: stats-API venues used by agents across corpora (US Census family, UK ONS Census 2021, Vietnam/Iceland PX-Web, DataUSA tesseract), plus one explicit negative-sweep record of theory-of-mind predicted venues with zero hits.

## Elastic index
`pxweb-national-stats` — created from the canonical mapping; docs bulk-loaded from `hits.jsonl`; `_count` verified; top-level field hygiene checked against the mapping (no extras).

## Limitations
- Click counts on rmn.re shortlinks prove usage of the shortlinks, not which downstream agent clicked (bots and humans both click).
- Negative sweep covers only the 8 listed indices; absence of evidence, not evidence of absence.
- No operator-identity fields retained (creator_ip16 present in source but not copied — out of scope by hunt rule).

## Closure 2026-09-28 (workstream D)

Bounded venue sweep complete: pattern-level sweep for national-stats APIs as
agent task targets across 8 ES indices + live docs probes. N=12 docs
(stats_api_target) is the full hit list — 11 named surfaces tested, the
headline-API predictions all NULL (recorded as negatives elsewhere; lane S
then confirmed the venue model with long-tail APIs). ES
`pxweb-national-stats` _count=12 verified. Nothing further to pull.
