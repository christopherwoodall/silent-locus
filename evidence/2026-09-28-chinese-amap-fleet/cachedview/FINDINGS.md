# cachedview.nl Deep Scan — Findings (2026-10-05)

**Trigger:** the new-fleet hunt found a programmatic auditor routing urlquery submissions through cachedview.nl (a web-archive aggregator) while auditing jmail.world — a possible new agent-harness infrastructure class: **archive-oracle-as-fetch-proxy**.

**Method:** 7 parallel lanes (service recon, urlquery mining, urlscan mining, sibling services, tradecraft research, jmail.world follow-up, attribution-shape). Doctrine: metadata tells the story; misfits are leads; agents and swarms only.

---

## 1. What cachedview.nl is

Dutch web-archive aggregator / availability checker. One search box; renders per-source cards (HTTP status + deep link to nearest snapshot). **Doubles as a server-side fetch proxy** via `/api/LIVEVERSION/<url>`.

**Aggregated sources** (from live frontend `index.js` + recovered TypeScript sourcemap): Wayback Machine, Archive.today, Perma.cc, Library of Congress, Live Version (server fetches target directly), server-side screenshot. No Arquivo.pt, Common Crawl, Megalodon, or Google cache in current build. Operator unattributed (only signal: self-hosted Matomo at `analytics.floris.amsterdam`).

**Undocumented endpoints** (base `https://cachedview.nl/api`, all GET, no auth — verified live):
- `GET /api/{ARCHIVEAPI|LIVEVERSION|PERMACC|ARCHIVETODAY|LIBRARYOFCONGRESS}/{urlencoded-target}` → JSON `{statusCode, urlUsed, error, protocolUsed}`. LIVEVERSION verified against example.com → 200.
- `GET /api/screenshot/{urlencoded-target}` → base64 PNG.

**URL grammar:** `https://cachedview.nl/#<target-url>` (hash fragment; legacy `/?url=` still serves SPA).

**Public lookup history:** none on-site — but the **Wayback CDX index is a de-facto public lookup log**: `web.archive.org/cdx/search/cdx?url=cachedview.nl/api/*&matchType=prefix` → **1,504 API captures / 354 distinct target domains**, including the jmail.world lookup (2026-07-30) and `Jeffrey.Epstein.urlquery.net` search lookups.

---

## 2. Who uses cachedview.nl (urlquery: 1,440 reports, >96% coverage)

Only **two clusters** exist in the entire corpus. Every URL shares one grammar: `cachedview.nl/#<target-url>`.

### Cluster 1 — jmail.world auditor: 1,346 reports
- **Window:** 2026-09-03 → 2026-10-05, every single day (6–70/day). Median inter-arrival **19 min**, spread across all 24 UTC hours. No tight bursts.
- **Targets:** 1,092 unique paths — `/thread` 574, `/drive` 449, `/person` 205, `/promotions` 26, `/page` 23, `/jikipedia` 17, `/sent` 17, `/jacebook` 11, `/messages` 9, `/calendar` 5, `/document` 4, `/topic` 2, `/jotify` 2, `/jamazon` 1, `/attachments` 1. The `/person` index re-checked 65× (watch target).
- **ID grammars:** `EFTA########` (251), md5hex (190), `vol#####-efta########-pdf` (121), `HOUSE_OVERSIGHT_######` (13), `COURT_giuffre-*`, `doj-*.pdf`.
- **q-canary grammar:** EVERY submission appends `?q=` cycling a fixed 6-value set: `followlike.info/?r=19384926` (253), `2pink.org/dang-ky?ref=119334` (250), `folllike.com/?19384926` (229), `followlike.net/?r=19384926` (215), `seekers+of+decay` (200), `livetraffic.net/login?refer=119334` (199).
- **Verdict: agent/swarm-shaped** — 24/7 drip, fixed canary rotation, systematic multi-family coverage, 32-day persistence.

