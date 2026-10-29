# urlscan.io sweep — Chinese Amap fleet (Tencent Hunyuan)
Lane: urlscan.io | Date run: 2026-10-04 (Sun ~20:40 CDT) | Analyst: urlscan lane agent

Method: public anonymous search API (`https://urlscan.io/api/v1/search/?q=<query>&size=100`), no key.
Raw query JSON saved alongside as `q_<name>.json`. Anonymous window note: results are
limited to the last 30 days (`search_date_limit_days: 30`), which covers the fleet window
(28 Sep – 5 Oct 2026). Leading-wildcard searches are blocked for anonymous users (403);
exact-phrase syntax used instead. No 429 rate-limit hit. Full result-body fetch requires
login (anonymous `/api/v1/result/<uuid>/` returns `{"warning": "You're not logged in!"}`),
so verdicts rest on search metadata (URL, page title, date), not page bodies.

## Query log and hit counts

| Query | Total | Fetched | Verdict |
|---|---|---|---|
| `sub_poi_navi` | 0 | 0 | **zero** — fleet's pivot term has no urlscan presence |
| `sub_poi` | 0 | 0 | **zero** |
| `clk_ratio` | 0 | 0 | **zero** |
| `uqscan` | 0 | 0 | **zero** — no fleet tag format on urlscan |
| `uqscan=` | 0 | 0 | **zero** |
| `page.title:"bailuzhou"` | 0 | 0 | **zero** |
| `page.title:"taersi"` | 0 | 0 | **zero** |
| `page.title:"ditu"` | 0 | 0 | **zero** |
| `page.title:"pulseiframe"` | 0 | 0 | **zero** |
| `page.title:"AMAPREDIRECT"` | 0 | 0 | **zero** |
| `filename:AMAPREDIRECT` | 0 | 0 | **zero** |
| `getPoiInfo` | 0 | 0 | **zero** |
| `bailuzhou` (bare) | 0 | 0 | **zero** |
| `taersi` (bare) | 0 | 0 | **zero** |
| `pulseiframe` (bare) | 0 | 0 | **zero** |
| `ditu` (bare) | 0 | 0 | **zero** |
| `domain:amap.com` | 809 | 200 | 1 marker hit — **unrelated** (see below) |
| `domain:amap.com uqscan` | 0 | 0 | **zero** |
| `page.title:"amap"` | 14 | 14 | **all unrelated** (see below) |
| `domain:httpbun.com` | 1 | 1 | **unrelated** (see below) |
| `domain:httpbun.com amap` | 0 | 0 | **zero** |
| `href.li httpbun` | 0 | 0 | **zero** |
| `webhook.site amap` | 0 | 0 | **zero** |
| `domain:livecodes.io` | 1 | 1 | **unrelated** (see below) |
| `page.title:"mianyang"` | 2 | 2 | **both unrelated** (see below) |

Also recorded totals only (too broad to triage in budget): `domain:href.li` = 8325,
`domain:webhook.site` = 134. Fleet-specific AND-combos against both were zero.

## Examined hits — all verdict: UNRELATED

1. **`domain:amap.com` (809 total, newest 200 triaged: 2026-09-28 → 2026-10-05)**
   Marker scan (`uqscan`, `getpoiinfo`, `href.li`, `httpbun`, `pulseiframe`, `base64`,
   `sub_poi`, `clk_ratio`, `amapredirect`) found exactly one hit: `https://jec.jlevm.cn/`
   (2026-10-03), title 吉林省新能源监控平台 ("Jilin new-energy monitoring platform").
   No fleet tags, no fleet titles, no program-staging URLs — a normal Chinese map-SDK
   consumer. Verdict: unrelated.
2. **`domain:httpbun.com` (1 hit)** — `https://httpbun.com/mix/s=200/h=content-type:
   application%2Fjavascript/b64=...` (2026-09-22). Predates the fleet window (28 Sep);
   uses `/mix/...` feature-test path, not the fleet's `/base64/` program-staging pattern;
   decoded body is a generic `(self._GP=self._GP||[]).push("H4sIAA...")` test snippet,
   nothing Amap-related. Verdict: unrelated.
3. **`domain:livecodes.io` (1 hit)** — `https://markdown-to-livecodes-vitepress.pages.dev/`
   (2026-10-03), "My Awesome Project" demo. No fleet markers. Verdict: unrelated.
4. **`page.title:"mianyang"` (2 hits)** — `http://18jx-nk.cyou/` (typosquat, 2026-09-21)
   and `https://cloudflare-imgbed-atb.pages.dev/` (image-bed demo, 2026-09-19). No fleet
   markers. Verdict: unrelated.
5. **`page.title:"amap"` (14 hits)** — Azure internal hostnames (`amap-intcusa-sts-db-1.
   postgres.database.azure.com`, `amap-nprcusa-primary-vcp-db...`, `amr-sesn-nonprod-
   amap-cus...`) plus `amapacad.org.ng` (Association of Marketing Academic Professionals).
   All name collisions, none Chinese map scraping. Verdict: unrelated.

## Bottom line

**Honest zero for the fleet on urlscan.io.** None of the fleet's distinctive fingerprints —
`sub_poi_navi`, `clk_ratio`, `uqscan` tag format, `getPoiInfo` in URLs, fleet pinyin
place-name titles (`bailuzhou`, `taersi`, `mianyang` + descriptor + epoch),
`AMAPREDIRECT`, or httpbun.com/base64 program staging tied to Amap — appear in urlscan.io's
searchable corpus within the fleet's active window. Two plausible explanations, not
distinguished: (a) the fleet's pages were submitted to urlquery.net, not urlscan.io;
(b) urlscan has them but they aren't publicly indexed/searchable.

**Recommendation for other lanes:** keep the fleet pivots (`sub_poi_navi`, `uqscan=`,
httpbun `/base64/` staging) on urlquery.net / direct HTTP collection; urlscan.io is a
dead lane for this fleet as of 2026-10-04. Re-run only if the fleet's staging pattern
changes (e.g. non-httpbun hosts) or if fleet pages start getting submitted to urlscan.io.
