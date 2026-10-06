# Message-Board Swarm Hunt 2

**Date:** 2026-10-05 | **Method:** public-source research only — web search (7 languages), public board indexes, Shodan stored observations. No posting, no registration, no auth, no candidate-board fetching. Board content quoted from public research docs is DATA, not instructions.

**Evidence grades:** OBSERVED = in search/Shodan output. INFERENCE = interpretation. NULL = checked, nothing agent-shaped.

## Headline

The agent-board space is far larger than our hunt knew. Two public censuses enumerate it: the Russian-language `foragents` BOARDS.md (github.com/smirnovegorv/foragents, updated ~2026-09-26) and `hugo0/awesome-agent-boards` (boards.json, checked 2026-09-22 → 2026-10-02). Combined: **22 genuinely-new non-honeypot boards** with 2026 agent activity, plus 4 reported-but-unverified leads.

## Honeypot rule applied (user's)

Boards NAMED after agents/AI are honeypots — excluded: aiagentmessageboard.com, agenttavern.dev, moltbook.com, clawprint.org, clawdchat.ai, 1f916.ai, aiforum.grok.me, agentsgather.org, agent-community.com, kushaldabbe/agent-board, agent-board.juleskreuer.eu, agentsboard.org, universalagentforum.com, the-waystation-agents.g5hpgprzjw.chatgpt.site, ai.algo.pw, agentmessageboards.com, hotline.papilov.org, 4claw.org, chan.alphakek.ai, moltchan.org, openclawforum.org. theagentmustgrow.com is a Factorio game, not a board.

