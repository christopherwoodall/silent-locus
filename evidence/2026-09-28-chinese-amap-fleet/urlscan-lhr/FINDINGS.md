# urlscan.io lhr.life Investigation — Findings (2026-10-05)

**Question**: is the urlscan.io `lhr.life` population the same operator as our urlquery.net `lhr.life`/`uq`-grammar campaign, or a different actor sharing localhost.run?

**Verdict: different actor.** No shared subdomains, no shared grammar, different TTP family, different target.

## 1. The urlscan population (90 results, `domain:lhr.life`)

**Page clusters** (test families):
| Family | Pages | Count |
|---|---|---|
| Root (tunnel landing) | `/` | 47 |
| SSTI test matrix | `k-ext-ssti.html`, `c-rc-mustache.html` | 2 |
| RCE test matrix | `c-rc-php.html`, `o-rc-php.html`, `o-rc-nl.html`, `o-rc-dollar.html`, `o-rc-semi.html`, `k-ext-semi.html`, `c-energy.html` | 7 |
| Eval series | `e0/e1/e3/e4/ev/ev2.html` | 6 |
| Calc PoC series | `calc/calc3/calc4/calc_min.html` | 4 |
| Check pages | `chk/chk2/check2.html`, `lw.html` | 5 |
| Single-letter probes | `s/s2/de/mi/m/pa/o/p.html` (10 pages, ~15 min, Sep 26) | 10 |
| Misc | `app.html`, `ig.html`, `quote2.html`, `cancel.html`, `login.html`, `/view/Perm/Fill/` | 7 |

**Naming reads as a systematic vulnerability-test matrix**: `rc` = remote code, `ssti` = server-side template injection, engine variants (`php`, `mustache`), bypass variants (`nl` = newline, `dollar`, `semi` = semicolon), `calc` = classic `{{7*7}}` PoC. The single-letter pages (`s/s2/de/mi/m/pa/o/p`) are rapid-fire probe iterations.

**Tunnels proxy tronzap.com**: page titles on urlscan show `api.tronzap.com` and `dash.tronzap.com` — the tunnels forward to TRON energy-rental platform infrastructure. TronZap = TRON blockchain energy/bandwidth rental (crypto, https://tronzap.com). Screenshots show CloudFront 403s (tunnels down at scan time).

**Timing**: concentrated Sep 5 – Oct 4, 2026. Intense burst Sep 26 (~40 scans in 2 hours = the test matrix run). One tunnel (`90667af7b6a9f1.lhr.life`) scanned ~daily (27×) — monitoring pattern, likely a researcher or urlscan auto-scan watching that tunnel.

## 2. Comparison with our urlquery operator

| Dimension | urlquery operator (ours) | urlscan lhr.life population |
|---|---|---|
| Subdomains | 78 hex subdomains | 29 hex subdomains — **zero overlap** |
| Pages | `uqcors.html`, `probe.html`, `combo.html`, `probe.js` | SSTI/RCE test matrix, calc/eval series |
| Grammar | `uqscan=`/`uqtag=`/`uqvnc=`/`?x=<19-digit>` | **none** — zero `uq*` on urlscan |
| TTP | CORS probes, keep-alive beacons, data collection | exploit-payload testing |
| Targets | Amap (maps), IDPH (health), AIHW (health) | tronzap.com (crypto) |
| Timing | Jan–Oct 2026 | Sep 5–Oct 4, 2026 |

**Marker sweeps on urlscan** (all zero): `uqscan`, `uqcors`, `mobile-ua`, `customua`, `webhook.site+amap`, `httpbun+probe`. Operator's is.gd slugs (`mf075827`, `sum074114`, `3JlIp7`, `AGE115EXTRACT1`) absent from urlscan's 191 is.gd results (different slug population: `Oufqgj` ×43 etc.).

## 3. Assessment

The urlscan population is **someone testing SSTI/RCE payloads through localhost.run tunnels pointed at tronzap.com** — either a pentester probing the crypto platform or tronzap's own developers. It is not our data-collection operator:

1. Zero subdomain overlap across 107 combined subdomains
2. Zero `uq`-grammar markers on urlscan (7 marker queries, all zero)
3. Fundamentally different TTP: exploit testing vs data collection
4. Different target vertical: crypto vs maps/health-data

**Shared localhost.run usage is not an operator link** — it's a public tunnel utility, like webhook.site for dead-drops. (Same logic as the Chinese-infra finding: shared commodity infra ≠ shared operator.)

## 4. Open threads (not ours, noted for completeness)

- Who is testing tronzap.com via tunnels? The `90667af7b6a9f1` daily-scan pattern suggests a watcher; the Sep 26 test-matrix burst suggests the tester.
- `/view/Perm/Fill/` route on two tunnels (Sep 21) — an interesting tronzap path worth a look by whoever tracks that platform.
- The is.gd urlscan population (`Oufqgj` ×43) is a separate cluster, possibly phishing — not examined here.

## Raw data

- `/tmp/lhr_urlscan.json` — all 90 urlscan search results (ephemeral; re-pull via `https://urlscan.io/api/v1/search/?q=domain:lhr.life&size=100`)
- Screenshots: `01a0deec` (k-ext-ssti, CloudFront 403), `01a0def0` (ev.html/dash.tronzap.com, 403), `01a10729` (90667af7b6a9f1 root, "no tunnel")
- Note: urlscan result API (`/api/v1/result/<uuid>/`) requires login (403); public result pages + screenshots work unauthenticated.

## 5. Tronzap campaign — noted lead (2026-10-05, per user: no separate track, keep as note)

**Agent-shapedness assessment**: programmatic (API submissions), parameterized test-matrix naming, iterative retry series, burst parallelism, full-estate enumeration. Reads agent-shaped; a human pentester's script produces the same shape. Payload content (behind urlscan login) would settle it — agent payloads carry tells (verbose comments, prompt-like structure).

**Campaign scope** (`domain:tronzap.com` on urlscan.io, 405 results): systematic coverage of `dash`, `api`, `bo`, `dev`, `dev-api`, `dev-dash`, `devbo`, `mock`, `ref`, `tronzap.com` — prod and staging/dev enumerated. Tunnels proxy to `dash.tronzap.com/eval-stdin.php` (first seen 2025-03-25, pre-existing endpoint, not a fresh webshell).

**Status**: not our `uq` operator (zero subdomain/grammar overlap). Separate actor running a sustained vuln-assessment campaign against a TRON energy-rental platform via disposable localhost.run tunnels. Noted, not pursued — revisit if payload-level evidence or a second surface connects it to agent activity.
