# CARTOGRAPHER — Target-Pattern Hunt

Persona: **The Cartographer**. Doctrine: swarms reveal themselves by *what they point at*.
A new target class under systematic enumeration = a new swarm's workload.

Date: 2026-10-05 (UTC). Method: urlquery htmx (keyless, ≤1 req/5s) + urlscan.io,
five parallel target-class hunters. Exclusions: known Amap operator
(`uqscan=`/`uqtag=`/`uqvnc=` grammar, amap.com, IDPH/iowa.gov, AIHW/aihw.gov.au,
museum `uqscan` family).

## Collection status (2026-10-05 ~05:10 UTC)

VM egress outage began ~04:30 UTC Oct 5 — all external HTTPS (urlquery.net,
urlscan.io, curl) times out at TLS handshake via the egress proxy. Likely cause:
15+ concurrent uq_htmx.py/uq.py queries from sibling subagents on one shared
egress IP → IP-level throttling/edge-block. Live htmx sweeps for most lanes are
**blocked, not completed**; background retry loops parked. Findings below are
prior-art synthesis + completed queries; residual gaps marked for re-run when
the throttle clears.

## Findings by target class

### 1. Map/POI systems — CLEAN NEGATIVE (covered ground)
- Known operator is **Amap-exclusive**: other-targets lane (auth API, 1,245
  reports) found honest zeros for `uqscan` grammar on map.baidu.com,
  map.qq.com, lbs.qq.com, tianditu.gov.cn, meituan, dianping, ctrip.
- Firehose window (~03:00–03:58 UTC Oct 5, 123 reports): 3 map/POI hits, all
  known operator (B03DF05V64, 3× resubmits at 03:43 — tag re-tests).
- **GAP**: Western map/POI (Google Maps place, OSM, TripAdvisor, Yelp,
  Zillow/Redfin, Naver, Yandex) still unswept via live htmx — re-run when
  egress recovers.

### 2. Health data portals — PARTIAL (blocked mid-sweep)
- Cartographer own-pass (pre-outage): `tableau` query, uq-grammar excluded →
  **non-operator health/gov Tableau targets**: `dshs-tableau-prd-831217639.us-gov-west-1.elb.amazonaws.com` ×2
  (US gov cloud, DSHS = social/health services), `apprenticeship.gov` ×1.
  Worth cluster-checking when htmx recovers.
- AIHW template (known, excluded): Tableau `.csv` export URLs with
  `:showVizHome=no` driven through cf-cors proxies / r.jina.ai bridges.
- urlscan probe: `domain:tableau.com` (30d) showed only stcroixhospice scans —
  loose matching, no health signal.

### 3. Dev consoles + crypto — PARTIAL (blocked after 1 query)
- `tronzap` on urlquery htmx (pre-outage): **0 reports** — the lhr.life SSTI/RCE
  campaign (urlscan-side: dash/api/bo/dev/mock subdomains, `/eval-stdin.php`,
  Sep 5 – Oct 4 2026) has **no urlquery-side footprint**. Campaign is
  urlscan-visible only.
- Sweep resume script parked at `personas/cartographer/sweep-resume.sh`
  (runs when egress returns).

### 4. Gov domains by country — PENDING (hunter running)

### 5. Phishing-redirector farms — COMPLETE (browser-path workaround, egress down)
- **jmail.world auditor EXTENDED**: cross-platform — same auditor submits to
  urlscan.io too (9 scans, 2026-10-03→10-04, identical `?q=` probe payloads,
  affiliate IDs 19384926/119334). Archive-oracle use extends beyond jmail:
  `cachedview.nl/#pinterest.mx/seekersofdecay/…` — the watch-phrase is a
  Pinterest slug. Sibling farm: `jmail.best`. Timing: median gap 3.0 min,
  33/71 gaps exactly 3 min — machine-metronomic.
- **NEW candidate 1 — xsph.ru bulk-created phishing farm (strong)**: 7
  hex-prefix subdomains (`f0575425`, `f0536218`, `a0655455`, …), all
  141.8.197.42 (AS35278 Sprinthost.ru), ~1 per 4–5 min at 04:31–05:04 UTC.
  Shared 3-char prefixes = sequential bulk-creation grammar.
- **NEW candidate 2 — workers.dev redirector flood (strong, live at 05:04)**:
  11+ `*.workers.dev` in ~32 min with phishing-kit names
  (`secureprovide.workers.dev` doc-lure, `agh-edu-pl.heidrun-smailus` agh.edu.pl
  impersonation, `green.qihu360`, …).
- **NEW candidate 3 — pages.dev bulk batch (strong)**: 11 `*.pages.dev` in
  13 min (03:20–03:33), date-stamped programmatic hostnames
  (`…-01-10-2026-aa.pages.dev`) + Cloudflare auto-names; Amazon-ASIN-path
  scam-shop shape (`tetes-air.pages.dev/dp/B0B6GK4VTC`).
- **NEW candidate 4 — urldance.com namespace walk (medium)**: `/7d/`, `/8d/`
  same minute — sequential shortener-path enumeration, needs history pull.
- `.shop` `an*` family grows to 8+; bare+slash dual-submission signature now
  echoes on blogspot (`binance-register.blogspot.com`).
- **Open question**: are candidates 1–4 the same operator as the jmail auditor
  rotating targets (jmail run ended 03:58, pages.dev burst overlapped its
  tail, workers/xsph began 04:31+)? Sequential rotation plausible, unproven.
  Second-precision timestamps + history pulls needed — blocked by egress.

## Bottom line so far

Every map/POI scan trace in the examined windows resolves to the known Amap
operator. The only non-operator health/gov Tableau targets seen
(`dshs-tableau-prd…us-gov-west-1`, `apprenticeship.gov`) are single-digit and
unclustered — leads, not swarms. Tronzap's exploit-probe campaign is
urlscan-only. No second systematic-enumeration swarm has surfaced on the
covered ground.
