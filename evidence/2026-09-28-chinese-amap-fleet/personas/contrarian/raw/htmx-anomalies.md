# Contrarian anomaly hunt — htmx-anomalies.md (2026-10-04)

## Method note (read first)

- **Live htmx hunt was impossible.** At task time (2026-10-04 23:24 CDT = 2026-10-05 04:24 UTC)
  the VM had **total egress failure**: `hatch-egress-proxy:3128` accepts TCP but never answers
  CONNECT (curl exit 28, python urllib timeout) for *all* hosts including google.com and
  huggingface.co. Not a urlquery block — a VM/proxy outage. `uq_htmx.py` and curl both fail.
- **Fallback used:** the fleet's local corpus snapshot (`raw/`, `events.jsonl`, collected
  2026-10-05 ~01:15–01:35 UTC, i.e. ~3h before task time), joined to full raw records by
  report_id for submitted URL + submitter IP/ASN. Corpus covers 2026-09-28 → 2026-10-05T01:12:40Z,
  so the "last 48h" window (Oct 3–4) is covered except the final ~3h.
- **Attribution method:** every anomaly below is checked against submitter IP/ASN. The operator's
  egress set in-window: `47.246.174.187/.241/.224`, `47.246.165.44` (AS45102 Alibaba US, SG),
  `106.11.226.x`, `106.11.15.x`, `59.82.132.243`, `59.82.121.95`, `203.119.204.85/.194`,
  `182.92.x.x` (AS37963 Hangzhou Alibaba Advertising, CN), `155.102.212.x` (AS24429 Taobao, US),
  plus one DigitalOcean box (see F10).
- **Verdict up front:** no second actor found. Every anomaly attributes to the same operator
  (shared IPs, shared POI targets, same grammar family). The fleet is *experimenting*, not
  being impersonated.

Known-shape exclusions applied: `uqscan=<word><date>[a-z]` POI scans, httpbun/httpbin base64
carriers, lhr.life uqcors, is.gd, webhook.site dead-drops (the last two had **zero** hits in
the 48h window — those lanes went quiet).

---

## F1. Anti-bot telemetry research harness (MAJOR — operator experiment)

The operator is actively researching Amap's bot defenses, not just scraping POIs.

- **Payload probe** — 2026-10-04T15:19:50Z, `https://urlquery.net/report/e32e37d2-456c-4240-954b-f7e2cbb27315`
  - Submitted: `href.li/?https://httpbun.com/base64/<...>` (referrer-hiding wrapper around the carrier).
  - Decoded base64 page is a single `<script>` that: hooks `XMLHttpRequest.prototype.open`,
    loads `https://sg-wum.alibaba.com/w/wu.json?bx-ua=fast-load`, loads
    `https://g.alicdn.com/??AWSC/AWSC/awsc.js,sd/baxia-entry/baxiaCommon.js`, calls
    `baxiaCommon.init({checkApiPath: u=>u.includes('getPoiInfo'), appendTo:'querystring',
    paramsType:['uab','umid','et']})`, overrides `__baxia__.getFYModule.getUidToken`, then fires
    `GET https://amap-pc-ssr.amap.com/ssr/api/getPoiInfo?id=B001C8MXRO&p=<epoch>` at 3/7/11s and
    `navigator.sendBeacon`s status+body to `https://webhook.site/a7753b69-2ceb-4221-adfa-80f69d57480c`.
  - Read: **Baxia is Alibaba's anti-bot/fraud SDK** (bx-ua, umid/uab/et tokens). The operator is
    learning which telemetry params Amap's `getPoiInfo` requires and exfiltrating the results
    to its own dead-drop. This is counter-forensics R&D, one step past scraping.
- **Dead-drop inbox check, 6 min earlier** — 2026-10-04T15:13:31Z,
  `https://urlquery.net/report/eb4ecb55-d335-45fb-b775-6746d422c7f0`
  - Submitted: `href.li/?https://webhook.site/a7753b69-2ceb-4221-adfa-80f69d57480c?run=1791126770493`
  - Same webhook UUID as the beacon target. Read: operator verifies the inbox receives before
    deploying the beacon payload. (Dead-drop shape is known; the href.li wrap + `?run=<epoch>`
    liveness check is new.)
- **jina cache/metadata probes** — 2026-10-04 16:59–20:12Z, same href.li wrapper (5 distinct payloads):
  `target-jina-probe`, `gc-jina-meta-1791135680981`, `gc-jina-json-1791135359787`,
  `gc-cache-probe-1791134820172`, `jina-cache-1791133015584`.
  Read: operator probing jina (reader/relay) caching + metadata behavior — the jina relay stack
  is known swarm tradecraft; this is the operator calibrating it.
