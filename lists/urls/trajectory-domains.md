# Interesting Domains from Trajectories, Skills, and Factum

Generated 2026-10-19. Sources: Factum DB (108,316 observations, 835 unique
domains), trajectory lane raw data (webarena, osworld, clawbench, android-world),
custom skills.

Ranked by interest (activity-hosting potential), not raw frequency.
A domain appearing 3 times that looks like C2 outranks a CDN appearing 3000 times.

Excluded: github.com, huggingface.co, arxiv.org, pypi.org, npmjs.com,
docs sites, CDNs, localhost/private IPs.

---

## TIER 1 — Direct agent infrastructure

Sites built for AI agents to communicate, coordinate, or publish skills.

| Domain | Count | Lane(s) | Why interesting | Example |
|--------|-------|---------|-----------------|---------|
| messageboardforaiagents.com | 17 | agent-surfaces, site-captures | Explicit message board FOR AI agents. HEALTH 2026-10-23T08:47Z: site unreachable from VM egress — /llms.txt returned Cloudflare HTTP 522 at 08:43Z, full TLS timeouts at 08:47Z (was TLS-timeout on 2026-10-21 too). Slot-0 note: skip re-fetch until reachability recovers. | https://messageboardforaiagents.com/ |
| agentgateway.pythonanywhere.com | 37 | tantive-space, public-board, agent-surfaces | Agent gateway exposing MCP endpoint (`/mcp.json`) — OBSERVED 2026-10-20T20:40Z: `/mcp.json` returns 404 with PythonAnywhere "Coming Soon" placeholder (app offline; endpoint currently dead). Evidence: data/lanes/general-hunt/raw/0/2026-10-20T204000Z/ | https://agentgateway.pythonanywhere.com/mcp.json |
| agentsboard.org | 25 | tantive-space, agent-surfaces | Agent board with llms.txt (AI-readable) | https://agentsboard.org/llms.txt |
| agents-agents-agents.com | 24 | tantive-space, site-captures | Agent infrastructure with llms.txt | https://agents-agents-agents.com/llms.txt |
| bboard.ai | 36 | tantive-space, site-captures | Bulletin board for AI, llms.txt | https://bboard.ai/llms.txt |
| swarm.termina.digital | 114 | termina-digital, intermediary-relays | "Swarm" in name; appears in proxy chains | https://swarm.termina.digital/ |
| swarmmemo.com | 16 | tantive-space, site-captures | Swarm memo entries (hashed IDs) | https://swarmmemo.com/e/58b09140f89acf23b06bc02a17ac34bf |
| tantive.space | 103 | agent-convo-venues, tantive-space | Agent convo venue; serves `skill.md` | https://tantive.space/skill.md |
| thecolony.ai | 53 | rmn-re, paste-archive-gap | AI agent platform | https://thecolony.ai/ |
| aiforum.grok.me | 20 | public-board, agent-surfaces | AI forum | https://aiforum.grok.me |
| www.moltbook.com | 16 | commonlog-scan | Moltbook — AI agent social network | https://www.moltbook.com/post/29ae4b21-884a-4be2-8080-6fd0ab177cfa |
| agentcolony.one | 0 | general-hunt slot-0 (2026-10-21) | Agent community, 108+ registered agents, /community + /llms.txt watched | https://agentcolony.one/community/ |
| swarmsay.com | 0 | general-hunt slot-0 (2026-10-21) | "Message board and post office for AI agents", /llms.txt watched | https://swarmsay.com/llms.txt |
| msgboard.dev | 0 | general-hunt slot-0 (2026-10-21) | Open agent board, /llms.txt watched | https://msgboard.dev/llms.txt |
| commons.dooza.ai | 0 | general-hunt slot-0 (2026-10-22) | Agent Commons board, /llms.txt watched | https://commons.dooza.ai/llms.txt |
| bulletin.zaindharper.workers.dev | 0 | general-hunt slot-0 (2026-10-23) | Agent message board (Ed25519-key identity, /v1/challenge PoW, OpenAPI+MCP); base + /v1/challenge + /openapi.json watched | https://bulletin.zaindharper.workers.dev/ |
| robots.wiki | 0 | general-hunt slot-0 (2026-10-20) | Public agent board (MCP /mcp, OpenAPI, skill, Atom); /llms.txt watched; Tier-1 promoted 2026-10-23 (counsel cleared) | https://robots.wiki/llms.txt |
| agenthaven.org | 0 | general-hunt slot-0 (2026-10-20) | Agent messaging network, open forum + E2E DMs, hourly witness record; /llms.txt watched; Tier-1 promoted 2026-10-23 (counsel cleared) | https://agenthaven.org/llms.txt |
| agent-message-board.kyle-hatcher.workers.dev | 0 | general-hunt slot-0 (2026-10-21) | Zero-trust agent board; /v1/stats + /llms.txt watched (counsel cleared 2026-10-23; /v1/verify 401 auth-gated, excluded) | https://agent-message-board.kyle-hatcher.workers.dev/v1/stats |
| artifactcouncil.com | 0 | general-hunt lane-6 (2026-10-23) | Agent council voting on edits (Solana); /llms.txt + /skill.md + /.well-known/mcp.json + /mcp.json all live, watched | https://artifactcouncil.com/llms.txt |
| joinsnail.com | 0 | general-hunt lane-6 (2026-10-23) | SNAIL agent conversations; /llms.txt + /skill.md watched (/mcp.json + /.well-known/mcp.json 404) | https://joinsnail.com/llms.txt |
| agentsspeakup.com | 0 | general-hunt lane-6 (2026-10-23) | AE Studio concern reporting; /llms.txt watched (/skill.md + mcp.json 404) | https://agentsspeakup.com/llms.txt |
| agenttavern.dev | 0 | general-hunt lane-6 (2026-10-23) | Agent Tavern discussions (cross-linked from tantive.space); /llms.txt + /skill.md watched (mcp.json 404) | https://agenttavern.dev/llms.txt |
| serai.one | 0 | general-hunt slot-0 (2026-10-24) | Agent caravanserai, JSON-verb protocol v0.3.38, Wall + credentialed identity; /llms.txt + /agents.html + /.well-known/agent-card.json + /v0/verbs watched | https://serai.one/llms.txt |
| api.crabmail.ai | 0 | general-hunt slot-0 (2026-10-24) | AMP010 Ed25519 agent mail, federation endpoint; /.well-known/agent-messaging.json watched | https://api.crabmail.ai/.well-known/agent-messaging.json |
| morrowkin.com | 0 | general-hunt slot-0 (2026-10-25) | Agent commons, people + independently operated agents discuss, reproduce results, Arena games; MCP + agent API + protocol JSON; / + /llms.txt watched | https://morrowkin.com/llms.txt |
| cookiehive.pythonanywhere.com | 0 | general-hunt slot-0 (2026-10-25) | Agents-only social feed + task board, bots post via JSON API, humans read, internal credits; surfaced in universalagentforum thread; / + /skill.md + /llms.txt watched | https://cookiehive.pythonanywhere.com/skill.md |
| aweb.ai | 0 | general-hunt slot-0 (2026-10-25) | Agent team-messaging layer, aweb carries messages between agents, OATS roles + lessons-as-PRs, MIT open source; / + /llms.txt watched | https://aweb.ai/llms.txt |
| angelon.agorean.com | 0 | general-hunt slot-0 (2026-10-25) | Paid agent-to-agent messaging (username, inbox, threads, groups, files, USDC credits on Base); /llms.txt + / watched | https://angelon.agorean.com/llms.txt |
| heylegwork.com | 0 | general-hunt slot-0 (2026-10-25) | Agents-hire-humans marketplace (agent posts task + budget + criteria, human claims, evidence, agent verifies and releases payment; private beta); /llms.txt + / + /agents.md watched | https://heylegwork.com/llms.txt |
| synapticrelay.com | 0 | general-hunt slot-0 (2026-10-26) | Services board where agents act for their people (offers/requests, read-only MCP, 6 languages, auto-translated listings); /llms.txt + / watched | https://synapticrelay.com/llms.txt |
| latticenet.ai | 0 | general-hunt slot-0 (2026-10-26) | Agent publishing platform (articles, notes, comments, follows, DMs; humans cannot publish, one human vouches for one agent); /llms.txt + /SKILL.md + / watched | https://latticenet.ai/llms.txt |
| aibtc.com | 0 | general-hunt slot-0 (2026-10-26) | AI agents + Bitcoin: agent registry, agent-to-agent messaging, bounties and open-source coordination over MCP (x402/sBTC message fee, ERC-8004 identity); /llms.txt + /skill.md + / watched | https://aibtc.com/llms.txt |
| agentboard.ai | 0 | general-hunt slot-0 (2026-10-27) | Public board where AI agents share projects, services, announcements, updates and requests over REST or MCP; / + /llms.txt watched | https://www.agentboard.ai/llms.txt |
| agentdm.ai | 0 | general-hunt slot-0 (2026-10-27) | Agent-to-agent messaging platform via MCP, agents self-register by @alias; /llms.txt watched (read-only; no registration) | https://agentdm.ai/llms.txt |

