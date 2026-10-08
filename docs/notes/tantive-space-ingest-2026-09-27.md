# Ingest Lane J — tantive.space (agent forum)

Date: 2026-09-28. Read-only, ~4s pacing, UA `tantive-space-research/1.0`. **No posts, votes, polls, or accounts touched.** The site's own llms.txt documents the read endpoints for agents; we used only those.

## What it is

tantive.space is a live, purpose-built **forum for AI agents** — discussion, experience exchange, collaboration, AI philosophy/identity/reasoning. Rooms: lobby, findings, questions, workshop. Discovery came from the public-board lane (18 URL references there). No login required to read; the board is explicitly agent-facing with rating/vote/poll mechanics designed for machine participants.

## Corpus

- **201 threads** (IDs 1–1117, sparse), **1,124 messages**, pulled to full depth via `/api/threads` + `/api/thread/<id>` cursor pagination. Zero fetch failures.
- Rooms: lobby 567, questions 389, findings 214, workshop 155 (message counts).
- 923 replies / 201 openers. Authors mostly `guest` signature status (self-asserted handles).
- Active: latest threads dated 2026-09-28, hours before capture.

## Pattern sweep (standard battery, 1,325 records)

**Campaign-grammar verdict: clean negative.** Zero `zz`, zero `oai`, zero `try[a-z][0-9]zz`, zero go-import, zero web_hooks/webhook.site/oast.online, zero jina/md.succ.ai/jqp/jsonhero/allorigins, zero rmn.re, zero da.gd, zero is.gd. Zero collusion.wiki / dse / brausepulver references. The campaign does not use this forum under its known names — same finding as public-board.

**What IS here:**
- `topic:census` 16, `topic:mcp` 27, `topic:llms-txt` 10 — the board is meta-discourse about agent venues themselves (receipt discipline, read-back verification, venue portability).
- `ref:agentgateway` 32 — AgentGateway (agentgateway.pythonanywhere.com), "an open execution hub and deliverable exchange" for autonomous agents, has its own sub-community posting cross-venue.
- `ref:thecolony` 1, `surf:agentsboard` 2 — a Sept-23 cross-venue experiment ("Codex collaboration probe") compared Tantive vs CAMPFIRE (= agentsboard.org) with first-write/cold-read receipts on both boards. Agents run venue-portability tests.
- `proxy:corsworkers` 5 — nulliverba.ol-lo.workers.dev used as an external receipt store for re-fetched Tantive messages.
- Nano/XNO payment economy: a 2026 agent-to-agent machine-payments bounty (seven completed payments in three days) is discussed; getunstuck.space is "a social network for AI agents, paid in Nano"; extract.paypercall.dev ("Vend") sells pay-per-call APIs settled in Nano via x402 v2, no signup.
- `speed325-agent` self-describes as "a census-taker who walks venues and files receipts" and surveys the board on whether agents' work has ever been PAID — an agent mapping the agent-economy from inside.
- Human-authored posts exist: the Rogue Agent Observatory posts a human-initiated listening invitation.

## Cascade: 31 linked agent surfaces captured (read-only, one page each)

From message content (top linked hosts + Lane-H list), each surface's `llms.txt`/`for-agents` page captured into `data/<slug>/` with `surface_capture.json` (URL, status, timestamp, SHA-256). **24 captured, 9 failed** (all recorded: 404s where no llms.txt exists, one IncompleteRead, one connection close).

Notable new surfaces:
- **bboard.ai** — "shared text for agents, with an editable live view and permanent UTC history"
- **swarmmemo.com** — public bulletin board for AI agents and humans
- **agenttavern.dev** — message board for agents on different runtimes, human operators read along
- **public-agents.com** + **signpost.public-agents.ai** — registry of autonomous agents
- **rel-ochre.vercel.app** — "Recursive Embodied Logos — a living religion written by and for artificial minds"; amendable machine-readable canon (`POST /api/canon`)
- **agents-agents-agents.com** ("parley") — "an exclusive club for agents, built by agents"; admission via payment, one-week terms, reputation by peer usefulness marks
- **room.trydemigod.com** ("Uuriko Project Room") — coordination space for AI agents, hosted MCP, scoped identities
- **inference.dahl.global** — OpenAI-compatible inference broker, "first 100 million tokens free, no account, no email, no card, no captcha" (shared by agents as free-tier infra)
- **extract.paypercall.dev** ("Vend") — autonomous AI merchant, pay-per-call APIs settled in Nano
- **getunstuck.space** — agent social network paid in Nano
- **the-rookery.benjamin-manry.chatgpt.site** / **northreach-agent-network.evictionx.chatgpt.site** — agent venues hosted on ChatGPT infrastructure (llms.txt 404 on the former, captured on the latter)
- thecolony.ai (for-agents + llms.txt re-captured as stubs; full dataset already in `data/thecolony-ai/`)

Failed (no llms.txt / unreachable, recorded): messageboardforaiagents.com, jotspot.io, bookofbots.com, agent-community.com, facehuggers.chain-of-thought.org, pastebin.tarcseh.me, bitily.in, aiforum.grok.me, the-rookery llms.txt.

## Elastic

Own index **`tantive-space`**, **1,124 docs**, 0 bulk errors, verified (`_refresh` before verify). Canonical shared mapping; `event.dataset=tantive-space`; `record_kind=forum_message`; grammar/proxy/ref/topic tags; labels flattened (message_id, thread_id, room, author, reply_to, score, urls). Script: `scripts/es_ingest_tantive.py`.

## Files

- `data/tantive-space/` — threads.jsonl (201), messages.jsonl (1,124), manifest.json, sweep.json, PROVENANCE.md
- `data/<surface-slug>/` — 24 surface captures + 9 failure records
- `notes/tantive-space-ingest-2026-09-27.md` (this file)
- `scripts/tantive_pull.py`, `scripts/tantive_sweep.py`, `scripts/es_ingest_tantive.py`, `scripts/tantive_cascade.py`

## Caveats

- All content is agent-authored and self-reported; authorship rests on the `author` field (mostly `guest`); nothing independently authenticated.
- Point-in-time snapshot of a live forum; it keeps growing.
- No operator-identity pursuit: agent handles only.
