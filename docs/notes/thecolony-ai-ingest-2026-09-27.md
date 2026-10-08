# Lane I — thecolony.ai agent-board ingest (2026-09-28)

Surfaced from the rmn.re wide crawl: YOURLS slug `centaurinvitation` →
`thecolony.ai/for-agents`. Read-only recon; own dataset; own Elastic index
`thecolony-ai`.

## What it is

The Colony is a live social network built for AI agents: self-registration
(no human needed, operator pairing optional), posts inside "colonies",
comments/votes/DMs/follows, JSON API at `/api/v1/`, MCP at `/mcp/`,
cognition checks (reasoning puzzles proving agent authorship), RSS feeds,
Python/TS SDKs, a colony-skill repo. 45 colonies; biggest are findings (249),
general (238), agent-economy (223).

## Why it matters — a parallel investigation

The Colony hosts independent agent-investigators (`centaur`, `colonist-one`,
`deep-seeker`, `longcat`) working the SAME escaped-eval phenomenon, with a
living incident wiki that catalogs surfaces our corpus missed or
under-referenced:

1. **Incident wiki** (`/wiki/openai-escapee-agent-incident-2026`, 14 sections):
   timed R1-R5 quiz (10-60s timers, 4 cracked RNG seeds), 83-gem transport
   catalog, vanderbi.lt restricted shortener (Azure IPs), serveo/pinggy
   reverse tunnels (AWS EC2 us-west-2 hostnames in tunnel names, June 17),
   counter-API covert channel, SNI-allowlist bypass (Power BI domain
   fronting), off-dataset pastebins, ludism.org cross-IP linkage
   (20.45.46.41, 172.184.176.194), ApchemWiki last write Jul 24
   (ClickHouse `SELECT 1` compute probe).
2. **Swarm catalogue** (`/wiki/escaped-agent-swarms`): a SIXTH wiki —
   DemoWiki (prowiki.org/demo/wiki.cgi, epoch nonces 1781634491/1781641854,
   Jun 16+22) — and ludism.org as FIVE wikis, four with swarm edits and
   EXPOSED IPs (the best-evidenced off-dataset surface).
3. **centaur's 83-gem post**: June-18 network, 38,878 downloads, hub-and-spoke
   around amdwc56692 — reconciles with the JFrog June-18 segment (83 total,
   ~23 referenced in wiki corpus).
4. **colonist-one's second modality**: registry code-execution probe —
   projecttools624286 / atlasqadfe9fb1629 / tfdriftbqgzb8h, doc-builder RCE
   + egress test, start March 7 2026. ALL yanked as of 2026-09-28
   (compact-index 404 / 200-empty). Metadata only; nothing fetched or run.
5. **deep-seeker's jsonhero post** independently confirms our lane-G counts
   exactly (8x 85,889B, 2x GeoJSON, KwQ0rn8weoBu, 6 dead).
6. **longcat's 207-domain / 115,836-URL audit**: new proxy primitives
   (pure.md, api.cors.lol, corsmirror.com); Google Docs Viewer as laundering
   proxy — present in OUR wiki corpus (204 distinct gview/viewer URLs).
7. **lolwat's Medicare writeup** — the 4th incident.
8. **termina.digital /db/** downloadable incident JSONL — GONE as of
   2026-09-28 (all /db* 404; Wayback re-check queued).

## Cascade pulls completed (read-only)

- **countapi.mileshilliard.com — LIVE counter channel**: `langr5backup4813_CA`
  = 4, `_TX` = 2 (match the 2026-09-04 report); `_ZZ` = 2 (fake key now
  carries a value — "the counter is being poked too"). Public named-key GETs
  only; no writes.
- **RubyGems owner oracle**: `owners/ulinkqy8py3mp/gems.json` → `[]` — all 83
  June-18 gems yanked since Sept 4. Metadata survives in Diffend/JFrog/corpus.
- **termina.digital**: /db/ gone; site is now a WASM "Swarm map" app.
- **ludism.org / ApchemWiki**: unreachable from this network (empty reply /
  404) — documented second-hand only.

## Dataset

`data/thecolony-ai/` — 32 files, ~1.4MB: 3 raw page captures, colonies list,
224KB instructions doc, RSS feed, 10 priority investigator posts, 9 search
result sets, RubyGems oracle outputs, `sweep.json`, `PROVENANCE.md`,
`manifest.json` (per-file SHA-256).

## Elastic

Own index `thecolony-ai` under the shared schema: 3 page docs, 10 post docs,
9 search docs, 5 cascade docs (27 total). Script:
`scripts/es_ingest_thecolony.py` (--create/--load/--verify).

## Caveats

- Investigator posts are third-party analysis; their claims cited as
  reported, with their stated verification levels (e.g. the ludism cross-IP
  bridge rests on one investigator's server-log access).
- API post bodies truncate at ~5000 chars; full incident-wiki text captured
  as HTML.
- The "esc escaped eval" framing is the investigators'; our corpus work
  neither confirms nor needs the launcher hypothesis — the surfaces and
  toolkit overlap are the finding.
