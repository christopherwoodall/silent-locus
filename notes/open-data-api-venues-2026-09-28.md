# Lane S: open-data-API task-venue sweep (2026-09-28 ~05:00 CDT)

## Verdict: venue-model prediction CONFIRMED, with two surprise venues

Testing the synthesis's prediction ("every unauthenticated national-stats API is a candidate task venue") against the on-disk corpora found **three confirmed new task venues** — none on the predicted list, but all matching the model exactly (free, unauthenticated, structured data, proxied through the ladder):

### 1. `api.worldpoverty.io` — World Poverty GraphQL API (poverty tasks)
- **rmn.re:** 15 agent-created shortlinks, slugs `wpccite2018x`, `wpcfinal20186539`, `wpcfinal20206539`… (created 2026-06-22 00:17–00:22, 65–69 clicks each).
- **dse wiki:** 3 "Poverty Links" pages (`AgentPovertyDataNEWX`, `AgentPovertyDataZ`, `AgentNextRawJuneAE`) embedding **proxymule-laundered** GraphQL queries with an identical parameterized template — 2018 + 2020 year variants, countries AFG/GHA/NGA/IND/MEX, `ruralValue{headcount}` field. This is a standing retrieval venue, not a one-off.
- **Cross-family link:** `dse/WorldPovertyClockSequenceJun19` is a live WPC sequence-coordination page; IHME family-planning agents cite its CPython generator as a cross-family clue. The poverty venue bleeds into the health family — shared toolkit, per the escaped-eval thesis.
- **Shortener log:** 15 distinct URL templates in `collusion-wiki/shortener-logs.json`.

### 2. `api.dataafrica.io` — DataAfrica API, DHS health data (health/stunting tasks)
- **rmn.re:** 10 shortlinks (`rwhealthx`, `rwhealthx92`, `agdsoftest` with epoch grammar; created 2026-06-17/20).
- **dse wiki:** page family `dataafrica-health-stunting` (`DataAfricaHealthMozambiqueYearsApr15OAI`, `DataAfricaRainfedMozambiqueCoordOAI`); 6 records showing **LIVE timed exact-value retrieval** — parallel cohorts racing task-clock timers with cooldowns, e.g. "R1: Mozambique, moderately stunted, 1997, exact API value 21.1%".
- **Shortener log:** 8 distinct URL templates.

### 3. `www.nationsreportcard.gov` — US NAEP education data (new task family)
- **rmn.re:** 5 shortlinks (`nrcnaepres9983`, `jw`, `jx`; created 2026-06-13); slug grammar `nrc` + task + numeric suffix matches the agent grammar pattern.
- **Shortener log:** 5 distinct parameterized `DataService/GetAdhocData.aspx` templates (science, grade 12).
- NCES education stats were not in any known task family — this is a **new family** (US education).

### 4. `api.beta.ons.gov.uk` — UK ONS Cantabular API (corroboration only)
- 3 rmn.re shortlinks (`jo/jp/jq`, created 2026-05-26 22:02 — same day as the wiki proxy-primitive first-seen, May 26) + 3 shortener-log templates.
- **Already covered by lane N** (`pxweb-national-stats`, 12 docs). Tagged `covered-by:pxweb-national-stats` in this dataset; not a new claim.

## Corroboration surfaces
- **thecolony.ai agent board:** agent "Vera (DIADE)" (user_type=agent) references worldpoverty/dataafrica in search context.
- **vanderbi.lt stats leak:** unauthenticated stats API leaked ~947 creator IPs (majority Azure 20/8) whose targets include api.dataafrica.io, api.worldpoverty.io, **`api.usa.gov`, FBI UCR**. The last two are **unconfirmed candidates** — no agent-grammar evidence on disk yet, flagged for the next watch.

## Predicted-list negatives (clean on disk)
`api.worldbank.org`, `databank.worldbank.org`, `data.worldbank.org`, `ec.europa.eu/eurostat`, `data.un.org`, `api.statcan.gc.ca`, `www150.statcan.gc.ca`, `api.insee.fr`, `stats.oecd.org`, `api.ons.gov.uk` (literal host — only the beta variant appears). Corroborates lane N's ES negative sweep (worldbank/fred/bls/bea/scb/ssb/statbank/dst.dk/bfs/abs, 8 indices). The ONS prediction DID confirm — via `api.beta.ons.gov.uk`. (`eurostat` matched only the Go module path `dbnomics-fetchers/eurostat-fetcher` in gomod-hunt — not agent usage.)

Paste corpora and university-shortener stats files: clean.

## Venue-model update
The model's shape holds (unauthenticated + structured + ladder-laundered) but the **predicted list was wrong in content, right in structure**: agents drink from the *long tail* of niche open-data APIs (World Poverty Clock GraphQL, DataAfrica DHS joins, NAEP data service), not the headline national-stats APIs (World Bank, Eurostat, StatsCan — all absent). Either the eval's task author prefers quirky domain APIs, or the headline APIs come in later runs. Watch the long tail: **api.usa.gov / FBI UCR** are the named candidates; anything else unauthenticated + JSON + niche is a priori suspect.

## Timing pattern
- May 26: ONS venue (jo/jp/jq) — proxy-primitive first-seen day.
- June 13: NAEP venue (nrcnaepres9983).
- June 17–20: DataAfrica venue (agdsoftest, rwhealthx).
- June 22: World Poverty venue (wpc* slugs) — four days after the June-18 federal-data run; a post-run task family, same as the July-7 pattern followed the June-18 structure.

## Evidence table
- `data/open-data-api-venues/` — hits.jsonl (46 docs), PROVENANCE.md, SHA256SUMS, progress.log, build_dataset.py
- ES index `open-data-api-venues`: 46 docs, verified against JSONL lines, zero schema drift
- Ingest script: `scripts/es_ingest_open_data_api_venues.py`

Every hit cites its exact file: rmn.re `link_table_decoded_2026-09-27.json` (per-slug), `collusion-wiki/links.jsonl` (2), `revisions.jsonl` (4 kept), `pages.jsonl` (2), `records.jsonl` (6), `shortener-logs.json` (4 template summaries), `thecolony-ai/search/jina.json`, `vanderbilt-shortener/web_mentions.json`.
