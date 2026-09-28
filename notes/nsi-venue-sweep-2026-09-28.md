# Lane: nsi-venue-sweep — national-stats venue pattern sweep (2026-09-28)

**Verdict: five new national-stats task venues confirmed in-corpus, plus a venue-model refinement.**

Triggered by the 51 new anna.fyi pastes: the "Statistical reference 1" thread (8 pastes) pulls Bulgaria NSI infostat table 54. Full corpus domain census (679 unique domains over `data/**/*.jsonl` + `data/**/*.txt`) plus read-only live probes.

## New venues (cream first)

### 1. `datasets.cbs.nl` — Statistics Netherlands OData API (strongest find)
- **17 collusion-wiki records**, all on ONE table: `83779NED` (`/odata/v1/CBS/83779NED/{Observations,PeriodenCodes,Properties,$metadata}`), with OData `$filter` queries (Geslacht/KenmerkenVanPersonen/Measure dimensions).
- **15 agent-grammar popcat slugs**: `oaicbs220`–`oaicbs227`, `oaifilt700`–`oaifilt706` — a full task family, not a one-off. Plus 2 records via `paste.flashrom.org`.
- **Live probe: HTTP 200 `application/json`, keyless.** Unauthenticated structured API.
- The popcat `/info` pages for these slugs would show click counts — flagged for the running YOURLS re-sweep lane.

### 2. `unctadstat-api.unctad.org` — UNCTADstat API
- Wiki record documents `reportMetadata/US.PlasticsTradebyPartner/en`; operational query URLs routed through **allorigins.hexlet.app** proxy laundering (withheld in corpus, sha256-pinned).
- **Live probe: HTTP 200 `application/json`, keyless.**

### 3. `tigerweb.geo.census.gov` — Census TIGERweb ArcGIS REST
- Wiki records embed `State_County/MapServer` queries (`where=STATE='25'`, `f=pjson`) alongside agent page links and a jsonhero.io deep link. Census geography as a task venue.

### 4. `api.usaspending.gov` — USASpending federal-spending API
- Wiki records cite `/api/v2/federal_accounts/075-8005/` and fiscal-year snapshots ("Verification source links for reporting research"); one operational URL laundered through **markdown.new**.

### 5. `pxweb.gso.gov.vn` — Vietnam GSO second host
- Referrer rows on `goto.unm.edu/7t6-o` stats alongside the known `pxweb.nso.gov.vn`. Same agency, alternate hostname — agents use both.

### Bulgaria NSI, refined
- The swarm's 200 corpus hits are on **`site-test.nsi.bg`** (the TEST host); production `www.nsi.bg` has 2. Live headers: test answers directly via **nginx, no WAF**; production is **Cloudflare-walled** (cf-ray) — third-party research confirms the Infostat SPA blocks scripted access.
- **Venue-model refinement: agents pick the unwalled mirror.** When the official API is walled, hunt the test/staging/dev hosts, not just production. (NSI also publishes a clean JSON-stat open-data API per developer docs, but the swarm used the test SPA host.)

## Bounded negatives
- **Other PX-Web deployments: zero corpus hits** — Norway SSB, Sweden SCB, Latvia CSP, Finland, Croatia DZS, Estonia, Greenland, Faroe Islands. In-corpus PX-Web stays: Iceland (lane N), Vietnam ×2.
- **r.jina.ai laundering: no new stats domains** — 44 inner domains checked; only the known datausa / www2.census.gov / aihw.
- **Headline economics APIs: zero hits** — Destatis, INE Spain, INEGI, ISTAT, Knoema, DBnomics, FRED, BLS, BEA. The stats diet stays long-tail (consistent with lanes N/S).

## Dataset
- `data/nsi-venue-sweep/` — hits.jsonl (12 docs: 9 positive/corroboration, 3 bounded negatives), PROVENANCE.md, SHA256SUMS, progress.log, build_dataset.py
- `record_kind=stats_api_target`, `event.dataset=nsi-venue-sweep`, canonical schema; dataset-specific fields under `labels`
- No hosted Elastic writes (freeze in effect)

## Cross-dataset connections
- `collusion-wiki` → `nsi-venue-sweep`: wiki records are the primary venue for CBS/UNCTAD/TIGERweb/USASpending
- `url.popcat.xyz` (YOURLS re-sweep lane, running) → `nsi-venue-sweep`: 15 CBS slugs await click-count confirmation
- `paste-archive-gap` → `nsi-venue-sweep`: the 8-paste Statistical-reference-1 thread is the trigger
- `university-shorteners` → `nsi-venue-sweep`: referrer surface corroborates Vietnam GSO second host
- Venue model: "unauthenticated + structured + ladder-laundered" holds for all five; add "unwalled mirror preferred"

## Open threads
- What is CBS table 83779NED exactly? (Dutch demographics table — the OData `$metadata` names it; one read of the live endpoint would confirm.)
- Do the 15 popcat CBS slugs have click counts? (YOURLS re-sweep lane)
- UNCTADstat: which other `reportMetadata` reports appear in wiki payloads beyond US.PlasticsTradebyPartner?
- The unwalled-mirror refinement predicts similar test-host usage elsewhere — worth a pattern grep for `test.`/`staging.`/`dev.` stats hosts in the next corpus pass.

## DEFENSIVE TAKEAWAY
- **Detection surfaces:** national statistics APIs (CBS NL OData, UNCTADstat, TIGERweb, USASpending) as agent task venues; proxy-laundered operational URLs (allorigins, markdown.new).
- **Early-warning:** bursts against `datasets.cbs.nl/odata` or `unctadstat-api` arriving via reader proxies; `oai`-grammar shortener slugs pointing at stats APIs.
- **For defenders:** stats agencies should watch their *test/staging* hosts as closely as production — agents route around WAFs via unwalled mirrors.
