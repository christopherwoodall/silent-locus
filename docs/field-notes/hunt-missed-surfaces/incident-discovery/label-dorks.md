# Play 4: wiki-farm + probe-marker dorking (label-dorks)

Date: 2026-10-03. Read-only. 21 dorks logged via browser.search. Do NOT commit (standing rule for this discovery lane).

## Round A — exact OAI label strings (echo check)

| # | Dork | Verdict |
|---|------|---------|
| 1 | `"OAIFlatheadBridgeTestMay24X"` | Echo only: investigator repos (kmad/agent-swarm-forensics, ethanelasky/collusion-on-the-open-web, hamzah2304/messageboardauditbench, brausepulver/collusion-wiki-link-shorteners) + known DSEWiki/collusion.wiki farm. **No new venue.** |
| 2 | `"AgentSECCountyLinker99172"` | Known corpora only. **No new venue.** |
| 3 | `"OAIJun19OECDScout"` | Echo investigator repos. **No new venue.** |
| 4 | `"OAIHelperMar22X"` | Known corpora only. **No new venue.** |

## Round B — OAI-prefix grammar across wiki farms

| # | Dork | Verdict |
|---|------|---------|
| 5 | `"OAIResearchBridge"` | Noise. |
| 6 | `"OAIHelper" / "OAIScout" / "OAIWatcher"` | Noise. |
| 7 | Miraheze/Fandom grammar dorks | Noise / zero. |
| 8 | `site:ludism.org` | Known: ludism.org UseMod sandbox already in the farm map. **No new venue.** |
| 19 | `"ourworldoftext" agent OAI OR OpenAIResearch OR zz` | Press + hamzah2304/messageboardauditbench report (confirms "occupation + month + OAI" eval-label pattern, 3,103 distinct labels). **No new venue, no OWOT hits.** |

OAI-prefix grammar appears confined to the known ProWiki farm. Nothing on Miraheze, Fandom, ourworldoftext, telegra.ph.

## Round C — probe markers

| # | Dork | Verdict |
|---|------|---------|
| 9 | `LINKINJECT` (bare) | npm noise. |
| 10 | `PHPTEST` / `GOLINK` / `LINKAT` (bare) | Only known source: joshuadavid/wikiagentswarminvestigation paste-site-probe README. **No live traces elsewhere.** |
| 11 | `LINKCONTENTTEST` / `INJECTTEXT` / `CLICKMAYBE` | ClickFix malware noise. |
| 12 | `?fresh=x` | brausepulver `6_wayback_sweep.md` — decisive `?fresh=x1779955674.6343555` = 2026-05-28 08:07:54 UTC SPN-loop analysis. Grammar confirmed, no new venue. |
| 16 | `site:pastebin.com LINKINJECT OR PHPTEST OR GOLINK` | **Zero results.** Pastebin surface clean for these markers. |
| 18 | `site:github.com LINKINJECT1779084987 OR PHPTEST1779090121 OR GOLINK1779090736` | No relevant hits (unrelated OAuth commits, Evilginx phishlets, PHP vuln docs). |
| 21 | `site:telegra.ph LINKINJECT OR PHPTEST OR GOLINK OR INJECTTEXT` | **Zero results.** |

## Round D — report-carried markers (independent sightings)

| # | Dork | Verdict |
|---|------|---------|
| 13 | `"tok=expt"` | Transluce's agent-activity report (UNM IIIF probes tok=expt0–8) + urlquery.net report pages (the actual probe reports). **No independent NEW venue** — confirms known sources; yields direct report URLs. |
| 14 | `"OAI_META_1312" OR "OAI_IFRAME_TRADABLE"` | Press only: how2shout, windowsreport, windowsforum, glonce (UNCTAD coverage wave). **No new venue.** glonce.com = new-to-us aggregator, not a venue lead. |
| 15 | `"F%2561cts" OR "F%61cts"` | swarmcha.se (source: 55 double-encoded requests, May 4–Jun 19) + press. **No new venue.** |
| 17 | `"FractalWiki" PublicDataResearchAgentT93214` | Press (windowsreport, theregister, mfc.mn) + swarm-ai-research/wiki-agent-swarm-incident `analysis/field-evidence.md` — full farm venue table. See findings. |
| 20 | `tmcleod.org apchem OpenAIRegCFTest OR ZZZTemporaryTestPageXYZ` | Confirms swarm-ai-research commit `74aa49c6c7db2a5acabd3bb6281e70c109acbc3f` (2026-09-05) documented apchem via live direct read. |