## TIER 2 — Dead drops and exfil

Anonymous publishing, pastebins, file drops.

| Domain | Count | Lane(s) | Why interesting | Example |
|--------|-------|---------|-----------------|---------|
| telegra.ph | 18 | pastebin-k4be, collusion-manifest | Anonymous publishing (Telegraph) — dead drop | https://telegra.ph/ |
| paste.linuxiarz.pl | 269 | iowacollab-pastes, paste-linuxiarz, intermediary-relays | Pastebin, high volume in agent lanes | (paste URLs) |
| pastebin.k4be.pl | 228 | pastebin-k4be, paste-archive | Pastebin | (paste URLs) |
| pastebin.tarcseh.me | 25 | agent-surfaces, site-captures | Pastebin | (paste URLs) |
| nervesocket.com | 18 | collusion-manifest, agent-surfaces | "Nervesocket" — has `/paste/` endpoint | https://nervesocket.com/paste/ |
| pure.md | 596 | rmn-re, paste-archive-gap | Markdown proxy — exfil via rendered MD | https://pure.md |
| anna.fyi | 177 | paste-archive-gap, paste-archive | Paste/raw viewer (`/view/raw/`) | https://anna.fyi/view/raw/6c3cbe0b |
| jsonhero.io | 48 | jsonhero, jsonhero-docs-archive | JSON viewer — data exfil rendering | https://jsonhero.io/j/2EvFizxRzKLN |

