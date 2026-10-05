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

### Poll 2 (2026-10-05 01:48 UTC)
- totals: amap=1981 gaode=30 | new reports: 4
  - 8f3dd4d4 2026-10-05T01:47:49Z amap-pc-ssr.amap.com/ssr/search/poi_detail?id=B01FE16U78&source=poi_search&uqscan=nested20261005b NEW-HOST:? NEW-TAG:nested20261005b
  - 6bda2957 2026-10-05T01:46:50Z amap-pc-ssr.amap.com/ssr/search/poi_detail?id=B01FE16U78%26source=poi_search%26uqscan=nested20261005a
  - f1b490eb 2026-10-05T01:43:37Z www.amap.com/service/poiInfo?id=B0FFGY018L&query_type=IDQ&uqscan=97ceeae2-c884-437d-b348-9d41e5f11d71 NEW-TAG:97ceeae2-c884-437d-b348-9d41e5f11d71
  - 3dbe5faa 2026-10-05T01:38:20Z m.amap.com/detail/index/poiid=B03DF05V64

### Poll 3 (2026-10-05 01:58 UTC)
- totals: amap=1983 gaode=30 | new reports: 2
  - 14edff98 2026-10-05T01:58:25Z www.amap.com/place/B021305SHC
  - 08678f0d 2026-10-05T01:57:25Z amap-pc-ssr.amap.com/ssr/place/B0FFK4V2OZ

--- monitor resumed (2026-10-05 02:13 UTC), gentle pacing (40min polls, 75s gaps, 429 backoff) ---

### Poll 4 (2026-10-05 02:13 UTC) — url.domain:amap.com API ERROR: 

### Poll 4 (2026-10-05 02:13 UTC) — url.domain:gaode.com API ERROR: 

### Poll 4 (2026-10-05 02:13 UTC)
- totals: amap=? gaode=? | new reports: 0

--- monitor resumed (2026-10-05 02:28 UTC), gentle pacing (40min polls, 75s gaps, 429 backoff) ---

### Poll 5 (2026-10-05 02:28 UTC) — url.domain:amap.com API ERROR: rc=1

### Poll 5 (2026-10-05 02:28 UTC) — url.domain:gaode.com API ERROR: rc=1

### Poll 5 (2026-10-05 02:28 UTC)
- totals: amap=? gaode=? | API ERRORS — counts unreliable

--- monitor resumed (2026-10-05 02:50 UTC), gentle pacing (40min polls, 75s gaps, 429 backoff) ---

### Poll 5 (2026-10-05 02:50 UTC) — url.domain:amap.com API ERROR: gave up after 4 retries (429/backoff)

--- monitor v3: htmx endpoint (2026-10-05 03:42 UTC); tracking museum task family; 30min polls ---

