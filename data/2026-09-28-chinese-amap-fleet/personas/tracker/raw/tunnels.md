# Tracker sub-task: TUNNEL DOMAINS — findings

Session: `044e514b-c1ff-4ea8-9c3a-377e6edf0dc2` (subagent depth 2/2), parent orchestrator task.
Written: Sun 2026-10-05 (CDT). Source: urlscan.io search API (via `browser.open` text fetch of JSON; VM egress is down so no direct curl/urlquery).

Scope: agents/swarms only. Excluded from findings: the known Chinese Amap-map-collection operator on `lhr.life` (hex subdomains + `uq*` tag grammar, already mapped) and the separate tronzap SSTI/RCE tester on `lhr.life` (noted lead, not target).

---

## 1. `lhr.life` (localhost.run) — NO new activity in newest 40

All newest results (Oct 2–4) are the **excluded** operators:

- Amap operator hex subdomains (all `api` submissions, AWS EC2 IPs, most returning 502/503 at scan time = tunnels already dead):
  `90667af7b6a9f1` (scanned Oct 4 13:45, Oct 3 13:29, Oct 2 09:42, Sep 30 09:27, Sep 29 09:23, Sep 28 05:31, Sep 27 05:24 — **daily ~same-time scans ≈ metronomic liveness polling**),
  `c7a1f824a6efc4` (Oct 2, manual submit), `1881e623217f7c` (Sep 29 ×2), `2f102b0544d3b3` (Sep 29, tagged `hybridanalysis`).
- tronzap SSTI tester (Sep 26 18:14–18:27 UTC, 9 scans across two hex subdomains `d51842b87c3e80` and `52949a80bf53fc`). Probe-page grammar is now fully confirmed from the result list:
  - `e0.html`, `e1.html`, `e3.html`, `e4.html` — incremental exploit-test pages,
  - `ev.html`, `ev2.html` — "eval" tests,
  - `lw.html` — Livewire (`/livewire/update` on `dash.tronzap.com`),
  - `c-rc-php.html`, `k-ext-ssti.html`, `c-energy.html` — RCE/SSTI themed names,
  - targets: `api.tronzap.com/eval-stdin.php`, `dash.tronzap.com/eval-stdin.php`, `api.tronzap.com/v1/orders/calculate`, `.../v1/orders/check`, `dash.tronzap.com/livewire/update`.
  - All blocked (403, CloudFront). The one live page (`e3.html`, 200) served by **SimpleHTTP/0.6 Python/3.11.2** = operator's dev machine, not a hardened server.

**Verdict:** no NEW lhr.life actor. Honest zero beyond the two excluded operators.

---

## 2. `*.zrok.io` (44 results, 30-day window, `has_more=false`, fully read)

**Cluster A — Spanish-language phishing operation (strongest live activity).**
- Rotating **12-char random slugs** (`hatp9x3bcemt`, `xken6ya0b8m2`, `xqqqmi4kvwbg`, `nz90quka1o7n`, `v3uwt50fgr58`, `fg54487jqduc`, `wq5qcswddhcx`, `s4jtkxzzygi4`, `q7z3os42iuse`, `ps7zesk4oqin`, `rblkuusfb8xe`, `wl3yp4cy41al`, `9oj9ovug1l9w`, `0a9092fafuju`) — this is **zrok's own default share-name grammar**, not operator-chosen naming.
- Timeline: Sep 11 → Oct 4 (rotation cadence ~8–9 days; `hatp9x3bcemt` live 200 at Oct 4 09:01, then 404 at 10:49 — active until ~Oct 4).
- Confirmed live content:
  - `xqqqmi4kvwbg` (Oct 1) — `/inges/login.php` live: **ING-bank login phish in Spanish**, tagged `phishing`, `phishnet` (source `openphish`). UUID `01a0f764-be92-705d-80fc-68b9cef54c96`.
  - `nz90quka1o7n` (Sep 25) — **"@java980 - Matrix Leads Tool"** live. UUID `01a0da56-f8be-76e2-9ab0-5e3985630392`. *(Page body not pullable — see gap note.)*
  - `v3uwt50fgr58` (Sep 25) — XAMPP default page.
  - `fg54487jqduc` (Sep 19–20) — Matrix Leads Tool + `/tpe/Seur_2026` **SEUR-carrier phish reached via `ett.re` shortlink**.
  - `wq5qcswddhcx` (Sep 11) — Matrix Leads Tool.
  - `ps7zesk4oqin` — `/sla/SEUu/seu/page/index.php` (dead at scan).
