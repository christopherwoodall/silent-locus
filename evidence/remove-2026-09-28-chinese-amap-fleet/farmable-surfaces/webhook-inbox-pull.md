# webhook.site inbox pull — active-campaign dead-drops (2026-10-05 ~07:00 UTC)

**Method:** urlquery htmx `webhook.site` search → decoded base64/httpbun + livecodes beacon
programs → extracted 14 inbox UUIDs → pulled each via the no-auth token API
`GET https://webhook.site/token/<uuid>/requests` (documented in FINDINGS.md Pull 1).
11 live with data, 1 expired (404: `a47a3b01`, the `uq-amap-d/e/f/g` inbox), 1 inbox
discovered mid-analysis (`ccad3060`), 1 via href.li decode (`cbcb10de`).
Raw: `raw/2026-10-05-inbox-pull/` (14 inbox JSONs + 6 htmx search pages).

## The headline: the fleet is running an ACTIVE campaign RIGHT NOW

urlquery htmx `uqscan` (offsets 0–75, ~94 unique rows) shows continuous operator
activity **2026-10-04 ~19:20 UTC → 2026-10-05 04:11 UTC** (latest at pull time).
New task family: **cultural/landmark POI collection across Chinese provinces** —
museums, zoos, hospitals, bazaars, monasteries, film studios:

| Tag grammar | Example | Target |
|---|---|---|
| `<city>museum<date><letter>` | `qingdaomuseum20261005b`, `henanmuseum_page_20261005a`, `gxmuseum20261005a`, `fujianmuseum20261005page`, `nanhaimuseum1791145001`, `jxmuseum-mobile-detail`, `qdmuseum20261005a/b/c` | Qingdao/Henan/Guangxi/Fujian/Nanhai/Jiangxi museums |
| `<place>20261005<letter>` | `wuxizoo20261005a`, `taiyuan20261005b`, `taersi20261005`, `zhenbeibao20261005a`, `dawugang20261005b`, `anhui-famous-direct-20261005b` | Wuxi Zoo, Taiyuan, Taersi monastery, Zhenbeibao studio, Anhui famous sites |
| `claude20261005<target>` | `claude20261005mobile1/2`, `claude20261005ditussr/dituold`, `claude20261005bazaar`, `claude20261005hospital2/3`, `claude20261005gxzyy`, `claudeprime` | **explicit model-attribution labels — the harness tests Claude-family agents** |
| `research/target/direct/mobileapi/mobilerich` + date | `research20261005final1`, `target20261005suzhou`, `qdnewapi20261005a`, `qdoldditu20261005a`, `mobileapi20261005a` | multi-surface API coverage per POI |
| epoch / epoch-ms raw | `17911717674179`, `1791159341`, `backend1791159341` | run IDs |
| `<word>legacy<epoch>` | `palacelegacy1791142556` (livecodes.io, redirect chain) | same label family as `pandalegacy` |

**New surfaces under test per POI:** `ssr/api/getPoiInfo`, `ssr/api/getPoiDetail`,
`m.amap.com/api/getPoiDetailById`, `ditu.amap.com/detail/get/detail` (legacy ditu),
`www.amap.com/service/poiInfo?query_type=IDQ`, `www.amap.com/service/switchVersion`,
`pre-amap-pc-ssr.amap.com` (Amap staging host!), Amap's own Next.js chunks
(`ssr-next.amap.com/.../_next/static/chunks/...` tagged `claudeprime`), `user_loc`
geolocation spoofing (Hefei 117.2494,31.814395; Qingdao 120.473116,36.101532;
Yinchuan 106.071976,38.615380).

## The operator's true agent stack (from beacon bodies, not scanner metadata)

Beacon JSON bodies carry the loader's real `navigator.userAgent`:

- **Primary: `Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0`**
  from **195.64.118.152 (Norway)** — the operator's agent exit. Full harness cycle
  observed 2026-10-04 07:03:24–07:03:53: `boot → bxinit → xdcinit → capture ×5 →
  error ×5 → done` in 29s. This is the operator's own test run (complete lifecycle,
  pre-dates urlquery's 07:04 scan of the page).
- Same FF134 UA also from Norway IP on the `ccad3060` (Baxia signed) and `cbcb10de`
  (jina-cache) inboxes.
- **Secondary sightings: `Chrome/116.0.0.0 X11 Linux`** from a spread of
  PL/CZ/US/IN/BD/HK/NL/DE IPs, 07:07–07:22 — same beacon page, `xdcerr:
  "webTracker is not defined"` instead of `xdcinit`. Assessed as **third-party
  scanners/sandboxes tripping the public beacon page** (start 4 min after the
  operator's run, coincident with urlquery scanning; geographic spread =
  researcher infrastructure). Logged as observed, attribution uncertain.
- **Operator provisioning tooling:** `?verify=1` / `?hello=world` / `?headers=1`
  hits with **`python-requests/2.32.5`** and **`curl/8.14.1`** from Tencent Cloud
  IPs (43.162.198.97, 43.163.128.105, 43.154.138.36 — HK). The operator's inbox-
  provisioning script checks liveness with python-requests before the campaign.

## The beacon protocol (decoded from program sources + inbox traffic)

