# urlscan-lane: grammar-hunt verdicts (urlscan.io, 2026-10-05)

12 queries, size=25, anonymous API. Raw: `urlscan-01.json` … `urlscan-12.json`.
Infra note: direct curl to urlscan.io is dead from this VM (egress-proxy CONNECT
stalls 40–60s); all collection went through the browser fetch path. `uq*`
grammar excluded per brief.

## Method caveat (read first)

`task.url` phrase search tokenizes loosely: `task.url:"step="` matches the bare
word anywhere (hostnames), NOT param position. Word queries (nonce/worker/agent/
batch/probe/eval/check) are dominated by hostname collisions. Param-position
search is not possible via task.url. So: word-query lanes are mostly hostname
noise; the real yield comes from domain-scoped queries and misfit review.

## Verdicts

| # | Query | Verdict | Evidence |
|---|---|---|---|
| 01 | `task.url:nonce` (total 130) | **noise** | `nonce=` is standard OAuth/OIDC param. Misfits (not swarm): `rib-nonce-injector.philtrust-bank.workers.dev` (2026-10-03, 404); `kalooms.com/84701200a6b933a7cad7342690150adc?id=<md5>&nonce=<hex32>&ts=<epochms>` (2026-10-01, clickfix/kalooms/stage1); `ramadatour.be/.within.website/x/cmd/anubis/api/pass-challenge?id=<uuid>&response=<hex64>&nonce=115012&redir=…&elapsedTime=1199` (2026-10-02, Anubis PoW) |
| 02 | `task.url:worker` (total 4289) | **noise** | Pure `*.workers.dev` hostname collisions. One true param: `accounts.intergrity.live/informations.aspx?worker=x` (typosquat phishing) |
| 03 | `task.url:agent` (total 3609) | **noise** | Hostname noise: `z3n-agent-home-split-view-{19-4,15-3,13-3,28-3}.zendesk.com`; `ai-agent-adi-<10rand>.milestonedev.info` burst; `CJ-Agent-v0.7.8-compatible.apk` (cj-agent-download.pages.dev); `icp0.io/agent-marketplace/*` |
| 04 | `task.url:"step="` | **noise** | One true param: `www.pusulabet1159.com/?step=register&btag=31446001_298936` (2026-10-04, gambling affiliate). Single occurrence, no recurrence |
| 05 | `task.url:"zz="` (total 419) | **NEW honest zero** | Zero `zz=<word>` params in window. Misfits noise: `trezor-suite-zz-site{069,092,097,917}.com.ph` phishing (zz in hostname); `uyghurkitchen.saifur.com.bd/okjxtrf/1vfnout/1zluxse/Zz/diff.html` (2026-10-04, exploit-kit path grammar on compromised site) |
| 06 | `task.url:oai` | **NEW honest zero + noise** | No `zz=oai` params (honest zero). Rest hostname noise: `oai-chat-data-backup-att-prod.s3.us-west-2.amazonaws.com` (domainAgeDays 7–9, 2026-10-02), `oai-academy-cert.occupyai.it`, `github.com/yomyoms/oai-proxy-mod/`, `oai-data-plane-*.eus.grafana.azure.com` |
| 07 | `domain:lhr.life` (total 90) | **KNOWN grammar, NEW dated evidence** | See lead below |
| 08 | `task.url:batch` | **noise** | Hostname noise (`buburuzac-split-payment-vat-batch-v1.velesagro.dev.oduist.com`, S3 `*-batch-data-*` buckets, `0-beta4.batch-1.barakaban.org`). UTM params only |
| 09 | `task.url:probe` | **noise** | Hostname noise (`probe-{eu-west,ap-southeast}.teraping.net` EC2 404s), Burp Collaborator `oastify.com/zq9k-sandbox-probe`. Malware mini-grammar noted: `probe-junk-{c,d}-<12alnum>.edgeone.dev` (phishing/malicious) |
| 10 | `task.url:eval` | **noise** | Hostname noise (S3 `*-eval-*` buckets, microsoftdynamics `gcc-eval-env` sandbox → login.microsoftonline oauth, arena-preview lab portals) |
| 11 | `task.url:eval-stdin` | **NEW honest zero** | total 0 — the phpunit eval-stdin paths were REDIRECT TARGETS of the lhr.life harness, never submitted URLs themselves |
| 12 | `task.url:check` | **noise + host lead** | `softwareworld.co/compare/plastiq-vs-online-check-writer` (aitm/malicious, resubmitted); `check-data-<12alnum>.edgeone.dev` (same malware family as #09, VI title "Phân Tích Dữ Liệu"); `sumup-login-check-app.osc-fr1.scalingo.io/app/login.php` (SumUp phishing); `www.zz-org-check-dev.edu.optisyslab.com` — zz-family HOST (zz label prefix on optisyslab.com; "No such academy at this address"; age 0) — not a param grammar, filed as host lead |

## Lead — lhr.life tronzap test-harness matrix (known style, new dated evidence)

**Burst:** 2026-09-26 16:44–18:27 UTC. `<14-hex>.lhr.life` subdomains (wildcard
DNS, EC2) serving harness matrix pages that redirect to `tronzap.com` targets:

- `52949a80bf53fc.lhr.life`: `/c-rc-php.html`, `/k-ext-ssti.html`, `/c-energy.html`, `/o-rc-nl.html`, `/o-rc-php.html`, `/o-rc-dollar.html`, `/k-ext-semi.html`, `/c-rc-mustache.html`, `/o-rc-semi.html` → `api.tronzap.com/v1/orders[/check|/calculate]`
- `d51842b87c3e80.lhr.life`: `/lw.html`, `/e4.html`, `/e3.html`, `/e1.html`, `/e0.html`, `/ev.html`, `/ev2.html` → `dash.tronzap.com/eval-stdin.php`, `api.tronzap.com/eval-stdin.php`
- `ba85c283a8f9e0.lhr.life`: `/calc4.html`, `/calc3.html`, `/ig.html`, `/lw.html`, `/app.html`, `/cancel.html`, `/calc.html`
- `d789d4fd5debd8.lhr.life` (16:44–17:03 UTC): `/chk2,/chk,/s2,/s,/de,/mi,/m,/pa,/o,/p.html` → mock/api phpunit eval-stdin + orders API
- `e815ded61da040.lhr.life`: `/calc_min.html` (2026-09-25)
- `90c6961dd9eba0.lhr.life`: `/app.html`, `/quote2.html`; `3be663c0dc1827.lhr.life`: `/chk2.html`
- `mock.tronzap.com/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php` — phpunit eval-stdin harness (CVE-2017-9841 RCE path) on mock target
- `90667af7b6a9f1.lhr.life`: bare host re-submitted near-daily 2026-09-26 → 2026-10-04 (liveness beacon)

**Page-naming grammar:** `<prefix>-<mid>-<suffix>.html` (prefixes c/k/o; mids rc/ext;
suffixes php/ssti/energy/nl/dollar/semi/mustache) + shorthand pages
(`eN`, `calcN`, `chkN`, `ig`, `lw`, `mi`, `de`, `pa`, `s`).

**Verdict:** known grammar confirmed with fresh dated evidence; harness probes
phpunit eval-stdin RCE + SSTI/RCE matrix payloads against a live-ish order API.
Not a query-param grammar, but the task's test-harness target. The beacon
subdomain (`90667af7b6a9f1`) is a NEW sub-lead: near-daily resubmission suggests
ongoing infrastructure.

## Bottom line

No novel `?<word>=<nonce>` swarm param grammar found on urlscan.io in this sweep.
Two honest zeros worth keeping (`zz=<word>` params absent; `zz=oai` params absent).
One known-style test-harness matrix with new 2026-09-26 burst evidence
(lhr.life → tronzap.com, phpunit eval-stdin RCE probing).
Two sub-leads filed: `90667af7b6a9f1.lhr.life` beacon; `zz-org-check-dev.edu.optisyslab.com` zz-family host.

Do not push.
