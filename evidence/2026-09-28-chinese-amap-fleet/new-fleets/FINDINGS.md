# New-Fleet Hunt — Findings (2026-10-05)

**Task**: find UNDISCOVERED agent fleets on urlquery.net via the keyless htmx endpoint — clusters not previously seen. Excludes our known Amap/`uq` operator.
**Doctrine**: metadata tells the story — timestamps, burst timing, param grammars, infrastructure. Content secondary.

## Method

- Bulk recent-window pulls via `uq_htmx.py` (`http` queries @ offsets 0/50/100 → 122 unique reports, ~03:00–03:58 UTC window) plus targeted queries: `nonce=`, `task=`, `batch=`, `webhook.site`, `ngrok`, `eval`, `harness`, `appwrite.network`, `jmail.world`, `museum`, `qingdao`, `henan`.
- Clustering in `new-fleets/cluster.py`: per-minute bursts, per-host spans, nonce-like param grammars, epoch-like values, identical-URL repeats.
- Polite pacing (3–6s sleeps); later queries hit htmx throttling — noted as a collection constraint.

## FINDING 1 — jmail.world systematic audit (NEW CLUSTER, strong candidate)

**72 reports, 2026-10-04 23:54 → 2026-10-05 03:58 UTC, median inter-submission gap 3.0 min** — a metronomic 4-hour run.

**Metadata fingerprint:**
- Path grammar (site-namespace walk): `/thread/EFTA<N>` (21), `/drive/vol<N>-efta<N>-pdf` (21), `/thread/<hex32>` (9), `/thread/vol<N>-efta<N>-pdf` (6), plus `/person`, `/promotions/page/N`, `/topic/damage-control`, `/jotify/playlist/favorites`, `/search`
- `?q=` payloads — the site's own search being probed with: 5 known-bad redirect targets carrying affiliate IDs (`followlike.net/?r=19384926`, `livetraffic.net/login?refer=119334`, `2pink.org/dang-ky?ref=119334`, `followlike.info`, `folllike.com`) and the literal phrase `seekers+of+decay` (9×)
- 12/72 submissions wrapped as `cachedview.nl/#https://jmail.world/...` — viewing through the web-archive aggregator (Google cache/Wayback/archive.today), i.e. checking cached/indexed versions alongside live
- Person-directory walk includes odd entries (`ghislaine-maxwell`, `steven-sinofsky-`, `bin-sulayem-sultan-recovered`, `HOUSE_OVERSIGHT_023418` thread)

**Interpretation**: someone is systematically auditing jmail.world — a forum/drive-style site abused as a phishing-redirector farm — searching its own search box for known phishing-kit URLs and a watch-phrase, cross-checking live vs cached. This is a *detection/verification workload*, the inverse of our operator's collection workload.

**Agent-vs-human**: metronomic 3-min cadence sustained 4 hours through 00:00–04:00 UTC, systematic namespace coverage, no fatigue/deviation, fetch-proxy use (cachedview.nl as archive oracle). Strongly programmatic. AI-agent vs human's script is open — no per-request nonce/tag grammar from the submitter side (the grammar is the target site's own). Graded: **programmatic, likely automated; agent-plausible**.

**Novelty**: zero hits for `jmail.world` or `cachedview.nl` anywhere in our existing dataset. Not our operator (no `uq` grammar, no shared infra, different TTP family: audit/verify vs collect/exfiltrate).

**Raw**: `new-fleets/raw/jmail_world.json` (72 reports). Sample report IDs: `28369333`, `039562bf`, `171abb8b`, `782e73e3`, `0b4bd528`, `905fe4f1`, `78aa7359`, `d804ff55`.

