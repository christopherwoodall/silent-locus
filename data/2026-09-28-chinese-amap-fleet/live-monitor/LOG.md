# Live monitor: Chinese agent fleet (Tencent Hunyuan / Amap)

- Started: 2026-10-05 01:27 UTC (approx)
- Poll cadence: ~20 min, 6 hours
- Baseline last-known report: 2026-10-05T01:12:40Z
- Queries: `url.domain:amap.com`, `url.domain:gaode.com` (limit 30, sorted by recency)

## Poll log

### Poll 0 — baseline (2026-10-05 ~01:27 UTC)
- amap.com total_hits: 1977 (was 1975 at 01:12) — fleet ACTIVE
- gaode.com total_hits: 30, latest 2026-10-04T17:42:52Z (quiet)
- 2 new amap reports since 01:12:40Z baseline:
  - `933a8eb5` 01:26:00Z `m.amap.com/detail/index/poiid=B03DF05V64?uqscan=claude20261005mobile2`
  - `2d2ae416` 01:25:34Z `m.amap.com/detail/index/poiid=B03DF05V64?uqscan=claude20261005mobile1`
- NEW: `m.amap.com` mobile endpoints (`/detail/index/poiid=`, `/api/getPoiDetailById`) — mobile-site task variant not in the article
- NEW tag style: `claude20261005mobile{N}` — "mobile" label family
- 56 report IDs baselined in seen.json

### Poll 1 (2026-10-05 01:28 UTC)
- totals: amap=1977 gaode=30 | new reports: 0
