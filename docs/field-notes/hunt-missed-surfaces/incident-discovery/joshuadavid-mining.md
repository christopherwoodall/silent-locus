# Mining: joshuadavid/wikiagentswarminvestigation

Date: 2026-10-03. Read-only (GitHub API + raw.githubusercontent, no clone).
Scope: agents and agent infrastructure only. Not committed (merger handles that).

Repo: https://github.com/joshuadavid/wikiagentswarminvestigation — 9 task dirs, each with
README + extract_evidence.py + outputs/. Pulled every outputs/ evidence file:
sec-regcf-ma-cache (6 files incl. 144KB regcf_narrative_lines.txt), url-fetch-proxy-usage,
paste-site-probe, epl-2000-01-bench, nsi-bg-tables, roi-et-labor-stats,
fast-follow-question-bench, plus tasks/first_last_observed (404 — not present at HEAD).

## 1. The county.json relay census (data-files.md) — the money table

31,525 corpus references to `sec.gov/files/county.json` across **33 distinct hosts**.
Ranked by URL instances:

| refs | relay | pattern |
|---:|---|---|
| 14,341 | jqp.vercel.app | `jqp.vercel.app/api/v0?url=<X>&jq=<Y>` — **dominant relay (45%)** |
| 11,332 | direct SEC | `www.sec.gov/files/county.json` |
| 7,946 | md.succ.ai | markdown-reader proxy |
| 4,928 | allorigins.hexlet.app | `/raw?url=` |
| 1,970 | r.jina.ai | reader proxy |
| 1,355 | investor.gov | SEC's own mirror |
| 1,326 | markdown.new | reader |
| 599 | md.dhr.wtf / pure.md | reader proxies |
| 480 | api.cors.lol | CORS bypass |
| 402 | webcrawlerapi.com | scrape-API playground |
| 139 | translate.goog | Google Translate proxy |
| 71 | proxymule.com | |
| 40 | vanderbi.lt | shortener, date-stamped link `maallraw260618` (= 2026-06-18) |
| 27 | web.archive.org | Wayback |
| 24 | platform.lemino.ai | **NEW — `platform.lemino.ai/api/url2md/`, not in our inventories** |
| ~200 | path-canonicalization probes | `sec.gov//files//county.json`, `sec.gov/foo/../files//county.json`, `sec.gov/Files/county.json`, `sec.gov:443/files/county.json`, **`sec.govwayback.com`** (typo-squat-shaped) |
| ~140 | SEC Drupal source | `www.sec.gov/sites/default/files/county.json` (+ `?_format=json`) |

Long tail also names: thingproxy.freeboard.io, api.codetabs.com/v1/proxy,
cors.hypnguyen.workers.dev, cors.isomorphic-git.org, proxy.corsfix.com,
cf-cors.findme-19.workers.dev, api.allorigins.win, httpbin.org/redirect-to,
docs.google.com/viewer, jsonformatter.curiousconcept.com, codebeautify.org/jsonviewer.

Companion file `sec.gov/files/regcf.json`: **1,342 refs**, treated as fallback (same
regCF_county_* jq expressions). 814 direct, 322 md.succ.ai, 113 investor.gov, 37 jina,
34 markdown.new, 20 pure.md, 2 translate. Distinct hosts: 7.

Two more cached files: SEC map JS `oasb_raising_capital_map/main.js` (1,137 refs —
fetched for `formatNumber` + FIPS lookup; cache-busters `?v=1.2`, `?_format=html`,
`?abc=88997`, `?x`) and `code.highcharts.com/mapdata/countries/us/us-ma-all.geo.json`
(450 refs). Duplication: 17,074 jqp-wrapped county.json URLs in the wiki, 1,293 distinct
jq expressions after normalization (~13× redundancy).

## 2. regcf burst timeline — MATCHES our county.json Wayback burst

| metric | value |
|---|---|
| regcf revisions | 5,067 |
| distinct pages | 1,253 |
| distinct labels | 810 |
| first revision | 2026-06-18T14:10:56Z |
| peak hours | 20:00 UTC (2,010 revs), 21:00 (740), 19:00 (1,025), 18:00 (699) |
| tail | through 2026-06-22 |

**Our Wayback county.json burst: June 18, 14:52–20:21 UTC (60 captures).**
The wiki coordination burst (14:10 → 21:00 UTC, same day) overlaps it almost exactly —
wiki activity starts ~40 minutes before the first Wayback capture. This is strong
corroboration that the Wayback burst is agent-driven: the same operation coordinating
on-wiki and saving to the archive in the same afternoon. Top regcf labels:
AgentRelent (254), LinkHelper771 (169), MapHelper (146), AgentTestLearnXYZ (112),
OpenAIResearchSec2028 (78), OpenAIResearchSec2027 (64), CountyAgentMySecLinksZZZ2 (56),
AgentSECCountyLinker99172 (46), ZZUniqueAgentJun18Citations (25), AgentNewMediaZZ (25).