JSON-body kinds: `boot` (`{ua, href}`), `bxinit`/`bxerr`, `xdcinit`/`xdcerr`,
`capture` (`{url, headers}` — **harvests Amap's `bx-ua` anti-bot token per request**),
`error` (`{n}`), `load` (`{n, status, text}` — logs API response bodies),
`done`. Query-string beacons: `?k=HOOK/NOW/TOK/BE/P/CB/M/T/s`,
`?m=<epoch>&kind=state|open&v=bxok|gofallback&u=<url>`, `?i=<n>`, `?run=<epoch>`,
`?page=header3`, `?h=`, `?c=`, `?redir=`, `?signed=<signed URL>`.
Exfil transports: `fetch` POST, `XMLHttpRequest`, `new Image().src`, `navigator.sendBeacon`.

## Baxia anti-bot reverse-engineering (the campaign's actual objective)

The beacon programs call Amap's own anti-bot SDK directly:

```js
baxiaCommon.init({checkApiPath: u => u.includes('getPoiInfo'),
  uabOptions: {location: 'cn' /* A/B tested vs 'us'*/},
  appendTo: 'header' /* vs 'querystring' */, needUmidToken: true,
  paramsType: ['uab','umid','et'], awscTimeout: 15000});
```

- **"Baxia signed navigation"** (livecodes.io, title `Baxia signed navigation`):
  hooks `XHR.open`, waits for Amap's SDK to mint the `bx-ua` token, captures the
  SIGNED URL, exfils to `ccad3060…?signed=<url with bx-ua=231!…>`, then navigates.
  **Confirmed working**: inbox shows the operator's Norway/FF134 client exfiltrating
  a live signed URL (Oct 4 13:27:52). "Baxia" (霸下) is Amap/Alibaba's bot-guard
  SDK name — the operator names their bypass after it.
- **COMBO-INIT**: 5 staggered `live=N_<epoch>` probes against
  `getPoiInfo?id=B0138027SQ`, capturing the rotating `bx-ua` token each time.
- **`uq-amap-d`–`uq-amap-i`** (new tag grammar, Oct 4 10:29–10:44): hook Amap's
  `__fycb` JSONP callback + `getUidToken()`, query `m.amap.com/service/valueadded/
  infosearch.json`, exfil status+response text per key.
- **jina-cache test** (`jina-cache-1791133015584`, via href.li): 
  `r.jina.ai/https://amap-pc-ssr.amap.com/ssr/place/B001C8MXRO` (Chengdu Zoo) →
  **HTTP 200, markdown content exfiltrated in chunks** (`body0-0`, `body1-0`).
  **r.jina.ai is a CONFIRMED working Amap anti-bot bypass** for SSR place pages
  (reader-proxy → markdown → dead-drop). Connects to the skill-tracer lane's
  r.jina.ai keyless-fetch finding.
- Amap fights back: `load` beacons log `FAIL_SYS_USER_VALIDATE` /
  `RGV587_ERROR::SM::哎哟喂,被挤爆啦,请稍后重试` + `x5secdata` punish URLs —
  the agent is being rate-limited/bot-checked mid-campaign.

## New utility services in the operator's kit

- **livecodes.io** — live HTML playground hosting beacon/redirect programs
  (`Baxia signed navigation`, `palacelegacy1791142556` redirect chain). Same role
  httpbun's `/base64/` played in June.
- **href.li** — referrer-hiding wrapper around httpbun programs (2 rows).
- **r.jina.ai** — validated working Amap fetch proxy (see above).

## Inbox inventory (14 UUIDs)

| Inbox | Campaign use | Requests | Verdict |
|---|---|---|---|
| `9b8517a8` | COMBO-INIT (harness lifecycle) | 44 | operator run + scanner replays |
| `837b86f9` | LIVE (bx-ua open/state beacons) | 15 | operator + scanners |
| `c453433b` | `?m=&u=` open beacons | 7 | operator + scanners |
| `70671675` | `hdr` (header-capture program) | 5 | mixed |
| `ae7c9361` | `live` (fycb hook program) | 4 | mixed |
| `7c1bce05` | `uq-amap-i` (`?k=NOW/TOK/BE/P`) | 7 | operator |
| `892c4f17` | `uq-amap-h` (`?k=HOOK/NOW`) | 9 | operator |
| `a47a3b01` | `uq-amap-d/e/f/g` | 0 | **404 — expired** |
| `3b5027e4` | baxia redirect/hostname/`?h=`/`?c=`/`?i=` tests | 25 | operator + `?page=header3` UI browse |
| `a7753b69` | `?run=` + `?k=s` + `?v=&k=` sendBeacon | 33 | operator + python-requests/curl verify |
| `6ddc559e` | (bare inbox) | 5 | scanners |
| `0a947514` | (bare inbox) | 1 | 1 scanner GET |
| `ccad3060` | Baxia signed-URL exfil | 4 | **operator success beacon** |
| `cbcb10de` | jina-cache test | 13 | **operator success (200 + markdown)** |

## Notes / caveats

- Inboxes are public until expiry; the fleet rotates UUIDs per program. Re-sweep
  `webhook.site` on htmx for new inboxes each run — the token API needs no auth.
- The `UrlQueryCollector/1.0` UA in inboxes = urlquery's own crawler re-fetching
  beacon URLs (matches htmx scan IPs' ASNs, not the operator).
- `palacelegacy` label family (`<word>legacy<epoch>`) recurs — treat new
  `<word>legacy` labels as operator redirect-chain tests, not third-party.
- Scope: all of the above is agent/harness infrastructure metadata. No human/
  operator identity work was done or is implied (IPs are infra exit points).