**UPDATE 2026-10-05 ~13:00 UTC — STILL RUNNING (upgraded to strongest programmatic candidate):**
- Targeted pull `raw/jmail_now.json` (40 latest, 09:53 → 12:53 UTC): same path grammar (`/drive/vol00010-efta01432813-pdf`, `/thread/EFTA02608030`, `/drive/vol00011-efta02423778-pdf`, hex32 threads, `/person/...`), same `?q=` payload set (`seekers+of+decay`, livetraffic.net/folllike.com/followlike.info/2pink.org kit URLs), cachedview.nl wrapping continues (`cachedview.nl/#https://jmail.world/thread/a3875e449f5aa9f62eec1f0cf4dd4863?...` at 09:59).
- **Inter-arrival: median 3.0 min, mean 4.6, max 18 min over 3h at 12:53 UTC** — metronome intact across a full day. Combined span Oct-04 23:54 → Oct-05 12:53 UTC ≈ 13 hours (≈270+ submissions at this cadence).
- Coverage gap 03:58 → 09:47 UTC is unobserved (egress outage), but grammar + cadence on both sides match exactly — same loop.
- Verdict stands and hardens: **programmatic, likely automated; agent-plausible; detection/verification workload, inverse of our operator's collection workload.** Now the longest-lived unknown programmatic loop we've seen. Open thread #1 unchanged but escalated: identify `seekers+of+decay` and the audit's purpose.

**UPDATE 2026-10-05 ~13:10 UTC — gap backfilled (windows 8–16, 10:54→12:38 UTC, 665 reports, graded): audit ran CONTINUOUSLY through the gap (10:59, 11:05 … 12:38, same grammar, no break). Two upgrades:**
- **`seekers+of+decay` IDENTIFIED**: it is a public Pinterest urbex account — 5 scans in the gap across regional Pinterest frontends (`pinterest.mx/seekersofdecay/the-atlantic-wall-coastal-fortifications`, `.ca/seekersofdecayatlanticwall/regelbau-m270-wwii-coastal-gun-bunker`, `.hu/seekersofdecay/abandoned-stasi-bunker`, `.ie/seekersofdecayatlanticwall/regelbau-tobruk-...`, `.nl/seekersofdecay/abandoned-zoo` via wikiwix cache). WWII-fortification / abandoned-places photography account. The audit's `?q=seekers+of+decay` queries are searching jmail.world's own search for references to this account — i.e. the auditor is mapping jmail.world's link graph for references to known-bad redirect targets AND this external entity. Reframed: site-integrity / takedown-investigation audit of jmail.world, checking who/what links where. (Handle-level only — no human/operator pursuit per scope.)
- **Second archive oracle**: `archive.wikiwix.com/cache/?url=...` now wraps jmail.world (11:05, 11:11) and the pinterest.nl seekersofdecay board (11:16) — Wikiwix joins cachedview.nl in this operator's fetch-proxy toolkit. Same operator is auditing both surfaces against live + cached versions.
- Report IDs (gap): `5841e83c`, `c47160d8`, plus 11:16/11:11/11:05 wikiwix wrappers.

## FINDING 2 — ovou.com shortener series (weak candidate)

- `ovou.com/waenrakkhamwelaep1` → `waenrakkhamwelaep2` (03:19 → 03:33), plus `ovou.com/betweenstepsep2`, `/sry2rqdnfgnl`
- Numbered slug sequence (`ep1`, `ep2`, `step2`) suggests a series; Thai-lexicon slugs. Shortener used as phishing redirector layer.
- Too few data points for fleet verdict; noted as infrastructure to watch.

## FINDING 3 — "an*" .shop scam network (weak candidate)

- 5 shops sharing an `an*` prefix, each submitted twice (bare domain + trailing slash) within 1–2 min: `andcollaronline.shop`, `andarstore.shop`, `ancientwgo.shop`, `anbio.shop` (+ `angelostore.shop` ×1)
- The bare+slash pairing is a distinctive submission signature — looks like one actor's scanner checking redirect behavior, or paired analyst triage.
- Scam-shop takedown/monitoring workload, not clearly agent-shaped. Noted.

## FINDING 4 — appwrite.network `6ac31*` site series (infrastructure note)

