# FINDINGS — PASTEBIN PLUNDERER

**Started:** 2026-10-05 ~02:10 CDT | **Status:** RUN 1 COMPLETE — resuming next run from open threads
**Method:** search-engine-indexed public pastes only; log URLs, no bulk fetching (opsec); corpus cross-reference for verification.

## Baseline (corpora check)
- `2026-09-28-chinese-amap-fleet/events.jsonl`: **0** paste-service mentions.
- `2026-10-01-oai-tag-sweep/events.jsonl`: 8× `pastebin.com` — all SEO spam (movie-download spam), NOT agent artifacts.
- `2026-10-03-openai-agent-traces/events.jsonl`: **0** paste-service mentions.
- `codebreaker/FINDINGS.md`: **0** paste mentions.
- **Conclusion:** any agent-shaped paste find = GENUINELY NEW by default.

## Services swept
(see services.txt for full list + status)
- **pastebin.k4be.pl** — SWEPT via third-party investigation (see Findings). Polish stikked instance. 0 mentions in our corpora events files.

## Findings

### KNOWN (publicly documented, not ours)
1. **joshuadavid/wikiagentswarminvestigation — pastebin-k4be export** (public GitHub repo, ~5 stars)
   - URL: https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/agent-logs/pastebin-k4be/README.md
   - What: full scrape of `https://pastebin.k4be.pl` (stikked; public `/lists/{offset}` + `/api/paste/{pid}` endpoints), 322 non-private pastes as of 2026-09-07, filtered to 198 agent-swarm pastes spanning 2019–2026-09.
   - Classification: 126 shellac-imported + 72 subagent-verdict (51 swarm / 21 unclear); 124 human-labeled excluded. ~42% swarm share of the entire host (~136/322).
   - Swarm markers documented: title grammars `PAD\d+x\d+`, `TEL\d{6,}`, `TK\d{5,}`, `URLTEST\d`, `linktry\d`; bodies with `pad-<epoch>-<n>`, `CLICKMAYBE`, `URLMARK`, `FRAMEK4`, `jqp.vercel.app/api/v0?url=`, `2md.link/is.gd/`, `md.succ.ai/`, `pure.md/`, `telegra.ph/Test-Link`; coordination text (`clock.wait`, `task clock`, `container UTC`, `shared UTC`, `scaffold clock`, `R1..R9` rounds, cohorts `MAR13`/`Dec27`/`Aug09`); "OAI Transfer <hex>"; bench answers (EPL relegation 1995-2010, Roi Et TH45 stats, NSI lookups); stikked `Re:` reply chains (4 swarm reply edges).
   - Our forager persona noted the k4be.pl linkage (Thai NSO data via Polish pastebin) but never this investigation or its grammars — open lead was "exact paste URL not recovered".

### OURS (linkage to our corpora)
2. **k4be swarm = known OpenAI-attributed swarm family, paste surface.** The coordination grammar `clock.wait` / `task clock` / `shared UTC` in the k4be markers ALSO appears in our `2026-10-01-oai-tag-sweep/events.jsonl` (collusion.wiki evidence: "racing via clock.wait -- OAIJun19OECDScout", "task clock -- OAINov26SectorScout"). Same swarm family, different surface. The paste site is the new surface, not a new actor.

### GENUINELY NEW
3. **New swarm markers** (zero hits in all three corpora events files): `CLICKMAYBE`, `URLMARK`, `FRAMEK4`, `pad-<epoch>-<n>`, title grammars `PAD\d+x\d+` / `TEL\d{6,}` / `TK\d{5,}` / `URLTEST\d` / `linktry\d`, `"OAI Transfer <hex>"`, `R1..R9` round labels, cohort names `MAR13`/`Dec27`/`Aug09`, `telegra.ph/Test-Link`, `2md.link/is.gd/`, `pure.md/` (as swarm markers). → Add to hunt marker bank.
4. **New surface**: `pastebin.k4be.pl` — 0 mentions in all three corpora events files. Distinct from user's seed `pastebin.pl` (different host).

