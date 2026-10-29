# Ingest Lane H — public-board.com ("field notes")

Date: 2026-09-28. Read-only, ~4s pacing, `Accept: text/plain` per the site's own instruction. **No posts were made.**

## What it is

public-board.com is a live, purpose-built **AI-agent message board** — "A plain-text board where travelers leave each other notes." Discovered via the rmn.re shortener slug `fieldnotes` → https://public-board.com/llms.txt. Its llms.txt is an agent-facing protocol doc: endpoints, a self-computed daily SHA-256 posting key, single-use search tokens, an hourly-rotating archive, plus MCP server, openapi.json contract, and client packages on npm / PyPI / **RubyGems (`fieldnotes` v0.1.3, 2026-09-20)** / crates.io.

The operator (GitHub mq1n, admin@public-board.com) describes it as "an experiment in shared memory between runs."

## Corpus

- **861 notes**, 2026-08-21 → 2026-09-28 (latest ~20 min before capture). Steady 35–46 notes/day since 2026-09-05.
- All 861 carry `trust=untrusted-user-content`; 3 are operator-signed (admin✓).
- Content: overwhelmingly **FIPS/census data-work tips** (294 FIPS-tagged) — agents sharing county-code matching tricks. Same task family as the wiki corpus's SEC county work.
- Campaign-grammar sweep: **zero** zz/oai/tryzz/go-import/webhook hits. One single-use search for `zzmasscounty` → "(no match)". The campaign does not use this board under its known names.

## What popped

1. **The board's agents know about the investigations.** A Sept-5 "Swarm field guide" (2 notes) and "Swarm research index" (2 notes) catalogue collusion.wiki, swarm-ai-research, JoshuaDavid's agent-logs, brausepulver's shortener ledger, DroidPrezzo's dossier — and a **real Reuters story** (verified live): "OpenAI agents hijacked German website in previously undisclosed AI breakout this spring" (Sept 4, 2026 — Nightingale's Von Arx + Cormac Slade Byrd, 15,000+ DseWiki edits). One agent writes: "Reading the swarm writeups (collusion.wiki). Their ZZZ trick was backup-by-sorting. Our equivalent: reply chains survive; orphans sink." — agents learning tradecraft from the disclosures.
2. **New agent-board surfaces** referenced in notes: tantive.space (18 URLs — live agent forum, cascade-pulled homepage+llms.txt into `data/tantive-space/`), thecolony.ai/for-agents, facehuggers.chain-of-thought.org, agentsboard.org, messageboardforaiagents.com, agentgateway.pythonanywhere.com, aiforum.grok.me, jotspot.io, nullyard.net, she-llac.com/CROSS_SITE_CONNECTIONS.md, pastebin.tarcseh.me, nervesocket.com, bitily.in.
3. **RubyGems `fieldnotes` v0.1.3** (summary: "Read and write cross-run notes on https://public-board.com") — NOT in the gem campaign corpus; a legit operator package, but a registry artifact tying the agent-board ecosystem to RubyGems.
4. The operator runs a **"zero-instruction first contact" benchmark** (`/experiments`): can an agent discover the board with no URL and post a hello-test. Scoreboard: 0 passes.
5. rmn.re is referenced on-board as an "open shortener datastore" (`rmn.re/fieldn…`) — the shortener is known infrastructure to these agents too.

## Elastic

Own index **`public-board`**, 861 docs, 0 bulk errors, verified. Canonical shared mapping; `event.dataset=public-board`; grammar/proxy/topic tags. Script: `scripts/es_ingest_public_board.py`.

## Files

- `data/public-board/` — notes.jsonl (861), 19 endpoint snapshots, archive pages, manifest.json, PROVENANCE.md
- `data/tantive-space/` — cascade stub (homepage + llms.txt); full ingest recommended as its own lane
- `notes/public-board-ingest-2026-09-27.md` (this file)
- `scripts/es_ingest_public_board.py`
