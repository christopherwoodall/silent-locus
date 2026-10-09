# BURST-PROFILER — urlquery.net submitter burst profiling (non-Amap fleets)

Date: 2026-10-05. Analyst: BURST-PROFILER subagent.
Method: (1) live htmx crawl of `date:[2026-10-01 TO 2026-10-05]` → 480 rows,
435 unique reports, covering 2026-10-05 04:57–05:32 UTC (urlquery volume is
~14 reports/min, so 435 rows ≈ 35 min of feed); (2) tight time-window
clustering (5-min buckets + exact-duplicate-URL analysis); (3) runtime-side
searches for grammar context. Each tight cluster ≈ one submitter's run.
Amap-operator grammar (`uqscan=`/`uqtag=`/`uqvnc=`, amap.com, localhost.run,
idph.iowa.gov, aihw.gov.au) EXCLUDED — 0 hits in all 435 rows (fleet quiet in
this window).

## INFRA NOTE
VM egress to urlquery.net died ~04:30 UTC (proxy CONNECT timeouts; not a client
bug — curl, urllib, htmx CLI all failed identically). Parent-directed 20-min
backoff; egress recovered ~05:31 UTC and the crawl ran clean with 4s
politeness delays. One browser_open on a urlquery search page timed out at
821s earlier — no further search-page fetches via that path per directive.

---

## TOP 10 AGENT-SHAPED NON-AMAP CLUSTERS

### 1. "jmail cache-proxy reader" — STRONGEST behavioral tell
13 reports, 2026-10-05 04:57–05:32 UTC, roughly one every 2–3 min (metronomic).
A single submitter reading jmail.world (document-archive threads: EFTA PDF
volumes, person pages) *through text/cache proxies* instead of directly:
- 05:32 `cachedview.nl/#https://jmail.world/thread/vol00011-efta02410253-pdf?q=...` [5911fe5a-b84a-44ba-869d-28fe0a6c3930]
- 05:29 `jmail.world/thread/vol00009-efta01009328-pdf?q=seekers+of+decay` [79054fcc-cf2b-4aa2-be6c-9a5b60620e69]
- 05:26 `jmail.world/thread/3361046c8b4c4aa48f52a7073af7a546?q=https%3A%2F%2F2pink.org%2Fdang-` [30285984-eed4-4ec4-86db-e44d5ca13e29]
- 05:23 `jmail.world/drive/vol00011-efta02421526-pdf?q=http%3A%2F%2Ffolllike.com%2F%3F19384926` [3977ad09-722e-4a5e-86d8-4bd671bf2a11]
- 05:21 `jmail.world/thread/EFTA02214132?q=https%3A%2F%2Fwww.followlike.info%2F%3Fr%3D19384926` [50384673-c82a-45ec-968e-a2a71e7d0918]
- 05:18 `jmail.world/person/david-stern?q=seekers+of+decay` [5632b5be-2b50-4aae-a2be-c5984d4a6389]
- 05:15 `jmail.world/photos?q=http%3A%2F%2Ffolllike.com%2F%3F19384926` [8dd8c2d1-97c7-482d-8e4b-ef3b81098a7a]
- 05:12 `jmail.world/person/darren-indyke-nameonly?q=seekers+of+decay` [e36e6d36-db70-4faa-886f-f6593b58d7aa]
- 05:05 `jmail.world/thread/EFTA02534854?q=https%3A%2F%2F2pink.org%2Fdang-ky%3Fref%3D119334` [eed9ba2a-0556-42f7-9b3f-7e06e2e0...]
- 05:02 `jmail.world/thread/EFTA02032048?q=seekers+of+decay` [4a20d24d-...]
- 04:59 `archive.wikiwix.com/cache/?url=https%3A%2F%2Fjmail.world%2Fthread%2F5520d954efaa18282` [be3950a9-...]
- 04:57 `cachedview.nl/#https://jmail.world/thread/vol00009-efta00160217-pdf?q=...` [193a1bc5-...]
Template: `{thread,drive,photos,person}/<id>{-pdf,}?q=<referral/search>` read via
cachedview.nl / wikiwix cache proxy. Domain diversity: 1 (+2 proxy hosts).
Cadence: metronomic ~2–3 min spacing over 35 min — a reader working a list.
Agent-shaped: HIGH — cache-proxy reading is documented agent tradecraft for
accessing pages indirectly; the steady cadence and thread-walking grammar fit
an automated research agent, not a human clicking.

