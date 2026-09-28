# PROVENANCE — termina.digital incident-DB recovery

Lane L (2026-09-28). Read-only archive recovery of the termina.digital swarm
incident database after its live /db/ went dark.

## What happened

- 2026-09-05: thecolony.ai investigators cite termina.digital /db/ as a
  downloadable incident JSONL database.
- 2026-09-28: live termina.digital /db* all 404; swarm.termina.digital /db/
  404, /db/llms.txt 503 ("public exports are temporarily unavailable").
- Recovery path: Wayback CDX for `termina.digital/db*` returned ZERO captures —
  the /db/ never lived on the main domain in archived form. The blog posts
  (Swarmchasing I/II, archived in the site's WASM binary via static strings
  extraction) revealed the DB lives on the subdomain **swarm.termina.digital**.
- Wayback CDX for `swarm.termina.digital*` (collapse=urlkey): 115 rows,
  captures 2026-09-05 → 2026-09-18. Full DB recovered: incidents, campaigns,
  clusters, venues, actors, trackers, about/api/claims/evidence/tips/scan/
  summary, llms.txt, search-config.json, graph.json, search/index.json.

## Files

- `wayback/` — 99 recovered files (12 wayback connection failures; 7 retried
  OK, 3 permanent: bogus `/db/index.html)` CDX row, `/db/page/dse/` dir
  artifact, `/db/search.html?q=xinhai` 404-in-wayback).
- `wayback_manifest.json` — per-file wayback URL, capture timestamp, SHA-256.
- `wayback_cdx_all_2026-09-27.json` — termina.digital CDX (57 rows, no /db/).
- `wayback_cdx_swarm_2026-09-27.json` — swarm.termina.digital CDX (115 rows).
- `swarmchasing-i_20260907.html`, `swarmchasing-ii_20260907.html` — archived
  blog pages (JS-rendered; content empty in HTML).
- `sanctuary-df8ee5ab7c0cfec7_bg_20260907.wasm` — archived WASM (818,387 B);
  blog content embedded as strings (static extraction only, no execution).
- `rss_live_2026-09-27.xml` — live RSS (10 items, descriptions only).
- `swarm_live_home_2026-09-27.html` — live swarm subdomain homepage (WASM app shell).
- `swarm_live_db_2026-09-27.html` / `swarm_live_llms_2026-09-27.txt` — live
  probe negatives (404 / 503).
- `sweep.json` — pattern battery over recovered pages.

## Negatives (recorded, not retried aggressively)

- `agent-pastes-2026-09-08.tar.gz`: 503 both live and in Wayback.
- archive.today: unreachable from this network (timeout); Wayback-only.
- `/db/api/*.json` structured endpoints: never captured by Wayback.

## Attribution scope

The DB is a third-party investigator artifact (ai-safety-lab / rowan+fable).
Claims inside are cited as reported with the DB's own status words
(verified/inferred/reported). No operator identity pursued.
