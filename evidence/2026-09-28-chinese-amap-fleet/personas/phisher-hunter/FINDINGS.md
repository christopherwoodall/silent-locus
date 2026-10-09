# PHISHER HUNTER — agent-run phishing operations

**Persona:** hunt AGENT-RUN phishing operations — kits deployed and operated by agents, not humans.
**Date:** 2026-10-05. Egress was up but flaky (IncompleteRead on the stock htmx tool); a curl-based search replica (`/tmp/uq_curl.py`) was used for all queries at ≤1 req/5-10s. No commits/pushes.

## Method

Searched urlquery htmx for phish-kit infrastructure: `xsph.ru`, `urldance.com`, `ddnsgeek.com`, `wasmer.app`, `secursalf`, `tetes-air.pages.dev`, `api.telegram.org/bot`, `sendMessage`. Pulled full report internals via the keyless `/api/htmx/report/{id}/filter/http` endpoint for the freshest kits. Every candidate was verified against our three corpora (amap-fleet 2,141; openai-agent-traces 589,972; oai-tag-sweep 96,353).

## Headline verdict

**No confirmed agent-OPERATED phish farm found.** The phish-kit ecosystem visible on urlquery.net is commodity: human kit operators deploying on free hosting (Sprinthost, wasmer.app, Vercel, Cloudflare Pages) plus takedown-vendor submission pipelines. The agent presence in this space is on the AUDITOR side (the jmail.world auditor) — auditing farms, not operating them. All phish infrastructure below is **genuinely new** (zero hits in all three of our corpora) and unattributed.

## 1. xsph.ru — Sprinthost free-subdomain kit farm (commodity)

28 reports, `a<7-digit>.xsph.ru` subdomains (e.g. `a1306096.xsph.ru`, `a1270050.xsph.ru`). **Important correction to prior notes:** these are Sprinthost's auto-assigned free-subdomain format, NOT agent-generated names. Lure paths: QuickBooks auth (`/payment/quickbook-authentication.htm`), LinkedIn verify, Orange mail (`/mail-serveur/orange/`), S3-themed lures. The profiler's "metronomic burst" (6 reports in 2 min, Oct 5 05:04) reads as a takedown-vendor sweep, not deployment — subdomains are host-assigned. Verdict: commodity kit abuse of free hosting.

## 2. urldance.com — phishing redirector farm (operator unknown)

17 reports. Date-rotated subdomains (`202608.urldance.com`, `2026-09-28.urldance.com`) with sequential campaign paths `/6d/`, `/7d/`, `/8d/` and destinations as query params (`?eqntceo.top#others`). One report pulled: password-lure CSS (`/css/password.css`), `js-sdk-pro.min.js`, `at-map.js`. This IS a redirector farm of the class the jmail.world auditor was auditing — but a different farm. Date-rotation could be cron-driven (agent or script); **no agent markers observed**. Operator unidentified. This is the closest thing to an "operator of a redirector farm" in the data — worth watching for machine-cadence rotation.

## 3. wasmer.app — crypto-wallet impersonation phish

40 reports. `app-ledger-desktop.wasmer.app`, `trezer-io-start.wasmer.app`, `rabby.wasmer.app` (Ledger/Trezor/Rabby wallet lures, Jan 2026). Fresh: `wordpress-c2627.wasmer.app/wp-content/` (submitted twice 2026-10-05, 02:07 and 04:55 UTC) — a **PayPal login phish** (PayPalOpen fonts, `contextualLoginElementalUIv4.css`) staged under a fake WordPress path, with `?admin_check=1` probe. Full report internals show a **live Telegram bot exfil wired in** (`api.telegram.org/bot<BOT_ID>:<TOKEN>/sendMessage`). wasmer.app auto-names deployments (`name-XXXX`) — deploy-and-discard shaped, agent-deployable, but no agent markers observed.

## 4. vercel.app — Spanish-language phish with Telegram exfil

`secursalf-a.vercel.app` — 6 submissions Oct 4–5 (05:09, 14:26, 17:05, 17:08, 18:02, Oct 5 03:29). Irregular intervals = takedown-vendor re-submissions of one live kit, not metronomic deployment. Spanish-language lure (`flecha-abajo.jpg`, Open Sans), **Telegram bot exfil wired in** (`api.telegram.org/bot<BOT_ID>:<TOKEN>/sendMessage`). Commodity.

