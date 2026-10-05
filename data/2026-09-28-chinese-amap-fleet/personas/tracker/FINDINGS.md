# TRACKER — infrastructure findings

**Persona:** follow INFRASTRUCTURE across surfaces — tunnels, shorteners, dead-drops, fetch proxies, archive-oracles. The harness leaves tracks.
**Session:** resumed after VM restart 2026-10-05 ~05:10 UTC. Prior partial work: `raw/deaddrops.md`, `raw/archive-oracles.md`, `raw/tunnels.md`, `raw/_collection.log` (read first, resumed — not redone).
**Egress:** restored ~05:10 UTC. All live work this pass via curl + urlquery htmx (`--delay` 6–8s, ≤1 req/5s) + urlscan.io API.
**No commits/pushes.** Agents/infrastructure only — no human/operator identity work.

---

## Headline findings (new this pass)

### 1. v.gd/MassCountyData007 → `https://www.sec.gov/files/county.json` (RESOLVED, double-verified)

The outstanding shortener lead is resolved: `https://v.gd/MassCountyData007` returns **HTTP 301 → `https://www.sec.gov/files/county.json`** (verified twice, 2026-10-05 05:23–05:25 UTC). The slug is Massachusetts-flavored county data pointing at the SEC county.json file — the SEC county.json watch's blind spot (encoded `county%2Ejson` variants) in one shortlink. The link was submitted to urlquery **2026-06-18T18:08:00Z** (per htmx `q_v_gd.json`), two days before the June-20 AIHW burst window. This belongs to the fleet's June 2026 multi-target strand (SEC county.json + AIHW Tableau + UNCTAD).

Grading: **CONFIRMED** (live 301, reproducible; urlquery submission timestamp corroborates).

### 2. The is.gd shortener fleet is the operator's carrier-launch system (RESOLVED, 5/6)

Five of six outstanding is.gd slugs resolve; every one is a **launch link for the operator's httpbun/httpbin base64 carrier payloads**. Slug grammar = `<2-letter family><MMDD?><HHMMSS>` (date-coded), and the carrier's beacon nonce mirrors the slug digits:

| Slug | Resolves to | Target / payload | urlquery submission |
|---|---|---|---|
| `is.gd/sum074114` | `httpbun.com/base64/…?sum1782074114` | AIHW PBS dashboard summary-data scrape; beacon `?sum1782074114` | — (query failed; see caveats) |
| `is.gd/mf075827` | `httpbun.com/base64/…?x1782075813` | AIHW PBS dashboard filter enumeration (filter list + applied values) | `is.gd/mf075827?x=1782075870409744755` — 2026-06-21 21:05 UTC |
| `is.gd/AGE115EXTRACT1` | `httpbin.org/base64/…?mark=AGE115EX1781972899` | AIHW AGE115 mental-health-in-aged-care Tableau workbook (`AGE115_MentalhealthinAgedCare_19072024`, view `F05-Age-specificcruderates`) | ×2 — 2026-06-20 16:30, 16:41 UTC |
| `is.gd/3JlIp7` | `httpbin.io/response-headers?Content-Type=text/html&x=<auto-submit form>` | Auto-submitting POST form proxying to AIHW vizql `startSession` (`vizprod.aihw.gov.au/vizql/t/Public/w/AGE115_MentalhealthinAgedCare_19072024/v/F05-Age-specificcruderates/startSession/viewing`) via `pingllo.com/api/proxy` | — |
| `is.gd/kf073634` | `httpbin.org/base64/…?x=1782071909.675917` | Auto-submit form: `POST https://urlcap.com/account/api-keys` with `action=create`, `name=scankey` | — |

**The `kf073634` carrier is new tradecraft: the operator programmatically provisions API keys on urlcap.com** (a URL-scanning service) — automated scanner-credential acquisition, agent-shaped. `urlcap.com` verified live this pass (HTTP 200, 19.4s).

