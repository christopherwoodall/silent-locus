# Nonce-encoding lane — verdicts

Corpus: 5,750 deduped urlquery reports mined offline from `~/workspace/silent-locus/data`
(691 files; network egress was down for the whole run, live htmx/urlscan corroboration
is pending in the background job `nonce_liveprobe.py` → `nonce-04-live-probe.json`).
Raw: `nonce-01-local-mine.json`, `nonce-02-lead-urls.json`, `nonce-03-pair-table.json`,
`nonce-05-findings.json`. Scripts: `nonce_mine.py`, `nonce_leads.py`, `nonce_liveprobe.py`.

Known operator baseline (excluded per brief): `uqscan=<word><YYYYMMDD>[letter]>`
(378 reports, 2026-09-30..10-05, amap family) and `?x=<19-digit>`.

## NEW

### E-hyph-label — `<poi>(-<aspect>)*-<YYYYMMDD>[letter]>` — NEW
43 reports (`uqscan`) + 4 (`uqresearch`) + 2 (`uqtarget`), 2026-10-04..10-05, amap family
(www / amap-pc-ssr / m / ditu). ~1 distinct label per report = per-probe nonce.
POI-themed, Chinese tourist spots: `anhui-famous-direct-20261005b`,
`tianshanzoo-parent-www-20261005a`, `potala-direct-20261004`, `weiyang-mobileua-20261004g`,
`hzoo-mobile-20261004`, `changchun-victory-park-wwwssr-20261004`, `bailuzhou-real-20261004a`,
`gucheng-migrate-20261004c`. Same labels also ride inside JS beacon payloads
(`?q=` on httpbun.com / httpbin.ceshiren.com). Same `uqscan` channel as the known
operator, overlapping POI theme with known labels (`changchunshengli20261004d` vs
`changchun-victory-park-20261004`) — same harness, evolved grammar (mimicry not
fully excluded).

### E-word-epoch — `<aspect-word><epoch10>` / `<aspect-word><epoch13>` — NEW
70 (`uqscan`) + 8 (`uqresearch`) + 2 (`src`), 2026-10-01..10-05, amap family.
`ditu1791146593`, `backend1791159341`, `nanhaimuseum1791145000/5001` (consecutive),
`xspoidetail1791146900/6901`, `hsdirect1791136783790` (epoch13), `uqjx1791119400`.
Per-probe timestamp nonces.

### E-label-ext — `<word><YYYYMMDD><extra-word|words|digit>` — NEW
350 reports (`uqscan`/`src`/`uqresearch`), 2026-09-30..10-05 — the largest new bucket.
Grammar extensions of the known label: `claude20261005mobile2`, `research20261005pageb`,
`taiyuan20261005research`, `research20261004final`, `target20261005b`, `proper20261005`.
Note the `claude` token in labels (`claude20261005mobile1/2`, `claudeprime`).

### E-hybrid-epoch — `<word>(-<word>)*-<epoch10>[letter]` — NEW
36 reports (`uqscan`), burst 2026-10-04 04:00..15:00 UTC. `palacepre1791129000p`,
`potala-pre-1791127001`, `stadiumwwwssr1791125274c`, `target-poidetail-1791121725`.
(Naive classifiers mislabel these as base64 — they are epoch-suffixed labels.)

### E-bare-epoch10 — `<epoch10>` — NEW
~90 reports (`uqscan`, `uqresearch`, `uq`, `uqhs`, `uquvnc`, `uqinteractive`,
`uqmusuem`, `uqts`, `fresh`, `research`, `n`), 2026-06-20..10-04. Values == submission
time to the minute. Includes `n=1782077002/7001` sequential pair on
`91ef9fc4c82a1b.lhr.life`, 2026-06-21T21:28.

### E-short-hex — hex8/9/10/12/14 — NEW
~35 reports in tight bursts, 2026-09-30..10-05 (`uqscan`, `uqresearch`, `uqmobile`,
`uqstack`, `uqquery`, `uqretry`, `s`). The hex11 cluster is `<epoch10><letter>`
(`1791121257c/d/e` sequential, daily-lbs-pc.amap.com). Pure short-hex nonces
(`a45ca478`) also present.

### E-uuid — NEW
15 reports (`uqscan`), 2026-10-04 04:00..10:00, www/pre-amap-pc-ssr/map.amap.com.
`7d52beed-5ec8-4f2d-bbae-e53c79a290b6` etc.

### E-bare-epoch13 — `<epoch13>` — NEW
4 reports (`uqpd`, `uqdirect`), 2026-10-04 14:00..15:00. `1791128766641` reused across
2 reports in the same minute.

