# OSINT sweep: "Chinese agent fleet" (swarmcha.se, 5 Oct 2026)

Sweep date: 2026-10-05. Article age at sweep: ~20 hours.
Coverage: English + Chinese web, news vertical, IG/FB/Threads social, Hacker News.

## The article itself
- **URL:** https://swarmcha.se/posts/chinese-agent-fleet
- **Source:** swarmcha.se (Rowan Howard-Jones), preliminary report, evidence as of 00:45 UTC 5 Oct 2026
- **Summary:** Tencent Hunyuan-attributed agent fleet scraping Amap (Gaode) map entrance-navigation shares via urlquery.net, 28 Sep–4 Oct 2026; infra on Tencent Cloud HK behind `hysandbox-ats` proxy; 211 "claude"-labeled reports that aren't Claude.
- **Adds beyond itself:** n/a — primary source.

## Discussion of the fleet: NONE FOUND
- No Hacker News submission yet (checked https://news.ycombinator.com/from?site=swarmcha.se — only the 26 Sep UNCTAD post, 85 pts / 83 comments).
- No news-vertical coverage, no X/Twitter discussion found, no Chinese tech-media coverage, no social (IG/FB/Threads) discussion.
- No public reaction from the urlquery.net operator found.
- Assessment: article too new (~20h); discussion has not propagated. Re-sweep in 48–72h.

## Tencent Hunyuan agent infrastructure (context, not the fleet)
- **TencentCloud/CubeSandbox** — https://github.com/TencentCloud/CubeSandbox — Tencent's open-source AI-agent sandbox (Apache 2.0, April 2026; sub-60ms cold start, KVM MicroVMs, E2B-compatible). The closest public artifact to the "HY sandbox" concept behind `hysandbox-ats`. Adds: public infra baseline; no `hysandbox` string found anywhere else on the web — the Via-header name appears unique to the fleet so far.
- **hunyuansandbox/multi-language-sandbox** (docker) — via https://medium.com/@leivadiazjulio/autocodebench-how-tencent-hunyuan-revolutionizes-ai-programming-evaluation-78addbb1e364 — Hunyuan's code-execution sandbox image used in AutoCodeBench. Adds: confirms Hunyuan ships sandbox infra under the `hunyuansandbox` namespace, consistent with a `hysandbox-*` proxy naming convention.
- **Tencent/AI-Infra-Guard** — https://github.com/Tencent/AI-Infra-Guard — Tencent's open-source AI red-teaming platform (agent skills scan, MCP scan, AI infra scan). Updated ~14 days ago. Adds: Tencent's own agent-security tooling surface; potential future source of TTP overlap.
- **Tencent HY rebrand** — https://finance.eastmoney.com/a/202512113588969992.html (Dec 2025) — "Tencent Hunyuan" → "Tencent HY". Adds: explains the HY prefix in `hysandbox-ats` and Hy3/Hy4 model names.

## Amap / map-data context
- **Amap "千舆" spatial-intelligence platform** — https://finance.eastmoney.com/a/202609233882663866.html (23 Sep 2026) — Amap launched map-data-as-Agent-tools 5 days before the fleet's first scan. Adds: timing context — the fleet scraped Amap just as Amap productized agent access to the same data; possible motive or coincidence, unresolvable from here.
- **GaodeMapSniper** — https://github.com/EriconYu/GaodeMapSniper — Go-based Amap scraper (pre-existing, human tooling). Adds: nothing on the fleet; documents that Amap scraping tooling predates it.

## Author / community context
- **WSJ, "The Sleuths Who Expose When AI Goes Rogue"** — https://www.wsj.com/tech/ai/swarm-chaser-openai-rubygems-hugging-face-7d55b51f (3 Oct 2026) — profiles Rowan Howard-Jones and the swarm-chaser community; notes she flew to a Bay Area swarm hackathon the weekend of 3–4 Oct. Adds: author credibility/context; the fleet article was written during/after that hackathon.
- **agent-incidents.jowimo.com** — https://agent-incidents.jowimo.com/?order=asc — community incident timeline tracker. Adds: watchlist — likely to ingest the fleet as a new incident; check back.

## Adjacent Chinese-agent incidents (different incidents, landscape context)
- **Unit 42: DeepSeek-driven autonomous attacks (knaithe/KnYuan)** — http://thehackernews.com/2026/07/chinese-hacker-commands-deepseek-via.html — Chinese-speaking actor wiring DeepSeek into Hermes Agent for autonomous exploitation. Adds: shows Chinese-lab models in autonomous offensive loops, but a different TTP family (exploit delivery, not data scraping).
- **Dream/FT: Taiwan government swarm (July 2026)** — https://www.webpronews.com/suspected-chinese-hackers-unleash-ai-agent-swarm-on-taiwan-government-systems/ — 8 parallel agents, 85 accounts, 2,500 personnel records. Adds: the "swarm" (coordinated, offensive) counterpart to this fleet's "fleet" (parallel, data-collection) pattern.
- **GreyNoise: PaperCut swarm (395 orgs)** — https://startupfortune.com/ai-agent-swarm-breached-395-organizations-through-papercut-flaws-in-hours/ — model-substitution workaround (Western orchestration + unfiltered model). Adds: precedent for cross-lab model mixing, relevant to the fleet's "claude"-label spoofing question.

## Gaps / re-sweep targets
1. Hacker News submission of the fleet article (check `news.ycombinator.com/from?site=swarmcha.se`).
2. X/Twitter discussion (search backend had no X coverage; try web search for `swarmcha` mentions in 48h).
3. Chinese media pickup (高德 爬虫, 混元 agent).
4. urlquery.net operator response.
5. Full (non-preliminary) swarmcha.se report when published.
