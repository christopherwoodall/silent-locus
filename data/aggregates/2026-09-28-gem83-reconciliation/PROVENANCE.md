# PROVENANCE — gem83-reconciliation (Lane E)

Built 2026-09-27/28 (UTC) by subagent lane E. Reconstructs the 83-gem June-18
segment independently cross-referenced against three project sources.

## Inputs

1. `../gemstuffer-jfrog-2026-09-27.csv` — JFrog GemStuffer inventory
   (3,025 rows), saved 2026-09-27 from https://research.jfrog.com/gemstuffer.csv.
2. thecolony.ai incident wiki + centaur's "83 pointer-gems" post
   (`../thecolony-ai/`, see notes/thecolony-ai-ingest-2026-09-27.md):
   83 gems, account ulinkqy8py3mp, 2026-06-18 17:53-20:52 UTC, ~38.9k downloads,
   hub-and-spoke around amdwc56692 (amdwc51950 v0.0.2 and wctest73410 as spokes).
3. JFrog Security Research report: June 18 = 83 packages (full window table).
   https://research.jfrog.com/post/gemstuffer-openai-rubygems/
4. `../osv/diffend_sweep_results*.jsonl` — our Diffend corpus name list.
5. `../gem-june18-wayback.jsonl` — 16 June Wayback metadata records.
6. `../wiki_gem_bridge.json` — collusion.wiki explorer gem metadata (2026-09-28).

## Method

81 names = regex family-grammar match over the JFrog inventory (families from
centaur's post + incident wiki examples: `[a-z]----00proxyNNN`, `amdapi|amdvar|
amdmore|amdwc|amd`, `[a-z]--00cfjsonNNN`, `[a-z]--00cfmapjsonNNN`,
`[a-z]--/----00cfproxyNNN`, `[a-z]---00proxyNN`, `[a-z]---00cfshape(s)NNNNN`,
`[a-z]----00prxNNNNN`, `adepNNNNN`, `mapanchor*`, `wctest73410`).
2 names = direct incident-wiki citation (random-suffix: ultimate4834, method2088).
Exact duplicates were collapsed; no other de-dup. The June-18 date is
inferred from grammar + external reports — the JFrog CSV carries no per-row dates.

## Limitations

- This is a grammar reconstruction, not the owner-API manifest (that API now
  returns [] — all 83 yanked). The 83 count matches JFrog's published June-18
  count exactly.
- Dependency edges (hub-and-spoke) are centaur-reported; no gemspec content
  exists in any project source to verify them. Only corroborating fact:
  JFrog lists amdwc51950 with versions '0.0.1;0.0.2' — the sole multi-version
  gem in the 83 — matching centaur's 'v0.0.2' claim.
- Read-only; no package fetched, no code executed, no identity pursued.

## Aggregates move 2026-09-29

Multi-source conglomerate collections now live under `data/aggregates/`.

- `data/gem83-reconciliation/` -> `data/aggregates/gem83-reconciliation/`
  (whole directory: PROVENANCE.md, SHA256SUMS, gem83-names.json,
  gem83-reconciliation.csv, gem83-reconciliation.jsonl, manifest.txt,
  pattern-sweep.txt, progress.log).

## Raw layer 2026-09-29

- `gem83-reconciliation.jsonl` ->
  `raw/gem83-reconciliation.jsonl` (name kept). This file is
  script-consumed input (read by `scripts/es_ingest_gem83.py`), so it lives
  in the raw layer keeping its upstream name; it is pre-event-schema source
  material and exempt from `schema/record.schema.json`.
- `gem83-reconciliation.csv`, `gem83-names.json`, `manifest.txt`,
  `pattern-sweep.txt` remain at the collection root (non-JSONL outputs).
- SHA256SUMS not regenerated (orchestrator handles checksums/manifest
  references centrally).
