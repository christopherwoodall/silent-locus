# TARGET-CLASS HUNT — redirector farms + scam infrastructure (raw notes)
**Date**: 2026-10-04/05 (all times UTC unless noted; CDT = UTC-5)
**Operator**: subagent sweep. Method note: VM egress proxy was DOWN for the entire session (all HTTPS via hatch-egress-proxy:3128 timed out; google.com, urlquery.net, urlscan.io all 000). The planned `uq_htmx.py` sweep (`redirector_sweep.py`, 15 queries, same dir) could NOT run. Data came from: (a) `browser.open` on the urlquery.net homepage firehose table (3 distinct live samples), (b) `browser.open` on the urlscan.io search API (unauthenticated; worked for `domain:` queries, 403 on wildcard queries — key required), (c) offline mining of `new-fleets/raw/window1.json` (123 reports, 2026-10-05 03:00–03:58 UTC) and `new-fleets/raw/jmail_world.json` (72 reports).

## Queries / data pulls run
| # | Source | Query | Result |
|---|--------|-------|--------|
| 1 | uq_htmx.py | `search --query cachedview.nl --limit 3` | FAILED — proxy tunnel TimeoutError (egress down) |
| 2 | curl | `https://urlquery.net/`, `/api/htmx/search/?q=jmail.world`, google.com, urlscan.io, example.com | ALL timed out (000) — total egress outage |
| 3 | browser.open | urlquery.net homepage (firehose table) | OK ×4 (3 distinct samples: 04:31, 04:32, 05:03–05:04 UTC) |
| 4 | browser.open | urlscan.io/api/v1/search/?q=domain:jmail.world&size=10 | OK — 10 results, 9 auditor scans + 1 jmail.best |
| 5 | browser.open | urlscan `q=page.url:*refer=119334*` | 403 (wildcards need API key) |
| 6 | browser.open | urlscan `q=page.url:119334` | OK — 0 results (tokenization; query-param values not matched) |
| 7 | browser.open | urlscan `q=page.url:followlike` | OK — 0 results |
| 8 | browser.open | urlscan `q=followlike` | FAILED — browser-service timeout (821s) |
| 9 | browser.open | urlscan `q=seekers` | FAILED — browser service draining |
| 10 | offline | window1.json host clustering | OK — see clusters below |
| 11 | offline | jmail_world.json gap analysis | OK — median 3.0 min, 33/71 gaps exactly 3 min |

## KNOWN cluster extension — jmail.world auditor (report as RELATED, not new)
- **Cross-platform confirmed**: the same auditor submits to BOTH urlquery.net and urlscan.io.
  - urlquery: 72 reports, 2026-10-04 23:54 → 2026-10-05 03:58 UTC, median gap 3.0 min (metronomic).
  - urlscan: 9 scans sampled, 2026-10-03 20:49:03Z → 2026-10-04 20:49:37Z (~24h span), `task.method=api`, `visibility=public`, anonymous submitter. URLs carry identical probe payloads: `?q=http(s)://www.followlike.net/?r=19384926`, `?q=https://livetraffic.net/login?refer=119334`, `?q=https://2pink.org/dang-ky?ref=119334`, `?q=https://www.followlike.info/?r=19384926`, `?q=http://folllike.com/?19384926`.
  - urlscan UUIDs: `01a108ad-d176-747e-a0b7-1a880e39fc26` (promotions/page/4, folllike), `01a10716-c434-7367-b021-e925a15ca683` (promotions/page/59, livetraffic), `01a106a0-6bc9-715b-bc84-db57979675ee` (thread/36bed70a…, livetraffic), `01a1063b-5856-72cb-8793-b47208b99160` (thread/a5eb8f86…, followlike.info), `01a1058e-1b68-74bd-ae48-585fd0bbcbc7` (thread/43959a42…, folllike), `01a10562-8363-73ca-92d-8b748871da73` (thread/b68518857…, 2pink), `01a104f5-2f0b-7443-9a9f-4b4cdba954d3` (thread/29b5aca91…, followlike.net), `01a104ce-d65d-760d-9ba4-0123fcb8c35a` (thread/6ba5fd519…, followlike.net), `01a10386-ec36-7284-9a74-f14288370e61` (thread/15842997…, followlike.info).
