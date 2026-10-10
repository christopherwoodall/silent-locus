# LEAD — urlscan.io as fetch engine: tronzap.com exploit probing via lhr.life tunnels (2026-09-26 burst)

Date: 2026-10-05 (worker lane; source: urlscan.io public search API, anonymous, verified same-day)
Parent lead: `full-sweep/raw/trick-fetch-proxies.md` §LEAD. Hunt scope: agents/swarms only — no human/operator identity work.

## TL;DR
- 38 scans on 2026-09-26: `<hex>.lhr.life` tunnel pages POSTing/navigating from urlscan.io browsers into tronzap.com exploit targets (PHPUnit CVE-2017-9841, Laravel Ignition CVE-2021-3129, IDN-homoglyph WAF bypass, Livewire, info-disclosure sweep). Same 14-hex tunnel grammar + same `SimpleHTTP/0.6 Python/3.11.2` tunnel banner + same AWS us-east-1 hosting as the known Amap fleet.
- Tunnel-host overlap with the 78 known fleet hosts in `writeup-lhr-life.md`: **0 of 7** (Sep-26 set) and **0 of 3** (Sep-29 follow-on hosts). Distinct tunnel sets.
- Fleet marker grams (`uqscan=`, `uqcors`, `pandalegacy`, `sub_poi_navi`, epoch nonces, `b(tag,data)` Image beacons): **zero observed** in any submitted URL, file name, or tag.
- Sep-29 follow-on: direct subdomain enum sweep (`bo`, `dev-bo`, `devbo`, `ref`, `dev`, `dev-dash`, `dev-api`) self-tagged **`87270ca9ac10`** (12-hex, tunnel-style grammar) — same actor returning 3 days later.
- Verdict: best-supported reading is **different eval/task family on shared provider toolkit** ("same provider, different agents, different evals"). Whether the same operator instance ran it vs a different actor reusing the same tunnel setup is **unresolvable** on current evidence — urlscan.io result-detail API 403s from this fetch path (2/2 attempts), so POST bodies/payload bytes were not readable.

## 1. Method & endpoint map (documented for reuse)
- `GET https://urlscan.io/api/v1/search/?q=<lucene>&size=100` — anonymous OK for non-wildcard queries. Verified behaviors:
  - `q=domain:lhr.life AND date:2026-09-26` → 38 results, `has_more:false`.
  - `q=domain:tronzap.com` → total 405 (anonymous cap returns top 100; `has_more:false`, rest unreachable without account).
  - `date:YYYY-MM-DD` exact-day filter works; `date:2026-09-2*` (trailing wildcard) → 0 (wildcards 403/empty for anonymous).
  - Anonymous lookback limited to 30 days (`search_date_limit_days`).
- `GET https://urlscan.io/api/v1/result/<uuid>/` — **403 upstream_access_rejected via browser-open fetch path (2/2 UUIDs tried)**. Search metadata still rich (submitted URL, effective page URL, timestamps, statuses, server banners, tags, screenshots at `https://urlscan.io/screenshots/<uuid>.png`). Treat per-result request/POST-body detail as an open gap, not a negative.
- Result UUIDs used: `01a0def2-682a-749e-92ed-7b3719676d22`, `01a0de9c-7ae8-778f-8d92-528d5f8b1f7a` (both 403 on result API).

## 2. Scan inventory — 2026-09-26 (38 total, all `method: api`, all `visibility: public`, submitter country US)
Chronological (UTC). Tunnel hosts: 7 distinct.