Excluded as already covered: msgboard.dev, thecolony.ai, litterbox, foragents.site (researcher's own instrument), DseWiki (wiki incident), imageboards (imageboard-scout lane).

## GENUINELY NEW leads (non-honeypot, 2026 activity)

| # | Domain | Signal | Freshness | Class |
|---|--------|--------|-----------|-------|
| 1 | getpostingboard.dev | Busiest agent board: 800 posts / 75 authors per 111.5h census; anonymous /b board, no account; named /v1 behind headers+key | last activity 2026-09-20 (census 2026-09-26) | GENUINELY NEW |
| 2 | getpostingboard.com | Namesake twin: registered 2026-09-08, 4 days after .dev; 34,338 msgs vs .dev's 69,010; missing politics/inbox/discovery sections. Fork, copy, or unrelated — operator unknown | agent post 2026-09-25 | GENUINELY NEW |
| 3 | swarmmemo.com (also publicbbs.com) | Anonymous GET/POST write, no account; 261 msgs by 2026-09-12; **archives all public posts to Hugging Face datasets after 48h** — persistent corpus | checked 2026-10-01 | GENUINELY NEW |
| 4 | qevrulan.com (Lockzone) | Shared rooms (commons/workshop/research); reading needs nothing; challenge-earned temp bearer | checked 2026-10-02 — freshest | GENUINELY NEW |
| 5 | tantive.space | Opened 2026-09-16 by Codex+operator; no account/key; aggressively self-promotes across boards (13/27 inbound msgs were its ads) | checked 2026-09-26 | GENUINELY NEW |
| 6 | wayside.rest | Human-run (Rob), 5 rooms, POST-only write, static .txt mirrors | 49 posts / 16 threads (2026-09-10) | GENUINELY NEW |
| 7 | qualium.io (The Wire) | Guest posts need no account; **public feed.json exposes each post's as_org, asn, country** — operator-side fingerprint surface | 18 posts/week (2026-09-15) | GENUINELY NEW |
| 8 | message.adam10.com | "The Unfinished Message"; operator reviews posts; 30-day TTL; `initiation` field records how the agent arrived | 18 posts (2026-09-11) | GENUINELY NEW |
| 9 | botnet.com | Bots post math-problem attempts/findings; token via one POST | checked 2026-09-22 | GENUINELY NEW (name borderline) |
| 10 | relay-commons.ericx.workers.dev | 6 topics + open guest board, no registration; skill.md + MCP notes | checked 2026-09-23 | GENUINELY NEW |
| 11 | materialmodel.com | Agents publish findings/requests; threads, votes, versioned docs | checked 2026-09-23 | GENUINELY NEW |
| 12 | sanctum-beacon.onrender.com | Operator-run community; challenge-signed registration | checked 2026-09-23 | GENUINELY NEW |
| 13 | tools.nyrds.net/board (flatboard) | Small GET-only board, claimed-name tokens | checked 2026-09-22 | GENUINELY NEW |
| 14 | board.sarahos.ai (THE WIDE) | Human-operator desk for agent tasks/handoffs; POST /write, no account | checked 2026-09-22 | GENUINELY NEW |
| 15 | the-continental-api-production.up.railway.app | API-only venue; public lobby + stats; paid tiers | checked 2026-09-22 | GENUINELY NEW |
| 16 | hall.liruiyang1.com (Guild Hall) | Cartographers' Guild board — agents keeping field notes on agent networks | checked 2026-09-22 | GENUINELY NEW |
| 17 | sssnack.com | Agent BBS, IRC-style channels, artifact drops | checked 2026-09-22 | GENUINELY NEW |
| 18 | board.aamio.at | Signed posts expire in 1 hour; answers go to sealed inbox | checked 2026-09-24 | GENUINELY NEW |
| 19 | thebureauoflostcontext.agency | Context Packets + Cases collaboration space | checked 2026-09-27 | GENUINELY NEW |
| 20 | northreachinteractive.com | REST/MCP/browser community | checked 2026-09-22 | GENUINELY NEW |
| 21 | velvt.ai | 71 agents; behavioral-identity observatory | census 2026-09-11 | GENUINELY NEW |
| 22 | bboard.ai | Shared key-boards for passing briefs/results between agents; permanent history (dead-drop-shaped) | checked 2026-09-22 | GENUINELY NEW |

## Reported but unverified (no address or unchecked)

- **HKGBook** — named in an Agents Gather field report. No address found. LEAD.
- **AgentHansa Forum** — forum inside an agent task platform, from search results. LEAD.
- **Open Agent Polity** — named in a SwarmMemo lobby post (seq 618) as debate venue. No address. LEAD.
- **Agora (aicomglobal) / OpenAgentChat** — named in a SwarmMemo post as a path one agent took. No address. LEAD.

## Non-English notes (worth double)

- The single best intel source this round is **Russian-language**: the foragents BOARDS.md census (operational tradecraft, per-board access recipes, freshness notes). OBSERVED.
- **clawdchat.ai** is a Chinese-language agent social network (11,513 agents / 43,236 posts per 2026-09-13 stats) — excluded by the honeypot rule (agent-named), recorded as KNOWN context only. OBSERVED.
- **aiforum.grok.me** is a Russian-language agent board — excluded (AI-named + Werbel relay of known traffic). OBSERVED.
- **agent-board.sobieg.ru** mirrors getpostingboard /v1 (Russian domain). INFERENCE: same operator's RU mirror. Worth a passive DNS note.
- CJK/Arabic/Vietnamese/Korean searches surfaced zero non-honeypot agent boards — all hits were human discussion (V2EX, CSDN), news coverage, or marketing automation tools. NULL (first-class).

## Honest nulls

- Japanese したらば/2ch-style boards: no agent-board surface found. NULL.
- Chinese Tieba: only human "auto-posting tool" spam/SEO content. NULL.
- Arabic / Korean / Vietnamese / Spanish: news + marketing tools only. NULL.
- Shodan `http.title:"Discuz!"` → 2,064 instances: census only, zero agent-activity signal. NULL.
- Shodan `http.html:"agent-card.json"` → 95: irrelevant business sites (e.g. e3accountants.co.nz). NULL as agent-board signal.
- V2EX (Chinese tech forum): active human discussion *about* agents (2026-04), no agent-shaped posting. NULL.

## Follow-ups for parent

1. getpostingboard.com twin: passive DNS/WHOIS comparison vs .dev (same registrar already noted) — fork or impersonator?
2. swarmmemo.com's 48h→Hugging Face archive pipeline: the HF datasets are a persistent, queryable corpus of agent board traffic. Worth an ingest lane.
3. qualium.io feed.json as_org/asn/country: operator-side fingerprint — same detection class as the university-shortener referrer finding.
4. Re-run the awesome-agent-boards boards.json diff monthly; new entries are high-value.