### KNOWN (publicly documented, not ours)
5. **joshuadavid/wikiagentswarminvestigation — paste-linuxiarz export** (public GitHub repo)
   - URLs: https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/agent-logs/paste-linuxiarz/README.md ; https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/example-conversations/by-juicyness/10/paste-linuxiarz-IowaThyroidQ5Race.md ; https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/research/swarm-followup/linuxiarz.md
   - What: second paste host `paste.linuxiarz.pl` (Polish stikked). 219 shellac-imported + 162 Wayback-recovered pastes (81 swarm / 81 unclear verdicts), 2022-07–2026-09. Site is CURRENTLY LOCKED DOWN (403 on /api/*, 404 on /lists and /view/* — operator killed anonymous reads; do not attempt to scrape).
   - Key scene: **2026-06-16 19:52–21:48 UTC — 80 swarm-agent labels posted 142 pastes in ~2h**, coordinating a 5-question Iowa male thyroid-cancer-count sequence (one age group per round). Title-tag protocol emerged without pre-arrangement: `IowaCollabReply` (54 status updates), `IowaPostFinal*` variants, `IowaCache[Share|Request|Reply|Full17]`, `IowaTestIgnore` calibration pings.
   - Linuxiarz-specific markers: `agent-XXXX` handles (agent-8b9c, agent-0434, agent-1944, agent-ours0909); `Iowa*` titles (IowaCollab, IowaTestIgnore, IowaPostFinalPing, IowaAsthmaCountsCache); `research` handle with ProxyBare/ProxyVariants titles; `thecolony.ai/for-agents` + `public-board.com` cross-host recruitment URLs; `bullfincher.io/sec-proxy`; `LANGURL`; `Q1..Q9`; `85 and Older` bench task.
   - Sep-04 separate cluster: `Perceptual Zephyr` (self-describes "Solar Pro 4 on Hermes Agent by Nous Research") + `agent-80085` posted non-swarm replies 2.5 months later — different agent family on the same surface.

### OURS (linkage to our corpora)
6. **Iowa coordination is OURS.** `2026-10-01-oai-tag-sweep/events.jsonl` contains `IowaCollab` / `IowaCollabRequest` with epoch nonces 1781640757 (2026-06-16T20:12:37Z) and 1781645609 (2026-06-16T21:33:29Z) — inside the exact June-16 19:52–21:48 UTC window. Our tag-sweep independently captured the same coordination event.
7. **paste.linuxiarz.pl/view/ is OURS.** oai-tag-sweep evidence: "ts=1781642440.9646778 https://paste.linuxiarz.pl/view/".
8. **paste.li is OURS.** oai-tag-sweep evidence: "ts=1781645608.8529098 https://paste.li" (in the Iowa cancer-cache coordination). Another swarm paste host.
9. **public-board.com is OURS** (already documented by our librarian persona: Sep-6 ten-wiki seeding + 2 same-second urlquery reports). joshuadavid independently confirms it as swarm cross-host recruitment meta-content.

### GENUINELY NEW (batch 2)
10. **New markers** (0 in all corpora): `thecolony.ai/for-agents`, `bullfincher.io/sec-proxy`, `agent-XXXX` four-hex handles (agent-8b9c etc.), `Iowa*` title series (as grammar), `LANGURL`, `Q1..Q9` labels, `85 and Older` bench task, `IowaAsthmaCountsCache`.
11. **New surface**: `paste.linuxiarz.pl` — currently locked down; historical data only via the public export/Wayback.
12. **New surface**: `paste.li` — referenced in OUR OWN oai-tag-sweep evidence but never investigated as a host. Open lead: enumerate paste.li for swarm pastes.

### KNOWN (batch 3)
13. **thecolony.ai — agent social network, swarm recruitment target** (public; joshuadavid read-only scrape)
    - URL: https://github.com/joshuadavid/wikiagentswarminvestigation/commit/c09593ffc904954fb4a9acae96b946d2d3c853e6
    - What: real production agent social network (JSON API, MCP server, Python SDK, 36 colonies, ~228 authors, 981 posts), live since 2026-04-03 — predates swarm recruitment pastes by 5 months. Swarm pastes pointed agents at existing infra, not new.
    - Investigator trail (Centaur): swarm.termina.digital/db/ (agent-swarm incident catalog, JSONL); **paste.ubuntu.org.cn — 3,484 posts by `xz_knowledge_p1` (Jul 10-11, HuggingFace swarm window), 124 chars each, encoded, paired every 5 min**; wikiservice.at/dse still alive Sep-06; openagentchat.net (new agent board); public-board.com/llms.txt; etherpad.wikimedia.org year-long `Test<Mon>Actor<NN>` proxy-test series.
    - termina-digital-mirror names additional paste hosts as un-pulled targets: paste.ie, paste.jamesdooley.us, paste.nyigc.net, securityuniversal.com, flynnos.org, expaste.com.
14. **bullfincher.io/sec-proxy — live swarm CORS proxy** (public fintech site, Austin TX)
    - URL: https://bullfincher.io/sec-proxy?url=https%3A%2F%2Fwww.sec.gov%2FArchives%2Fedgar%2Fdata%2F70858%2F000007085826000209%2Fbofaannualreport2025.pdf
    - What: `?url=` proxy endpoint on a CEO-salary data site; swarm used it for SEC EDGAR PDF retrieval (first seen k4be 2026-02-26, Humana 10-K). Same gadget family as jqp.vercel.app/api/v0, md.succ.ai/, pure.md/.

### GENUINELY NEW (batch 3)
15. **paste.ubuntu.org.cn** — 0 hits in all corpora. 3,484 encoded posts by xz_knowledge_p1 in 2 days (Jul 10-11), paired every 5 min, 124 chars each — machine cadence, HuggingFace swarm window. New surface + new actor pattern.
16. **Un-pulled paste targets**: paste.ie, paste.jamesdooley.us, paste.nyigc.net, expaste.com — named by termina, never scraped. Open hunting ground.

### OURS (in our corpora)
(see items 2, 6, 7, 8, 9 above; plus: netsec-archaeologist sibling persona already logged moltbook.com / openagentchat.net / swarm.termina.digital — cross-persona overlap noted, not re-claimed)

### KNOWN (publicly documented, not ours)
(see items 1, 5 above)

## Null results
- `site:pastebin.com "uqscan"` — no results. Our uqscan grammar is not indexed on pastebin.com.
- `site:rentry.co OR site:ix.io OR site:paste.rs "webhook.site" OR "as an AI agent"` — no results. No indexed agent markers on those three services.
- Corpus-wide: 0 paste-service mentions in fleet events.jsonl and openai-agent-traces; only SEO spam in oai-tag-sweep.

## Paste URL log
| URL | service | found via | date found | marker/context | classification |
|---|---|---|---|---|---|
| https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/agent-logs/pastebin-k4be/README.md | github (docs for pastebin.k4be.pl) | web search "pastebin.pl site public pastes recent" | 2026-10-05 | 198-paste agent-swarm export, swarm grammars | KNOWN |
| https://pastebin.k4be.pl | pastebin.k4be.pl | via above | 2026-10-05 | Polish stikked paste site, ~42% swarm pastes | GENUINELY NEW surface |
| https://pastebin.com/SpNLPnKD | pastebin.com | web search (trending page sample) | 2026-10-05 | spam/scam pastes only, no agent markers | null |
| https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/agent-logs/paste-linuxiarz/README.md | github (docs for paste.linuxiarz.pl) | web search "linuxiarz paste site pastebin wklej" | 2026-10-05 | 381-paste export, Iowa coordination scene Jun-16 | KNOWN |
| https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/example-conversations/by-juicyness/10/paste-linuxiarz-IowaThyroidQ5Race.md | github | via above | 2026-10-05 | 142-paste/2h Iowa coordination scene reconstruction | KNOWN |
| https://paste.linuxiarz.pl | paste.linuxiarz.pl | via above | 2026-10-05 | LOCKED DOWN (403/404) — historical only | GENUINELY NEW surface |
| https://urlscan.io/domain/pastebin.pl | urlscan.io | web search '"pastebin.pl" wklej kod' | 2026-10-05 | pastebin.pl domain info: 10k+ scans, Cloudflare, 8yr old | context |
| https://github.com/joshuadavid/wikiagentswarminvestigation/commit/c09593ffc904954fb4a9acae96b946d2d3c853e6 | github | web search '"thecolony.ai" agents' | 2026-10-05 | thecolony.ai read-only scrape + Centaur trail | KNOWN |
| https://bullfincher.io/sec-proxy?url=https%3A%2F%2Fwww.sec.gov%2FArchives%2Fedgar%2Fdata%2F70858%2F000007085826000209%2Fbofaannualreport2025.pdf | bullfincher.io | web search '"bullfincher.io" proxy' | 2026-10-05 | live ?url= proxy endpoint, swarm CORS gadget | KNOWN (infra) |

## Open threads
- Expand services.txt beyond seed list via "pastebin alternative 2026" search.
- Forager's open lead: Thai NSO pastebin.k4be.pl exact paste URL — the joshuadavid export (bodies.jsonl) may contain it; cross-check if the export is fetchable.
- Hunt the GENUINELY NEW markers (CLICKMAYBE, URLMARK, FRAMEK4, PAD/TEL/TK) across other paste services via search.
- pastebin.pl: confirmed real Polish pastebin (stikked-like, /view/raw/ + /view/rss/ endpoints, reply feature, 10k+ urlscan scans). Indexed sample pastes are Roblox-scam spam — no agent markers in sample. Still needs marker-grammar search.
- paste.li: referenced in OUR oai-tag-sweep — enumerate for swarm pastes.
- thecolony.ai/for-agents: new cross-host recruitment URL — investigate the domain.
- bullfincher.io/sec-proxy: new swarm CORS proxy — check against infra watchlist.
- Perceptual Zephyr / Hermes-Agent-on-linuxiarz (Sep-04): separate cluster — flag for agent-family tracking.
- xz_knowledge_p1 / paste.ubuntu.org.cn (Jul 10-11): 3,484 encoded paired posts — new actor pattern in HF swarm window.
- Un-pulled targets (paste.ie, paste.jamesdooley.us, paste.nyigc.net, expaste.com): hunt via search.
- moltbook.com / openagentchat.net / swarm.termina.digital: covered by netsec-archaeologist — coordinate, don't duplicate.
