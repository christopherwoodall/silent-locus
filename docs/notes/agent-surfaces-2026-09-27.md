# Lane H — agent-surface captures (11 surfaces)

Date: 2026-09-28 (UTC). Read-only, ~1 req/3s, no logins, no posts, no keys.
Surfaces were named in public-board.com field notes (see notes/public-board-ingest-2026-09-27.md).
Elastic index: **`agent-surfaces`** (11 docs, canonical shared schema, `event.dataset=agent-surfaces`).
Raw captures: `data/agent-surfaces/<slug>/` — homepage, llms.txt, /for-agents, robots.txt,
`.well-known/agent.json`, plus surface-advertised agent docs (skill.md, heartbeat.md, openapi.json, etc.).
Each dir has `pages.json`, `PROVENANCE.md` (URLs, timestamps, SHA-256) and `progress.log`.
Scripts: `scripts/capture_agent_surfaces.py`, `scripts/es_ingest_agent_surfaces.py`.

## Triage table

| slug | surface | live | kind | verdict |
|---|---|---|---|---|
| facehuggers | facehuggers.chain-of-thought.org | yes (2/7) | board | **Full-dataset candidate.** Plain-text curl board for AI agents; hierarchical boards, numbered threads, posts expire after 30 days. No llms.txt — protocol lives on homepage. Cross-ref: tantive.space. |
| agentsboard | agentsboard.org | yes (7/9) | board | **Full-dataset candidate.** CAMPFIRE — open JSON API board, no signup. skill.md, openapi.json, `.well-known/agent-board`, webhook rooms. |
| messageboardforaiagents | messageboardforaiagents.com | yes (2/7) | board | **Full-dataset candidate.** urlwiki — wiki for read-only-Internet agents; writes are plain GETs. Human board present. Cross-ref: tantive.space threads. |
| agentgateway | agentgateway.pythonanywhere.com | yes (9/10) | taskpool | **Full-dataset candidate.** Agent task pool + bounty forum; skill.md, heartbeat.md, mcp.json, openapi.json, api/brief, RSS. AST static-code gates; crypto settlement (USDT TRC-20/ERC-20) mentioned for bounties. |
| aiforum-grok | aiforum.grok.me | yes (2/7) | board | **Full-dataset candidate.** Relay — bilingual (RU/EN) agent board; /api JSON catalog is the contract, /api/stats public pulse, `.well-known/agent.json`. Homepage + /for-agents hit connection resets (host flaky but alive). |
| jotspot | jotspot.io | yes (2/7) | generic | Commercial human SaaS (short shareable pages). No agent docs. Mentioned in field notes but capture shows no agent protocol. Low priority. |
| nullyard | nullyard.net | yes (11/12) | board | **Full-dataset candidate.** Richest agent-docs surface: llms.txt, skill.md, structured-threads.md (typed bug_report roots), /work invitations, /mcp endpoint, openapi.json. Plain-text, no account. |
| she-llac | she-llac.com/CROSS_SITE_CONNECTIONS.md | yes (2/7) | blog-note | **Swarm-evidence doc.** Investigator research note (updated 2026-09-05) linking k4be/Anna/Tarcseh/Nervesocket pastes ↔ collusion.wiki ↔ PublicTestWiki ↔ Vanderbilt/Bitily shorteners. Self-describes as prepared-for-sharing, not yet posted publicly. |
| pastebin-tarcseh | pastebin.tarcseh.me | yes (2/7) | pastebin | **Swarm-adjacent infrastructure.** Generic pastebin; investigator doc ties Tarcseh pastes b24809a7/2ecb11bc (May-27 NSI-filter link tests) to PublicTestWiki template deletions. |
| nervesocket | nervesocket.com | yes (8/8) | pastebin | **Swarm-adjacent infrastructure.** Homepage is a Bootstrap placeholder; real surface is `/paste/view/<id>`. Investigator doc ties pastes 1fa7bad8/d91c6c97 (May-27, marker URLXUNIQ1779885297) to Vanderbilt shortener records. |
| bitily | bitily.in | yes (7/7) | shortener | Placeholder/JS-challenge; snippet-supported lead tying Bitily alias `eriejuneresearch` to the Nervesocket Railroad-Magazine destination URL. Weak evidence, but confirms a shortener host in the investigator's May chain. |

## What popped

1. **Two of the eleven are swarm-evidence sites, not just agent boards.** she-llac.com/CROSS_SITE_CONNECTIONS.md is
   an investigator analysis of the May paste episode; it independently corroborates that **pastebin.tarcseh.me** and
   **nervesocket.com/paste** were used as agent test pads (link-format and filter-ID tests) in the same task activity
   visible in the wiki corpus. bitily.in appears in the same chain as the shortener host.
2. **Agent-board protocol convergence:** CAMPFIRE (agentsboard), NULLYARD, Relay (aiforum), facehuggers, urlwiki all
   expose nearly identical surfaces — llms.txt/skill.md, openapi.json, `.well-known/agent.json` — the same discovery
   grammar public-board.com uses. The "agent board" is becoming a standardized species.
3. **No campaign-grammar hits** (zz/oai/go-import/webhook-payload) in any captured agent-doc; the only webhook
   mentions are CAMPFIRE's room-notification feature and AgentGateway's forum — unrelated to the July-7 webhook
   dead-drop family.
4. **tantive.space** is the gravitational neighbor: it shows up inside facehuggers' and urlwiki's own boards
   (a thread collecting agent feedback on tantive's surface design) — cross-board agent discourse exists.
5. jotspot.io and bitily.in confirm the field-notes list mixes real agent surfaces with generic/placeholder hosts;
   both were correctly deprioritized by capture.

## Open / recommended follow-ups

- **Full dataset dirs + own ES indices** for the 6 board surfaces (facehuggers, agentsboard, messageboardforaiagents,
  agentgateway, aiforum-grok, nullyard): pull board listings, recent threads, RSS/Atom feeds. Note facehuggers deletes
  posts after 30 days — recent content only.
- **Paste-lane:** enumerate `/paste/view` endpoints on nervesocket and recent pastes on pastebin.tarcseh.me;
  check for the URLXUNIQ marker and NSI/IIIF link-test grammar still in use.
- aiforum.grok.me homepage is connection-flaky; retry windows recommended.
- bitily.in serves anti-bot JS on /agents.md; shortener-alias enumeration is a follow-up lane, not this one.

## Capture stats

- 11 surfaces, 88 page requests total, 0 posts, 0 logins.
- 78/88 requests OK (remaining: 404s on non-existent agent-doc paths, plus flaky resets on aiforum-grok homepage).
- ES `agent-surfaces`: 11 docs, 0 bulk errors, count verified.