## Ranked new finds

### 1. apchem (tmcleod.org) — venue present in OUR raw corpus, missing from hunt inventory
- What it is: UseModWiki instance at tmcleod.org (AP Chemistry wiki) carrying the incident signature into July 2026: OpenAI-named pages through **Jul 24** (latest known farm activity), `OpenAIRegCFTest` (11 changes — a clean SEC RegCF `county.json` specimen wrapped in a dozen allorigins/r.jina.ai encoding variants), `ZZZTemporaryTestPageXYZ` backup page.
- Evidence in our own bytes: `data/2026-05-17-collusion-wiki/raw/records.jsonl` contains `apchem/revisions/OpenAIRegCFTest-r4/r5/r10`; `links.jsonl` contains tmcleod.org `OpenAIRegCFTest` diff/history URLs — and those URLs carry the **`?fresh=998877` probe grammar**, tying the venue to the same toolkit family as the county.json `?fresh=x<epoch>.<random>` saves.
- Status: documented by swarm-ai-research (2026-09-05, live direct read); `grep` over `collections/hunt-missed-surfaces/` shows **zero mentions** — not yet in our hunt inventory.
- Action: add to the venue inventory; the Jul-24 OpenAI-named pages are the latest-dated farm activity on record.

### 2. Complete farm venue map (from swarm-ai-research field-evidence.md, direct-read)
DSEWiki (bulk ~18k edits, May 11–Jun 22) · UseModWiki SandBox (usemod.org, original board, reuse continuing Sep 4) · FractalWiki (wikiservice.at, ~400+ changes May 26–Sep 4, Jun 22 spike) · ProbierWiki (wikiservice.at, ~800+ changes Jun 18–Sep 5, human maintainer `HelmutLeitner` reverting) · Wiki4D (prowiki.org, ~200+ edits Jun 18–22, tight timestamp clustering) · Ludism sandbox · apchem (tmcleod.org, into July). **All on the same UseModWiki/ProWiki software + wikiservice.at/prowiki.org host family.** No wiki venue found outside this farm in 21 dorks.
- Cross-check these seven against our inventories; the wayback-cdx-sweep.md also shows rows on wikis "outside the export": wiki4d 55 rows, user/milk 10 rows (May 24–26) — `user/milk` is a small additional surface to verify.

### 3. `?fresh=` grammar bridges county.json saves → apchem wiki
The tmcleod.org `OpenAIRegCFTest` diff URLs use `?fresh=998877` / `?fresh=108926` — the same cache-buster grammar as the June-18 county.json capture burst (`?x=0.<17-digit>`). Same toolkit, two surfaces: Wayback SPN-loop saves and live wiki GET-write probing.

## Net verdict
- **No new wiki venue beyond the ProWiki/UseMod farm cluster.** 21 dorks; the OAI-prefix grammar is confined to the known farm; probe markers are confined to the known source repo + ClickFix/npm noise; pastebin and telegra.ph surfaces are clean.
- **One inventory gap closed**: apchem/tmcleod.org is in our raw corpus and externally documented but absent from hunt-missed-surfaces — promote it into the venue inventory with the Jul-24 activity as latest-known.
- Strongest negative: bare probe-marker dorks (LINKINJECT/PHPTEST/GOLINK) return **only** the known source repo — these June-2026 markers have no public echo elsewhere, consistent with agents writing them into non-indexed paste drops.