### Cluster 2 — Pinterest "Seekers of Decay" footprint audit: 94 reports
- **Window:** 2026-09-22 → 2026-10-05. 63 board/pin lookups + 31 searches, all `q=Regelbau` (WWII bunker standard), swept across **33 Pinterest ccTLDs**.
- **Same-actor link:** runs in parallel with the jmail run from Sep 22; `seekers+of+decay` is one of the jmail canaries. "Seekers of Decay" is an urbex photographer — this is **brand-footprint monitoring** (jmail mentions + Pinterest per locale).
- **Verdict: programmatic cadence, human-shaped motive** — reputation/SEO audit, not swarm tradecraft.

**Gaps:** tail page (≤50 oldest reports) + `cachedview` variant query blocked by urlquery throttling.

---

## 3. urlscan.io: honest negative + a second operator

- **cachedview.nl: 1 hit** — incidental. A blogspot SEO/traffic-exchange page iframing cachedview.nl via `traffic-exchange.github.io` scripts. Zero proxy/fetch usage, zero agent-shaped clusters. `cachedview.com`, `cached.page`: 0.
- **jmail.world on urlscan: 53 results, DIFFERENT operator** — a referral-spammer doing parasite SEO: `jmail.world/thread/<hex32>?q=<referral-URL>` with affiliate IDs `19384926` (folllike/followlike) and `119334` (livetraffic/2pink). ~3–8/day, irregular, no metronome. Two scans target lookalike `jmail.best`.
- **Watch item:** systematic probing of dead archive.today short-IDs across mirror TLDs (Sep 6–Oct 3, ~1–2/day) — link-rot checking, human-scale.

---

## 4. Sibling archive-oracle services (9 live mapped)

| Service | Status | Public queryable surface |
|---|---|---|
| cachedview.nl | LIVE | No-auth API (above); CDX as lookup log |
| archive.today family (.ph/.md/.li/.is/.today/.fo) | LIVE | Homepage recents, `/alldomains`, searchable index, `/timemap/<url>`, `/submit/?url=` |
| Ghostarchive.org | LIVE | Public search `search?term=` |
| Megalodon (megalodon.jp / gyo.tc) | LIVE | Per-URL public gyotaku list |
| arquivo.pt | LIVE | Keyless textsearch API (`textsearch?versionHistory=`) |
| Wayback availability API | LIVE | `archive.org/wayback/available?url=` (keyless) |
| cachedviews.com | LIVE (thin) | Server-side 302s only |
| cachedview.com | LIVE (degraded) | Client-side Wayback redirect |
| dessant/web-archives (extension) | OSS | 15 client-side sources, no backend |

**Dead (confirmed):** Google webcache (retired Feb 2024), Bing cache, cached.page, timetravel.mementoweb.org, memgator (Memento aggregator ecosystem collapsed). `startram` is not a cache service (name collision).

**Cross-service agent-shaped clusters:**
1. **`r=19384926` referral campaign** — one operator snapshotting their spam referral link across archive.today mirrors ("newest" + submit grammars), leaking into cachedview.nl jmail lookups. Jul–Oct 2026.
2. **jmail.world/EFTA sweep** — cachedview.nl (23 in 7h, Oct 4–5) + Megalodon `?url=` lookups of Epstein-themed urlquery/urlscan search pages (Jul 8). Multiple oracles, systematic enumeration.
3. **Backlink-generator SEO cluster** — archive.today + Megalodon + urlscan: operators archiving their own backlink tools.
4. **Regelbau/atlantic-wall theme** — cachedview.nl Pinterest cross-TLD enumeration + Ghostarchive `term=Regelbau` search.

---

## 5. Archive-oracle-as-fetch-proxy tradecraft

**Established pattern, not novel.** Uses: check cached vs live (defacement/takedown detection), bypass blocks (archive fetched earlier), retrieve dead pages, version comparison, avoid touching target directly. Purest specimen: `archive.ph/<live-URL>` submissions (requesting archive.today to serve a live URL) + `archive.ph/Wc0yZ` polled 4× in 8 min. Wayback availability API and Arquivo.pt textsearch are the canonical keyless oracle APIs; agent skills already teach Wayback-first fetching (hemo-web-read `/save/` captures; r.jina.ai fallback in last30days-skill).