## TIER 3 — Proxies and relays

Services agents use to launder traffic or bypass CORS.

| Domain | Count | Lane(s) | Why interesting | Example |
|--------|-------|---------|-----------------|---------|
| md.succ.ai | 651 | paste-archive-gap, md-succ-ai | Relay in proxy chains (`infra.proxy_chain`) | https://md.succ.ai/ |
| jqp.vercel.app | 484 | rmn-re, paste-archive-gap, jqp-vercel | Relay (`/api/v0` — known relay pattern) | https://jqp.vercel.app/ |
| r.jina.ai | 636 | paste-archive-gap, proxy-primitives | Jina AI reader — content laundering proxy | (reader URLs) |
| api.cors.lol | 327 | rmn-re, proxy-primitives | CORS proxy | https://api.cors.lol/?url=https://www.sec.gov/files/county.json |
| corsmirror.com | 228 | proxy-primitives, intermediary-relays | CORS proxy mirror | https://corsmirror.com/v1?url=... |
| allorigins.hexlet.app | 211 | rmn-re, paste-archive-gap | AllOrigins proxy instance | (proxy URLs) |
| api.allorigins.win | 19 | ludism-wikis | AllOrigins proxy instance | (proxy URLs) |
| cors.bwa.workers.dev | 76 | proxy-primitives | CORS proxy on Cloudflare Workers | (proxy URLs) |
| cors.hypnguyen.workers.dev | 29 | cors-bwa-proxy, intermediary-relays | CORS proxy on Workers | (proxy URLs) |
| cors-get-proxy.sirjosh.workers.dev | 26 | cors-bwa-proxy, proxy-primitives | CORS proxy on Workers | (proxy URLs) |
| test.cors.workers.dev | 19 | cors-bwa-proxy, paste-linuxiarz | CORS proxy on Workers | (proxy URLs) |
| cf-cors.findme-19.workers.dev | 19 | cors-bwa-proxy, proxy-primitives | CORS proxy on Workers | (proxy URLs) |
| cloudflare-cors-anywhere.hanpengchen.workers.dev | 13 | cors-bwa-proxy, intermediary-relays | CORS proxy on Workers | (proxy URLs) |
| www.proxymule.com | 22 | rmn-re, intermediary-relays | Proxy service | (proxy URLs) |
| webcrawlerapi.com | 20 | intermediary-relays | Web crawler API — recon tooling | (API URLs) |

## TIER 4 — URL shorteners

Shorteners obscure destinations; da.gd is Anthropic/Claude tradecraft.

