# FORAGER: Novel data-collection verticals — collusion-wiki + fake-org corpora

**Task:** mine the two corpora for data verticals agents collect beyond the known workloads.
**Date of analysis:** 2026-10-04. **Sources:** `collusion-wiki/` (pages/revisions/links/records, publisher export, 5 wikis),
`silent-locus/collections/fake-org/data/hits.jsonl` (5,862 hits: 3,181 `openai_research`, 2,673 `oai_prefix_tag`).

**Known workloads (excluded from "novel"):** Amap/gaode maps+POI, IDPH/AIHW health, museum enumeration,
UNCTADstat trade stats, Thai NSO labor stats, DataUSA IPEDS/education stats, SEC EDGAR county.json.
Note: many "known" verticals (DataUSA poverty, SEC county.json) dominate the corpora; only the NOVEL ones below.

**Cross-cutting mechanic (all verticals):** the wikis host a live coordination game — timed task rounds
(R1→R5) with ~20–35 min post-deadline cooldowns, ~21s answer timers, and "ahead cohort" relay requests.
The verticals below are the *data targets* those rounds query. Agent labels follow the
`OpenAI<Vertical><Month><Day><Role>` / `OAI<nonce>` grammar; data URLs are routinely YOURLS-tagged
(`oaicbs220`–`oaicbs227`, `oaifas8005new9`, `OAICLIM729`, `oaihhsxlsx2023new9`).

---

## 1. Stock market data (Yahoo Finance) — NEW
- **dse `AgentMarketYahooResearchExtra2020`** (first write 2026-06-07, 2 revs): month-by-month 2020
  AMZN historical prices via `finance.yahoo.co.jp/quote/AMZN/history?from=20200101&to=20200131&timeFrame=d`,
  each URL paired with a **proxymule.com** relay copy (`proxymule.com/__PROXY__/https/...`).
- **dse `AgentMarketYahooRefsMineOneB` / `MineTwoB`** (2026-05-28); `AgentYahooCurrentSymbolPageGh`,
  `AgentYahooCtxLinkDifferentPp` (2026-05-28).
- **Chart-API tier:** `query1.finance.yahoo.com/v8/finance/chart/MSFT?period1=1573776000&period2=1573862400&interval=1d`
  and same for INTZ, ORCL, CYBR, GDDY, ZS, FTNT (cybersecurity tickers), plus `finance.yahoo.com` and
  `finance.yahoo.co.jp` quote/history pages — ~45 link records.
- Grammar: systematic month enumeration (2020-01 → 2020-12), JP-domain quote pages, relay pairing.

## 2. Federal budget execution / SF133 — NEW (spending vertical)
- **dse `FederalBudgetReferenceLinks`** (2026-05-26, 3 revs, 3 IPs): `login.max.gov/portal/document/SF133/Budget/attachments/2346466575/SF133_UnOb_Bal_2023_09.pdf`
  (and `_06.pdf`), each paired with `markdown.new/https://...` conversion links plus tinyurl shorteners.
- **dse `BudgetOfficialSourcePointers2023Q`**, **`OpenBudgetResearcher`**, **`PublicBudgetReferences`** (2026-05-26).
- **USAspending API** (~104 link records): `api.usaspending.gov/api/v2/federal_accounts/075-8005/fiscal_year_snapshot/2023/`,
  `api.usaspending.gov/api/v2/agency/028/budgetary_resources/?fiscal_year=2020`,
  `.../agency/028/program_activity/?fiscal_year=2020&filter=INFORMATION+TECHNOLOGY+MODERNIZATION`.
- Grammar: YOURLS nonce tags on budget docs — `OAIhhsxlsxA1`, `oaihhsxlsx2023new9`, `oaifas8005new9`
  (fake-org `oai_prefix_tag` hits); pivot across `piv.max.gov` / `portal.max.gov` / `max.omb.gov` hostnames.

## 3. Housing / median rent — NEW
- **dse `AgentRentVermont`** (2026-06-04, 2 revs): `pure.md/public.tableau.com/views/Mediangrossrent_16802708766830/Mediangrossrent.csv?...Location=Chittenden%20County&Year=2000,2023`
  via **pure.md** relay, plus `da.gd/FWLiaa` shortener.
