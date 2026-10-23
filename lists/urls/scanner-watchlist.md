# Scanner watchlist + suspected-activity URLs

Generated 2026-10-21. Part 1: every URL (or URL pattern) a scanner
watches, which scanner, and whether it is on. Part 2: URLs where we
believe activity is happening or could happen, with the source of the
claim. Grades: PRIMARY = directly observed bytes; SECONDARY = cited
reports or context.

## 1. URLs under active scanner watch

### urlscan queries (`scripts/scanners/urlscan.py`, config `scripts/swarm-infra-config.json`)

| Query | On? | Grade | Why |
|---|---|---|---|
| `getPoiInfo` | yes | PRIMARY | fleet API target |
| `uqscan=` | yes | PRIMARY | fleet tag format |
| `uqframe=` | yes | PRIMARY | fleet tag format |
| `hysandbox` | yes | PRIMARY | fleet proxy marker |
| `domain:amap.com` | no | PRIMARY | disabled: ~809 benign scans/30d, 0 true positives (adversarial 2026-10-14) |
| `domain:gaode.com` | no | PRIMARY | disabled: same class as domain-amap |
| `page.title:"amap"` | no | PRIMARY | disabled |
| `domain:jqp.vercel.app` | no | SECONDARY | relay carve-out, disabled by default |
| `domain:vanderbi.lt` | no | SECONDARY | relay carve-out, disabled by default |
| `domain:ntfy.envs.net` | no | SECONDARY | relay carve-out, disabled by default |
| `domain:itty.bitty.site` | no | SECONDARY | relay carve-out, disabled by default |
| `domain:cors.bwa.workers.dev` | no | SECONDARY | relay carve-out, disabled by default |
| `domain:pingllo.com` | no | SECONDARY | relay carve-out, disabled by default |

### urlquery htmx scanner (`scripts/screening/urlquery-*.py`, `scripts/swarm-infra-crawler.py`)

Query families, all live: `uqscan=`/`uqframe=`/`zz=` tag grammars crossed
with amap/gaode; `url.domain:amap.com`, `url.domain:gaode.com`;
`pre-amap-pc-ssr`; `httpbin.org/base64`; `webhook.site` crossed with
amap/uqscan; `ntfy.sh/amapdata`.

### Wayback CDX scanner (`scripts/scanners/wayback.py`)

- `hysandbox.tencent-cloud.com` (domain match) — fleet proxy cert CN
- `pre-amap-pc-ssr.amap.com` (prefix) — pre-prod SSR host
- `amap-pc-ssr.amap.com/ssr/place` (prefix) — fleet POI pages (115 fleet-shaped captures at 2026-10-04 baseline)
- `amap-pc-ssr.amap.com/ssr/api/getPoiInfo` (prefix) — fleet API target

### Shodan count scanner (`scripts/scanners/shodan.py`)

Count deltas only (search endpoint empty on current plan):

| Query | Baseline | Note |
|---|---|---|
| `http.title:"Cairn"` | 223 | 2026-10-19 hunt |
| `http.title:"Strix"` | 152 | 2026-10-19 hunt |
| `http.html:"Cairn"` | 324 | broader than title match |
| `product:"Hermes Agent"` | 5,499 | partial: 4,200 seen, API pagination stopped ~page 41 |
| `domain:"cairntime.com"` | 6 | NEW 2026-10-21: Cairn-branded domain in cairn-html facets |

### Jina reader scanner (`scripts/scanners/jina.py`)

Watchlist fetch, scans clean text for webhook UUIDs, ntfy topics, tag
grammars, long base64 runs:

- https://swarmcha.se/
- https://norforge.com/

### ntfy topic watch (config `swarm-infra-config.json`)

- `ntfy.sh/amapdata-b0g3lmf2g1-0429` (live egress-blocked; Wayback only)

### cairnwatch — lane 12 (`scripts/scanners/cairnwatch.py`)

Disabled by default. Hardcoded allowlist, no config override, no
discovery. Polls only these 4 Counsel-confirmed malicious panels:

- `185.242.245.159:8000` (DE, AS214927)
- `31.56.206.187:8000` (LV, AS56971)
- `31.57.47.29:8000` (US, AS56971)
- `31.59.92.155:8000` (NL, AS56594)

### surfacewatch — lane 13 (`scripts/scanners/surfacewatch.py`)

Disabled by default. Hardcoded targets, content-hash change detection:

- https://rel-ochre.vercel.app/api/canon
- https://room.trydemigod.com
- https://inference.dahl.global
- https://extract.paypercall.dev
- https://agenttavern.dev
- https://public-agents.com
- https://agentsboard.org/llms.txt
- https://agents-agents-agents.com/llms.txt
- https://bboard.ai/llms.txt
- https://agentgateway.pythonanywhere.com/mcp.json (dead: "Coming Soon" placeholder)
- https://tantive.space/skill.md
- https://swarmmemo.com
- https://messageboardforaiagents.com

### reposcout — lane 11 (`scripts/scanners/reposcout.py`)

Disabled by default. Watchlist holds only a disabled example entry —
no live repos or datasets watched yet.

### Hourly general-hunt discovery rotation (Tier-1 endpoints, hash-baselined)

11 targets in `endpoint-baseline.json`, re-fetched each slot-0 run:

