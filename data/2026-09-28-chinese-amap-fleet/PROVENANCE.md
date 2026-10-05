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
- `events.jsonl` — 2,110 `venue_finding` records (one per report; deduped by report_id)
- `build_events.py` — event builder (co-located per schema)
- `COLLECT.md` — collection stats and gaps
- `PATTERN.md` — fleet fingerprint
- `INFRA.md` — infrastructure inventory + watchlist
- `LINKS.md` — running link log
- `SHA256SUMS` — manifest

## Caveats
- urlquery search returns a relevance-capped view; counts are lower bounds.
- Relay/carrier reports (jina, microlink, webhook.site URLs) carry non-Amap submitted domains; enumerated via targeted follow-up searches, not the domain sweep.
- Report bodies for the 7 cited IDs are full captures; page listings are search-result summaries (no HTTP transaction detail).
- Fleet still active at collection end (latest report 2026-10-05T01:12:40Z); this is a snapshot, not a closed set.
