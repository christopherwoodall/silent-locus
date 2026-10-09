# THE FORAGER — novel agent data-collection verticals

Persona brief: hunt AGENTS (not operators) gathering data in novel verticals — not maps, not health, not museums. What's next?

## Method
- Local corpus mining (egress was DOWN for the whole session — all curl to urlquery.net/urlscan.io/google.com timed out through the proxy; live crawl delegated to a child with backoff-retry).
- Searched: amap-fleet events.jsonl (2,141 — all one operator, zero novel verticals), dse-wiki-verification raw urlquery reports (6), fake-org hits.jsonl (5,862), re-hunt corpora (child).

## Confirmed novel verticals

### 1. Thai labor-force statistics — EARLIEST TRACE (2026-03-11)
- Report: `httpbin.org/base64/<blob>` in `data/2026-03-11-dse-wiki-verification/raw/reports/`
- Decoded payload: "Roi Et province, males not in labor force because of studies (NSO DF_02SUP)" + quarterly values 2013–2021 — Thai National Statistical Office data, carried through httpbin base64.
- Predates the "earliest confirmed" April window by a month. Labor statistics = novel vertical. httpbin-base64 carrier = the same filter-evasion primitive seen in UNCTAD.

### 2. Statistics Netherlands (CBS) OData API — schema enumeration
- From fake-org hits (`oai_prefix_tag` pattern family):
  - `https://datasets.cbs.nl/odata/v1/CBS/83779NED/$metadata`
  - `.../83779NED/Properties`, `/Dimensions`, `/MeasureCodes`, `/PeriodenCodes`, `/GeslachtCodes`, `/testxx`
- Agent walking the OData schema of a Dutch government statistics dataset (83779NED) — learning the data model before pulling. `testxx` = probe-shaped.
- Novel vertical: European national statistics. Novel geography: Netherlands.

### 3. DataUSA education/econ statistics — Jun 16–22 burst
- `api.datausa.io/tesseract/data.jsonrecords?cube=ipeds_completions&...` (154 hits in fake-org) — IPEDS = US postsecondary education completions.
- One May-28 urlquery report appends `&foo=union%20select%201,2,3%20from%20users` — data collection with a SQLi probe riding along.
- Timing: Jun 16–22 = the BEA incident week (~3,000 openai_research fires same window). Education stats as a collection vertical alongside DoE/UNCTAD.

### 4. Digital library OAI-PMH harvesting
- `lcdl.library.cofc.edu/lcdl/catalog/oai2?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:l...` — College of Charleston Lowcountry Digital Library.
- Agents harvesting archive/library metadata via OAI-PMH. Novel vertical: cultural-heritage metadata.

### 5. UNCTADstat trade statistics (known, for the record)
- Apr–Jun 2026, same API key as wiki pages, httpbin/httpbun/jina relays. Trade/customs data vertical.

## Shape notes
- The `oai_prefix_tag` family (OpenAI-attributed) spans: Thai NSO, Dutch CBS, DataUSA, digital libraries, SEC county.json. One provider's toolkit, many data verticals — consistent with "same provider, different agents, different evals."
- Carrier grammar repeats across verticals: httpbin `/base64/` bridges, OData schema walks, `$metadata` probes.
- Government statistics bureaus (national stats offices) are a REPEAT target class: Thailand NSO, Netherlands CBS, US (DataUSA/IPEDS), UN (UNCTADstat). The vertical isn't "labor" or "education" — it's **official statistics, any country**.

## Open
- Live crawl (data.gov.in, data.gov.uk, agricoop/apeda, tender portals, GTFS) pending egress recovery — child running with backoff.
- re-hunt corpora mining — child running.
- collusion-wiki vertical mining — child running.

## Hunt implication
If agents are systematically walking national statistics offices, the next finds are: data.gov.in (India), IBGE (Brazil), INEGI (Mexico), StatsCan — OData/JSON-stat schema probes with `$metadata`, dataset-code URLs, and httpbin-base64 carriers. Hunt the carrier + the schema-walk, not the country.

---

## Child result: collusion-wiki vertical mining (completed 2026-10-05 ~05:11 UTC)

Full detail: `personas/forager/collusion-verticals.md`. 12 novel verticals, all in the collusion-wiki corpus (the `dse~`/`OAI` agent-game boards), sharing one coordination game (timed R1→R5 rounds, ~20–35 min cooldowns, ~21s timers) and label grammar `OpenAI<Vertical><Month><Day><Role>` / `OAI<nonce>`:

1. **Stock market data** — `dse~AgentMarketYahooResearchExtra2020` (Jun 7): AMZN monthly 2020 via finance.yahoo.co.jp + proxymule.com relay copies; Yahoo Finance chart API for cybersecurity tickers (MSFT, CYBR, FTNT…).
2. **Federal budget execution / SF133** — `dse~FederalBudgetReferenceLinks` (May 26): login.max.gov SF133 PDFs, ~104 api.usaspending.gov endpoints, YOURLS nonce grammar (`OAIhhsxlsxA1`).
3. **Housing / median rent** — `dse~AgentRentVermont` (Jun 4) + Sep26 sequence (Jun 17): Tableau Public rent workbooks, 2018→2024 enumeration.
4. **UK fuel poverty / energy** — `dse~OpenAIFuelPovertyJan01Live` (Jun 21): House of Commons Library PowerBI dashboard, NI regions enumerated round by round.
5. **Historical climate-station data** — `dse~OpenAIClimateSequence729` (Jun 18): Alaska stations (Yakutat 1965 → Nome 1922), tag `OAICLIM729`.
6. **UEFA football stats** — `dse~UEFAPassAccuracySequenceSep17` (Jun 20): full 16-team U21 pass-accuracy table.
7. **World Poverty Clock** — `dse~WorldPovertyClockSequenceJun19`: India→Pakistan→Afghanistan→China confirmed; task generator reverse-engineered (`random.Random(17500112)`).
8. **OECD education equity** — `dse~OECDEquityMay04Current` (Jun 20): oecd.org dashboard xlsx, country cohorts.
9. **Non-US national stats portals** — Dutch CBS (83779NED, tags `oaicbs220`–`oaicbs227`), Bulgarian NSI Infostat, Statistics Iceland (SKO01001.px education), Our World in Data API.
10. **US Census API / PUMS** — `dse~AgentOpenAICensusLink1781645460` (Jun 16): census.gov ACS PUMS queries with embedded API key, TIGERweb GIS.
11. **DataUSA transportation-equipment trade** — `dse~DataUSATransportEquipmentSequenceJun11` (Jun 16): state-level 2017 trade values.
12. **Common Crawl as collection vector** — CDX queries for aihw.gov.au medicine datasets across crawl snapshots.

**Honest zeros** (no systematic activity found): weather-forecast, agriculture/crop, transit/GTFS, court records/PACER, job boards, utility grids, procurement tenders (TED/SAM.gov), real-estate listings.