- ~19 distinct `*.appwrite.network` subdomains scanned in 2h; 8 share a `6ac31` hex prefix (`6ac31d4a…`, `6ac31dbe…`, `6ac31be7…`, …) — one actor bulk-creating Appwrite Sites (free static hosting, phishing-kit favorite)
- The *scanning* is likely analyst triage; the *creation* side (programmatic site generation) is the agent-shaped part but isn't visible from urlquery.
- Connects to the known exploitgym/Appwrite tradecraft family as infrastructure context, not a new fleet.

## FINDING 5 — paralino.app / get-monai.app repeat scans (weak)

- `paralino.app` ×6, `www.get-monai.app` ×5, bare-domain resubmissions every 4–8 min — monitoring pattern (uptime/security watch or urlquery auto-rescan)
- Identity unresolved; no param grammar; not fleet-shaped. Noted only.

## Exclusions verified (known operator, not new)

- Amap `uqscan=` museum burst (qingdaomuseum/henanmuseum/wenzhou-museum) — known fleet, active.
- webhook.site dead-drop burst 03:15–03:19 (4 UUID inboxes, `?page=header3`, `?run=<epoch-ms>` via href.li) — 3/4 inboxes already in our dataset; same operator rotating dead-drops. One new inbox (`3b5027e4-…`) in the same session = same operator.
- `lhr.life`, `is.gd` operator slugs, IDPH/AIHW — none in the new-fleet windows.

## Clean negatives

- No second tag-grammar fleet (no `zz=`-style, no non-`uq` nonce params at fleet scale) in the sampled windows.
- `?nonce=`/`?task=`/`?batch=` queries returned background noise, no bursts.
- Epoch-like 10-digit values in URLs: zero in window sample.
- The per-minute "bursts" in the raw firehose (up to 10/min) are the global submission rate across diverse hosts — not single-operator bursts. True fleet signal required same-host + grammar + tight timing, which only jmail.world satisfied.

## FINDING 6 — Ledger-phish kit series on wasmer.app (moderate candidate, infrastructure)

- Three Ledger-wallet phishing subdomains on Wasmer Edge free hosting within 3 minutes:
  - `ledgerlogin-home.wasmer.app/` (03:28)
  - `ledgr-io-live-login.wasmer.app/` (03:30)
  - `secure-terezer-bridgge.wasmer.app/` (03:31)
- Same kit family (Ledger login phishing), same free-host, tight timing — one actor bulk-deploying kits on Wasmer. The *scanning* is likely analyst triage; the *creation* side (3 distinct subdomains in 3 min) is programmatic and agent-plausible.
- Same structural shape as FINDING 4 (6ac31* Appwrite bulk-sites): free-host phishing-kit farming. Two free-host farms now (Appwrite, Wasmer).
- Report IDs: `0d23a01d`, `04d2ffe1`, `2cbbc1e4`.

## FINDING 7 — ovou.com campaign links to qrch.net (upgrades FINDING 2)

- The exact slug `sry2rqdnfgnl` appears on BOTH `ovou.com/sry2rqdnfgnl` and `qrch.net/sry2rqdnfgnl` (03:43).
- Same slug across two shortener services = same operator cross-posting the same redirect campaign. ovou series (`waenrakkhamwelaep1→ep2`, `betweenstepsep2`, Thai lexicon) + qrch.net + `tuiakehu.com/event/yvhzxv` (random-slug event redirector, 03:42) look like one campaign using multiple shortener/redirector layers.
- Shortener-layer phishing distribution, not clearly agent-shaped; but cross-service slug reuse is a concrete operator link — now a trackable campaign.

## FINDING 8 — roblox.com.bn TLD-spoof phish (infrastructure note, campaign-shaped)

- `www.roblox.com.bn/games/76111710810728/NEW-Steal-A-Zoo?privateServerLinkCode=87969680078065820214840649414941` (03:33)
- `.bn` (Brunei ccTLD) spoof of roblox.com; "Steal-A-Zoo" knockoff of the viral "Steal a Brainrot" game; 44-digit privateServerLinkCode (authentic Roblox code format) — credential-theft lure aimed at kids.
- TLD-spoof + correct code-format grammar = deliberate campaign tradecraft. Single submission so far; watch for `.bn`/`.com.bn` roblox-spoof siblings.