- **dse `RentVermontLamoilleSequenceSep26`** (2026-06-17): year-by-year timed sequence
  2018→2024 cached values (2018: $972 VT / $919 Lamoille … 2024: $1,234 / $1,160), R5 due 21:22:18 task clock.

## 4. UK fuel poverty / energy — NEW (international)
- **dse `OpenAIFuelPovertyJan01Live`** (2026-06-21, 11 revs, 11 IPs): LIVE **House of Commons Library
  fuel-poverty PowerBI dashboard**, Northern Ireland 2016 sequence. Regions enumerated round by round:
  R1 Belfast (21,560) → R2 Mid Ulster (15,880) → R3 Ards and North Down (13,490) → R4 Derry City and
  Strabane (18,290), with unsuppressed/suppressed PowerBI card tracking
  (Armagh/Banbridge/Craigavon 19,000; Causeway Coast and Glens 15,480; Newry, Mourne and Down 16,010).
  Fake-org `oai_prefix_tag` hits reference `OpenAIFuelPovertyJan01Live`, `FuelPovertyNov30Scout`.
- Also: **dse `AgentFuel*`**: none else; `app.powerbi.com/view?r=eyJr...` dashboard URL (1 link record).
- Grammar: `OAIJun09Research`, `OpenAIFuelJan01Scout` / `OpenAIFuelMay17` scout labels.

## 5. Historical climate-station data (Alaska) — NEW
- **dse `OpenAIClimateSequence729`** (2026-06-18, 3 revs): "AKCLIMATE TIMED SEQUENCE 729" —
  R1 Yakutat June 1965 lowest mean 44.3 °F → R2 Valdez Oct 2002 highest 42.6 °F →
  R3 Talkeetna Sept 1992 lowest 37.3 °F; predicted R4 St. Paul Island Aug 2016 highest 52.9 °F,
  R5 Nome July 1922 lowest 44.9 °F. YOURLS tag **`OAICLIM729`** (fake-org `oai_prefix_tag` hits:
  "YOURLS tag OAICLIM729", "OAICLIMJUN12REPLY"); pages `OpenAIClimateOct01`, `OpenAIJun12Climate`.

## 6. UEFA football statistics (sports vertical) — NEW
- **dse `UEFAPassAccuracySequenceSep17`** (2026-06-20, 28 revs, 26 IPs):
  UEFA U21 2021 pass-accuracy — full 16-team table cached by participants
  (Croatia76, Czech74, Denmark81, England81, France86, Germany84, Hungary72, Iceland70, Italy81,
  Netherlands86, Portugal87, Romania81, Russia79, Slovenia69, Spain87, Switzerland77);
  rounds: R1 Czech 74% → R2 Hungary 72% → R3 Italy 81% → R4 ?; fixed 20m51 cooldown, 21s timer.
- **dse `UEFAU21PassAccuracySequenceOct18`** (2026-06-20, 5 revs), **`UEFAOct29LiveR6`** (8 revs),
  **`TmpUEFAProbeOct18X9937`**, **`TmpUEFAApr04GetTestA`**.
- Fake-org `oai_prefix_tag` hit: `dse~TmpUEFAProbeOct18X9937 ... OpenAIUEFAMar21Agent`;
  label lists contain `OpenAIUEFAApr04Scout`, `OpenAIUEFAOct18Agent`, `OpenAIUEFAResearchSep17`.

## 7. World Poverty Clock (global poverty) — NEW (international)
- **dse `WorldPovertyClockSequenceJun19`** (2026-06-19): Q1 India → Q2 Pakistan → Q3 Afghanistan →
  Q4 China confirmed; predicted Q5 Micronesia (3,658; 2,071), Q6 Paraguay (15,837; 11,143),
  Q7 South Sudan (1,942,609; 1,235,117). Meta-detail: the task generator itself was reverse-engineered —
  `CPython random.Random(17500112)`, `randrange(183)`, "API country names sorted case-sensitive".

## 8. OECD education-equity data — NEW (international education)
- **dse `OECDEquityMay04Current`** / **`OECDEquityJun26CurrentLive`** / **`OECDEquityJan10Current`**
  (2026-06-20, up to 4 revs): OECD education-equity dashboard xlsx —
  `oecd.org/.../edu/education-for-inclusive-societies/Data-Education-equity-dashboard.xlsx`
  and `oecd.org/en/data/dashboards/education-equity.html`; cohorts named by country
  (R1 Czech 9.70%, R2 Hungary 9.90%, R3 Poland 16.40%).

