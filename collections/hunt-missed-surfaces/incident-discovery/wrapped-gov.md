# Incident discovery play 2: relay-wrapped .gov enumeration

Date: 2026-10-03. Method: Wayback CDX API (curl, 2–3s pacing, no blocks hit).
Inverted the hunt: instead of searching for incident URLs in archives, enumerated
every .gov URL ever wrapped in a relay and looked for incident-shaped clusters.

## Queries (all `from=2026`, `collapse=urlkey`, `filter=original:.*\.gov.*`)
- `url=r.jina.ai/http*` → 68 distinct wrapped .gov URLs (+3 via broad `r.jina.ai/*`: NASA PDF, linyi.gov.cn page, LOC resource — all benign)
- `url=api.allorigins.win/*` → 13 distinct
- `url=corsproxy.io/*` → 39 distinct
- Uncollapsed follow-ups: aihw.gov.au (7 captures), census file across wrappers

CDX quirk noted: `url=r.jina.ai/http*://*.gov*` (multi-wildcard) silently returns [];
the working form is `url=r.jina.ai/http*` + `filter=original:.*\.gov.*` regex.

## Ranked host table (jina wrapper)

| host | n | date range | shape |
|---|---|---|---|
| id.loc.gov | 7 | 2026-01-26..03-07 | LOC authorities lookups, spread out — researcher-shaped |
| www.aihw.gov.au | 5 | 2026-06-18..09-05 | **CANDIDATE** — health data cubes, see below |
| www.sec.gov | 5 | 2026-09-04..10-03 | county.json wrapped, all post-incident — observer traffic (known) |
| files.santaclaracounty.gov | 4 | 2026-06-02..07-14 | latino-health PDFs (secondary) |
| tile.loc.gov | 4 | 2026-07-31 (all same day) | one newspaper scan ×4 — odd, single-target |
| www.huduser.gov | 3 | 2026-05-28 (same day) | FMR PDFs (secondary) |
| www.investor.gov | 3 | 2026-09-04 (same day) | county.json w/ `uniqmk13`+`mode=fit&max_tokens` — jina param grammar (known) |
| www.gov-online.go.jp | 3 | 2026-05-12..07-26 | JP gov articles — benign |
| www.nasa.gov | 3 | 2026-01-01..01-15 | PDF, incl. one with `)` typo in URL — sloppy, benign |
| rptsvr1.tea.texas.gov | 2 | 2026-07-29 (same day) | **CANDIDATE (secondary)** — TX Education disciplinary-data downloads |
| viz.aihw.gov.au | 2 | 2026-09-05 (same day) | PBS dashboard (AIHW family) |
| 21 more hosts | 1–2 | scattered | mostly benign singletons (see logs) |

## New candidate incidents

### 1. AIHW — Australian Institute of Health and Welfare (STRONGEST)
- `https://r.jina.ai/http://https://www.aihw.gov.au/getmedia/57e4c61f…/Principal-Diagnosis-cube_2014-15.xls` — **2026-06-18** (doubled `http://https://` scheme = agent URL-construction sloppiness)
- Sep 4–5 cluster: PBS prescription data + PBS dashboard (viz.aihw.gov.au), wrapped in both `http://` and `https://` jina forms
- Independent corroboration: public-chatter lane found Forkast/metirai reporting AIHW SQLi/XSS/**command-injection** attempts — a NEW target distinct from the Medicare portal
- In-window + agent-shaped URL + externally corroborated + health-data target. Previously unknown to this hunt.

### 2. Census ACS file, triple-relay pull, 2026-06-17 (NEW)
- `www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/1YRData/acsdt1y2022-b16001.dat`
- jina 2026-06-17 02:59:07 → corsproxy.io 2026-06-17 03:03:01 → allorigins 2026-06-17 (same day)
- Same file, three relays, four minutes apart — relay-rotation behavior, the SAME MORNING as the DoE fuzz run. Census was a weak eval candidate (dsqa_862).

### 3. Texas Education Agency disciplinary data (secondary)
- `rptsvr1.tea.texas.gov/adhocrpt/Disciplinary_Data_Products/{campusdiscipline,Download_All_Campuses}.html` — 2 captures, 2026-07-29
- Texas DSHS slug was zero rows in our corpus; this is a different Texas agency (Education). Campus-discipline downloads.

### 4. Santa Clara County health PDFs (secondary)
- 4 captures Jun 2–Jul 14 (latino-health-vol2 PDFs) + a triple-laundered variant: `tb-cors-proxy.deno.dev/https://web-archive-org.translate.goog/web/…` (CORS proxy → Google Translate → Wayback)

## Known incidents (corroborated, not new)
- sec.gov county.json wrapped via jina/allorigins/corsproxy — ALL post-incident (Sep–Oct 2026), observer/researcher traffic. No in-window wrapped captures.
- investor.gov county.json via jina with `mode=fit&max_tokens` — matches the skill-ladder jina param grammar.

## Honest negatives
- Zero wrapped captures for civilrightsdata.ed.gov, bea.gov/apps.bea.gov, bac-lac.gc.ca / recherche-collection-search.bac-lac.canada.ca in-window — consistent with arquivo.pt (not jina) being the DoE relay.
- allorigins/corsproxy.io results are dominated by RSS-feed pulls (bot noise, not agent incidents).

## Tradecraft notes
- Doubled schemes (`http://https://`) and stray `)` in wrapped URLs = agent-side URL construction sloppiness; a usable agent-traffic marker.
- Triple-laundering observed: CORS proxy → Google Translate → Wayback Machine.

## Recommended follow-ups
1. AIHW: pull the 2026-06-18 WARC record; search Forkast/metirai writeups for dates to align; check arquivo.pt for aihw.gov.au.
2. Census file: check Common Crawl + arquivo.pt for the same URL; look for dsqa_862 parameter shapes.
3. TEA: uncollapsed CDX for the host; check for more July 2026 captures.
4. Extend the wrapper matrix: corsproxy.io `/raw` paths, `r.jina.ai/http://` variants for LAC/BEA hosts (cheap).

Raw: /tmp/wgov-full.json, wao.json, wcp.json, waihw.json, wcensus.json, wgov-broad.json (ephemeral; re-runnable via queries above).