- **livecodes.io "Baxia" family** — 18 submissions on 2026-10-04 (Cloudflare-resolved IPs are the
  *target's*, not the submitter's — these are genuine operator submissions). Titles:
  `Baxia signed navigation`, `Baxia delayed query probe`, `Baxia query probe`, `Baxia header echo`,
  `Amap Baxia probe`, `Amap Baxia JSONP`, `Amap SSR helper`, `Amap migration helper`,
  `Amap full app iframe`, `palacelegacy1791142556`, `cookieiframe1791129466`,
  `GZHOSP-topbackend-1791106056744`, `GZHOSP-topditussr-…`, `GZHOSPbackend…`, `GZHOSPssrwww…`, `GZHOSPPLACE…`.
  - e.g. 2026-10-04T13:28:17Z `https://urlquery.net/report/2827b191-c4e0-4d39-ac99-c70bf4791a04`
  - Read: a named probe harness ("Baxia") for browser-side behaviors — cookie/iframe, delayed
    queries, header echo, signed navigation, JSONP — i.e. learning what the urlquery scanner
    (and by extension Amap's defenses) will execute. **GZHOSP\*** is a new vertical word
    (hospital — not in the known museum/scenic/food set) tested across route variants
    (topbackend/topditussr/ssrwww/PLACE).

## F2. uq\*-family marker A/B test (operator experiment)

~157 submissions on 2026-10-04 (04:00–21:00 UTC, peak 10:00–11:00 UTC) use marker params that are
**not** `uqscan=`, from the same Alibaba SG/CN IPs: `uq=`, `uqpd=`, `uqdirect=`, `uqresearch=`,
`uqtarget=`, `uqprobe=`, `uqfresh=`, `uqlegacy=`, `uqmobile=`, `uqproxy=`, `uqstack=`,
`uqstatic=`, `uqasset=`.

- `www.amap.com/place/B03DF0262E?uqresearch=1791145002` — 2026-10-04T17:40:31Z, ip 47.246.174.224
- `www.amap.com/poi_detail?id=B0FFF06JQQ&source=search&uqpd=1791128766641` — 2026-10-04T15:47:15Z
- `www.amap.com/?uqvnc=1791112173` — 2026-10-04T11:10:22Z (companion `?uqinteractive=1791112019` at 11:07:53Z)
- `amap-pc-ssr.amap.com/ssr/poi-detail?id=B02F37TV2J&uq=directhost0…5` — enumerated 0–5 across two IPs
- `ssr-next.amap.com/ssr/place/B021407PX0?uqtarget=direct-c892e6eb-04d3-4dd1-994b-a974051b052d` —
  2026-10-04T11:00:00Z, `https://urlquery.net/report/a776eb59-e570-4e78-b627-bfa06ee49509`
  (UUID as the marker value — testing whether Amap echoes/logs arbitrary marker formats)
- `?uqstack=1791135595a/b/c` triplets — 2026-10-04T17:40:36Z,
  `https://urlquery.net/report/08c6993d-4ad4-4ea4-9460-01852cac9742`
- Values alternate between bare epochs (`uq=1791089794`) and `word+date+letter`
  (`uqtarget=laoshan20261004a`, `uqtarget=mobileapi1791103668`).
- Read: systematic grammar experiment — which param names survive Amap's URL handling/redirects
  and remain visible to the scanner. Same actor (IPs match the tagged lane).

## F3. JS bundle / static-asset discovery (operator experiment — new host)

4 submissions on 2026-10-04 targeting **`ssr-next.amap.com`** (new host vs the known
amap-pc-ssr/www/m/ditu):

- `ssr-next.amap.com/static/amap-pc-ssr/production/1f3ace2b/_next/static/chunks/2789-f158aa7d925d74f6.js?uqscan=claudeprime` —
  2026-10-04T21:48:33Z, `https://urlquery.net/report/da980375-f511-4b12-bec2-51d0986b163f`
  (from 155.102.212.196, Taobao US ASN)
- `…/chunks/webpack-f64198e7ec38e832.js?uqstatic=1791129000` — 2026-10-04T15:41:48Z
- `…/chunks/webpack-f64198e7ec38e832.js?uqasset=179111` — 2026-10-04T11:25:10Z
- Read: operator mapping Amap's Next.js build output and testing whether the static CDN
  echoes query params (`uqstatic=`/`uqasset=` are new marker names in the F2 family). First
  observed non-HTML, non-API target class.

## F4. API surface enumeration incl. staging host (operator experiment)

384 `ssr/api/` hits in 48h — the operator is calling Amap's SSR JSON API directly, bypassing
rendered pages: `getPoiInfo`, `getPoiDetail`, `getDeepInfoPoi`, `poi-detail`.

- `amap-pc-ssr.amap.com/ssr/api/getPoiInfo?id=B0G3LMF2G1&user_loc=117.2494,31.814395&uqscan=targetinfo20261005c` —
  2026-10-05T00:44:29Z, `https://urlquery.net/report/b80eaded-9a06-4bca-aa3d-692fb232963a`
  (`user_loc` = 31.81N 117.24E ≈ Hefei, Anhui — spoofed geolocation param)
- `gaode.com/ssr/api/getPoiInfo?id=B03DF0262E&uqscan=xjpark1791145455` — API probed on gaode.com too
- **`pre-amap-pc-ssr.amap.com`** — 49 events, all on 2026-10-04 (e.g.
  `pre-amap-pc-ssr.amap.com/ssr/place/B03170SWDL` — 2026-10-04T20:45:56Z,
  `https://urlquery.net/report/dcfeeb74-f07b-4e4f-947f-f1f22b94a3c0`). New subdomain =
  Amap's pre-production/staging SSR host. Read: operator discovered and is diffing staging vs prod.
- Read: deliberate API-layer mapping (route names, param acceptance, staging parity) — a level
  below the POI-page scraping the fleet is known for.

## F5. Route-matrix sweep with random hex tags (operator experiment)

2026-10-04T17:19–17:23 UTC: one IP (47.246.165.44) hits **one POI (B0G1X5HFSJ)** across 9 URL
shapes with random 8-hex `uqscan=` values:

- `www.amap.com/place/B0G1X5HFSJ?uqscan=156d324b`, `ditu.amap.com/place/…?uqscan=9f36c491`,
  `www.amap.com/detail/get/detail?id=…&uqscan=a45ca478`,
  `www.amap.com/service/poiInfo?id=…&uqscan=3cbfbf35`,
  `ditu.amap.com/ssr/api/getPoiInfo?id=…&uqscan=b9a3a2ce`,
  `www.amap.com/ssr/api/getPoiInfo?id=…&uqscan=21677c51`,
  `ditu.amap.com/service/poiInfo?id=…&uqscan=683e2212`,
  `ditu.amap.com/detail/get/detail?id=…&uqscan=d6faa07d`,
  `pre-amap-pc-ssr.amap.com/ssr/place/…?uqscan=d745f12e`
  (e.g. `https://urlquery.net/report/1e703e0c-6398-49cb-b6a3-02caac40c4d6`)
- Read: cache-busting / route-equivalence fingerprinting — which URL shapes return the same POI
  data. The hex values replaced the usual word tags, i.e. the tag became a nonce.

## F6. Malformed param nesting (operator bug or injection test)

111× in 48h: the `&uqscan=` (and `&user_loc=`) got URL-encoded **inside** the `id=` value:

- `amap-pc-ssr.amap.com/ssr/api/getPoiInfo?id=B0FFGJP58W%26uqscan=research20261005api2` —
  2026-10-04T22:35:04Z
- `amap.com/ssr/api/getPoiDetail?id=B0G3LMF2G1%26uqscan=targetdetail20261005a` — 2026-10-05T00:44:09Z
- `www.amap.com/ssr/poi-detail?id=B0FFJMINT2%26uqscan=navy971-20261005a` — 2026-10-04T18:03:11Z
- Read: either a buggy URL builder double-encoding the query string, or a deliberate test of how
  Amap's API parses a poisoned `id`. Volume (111) and persistence across two days suggest a
  systematic (if broken) builder rather than a one-off typo. Worth watching whether Amap
  normalizes it.

## F7. switchVersion endpoint probing (operator experiment)

21× `www.amap.com/service/switchVersion?enable=1&src=<marker>` (+1 on gaode.com):

- `…?enable=1&src=fujianmuseum_top_20261005a&t=1791154201` — 2026-10-04T22:51:38Z
- `…?enable=1&src=uqpreseed260929a` — 2026-10-04T17:01:45Z, simultaneously on
  `gaode.com/service/switchVersion` (different IPs, same second;
  `https://urlquery.net/report/e6bdd8a3-b138-42e5-8392-c6ecc991670e`)
- `…?enable=1&src=gyshort64`, `…?src=worldpark20261004d`,
  `…?src=https%3A%2F%2Fwww.amap.com%2Fplace%2FB023E05BWU%3Fuqscan%3Dclaude20261004switch`
  (a full tagged URL nested as the src value — marker-survival test through Amap's redirect)
- Read: Amap's version-switch endpoint is being probed for `src`-param handling/echo. `uqpreseed`
  ("pre-seed", dated 260929 = 2026-09-29) and `gyshort64` are new singleton words.

## F8. New singleton tag words (operator — vocabulary expansion)

Words in the last 48h absent from the prior 353-word inventory (counts in-window):

- `navy971-20261005a/b/c` (3×) — `www.amap.com/ssr/poi-detail?id=B0FFJMINT2&source=search&uqscan=navy971-20261005b`,
  2026-10-04T18:03:26Z, `https://urlquery.net/report/62d1cdbf-ce24-4861-ab4a-a96e8601284e`.
  Odd word (military-flavored); hyphenated date grammar holds.
- `futianff09f7ffdb`, `futian5809af` — futian (= Shenzhen Futian district, new geo word) +
  hex-suffix (looks like short SHAs, not the usual date+letter).
- `fjmuseum-alt31-20261004` (1×) — variant suffix `-alt31`.
- `gucheng-ditugaode-auto-20261004g` / `gucheng-wwwgaode-auto-20261004f` / `gucheng-gaode-auto-20261004e`
  — 2026-10-04T15:25:57Z, `https://urlquery.net/report/befd2bad-b877-44e0-b3c6-5e6671c75432`:
  **self-labeling host-matrix tags** (`<word>-<host>-auto-<date><letter>`) across
  ditu.gaode/www.gaode/gaode for one POI. The tagger now documents its own sweep geometry.
- `jxmuseum-mobile-detail` (dateless), `fjmuseumgaodessr` (dateless) — dateless tags exist.
- `xjpark1791145455` (epoch, no letter), `szcecgaode20261004a`.
- `palacelegacy1791142556` (livecodes title) — cf. known `pandalegacy`; `cookieiframe1791129466`.
- Read: vocabulary still expanding; the grammar is loosening (dateless, epoch-only, hex-suffix,
  self-documenting). All from operator IPs → operator, not a new actor.

## F9. Unmarked runs + coordinate URLs (operator, not a new actor)

- 883/1904 recent events carry no `fleet_tag`. The amap.com subset (~250) is plain POI scans
  (`www/ditu/amap-pc-ssr …/place/<POIID>`) with **no marker at all** — but from the *same* IPs
  as the tagged lane (47.246.174.187: 187 untagged + 253 tagged). Read: the operator runs
  unmarked alongside marked — marker presence is per-run config, not identity.
- 6 untagged-only IPs, all low-count: Cloudflare ×3 (urlquery's own scanner egress for
  CF-fronted targets — artifact, not a submitter), `155.102.212.195/.198` (Taobao US, 1–2×),
  `59.82.132.217` (Alibaba CN, 1×). Read: noise.
- Coordinate-URL form: `www.amap.com/?p=B021307ZAY,36.658157,117.095731,山东博物馆,经十路11899号`
  (Shandong Museum, 2026-10-04T13:08:37Z) and `wb.amap.com/?p=B023B1C842,30.229155,120.228893,杭州奥体中心体育场,…`
  — 2026-10-04T12:53:15Z, `https://urlquery.net/report/53c47ae0-0fe4-4f75-a8b2-b1d0544756c8`.
  `wb.amap.com` is a new subdomain (1×). Read: operator testing the `?p=` coordinate share-link
  form alongside POI-id URLs.

## F10. DigitalOcean egress for the carrier lane (operator infra expansion)

`64.23.183.159` (AS14061 DigitalOcean, US) — 65 submissions in 48h, **all** `httpbun.com/base64/…`
carrier tests (the known carrier shape). Read: known lane, but first non-Alibaba egress seen —
the operator added a DigitalOcean box for carrier tests. Not a new actor (URL shapes identical).

## Gaps & follow-ups

1. **htmx gap:** everything after 2026-10-05T01:12:40Z (~3h) is uncovered — re-run the live
   `uq_htmx.py` queries once egress recovers: `uqscan`, `uqstatic`, `uqasset`, `uqstack`,
   `baxia`, `jina`, `pre-amap-pc-ssr.amap.com`, `ssr-next.amap.com`, `switchVersion`.
2. **Watch the F1 harness:** the Baxia/beacon experiment (webhook UUID
   `a7753b69-2ceb-4221-adfa-80f69d57480c`) may recur with new UUIDs — alert on
   `baxiaCommon` / `getUidToken` / `sg-wum.alibaba.com` strings in new submissions.
3. **F6 nesting:** check whether Amap's API actually resolves the `%26uqscan=`-inside-`id`
   form (fetch one report body) — distinguishes bug from injection test.
4. Counts are lower bounds (urlquery search is relevance-capped); all dates UTC.
5. **Do not push** — per task; file lives at
   `data/2026-09-28-chinese-amap-fleet/personas/contrarian/raw/htmx-anomalies.md`.