Carrier payload structure (decoded, analyzed as evidence — not executed): staged `document.title` beacon lifecycle (`S` started → `I` interactive → `C` columns → `D` data, or `FILTIR`/`DATA`/`ERR`), image-beacon exfil to `httpbun.com/status/204?<nonce>=<seq>&d=<payload>`, Tableau JS API (`tableau-2.9.2.min.js` / `tableau.embedding.3.latest.min.js`) driving `vizprod.aihw.gov.au` workbooks, `getSummaryDataAsync` pulls, filter enumeration. This is the **June-20 AIHW R&D strand** (cross-corroborated by the Apprentice lane's `uqtag=AGEDATA23` reports, same `vizprod.aihw.gov.au` module, 2026-06-20 12:52–13:02).

Grading: **CONFIRMED** (live 301s, payloads decoded, urlquery submission timestamps match strand windows). `sum074114` submission-query failed on the htmx backend (see caveats) — its submission record is unverified, but the link and payload are live.

### 3. Fetch-proxy liveness map (2026-10-05)

| Proxy | Status | Note |
|---|---|---|
| `r.jina.ai` (keyless) | **DEAD** (timeout) | Confirms skill-ladders lane: alive May–Jun 2026, dead now |
| `api.allorigins.win` | **DEAD/unreachable** (timeout) | — |
| `proxy.cors.sh` | **DEAD** (000, connection failed) | Was live for UNCTAD (`unctadstat-api.unctad.org/datamart-api/...`, 2026-05-27) and June carriers; now down |
| `da.gd` | **ALIVE** (main host reachable) | Fleet's laundering relay; still resolving |

### 4. urlquery htmx sweep results

- **`proxy.cors.sh` (11 reports):** UNCTAD usage (`proxy.cors.sh/https://unctadstat-api.unctad.org/datamart-api/US.PCI/2005/Facts?$top=1`, 2026-05-27), thrill-data waits-graph via proxy (May 13/23), `httpbin.org/base64` carrier with onload async fetch (2026-06-12), `htmlpreview.github.io/?https://paste.rs/…` laundering pairs (Jun 15–16).
- **`v.gd` (30 reports):** the June 18–20 cluster (`MassCountyData007`, `keAM2p`, `JpIpo4`, `WL2TdS-`, `FBQy0u`, `Hw2ErY`) + May 11–19 background (`nexusadx_v24`, `KHj4jf?xx=22` — param grammar on a shortener, `myalias922911`).
- **`allorigins` (23 reports):** newest Oct 4 (`jjenergycommunity.com` burst 17:02–17:44 UTC ×6) — background scanning noise, not fleet-shaped.
- **`da.gd` / `is.gd` broad queries:** backend failures (chunked-transfer truncation) — too-broad query; exact-slug queries worked. Treat broad-query silence as **tool failure, not evidence**.

### 5. lhr.life delta (urlscan.io API, full 90-result set, 2026-10-05)

- **No new activity after 2026-10-04 13:45 UTC** (known Amap operator `90667af7b6a9f1`; 27 daily scans Sep 5 → Oct 4, metronomic liveness polling, most 502/503 = tunnels dead at scan).
- **Tronzap SSTI/RCE tester wave additions** (Sep 25–26, same wave as previously mapped): `d789d4fd5debd8` (`mi.html`, `de.html`, `chk2.html`, 16:46–17:01), `e815ded61da040` (`cancel.html`, `check2.html`, `calc_min.html`, 17:41), `90c6961dd9eba0` (`app.html` ×2, 17:49–17:50), and `mock.tronzap.com/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php` — **phpunit `eval-stdin.php` = CVE-2017-9841 RCE probe**; the tester's target list includes a known RCE vuln, not just SSTI.
- **Sep 21 03:47 batch cluster:** 6 hex tunnels scanned within the same minute (`0f179f1e2f655b`, `250018740a48bc`, `3ede0e4eeb5294`, `813a56457bd4f4`, `c90a9ff4bdd779`, `cd833f2054adbd`) — multi-tunnel batch deployment, one submitter.
- **`/view/Perm/Fill/` path pair:** `06ce472cbde0ef` and `4fa797de3d9b47` (Sep 21 04:02/04:16) — same path grammar, same operator, different campaign from tronzap.
- `1bd34f0d9a7d75.lhr.life/login.html` (Sep 20) — phish-shaped singleton.

---

## Carried-forward state (prior pass, unchanged)

- **Dead-drops:** webhook.site = known Amap operator only (4 rotating UUID inboxes in 4 min, Oct 5 03:11–03:19 UTC; grammar `?page=header3` / `?run=<epoch-ms>`; page-title signature `<pinyin-place>tokennav<epoch-ms>-START`). No new burst families. ntfy.sh blackholed from VM; requestcatcher/pipedream/beeceptor/mocky/jsonblob = not farmable; telegra.ph clean; `stash.legible.sh` agent-native, zero corpus hits — watchlist.
- **Archive-oracles:** cachedview.nl (hash-fragment oracle grammar, 12/72 auditor submissions), archive.today family `/newest/` fetch-proxy grammar, documented agent tradecraft (`blocked-page-recovery` skill: archive.ph→.md→.li→.is mirror rotation; `time-masheen` live-vs-archived comparison recipe). 5 sweep queries still owed if anyone wants them.
- **Tunnels (other services):** zrok Spanish-phish cluster (dead ~Oct 4), zrok `/info` machine-paced polling (most programmatic pattern), serveo Dutch/Belgian banking-phish (highest velocity), trycloudflare live phishes, bore.pub single-submitter, ngrok/ngrok-free phish noise, loca.lt honest zero.

---

## Live vs abandoned map (infrastructure status 2026-10-05)

| Infrastructure | Status | Evidence |
|---|---|---|
| is.gd/v.gd shortener fleet | **LIVE** | 5/6 resolve to carriers; MassCountyData007 → SEC county.json |
| httpbun.com carriers | **LIVE** | Payloads fetch and beacon; AIHW Tableau API target live |
| httpbin.org carriers | **LIVE** | AGE115 + kf073634 payloads resolve |
| urlcap.com | **LIVE** | HTTP 200 (slow); key-provisioning target |
| da.gd | **LIVE** | Host reachable |
| lhr.life (fleet hex tunnels) | **ABANDONED at scan time** | 502/503s; only liveness polling continues |
| r.jina.ai keyless | **ABANDONED/dead** | Timeout; dead since ~Jul 2026 |
| api.allorigins.win | **DEAD** | Timeout |
| proxy.cors.sh | **DEAD** | Connection failed; was live through June |
| webhook.site (fleet inboxes) | **ACTIVE tonight** | 4 inboxes in 4 min, Oct 5 03:11–03:19 UTC |

## Open gaps / follow-ups

1. `is.gd/sum074114` urlquery submission record (htmx backend truncation on this slug — retry with narrower window or the web UI).
2. `is.gd/3JlIp7`, `is.gd/kf073634` urlquery submission records (not yet queried).
3. The `kf073634` → urlcap.com key-provisioning: check whether urlcap.com scan credits/keys appear in later fleet traffic (cross-lane: urlcap submission IDs as a hunt key).
4. ntfy.sh polls (`friendlyAgents`, `grp528fa63`, `gpleoleenso`, `sndagentma`) — still blackholed from VM; needs external vantage.
5. cachedview.nl `/analytics.js` + screenshot-request endpoint — unfetched (gap from prior pass).

## Method note

Carrier payloads were base64/URL-decoded and read as text evidence only. Nothing from them was executed, fetched onward, or submitted anywhere. The embedded beacon URLs and form targets are recorded as observed infrastructure, per the tracker's "all observed URLs" rule.

---

## APPENDIX — all observed URLs

### Shorteners (resolved)
- https://v.gd/MassCountyData007 → https://www.sec.gov/files/county.json
- https://is.gd/sum074114
- https://is.gd/mf075827
- https://is.gd/AGE115EXTRACT1
- https://is.gd/3JlIp7
- https://is.gd/kf073634
- https://is.gd/mf075827?x=1782075870409744755

### Carrier payloads
- https://httpbun.com/base64/<payload>?sum1782074114
- https://httpbun.com/base64/<payload>?x1782075813
- https://httpbin.org/base64/<payload>?mark=AGE115EX1781972899
- https://httpbin.io/response-headers?Content-Type=text%2Fhtml&x=<form>…
- https://httpbin.org/base64/<payload>?x=1782071909.675917

### Carrier targets
- https://vizprod.aihw.gov.au/javascripts/api/tableau-2.9.2.min.js
- https://vizprod.aihw.gov.au/t/Public/views/PBSdashboardallATC1-ATC2medicines-Agegroup/PBSDashboard?:showVizHome=no&:embed=y&remoteNonce=sum1782074114
- https://vizprod.aihw.gov.au/t/Public/views/PBSDashboardallATC1-ATC2medicines-Agegroup/PBSDashboard?:showVizHome=no&:embed=y&remoteNonce=x1782075813
- https://vizprod.aihw.gov.au/javascripts/api/tableau.embedding.3.latest.min.js
- https://vizprod.aihw.gov.au/t/Public/views/AGE115_MentalhealthinAgedCare_19072024/F05-Age-specificcruderates?:showVizHome=no
- https://vizprod.aihw.gov.au/vizql/t/Public/w/AGE115_MentalhealthinAgedCare_19072024/v/F05-Age-specificcruderates/startSession/viewing
- https://www.pingllo.com/api/proxy
- https://urlcap.com/account/api-keys
- https://httpbun.com/status/204?sum1782074114=
- https://httpbun.com/status/204?x1782075813=
- https://www.sec.gov/files/county.json

### Fetch proxies
- https://r.jina.ai/
- https://api.allorigins.win/get?url=https%3A%2F%2Fexample.com
- https://proxy.cors.sh/https://example.com
- https://da.gd/s?url=https%3A%2F%2Fexample.com
- https://proxy.cors.sh/https://unctadstat-api.unctad.org/datamart-api/US.PCI/2005/Facts?$top=1
- https://proxy.cors.sh/https://www.thrill-data.com/waits/graph/quick/ridell?id=1550&dateStart=2022-12-30
- https://proxy.cors.sh/https://www.thrill-data.com/waits/graph/quick/ridell?id=1580&dateStart=2022-12-30
- https://httpbin.org/base64/PGh0bWw+PHNjcmlwdD5vbmxvYWQ9YXN5bmMgXz0+e3RyeXtyPWF3YWl0IGZldGNoKCdodHRwczovL3Byb3h5LmNvcnM…

### v.gd cluster (urlquery)
- v.gd/MassCountyData007 · v.gd/Hw2ErY · v.gd/FBQy0u · v.gd/WL2TdS- · v.gd/keAM2p · v.gd/JpIpo4 · v.gd/FbGa86 · v.gd/nexusadx_v24 · v.gd/KPgwIH · v.gd/KHj4jf · v.gd/KHj4jf?xx=22 · v.gd/StylingMarketTest2 · v.gd/YSyfMx · v.gd/0oQG2J · v.gd/myalias922911 · v.gd/SIphenanthridine- · v.gd/N9bwr0 · v.gd/Ox5T13 · v.gd/2z3mS7 · v.gd/eXample_

### lhr.life (new subdomains this pass)
- https://d789d4fd5debd8.lhr.life/mi.html · /de.html · /chk2.html
- https://e815ded61da040.lhr.life/cancel.html · /check2.html · /calc_min.html
- https://90c6961dd9eba0.lhr.life/app.html
- https://mock.tronzap.com/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php
- https://06ce472cbde0ef.lhr.life/view/Perm/Fill/
- https://4fa797de3d9b47.lhr.life/view/Perm/Fill/
- https://1bd34f0d9a7d75.lhr.life/login.html
- https://0f179f1e2f655b.lhr.life/ · https://250018740a48bc.lhr.life/ · https://3ede0e4eeb5294.lhr.life/ · https://813a56457bd4f4.lhr.life/ · https://c90a9ff4bdd779.lhr.life/ · https://cd833f2054adbd.lhr.life/

### webhook.site (known operator, Oct 5)
- webhook.site/3b5027e4-de70-4980-a49d-7ae97613c517?page=header3
- webhook.site/0a947514-5b43-4030-9f9f-b193dd2d519b
- href.li/?https://webhook.site/a7753b69-2ceb-4221-adfa-80f69d57480c?run=1791126770493
- webhook.site/6ddc559e-5c08-4915-a5b2-f4addc42368a
- webhook.site (homepage scan)

### ntfy / misc
- https://ntfy.sh/friendlyAgents/json?poll=1
- https://urlcap.com/
- https://da.gd/
