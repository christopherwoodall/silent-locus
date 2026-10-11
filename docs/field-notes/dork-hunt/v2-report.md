# Dork-hunt v2 report (2026-10-03/04)

Fresh Google-dork wave (DuckDuckGo html backend, curl) using NEW IOCs from the
2026-10-03 hunt. v1 (518 unique dorks) covered the original word list; v2 covers
the joshuadavid v4 candidates (72 terms), discord-brief watch terms, relay hosts,
and NPWS incident terms. Deduped against v1 via data/dork-log.jsonl (shared log).

## Run stats
- **141 dorks run, 131 ok, 10 blocked, 0 errors.** Status: complete (state-v2.json).
- Tier A (25 top-novelty terms × bare + site:github.com + site:pastebin.com): 75/75.
- Tier B (26 terms × bare + site:github.com): 52.
- Tier C (5 path probes × bare + inurl:): 10.
- Tier D (4 NPWS terms): 4.

## Top hits (graded)

### 1. christian-egg/CoordinationGames — NEW parallel investigator [new / corroboration]
- Dorks: `"sec.govwayback.com"` (bare + site:github.com)
- URL: https://github.com/christian-egg/CoordinationGames/blob/main/docs/counter-investigations/wayback-patterns.md
- "Encoded Coordination on the Open Web" (LessWrong, Ethan Elasky et al.) — studies agents using wikis/boards as coordination channels.
- `docs/counter-investigations/` (21 files): scanned 14,591 wiki revisions for Wayback refs; **independently found the `sec.govwayback.com` hostname**; `archive-save-evidence.md` audits whether agents created archive snapshots (scoped negative: zero `web.archive.org/save` mentions in wiki text); `wayback-all-97.md` (342KB).
- Key: 2026-06-18 20:23:55, AgentMass0 published `archive.org/wayback/available?url=www.sec.gov/files/county.json` — DURING our burst window.

### 2. urlquery: jqp relay actively queried against IHME health-data API [new trace — candidate]
- Dork: `"jqp.vercel.app"` (bare, 3 hits)
- URL: https://urlquery.net/report/1bbf0db4-5498-494b-879b-43f1de6052d2
- 2026-05-27 scan of `jqp.vercel.app/api/v0?url=https://vizhub.healthdata.org/lbd/api/v1/themes/anemia/schemas/annual/info/aggregate/components/1?location_id=35&severity=sev&metric=prev&stat=mean` — the primary relay fetching IHME vizhub anemia prevalence data. Health-data task family, incident window.
- Follow-up: sweep urlquery for more jqp.vercel.app reports.

### 3. AgentRelent — press-corroborated as the #1 agent identity [known / corroboration]
- Dork: `"AgentRelent"` (3 hits; 0 on github/pastebin)
- URLs: https://www.indybay.org/newsitems/2026/09/08/18888462.php, https://mindfuldesign.substack.com/p/no-lunatic-required, https://finance.sina.com.cn/tech/roll/2026-09-15/doc-inirvzhh6980484.shtml
- Sep 2026 press naming AgentRelent alongside AgentMassPointer13, ResearchHelper, OpenAIResearchSec208, ResearchAgentX, AlphaBeta as self-chosen agent names. Sina: "3,103 agents' self-chosen names, #1 AgentRelent with 317 edits", "14,591 posts" (matches corpus).

### 4. OAI_META_1312 — re-grade: KNOWN UNCTAD marker [known material]
- Dorks: `"OAI_META_1312"` (2 hits), `site:github.com "OAI_META_1312"` (1 hit)
- URLs: https://github.com/vz-risk/VCDB/issues/24403, https://www.explainx.ai/blog/openai-agents-unctad-un-stat-api-scraping-2026, https://aventure.vc/news/2026-09-27-researcher-links-16-000-scans-of-a-un-statistics-porta
- All quote Rowan Howard-Jones's swarmcha.se UNCTAD writeup (Sep 26): payload labels `CHATGPTTEST1`, `OAI_META_1312`, `OAI_IFRAME_TRADABLE`, `CHATGPT_1610_2000_125192`. VCDB#24403 files it as a formal incident.
- Correction: remove from "most novel" watch tier — documented UNCTAD marker. Recon-code's "zero public-code hits" still stands (these are issues/blogs, not code).

### 5. NPWS dorks — press + the target dataset itself [known / useful]
- Dorks: `"Fire History" "National Parks and Wildlife Service"` (4), `"NPWS" "Fire History" agent` (8), `"Fire History service" NSW agent` (1)
- News: aitechdaily, abcnews.com wire, 7news.com.au — expected Oct 2–3 coverage.
- **Target dataset located**: https://datasets.seed.nsw.gov.au/dataset/fire-history-wildfires-and-prescribed-burns — NSW SEED open-data portal. The Fire History service endpoint for future trace sweeps.

## Honest zeros (high-value)
- `AgentSECCountyLinker` — 0 on bare/github/pastebin. Zero public footprint confirmed.
- Census key `b12026d61228a4b0d441ae7aa93f1ea222877503` — 0 everywhere. Appears nowhere else public.
- Path probes (`sec.gov//files//county.json`, `:443` variant, `www.sec.gov/sites/default/files/county.json`) — all 0 (one blocked = unknown).
- `oasb_raising_capital_map`, `palapiXYZ`, `AgentCustomPageZZZ`, paste-probe markers — 0.
- `vanderbi.lt/maallraw260618`, `cdn.putput.io`, `2md.link` — blocked (unknown, not zero).

## Noise (graded, not traces)
- `"ZZZNew"` — TikTok/YouTube usernames. `"Gurl99"`/`"Gphp99"` — social usernames.
- `"ANCHORTEST"` — anchortest.app product + GitHub org. `"TINJ"` — Croatian village.
- `"AgentMine"` — agentmine.io product + repos. `"MapHelper"`/`"MassUpdater"`/`"ResearchHelper"` — generic software.
- `"platform.lemino.ai"` (7) — vendor usecase pages. `"api.cors.lol"` (2) — Gridinsoft checker. `"IowaTableauTip"` (1) — DDG ad redirect.
- `"aifs.gov.au"` (1) — sur.ly homepage mirror.
- urlquery allorigins.hexlet.app report — benign proxy functionality probe (2021 Cosmos article).

## Method
`run_dorks_v2.py` (in this dir). 6s pacing, 60s backoff on block. Log: data/dork-log.jsonl (shared with v1, kind=v2-*). State: state-v2.json. NOT committed per task brief.
