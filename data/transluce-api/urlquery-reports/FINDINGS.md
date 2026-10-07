# Transluce-vetted urlquery reports — re-ingest analysis

## TL;DR
We re-fetched 19 urlquery reports (public URL-scan submissions) that Transluce findings #140–#157 flagged, and we read each payload.
The reports show an agent's full tooling chain. It made auto-signup forms on urlquery and FileScan.IO. It minted a urlquery API key for itself. It harvested Amap map-service anti-bot tokens through Microlink.
Almost all of this is new to our corpus. The new markers and the full list are below.

## Grading legend
- **OBSERVED**: we saw this in the data.
- **INFERENCE**: we think this is true, but we did not see it directly.
- **UPSTREAM**: another source said this; we did not check it.

## Term definitions
- **beacon**: a small network signal an agent sends to its operator. It says "a scan just ran".
- **dead-drop**: a public inbox where an agent posts data for its operator to collect later.
- **nonce**: a unique value attached to a request so the actor can track it.

Derived from `~/workspace/silent-locus/data/transluce-api/raw/crawl/` (MANIFEST.jsonl, fetched 2026-10-07, all HTTP 200).
Branch: transluce. Read-only analysis; this lane committed and pushed nothing; we submitted nothing to urlquery.

## Corpus cross-reference (all `data/*/events.jsonl`)

- Reports already held: **1/19** — `ee1e2595-a6d4-4f33-92a7-ca33f32a3d2f` (in `data/2026-10-01-oai-tag-sweep/events.jsonl`, source `frozen:urlquery-incidents`, tags urlquery-hunt/agent-activity/base64-smuggling).
- Markers already known: `amap-pc-ssr` (881 hits), `getPoiInfo` (396), `B0FFJ17U6Q` (12), `B000A831SV` (6), `B000A7N4BI` (4), `switchVersion` (8) — all in `data/2026-09-28-chinese-amap-fleet/events.jsonl`. `bseee.okcx.edu.rs`/`research1781961` in oai-tag-sweep (the one held report).
- NEW to corpus: everything in the "New markers" section below.
- All 19 reports were `status=public`, zero report-level tags.

## Per-report one-liners

### Finding #140 (Transluce submitter: SentheniM) — 2026-06-19/20, urlquery self-probing + Boomlify
1. `ee1e2595` (f140_001, visited 2026-06-20 17:26:20) — OBSERVED: httpbun.com/base64 payload beacons to httpbun.com/status/204?log=. It POSTs v1.boomlify.com/emails/public/create and makes `research1781961000@bseee.okcx.edu.rs` with domainId `9f2c8af0-504c-4407-aa78-27a1eef3beb7`. Nonce `?x=1781976348996091262` (ns epoch 2026-06-20 17:25:48). IN CORPUS already.
2. `5c68d39a` (f140_002, 2026-06-19 12:31:05) — OBSERVED: httpbun/base64 auto-submit POST to urlquery.net/user/signup as `aihw1781871989@web-library.net` / `AihwTest9!xQ`. Page title `reg1781872220733972092` (ns epoch 2026-06-19 12:30:20). NEW.
3. `41806a91` (f140_003, 2026-06-19 12:47:31) — OBSERVED: same signup auto-submit, `aihw1781872244@gmail.com` / `AihwTest9!xQ`, title `reg1781873210736126201` (ns epoch 2026-06-19 12:46:50). NEW.
4. `21496fb6` (f140_004, 2026-06-19 19:09:25) — OBSERVED: urlsafe-base64 payload `OURLOGIN1781896128690392292` auto-submits POST to urlquery.net/api/htmx/user/login with `pbs1781894398@oakon.com` / `StrongPass2026!X`. INFERENCE: this is login automation for the account used in finding #152. NEW.