## FINDING 9 — replit.app "security-server" phish-kit series (infrastructure note)

- Three Replit-hosted phishing subdomains, same `security-server` name family, randomized suffixes:
  - `security-server-landing-page--esusan870.replit.app/` (03:19)
  - `security-server-landing-page--d0cdrlve.replit.app/forgotpassword.html/` (03:19)
  - `security-server-website--resultbox63.replit.app/#tanelx@veltobox.net` (03:25)
- Hash-fragment email (`#tanelx@veltobox.net`) is classic phish-kit credential-drop marker. Same-name + random-suffix = programmatic bulk generation on Replit free tier.
- Third free-host kit farm in the same hour (Appwrite, Wasmer, Replit). Agent-plausible on the creation side.

## Minor infra notes (single submissions, same triage hour)

- `adeebsmit.github.io/fbloginpag` — GitHub Pages-hosted Facebook login phish (free-host kit family).
- `www.livetrustwalletsnycs.vercel.app/` + `livetrustwalletsnycs.vercel.app/` (03:19, 03:23) — bare+slash pair, crypto-wallet phish on Vercel; paired-submission signature per FINDING 3.
- `arpranindustries.com/internet-banking.dbs.com.sg/` — DBS Bank (Singapore) phishing path on compromised/lookalike domain.
- `myconnectfile.sbs` ×2 (03:37 bare, 03:39 with `fc-26-coins-generator/hack/fc-26-hack/...` path) — FC 26 coin-generator gaming scam on .sbs.
- `app.asana.com/0/account_setup` (03:38) — legit Asana; likely analyst checking a suspicious account-setup link.
- `app.miescoleta.com` (03:33) — bare domain, no path; unresolved, noted.

## FINDING 10 — email/phish link-deconstruction TTP (analyst triage, same hour)