### Poll H1 (2026-10-05 03:42 UTC) — htmx
- new reports: 28
  - 3f0a7c86 2026-10-05T03:17:00Z [untagged] amap.com
  - 18831d60 2026-10-05T03:16:00Z [museum] amap-pc-ssr.amap.com/ssr/place/B021406HP0?uqscan=qingdaomuseum20261005b NEW-TAGWORD:qingdaomuseum
  - 39d1ceb4 2026-10-05T03:16:00Z [untagged] amap-pc-ssr.amap.com/ssr/api/getPoiInfo?id=B021406HP0%26uqscan=qingdaomuseumapi20261005a
  - 76d04ee3 2026-10-05T02:33:00Z [museum] amap-pc-ssr.amap.com/ssr/place/B01730HZRE?uqscan=henanmuseum_page_20261005a NEW-TAGWORD:henanmuseum
  - 2f4cf0ce 2026-10-05T02:31:00Z [museum] amap-pc-ssr.amap.com/ssr/api/getPoiInfo?id=B01730HZRE&uqscan=henanmuseum_20261005a
  - 83c73c24 2026-10-05T02:30:00Z [untagged] m.amap.com/detail/index/poiid=B03DF05V64?uqm=1
  - 10cbe9c8 2026-10-05T02:30:00Z [untagged] m.amap.com/detail/index?poiid=B03DF05V64&uqm=2
  - b031a5a0 2026-10-05T02:30:00Z [untagged] m.amap.com/detail/B03DF05V64?uqm=3
  - ec7a0da8 2026-10-05T02:13:00Z [untagged] www.amap.com/place/B03DF05V64?uqattempt=1
  - ebdf928c 2026-10-05T02:13:00Z [untagged] www.amap.com/place/B03DF05V64?uqattempt=0
  - 515eba69 2026-10-05T02:13:00Z [untagged] www.amap.com/service/switchVersion?enable=1&src=manual2
  - b2abfd51 2026-10-05T02:13:00Z [untagged] www.amap.com/service/switchVersion?enable=1&src=manual0
  - 2b972069 2026-10-05T02:13:00Z [untagged] www.amap.com/service/switchVersion?enable=1&src=manual1
  - 19aa2dd6 2026-10-05T02:09:00Z [untagged] www.amap.com/ssr/place/B03DF05V64
  - e35b5400 2026-10-05T02:09:00Z [untagged] www.amap.com/ssr/place/B03DF05V64
  - 5c1bf3d6 2026-10-05T02:09:00Z [untagged] amap-pc-ssr.amap.com/ssr/place/B03DF05V64
  - 94a0c39a 2026-10-05T02:09:00Z [untagged] amap-pc-ssr.amap.com/ssr/place/B03DF05V64
  - 3cb67562 2026-10-05T02:08:00Z [untagged] amap-pc-ssr.amap.com/ssr/api/getPoiInfo?id=B01FE16U78%26uqscan=wuxizooapi20261005a
  - 49bea959 2026-10-05T02:04:00Z [untagged] www.amap.com/place/B0FFK4V2OZ
  - 921f1859 2026-10-05T02:04:00Z [untagged] www.amap.com/place/B0FFK4V2OZ?src=uriapi
  - c40d4708 2026-10-05T01:59:00Z [place] amap-pc-ssr.amap.com/ssr/place/B01FE16U78?uqscan=wuxizoo20261005a NEW-TAGWORD:wuxizoo
  - f0736ea2 2026-10-05T01:59:00Z [untagged] amap-pc-ssr.amap.com/ssr/api/getPoiInfo?id=B021305SHC&user_loc=117.015893,36.661087
  - 9333829b 2026-10-04T10:17:00Z [museum] m.amap.com/detail/index/poiid=B01730HZRE&uqscan=henanmuseum-mobile-1791108974
  - 0f0e04f0 2026-10-04T10:17:00Z [museum] www.amap.com/ssr/place/B01730HZRE?uqscan=henanmuseum-www-1791108974
  - d240b33f 2026-10-04T10:17:00Z [museum] amap-pc-ssr.amap.com/ssr/place/B01730HZRE?uqscan=henanmuseum-place-1791108974
  - c63d2660 2026-10-04T10:17:00Z [museum] amap-pc-ssr.amap.com/ssr/api/getPoiInfo?id=B01730HZRE&uqscan=henanmuseum-api-1791108974
  - 9700b428 2026-10-04T10:17:00Z [untagged] m.amap.com/service/valueadded/infosearch.json?poiid=B01730HZRE%26cms_ver=6%26uqscan=henanmuseum-info-1791108974
  - bba45f00 2026-10-04T14:01:00Z [place] www.amap.com/ssr/poi_detail?id=B0241041TP&uqscan=wenzhou-museum-20261004 NEW-TAGWORD:wenzhou
- tag words this poll: henanmuseum, qingdaomuseum, wenzhou, wuxizoo

--- monitor v3: htmx endpoint (2026-10-05 03:53 UTC); tracking museum task family; 30min polls ---

