# TARGET-CLASS HUNT — dev consoles + crypto platforms (urlquery-side)
Persona: cartographer | Date: 2026-10-04 (Sun)
Goal: hunt NEW swarms by TARGET patterns (dev consoles / crypto), not by language.
Method: urlquery keyless htmx endpoint (`uq_htmx.py search`), ≤1 req/5s; urlscan.io search API.
Exclude: Amap/IDPH/AIHW operator (`uqscan=`/`uqtag=`/`uqvnc=` grammar).
Tronzap (lhr.life tunnels → tronzap.com SSTI/RCE matrix) = NOTED LEAD, different actor.

## Query plan (background sweep /tmp/devconsole_sweep.sh, limit 60–100 each)
Dev-console lane: phpmyadmin | grafana | jenkins | wp-admin | wp-login.php | gitlab | admin/login | staging. | dev- | console | panel
Crypto lane: tronzap | tron | binance | coinbase | metamask | wallet | mining | exchange
Test-matrix/relay grammar: {{7*7}} (SSTI PoC) | ssti | lhr.life
urlscan.io API: domain:lhr.life | domain:tronzap.com | task.url:phpmyadmin* | task.url:*grafana*

## STATUS (as of 2026-10-05 ~00:06 CDT / 05:06 UTC)
BLOCKED: VM egress down. First htmx request (~23:24 CDT) succeeded (`tronzap` → 0 reports, zero footprint on urlquery).
Subsequently: ALL external HTTPS times out at TLS handshake (urlquery.net, www, api.urlquery.net, urlscan.io, google.com, example.com).
TCP/443 opens via egress proxy; DNS resolves. Local loopback fine. → VM-level egress outage, not a site block.
Attempts at ~23:40, ~23:52, ~00:06 CDT all failed. A background paced sweep (/tmp/devconsole_sweep.sh) was launched
but /tmp was wiped mid-run (ephemeral) and the sweep died before egress recovered.
RESUME: run `bash ~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/cartographer/sweep-resume.sh`
once egress is back; it writes durable JSON to `personas/cartographer/sweep-out/` and runs the grammar-exclusion check.

## SWEEP EXECUTION (2026-10-05 ~05:19–06:03 UTC) — COMPLETE
Egress flapped all night (TLS hangs; curl to urlquery.net/google.com/example.com timing out, TCP/443 open).
- Watchdog loop probed every 90s; egress window opened 05:19 UTC → launched sweep-resume.sh.
- First pass: only 4/22 urlquery queries survived (grafana, wp-login.php, ssti, tronzap) — urllib hit
  `IncompleteRead` on flaky responses (36–40KB read then cut).
- Fix: wrote `sweep-curl.py` (same parse logic as uq_htmx.py, fetch via curl) — collected the other 18 queries
  (100 reports each where the query supports it) over 05:43–06:03 UTC.
- All JSON in `personas/cartographer/sweep-out/` (uq_*.json + urlscan_*.json), plus `analysis.json` (this summary),
  `watchdog.log`, `retry.log`, `retry2.log`, `retry3.log` (pass logs; retry3 "FAILED" lines are a logging bug —
  every query has a matching success line above it).
- urlscan.io reachable for 3/4 queries. `task.url:*grafana*` → 403 (leading wildcard blocked for anonymous);
  retried as `task.url:grafana*` → 200 (total 2864: Azure-managed Grafana instances, Oct 3–5 stream, no fleet).