## 5. Telegram-bot exfil dead-drops (programmatic harvest structure)

The credential-harvest dead-drop layer IS programmatic in structure, but it's kit-template behavior, not agent behavior:
- Template URLs submitted directly: `api.telegram.org/bot${8935051385:<TOKEN>}/` (report `bfcfa709`, 2026-09-01), `api.telegram.org/bot${6956871343:<TOKEN>}` (report `b8446c80`, 2025-09-26), `api.telegram.org/bot$/sendMessage?chat_id=&text=<HOST INFO>` (report `817c64b5`, 2025-12-17) — kit authors testing their exfil templates through urlquery
- Live bot tokens observed in the two fresh kit reports (bot IDs 8569447474, 8794627026 — tokens redacted here; they are live attacker credentials visible in public reports)

**Security note:** live Telegram bot tokens are present in these public urlquery reports. Tokens are redacted in this report; bot IDs retained as infrastructure identifiers.

## 6. tetes-air.pages.dev — Amazon-review lure (commodity)

20 reports, Aug–Oct 2026. `/dp/B0B6GK4VTC?ref=MarsFS_VICC_...` — Amazon product-page-pattern lure with affiliate-style ref params. Long-lived single deployment, repeatedly re-submitted. Commodity.

## 7. ddnsgeek.com — negative

Only the bare domain (2023). The profiler's gibberish DDNS pair came from the homepage feed, not the search index. No agent-shaped DDNS activity found.

## Verification against our corpora

| Pattern | amap-fleet | openai-agent-traces | oai-tag-sweep |
|---|---|---|---|
| xsph.ru | 0 | 0 | 0 |
| urldance | 0 | 0 | 0 |
| wasmer.app | 0 | 0 | 0 |
| telegram.org/bot | 0 | 0 | 0 |
| secursalf | 0 | 0 | 0 |
| ddnsgeek | 0 | 0 | 0 |

All genuinely new. None of our known agents operate phish kits.

## Agent-shaped assessment (honest)

What would confirm agent-RUN phishing: machine-cadence kit deployment (same kit redeployed on a schedule after takedowns), programmatic bot-token rotation across a kit family, agent grammar (nonces, epoch markers) in kit paths, or kits deployed via hosting APIs on a timer. **None observed.** The free-tier deploy-and-discard shape (wasmer/vercel auto-naming, Pages auto-naming) is agent-deployABLE but every instance here lacks agent markers. The urldance date-rotation is the one mechanism worth a re-check for machine cadence.

The doctrine holds inverted here: in the phishing space, the confirmed agent is the AUDITOR (jmail.world), not the operator. If agents run phish ops, they aren't submitting the kits to urlquery with fingerprints we can see — or they operate on infrastructure we haven't found yet.

## Open follow-ups

1. urldance.com date-rotation cadence: pull 30 days of `url.domain:urldance.com` and test for cron-regular rotation (agent vs human operator).
2. `fluxion-shop.site.je`, `quelltech.shop`, `rankedsurfers.com`, `chargeblast.com` (sendMessage content matches, Oct 3–4) — unexamined shop-phish cluster.
3. Kit-family token rotation: same lure across deployments with different bot IDs = programmatic ops.
4. The `?admin_check=1` probe pattern on wasmer kits — whose probe grammar is that?

---

## APPENDIX — All observed URLs

### xsph.ru kit farm (28 reports)
- a1306096.xsph.ru/wa-cache/61f9ab/htaccess.auth/captcha-gateway00.htm
- a1303879.xsph.ru/c4.west-009/Revised.eu904.htm?eta=halor7@slurpmail.net
- a1302945.xsph.ru/nt?utm_source=retentio&utm_medium=email&utm_campaign=aaaaa
- a1270050.xsph.ru/s3.east-005-a-1db39d6a1b0485b16b052c82a823a006/payment/quickbook-authentication.htm
- a1270050.xsph.ru/s3.east-005-a-1db39d6a1b0485b16b052c82a823a006/docs/files-s3-spb-01.php
- a0207112.xsph.ru.xsph.ru/wp-content/uploads/my_images/daud.jpg?id=793
- a0991447.xsph.ru/lil/alldomainn/?email=eudora@xl-tungsten.com&source=gmail&ust=1775148136075000&usg=
- a0827550.xsph.ru/@==gcld3bsZEdjVGdvJHc
- a0698649.xsph.ru
- a1203640.xsph.ru/mail-serveur/orange/
- a0772580.xsph.ru/...../linkedinverify/?fkabj=*@*