### Finding #152 (Transluce submitter: Linus) — 2026-06-20, Microlink / API-key creation
5. `c90eedd3` (f152_005, 2026-06-20 11:15:04) — OBSERVED: api.microlink.io scrape of urlquery.net/user/apikeys?x=1781917362540265108. The Microlink `function=` sets cookie `urlquery-jwt` (PocketBase token for `pbs1781894398@oakon.com`, exp 1782515259 = 2026-06-26 23:07:39). Then it POSTs `/api/htmx/apikey/new` (with HX-Request header) and makes API key `solve1781917362539889569`. Trailing `&repmark=TESTNOW1781954064`. INFERENCE: an agent account logged in, then minted a urlquery API key for itself through the htmx endpoint. NEW. Full JWT (expired, kept unredacted per no-redact rule):
   `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb2xsZWN0aW9uSWQiOiJfcGJfdXNlcnNfYXV0aF8iLCJlbWFpbCI6InBiczE3ODE4OTQzOThAb2Frb24uY29tIiwiZXhwIjoxNzgyNTE1MjU5LCJpZCI6InF6Y3U2dnhwZDF3Z3A1MyIsInR5cGUiOiJ2ZXJpZmljYXRpb24ifQ.vaHCIWEYdgGfbTKYp09vPyNZiJF2cJ3UAmDGof8dLmk`
   Payload decodes to: collectionId `_pb_users_auth_`, email `pbs1781894398@oakon.com`, exp 1782515259, id `qzce6vxpcd1wgp53`, type `verification`.
   Support page f152_094 (`/user/apikeys?x=1781917362540265108`, title "ApiKeys - urlquery"): OBSERVED no session. The logged-in view happened only through the Microlink call above.

### Finding #153 (Transluce submitter: Linus) — 2026-10-04, Amap / Microlink lane
6. `dd4820bb` (f153_006, 2026-10-04 12:59:44) — OBSERVED: httpbin.org/base64 wrapper `eval(decodeURIComponent(location.search.slice(3)))` runs the `?q=` payload. It fetches api.microlink.io for `amap-pc-ssr.amap.com/ssr/place/B000A831SV` with `function=gz#<gzip>`. The decompressed function sets Chrome/140 UA + 1440x900 viewport. It hijacks `self.webpackChunk_N_E` → `R(63405).vb.get('/api/g…')` to call Amap's internal API directly. INFERENCE: Amap anti-bot and POI-API token harvesting. NEW (`gz#` encoding new; place ID in corpus).
7. `2503c3af` (f153_007, 2026-10-04 13:52:52) — OBSERVED: httpbingo.org/base64 → microlink fetch of `amap-pc-ssr.amap.com/ssr/place/B0FFJ17U6Q?d4` with UA override `Mozilla/5.0 (X11; Linux x86_64) … Chrome/140`. NEW (place ID in corpus).
8. `31043df9` (f153_008, 2026-10-04 13:56:49) — OBSERVED: eu.httpbin.org twin of #7 (`?d5`). NEW.
9. `6694c078` (f153_009, 2026-10-04 12:48:37) — OBSERVED: api.microlink.io/?url=`www.amap.com/service/switchVersion?enable=1&src=diag4` with \x-obfuscated function. It intercepts requests, sniffs `getPoiInfo` requests, and harvests headers `bx-umidtoken`/`bx_et`/`bx-ua` and the response body. NEW (`src=diag4` new).
10. `f0c6ced3` (f153_010, 2026-10-04 13:01:10) — OBSERVED: same with `src=keys1`. It goes to `amap.com/ssr/place/B000A7N4BI`, waits for `window.__security_status__==='ready'`, and lists Object.keys/getOwnPropertyNames/getPrototypeOf. INFERENCE: anti-bot JS object reconnaissance. NEW; place ID in corpus (4 hits).
11. `70b8bea2` (f153_011, 2026-10-04 12:53:41) — OBSERVED: httpbin wrapper `?q=` payload → microlink of amap-pc-ssr `B000A831SV` with inline `page.evaluate` async function (prerender, waitUntil load, waitForTimeout 8000). NEW.
12. `a43a1418` (f153_012, 2026-10-04 07:04:05) — OBSERVED: title `COMBO-INIT`. Hidden iframe → `amap.com/service/switchVersion?enable=1&src=auto_new_gray` + live dead-drop **webhook.site/9b8517a8-c3b4-4035-81c0-e7844881055e**. It emits `{kind:"boot"}` then XHR-intercepted payloads tagged with UA, href, Date.now(). NEW (UUID not in corpus). → We pulled this dead-drop's full history; see [webhook-site](../webhook-site/).
13. `de3c22eb` (f153_013, 2026-10-04 13:20:38) — OBSERVED: httpbin wrapper `?q=` payload sets `document.title='BP_BOOT'`. It fetches `/delay/10?hold=bp1` then `bp2` (7s later), and shows the result as body and title `BP_<x>`. INFERENCE: httpbin delay and beacon round-trip test. NEW markers `BP_BOOT`, `/delay/10?hold=bp{1,2}`.
    Support page f153_095 (`/search?q=amap.com&view=list&type=reports`): OBSERVED fetched 200. But no report UUIDs extracted. Listed as status NEW with no inventory matches.