## PER-QUERY RESULTS (urlquery htmx, uq-grammar exclusion = 0 hits on all 22)
| Query | n | Range | Verdict |
|---|---|---|---|
| phpmyadmin | 100 | 2026-01-18..10-04 | noise — scattered panels; phpmyadmin.inoqta.com scanned 2× (Jul 11, Sep 20) |
| grafana | 23 | 2026-09-27..10-04 | note — tecnalia.dev own-infra cluster (4 hosts Oct 3–4); u89raiojze.abqnhtupni.net game-load ×5 (Sep 27) |
| jenkins | 46 | 2026-07-08..10-04 | noise — legit CI (opensearch ×8, ros2 ×4, fedora) + name collisions |
| wp-admin | 100 | 10-04..10-05 | noise — scattered site homepages |
| wp-login.php | 23 | 2026-08-30..10-04 | note — 2 phish reset kits w/ crypto lures: "1.3421 BTC BINANCE" (oroetentazioni.com), "112 957 USD VISA" (live.tichyseinblick.shop) |
| gitlab | 71 | 2026-09-14..10-05 | noise — scattered; git.code.tecnalia.dev ×2 |
| admin/login | 100 | 10-02..10-05 | CANDIDATE — RU namespace sweep: ~100 .ru/.su/.by domains, peak 9/hr (Oct 3 07:00/16:00 UTC); programmatic, purpose unknown |
| staging. | 100 | 10-03..10-05 | note — ovou.com Thai pirate-stream ×16 (own scans); appwrite *-staging branch deployments |
| dev- | 100 | 10-05 only | CANDIDATE — 91 submissions in 1hr (04:00–05:45 UTC), global random domains; live bulk sweep, same window as appwrite enumeration |
| console | 100 | 10-05 only | CANDIDATE — LIVE appwrite deployment-ID enumeration: 18 sequential hex IDs (6ac327aa→6ac33619) + branch-main-*/master/staging names, ~60 reports in ~1hr; esports.freefirecommunity.com ×7, scholia.io ×4 |
| panel | 60 | 10-05 only | note — same appwrite burst + roblox phish-mirror fleet (roblox.com.mu/ly/et /users/<id>/profile, privateServerLinkCode) |
| tronzap | 0 | — | confirmed-zero (0 reports twice: Oct 4 23:24, Oct 5 05:19) — no urlquery-side footprint |
| tron | 100 | 2026-09-21..10-05 | note — crypto phish: relay-cc.appwrite.network ×6, pumpfunlivesstreamnow.xyz ×4 (Sep 29) |
| binance | 100 | 2026-09-25..10-05 | note — infinitenova.org support-scam ×6, relay-cc.appwrite.network ×3, novascreener.com ×3 |
| coinbase | 100 | 2026-09-23..10-05 | note — coinbaise.vercel.app typosquat ×3 (Oct 1), walletrecovery.net ×3, tonelib.net ×3, relay-cc ×3 |
| metamask | 100 | 2026-09-22..10-05 | note — GitBook MetaMask-drain phish fleet: 10 typo subdomains (*.gitbook.io, Sep 24–Oct 5); relay-cc ×4 |
| wallet | 60 | 10-04..10-05 | note — grosats.com ×7 (Oct 5); wasmer.app Ledger/Trezor phish kits ×4 |
| mining | 60 | 2026-09-26..10-04 | noise — scattered; poki.com ×6 (gaming) |
| exchange | 60 | 10-04..10-05 | noise — blogspot/blogger spam |
| {{7*7}} | 100 | 10-03..10-05 | noise — 100 unique hosts, one-off SSTI probes (pentester noise; incl app.debridge.com, duckdice.io, vechain.org) |
| ssti | 23 | 2026-08-02..10-03 | note — jojobet*.vip Turkish betting phish-mirror fleet (8 subdomains Aug 2–20); flrdrop.vip ×3; BR gov phish |
| lhr.life | 100 | 2026-01-06..10-04 | **KEY — OWN OPERATOR CONFIRMED urlquery-side**: 6 subdomains / 20 reports Jun 18–21: `uqcors.html?v=1` ×8 burst (Jun 18 14:37–14:38), `probe2.html?n=` ×4 with SEQUENTIAL nonces (1782077001/2/3/4), `combo.html?slow/fix/x=<19-digit>` ×4, `probe.html?cached/x=` ×4; PLUS httpbun→Google-Translate relay serving `probe.js` (`httpbun-com.translate.goog/...`, uqn=988806031057, Jun 21) — corpus-tradecraft match (httpbun relay laundering) |

urlscan.io: `domain:lhr.life` 90 results (tronzap campaign per FINDINGS.md; daily watcher 90667af7b6a9f1 active → Oct 4; Sep 21 tunnel-farm burst 6 subdomains in ~4s) — known actor. `domain:tronzap.com` 405 total (Sep 26 Laravel/PHP debug-endpoint sweep: `index.php?-s`, `cgi-bin/eval-stdin.php`, `vendor/composer/installed.json`, `phpinfo.php`, `/_ignition/execute-solution`, `/livewire/update`, `/@vite/client`, `/.git/config`, `/healthz`, `/fpm-status`, `/nginx_status`, `/server-status`, `/up.json`, `/ready`; nothing after Sep 29 in first 100) — known actor. `task.url:phpmyadmin*` 664 total — scattered admins + phishing, no fleet.