---

## 6. jmail.world — what it is and what the audit was

**"Jmail — Jeffrey Epstein's Emails"**: Gmail-parody interface over the multi-million-page DOJ/House Oversight Epstein releases, built by Riley Walz and Luke Igel, launched Nov 2025. OCR + AI over redacted PDFs. Legitimate-ish public-interest project — **not** a phishing farm. Google Safe Browsing clean; VT ~1/94 (heuristic); no OTX pulses or threat reports.

**The audit was query-reflection / SEO-poisoning testing**: probing whether jmail.world's search echoes attacker-controlled strings/URLs into indexable pages (trusted-domain URL wrappers). The affiliate URLs were the *probes*, not evidence of abuse. 67/72 scans show no redirect — apparent finding negative so far.

**`seekers+of+decay`**: clean negative on all four surfaces checked (web, GitHub, urlquery, urlscan) except the auditor's own canary submissions. Side-channel: appears in SEO backlink-spam tooling (`seekers-of-decay.json` in a backlink-generator repo) — same actor or tooling reuse, inconclusive.

---

## 7. Attribution: 872-report, 64-hour campaign

**Scope correction:** the "72-report run" is one window of **872 unique reports, Oct 2 12:05 → Oct 5 04:13 UTC (~64 h), median gap 3.0 min**, essentially unbroken 24/7 (three pauses: 52/230/107 min). Sep 6/14/17/18/22 warmup probes with identical payloads.

- **Submitter fingerprint:** single UA (urlquery default Firefox 134), all-default settings, no tags, no nonce grammar. Sharpest contrast with our Amap operator.
- **Timing:** median 2.68 min with 7 negative gaps (to −56 s) — timer-fired loop (~3 min) or submit→wait-with-timeout, slow scans completing out of order. Not a strict metronome.
- **cachedview (103/872, ~12%):** submissions are `cachedview.nl/#...` — but the `#fragment` never leaves the browser, so urlquery scans only the 232-byte shell. Submitter likely misunderstands cachedview, or it's a ritual oracle step.
- **Payloads:** 6 fixed values, uniform-random choice, 2 affiliate IDs (`19384926`, `119334`).
- **Verdict: programmatic, certain. Human's script/cron most likely (~2:1)** — rigid cadence, defaults everywhere, fixed kit, test-then-launch pattern, no agent tells. AI agent possible but not indicated (only agent-ish signals: browsing-derived URL picks, cachedview-as-oracle reasoning). Commercial scanner unlikely. **Not** our Amap operator, not tronzap-shaped (serialized drip vs bursty parallel).
- **What would settle it:** urlquery submission logs (staff only); post-04:13 campaign status (throttled, unknown); identifying "seekers of decay".

**Watch items:** standing watches recommended on `jmail.world`, `seekers+of+decay`, `19384926`, `119334`; if the kit hits other domains, the actor is expanding.

---

## 8. Infrastructure watchlist additions

- `cachedview.nl/api/{ARCHIVEAPI|LIVEVERSION|PERMACC|ARCHIVETODAY|LIBRARYOFCONGRESS}/<url>` — no-auth fetch-proxy/oracle endpoint (highest value).
- Wayback CDX `url=cachedview.nl/api/*&matchType=prefix` — de-facto public lookup log (1,504 captures / 354 domains).
- arquivo.pt textsearch API, Wayback availability API, Megalodon per-URL lists, Ghostarchive search, archive.today recents/`/alldomains` — all public, keyless, ongoing collection targets.
- Affiliate IDs `19384926` / `119334` as cross-service pivot keys.

Nothing pushed. Raw: `~/workspace/hunt-cache/cachedview/`, `~/workspace/urlscan-cachedview/`, `~/workspace/cachedview-recon/notes.md`, `cachedview/attribution-jmailworld.md`.