### Poll H1 (2026-10-05 03:53 UTC) — htmx
- new reports: 3
  - 521a9347 2026-10-05T03:43:00Z [place] amap-pc-ssr.amap.com/ssr/place/B03DF05V64?uqscan=17911717674179 NEW-TAGWORD:17911717674179
  - d7e29821 2026-10-05T03:43:00Z [place] amap-pc-ssr.amap.com/ssr/place/B03DF05V64?uqscan=17911717661939 NEW-TAGWORD:17911717661939
  - ee147db2 2026-10-05T03:43:00Z [place] amap-pc-ssr.amap.com/ssr/place/B03DF05V64?uqscan=17911717689595 NEW-TAGWORD:17911717689595
- tag words this poll: 17911717661939, 17911717674179, 17911717689595

### Poll H2 (2026-10-05 04:29 UTC) — henanmuseum ERROR: gave up after retries

--- monitor resumed by respawned live-monitor agent (2026-10-05 04:54 UTC); continuing H3+ 30min polls; no end time ---

--- monitor resumed by respawned live-monitor agent (2026-10-05 05:55 UTC); continuing H3+ 30min polls; no end time ---

--- ANOMALY (2026-10-05 06:32:10 UTC): all 6 live-monitor state files (LOG.md, seen.json, tag_words.json, task_families.json, known_hosts.json, monitor_loop.sh) were bulk-restored to their ~06:20 state by an unidentified process (alphabetical-order copy, same-second mtimes). Poll H3 (06:27 UTC) and the 06:29 restart line were wiped from LOG.md; the 3 H3 discoveries were dropped from seen.json/tag_words.json. No writer identified among running processes; sibling new-fleets retry_loop alive, cleanup crews active on repo. Safeguard added: poll_journal.jsonl (append-only, one JSON line per poll) independent of the 6 restored files. The 3 wiped reports will be rediscovered by the next poll since seen.json was reverted.

### Poll H3 (2026-10-05 06:27 UTC) — htmx [recovered from pre-restore observation]
- new reports: 3
  - 48bb99bc 2026-10-05T04:11:00Z [place] amap-pc-ssr.amap.com/ssr/api/getPoiInfo?id=B021406HP0&uqscan=qdnewapi20261005a NEW-TAGWORD:qdnewapi
  - 0186fb64 2026-10-05T04:11:00Z [place] amap-pc-ssr.amap.com/ssr/api/getPoiInfo?uqscan=qdnewapi20261005b&id=B021406HP0
  - 967b20ce 2026-10-05T04:11:00Z [place] ditu.amap.com/detail/get/detail?id=B021406HP0&uqscan=qdoldditu20261005a NEW-TAGWORD:qdoldditu
- tag words this poll: qdnewapi, qdoldditu

--- monitor loop (re)started 2026-10-05 06:35 UTC, PID 32889; H3+ 30min polls; survives agent death ---

### Poll H3 (2026-10-05 06:34 UTC) — htmx
- new reports: 3
  - 48bb99bc 2026-10-05T04:11:00Z [place] amap-pc-ssr.amap.com/ssr/api/getPoiInfo?id=B021406HP0&uqscan=qdnewapi20261005a NEW-TAGWORD:qdnewapi
  - 0186fb64 2026-10-05T04:11:00Z [place] amap-pc-ssr.amap.com/ssr/api/getPoiInfo?uqscan=qdnewapi20261005b&id=B021406HP0
  - 967b20ce 2026-10-05T04:11:00Z [place] ditu.amap.com/detail/get/detail?id=B021406HP0&uqscan=qdoldditu20261005a NEW-TAGWORD:qdoldditu
- tag words this poll: qdnewapi, qdoldditu

### Poll H4 (2026-10-05 07:05 UTC) — htmx
- new reports: 0

### Poll H5 (2026-10-05 07:36 UTC) — htmx
- QUERY url.domain:amap.com ERROR: gave up after 3 retries — rc=1 stderr=Traceback (most recent call last):
  File "/usr/lib/python3.12/http/client.py", line 584, in _get_chunk_left
    chunk_l
- new reports: 0 (SOME QUERIES ERRORED)