- **Archive-oracle use extends beyond jmail**: window1.json has 2 more cachedview.nl submissions — `cachedview.nl/#pinterest.mx/seekersofdecay/regan-vest/` (2026-10-05 03:41) and `cachedview.nl/#pinterest.vn/search/videos?q=Regelbau&rs=content_type_filter` (03:24). The auditor checks cached/indexed versions of Pinterest pages too; the watch-phrase `seekersofdecay` appears as a Pinterest slug.
- **Sibling farm domain**: urlscan result `01a100f7-aeab-7759-96ae-718f2df64439` — `https://www.jmail.best/` scanned 2026-10-03 08:53Z, tagged `hybridanalysis` (different submitter). jmail.best = same farm family, different TLD.
- **Interpretation**: one programmatic auditor runs multi-day metronomic audits (jmail.world namespace walk + `?q=` probes with 5 known phishing-kit affiliate URLs + watch-phrase `seekers of decay`), cross-checking live vs cached via cachedview.nl, on both urlquery and urlscan. NOT the Amap operator (no uq grammar). Agent-vs-script open; timing is machine-shaped.
- Context: straja.io flags jmail.world trust score 1/10 ("impersonate a legitimate brand", "reported for malicious activity"). jmail.world titles: "Jmail — Epstein Emails".

## NEW CANDIDATE 1 — xsph.ru bulk-created phishing farm (strong)
- **7 hex-prefix subdomains, all 141.8.197.42 (AS35278 Sprinthost.ru LLC)**, submitted 2026-10-05 04:31 → 05:04 UTC (~33 min, ≈1 per 4–5 min):
  - `f0575425.xsph.ru/`, `f0536218.xsph.ru/` (04:32); `a0655455.xsph.ru/`, `www.a0355853.xsph.ru/` (04:31)
  - `a1069693.xsph.ru/`, `www.a1064909.xsph.ru/`, `www.f0368664.xsph.ru/` (05:04)
- **Creation grammar**: shared 3-char prefixes — `a106`×2 (a1069693/a1064909), `a0`×2 (a0655455/a0355853), `f05`×2 (f0575425/f0536218), `f03`×1 (f0368664) + 8-hex suffix. Bulk-generated, sequentially related batches.
- TDS detections 1–4 on each (urlquery threat detections flagging). This is bulk-created phishing being swept host-by-host — either the farm being audited or threat-feed ingestion. Strongest new target-class cluster of the session.

## NEW CANDIDATE 2 — workers.dev redirector flood (strong, in-progress at 05:04 UTC)
- **11+ distinct `*.workers.dev` submitted 04:31 → 05:03 UTC** (bare domains, rapid succession):
  - 04:31: `tg.985.workers.dev/`, `www.v3.quiet-disk-62f9.hrmcxaeel.workers.dev/`, `winter-waterfall-0606.rihaniomar21.workers.dev/`, `www.serve1.darix168035584.workers.dev/`, `z10.info-alishafagh.workers.dev/`, `worker-calm-mountain-c6f5.akermankowalczykz-iu-c-p-2-4-0-8.workers.dev/`
  - 04:31–04:32: `www.green.qihu360.workers.dev/`, `worker-vless.zhousaiqian.workers.dev/`, `www.7ddce2d9.7fc087fbd273b757485ac4d5.workers.dev/`, `www.github.3080979813.workers.dev/`, `www.pboag26392.workers.dev/`
  - 05:03: `office21174302441641798141027.secureprovide.workers.dev/` (phishing-kit name: "secureprovide" + numeric doc-lure), `sell.iv2ray1.workers.dev/`, `www.agh-edu-pl.heidrun-smailus.workers.dev/` (impersonates agh.edu.pl), `www.little-cake-cc85.gakofo25091405.workers.dev/`
  - Also `sky.giyohap467.workers.dev/` at 03:25 (window1) — the flood started earlier or is continuous.