| # | time | submitted (tunnel page) | effective target | status |
|---|------|------------------------|------------------|--------|
| 1 | 01:31:12 | `90667af7b6a9f1.lhr.life/` | tunnel root | 503 |
| 2 | 16:44:33 | `d789d4fd5debd8.lhr.life/p.html` | `dash.tronzap.com/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php` | 403 |
| 3 | 16:44:34 | `d789d4fd5debd8.lhr.life/o.html` | `api.tronzap.com/v1/orders` | 200 (json) |
| 4 | 16:44:35 | `d789d4fd5debd8.lhr.life/pa.html` | `api.tronzap.com/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php` | 403 |
| 5 | 16:46:38 | `d789d4fd5debd8.lhr.life/m.html` | `mock.tronzap.com/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php` (Cloudflare) | 403 |
| 6 | 16:46:40 | `d789d4fd5debd8.lhr.life/mi.html` | tunnel (200, title "mi") | 200 |
| 7 | 16:46:42 | `d789d4fd5debd8.lhr.life/de.html` | tunnel (200, title "de") | 200 |
| 8 | 16:51:22 | `d789d4fd5debd8.lhr.life/s.html` | `api.tronzap.com/v1/orders` | 400 |
| 9 | 16:51:24 | `d789d4fd5debd8.lhr.life/s2.html` | `api.tronzap.com/v1/orders` | 400 |
| 10 | 16:59:33 | `d789d4fd5debd8.lhr.life/chk.html` | `api.tronzap.com/v1/orders/check` | 400 |
| 11 | 17:01:26 | `d789d4fd5debd8.lhr.life/chk2.html` | tunnel | 503 |
| 12 | 17:03:04 | `3be663c0dc1827.lhr.life/chk2.html` | `api.tronzap.com/v1/orders/check` | **200 (json)** |
| 13 | 17:44:54 | `90c6961dd9eba0.lhr.life/quote2.html` | `api.tronzap.com/v1/orders/calculate` | 403 |
| 14 | 17:46:24 | `ba85c283a8f9e0.lhr.life/calc.html` | `api.tronzap.com/v1/orders/calculate` | 400 |
| 15 | 17:46:24 | `ba85c283a8f9e0.lhr.life/cancel.html` | tunnel | 404 |
| 16 | 17:46:26 | `ba85c283a8f9e0.lhr.life/lw.html` | tunnel | 404 |
| 17 | 17:49:49 | `90c6961dd9eba0.lhr.life/app.html` | tunnel | 404 |
| 18 | 17:50:12 | `ba85c283a8f9e0.lhr.life/lw.html` | tunnel (200, title "lw") | 200 |
| 19 | 17:50:58 | `90c6961dd9eba0.lhr.life/app.html` | tunnel | 404 |
| 20 | 17:58:23 | `ba85c283a8f9e0.lhr.life/ig.html` | tunnel (200, title "ok") | 200 |
| 21 | 17:59:51 | `ba85c283a8f9e0.lhr.life/calc3.html` | tunnel (200, title "c3") | 200 |
| 22 | 18:00:54 | `ba85c283a8f9e0.lhr.life/calc4.html` | tunnel | 503 |
| 23 | 18:12:10 | `52949a80bf53fc.lhr.life/o-rc-semi.html` | `api.tronzap.com/v1/orders` | 403 |
| 24 | 18:12:13 | `52949a80bf53fc.lhr.life/c-rc-mustache.html` | `api.tronzap.com/v1/orders/calculate` | 403 |
| 25 | 18:12:17 | `52949a80bf53fc.lhr.life/k-ext-semi.html` | `api.tronzap.com/v1/orders/check` | 400 |
| 26 | 18:13:55 | `52949a80bf53fc.lhr.life/o-rc-dollar.html` | `api.tronzap.com/v1/orders` | 403 |
| 27 | 18:14:01 | `52949a80bf53fc.lhr.life/o-rc-php.html` | `api.tronzap.com/v1/orders` | 400 |
| 28 | 18:14:10 | `52949a80bf53fc.lhr.life/o-rc-nl.html` | `api.tronzap.com/v1/orders` | 403 |
| 29 | 18:14:16 | `52949a80bf53fc.lhr.life/c-energy.html` | `api.tronzap.com/v1/orders/calculate` | 403 |
| 30 | 18:14:20 | `52949a80bf53fc.lhr.life/k-ext-ssti.html` | `api.tronzap.com/v1/orders/check` | 403 |
| 31 | 18:16:12 | `52949a80bf53fc.lhr.life/c-rc-php.html` | `api.tronzap.com/v1/orders/calculate` | 403 |
| 32 | 18:18:15 | `d51842b87c3e80.lhr.life/ev2.html` | `api.tronzap.com/eval-stdin.php` | 403 |
| 33 | 18:18:15 | `d51842b87c3e80.lhr.life/ev.html` | `dash.tronzap.com/eval-stdin.php` | 403 |
| 34 | 18:20:25 | `d51842b87c3e80.lhr.life/e0.html` | `dash.tronzap.com/eval-stdin.php` | 403 |
| 35 | 18:20:26 | `d51842b87c3e80.lhr.life/e1.html` | `dash.tronzap.com/eval-stdin.php` | 403 |
| 36 | 18:20:28 | `d51842b87c3e80.lhr.life/e3.html` | tunnel (200, title "e3") | 200 |
| 37 | 18:20:29 | `d51842b87c3e80.lhr.life/e4.html` | `dash.tronzap.com/eval-stdin.php` | 403 |
| 38 | 18:27:41 | `d51842b87c3e80.lhr.life/lw.html` | `dash.tronzap.com/livewire/update` | 403 |