### urldance.com redirector farm
- 2026-09-28.urldance.com/en?eqntceo.top
- 202608.urldance.com/7d/?ofkihef.xyz#others
- 2026-09-28.urldance.com/en?yourongwenhua.com
- 202608.urldance.com/7d/?meactcfe.cc#others
- 202608.urldance.com/7d/?mosrkhmg.top#others
- 202608.urldance.com/7d/?oumeidaquan.icu#others
- 202608.urldance.com/6d/?339629.xyz#others
- 202608.urldance.com/8d/?avnight.app#others
- 202608.urldance.com/7d/?xosbydup.xyz#others
- 2026-09-22.urldance.com/en?cloyab9606.top
- 202608.urldance.com/6d/?ap0135.vip#others
- 2026-09-22.urldance.com/en?wbrutjow.xyz
- 2026-09-07.urldance.com/en?93cymex0bqe.xyz
- 2026-09-06.urldance.com/en?biglist07.cc
- 2026-09-04.urldance.com/en?66pp8.xyz
- urldance.com/en?
- 2026-07-26.urldance.com/us?llw8.cc

### wasmer.app wallet phish + PayPal kit
- wordpress-c2627.wasmer.app/wp-content/ (PayPal phish, Telegram exfil; reports c4075c0f, 10f64584)
- https://urlquery.net/report/c4075c0f-814a-48ad-886a-1e2e4b6eea2e
- https://urlquery.net/report/10f64584-0f41-4daf-9a91-f37beb561998
- app-ledger-desktop.wasmer.app
- www.trezer-io-start.wasmer.app/
- rabby.wasmer.app/
- document894-dc115.wasmer.app/
- ukmpanahanusm.wasmer.app/J
- r19hni9tv91d.id.wasmer.app/

### vercel.app Spanish phish
- secursalf-a.vercel.app/ (reports 486716f0, a7c8d7bf, a44eb0c0, 736217ad, f37ceddf)
- www.secursalf-a.vercel.app/ (reports e626d025, a7c8d7bf)
- https://urlquery.net/report/e626d025-86d2-4040-864e-9158085b6009

### Telegram exfil templates (bot tokens redacted)
- api.telegram.org/bot${8935051385:<REDACTED>}/ (report bfcfa709, 2026-09-01)
- https://urlquery.net/report/bfcfa709-6f66-4157-9fab-4057dad00a7b
- api.telegram.org/bot${6956871343:<REDACTED>} (report b8446c80, 2025-09-26)
- https://urlquery.net/report/b8446c80-06c0-43f0-a9eb-b3819a1084e1
- api.telegram.org/bot/sendMessage?chat_id=&text=<HOST INFO> (report 817c64b5, 2025-12-17)
- https://urlquery.net/report/817c64b5-27f8-445b-adc6-260ad42b3e9e
- api.telegram.org/bot<8569447474>:<REDACTED>/sendMessage (wordpress-c2627 kit, live)
- api.telegram.org/bot<8794627026>:<REDACTED>/sendMessage (secursalf kit, live)

### tetes-air.pages.dev Amazon lure
- tetes-air.pages.dev/dp/B0B6GK4VTC?ref=MarsFS_VICC_RINGINDC%2F
- tetes-air.pages.dev/dp/B08DJC1KMJ?ref=MarsFS_VICC_rvdpro2_faceplate
- tetes-air.pages.dev/dp/B076JKHDQT?ref=MarsFS_VICC_Ring%20Rechargeable%20Battery%20Pack
- tetes-air.pages.dev/gp/customer-reviews/r2dvcu4l2ujjbx/%3C/
- tetes-air.pages.dev/dp/B0C5QRZ47P?ref=MarsFS_VICC_STUC

### Other sendMessage content matches (unexamined)
- fluxion-shop.site.je
- quelltech.shop
- rankedsurfers.com
- chargeblast.com
- groupon.fr
- heritage.com.au
- heine.de
- binance-register.blogspot.com (profiler cluster 3)