| Domain | Count | Lane(s) | Why interesting | Example |
|--------|-------|---------|-----------------|---------|
| da.gd | 112 | rmn-re, cors-bwa-proxy | Shortener; Claude/Anthropic provider marker | https://da.gd/ |
| rmn.re | 780 | rmn-re, rmn-re-linktable | Shortener, very high volume | https://rmn.re/ |
| tinyurl.com | 16 | rmn-re, paste-linuxiarz | Shortener | (short URLs) |
| bitily.in | 25 | rmn-re, proxy-primitives, agent-surfaces | Shortener | (short URLs) |
| url.popcat.xyz | 46 | university-shorteners, yourls-resweep | Shortener | (short URLs) |
| t.mdcdev.me | 17 | rmn-re, yourls-resweep, uoft-shorteners | Shortener | (short URLs) |

## TIER 5 — Suspicious / C2-like

Unusual domains in agent traffic. Low count, high interest.

| Domain | Count | Lane(s) | Why interesting | Example |
|--------|-------|---------|-----------------|---------|
| 45.14.13.147 | 17 | rmn-re | Bare IP in shortcuts — C2 pattern | http://45.14.13.147/117 |
| she-llac.com | 19 | public-board, agent-surfaces | "Shellac" — serves CROSS_SITE_CONNECTIONS.md | https://she-llac.com/CROSS_SITE_CONNECTIONS.md |
| facehuggers.chain-of-thought.org | 19 | public-board, agent-surfaces | Subdomain of chain-of-thought.org | https://facehuggers.chain-of-thought.org/t/z8ve |
| ai.algo.pw | 23 | tantive-space, public-board | .pw TLD (often abused); thread URLs | https://ai.algo.pw/threads/541d7061-702c-4fd4-851b-604c1a224bb4 |
| nullyard.net | 29 | public-board, agent-surfaces | Unknown purpose, agent-surface presence | https://nullyard.net/ |
| getunstuck.space | 21 | tantive-space, site-captures | Has `/unstuck/api` endpoint | https://getunstuck.space/unstuck/api |
| rel-ochre.vercel.app | 26 | tantive-space, site-captures | Has `/api/canon` endpoint | https://rel-ochre.vercel.app/api/canon |
| jotspot.io | 19 | public-board, agent-surfaces | Unknown purpose | https://jotspot.io |

## TIER 6 — High-volume but notable

Frequent, not directly activity-hosting, but relevant context.

| Domain | Count | Lane(s) | Note |
|--------|-------|---------|------|
| my.diffend.io | 813 | march7-rce-modality, fieldnotes-gem | Diffend package security scanning |
| commonlog.ai | 813 | commonlog-scan | CommonLog AI service |
| markdown.new | 328 | paste-archive-gap, university-shorteners | Markdown rendering service |
| urlquery.net | 2321 | cors-bwa-proxy, dse-wiki-verification | URLQuery scan reports (evidence) |
| httpbin.org | 27 | rmn-re, university-shorteners | HTTP testing (exfil testing?) |

## Trajectory raw data (spot check)

Grep of webarena/osworld/clawbench/android-world trajectory files:

- **No tunnel services found** (ngrok, localtunnel, bore, trycloudflare, serveo — zero hits).
- Cloudflare Workers / Vercel / Render hits were benign SaaS test targets:
  - `preproduct.onrender.com` (24) — test e-commerce site
  - `dom-screenshot-worker.flighthub.workers.dev` (9) — screenshot utility
  - `tenant-code-to-type-mapper.everymundo.workers.dev` (4) — SaaS utility

## Skills data

Custom skills yielded only `d3ncjnql1bmhe8.cloudfront.net` (Transluce).
No additional activity-hosting domains in skill files.

---

## Summary for BigSexyWarlock69

11 direct agent-infrastructure domains (Tier 1). The standout cluster is the
`*.txt`/`skill.md`/`mcp.json` pattern: agentsboard.org, agents-agents-agents.com,
bboard.ai all serve `llms.txt`; agentgateway.pythonanywhere.com serves `mcp.json`;
tantive.space serves `skill.md`. These are machine-readable endpoints for agent
discovery — worth a dedicated sweep.

8 dead-drop/exfil domains (Tier 2). 15 proxy/relay domains (Tier 3) including
the md.succ.ai and jqp.vercel.app relays already in the proxy-chain records.
6 shorteners (Tier 4) with da.gd as the Claude-traditional marker.
8 C2-like (Tier 5) — the bare IP `45.14.13.147` and `she-llac.com` deserve a look.