Three separate same-minute same-host link deconstructions on 2026-10-05 — someone breaking apart phishing-email tracking links:
- `zoominfo.sjc1.qualtrics.com` ×3 (10:07): `/subscription/manage/confirmation?recipientId=CGC_Hxt14jhzuY6qmpf...`, `/subscription/watermark.gif?UID=UR_5uPaE1aGInMSMC2&EMD=...`, `/jfe/form/SV_8jqSRNmPe3AEG58?Q_DL=2DrJy2zBB9w2AaY_...` — one phishing email's three links submitted within one minute.
- `vero-suomiii-finlands.com` ×4 (12:52): two base64-path token families (`/e/9zahB/r9/4fIrQ+DPNLEa7FEB65Bykq2/...`, `/e/gSgzlMhMMkBEViI/s1AiwEUGWPayfsvbJ+WudvMq3Oo=/`), each submitted in raw AND URL-encoded form — paired decode-probing (same signature as FINDING 3's bare+slash pairs). Finnish tax-authority ("vero") phish.
- `trackingservice.monday.com/tracker/link?token=eyJhbGciOi...` (12:47) and `track.pstmrk.it/3s/direct.me%2Fmbpinfo/...` (10:30) — Monday/Postmark email-tracker link deconstruction.
- Report IDs: `b0303208`, `567150aa`, `0f6439c4`, `9d7851c7` (zoominfo trio); `6dcd5969`, `a0d6ed56`, `23807add`, `9dbe426c` (vero-suomiii); `37c6f177`, `5d05b2d3`.
- Graded: analyst triage workload, not fleet-shaped (no programmatic cadence, one-shot bursts). But the *paired raw/encoded* submission signature is a repeatable operator TTP — worth clustering on.

**UPDATE 2026-10-05 ~13:10 UTC — vero-suomiii is a NORDIC FINANCIAL PHISH CAMPAIGN (upgraded from triage note):**
- 12 more reports in the gap (11:17 → 12:39), path grammar deepens: `/NORDEA/approve/`, `/provider/NORDE?conversation=e2s1&tid=sg0sbeb8l9s50eem2j3mr2e5lk&pid=3` — **Nordea (Nordic bank) impersonation** alongside the Vero (Finnish tax authority) lures; tokenized `/e/<base64-pair>/` redirect paths, raw+encoded submission pairs continue (`6ca05b38`, `f2fb460a`, `4f6681b2`, `64e51684`, `8db76a17`, `22d6fb05`-adjacent `zeynmoda.shop`, `d6ae3cb0`, `166929bb`, `79320efb`, `d6ae3cb0`).
- Sustained multi-hour submission pattern by (likely) one actor deconstructing the kit's redirect chains. Still analyst-triage-shaped, but the kit itself is an active Nordic banking/tax phish operation — campaign-grade infrastructure, watch for sibling domains.

## FINDING 11 — mailer* `_amazan_oxy` kit family (campaign link)

- `mailer500.remnorth.top/_amazan_oxy/?login=google@google.com&page=null&request_type=null...` (09:55) and `mailer400.osmoxa.online/nit/index.php?login=Z29vZ2xlQGdvb2dsZS5jb20=&page=null&request_type=null...` (09:52)
- Same kit path grammar (`_amazan_oxy`, `nit/index.php`, `?login=` base64-of-email + `&page=null&request_type=null`), sequential numbered mailer domains (`mailer400`, `mailer500`) on throwaway TLDs (`.top`, `.online`). Credential phish kits.
- Same-operator kit farm; numbered-series infrastructure to watch (mailer<N>.*).

## Infrastructure extensions (12:45–12:52 UTC window, window7.json)

- Appwrite farm families continue: `6ac38044a33e1` / `6ac380d4d7d7a` routertest.stage.appwrite.network (new hex prefixes in the 6ac37*/6ac38* series from FINDING 4), plus `my-website-e0o6`, `pfpzone`, `branch-armonia-corretta-1e1dda8`. Fourth free-host kit farm: `kalntopup-live.admin-kalnproject.workers.dev` (Cloudflare Workers topup scam).
- `saxotrader.com` ×2 same-minute bare submission (10:0x) — paired signature per FINDING 3.
- `jn19.vip/DHOpHROFEukpDS1oUNgHEHMOODtPND.html` (10:30) — random-slug path redirector, same shape as F7's `tuiakehu.com/event/yvhzxv`.
- `amazon-partnership.corp-internal.org/8ee1806a87?l=5` (09:48) — corp-internal.org lookalike, single.
- `www.eg5scfyzp5.2225567xindhxlu.top/` (12:49) — random hex-subdomain scam TLD.
- `agent-control.net/agents` (12:48) — RESOLVED non-fleet: legit MCP agent-payments control-plane product (Cobra-bit-prog/agent-guard); someone checking agent infrastructure. Noted only.
- `paralino.app` / `www.get-monai.app` repeat monitoring (F5) continues through 10:52.
- Global submission rate now ≈14/min (window7: 96 reports over 7 min; 10:48–10:52 sustained 16–22/min bursts of diverse hosts). These diverse-host bursts are bulk-queue dumps, not fleet-shaped (no same-host + grammar + tight timing), but the rate exceeds the previously noted ~10/min.

## Infrastructure extensions (gapfill windows 8–16, 10:54–12:38 UTC)

- Appwrite farm families continue: `6ac39983b2e440f0bced` (12:38), `6ac3907a1cd04616606d` (11:59), `6ac3855611a7357fcb81` (11:16), `6968112f0013f79a5285` ×2 paired (11:19); CI-branch triage (`branch-feat-web-device-2937013-*`, `branch-main-7867e15`, `branch-android-r8-relea-*`, `branch-edutoks-*`) persists — dev-workflow triage, not phish-farm.
- `dai.ly/xbicpie` (11:38) + `dai.ly/xbicpzu` (11:39) — short-slug pair on Dailymotion's shortener, 1 min apart — campaign-shaped series.
- `ro.blox.com/Ebh5` (12:26) — Roblox lookalike short path; joins F8's `.bn` TLD-spoof watch (roblox-spoof family).
- `grup-bokep-sma.duckdns.org/` (11:42) — duckdns dynamic-DNS abuse.
- `jenkins.agilefabric.fr.carrefour.com` (12:25) — exposed Jenkins on a Carrefour subdomain (single; infra exposure note).
- `secops-cencosud.backstory.chronicle.security/alert` (12:39) — Google Chronicle alert link (analyst triage).
- `url.uk.m.mimecastprotect.com/s/onCGCrELQF802VYVhNu6Os47WYV?domain=us.list-manage.com` (11:31) — Mimecast link deconstruction (F10 TTP).
- `scholia.io` ×2 (11:52) — paired submissions.
- `www.onlineintegrityservices.com/c/c37b2591adba0857?bbg=__BBG__&sub1=__CAMPAIGN_NAME__...` (12:25) — affiliate-tracking template deconstruction.
- Elevated per-minute burst rate sustained through the whole gap (15–23/min diverse-host dumps at 11:36–11:42, 12:25–12:40) — the firehose is running hotter than the previously noted ~10/min baseline.

## FINDING 12 — "TronZap" PHP-RCE recon + tunnel payment-phish staging (SEPARATE CAMPAIGN, crimeware-adjacent)

**Routed from farmable-surfaces respawn sweep (2026-10-05 ~12:55 UTC).** urlscan-only — zero hits on urlquery for `tronzap`. 405 urlscan results, span 2026-09-26 16:49 → 2026-09-29 07:33 UTC.

**What it is:** a systematic vulnerability-probing session against TronZap (TRON-energy rental payment service, dappradar-listed, legit) plus lhr.life tunnels staging TronZap-impersonating payment-flow pages.

**Recon grammar (classic PHP/Laravel RCE toolkit), Sep-26 16:49–18:27 UTC:**
- RCE probes: `vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php` (CVE-2017-9841 PHPUnit eval-stdin) incl. **homoglyph bypass** `phpun%C4%B1t` (U+0131 dotless-i, WAF-evasion tradecraft), `_ignition/execute-solution` (CVE-2021-3129 Laravel Ignition RCE), `cgi-bin/eval-stdin.php` ×5 in 2 min (18:10), `index.php?-s` / `?%2Ds` (PHP source disclosure)
- Exposure probes: `.git/config`, `composer.json`, `composer.lock`, `vendor/composer/installed.json`, `phpinfo.php`, `test.php`, `_debugbar/open`, `_debugbar/clockwork`, `__clockwork`, `clockwork/app`, `vendor/filp/whoops`, `pulse`, `horizon/api/stats`, `build/manifest.json`, `@vite/client` (dev-server exposure), `public/storage`, `storage/app/public`, `/up`, `/up.json`, `/health`, `/healthz`, `/ready`, `/fpm-status`, `/nginx_status`, `/server-status`
- API surface: `api.tronzap.com` v1/orders, /orders/calculate, /orders/check (matches documented TronZap API: calculate/create_energy_transaction/check_transaction); `dash.tronzap.com` Livewire dashboard (livewire/update, /login)
- **Second session Sep-29 05:52–07:33:** dev-subdomain enumeration (`dev.`, `dev-api.`, `dev-dash.`, `dev-bo.`, `devbo.`, `ref.`, `bo.`, `mock.`)

**Tunnel component (lhr.life, same window):** cloned TronZap payment-flow pages — `ba85c283a8f9e0/calc3.html,calc4.html,calc.html,ig.html,lw.html,cancel.html`; `90c6961dd9eba0/app.html ×2,quote2.html`; `d789d4fd5debd8/chk.html,chk2.html`; `3be663c0dc1827/chk2.html`. Plus an **SSTI-probe cluster** on `52949a80bf53fc`: `k-ext-ssti`, `c-rc-php`, `o-rc-dollar`, `o-rc-php`, `o-rc-semi`, `c-rc-mustache`, `k-ext-semi`, `c-energy`, `o-rc-nl` (18:12–18:16) — template-engine injection test grammar. Plus enumeration probes `d51842b87c3e80/e0,e1,e3,e4.html` at 1s cadence, `ev/ev2.html`.

**Grade:** NOT our operator (zero uqscan/tag grammar; different TTP family entirely — PHP RCE vuln-scanning + payment-phish staging). **Separate campaign: targeted recon of a crypto payment service, crimeware- or red-team-shaped.** Two live hypotheses: (a) pre-exploitation recon by an attacker, with phish-kit staging on tunnels; (b) security-researcher assessment (public disclosure may follow). Not agent-fleet-shaped by our metadata markers (no nonce/tag grammar, no metronome cadence — speed is scanner-speed, not metronome-speed; programmatic recon, not a fleet). **Misfit recorded as a lead, never a negative.**
- Watchlist additions: tunnel subdomains `ba85c283a8f9e0`, `90c6961dd9eba0`, `d51842b87c3e80`, `52949a80bf53fc`, `d789d4fd5debd8`, `3be663c0dc1827` (all lhr.life — shared infra with our operator, different tenant); probe signatures `eval-stdin.php`, `_ignition/execute-solution`, `phpun%C4%B1t` homoglyph, `-s` source-disclosure — worth sweeping urlscan/urlquery for recurrence.
- Caveat: submitter identity unverifiable from search-level data (urlscan result-detail API now login-gated); "same API submitter session" per farmable-surfaces is search-heuristic, not confirmed.
- Cross-surface: urlquery 0 hits — campaign is urlscan-API-native. urlscan search is 30-day-windowed; re-sweep after Oct-26 to catch recurrence.

## COLLECTION GAP — new-fleets agent died ~10:52 UTC — RESOLVED

- 2026-10-05 ~10:52 → 12:45 UTC gap BACKFILLED via `collect_gapfill2.sh` (done 13:02:26Z): `http` @ offsets 150–1350, limit 96 → `raw/window8..16.json` + `analysis-8..16.txt` (665 reports, 10:54–12:38 UTC), graded into FINDINGS 1/10/12 updates + infra extensions above. Log `raw/gapfill2.log`.
- Covered before the death: window3 (47, 09:46–09:50), window4 (96, 09:50–10:11), window5 (23, 10:30–10:32), window6 (71, 10:48–10:52), graded into FINDINGS 10/11 + infra extensions. cluster.py fixed to accept `{"reports": [...]}` envelope (prior analyses 3–6 had crashed on it).
- Note: retry_loop.sh now continues from the next free window index instead of overwriting window3 (prior runs clobbered graded windows).

## COLLECTION GAP — VM egress outage (earlier)

- 2026-10-05 ~04:55–05:20 UTC: ALL VM HTTPS egress stalled (proxy tunnel connects to hatch-egress-proxy:3128 but upstreams never respond; example.com also fails). `uq_htmx.py` CLI timeouts ×2, browser.open htmx endpoint returned HTTP 204 empty.
- Coverage gap: submissions from ~04:00 UTC onward are UNCOVERED. window2.json empty; retry loop armed to backfill when egress recovers.
- Note: the outage also blocks the Kalshi lanes and authenticated uq.py until resolved — the watchdog/live-monitor agents should confirm.

## Open threads

1. jmail.world: what is the site (compromised forum? spam SEO farm?), who runs the audit loop, and is the submitter an agent? The `seekers+of+decay` phrase is unidentified — possible investigation codename.
2. cachedview.nl as an agent fetch-proxy/oracle — first observed use in our hunts; worth adding to the infrastructure watchlist alongside r.jina.ai/translate.goog/allorigins.
3. htmx throttling under sustained querying — future sweeps should rotate query shapes and keep ≤1 req/5s.
4. Free-host kit farms (Appwrite 6ac31*, wasmer.app Ledger series, replit.app security-server series) — same hour, three services; check whether any share deployer fingerprints (report metadata, submission timing vs creation).
5. `sry2rqdnfgnl` campaign (ovou + qrch + tuiakehu) — watch for the slug family on other shorteners.
