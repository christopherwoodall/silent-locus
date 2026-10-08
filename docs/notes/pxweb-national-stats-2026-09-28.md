# Lane N: national-statistics-API task targets (2026-09-28)

**New task family found: national statistics APIs.** Agents need public structured demographic/census data, and the corpora show them hitting national-stats venues across four countries, often through proxy laundering.

## Finds (cream first)

1. **UK ONS Cantabular API — NEW task family, in-corpus with click evidence.** Four agent-created `rmn.re` shortlinks point at the UK Office for National Statistics Census 2021 API (`api.beta.ons.gov.uk/v1/datasets/TS030*`), with 44/36/33/30 clicks (slugs `jp jr jo jq`; live docs probe: API root returns 200 JSON, keyless). This is a *UK census* task family we had not tracked — the wiki census family was US-only. Cross-dataset link: `rmn-re-linktable` index (4 docs) ← the same rmn.re venue agents use for wiki-task exchanges.
2. **Statistics Iceland PX-Web (`px.hagstofa.is`) — in a "Links for research" wiki paste** (`paste.probyte.ee/view/e48589b5`). Live probe: host is a public PxWeb UI ("PxWeb - Select database"). Second national PX-Web instance after Vietnam GSO — pattern holds: agents treat PX-Web as a portable national-stats API surface.
3. **Vietnam GSO PX-Web (`pxweb.nso.gov.vn`)** — confirmed as HTTP referrer on the `goto.unm.edu/7t6-o+` shortener stats page (proxied through jqp/pure.md/md.succ.ai/r.jina.ai; peak 2026-06-18). Evidence file: `data/university-shorteners/goto-unm-edu/7t6-o_stats_2026-09-28.txt`.
4. **DataUSA tesseract API is the dominant stats venue** — 1,914 `data.jsonrecords` link mentions in `collusion-wiki/links.jsonl` (cubes: acs poverty/demographics, ipeds_admissions); 3 proxy-primitive hits show pure.md laundering of `api.datausa.io/tesseract/data.csv` (ipeds_admissions, Universities 164988/147767/216339) by 6 dse-wiki Clark-family agents. Live probe: `api.datausa.io` → public Tesseract docs UI.
5. **US Census Bureau API core venue** — 125 collusion-wiki docs (94 `api.census.gov`): ACS5/ACS1/PUMS/Decennial-PL endpoints inside wiki task families (GCT bridges, CensusLink, TexasPovertyRace, AgentMassData).

## Theory-of-mind update

Agents want **structured public microdata**: census/poverty/demographics (US Census API, DataUSA tesseract, UK ONS TS030), university admissions (IPEDS), national PX-Web tables (Vietnam, Iceland). They launder through reader proxies (jqp/pure.md/md.succ.ai/r.jina.ai) and URL shorteners (rmn.re), suggesting the stats hosts are queried *from* sandboxed/proxied runners, not from bare egress. Prediction test: World Bank API, FRED, BLS, BEA, SCB (Sweden), SSB (Norway), Statbank.dk, ABS all score **zero hits across 8 indices** — either agents never needed them or those runs aren't in our corpora. Unseen candidates worth the next lane: StatsCan, ISTAT, INEGI, Eurostat, ABS API.

## Cross-dataset connections
- `rmn-re-linktable` → `pxweb-national-stats`: the rmn.re shortener is the shared venue linking wiki-task exchanges to UK-stats task targets.
- `proxy-primitives` (pure.md) → `pxweb-national-stats`: pure.md launders both r.jina.ai-style reader traffic and DataUSA API CSV endpoints.
- `university-shorteners` → `pxweb-national-stats`: UNM shortener referrer surface caught the Vietnam PX-Web proxy traffic.
- `collusion-wiki` → all: wiki task families (GCT/CensusLink/TexasPovertyRace/Clark) are the primary stats-API users.

## Dataset
`data/pxweb-national-stats/` (hits.jsonl: 12 records, PROVENANCE.md, checksums.txt, progress.log); ES index `pxweb-national-stats` = 12 docs, zero unexpected top-level fields; record_kind `stats_api_target`, canonical schema `notes/gems-es-mapping.json`.

## Open questions
- TS030 = which Census 2021 table exactly? (number-of-rooms theme; the `area-type=p19wpc` query filters to Westminster parliamentary constituencies — agent was doing per-constituency UK analysis.)
- Who created the rmn.re ONS shortlinks (clicks peaked when?)? — out of scope; infrastructure only.
- Are there PX-Web instances for other countries in wiki payloads we haven't grepped for (pattern: `px*.gov.*`, `pxweb`)? Follow-up lane.

## DEFENSIVE TAKEAWAY

- **Detection surfaces exposed:** national statistics PxWeb APIs (ONS, DataUSA, Hagstofa) as agent task venues — same family as the open-data-api-venues lane.
- **Early-warning signals:** proxy-laundered bursts against stats endpoints; referrer URLs carrying embedded secrets (Census API keys found in the wild — redact on sight).
- **What a defender could instrument:** fingerprint proxy-laundered access the way the open-data lane describes; stats agencies should treat bulk proxied reads as a signal, not background noise.
