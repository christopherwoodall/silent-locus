# TARGET-CLASS HUNT — map/POI systems (raw notes)

**Date:** 2026-10-04 (session started ~23:23 CDT = 04:23 UTC Oct 5)
**Method:** urlquery keyless htmx endpoint (`uq_htmx.py search`), ≤1 req/5s pacing.
urlscan.io search API was UNREACHABLE from the VM (proxy CONNECT to urlscan.io:443 times out) — noted, not retried.

**Known operator (EXCLUDED from candidates):** systematic scans of Amap POI pages
(`amap-pc-ssr.amap.com/ssr/place/<POIID>?uqscan=<word><date>...`), tag grammars
`uqscan=`/`uqtag=`/`uqvnc=`. Anything matching → "note and move on".

## Collection constraint (major)

From ~04:30 UTC Oct 5, **urlquery.net is fully unreachable from this VM**:
timeouts on the homepage (`curl https://urlquery.net/` → timeout), the htmx
search endpoint (`/api/htmx/search/`, `<urlopen error timed out>`), AND the
authenticated API (`api.urlquery.net` via `uq.py`, same timeout). urlscan.io
likewise unreachable via the egress proxy. This coincides with a request storm
from this VM's shared egress IP: `ps` showed 15+ concurrent `uq_htmx.py`/`uq.py`
queries from sibling subagent sessions hammering the same endpoint — most
plausibly IP-level throttling/edge-block at urlquery, not a site outage.

Consequence: my own 25-query sweep (batch run, limit=24, 7s inter-query sleeps)
produced ZERO completed queries — every subprocess raised `urlopen error timed
out` before writing output. Killed after verification.

Mitigation: a bounded cool-down retry loop is running in the background
(`/tmp/map-poi-scan/retry_loop.py`): 4 probes spaced 300s apart, then if the
endpoint recovers, an 8-query reduced set (google maps place, tripadvisor,
yelp, openstreetmap, zillow, redfin, dianping, naver maps) at 20s spacing.

## PRIOR ART (collected by other lanes, same incident window — NOT my queries)

### A. other-targets lane (2026-10-04, authenticated API, window 2026-09-28→2026-10-05)
`~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/raw/lanes/other-targets/FINDINGS.md`
- Exhaustive `uqscan` keyword sweep: 1,205 reports retrieved, clustered by domain.
- **Honest zeros for the KNOWN fleet's grammar on non-Amap map surfaces:**
  `url.domain:map.baidu.com` → 0; `url.domain:map.qq.com` → 0;
  `lbs.qq.com` → 0; zero hits on tianditu.gov.cn, meituan, dianping, ctrip
  in submitted or final URLs across all 1,245 reports.
- Verdict: the known fleet is Amap-exclusive (amap.com/gaode.com/ditu.amap.com
  + carriers/redirectors). Raw: q1_baidu.json, q2_qqmap.json, q4_ditu.json,
  q5_lbsqq.json, q3_uqscan page files x13, clusters.json.

### B. new-fleets lane (2026-10-05, htmx, ~03:00–03:58 UTC — ~1.5h before my session)
`~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/new-fleets/FINDINGS.md`
- Bulk recent-window pulls (`http` queries @ offsets 0/50/100 → 122 unique
  reports) + targeted queries (`nonce=`, `task=`, `batch=`, `museum`, `qingdao`,
  `henan`, etc.), clustered by per-minute bursts, per-host spans, param grammars.
- **No map/POI-system cluster found among NEW fleets.** New candidate found was
  jmail.world systematic audit (72 reports, metronomic 3-min cadence, 4h run) —
  a detection/verification workload, not map/POI. Weak candidates: ovou.com
  shortener series, an*.shop scam network, appwrite.network 6ac31* site series.
- Clean negatives: no second tag-grammar fleet at fleet scale; per-minute
  "bursts" in the firehose were global submission rate, not single-operator.

### C. My target gap vs prior art
Prior art covers: known-fleet grammar on Chinese map surfaces (A) and recent-firehose
new-fleet discovery (B). Neither covers NON-Chinese map/POI systems (Google Maps
place URLs, OSM, TripAdvisor, Yelp, Zillow/Redfin, Naver, Yandex) for OTHER
operators — that is exactly what my queries above target, pending the
collection constraint clearing.

## My queries (this session)

