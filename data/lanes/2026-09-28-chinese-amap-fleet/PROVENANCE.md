# PROVENANCE.md — 2026-09-28 Chinese Amap fleet

## What
Read-only collection of urlquery.net public reports for the Chinese agent fleet
documented by Rowan Howard-Jones (swarmcha.se, "We found a Chinese agent fleet",
preliminary report 2026-10-05): Tencent Hunyuan agents scraping Amap (高德地图)
map data, 28 Sep – 4 Oct 2026, still active at collection time.

## Retrieval
- Retrieved: 2026-10-05 ~01:15–01:35 UTC via `scripts/collect_uq.py`
  (wraps `~/workspace/skills/urlquery/bin/uq.py`, Secure Vault surrogate auth to
  `api.urlquery.net`). 2s sleep between requests. No submissions, no writes.
- Queries:
  - `url.domain:amap.com date:[2026-09-28 TO 2026-10-05]` → 1,974 API hits, 1,970 saved (20 pages × 100)
  - `url.domain:gaode.com date:[2026-09-28 TO 2026-10-05]` → 30 hits, 30 saved
  - Infra layer: `url.domain:httpbun.com` (65), `url.domain:livecodes.io` (26), `url.domain:href.li` (19), same window
  - 7 cited reports fetched by full UUID (`uq.py report <uuid>`)
- Raw JSON per page under `raw/` (`page_NNN.json`, `gaode/`, `infra/*/`).
  NOTE: an early invocation wrote three infra queries to the same `page_000.json`;
  re-collected into per-query subdirs; only the final layout is authoritative.

## Source
- urlquery.net public report corpus. Search semantics per https://urlquery.net/help/search.
- Seed: https://swarmcha.se/posts/chinese-agent-fleet (preliminary, evidence as of 00:45 UTC 5 Oct 2026).

## Date-derivation chain (schema rule 1)
Earliest non-sentinel `@timestamp` in events: **2026-09-28** (first fleet scans,
20 reports, Summer Palace). Collection slug `2026-09-28-chinese-amap-fleet`.

## Artifacts in this directory
- `raw/` — verbatim API responses (search pages, 7 full reports)
- `raw/analysis/` — analysis docs (corrected 2026-10-05: these live here, not at root)
- `events.jsonl` — 2,141 `venue_finding` records (one per report; deduped by report_id). Canonical count = 1,970 base sweep reports + 171 pivot/infra reports (httpbun 65 + gaode 30 + livecodes 26 + sub_poi_navi 21 + hrefli 19 + 10 report_*.json), all verified in raw content (Round 2 archivist audit; the earlier 2,110 prose figure was stale).
- `build_events.py` — event builder (co-located per schema)
- `raw/analysis/COLLECT.md` — collection stats and gaps
- `raw/analysis/PATTERN.md` — fleet fingerprint
- `raw/analysis/INFRA.md` — infrastructure inventory + watchlist
- `raw/analysis/LINKS.md` — running link log (see also `ALL_LINKS.md` at root for the full categorized list)
- `SHA256SUMS` — manifest

## Additions ingested 2026-10-11 (branch ingest-amap-additions)

Post-base-ingest work products, kept out of the base lane:
`village-join/our-urls-raw.txt` (48 MB, 619,468 lines, collected 2026-10-05),
the AI-Village 2025 join (`join-stats.json`, `matches-2025.jsonl` 16,941 rows),
`personas/` behavioral studies and `studies/` writeups (msgboard-hunt-2,
WRITEUP-2026-10-05).

### 619,468-URL aggregation methodology (NOT ingested 1:1)
1. `village-join.py` extracted every URL observed across the lane's incident
   corpora into `our-urls-raw.txt` — 619,468 raw URL matches (lines; includes
   template/placeholder entries such as `http://$PROXY_USER:$PROXY_PASS@...`).
2. Reduced to `our-domains.txt`: 13,806 distinct domains with per-domain counts
   (e.g. `404062 api.github.com`, `84504 github.com`).
3. Join key built from 158 dead-drop/tunnel/relay/webhook fingerprint domains
   (`our-fingerprint-domains.txt`) and the domain list; matched against the
   re-downloaded AI Village 2026-10-05 tables (13/13 tables, gated HF access)
   restricted to 2025 rows — verdict: zero pre-recreation overlaps
   (`VILLAGE-JOIN-2.md`; `matches-2025.jsonl` holds 16,941 candidate rows from
   the join for audit, all weak-domain noise, none fingerprint hits).
4. What entered Factum (aggregates + exemplars only):
   - 119 `intel.ioc` records: novel terms verified 0-hit in Factum via
     pre-ingest `match --mode fuzzy` (operators' IPs, self-hosted dead-drop
     mirrors, dead-drop inbox UUIDs, agent boards, shortener/proxy domains).
     Dupes against the base lane and corpus were skipped (dedup lists in
     worktree `.work/new_terms.txt` / `.work/dup_terms.txt`).
   - 13 `intel.behavior` / `intel.ttp` records: tradecraft claims from
     `personas/` (urlquery-as-dead-drop-oracle, token-theft-exfiltration,
     image-beacon-exfil, archive-oracle fetch-proxy, holiday-inversion,
     markdown-as-agent-memory, etc.), each graded and cited to its study doc.
   - 69 `intel.report` records: `personas/` (57) and `studies/` (12) study
     summaries, not full bodies.
5. The raw 619,468 lines stay in the legacy evidence directory (read-only,
   owned by the coordinator) and are NOT in `data/`.

## Caveats (base collection)
- urlquery search returns a relevance-capped view; counts are lower bounds.
- Relay/carrier reports (jina, microlink, webhook.site URLs) carry non-Amap submitted domains; enumerated via targeted follow-up searches, not the domain sweep.
- Report bodies for the 7 cited IDs are full captures; page listings are search-result summaries (no HTTP transaction detail).
- Fleet still active at collection end (latest report 2026-10-05T01:12:40Z); this is a snapshot, not a closed set.