### E-epoch-ns-params — 19-digit = **epoch nanoseconds** — known encoding REFINED, new params
37 reports, single-day campaign 2026-06-21. **All sampled 19-digit values decode to
epoch-ns matching their report timestamps to the minute** (6/6 verified):
`x=1782073472114233418`→20:24:32Z, `ov=1782020817507639092`→05:46:57Z,
`retry=1782013528589229193`→03:45:28Z, `r=1782071176301141190`→19:46:16Z,
`slow=1782076054319184895`→21:07:34Z, `uqfresh=1791108055835622921`→2026-10-04T10:00:55Z.
New param names beyond `x`: `ov` (8, IDPH Tableau SQLi probes — County=`O'Brien` /
`O''Brien` / `O&#39;Brien` / `O%20Brien` quote-escape variants, one nonce each),
`retry` (3), `r` (2, webhook.site), `slow` (2, `*.lhr.life`), `uqfresh` (4, amap,
sequential nonces `...919/920/921`). Targets: pinggy tunnel `/probe.html`, IDPH
Tableau, webhook.site, lhr.life, is.gd, httpbin.org. **Linkage lead**: one nonce
encoding across IDPH + lhr.life + pinggy + webhook.site on the same day.

### E-staging — probe pages on public render surfaces — NEW harness fingerprint
~30 reports, 2026-09-30..10-05. Probe HTML staged on:
- `livecodes.io/?mode=result&html=<page>` — titles `<word><epoch10>`
  (`palacelegacy1791142556`, `cookieiframe1791129466`), `<WORD><epoch13>`
  (`GZHOSPbackend1791105292618`, `GZHOTP-topbackend-1791106056744`), and
  "Baxia … probe" / "Amap SSR helper" titles
- `httpbun.com/base64/<b64-XSS>?q=<JS beacon>` and `httpbin.ceshiren.com?q=<JS beacon>`
  — beacons carrying hyphen labels (`gucheng-minclient-httpbun-20261004v`,
  `gucheng-ceshiren-delay-20261004r`)
- `httpbin.org/base64/<b64>?u=<epoch10>` — staged pages iframing amap with `t=<epoch10>`
All probes target amap SSR/API. Distinct MO from direct uqscan submission;
possibly same provider, different agent/eval (per 2026-10-03 refined hypothesis).

## KNOWN (excluded per brief, confirmed present)
- `uqscan=<word><YYYYMMDD>[letter]>` — 378 reports, 2026-09-30..10-05.
- `?x=<19-digit>` classic form — subset of E-epoch-ns-params (now known to be epoch-ns).

## NOISE
- **E-eloqua** — Oracle Eloqua marketing automation (`elqtrackid`/`elq`/`elqak`/`sp_eh`/
  `em`/`s`/`utm_*` × hex32/hex64/hex68/uuid/base64ish), ~400 reports, informamail* /
  informamarkets.com, 2025-10..2026-08.
- **E-amap-native** — amap's own POI ids (`id`/`poiid` = `B0…` 10-char, `userrelationtoken`),
  ~200 reports.
- **E-appwrite** — Appwrite vendor URL grammar (`userId`×hex20, `secret`×hex256,
  `expire`×ISO8601 = report time + ~1h TTL), 7 reports. Vendor grammar = noise for this
  lane, BUT behavioral note for the exploit-gym lane: same `userId=6a769ace0015efdd7fac`
  forwarded with 4 different secrets to `webhook.site/c6aaa535-…` within 6 minutes
  (2026-08-08 12:24..12:30) — agent harvesting reset links to a dead-drop.
- **E-redirect-wrap** — full amap scan URLs (with uqscan labels) wrapped as `?url=` on
  httpbin.org / postman-echo.com redirect/echo endpoints, 24 reports — known-op echo.
- **E-token-misc** — email-campaign trackers (`token`=base64 JSON), 2 reports.
- **E-filterid** — `filterid`=uuid on memoryexpress.com, 3 reports — site-native.

## Open / follow-ups for coordinator
1. Live corroboration pending: background job `nonce_liveprobe.py` (session
   `proc_2284027287d2`) retries egress ~40 min, then runs htmx (`gucheng-`, `uqscan`,
   `17911`) + urlscan.io (`page.url:"uqscan"`, livecodes+amap) → `nonce-04-live-probe.json`.
2. E-epoch-ns-params is the strongest cross-incident linkage lead: same epoch-ns nonce
   on IDPH Tableau (SQLi probes), lhr.life, pinggy tunnel, webhook.site — all 2026-06-21.
3. Attribution question: hyphen/epoch grammars ride the known `uqscan` channel — same
   harness evolving, or a mimic blending in? The `claude` token in labels is new.
4. `uqscan=<uuid>` / short-hex / bare-epoch bursts are all 2026-10-04 — one campaign
   cycling nonce encodings; worth a per-hour interleave analysis against the hyphen
   campaign to confirm single-harness.