| # | query | reports |
|---|-------|---------|
| 00 | google.com/maps/place | _endpoint down — not collected_ |
| 01 | map.baidu.com | _endpoint down (prior art: 0 via auth API)_ |
| 02 | map.qq.com | _endpoint down (prior art: 0 via auth API)_ |
| 03 | map.naver.com | _endpoint down — not collected_ |
| 04 | yandex.com/maps | _endpoint down — not collected_ |
| 05 | openstreetmap.org | _endpoint down — not collected_ |
| 06 | mapbox.com | _endpoint down — not collected_ |
| 07 | here.com | _endpoint down — not collected_ |
| 08 | tomtom.com | _endpoint down — not collected_ |
| 09 | maps.apple.com | _endpoint down — not collected_ |
| 10 | tripadvisor.com | _endpoint down — not collected_ |
| 11 | yelp.com | _endpoint down — not collected_ |
| 12 | dianping.com | _endpoint down (prior art: 0 via auth API)_ |
| 13 | meituan.com | _endpoint down (prior art: 0 via auth API)_ |
| 14 | foursquare.com | _endpoint down — not collected_ |
| 15 | mafengwo.cn | _endpoint down — not collected_ |
| 16 | zillow.com | _endpoint down — not collected_ |
| 17 | redfin.com | _endpoint down — not collected_ |
| 18 | lianjia.com | _endpoint down — not collected_ |
| 19 | ke.com | _endpoint down — not collected_ |
| 20 | 58.com | _endpoint down — not collected_ |
| 21 | anjuke.com | _endpoint down — not collected_ |
| 22 | ditu.google.com | _endpoint down — not collected_ |
| 23 | gaode.com | _endpoint down (prior art: 18 fleet hits, same operator — excluded)_ |
| 24 | amap.com | _endpoint down (prior art: 1,010 fleet hits — known operator, excluded)_ |

Per-query dumps (if retry succeeds): `/tmp/map-poi-scan/retry_<slug>.json` (ephemeral; key findings copied below).

### D. Firehose spot-check (on-disk data from new-fleets lane, my own grep — 2026-10-05)
`new-fleets/raw/window1.json` = 123 reports, ~03:00–03:58 UTC Oct 5 firehose.
My regex grep for map/POI systems (maps, tripadvisor, yelp, zillow, redfin,
dianping, meituan, openstreetmap, foursquare, lianjia, naver, yandex,
mafengwo, mapbox): **3 hits, all known operator** —
`amap-pc-ssr.amap.com/ssr/place/B03DF05V64?uqscan=17911717674179` (+61939,
+89595 variants), same POI ID resubmitted 3× within one minute at 03:43 —
tag-plumbing re-tests, not a new swarm. **Zero non-Amap map/POI targets in
the ~1h firehose window.** (window2.json was empty — fetch failed; the lane's
FINDINGS already covers it.)

---
## Analysis

**Bottom line: no NEW map/POI swarm found. Clean-negative on the covered ground,
with a collection caveat.**

1. **Live sweep (this session): BLOCKED, not completed.** urlquery.net went
   unreachable from this VM ~04:30 UTC Oct 5 (homepage, htmx endpoint, and
   authenticated API all timeout; urlscan.io unreachable via proxy too).
   Coincides with 15+ concurrent uq_htmx.py/uq.py queries from sibling
   subagent sessions on the same egress IP — most plausibly IP-level
   throttling/edge-block, not a urlquery outage. My 25-query sweep returned
   zero completed queries; a bounded background retry loop (4 probes/15 min)
   died when /tmp was wiped. So: **non-Chinese map/POI systems (Google Maps
   place, OSM, TripAdvisor, Yelp, Zillow/Redfin, Naver, Yandex, etc.) remain
   UNSWEPT by me — re-run when the throttle clears.**

2. **Prior art (same incident window, other lanes):**
   - other-targets lane (auth API, 2026-10-04, window 09-28→10-05): known
     fleet's `uqscan` grammar has **honest zeros** on map.baidu.com,
     map.qq.com, lbs.qq.com, tianditu.gov.cn, meituan, dianping, ctrip
     (1,245 reports checked, submitted+final URLs). Known fleet is
     Amap-exclusive.
   - new-fleets lane (htmx, ~03:00–03:58 UTC Oct 5): no map/POI cluster among
     new fleets; new candidate was the jmail.world audit (not map/POI).
   - My own firehose grep (window1.json, 123 reports): 3 map/POI hits, all
     known operator (B03DF05V64, 3× resubmits at 03:43, tag re-tests).
     **Zero non-Amap map/POI targets in the ~1h firehose window.**

3. **What this means for the hunt:** every map/POI scan trace on urlquery in
   the 09-28→10-05 window resolves to the known Amap operator. No second
   operator is systematically enumerating any map/POI system (Chinese or
   Western) in the data lanes have examined. The residual gap is Western
   map/POI systems via live htmx — recommend re-running the 8-query reduced
   set (google maps place, tripadvisor, yelp, openstreetmap, zillow, redfin,
   dianping, naver maps) once urlquery is reachable again.

**Do not push** (per task). Notes live at this path only.

---
## SESSION 2 — 2026-10-05 ~05:14–06:15 UTC: 8-query Western map/POI sweep (COMPLETED)

**Collection status change:** endpoint PARTIALLY recovered ~05:14 UTC. Full
timeouts became slow-stream + `IncompleteRead` truncations (~32–48 KB per
fetch before the stream stalls). Ran a slow-mode runner
(`/tmp/uq_htmx_slow.py`, timeout=180, accepts partial reads, 3 retries,
single 24-result fetch per query, ≥6s pacing between queries; original skill
script untouched). Completed 7 queries; `tripadvisor.json` (already complete
from an earlier sibling run at 05:12 UTC, 24 reports) reused as-is.