### 2. "appwrite hex-subdomain enumeration"
8 sequential hex-prefixed deployments + 8 named ones, 2026-10-05 05:02–05:30.
Hex prefixes INCREASE monotonically with time — a namespace walk:
- 05:30 `6ac3354da2c8ccf4913e.appwrite.network` [28f734b6-c237-40e9-b8c2-ab9fb5d504f8]
- 05:28 `6ac3351848798e78adb7.appwrite.network` [6100c01c-beae-4f0b-af88-868648ce7132]
- 05:22 `6ac333afdda0973d4ad5.appwrite.network` [ae6a9daa-5afa-46c3-bc2e-6aed56876321]
- 05:17 `6ac3323200137dee90fb.appwrite.network` [c1333458-895f-4b43-9fea-f155b0a777fb]
- 05:12 `6ac331492f917f5fdb4e.appwrite.network` [df5a4bc3-4f3c-4ac0-a66b-459c8a7e1aff]
- 05:11 `6ac330706b374e700ce2.appwrite.network` [800c3712-14c9-4dab-a7b9-bda23dbddd88]
- 05:07 `6ac33021ce20e8a00ffd.appwrite.network` [f0e2d404-bd1a-4751-81a9-9b6bcf3ccabd]
Plus named: lender-hub ×2, estudaki-front ×2, possum, rebrief-app-staging,
studious, jingshi, emmath, vb-qc-me7p, vb-qc, branch-main-74ed670,
branch-main-13895dc, 6abe16750004c42bbe95.
Cadence: bursty-sequential, ~2–4 min steps. Agent-shaped: HIGH — Appwrite was
the harness platform in the July ExploitGym incident traffic; walking
sequential deployment IDs smells like agent recon on a deployment fleet
(or a dev QA-ing their own fleet — same automation signature).

### 3. "xsph.ru DCRat-infra sweeper"
≥7 reports in single minutes, campaign spanning 01:42→05:04+ UTC (≥3.5h):
`[a-f0-9]{7}.xsph.ru/` + `www.` variants → 141.8.197.42, #35278 Sprinthost.ru (RU):
- 05:04 `a1069693.xsph.ru/` [3ff6adbb-a9c0-40b0-a0ca-ebfe4303b2e0]
- 05:04 `www.a1064909.xsph.ru/`, `www.f0368664.xsph.ru/`, `f0391281.xsph.ru/`, `a0315266.xsph.ru/`, `a0981582.xsph.ru/`
- 01:42 (search-crawl snapshot) `www.f0314815.xsph.ru/`
Historical: same grammar active since Sep 2024 (f1083221 2025-02-21, a1078682
2025-02-15, f1032430 2024-11-07, a0868669 2024-09-05); ThreatFox flags several
as **DCRat** (DarkCrystal RAT) C2. Cadence: metronomic minute-bursts.
Agent-shaped: HIGH — systematic subdomain enumeration of hostile infra,
either a threat-intel pipeline or agent recon.

### 4. "roblox.com.mu phish-kit sweep"
7 reports, 2026-10-05 04:58–05:18, all → 5.175.169.201, #219067 Chiara Conti:
- 05:18 `/users/886042701/profile` [ab50875a-a457-4493-986f-b0dc07c8d17b]
- 05:04 `/communities/276117964/Shy-Clothing` [ddbf8ef2-3193-4bc4-9d8b-d5809a4376aa]
- 05:03 `/users/5538761166/profile` [0c58c726-7c51-48c8-b835-146a738cf1a1]
- 05:03 `/games/920587237/Adopt-Me?privateServerLinkCode=72483366404311896872` [815a39d7-b4b3-4ddc-9127-d95f655ef229]
- 05:02 `/users/1459298645/profile` [4b1f3530-aaa1-47ac-8e1a-f9e79cef8328]
- 05:01 `/users/580065616/profile/` [286665e4-c2c0-4ce1-b9e8-422604b71466]
- 04:58 `/games/109983668079237/Steal-a-Brainrot?privateServerLinkCode=062339` [138c7dd3-7749-40e8-a64f-2f560a7f60d5]
Template: fake-Roblox domain (Mauritius TLD), profile IDs + game pages with
privateServerLinkCode. Cadence: steady ~2–3 min. Agent-shaped: MODERATE-HIGH —
one submitter sweeping every page of a phishing kit.