- Uniform stack: **Apache/2.4.58 (Win64) OpenSSL/3.1.3 PHP/8.2.12** = XAMPP on Windows behind zrok — one operator image redeployed under rotating share names.
- Spanish-language templates (ING, SEUR). Slug grammar differs from our operator's 12-hex `lhr.life` grammar (zrok slugs are base62-ish random, not hex) — possible separate fleet, not the same hand. **No `uq*`-analogous tag grammar observed** (tags seen: `phishing`, `phishnet`, `hybridanalysis`).

**Cluster B — machine-paced liveness polling (most programmatic pattern seen anywhere this sweep).**
- Sep 10 16:52–17:05 UTC: rapid-fire API scans of `0a9092fafuju.shares.zrok.io/info` and `9oj9ovug1l9w.shares.zrok.io/info` **~6–8 s apart**, all 404; then root re-scans of the same share names ~6 h and ~12 h later (still 404).
- Reads as a **dead-drop / rendezvous listener polling randomly-named zrok share URLs** — client-side programmatic polling, not a human refreshing. Agent-shaped.

**Cluster C — named share:** `relatoriocrd.shares.zrok.io` (Sep 21, tagged `hybridanalysis`, title "zrok", 200). Only operator-chosen share name in the set; "relatoriocrd" ≈ Portuguese "relatório" (report). UUID `01a0c5f3-c2d2-77c9-baae-093b44b8d114`.

**Noise:** `mcdebtdataadmin.mefmi.org` (legit Vercel dashboard, matched via page refs); tigris.systems dev dashboard referencing dead share `7bqhadbr6uyi`.

**Gap:** `browser.open` on the Matrix Leads Tool result-detail URL failed ("not found") and per system instruction was not retried — its page body/form fields are unconfirmed. Title string verbatim: "@java980 - Matrix Leads Tool". Web search on "@java980" returned only generic phishing results; the tool is unidentified.

---

## 3. `bore.pub` (7 results, 30-day window, all read)

- Single submitter enumerating the bore relay itself, ~1/day Sep 6 → Sep 23:
  `bore.pub:6668/kapubot`, `bore.pub:6668/deploy.zip`, `bore.pub:6088`, `bore.pub:4410`, `bore.pub:2145`, `bore.pub/` root.
- `kapubot` string suggests botnet C2 operator checking tunnel availability; `deploy.zip` suggests payload hosting. Not agent-shaped per se (single actor, manual cadence), but worth a watch.

---

## 4. `ngrok.io` / `ngrok-free.app`

**ngrok.io** (noisy; newest results):
- `paypal-login-confirm.ngrok.io` (Oct 5 00:46–01:21, 3 scans) — all `ERR_NGROK_3200` offline.
- `pavi-saascada.eu.ngrok.io` (Oct 4 22:08), `porres.willo-platform.ngrok.io` (Oct 4 19:38, tagged `@phish_report`), `wetalk.ngrok.io`, `b27562c1.ngrok.io`.
- Phishing-oriented; every endpoint dead at scan time. No cadence or grammar pattern → honest zero for agent-shaped use.

**ngrok-free.app:**
- `www.instagram.com.ngrok-free.app` (Oct 1, `hybridanalysis`, offline).
- `1f01-103-3-221-101.ngrok-free.app` + `29ff-103-3-222-1.ngrok-free.app` (Sep 29, ~4 min apart, tagged `sandbox-shell`; IPv6-ish hex subdomain names).

---

## 5. `*.trycloudflare.com`

Two **live** phishes on Oct 4–5 (Cloudflare quick-tunnel default grammar: `<4 random words>`):
- `subscribe-crimes-ages-nitrogen.trycloudflare.com` (Oct 4 23:50 and Oct 5 01:03, source `openphish`) — Spanish **credit-card phish "Solicita tu Tarjeta de Crédito"**, live 200.
- `seeker-snake-burn-influences.trycloudflare.com/apps/instagram-followers/?i=322743` (Oct 5 04:47) — "Free 5k Instagram Followers", live 200 (query-string `?i=` = campaign id).
- Other names only returned tunnel-error 530. Default random naming = no operator grammar to read. Verdict: active phishing, not agent-shaped.