## CANDIDATE CLUSTERS (evidence grading)
- **A. Appwrite deployment enumerator (LIVE, Oct 5 ~04:49–05:47 UTC)** — STRONG programmatic / agent-shapedness UNCONFIRMED.
  18 sequential hex deployment IDs `6ac327aa…6ac33619` + `branch-main-74ed670/a0904a4/13895dc/3c78651`,
  `branch-master-fff79b3`, `branch-staging-d9ca8d2`, `praxis-staging`, `rebrief-app-staging`,
  `survival-board-game-staging`; ~60 reports in ~1h across console/panel/staging queries. Sequential-ID namespace
  enumeration + burst cadence. Cross-link: ExploitGym corpus ran agents against Appwrite console/branch deployments
  — same surface. Could be a researcher/harness rather than an agent.
- **B. RU admin/login sweep (Oct 2–5)** — MEDIUM. ~100 .ru/.su/.by domains, peak 9/hr (Oct 3 07:00 & 16:00 UTC).
  Programmatic .ru-namespace sweep for admin/login content; purpose unknown.
- **C. dev- global sweep (live, Oct 5 04:00–05:45)** — MEDIUM. 91 submissions/hr, random global domains; same
  window as A — possibly the same actor sweeping broad domains while enumerating appwrite deployments.
- **D. Own operator on lhr.life (Jun 18–21)** — CONFIRMED (not a new swarm). New cross-surface evidence:
  our operator's `uqcors`/`probe`/`combo` pages on lhr.life tunnels on urlquery.net, sequential 19-digit nonces,
  plus the httpbun→translate.goog relay serving `probe.js` with `uqn=` nonce — first urlquery-side proof our
  operator used localhost.run tunnels + httpbun relay laundering.
- Human phish fleets (NOTED, not pursued — hunt is agents, not human operators): metamask GitBook typosquat
  fleet (10 subdomains), roblox mirror fleet (com.mu/ly/et), jojobet betting mirrors (8 subdomains),
  wasmer.app Ledger/Trezor kits, coinbaise.vercel.app, infinitenova.org support-scam, relay-cc.appwrite.network
  (cross-query crypto-phish page, scanned Sep 22/27/30).

## Prior context pulled locally (no egress needed)
- Tronzap campaign documented in data/2026-09-28-chinese-amap-fleet/urlscan-lhr/FINDINGS.md (urlscan-side):
  - SSTI/RCE test-matrix naming (rc/ssti/php/mustache/nl/dollar/semi/calc), tunnels `*.lhr.life` → tronzap.com
  - Subdomains enumerated: dash/api/bo/dev/dev-api/dev-dash/devbo/mock/ref; `/eval-stdin.php` endpoint (first seen 2025-03-25)
  - Burst: Sep 26 (~40 scans/2h); timing Sep 5 – Oct 4 2026
  - Zero overlap with our operator (78 vs 29 subdomains, no uq* grammar) — separate actor
- urlquery-side footprint of tronzap: UNKNOWN (single `tronzap` htmx query returned 0 reports at 23:24, before outage)
- Open urlscan threads (from FINDINGS.md): `90667af7b6a9f1.lhr.life` daily watcher; `/view/Perm/Fill/` route (Sep 21); is.gd `Oufqgj` ×43 cluster

## Queries run
1. `tronzap` (htmx, limit 20) @ 2026-10-04 23:24 CDT — SUCCESS, 0 reports. Real zero: valid JSON
   `{"reports": [], "query": "tronzap"}` returned BEFORE the egress outage. No urlquery-side footprint for the
   tronzap lead as of that timestamp.
2. `phpmyadmin` — never completed (outage began between query 1 and 2).
3–22 (planned, not yet run — in sweep-resume.sh): grafana, jenkins, wp-admin, wp-login.php, gitlab, admin/login,
   staging., dev-, console, panel, tron, binance, coinbase, metamask, wallet, mining, exchange, {{7*7}}, ssti, lhr.life,
   + urlscan.io: domain:lhr.life, domain:tronzap.com, task.url:phpmyadmin*, task.url:*grafana*.
