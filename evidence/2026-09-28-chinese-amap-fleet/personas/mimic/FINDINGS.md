# THE MIMIC — thinking like the operator (2026-10-05)

## Operator model (ground truth)

Data-collection swarm, Chinese Amap POI vertical, Jan–Oct 2026, still live. Grammar `uqscan=<pinyin><YYYYMMDD>[a-z]` → drifting (`uqm=`, `uqattempt=`, `uqid=`, bare epoch-ms). Task families: parks → museums → zoos → hospitals → food. Infra: lhr.life tunnels, is.gd, webhook.site, fetch relays (jina DEAD keyless), httpbun/httpbingo/postman-echo staging, LiveCodes. Date labels on China time. 4–8 concurrent runs, peak 10:00–11:00 UTC.

## Mimic predictions

### Next task families (POI verticals, in likely order)
1. **Schools/universities** — rich structured POI data, same shape as museums. Predicted tags: `<city>school2026100X`, `<city>university`.
2. **Government service centers** (政务) — predicted: `<city>gov`, `<city>zhengwu`.
3. **Malls/commercial** — `<city>mall`.
4. **Restaurants** — extension of food family.
5. **Pharmacies/banks/charging** — long tail.
6. **Geography**: HK/Macau/Taiwan POIs or overseas Chinese tourist spots (`hongkong`, `macau`, `taiwan`, `taipei`).

### Next infrastructure (dead-service migration)
- **jina replacement** (keyless dead): md.dhr.wtf, urltotext, markdowner, or NEW fetch-proxy domains carrying `uq` grammar. Watch for first-seen proxy + Amap co-occurrence.
- **Dead-drop**: webhook.site alive; if it dies → ntfy.sh, requestcatcher, beeceptor, stash.legible.sh.
- **Shorteners**: is.gd alive; watch da.gd, t.cn, dwz.cn, clck.ru, s.id, gg.gg.
- **Tunnels**: lhr.life alive; watch ngrok-free.app, trycloudflare.com, loca.lt, bore.pub.

### Grammar evolution (observed drift)
`uqscan=` → `uqm=` → `uqattempt=` → **`uqid=` (CONFIRMED 2026-10-04, see below)** → bare epoch-ms (`?uqscan=17911717661939`). Direction: shorter, more opaque, less self-documenting. Next: single-char params, bare nonces.

## Prediction scorecard (2026-10-05)

### CONFIRMED
- **`uqid=` grammar drift** (2026-10-04T14:21/14:22Z): `postman-echo.com/redirect-to` and `nghttp2.org/httpbin/redirect-to` → Amap SSR place URLs carrying `uqid=` instead of `uqscan=`. Novel staging host: **nghttp2.org/httpbin** (not in known set). Zero urlscan presence.
- **More drift**: tags migrating into `src=` param (`src=claude20261005jxmuseum`, `src=fujianmuseum_top_20261005a`); hyphenated tags (`uqscan=tianshanzoo-parent-www-20261005a/b`, `uqscan=navy971-20261005a/b/c`). `uqt=`/`uqv=` zero. `src=manual0/1/2` pre-existing.
- **Fleet expanding within known families** (not new verticals): new museums (fujian, gx/Guangxi, jx/Jiangxi), new zoo (tianshanzoo, Xinjiang), new scenic (zhenbeibao Ningxia, gubei, hzparadise, dawugang), hospitals continuing.
- **Geography direction**: domestic-western provinces (Ningxia, Xinjiang, Guangxi, Fujian, Jiangxi, Shanxi) — NOT HK/Macau/Taiwan/overseas.
- **New infra host**: `ditu.amap.com` usage observed.

### CLEAN NEGATIVES (predicted, not found)
- New verticals: school/gov/mall/food/scenic/pharmacy/bank/estate, xuexiao, zhengwu — zero.
- HK/Macau/Taiwan/overseas tags — zero.

### Pending
- `raw/nv_hunt.py` — 24-query paced sweep driver, resumable; re-run when urlquery.net recovers (live hunt was blocked by VM egress outage ~04:26–05:10 UTC).
- `raw/infra-migration.md` — hunter still running.

## Other operators modeled

### Vuln-assessment swarm (tronzap precedent)
Shape: exploit-test matrix naming (`k-ext-ssti`, `c-rc-php`, `o-rc-{nl,dollar,semi}`, `calc`, `e0-ev2`), tunnels as disposable infra, urlscan API submissions, ~40-scan bursts. Hunt result: **honest negatives** — zero open-web hits, zero Google-indexed urlscan/urlquery traces (operator-internal labels; campaign used urlscan only). No second campaign found. Pending: urlscan-API matrix hunt needs a urlscan API key + recovered egress (delegation spec in `raw/other-operators.md`).

### Detection swarm (jmail.world precedent) — CAMPAIGN MUCH BIGGER THAN KNOWN 72
- `seekers+of+decay` watch-phrase probed on **Google AI Mode (`udm=50`)** across google.ca/.co.nz/.im/.es/.ru starting **July 2026**, ~2 months before the September jmail bursts.
- jmail probes span 09-05→09-26 in repeated 2–5 min bursts (the known 72 is one burst), alternating canary phrase with known-bad redirector URLs across person/thread/drive/promotions/sent paths.
- **NEW second swarm (misfit → lead): `udm=50` SEO-indexation verification** — same AI-Mode oracle grammar, interleaved in the same submission batches, asking AI Mode about the operator's own spam pages (11+ domains: backlink-generator-tool.github.io, blogspot farms…), rotating Google country domains, running since **January 2026**. cachedview.nl usage ties it to the jmail lane — likely same operator's second lane.
- Phishing-redirector audit lane: Google `/url` → AMP-cache → base64-email redirect chains submitted to urlquery (victim emails recorded as metadata only).
- Archive-oracle tradecraft (cachedview.nl) is shared across both swarms — operator-family marker.

## Pending hunter reports
- `raw/next-verticals.md` — COMPLETE (see scorecard)
- `raw/infra-migration.md` — hunter still running
- `raw/other-operators.md` — COMPLETE (see above)
- Note: one hunter hit full VM egress outage during its session; its live-API items are marked `[pending-egress]` with a re-run script at `/tmp/mimic/run_opA_htmx.py` (ephemeral — re-create from `raw/other-operators.md` delegation spec if needed).