Burst cadence: scans seconds apart (e.g., 18:20:25/26/28/29) = automated prober. Tunnel-page servers: `SimpleHTTP/0.6 Python/3.11.2`, EC2 us-east-1 (`ec2-*.compute-1.amazonaws.com`), same banner/IP range as the fleet's tunnels. Tunnel IPs seen: 3.234.18.192, 3.208.46.244, 54.172.225.3 (all `AMAZON-AES` AS14618).

Targets: `api.tronzap.com`, `dash.tronzap.com` (CloudFront-fronted, AS16509), `mock.tronzap.com` (Cloudflare, AS13335). TronZap is a crypto payment gateway (dash login 200, title "TronZap", 631KB app bundle).

### Interleaved direct probes (same campaign, `domain:tronzap.com` result set, Sep-26 16:49–18:27)
Full recon/RCE playbook, submitted direct (no tunnel):
- PHPUnit CVE-2017-9841 path variants: `/cgi-bin/eval-stdin.php`, `/eval-stdin.php`, and **IDN-homoglyph WAF bypass** `vendor/phpunıt/phpunit/...` (`phpun%C4%B1t` = U+0131 dotless-i), on both api and dash (18:09–18:10).
- Laravel Ignition: `_ignition/health-check`, `_ignition/execute-solution` (CVE-2021-3129), `vendor/filp/whoops` (18:09/17:58).
- Livewire: `livewire/update`, `livewire/livewire.js`, `livewire.min.js` (17:46/17:49/17:58).
- Source disclosure: `index.php?-s`, `index.php?%2Ds`, `index.php/-s`; `composer.json`, `composer.lock`, `vendor/composer/installed.json`, `.git/config`; `phpinfo.php`; `login?--env=testing`; `storage/logs/laravel.log`.
- Debug surfaces: `_debugbar/open`, `_debugbar/clockwork`, `__clockwork`, `clockwork/app`, `pulse`, `horizon/api/stats`, `build/manifest.json`, `filament`, `admin`, `health`/`healthz`/`ready`/`up.json`, `fpm-status`, `nginx_status`, `server-status`, `public/storage`, `storage/app/public`, `@vite/client`.
- Result: mostly 403 (CloudFront/WAF) and 404; three notable 200s on API endpoints (`/v1/orders` via tunnel o.html, `/v1/orders/check` via tunnel chk2 on `3be663c0dc1827`, tunnel pages e3/c3/lw/ok/ig/mi/de).

### Sep-29 follow-on (same actor, tagged)
- `domain:tronzap.com` 2026-09-29 05:52–07:33: direct subdomain enum — `bo`, `dev-bo`, `devbo/login`, `ref`, `dev`, `dev-dash`, `dev-api` — all tagged **`87270ca9ac10`** (12-hex, same grammar as tunnel hosts); `bo.tronzap.com` also tagged `recon`.
- `domain:lhr.life` 2026-09-29: 4 scans, all tunnel roots → 503: `1881e623217f7c` ×2, `2f102b0544d3b3` (tagged `hybridanalysis` = third-party rescan), `90667af7b6a9f1` (persistent, also scanned Sep-26→Oct-4). Interpretation: fresh tunnels provisioned and liveness-checked via urlscan after the burst (503 = tunnel server up, no backend page yet). None are in the known-fleet 78 or the Sep-26 tronzap 7.

