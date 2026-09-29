# PROVENANCE — Lane S: open-data-API task-venue sweep

**Lane:** S (2026-09-28 night watch) — "Test the venue-model prediction: do agent corpora reference open-data / national-stats API hosts?"
**Dataset dir:** `data/open-data-api-venues/` (project-relative)
**Collector:** hunt night-watch subagent (read-only research; corpora on disk only; no API crawling, no submissions)

## Verdict

The venue-model prediction **confirmed**, with two surprise venues beyond the predicted list:

1. **`api.worldpoverty.io` (World Poverty GraphQL API)** — 15 agent-created rmn.re shortlinks (slugs `wpccite2018x`, `wpcfinal20186539`, `wpcfinal20206539`…, created 2026-06-22 00:17–00:22, 65–69 clicks each); 3 dse-wiki "Poverty Links" pages (`AgentPovertyDataNEWX`, `AgentPovertyDataZ`, `AgentNextRawJuneAE`) embedding proxymule-laundered GraphQL queries with an identical parameterized template (year 2018/2020 variants, countries AFG/GHA/NGA/IND/MEX); a live `WorldPovertyClockSequenceJun19` sequence-coordination task page cross-cited by IHME family-planning agents; 15 distinct URL templates in the wiki shortener log.
2. **`api.dataafrica.io` (DataAfrica API, DHS health data)** — 10 rmn.re shortlinks (`rwhealthx`, `rwhealthx92`, `agdsoftest` with epoch grammar; created 2026-06-17/20); 2 dse-wiki task pages (`DataAfricaHealthMozambiqueYearsApr15OAI`, `DataAfricaRainfedMozambiqueCoordOAI`, page family `dataafrica-health-stunting`); 6 wiki records showing LIVE timed exact-value retrieval tasks (parallel cohorts, task-clock timers, cooldowns; e.g. Mozambique stunting 21.1% / 23.8%); 8 distinct URL templates in the wiki shortener log.
3. **`www.nationsreportcard.gov` (US NAEP education data service)** — 5 rmn.re shortlinks (`nrcnaepres9983`, `jw`, `jx`; created 2026-06-13); 5 distinct parameterized `GetAdhocData.aspx` templates in the wiki shortener log.
4. **`api.beta.ons.gov.uk` (UK ONS Cantabular API, Census 2021)** — corroborating evidence only (3 rmn.re shortlinks + 3 shortener-log templates); the venue itself is already covered by lane N's `pxweb-national-stats` index (12 docs). Tagged `covered-by:pxweb-national-stats` here.

**Unconfirmed candidates:** `api.usa.gov` and FBI UCR appear only in a vanderbi.lt stats-leak referrer note (no direct agent-grammar evidence yet) — recorded as candidates, not confirmed venues.

**Predicted-list negatives (clean on disk):** `api.worldbank.org`, `databank.worldbank.org`, `data.worldbank.org`, `ec.europa.eu/eurostat`, `data.un.org`, `api.statcan.gc.ca`, `www150.statcan.gc.ca`, `api.insee.fr`, `stats.oecd.org`, `api.ons.gov.uk` (literal host — only the beta variant appears). Corroborates lane N's ES negative sweep. (`eurostat` matched only a Go module path name in gomod-hunt — not agent usage.)

## Sources (all read-only, existing corpora)
1. `data/rmn-re/link_table_decoded_2026-09-27.json` (764 slugs) — 30 agent-created shortlinks to the four venues.
2. `data/collusion-wiki/links.jsonl` — 2 worldpoverty links (proxymule-laundered, `link_in_selected_agent_related_text`).
3. `data/collusion-wiki/revisions.jsonl` — 4 worldpoverty task-page revisions (3 Poverty Links + WorldPovertyClockSequenceJun19).
4. `data/collusion-wiki/pages.jsonl` — 2 dataafrica task pages (health-stunting family).
5. `data/collusion-wiki/records.jsonl` — 6 dataafrica retrieval-task records.
6. `data/collusion-wiki/shortener-logs.json` — 65 venue-URL strings across the four hosts.
7. `data/thecolony-ai/search/jina.json` — agent-board reference (Vera DIADE: worldpoverty/dataafrica).
8. `data/vanderbilt-shortener/web_mentions.json` — stats-leak referrer note.
9. Paste corpora (`paste-archive`, `paste-linuxiarz`, `iowacollab-pastes`) and shortener stats files (`university-shorteners`, `university-shorteners-batch2`): clean, no venue hits.

## Schema
Canonical shared schema: `notes/gems-es-mapping.json` (`record_kind: api_venue_target`; detail in `labels` (flattened) + `tags`; `event.dataset.keyword` multi-field declared at index creation). Zero top-level fields beyond the mapping.

## Elastic index
`open-data-api-venues` — created from the canonical mapping; docs bulk-loaded from `hits.jsonl`; `_count` verified against JSONL line count; top-level field hygiene checked against the mapping (no extras).

## Limitations
- Click counts on rmn.re shortlinks prove usage of the shortlinks, not which agent clicked (bots and humans both click).
- No operator-identity fields retained (creator IPs present in source but out of scope — not copied).
- api.usa.gov / FBI UCR remain candidates only; no agent-grammar evidence on disk.

## Closure 2026-09-28 (workstream C)

Closed: venue-model sweep complete — 46 docs across the four confirmed task
venues (api.worldpoverty.io, api.dataafrica.io, nationsreportcard.gov,
api.beta.ons.gov.uk) plus corroborating and predicted-negative records.
api.usa.gov / FBI UCR remain candidates only (lane T null verdict, no index —
not re-litigated). Nothing further retrievable from on-disk corpora; live API
crawling was out of lane scope. ES `open-data-api-venues` _count=46 verified,
schema-drift clean.
