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

## COLLECTION GAP — VM egress outage

- 2026-10-05 ~04:55–05:20 UTC: ALL VM HTTPS egress stalled (proxy tunnel connects to hatch-egress-proxy:3128 but upstreams never respond; example.com also fails). `uq_htmx.py` CLI timeouts ×2, browser.open htmx endpoint returned HTTP 204 empty.
- Coverage gap: submissions from ~04:00 UTC onward are UNCOVERED. window2.json empty; retry loop armed to backfill when egress recovers.
- Note: the outage also blocks the Kalshi lanes and authenticated uq.py until resolved — the watchdog/live-monitor agents should confirm.

## Open threads

1. jmail.world: what is the site (compromised forum? spam SEO farm?), who runs the audit loop, and is the submitter an agent? The `seekers+of+decay` phrase is unidentified — possible investigation codename.
2. cachedview.nl as an agent fetch-proxy/oracle — first observed use in our hunts; worth adding to the infrastructure watchlist alongside r.jina.ai/translate.goog/allorigins.
3. htmx throttling under sustained querying — future sweeps should rotate query shapes and keep ≤1 req/5s.
4. Free-host kit farms (Appwrite 6ac31*, wasmer.app Ledger series, replit.app security-server series) — same hour, three services; check whether any share deployer fingerprints (report metadata, submission timing vs creation).
5. `sry2rqdnfgnl` campaign (ovou + qrch + tuiakehu) — watch for the slug family on other shorteners.
