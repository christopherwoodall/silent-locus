# FINDINGS — webhook.site dead-drop 9b8517a8 (live Amap-scraper beacon)

## TL;DR
This inbox was the target in a urlquery report ([f153_012](../urlquery-reports/), title COMBO-INIT).
We read its full history (read-only; no auth needed): 47 requests from 9 IPs in 8 countries. Seven sessions run the same scraper state machine (boot → bxinit → xdcinit → capture → error → done). Two requests are strays.
One beacon captured Amap's own rejection: "system overwhelmed, please retry later" plus a captcha challenge. We found zero of our marker grammar (no `oai*`, `zz=`, epoch nonces).

## Grading legend
- **OBSERVED**: we saw this in the data.
- **INFERENCE**: we think this is true, but we did not see it directly.
- **UPSTREAM**: another source said this; we did not check it.

## Term definitions
- **inbox**: a web address that receives and shows data. webhook.site gives one inbox per token.
- **dead-drop**: a public inbox where an agent posts data for its operator to collect later.
- **beacon**: a small network signal an agent sends to its operator. Example: `{kind:"boot"}`.
- **nonce**: a unique value attached to a request so the actor can track it.
- **POI**: point of interest. Amap's `getPoiInfo` API returns data for one POI id.

Date: 2026-10-07. Read-only: `GET https://webhook.site/token/9b8517a8-c3b4-4035-81c0-e7844881055e/requests` (HTTP 200, 312,520 bytes, sha256 e9130654… in PROVENANCE.md). We submitted nothing. We removed nothing.

## What this inbox is (INFERENCE)

The token UUID `9b8517a8-c3b4-4035-81c0-e7844881055e` is hard-coded in the COMBO-INIT page from urlquery report f153_012 (finding #153, [urlquery-reports](../urlquery-reports/)). That page is a JavaScript scraper aimed at Amap's map service (amap.com, the Chinese mapping platform). It hijacks the page's network calls. Each time a `getPoiInfo` (POI lookup) request fires, it POSTs the request URL + headers + cookies to this inbox. A webhook.site token URL is its own read credential. No other auth is needed. So we pulled the full history without touching the inbox.

## The sessions (OBSERVED)

47 requests, 9 IPs, 8 countries. Seven sessions run the beacon state machine. Two are strays.

| Session (IP → country) | Time (UTC) | Beacon sequence |
|---|---|---|
| 195.64.118.152 → Norway | 2026-10-04 07:03:24–07:03:53 | boot, bxinit, xdcinit, then 5× (capture, error), done |
| 137.97.194.74 → India | 2026-10-04 07:07:25–07:07:39 | boot, bxinit, xdcerr, capture, load |
| 85.237.212.35 → Poland | 2026-10-04 07:10:26–07:11:04 | boot, bxinit, xdcerr, 5 captures, 5 errors, done |
| 178.93.150.39 → Hong Kong | 2026-10-04 07:17:05–07:17:07 | boot, bxinit, xdcinit (cut short — no captures) |
| 147.90.209.20 → USA | 2026-10-04 07:19:20–07:19:21 | boot, bxinit, xdcinit (cut short) |
| 158.173.77.2 → Netherlands | 2026-10-04 07:22:21–07:22:22 | boot, bxinit, xdcinit (cut short) |
| 108.211.177.16 → USA | 2026-10-07 03:13:53–03:13:54 | boot, bxinit, xdcinit (cut short) |
| 170.246.54.143 → Canada | 2026-10-04 07:05:00 | single GET, UA `UrlQueryCollector/1.0`, empty body — a scanner, not the scraper |
| 212.102.39.87 → Czechia | 2026-10-04 07:09:20 | single GET, Android UA, empty body — stray |

The six 2026-10-04 beacon sessions land in a ~19-minute window (07:03–07:22). A seventh beacon session arrived 2026-10-07 03:13. The drop was still live three days later.

## The state machine (OBSERVED)

- `boot` — the page loaded. The beacon carries UA + page URL (an httpbin.org/base64-wrapped COMBO-INIT page) + `Date.now()`.
- `bxinit` / `xdcinit` — the two Amap tracker SDKs started. On the two Chrome/116 sessions the XDC tracker failed: `xdcerr` = `ReferenceError: webTracker is not defined`.
- `capture` — one intercepted `getPoiInfo` call: request URL + harvested headers (`bx-ua`, `bx-umidtoken` family) + cookies + seq number.
- `error` — a failed attempt (numbered n=1..5).
- `load` — one captured full API response body.
- `done` — session end.

## The Amap rejection (OBSERVED)

The India session's `load` beacon (07:07:39) carries Amap's actual response to `getPoiInfo?id=B0138027SQ`:

- Status: `"ret":["FAIL_SYS_USER_VALIDATE", "RGV587_ERROR::SM::您好，被挤爆了，请稍后重试"]`. The Chinese text means: "Hello, the system is overwhelmed, please retry later."
- The response also embeds a captcha-challenge URL (`.../ssr/api/getPoiInfo/_____tmd_____/punish?x5secdata=...&action=captcha`). Amap was actively challenging this lookup.

INFERENCE: Amap was rate-limiting or challenging the scraper. The dead-drop captured the rejection itself. The operator sees exactly when Amap pushes back. This matches the anti-bot-token-harvesting tooling in [urlquery-reports](../urlquery-reports/) finding #153.

## Marker grammar (OBSERVED)

Zero hits for our families across all 47 requests: no `zz=` params, no `oai*` tags, no epoch nonces. The one case-insensitive "oai" match is an uppercase `OAi` fragment inside a base64 cookie blob. It is noise, not grammar. Same marker space as finding #153: platform-auth and relay oriented, not tag oriented.

## Verdict

This is the live operational side of finding #153's COMBO-INIT report. These are real scraper sessions, not only a scanned page. They phone home to this inbox. The ~19-minute, 6-country burst on 2026-10-04 plus a fresh session on 2026-10-07 says the tooling is active. It is not a one-off test. The captured Amap rejection is the strongest single byte of evidence. It shows the operator's scraper losing the anti-bot fight on `getPoiInfo?id=B0138027SQ` and reporting the loss home.

## Most actionable lead

Watch the inbox. A new session pattern (or its absence) shows if the operator kept this drop after the 2026-10-07 session. The captured URLs carry `live=N_<epoch>` params (per-request counters and times). Future capture URLs against these 11 would show if the same scraper binary kept running.