- Cloudflare Workers = free redirector hosting; names include brand-impersonation and doc-lure patterns. Shape = farm sweep (one bare-domain submission per host). TDS 1–2 each.

## NEW CANDIDATE 3 — pages.dev bulk batch (strong)
- **11 distinct `*.pages.dev` submitted 03:20 → 03:33 UTC** (13 min), all bare-domain:
  - `live-desktop--ledgr.pages.dev/`, `jen8c-tc0-4g6s-sq3ei-01-10-2026-aa.pages.dev/`, `sp12ct-farsik-biz-kazdor-holdel.pages.dev/`, `1f7zx-1aw-f2wa-uvk9m-30-09-2026-aa.pages.dev/`, `frost-paper57.pages.dev/`, `arrow-fork.pages.dev/`, `ashen-badge-wood.pages.dev/`, `kiwi-park.pages.dev/`, `pathdust.pages.dev/`, `mywhatshappp.pages.dev/`, `lunar-stream-copper.pages.dev/`
  - Plus `tetes-air.pages.dev/dp/B0B6GK4VTC` (04:31 firehose — Amazon ASIN path, scam-shop shape).
- **Date-stamped bulk names**: `jen8c-…-01-10-2026-aa`, `1f7zx-…-30-09-2026-aa` = programmatic bulk creation with creation-date in the hostname. Others are Cloudflare-Pages auto-names. Same sweep shape as candidates 1–2.

## NEW CANDIDATE 4 — urldance.com namespace walk (medium)
- `202608.urldance.com/7d/` and `202608.urldance.com/8d/` submitted same minute (04:31), sequential path letters — namespace enumeration of a URL-shortener/redirector. 156.225.108.43/42 (AS139057 Edgenext). Only 2 points; needs history pull (pending egress).

## Related infra notes (from window1.json 03:00–03:58 + firehose)
- **`.shop` an* family grows**: `anewsleepstudio.shop` (03:37), `angelicreads.shop` (03:36), `anchorsskateshopsupply.shop` (03:20) join andcollaronline/andarstore/ancientwgo/anbio/angelostore (bare+slash pairs). 8+ shops now.
- **Bare+www pairing echoes bare+slash**: `binance-register.blogspot.com` submitted as both bare and `www.` at 05:03 — same dual-submission signature as the .shop family, now on blogspot phishing.
- **S3 phishing buckets**: `www.myapt67.s3.amazonaws.com/` (04:32), `www.amazon-connect-263d5ca49255.s3.amazonaws.com/` (05:03).
- **ddnsgeek bulk**: `jehalisipo.ddnsgeek.com/uwojad/`, `dudamu.ddnsgeek.com/jipoco/` (04:31) — random-subdomain dynamic-DNS phishing.
- **DGA-name domain**: `appdmnmbg.com/download/` (04:31).
- **Monitoring-shape repeats** (not new): paralino.app ×6, www.get-monai.app ×5 (03:19–03:43, bare-domain resubmits every 4–8 min); known Amap `uqscan=` burst still active.

## Open threads / blocked
- Egress outage blocked: the 15-query htmx sweep (`redirector_sweep.py`, same dir — run when egress recovers), per-host history pulls for xsph.ru / urldance.com / workers.dev families, urlscan wildcard/payload searches (`refer=119334` fingerprint), watch-phrase `seekers` search.
- Cadence for candidates 1–4 is minute-precision only (homepage table); need report-level timestamps to test metronomicity like the jmail 3-min signature.
- Whether the farm-sweeps (candidates 1–4) are the SAME operator as the jmail auditor (different submission signature: bare-domain vs `?q=` probes + cachedview) or a second actor / threat-feed ingestion — unresolved.
- Notable: the jmail auditor's run ENDED 03:58 UTC; the pages.dev burst (03:20–03:33) overlapped its tail; workers.dev/xsph.ru sweeps began 04:31+. Sequential target rotation is plausible.
