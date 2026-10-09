# PATTERN.md — Chinese Amap fleet fingerprint (2026-09-28 → 2026-10-05)

Mined from 2,000 urlquery reports (1,970 amap.com + 30 gaode.com). A hunter can match this fingerprint elsewhere.

## Task signature
- Target: Amap (高德地图) place pages and `getPoiInfo` API — entrance navigation shares (`sub_poi_navi`, `clk_ratio`) for parks, museums, zoos, hospitals.
- 216 distinct place IDs (`B…` format, e.g. `B001C8MXRO`), peak 213 places on 4 Oct.

## Tag grammar (`fleet_tag`)
- Params: `uqscan=` (1,024 uses), `uq=` (31), plus `uqtarget=` and `uqhost=` (4 reports, ditu subdomain). No `uqtag=` in the main fleet (but `uqtag=` keys the ltzh family's beacon exfil).
- Shape: `<word-fragment><YYYYMMDD>[a-z suffix]` or `<word-fragment><epoch>` or bare UUID/epoch.
  - Examples: `claude20261004target1`, `research20261004b`, `target20261004a`, `direct1791108114`, `7d52beed-…`
- 932 distinct tags — high-entropy per-run labels, ~783/843 used once (per report).
- Pinyin fragments: place names (`taersi`, `mianyang`, `jincheng`, `beihai`, `potala`, `bailuzhou`), task words (`ditu`=map, `target`, `api`, `mobile`, `ssr`), English (`research`, `direct`, `verify`, `share`).
- "claude" labels (211): `claude20261004…` — false-flag per report; code matches Tencent Hy4/Zhipu GLM.

## Route taxonomy (submitted-URL domain)
- `direct` (amap.com/gaode.com submitted directly) — majority early phase.
- `relay` (r.jina.ai, microlink, href.li, translate.goog, allorigins) — grows on 4 Oct (30 relay submissions 06:00–12:00).
- `carrier` (httpbin/httpbun programs, LiveCodes pages, webhook.site inboxes submitted as scan targets).
- Wrapper chain observed: `href.li/?https://httpbun.com/base64/<program>` — base64 programs staged on httpbun, submitted via redirector.

## Dead-drop pattern
- Programs exfiltrate to `webhook.site/<uuid>` inboxes; inboxes themselves submitted to urlquery (report `97f0619b` = inbox URL).
- Inbox creation → first marked request in ~1s (report evidence); creator = `python-requests/2.32.5` from Tencent Cloud.

## Program shape (from full reports)
- `<!doctype html>` lowercase (74%), single-line programs (66%) — matches Hy4/GLM, not Claude.
- Reads `sub_poi_navi`/`clk_ratio`, writes `name:ratio` into `document.title`.
- Generates Alibaba anti-bot tokens (`bx-ua`, `bx_et`, UMID); reads browser cookies and exfiltrates them.

## Timing
- Active hours (UTC): broad 00:00–13:00, peak 10:00–11:00 (188/hr). Quiet 14:00–17:00 UTC.
- Parallelism: 4–8 concurrent runs, peak 15; 51 places in busiest hour.
- Date labels run on China time (UTC+8): late-UTC tags carry next-day China dates. Time-of-day tags match UTC within 3 min.
- Fleet still active at collection time (latest report 2026-10-05T01:12Z).


## `ltzh-` program family (alternate/copycat, 2026-10-04)
6 httpbin.org/base64 programs, all 2026-10-04 12:58–13:15 UTC. `ltzh` prefix unattributed; raw `ltzh` keyword is 99% noise (207 hits) — only these 6 are signal.
- `ltzh-jina-post-inject-20261004a` — POSTs Amap place URLs to `https://r.jina.ai/` with `injectPageScript` (jina browser-automation API); injected script XHRs `/ssr/api/getPoiInfo`; exfils via chunked image beacons `/status/204?uqtag=<tag>&part=<n>&data=<b64>` keyed `jinapostinj`/`jinaposterr`; sets `document.title='jpost-<status>-<len>'`.
- `ltzh-jina-json-cache7d-20261004a/b` — jina JSON-cache variants (7-day cache), same beacon exfil.
- `ltzh-iframe-ssr-20261004a`, `ltzh-iframe-ssr-big-20261004a`, `ltzh-iframe-www-20261004a` — iframe loaders.
- Distinguisher vs main fleet: uses `uqtag=` (not `uqscan=`), jina POST API (not GET), image-beacon exfil (not webhook POST). Same Amap task family, same day — likely fleet alternate tooling or a copycat.

## Redirector diversification (other-targets lane, 4 Oct)
Beyond href.li: postman-echo.com, kennethreitz.org, nghttp2.org, google url-redirect, spoo.me, httpbingo.org, tinyurl.com — same redirect-to-Amap shape, same tag grammar. First China-hosted carrier: ceshiren.com (httpbin mirror). Fleet also self-surveys on urlquery.net (own place-ID search).

## Negative space (what's absent)
- No `zz=`/`zzbulk`/`prepnonce` nonce grammar (June OpenAI incidents) — different operator, different harness.
- No `uqtag=` — fleet uses `uqscan=`/`uq=` only.
- No Amap/gaode hits in our June corpora (147 `mamap260618` substring false positives only).
- Predicted dead-drop alternatives all zero in-window: beeceptor, pipedream, requestcatcher.
- Predicted JS sandboxes all zero in-window: codepen.io, jsfiddle.net, observablehq.com.
- pastebin.com ×2 in-window: fetched one, zero fleet markers — not fleet-related.

## Stylometric pivots (n-gram → search term → result)
Mined from fleet program text (httpbun base64-decoded programs, LiveCodes pages).
Ranked by fleet-frequency × web-rarity:

| n-gram | Fleet hits | Web hits | Pivot result |
|---|---|---|---|
| `sub_poi_navi` | 24 urlquery | 0 (confirmed) | 21 httpbin.org + 2 amap.com + 1 httpbun.com — all fleet. Perfect fingerprint. |
| `clk_ratio` | 6 urlquery | — | 6 httpbin.org — all fleet programs. |
| `bailuzhou` (+`<word>-<epoch>` titles) | 8 | — | 7 httpbun.com + 1 amap.com. Place-anchored program titles. |
| `hanshan-baxia` | 1 | — | 1 httpbun.com. |
| Program title grammar | — | — | `<place>-<descriptor>-<epoch>`: `dalian-jsapi-1791135514199`, `bailuzhou-pulseiframe-1791131179`, `Amap popup boot 1791130764`, `BT1791131775910`, `PS1791126733846`. |
| `AMAPREDIRECT` | 1 | — | 1 httpbin.org program title. |

## Technique-based predictions (checked)
| Predicted surface | Rationale | Result |
|---|---|---|
| beeceptor / pipedream / requestcatcher | dead-drop alternatives to webhook.site | 0/0/0 in-window — fleet stays on webhook.site |
| codepen.io / jsfiddle.net / observablehq.com | JS sandbox alternatives to LiveCodes | 0/0/0 — fleet stays on LiveCodes + httpbun |
| Baidu Translate as relay | Chinese-infra mirror of translate.goog tradecraft | HIT — `fanyi.baidu.com/transpage?query=<amap-url>` ×2 (see INFRA.md) |
| pastebin.com | paste alternative | ×2, neither fleet-related |