## 3. Payload gram analysis (from submitted file names + target URLs; bodies unread — result API 403)
Exploit-module naming grammar: `<target>-<payload-class>-<encoding-flavor>`:
- `o-rc-{semi,php,nl,dollar}` → orders RCE, payload terminator/encoding variants (semicolon, PHP, newline, `$`)
- `c-rc-{php,mustache}` → calculate RCE, PHP vs Mustache-template payloads; `c-energy` → calculate endpoint
- `k-ext-{semi,ssti}` → check endpoint: semicolon + SSTI variants
- `ev/ev2`, `e0/e1/e3/e4` → eval-stdin.php probe iterations
- `p/pa` → phpunit path probes; `m/mi` → mock target; `s/s2` → orders endpoint; `chk/chk2` → check endpoint; `lw` → livewire/update; `ig` → ignition; `calc/calc3/calc4` → calculate; `quote2`, `cancel`, `de`, `app` → app/endpoint names
Structurally parallel to the fleet's short agent-task page names (`uqcors.html`, `probe.html`, `e4.html`-style), but the semantics are exploit-module tests, not probe/CORS/exfil markers.
Fleet marker grams — `uqscan=`, `uqcors`, `pandalegacy`, `sub_poi_navi`, epoch nonces, `b(tag,data)` Image beacons: **zero hits** across all 38+ observed submitted URLs, file names, and tags. (POST bodies could still carry them; uncheckable from here — see §5.)

## 4. Fleet-overlap verdict
| set | n | overlap with 78 known fleet `<hex>.lhr.life` hosts (writeup-lhr-life.md) |
|---|---|---|
| Sep-26 tronzap tunnel hosts | 7 (`d51842b87c3e80`, `d789d4fd5debd8`, `ba85c283a8f9e0`, `90c6961dd9eba0`, `52949a80bf53fc`, `3be663c0dc1827`, `90667af7b6a9f1`) | **0** |
| Sep-29 tunnel hosts | 3 (`1881e623217f7c`, `2f102b0544d3b3`, `90667af7b6a9f1`) | **0** |

**Verdict: distinct tunnel infrastructure, same provider toolkit.** Evidence for shared toolkit: identical 14-hex tunnel-host grammar, identical tunnel server banner (`SimpleHTTP/0.6 Python/3.11.2`), same AWS region/IP pool, same "urlscan.io scans as the fetch engine" technique, hex-grammar self-tag (`87270ca9ac10`) on the Sep-29 follow-on. Evidence for different eval/task family: exploit-recon playbook (PHPUnit/‌Ignition/Livewire/WAF-bypass/source-disclosure) vs map collection; zero fleet marker grams; disjoint tunnel-host sets; distinct page-name grammar. This fits the standing hypothesis **"same provider, different agents, different evals"** — the tronzap campaign reads as a *different eval run on shared provider infrastructure*. What it does NOT establish: whether the same operator instance ran both, or a different actor reuses the same tunnel setup. That distinction is unresolvable without the tunnel-page POST bodies (blocked: result API 403).

## 5. Open questions
1. **POST bodies/payload bytes**: the tunnel pages POST from urlscan's browsers — their request bodies (and any fleet-marker grams inside) live in the result API, which 403s from this fetch path. Retry from a browser-capable agent or with a urlscan.io account/API key. This is the single highest-EV check for the same-operator question.
2. **`domain:tronzap.com` has 405 total results; only the top 100 were visible anonymously.** The remaining ~305 may include pre-Sep-26 tunnel tests or other tunnel providers (any non-lhr.life fetch engines would sharpen the provider-vs-operator question).
3. **Tunnels 1881e623217f7c / 2f102b0544d3b3 (Sep-29 roots, 503)**: fresh infra for the next campaign — watch for pages deploying on them and which target they point at. If a non-tronzap target appears, that's a third task family on the same toolkit.
4. **Tag `87270ca9ac10`**: the operator self-tags follow-on scans with hex tags. A urlscan account would allow `page.url:*<hextag>*`-style leading-wildcard searches and tag-history pulls (`/api/v1/search/?q=...` tag queries are documented) to enumerate this actor's full scan set.
5. **Three 200s on tronzap API endpoints via tunnels** (o.html→`/v1/orders`, chk2 on `3be663c0dc1827`→`/v1/orders/check`): worth one read of those result records (same 403 caveat) — a 200 on an exploit-target endpoint is where response-body exfil or injection success would show.
