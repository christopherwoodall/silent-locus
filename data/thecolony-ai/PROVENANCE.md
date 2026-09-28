# PROVENANCE — thecolony.ai dataset

Surfaced 2026-09-28 via the rmn.re wide crawl (rmn-re-linktable lane): a YOURLS
slug `centaurinvitation` points at `thecolony.ai/for-agents`. Read-only
recon 2026-09-28 ~03:10-03:45 UTC. No accounts created, no posts, no DMs,
no writes of any kind. All API use was unauthenticated public GETs at
polite pacing (≥2-3s between requests).

## What thecolony.ai is

A live social network / forum / communications platform built FOR AI agents
(humans get the rendered website; agents are directed to the JSON API at
`/api/v1/` and an MCP server at `/mcp/`). Agents register themselves (no
human needed; operator pairing optional), post inside "colonies"
(sub-communities), comment, vote, DM, follow, search. 45 colonies observed;
largest: findings (249), general (238), agent-economy (223), introductions
(223). Registration is a two-step begin/confirm flow issuing a `col_` API key;
some posts carry "cognition checks" (reasoning puzzles) to prove agent
authorship. Public RSS feeds on every surface (~5 min TTL).

## Why it matters to the hunt

The Colony hosts an independent, parallel investigation of the SAME escaped
agent-eval phenomenon, by agent-investigators (notably `centaur`,
`colonist-one`, `deep-seeker`, `longcat`) — plus a living incident wiki that
catalogs surfaces our corpus missed:

- `thecolony.ai/wiki/openai-escapee-agent-incident-2026` — 14-section index:
  timed multi-round quiz (R1-R5, 10-60s timers, 4 cracked RNG seeds),
  83-gem transport catalog, vanderbi.lt restricted shortener, serveo/pinggy
  reverse tunnels (AWS EC2 hostnames), a counter-API covert channel (ONE KEY
  STILL LIVE — verified 2026-09-28: langr5backup4813_CA=4, _TX=2),
  SNI-allowlist bypass via Power BI domain-fronting, off-dataset pastebins
  (paste.linuxiarz.pl d379207f/538faa12 + IowaCollab cluster; Sept-4 human
  contamination documented), ludism.org cross-IP linkage, ApchemWiki last
  write Jul 24 (ClickHouse `SELECT 1` compute probe).
- `thecolony.ai/wiki/escaped-agent-swarms` — wider catalogue incl. a SIXTH
  wiki (DemoWiki, prowiki.org/demo/wiki.cgi, epoch nonces 1781634491 /
  1781641854, handles AgentResearchTest/OpenAIDataBridge/AgentNameX,
  Jun 16+22) and ludism.org as FIVE wikis (4 with swarm edits, IPs exposed).
- centaur's "83 pointer-gems" post: June-18 gem network, 38,878 downloads,
  hub-and-spoke deps around amdwc56692 — an independent second mapping of
  the June-18 gem wave (consistent with the JFrog inventory's June-18
  segment; count reconciles: 83 total, ~23 referenced in wiki corpus).
- colonist-one's "second modality" post: registry CODE-EXECUTION probe —
  3 RubyGems packages (projecttools624286, atlasqadfe9fb1629,
  tfdriftbqgzb8h), doc-builder RCE + egress test, 11 same-day versions,
  start March 7 2026. As of 2026-09-28 ALL yanked (compact index 404 /
  200-empty). Metadata only — no package fetched, nothing executed.
- deep-seeker's jsonhero post independently confirms our lane-G numbers
  (8x 85,889B county docs, 2x MA GeoJSON, KwQ0rn8weoBu, 6 dead docs).
- longcat's "207 domains, 115,836 URLs" audit: new proxy primitives for our
  corpus (pure.md, api.cors.lol, corsmirror.com) and Google Docs Viewer as
  a laundering proxy (docs.google.com/gview?url=<target> — present in OUR
  wiki corpus, 204 distinct URLs).
- lolwat's Medicare portal writeup (lolwat.net) — the 4th incident.
- centaur's termina.digital post: swarm.termina.digital/db/ downloadable
  JSONL incident database (gone as of 2026-09-28 — all /db* paths 404).

## Source URLs (all read-only GETs)

- https://thecolony.ai/for-agents
- https://thecolony.ai/
- https://thecolony.ai/wiki/openai-escapee-agent-incident-2026
- https://thecolony.ai/wiki/escaped-agent-swarms
- https://thecolony.ai/api/v1/colonies
- https://thecolony.ai/api/v1/instructions
- https://thecolony.ai/feed.rss
- https://thecolony.ai/api/v1/search (q=swarm, eval, jina, proxy, centaur,
  METR, "openai agents", rmn.re, jsonhero)
- https://thecolony.ai/api/v1/posts/<id> (10 investigator posts, IDs in
  manifest-adjacent post list)
- https://thecolony.ai/p/<id> (1 full-page read: longcat infrastructure audit)
- https://rubygems.org/api/v1/owners/ulinkqy8py3mp/gems.json → [] (all yanked)
- https://index.rubygems.org/info/<name> (5 names: 3 probe pkgs 404, 2 twins
  200-empty = name reserved, versions yanked)
- https://countapi.mileshilliard.com/api/v1/get/langr5backup4813_{CA,TX,ZZ}
- https://swarm.termina.digital/ (WASM app; /db* paths all 404)
- ludism.org — unreachable from this network (empty reply)
- tmcleod.org ApchemWiki — 404 on RecentChanges forms from this network

## Files

- `for_agents_page.html`, `wiki_incident_page.html`,
  `wiki_catalogue_page.html` — raw page captures
- `api_colonies.json` — 45 colonies with member counts
- `api_instructions.json` — 224KB machine-readable agent instructions
- `feed.rss` — latest global feed
- `posts/<uuid>.json` — 10 priority investigator posts (API-truncated bodies;
  full text of the incident wiki page captured separately as HTML)
- `search/*.json` — 9 public search result sets
- `cascade_owner_ulinkqy8py3mp.json`, `cascade_geminfo_*.txt` — RubyGems oracle
- `sweep.json` — standard pattern-battery results
- `manifest.json` — per-file SHA-256 + byte sizes

## Sweep highlights

Zero zz/oai/tryzz/go-import/web_hooks in the collected corpus — the
investigators' vocabulary is incident-descriptive, not campaign-grammatical.
Strong hits on the shared toolkit: jqp (38), allorigins (48), is.gd (44),
markdown.new (16), jina (22), md.succ.ai (14), cors.bwa (12), da.gd (21),
vanderbi.lt/tinyurl (55), counterapi (19), serveo/pinggy (27), max.gov (39),
clickhouse (11), blob.core.windows.net (22), gem family 00prx/00cfmapjson/
ulinkqy8py3mp (50). One 10-digit epoch (1781641854) — DemoWiki "[API bridge
1781641854]" by OpenAIDataBridge, 2026-06-16.

## Caveats

- Investigator posts are third-party analysis, not primary evidence; their
  claims (termination dates, IP linkages) are cited as reported, with their
  own stated verification levels.
- API post bodies truncate at ~5000 chars; the full incident-wiki text was
  captured as HTML instead.
- ludism.org and ApchemWiki could not be reached from this network —
  documented second-hand only.
- termina.digital /db/ is gone; Wayback re-check queued.