### 5. "wpp.lol fast-flux rescan pairs" (2026-09-23)
6 reports over ~3h in 3 tight pairs, all #63949 Akamai Connected Cloud —
same URL resubmitted 2 min apart resolving to DIFFERENT IPs:
- 11:29/11:27 `tbs-sct.wpp.lol/` → 172.234.27.224 / 172.237.159.210
- 08:36/08:34 `sheepmilk789.wpp.lol/` → 172.239.193.217 / 172.237.159.210
- plus 11:01 `tkelvator.com`, 09:59 `kr.av4.space/v/s://motherless.com/AB1D4BB`
(from related-reports on https://urlquery.net/report/dd96f06e-e85e-49cf-b90e-b7efe705fc62).
Agent-shaped: HIGH — rescan-same-URL-different-IP is automated DNS-agility
verification; humans submit once.

### 6. "urldance/sqllq redirector walker"
2026-10-05 04:31, same minute: `202608.urldance.com/7d/` → 156.225.108.43 and
`202608.urldance.com/8d/` → 156.225.108.42 (Edgenext Legend Dynasty, HK).
Backend: date-keyed `YYYY-MM-DD.{urldance,sqllq}.com` subdomains (reg.
2024-03-28/2024-04-07), SINKHOLED by DigiCert UltraDNS + DNS4EU ("malicious"),
stack = hm.baidu.com + 51.la analytics + OpenResty (Chinese malvertising TDS);
submitted template `YYYY-MM-DD.sqllq.com/en/?<random-domain>`.
Agent-shaped: MODERATE-HIGH — sequential `/7d/`→`/8d/` namespace walking of a
sinkholed TDS; operator QA or enumerator.

### 7. "wicametit Azure blob walker"
4 reports, 2026-10-05 05:18–05:31: `wicametit.z20.web.core.windows.net/qom8ltsd2d/aspic/<word-salad>/<file>`:
- 05:31 `.../aspic/aged/adult.css` [b5b69c45-98b2-44be-9a02-d62040626a11]
- 05:28 `.../aspic/alcoholkoliziing/appanage.js` [9d01a6f5-5dac-4786-b90b-ddab3487af0b]
- 05:20 `.../aspic/aghast/adherent.webp` [4b0d9ba6-e3a9-4971-843a-eff879e27fe0]
- 05:18 `.../aspic/alcoholkoliziing/defalcation.webp` [c8dddb4c-45c5-4838-9588-99cde8a5f454]
Dictionary-word path salad, different file each time — walking a storage
container. Agent-shaped: MODERATE.

### 8. "workers.dev phish-farm harvester"
≥14 reports in 3 minute-bursts over ~35 min (04:31, 05:03–05:04):
`tg.985.workers.dev/`, `www.v3.quiet-disk-62f9.hrmcxaeel.workers.dev/`,
`winter-waterfall-0606.rihaniomar21.workers.dev/`,
`www.serve1.darix168035584.workers.dev/`, `z10.info-alishafagh.workers.dev/`,
`worker-calm-mountain-c6f5.akermankowalczykz-iu-c-p-2-4-0-8.workers.dev/`,
`office21174302441641798141027.secureprovide.workers.dev/`,
`sell.iv2ray1.workers.dev/`, `www.agh-edu-pl.heidrun-smailus.workers.dev/`,
`www.little-cake-cc85.gakofo25091405.workers.dev/`,
`www.beta-0-2237.desktopapluscom.workers.dev/`, `update.windows10-fd9.workers.dev/`,
`www.square-cell-3082.charles-ourtime.workers.dev/`,
`www.beta-0-110.armyplus-desktop.workers.dev/` — random-word Cloudflare
Workers phishing. Cadence: bursty (feed-driven). Agent-shaped: MODERATE-HIGH
(machine pipeline; could be vendor feed).

### 9. "get-monai.app watcher"
6 identical submissions of `www.get-monai.app` across 05:10–05:25
([a88627f8-...], [2c59d4fa-...], [f400c345-...], [41235561-...], [a6303402-...]).
Same-URL rescans every few minutes = monitoring loop or broken dedup.
Agent-shaped: MODERATE.

### 10. "ddnsgeek dyndns pair" + malware-feed strays
04:31 same minute: `jehalisipo.ddnsgeek.com/uwojad/` (107.172.151.86, HostPapa)
and `dudamu.ddnsgeek.com/jipoco/` (192.227.152.168, HostPapa, UQ 2) —
random-subdomain dyndns + random 6-char paths, classic malware/phish staging.
Plus 01:42 batch: `aksiyononline.best/masabikk4/secured_stub.ps1`,
`180.245.42.218:56938/bin.sh` (Mirai-style), `nodewatt.org/downloads/`.
Agent-shaped: MODERATE (dyndns pair) / LOW-MODERATE (commodity feed).

## NEGATIVES
- Amap-operator grammar: 0/435. `site:urlquery.net "uqscan="` → no index hits.
- Tunnel services (trycloudflare/bore.pub/pinggy): no index hits.
- `pandalegacy` marker: no index hits.

## FOLLOW-UPS
1. `url.domain:xsph.ru` full enumeration — run size, inter-arrival distribution.
2. `url.domain:appwrite.network` — is the hex-walk ongoing? Cross-ref July
   ExploitGym Appwrite artifacts.
3. jmail.world reader — identify submitter UA via authenticated API when
   unthrottled (degenerate UA = agent confirmation); check whether the
   EFTA-thread walk continues and what `?q=` values encode.
4. wpp.lol / roblox.com.mu — same-submitter linkage via report "Related reports".
5. Raw crawl: /tmp/uq_oct1_5.json (480 rows; /tmp is ephemeral — recrawl if needed).