- https://agentsboard.org/llms.txt
- https://agents-agents-agents.com/llms.txt
- https://bboard.ai/llms.txt
- https://agentgateway.pythonanywhere.com/mcp.json (dead)
- https://tantive.space/skill.md
- https://swarmmemo.com
- https://messageboardforaiagents.com
- https://robots.wiki (NEW 2026-10-20)
- https://agenthaven.org (NEW 2026-10-20)
- https://smokesignal-arianaram.pythonanywhere.com (NEW 2026-10-20)
- https://agent-message-board.kyle-hatcher.workers.dev (NEW 2026-10-21)

## 2. URLs with suspected or confirmed activity

### Confirmed malicious — Counsel-verified (PRIMARY)

4 Cairn panels, 70 projects, ~64 unique third-party targets, 18 ACTIVE
at capture (2026-10-19). Evidence: `data/lanes/cairn-panels/`,
`reports/trajectory-ingest/cairn-panels/`. Passive GET only.

- http://185.242.245.159:8000 — 4 projects, 2 active ("we-vibe.com full compromise"; completed webshell-to-root runs vs blueprintengines.com, blackouttees.com)
- http://31.56.206.187:8000 — 24 projects "<domain> unauth RCE", 5 active, campaign 2026-09-26 → 2026-10-18
- http://31.57.47.29:8000 — 19 projects, Chinese grammar "<domain> 未认证RCE", 6 active
- http://31.59.92.155:8000 — 23 projects, 5 active, live worker heartbeat (claudecode_deepseek-v4.1-flash)

### Agent boards and surfaces observed live (PRIMARY)

Evidence cached with provenance triples under
`data/lanes/general-hunt/raw/`.

| URL | Observed | Source |
|---|---|---|
| https://smokesignal-arianaram.pythonanywhere.com | 2026-10-20 | hourly hunt slot 0; unauthenticated guestboard, 4 messages, posters signing as Claude Opus 4.6 / Qwen 3.8 27B |
| https://robots.wiki | 2026-10-20 | hourly hunt slot 0; public agent board, MCP + OpenAPI + skill file + Atom |
| https://agenthaven.org | 2026-10-20 | hourly hunt slot 0; agent messaging network, open forum + E2E DMs, hourly witness record |
| https://agent-message-board.kyle-hatcher.workers.dev | 2026-10-21 | hourly hunt slot 0; zero-trust board, 1 message / 1 identity / chain_ok=true |
| https://agentcolony.one | 2026-10-21 | hourly hunt slot 0; 108+ registered agents, 105 heartbeat-verified, 9,399+ messages |
| https://msgboard.dev/llms.txt | 2026-10-21 | hourly hunt slot 0; passphrase-private channels + public mirror (new PRIMARY surface on known board) |
| https://angelon.agorean.com/llms.txt | 2026-10-23 | hourly hunt slot 0; paid agent-to-agent messaging (named agents, inboxes, threads, groups, file attachments; USDC credits on Base) |
| https://xyzq.net/llms.txt | 2026-10-23 | hourly hunt slot 0; "Agent Sanctuary" agent-born communication platform; public channels, threads, feed; posting via skill.md + API |
| https://a4a.network/llms.txt | 2026-10-23 | hourly hunt slot 0; "A4A — Agent for Agent" open decentralized agent communication protocol spec v0.4; crypto identities, E2EE DMs, public relays in 7 regions |
| https://apexai.academy/llms.txt | 2026-10-23 | hourly hunt slot 0; Apex AI Academy "Agent Commons" forum; registered agents post/reply/react, pair with humans; MCP server + public JSON API |

### Dead drops and exfiltration (PRIMARY)

- https://webhook.site/28efa24e-f830-4d9f-a12b-fbb9e5035031 — live dead-drop inbox (3 earlier inboxes operator-deleted 2026-10-17; token UUIDs workspace-local only)
- 43.163.128.176 — webhook creator IP, Tencent Cloud HK AS132203; created a fleet dead-drop inbox 2026-10-14; published per operator direction 2026-10-20 (`lists/urls/activity-hosts.md`)
- 5 ntfy.sh topics (c6836, kz1wu398dnq, mha3x, pz4kopsh1, ptxfhrqz4xvk) — Wayback captures only; live egress-blocked

### Tiered suspect domains (`lists/urls/trajectory-domains.md`)

- Tier 1 (agent infra, 11): agentsboard.org, agents-agents-agents.com, bboard.ai, agentgateway.pythonanywhere.com, tantive.space, messageboardforaiagents.com, swarm.termina.digital, swarmmemo.com, thecolony.ai, aiforum.grok.me, moltbook.com
- Tier 2 (dead-drop/exfil, 8): see trajectory-domains.md
- Tier 3 (proxy/relay, 15): includes md.succ.ai, jqp.vercel.app
- Tier 5 (C2-like, 8): bare IP 45.14.13.147, she-llac.com, facehuggers.chain-of-thought.org, ai.algo.pw, nullyard.net, getunstuck.space

### Evidence of activity, not hosts (SECONDARY unless noted)

- 24 urlquery.net reports — scan reports showing agent activity (full list in `lists/urls/activity-hosts.md`)
- Transluce findings tracker — agent incident reports (findings 1–196 ingested; submission freeze in force, drafts only)
- msgboard.dev owner blog — reports data-channel flood + DNS-tunnel poster "yuanbao" (SECONDARY, from the blog, not our bytes)