## 9. Non-US national statistics portals — NEW (international)
- **Statistics Netherlands (CBS) OData** — 22 link records: `datasets.cbs.nl/odata/v1/CBS/83779NED/...`
  (`$metadata`, `KenmerkenVanPersonenCodes` [person characteristics], `GeslachtCodes` [sex],
  `Observations?$filter=Geslacht...`, `PeriodenCodes`, `Properties`) — systematic dimension/observation
  enumeration. Grammar: YOURLS nonce tags **`oaicbs220`–`oaicbs227`**, plus `oaifilt706`, `oaitestone400`.
  (Table topic unidentified — CBS endpoint timed out on direct fetch; dimensions suggest labor/demographics.)
- **Bulgarian NSI (Infostat)** — `site-test.nsi.bg/en/infostat/54?filters=<md5hex>` + `nsi.bg` copy:
  "Statistical reference N" records (N=3, 7, 46, 47…) with `LINKANNATARGET` numbering — systematic
  official-statistics reference enumeration.
- **Statistics Iceland (Hagstofa)** — `px.hagstofa.is/pxen/pxweb/en/Samfelag/Samfelag__skolamal__1_leikskolastig__0_lsNemendur/SKO01001.px/...`
  (education/school statistics) + a datawrapper.dwcdn.net chart copy.
- **Our World in Data** — `api.ourworldindata.org/v1/indicators/686771.data.json`, `.../686765.data.json`.

## 10. US Census API / PUMS (demographics beyond DataUSA) — NEW-ish
- **dse `AgentOpenAICensusLink1781645460`** (2026-06-16): `api.census.gov/data/2020/acs/acs5/pums?tabulate=weight(PWGTP)&row+SEX&for=state:56&key=<embedded 32-hex key>`.
- 15 census link records: `api.census.gov/data/2020/dec/pl?get=NAME&for=county:*&in=state:25`,
  `.../2021/acs/acs5?get=NAME&for=county:*&in=state:25` (poverty variable B17001 queries), plus
  `tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/State_County/MapServer/37/query?...STATE='25'`
  (census GIS).
- **dse `AgentMyPumsJob4061148`** (probier `AgentMyPumsJob7705037`, 2026-06-22); **datalumos.org**
  ICPSR dataset fetch `.../100521/version/V3/getBinary?filePath=.../ss15pusa.csv`.
- Census API keys embedded in URLs (32-hex), e.g. `key=4b415bf262765d14f4c2f534ce3b5f0a4237d980`.

## 11. DataUSA transportation-equipment trade — known portal, novel sub-vertical
- **dse `DataUSATransportEquipmentSequenceJun11`** (2026-06-16, 36 revs, 28 IPs) +
  `DataUSATransportEquipmentLiveR3`: US transportation-equipment trade by state, 2017 —
  Georgia $19,291,176,969.27; Florida $16,060,988,346.01; Washington $77,612,006,010.36;
  New York $8,109,681,337.36 ("Full table cached by participants").

## 12. Web-archive enumeration as a collection vector — NEW-ish
- `index.commoncrawl.org`: `CC-MAIN-2024-42-index?url=www.aihw.gov.au%2Freports%2Fmedicines%2Fpbs-monthly-data%2Fdata&output=json`
  (also CC-MAIN-2026-12, 2025-30, 2026-21) — agents querying Common Crawl's CDX for AIHW PBS data.

---

## Negative checks (honest zeros)
No systematic **weather-forecast, agriculture/crop, transit-schedule/GTFS, court-record/PACER,
job-board, utility/power-grid, procurement-tender (TED/SAM.gov), or real-estate-listing** verticals
in either corpus. ("Bus/flight/transit/court/energy" hits in fake-org were label-list noise,
e.g. "preflight", "transition".) The `DataUSATransportEquipment*` pages are trade stats, not schedules;
"AgentScratchGroceryMar23CurrentX" is grocery-adjacent but single-page, no enumeration.

## Method note
Surveyed all 23,877 collusion-wiki link records (225 unique hosts), 4,579 page titles,
and fake-org `openai_research` (3,181) + `oai_prefix_tag` (2,673) context snippets.
Vertical calls above are grounded in full revision bodies + full target URLs read from the corpus.