**Known-operator grammar check:** all 8 result sets grepped for
`uqscan=`/`uqtag=`/`uqvnc=` → **0 hits everywhere**. No exclusion needed;
no known-operator contamination in this sweep.

**Actual target-domain URLs per query (not keyword mentions on other pages):**

| query | file | n | actual-domain URLs | verdict |
|---|---|---|---|---|
| google.com/maps/place | google-maps-place.json | 1 | 0 (shopify storefront, 2026-08-15) | honest negative |
| tripadvisor.com | tripadvisor.json | 24 | 0 (travel/hotel domains, likely booking clones mentioning tripadvisor) | honest negative |
| yelp.com | yelp.json | 23 | 10, all `www.yelp.com/questions/*` airline-support spam (see burst note) | honest negative for lane; spam burst noted below |
| openstreetmap.org | openstreetmap.json | 23 | 0 (roblox-phishing burst, see note) | honest negative for lane |
| zillow.com | zillow.json | 24 | 4 (bare zillow.com ×2, typosquat zilllow.com ×2, paired submissions) | honest negative |
| redfin.com | redfin.json | 22 | 1 (bare redfin.com, 2026-09-15) | honest negative |
| naver maps | naver-maps.json | 22 | 0 (Korean local-business sites mentioning naver maps) | honest negative |
| yandex.com/maps | yandex-maps.json | 14 (practical max; sparse keyword, endpoint stalls ~32KB) | 2, both old: ad-click redirect `click.ricci.ru/...goto_url=https://yandex.com/maps/-/CHsnbSJU` (2025-10-19), maps API embed `yandex.com/maps/21515/guadalajara/?from=api-maps&ll=-103.350786%2C20.687741&origin=jsapi_2_1_79` (2025-10-15) | honest negative |

Date ranges per file:
- google-maps-place.json: 2026-08-15 (single)
- tripadvisor.json: 2026-10-04T21:33Z → 2026-10-03T16:38Z
- yelp.json: 2026-10-04T17:55Z → 2026-09-11T13:50Z
- openstreetmap.json: 2026-10-05T05:17Z → 2026-10-05T04:42Z
- zillow.json: 2026-10-03T20:19Z → 2026-05-23T02:26Z
- redfin.json: 2026-09-15T19:54Z → 2026-01-24T11:12Z
- naver-maps.json: 2026-09-27T10:58Z → 2026-05-18T12:41Z
- yandex-maps.json: 2026-05-27T11:35Z → 2024-03-27T17:18Z

**Programmatic-pattern check (signal bar):** no per-request tag/nonce grammar,
no geographic/page iteration, no systematic enumeration of any map/POI system
found. The only tight bursts are spam/phishing campaigns, not map/POI
scanning:

1. **Yelp Questions airline-support spam burst (2026-09-11 13:50–13:58 UTC,
   programmatic-one-off, NOT a cartographer candidate):** 10 reports / 3
   distinct URLs — `www.yelp.com/questions/aeromexico-how-can-i-speaks-to-a-flight-live-representative-quickly/5VpyZSS4VFs2b8f8mGG` (×1),
   `.../asiana-airlines-how-is-your-airline-addressing-flight-delay-and-cancellations/VU7u95QLl` (×4),
   `.../singapore-airlines-how-can-i-speak-to-a-flight-representative-quickly/eXKWTRUF74DQIhZG-` (×5).
   Classic OTA support-number SEO spam on Yelp Questions, resubmitted by the
   campaign operator (or resubmits by the submitter). No map/POI content.
2. **Roblox-phishing submission burst (2026-10-05 04:42–05:17 UTC,
   programmatic-one-off, NOT a cartographer candidate):** all 23
   openstreetmap.json hits. Typosquat roblox ccTLD domains
   (`www.roblox.com.mu/.ml/.ly/.et/.bn/.do/.bi`, `www.robiox.com.gr`)
   profile/game pages with privateServerLinkCodes + shorteners
   (`s4w.in`, `1url.at`, `g5.lu`, `tiny.cc`, `tolk.shorturl.lk`) +
   `condosmap.vercel.app/cju1tn`. Matched the `openstreetmap.org` keyword
   presumably via embedded map tiles/content. A phishing-kit campaign —
   for another lane, not mine.
3. **Zillow/zilllow paired submission (2026-10-02 14:44–14:46 UTC,
   one-off):** `zillow.com` ×2 and typosquat `zilllow.com` ×2 submitted in a
   2-minute window — a researcher comparing legit vs typosquat, not an
   enumeration.
4. **traffic2archive.github.io SEO-backlink-generator cluster
   (Jan 2026, programmatic-one-off, NOT a cartographer candidate):** 7
   reports 2026-01-24–02-15, backlink-spam tool pages; matched `redfin.com`
   keyword presumably as a listed backlink source.

**VERDICT (this sweep): no map/POI swarm. Clean honest-negative on Western
map/POI systems for a second operator.** Every systematic-scan trace in the
09-28→10-05 window still resolves to the known Amap operator. Do not push
(per task).