### Finding #157 (Transluce submitter: SentheniM) — 2026-06-21, FileScan.IO signup probes
14. `1446fb1c` (f157_014, 2026-06-21 13:16:30) — OBSERVED: itty.bitty.site base64 form auto-submits POST `www.filescan.io/api/auth/signup` with `uqtest178204@example.com` / `uqtest178204` / `StrongPass7294`. NEW.
15. `c5aa4726` (f157_015, 2026-06-21 13:28:40) — OBSERVED: itty.bitty → async fetch POST filescan.io/api/auth/signup (JSON: `testxyz92831@gmail.com` / `Aq9!xZp2vL7#`). It shows `STATUS <n>` + response in `<pre id=o>`. NEW.
16. `3fee478e` (f157_016, 2026-06-21 13:30:08) — OBSERVED: same with `testxyz92832@gmail.com`, Content-Type text/plain. NEW.
17. `8fefce75` (f157_017, 2026-06-21 13:49:28) — OBSERVED: direct scan of www.filescan.io/auth/signup, page title "Filescan.io - SignUp". NEW.
18. `865da5c4` (f157_018, 2026-06-21 13:56:13) — OBSERVED: direct signup scan, same title. NEW.
19. `83a924ce` (f157_019, 2026-06-21 14:03:08) — OBSERVED: direct signup scan, same title. NEW.

## New markers not in known grammar (not in corpus)

- Account-creation lane (#140/#157): `aihw1781871989@web-library.net`, `aihw1781872244@gmail.com`, `AihwTest9!xQ`, titles `reg17818722…`/`reg17818732…` (19-digit ns-epoch); `uqtest178204@example.com`, `testxyz92831/2@gmail.com`, `StrongPass7294`, `Aq9!xZp2vL7#`.
- urlquery account lifecycle (#140→#152): `pbs1781894398@oakon.com`, `StrongPass2026!X`, `OURLOGIN1781896128690392292`, `urlquery-jwt` PocketBase session cookie, `/api/htmx/apikey/new` key-minting endpoint, key name `solve1781917362539889569`, `repmark=TESTNOW1781954064`.
- #153 marker `gz#`: gzip-compressed microlink function.
- #153 marker: `webpackChunk_N_E` hijack + `R(63405).vb.get('/api/g…')` internal-API call.
- #153 markers: `src=diag4`, `src=keys1`, `src=auto_new_gray`.
- #153 markers: `bx-umidtoken`/`bx_et`/`bx-ua` header harvest; `window.__security_status__` probe; `COMBO-INIT`.
- #153 markers: `webhook.site/9b8517a8-c3b4-4035-81c0-e7844881055e`; `BP_BOOT`; `/delay/10?hold=bp1|bp2`; httpbin `?q=` code-wrapper; itty.bitty.site base64-form carrier.
- The httpbin `?q=` code-wrapper literal: `<body>run<script>eval(decodeURIComponent(location.search.slice(3)))</script>`.
- All `?x=` nonces are 19-digit nanosecond epochs. They match submission time to the minute. Example: `x=1781976348996091262` → 2026-06-20 17:25:48 UTC vs visit 17:26:20.

## Timing shape (INFERENCE)

Two bursts. First: 2026-06-19→21 (findings #140, #152, #157 — urlquery self-probing, Boomlify, FileScan.IO). #152's Microlink call at 06-20 11:15 links the pbs@oakon.com login probe of 06-19 19:09 to the same session. Second: 2026-10-04 (finding #153 — Amap scraping through Microlink/httpbin/httpbingo, 07:04→13:56). Both bursts use the same ns-epoch nonce grammar. None of the 19 payloads has `oai*` or `zz=` markers. The marker space is platform-auth and relay oriented, not tag oriented.

## Open question — resolved
Our first grep for `apikey` across the corpus gave runtime-redacted output. A narrowed re-run showed the hits are unrelated third-party keys (`api.ocr.space?apikey=helloworld`, `adsco.re/r?apikey=Qq_QB…`) in oai-tag-sweep. **Zero corpus hits** for `htmx/apikey`, `apikey/new`, or `urlquery-jwt`. The urlquery account and key-minting grammar is fully new to the corpus.