## 3. url-fetch-proxy-usage — probe series with timestamps

- **TEL_series** (May 18, 08:51–08:58 UTC): ~17 pastes, `telegra.ph/Test-Link-88990-05-18 CLICKMAYBE <epoch>` — telegra.ph as probe target.
- **TK_series** (May 18, 06:15): `TK084908` + `api.microlink.io`.
- **URLTEST_series / ANCHORTEST** (May 18, 10:16–10:19): `URLTEST1779099362` + `2md.link` (**new shortener**).
- **Ghtml_probe_series** (May 28, 13:03): `Ghtml599`, `Ghtml4strict99`, `Gxml99`, `Gbbcode99`, `Gmarkdown99`, `Gurl99`, `Glatex99`, `Gphp99`, `Gjavascript99`, `Grobots99` — all via **jqp.vercel.app** targeting `rspace.library.cofc.edu` (jqp in the wild against a new target).
- **linktry_series** (May 28): `linktry97976` via md.succ.ai → finance.yahoo.co.jp.
- **SFTEST_RefQ_series** (May 26): allorigins.hexlet.app + markdown.new + workers.dev → **portal.max.gov** (matches our omb-max slug).
- **Proxy_series** (Jun 17): `ProxyTestWonder` via markdown.new — same day as DoE fuzz run.
- `IowaTableauTip` (Jun 16): markdown.new → da.gd (**new shortener**). `palapiXYZ` (Jun 17): allorigins → mapgenie.io.
- `cdn.putput.io` (Aug 21): pari-transfer probe. `pastebin.tarcseh.me` (new paste host).

## 4. paste-site-probe — marker bodies verbatim

ZZ-labeled probes (May 18, pastebin.k4be.pl): `LINKINJECT1779084987`, `PHPTEST1779090121`,
`GOLINK1779090736` (+ twin), `LINKCONTENTTEST`, `INJECTTEXT`, `RAND1779099668`,
`LINKAT`. Epoch-suffixed markers = machine cadence. Also `TestHelloABC`, `EPL95test`,
`hd-test-1450`/`hello-hd-1450`, and a tarcseh.me XSS probe referencing `site-test.nsi.bg`.

## 5. v4 word-list candidates — 72 strings missing from v3 (3,827 terms)

Cross-checked 120 extracted candidates against `ioc-wordlist` branch v3: 48 present,
**72 missing**. Full machine-readable list: `/tmp/jdwiki/v4-candidates.json`
(schema: term, category, provenance). Category split: 68 launcher_toolkit, 2 relays,
2 targets.

Notable v4 candidates:
- **New relay hosts**: `2md.link`, `cdn.putput.io` (+ `platform.lemino.ai` from §1 — captured as relay)
- **Path-probe family**: `sec.gov//files//county.json`, `sec.gov/foo/../files//county.json`, `sec.gov/Files/county.json`, `sec.gov:443/files/county.json`, `sec.govwayback.com`
- **Probe series**: `TK_series`, `TEL_series`, `URLTEST_series`, `Ghtml_probe_series` (+ 10 G*99 labels), `linktry_series`, `SFTEST_RefQ_series`, `Proxy_series`
- **regcf labels**: `AgentRelent` (254 revs), `MapHelper` (146), `ResearchHelper` (51), `MassUpdater` (44), `AgentMine` (32)
- **Fresh family**: `AgentOurFreshLinks778899`, `DoubleSlashPrettyFresh123`, `UltraFreshMassLinksA8899`, `BridgeNowFresh`, `ContinueFresh99282`, `FreshMDHostChain7711`
- **ZZZ markers**: `AgentCustomPageZZZ`, `AgentMySecLinksZZZ2`, `ZZZNew`
- **Misc**: `IowaTableauTip`, `ProxyTestWonder`, `palapiXYZ`, `linktry97976`, `URLTEST1779099362`, `ANCHORTEST`, `TINJ`, `RAND`, `EPL95test`, `TestHelloABC`, `hd-test-1450`, `oasb_raising_capital_map`, `?_format=json`
- **Targets**: `vanderbi.lt/maallraw260618`, `www.sec.gov/sites/default/files/county.json`

Deliberately NOT staged (judgment calls): single-letter label `A` (undorkable), generic
`Refresh`/`refresh`/`refreshers` (too noisy alone — kept the compound forms), 1-occurrence
narrative labels below the bar, epoch-suffixed marker instances (base forms cover them).

Note: extraction was deliberately narrow (top-25 rev labels, top fresh/ZZZ tokens).
The repo holds 810 distinct regcf labels and 3,566 narrative lines — deeper mining could
2–3× the candidate count. epl/nsi/roi benches are eval-task content, low hunt value.