---

## 6. `*.loca.lt` — honest zero for direct endpoints

Newest 40 results entirely drowned in Indonesian gambling-spam link-farm noise — matched pages only *reference* loca.lt; **no actual `*.loca.lt` endpoint scans seen in this window**. Honest zero.

---

## 7. `*.serveo.net` — richest, most active tunnel surface

**Dutch/Belgian banking-phishing cluster + worldwide brand phish + Sep 28 submission burst.**

Newest (Oct 3–4):
- `munero.serveo.net/login.html` + `recepi.serveo.net/login.html` (Oct 4 01:14–01:16, ~2 min apart — `/login.html` path grammar, Spanish "número").
- `administrador.www.edu.b.009.serveo.net` (Oct 3 20:10–20:12), `tanpa.data.serveo.net` (Oct 3 16:39; "tanpa data" = Indonesian "without data" — possible dead-drop probe).
- `icscards-service-blokkade.serveo.net` (Oct 3 10:16, Dutch "blokade").
- `css.www.facebook.com-login-home-lepus.serveo.net` (Oct 3 03:18).
- `kassa-olx.295503plid.picsviabtc.comicscards-compensatie-services.serveo.net` (+www variant, Oct 3 03:07 / Oct 1 03:27, Dutch OLX/ICS phishing).

Oct 1: `nab-internetbanking.serveo.net`, `nationalau-nab.serveo.net` (NAB = National Australia Bank), `neat3`, `exorior`, `nab`, `neco`, `nationalau-nab`, `neat1`, `nab-internetbanking` — **dictionary-word subdomains** (phishing-kit auto-deployment pattern).

Sep 30: `prive-aanvraagverwerking`, `prive-mijnvasco-aanvraagcontrole`, `prive-mijnvascocollectiemoment` (Dutch "private request processing / my-vasco"; Vasco = Belgian bank).

**Sep 28 submission burst (10:35–13:57 UTC, ~2.5 h):** `snsdigipas-verwerkcentrum` (SNS Bank digipas), `secure-optus-billing` (Optus Australia), `sucursalvirtualbancolombiapersonas` + `...dinamica` (Bancolombia), `servlinkedini` (LinkedIn), `etransferinter` (Interac e-Transfer Canada), `taskteam`, `sell`, `vace003`, `white` — ~10 phishing-named subdomains submitted in one window.

Targets span: Colombia (Bancolombia), Belgium/Netherlands (SNS, ICS, OLX, Vasco), Australia (NAB, Optus), Canada (Interac e-Transfer), Spain (SEUR), plus Facebook. Multi-brand, multi-country operator(s). Most resolved to serveo.net's own landing page at scan time (tunnels down by then, or redirect followed).

**Verdict:** highest-velocity phishing tunnel in the sweep. Naming grammar is brand-impersonation hyphenated names + dictionary words — human operator kit grammar, not agent test matrices. Not agent-shaped, but the Oct 4 `munero`/`recepi` pair (~2 min apart, identical `/login.html` path) shows automated deployment.

---

## Cross-cutting notes

- **Tag grammars observed:** `phishing`, `phishnet`, `hybridanalysis`, `sandbox-shell`, `@phish_report`, `malicious`. **No `uq*`-analogous operator tag grammar on any tunnel domain.**
- **Most programmatic pattern:** the Sep 10 zrok `/info` polling (6–8 s cadence, repeat sweeps hours apart) — dead-drop/rendezvous behavior.
- **Live right now (Oct 4–5):** Spanish credit-card phish (trycloudflare), "5k Instagram followers" (trycloudflare), `/login.html` pair on serveo (Oct 4). The zrok rotation died ~Oct 4.
- **Swarm scent verdict:** nothing matches our operator's grammar elsewhere, but the zrok 12-char share slugs are the closest structural analog (fixed-length random subdomains, rotating cadence) — a separate fleet using zrok rather than lhr.life.
- **Gaps:** (1) Matrix Leads Tool page body unpulled (fetch failed, not retried per system instruction). (2) urlquery.net unusable from this VM (all HTTPS egress times out); urlquery's keyless htmx endpoint may still work via `browser.open` (`https://urlquery.net/api/htmx/search/?...`) — not attempted this session. (3) serveo results older than Sep 28 partially skimmed; same shape as reported.

All times UTC as returned by urlscan.
