# Trick class: URL-scanners + threat-intel databases
Sweep date: 2026-10-04 (Sun). Operator: subagent d5b97aa7.
Scope: Hatching Triage, abuse.ch family (MalwareBazaar/URLhaus/ThreatFox/YARAify), PhishTank, PhishStats, Kaspersky OpenTIP, MetaDefender Cloud (OPSWAT), ThreatBook sandbox, Tencent Habo, VirSCAN, MISP public communities.
Already covered by siblings (not redone): urlquery, urlscan, VirusTotal, ANY.RUN, Hybrid Analysis, Joe Sandbox, FileScan, OTX, ThreatMiner, Pulsedive, IBM X-Force.

Markers run per service: `uqscan=`, `uqcors`, `lhr.life` subdomains, tunnel patterns, tag-grammar shapes (epoch nonces, per-request labels).
Known operator context (NOT new): Chinese Amap-map data-collection fleet, `uqscan=<word><date>` tags, `<hex>.lhr.life` tunnels, active Jan–Oct 2026.

Doctrine applied: no-API-key is not a stop — page sources were read and frontend XHR/fetch endpoints hunted; every undocumented endpoint found is documented below with path/headers/params.

---

## 1. Hatching Triage (tria.ge) — GATED (account required)
- **Queryable without account?** No. `https://tria.ge/` renders a login wall (Sign in / Continue with Google / GitHub / Sign up). The Cloud API `GET https://tria.ge/api/v0/search?query=...` returns `{"error":"UNAUTHORIZED","message":"Missing Authorization header"}` (HTTP 401) without a Bearer token; a token requires a Researcher-tier account.
- **Marker results:** none run — no anonymous search path exists. Public reports are viewable only via direct sample-ID links (not enumerable/searchable).
- **Undocumented endpoints:** none found; frontend is behind auth.
- **Verdict:** clean negative on access; needs a Triage account to hunt. (If a key is provisioned later: `GET /api/v0/search?query=<query>` with `Authorization: Bearer <key>`, e.g. `query=tag:android`, `family:emotet`.)

## 2. abuse.ch family — GATED (free Auth-Key required, was anonymous)
All four community APIs now **require an `Auth-Key`** (free, self-service at https://auth.abuse.ch/, but that is a registration flow — not completable from here). Verified live 2026-10-04:
- **URLhaus** `POST https://urlhaus-api.abuse.ch/v1/url/` `{"url":"lhr.life"}` → `{"error":"Unauthorized"}` HTTP 401. Same for `uqcors`. Docs (https://urlhaus.abuse.ch/api/) now state Auth-Key required for all interaction.
- **ThreatFox** `POST https://threatfox-api.abuse.ch/api/v1/` `{"query":"search_ioc","search_term":"lhr.life"}` → `{"error":"Unauthorized"}` HTTP 401.
- **MalwareBazaar** `POST https://mb-api.abuse.ch/api/v1/` `{"query":"get_taginfo","tag":"uqscan","limit":10}` → `{"error":"Unauthorized"}` HTTP 401.
- **YARAify** — PARTIAL EXCEPTION: `POST https://yaraify-api.abuse.ch/api/v1/` `{"query":"lookup_hash","search_term":"d41d8cd98f00b204e9800998ecf8427e"}` (empty-file MD5) returned **HTTP 200 `query_status: ok`** with full metadata (first_seen 2021-07-12, last_seen 2026-10-04 16:27:45 UTC, 136171 sightings) — i.e. **`lookup_hash` is anonymously queryable** despite docs saying Auth-Key is required. BUT: YARAify is hash-only (md5/sha1/sha256/sha3-384, imphash/tlsh/gimphash/telfhash, YARA rule names) — **no URL/domain/substring search**, so our URL markers cannot be run there. Verdict: not a hunting surface for this trick class, noted as an anonymous hash oracle.
- **Undocumented endpoints:** none usable without key. URLhaus web UI: homepage `https://urlhaus.abuse.ch/` and `/browse/` load anonymously (HTTP 200), but `/browse/` ships **zero table rows and zero data-loading JS** in static source (only jquery/popper/bootstrap/gtag/hcaptcha) — the entry table's data XHR is not discoverable from page source; no anonymous search endpoint found. If an Auth-Key is obtained later, the documented bulk-query endpoints support exact-URL/hash/tag lookups.
- **Marker results:** none runnable without key. Clean negative on anonymous access.

## 3. PhishTank (phishtank.org / checkurl.phishtank.com) — GATED (free key; web search bot-walled)
- **Queryable without account?** Website search ("Phish Search", `/phish_archive.php`) exists, but the page is behind **Cloudflare "Just a moment..." challenge** — curl gets HTTP 403 even with homepage cookies; needs a real browser session.
- **API:** `https://checkurl.phishtank.com/checkurl/` — POST with `url` + `app_key`; the key is **free via signup** at phishtank.org (register → key issued). Not completable from here without creating an account.
- **Marker results:** none run (gated). 
- **Undocumented endpoints:** none found; homepage source shows only a login form (`action="login.php"`) and nav links.
- **Verdict:** blocked pending (a) a browser session for the web search, or (b) a free API key via signup.

## 4. PhishStats (phishstats.info / api.phishstats.info) — OPEN, markers run, CLEAN NEGATIVES
- **Queryable without account?** YES. Read-only REST API is public: `GET https://api.phishstats.info/api/phishing` — anonymous quota 50 req/day/IP (registered free tier 150/day). Filter syntax `_where=(field,operator,value)`, operators eq/ne/gt/lt/like/and/or; pagination `_p`, `_size` (max 100). Docs: https://phishstats.info/api-docs.
- **Marker results (all HTTP 200):**
  - `_where=(url,like,uqscan)` → `[]`
  - `_where=(url,like,uqcors)` → `[]`
  - `_where=(url,like,lhr.life)` → `[]` (retried, confirmed)
  - `_where=(title,like,uqscan)` → `[]`
- **Undocumented endpoints:** none needed — the documented public API suffices. (No key flow required for read-only.)
- **Verdict:** fully queryable anonymously; **clean negatives on all markers** in URL and title fields (4 of 50 daily anonymous quota consumed).

## 5. Kaspersky OpenTIP (opentip.kaspersky.com) — GATED (free token via registration)
- **Queryable without account?** No. API endpoint confirmed live: `GET https://opentip.kaspersky.com/api/v1/search/domain?request=lhr.life` → **HTTP 401** (endpoint exists, auth enforced). Documented endpoints (via seifreed/opentip README): `GET /api/v1/search/hash`, `/search/ip`, `/search/domain`, `/search/url` (URL endpoint requires a path, e.g. `example.com/index.html`; bare hosts → use domain), `POST /scan/file`, `POST /getresult/file`. Token requested in the OpenTIP web interface after free registration.
- **Frontend:** Vite SPA (`/public/app-Dhy7oeKq.js`, 4.8 MB, minified) — no literal API paths in bundle; routes seen: `/ui/login`, `/ui/checksession`, `/token`, `/requests` (quota page). No anonymous XHR endpoint recoverable from page source.
- **Marker results:** none run (gated).
- **Verdict:** needs free OpenTIP token; then domain+URL lookups are directly runnable.

## 6. MetaDefender Cloud (OPSWAT, api.metadefender.com) — GATED (free key via signup)
- **Queryable without account?** No. API requires key from free signup at https://metadefender.opswat.com/account. Free Community tier quotas (per public sources): Reputation 1000 req/day, Prevention 150/day, Sandbox 75/day, Threat Intel API 25/day.
- **Endpoints (documented, for use once keyed):** v4 API at `api.metadefender.com` — HashLookups (`lookupHash`), Reputation Service (`lookupIP` / `lookupDomain` / `lookupURL`), file scanning, dynamic analysis. (Note: filescan.io is OPSWAT's public sandbox — covered by sibling under FileScan, not redone.)
- **Marker results:** none run (gated).
- **Verdict:** needs free API key; then URL/domain reputation lookups are directly runnable.

## 7. ThreatBook (微步在线, x.threatbook.com / api.threatbook.cn) — GATED (registration; web UI bot-walled)
- **Queryable without account?** No. Web UI `https://x.threatbook.com/` serves a **JS math-challenge anti-bot page** (`Challenge=...`, `X-AA-Cookie-Value` handshake) — curl cannot pass; needs a real browser. 
- **API:** `https://api.threatbook.cn/v3/file/upload` (POST: file, sandbox_type → sha256), `GET https://api.threatbook.cn/v3/file/report` (params: sha256, sandbox_type); intel endpoints (IP/domain/hash/URL) exist on the same host. **Public API key is free** via ThreatBook online account Personal Center (registration may require CN phone verification — not completable from here). Note: `https://api.threatbook.com/` did not resolve/connect from this VM (HTTP 000); the `.cn` host is the documented one.
- **Marker results:** none run (gated).
- **Verdict:** blocked pending browser session (web UI) or registered API key. Sandbox is file/URL-submission based; the intel API supports domain/URL reputation once keyed.

## 8. Tencent Habo (habo.qq.com) — BLOCKED (bot-walled, browser needed)
- **Queryable without account?** Unknown — the site returns **HTTP 200 with an empty body** to both curl and the text-fetch pipeline (bot detection / JS-required shell). Habo (哈勃分析系统) is Tencent's file sandbox; historically QQ-login-gated.
- **Marker results:** none run.
- **Undocumented endpoints:** none recoverable (empty body).
- **Verdict:** needs a real browser session to even see the UI; then likely QQ login for search.

## 9. VirSCAN (virscan.org, CN) — NOT A URL SURFACE (file+hash only)
- **Queryable without account?** For URLs/domains: **no — the service has no URL search at all.** VirSCAN is a multi-engine **file** scanner: "File upload" + "Hash query" only (Next.js SPA). The `/apis` page renders empty props and links API docs behind login (`/login?callbackURL=%2Fapis`).
- **Marker results:** N/A — no URL/domain search exists to run markers against.
- **Verdict:** clean negative by design; file-hash oracle only.

## 10. MISP public communities — OPEN (feeds, no account), marker grep running
- **Queryable without account?** YES for public **feeds** (static JSON/CSV, no auth). MISP instances themselves need accounts, but the community feed layer is open: CIRCL OSINT feed `https://www.circl.lu/doc/misp/feed-osint` (manifest.json fetched: **1,681 events**), DigitalSide Threat-Intel OSINT feed `https://osint.digitalside.it/Threat-Intel/digitalside-misp-feed/`, plus ~50 default feeds (abuse.ch CSVs, blocklist.de, etc. — see https://www.misp-project.org/feeds/).
- **Marker test:** downloaded all **293 CIRCL OSINT feed events dated ≥2026-01-01** and grepped for `lhr.life`, `uqscan`, `uqcors` → **2 EVENTS HIT** (see Lead below). Supplementary tunnel-provider grep (`trycloudflare.com`, `ngrok*`, `oastify.com`, `interactsh`, etc.) hit ~10 events — sampled; all are Maltrail daily-IOC batches with generic malware-C2 tunnel domains (random-word `*.trycloudflare.com`, comments `generic`/`generic_stealer`), plus random-subdomain `*.oastify.com` OOB domains tagged `hacked_npmrepos` (same trail family/timeframe as the lhr.life hits — see Lead).
- **Caveat:** MISP feeds are IOC feeds (malware IOCs, no scan-submission metadata) — weaker surface for fleet-behavior hunting than scanner DBs, but they do carry first_seen timestamps and org attribution per event, so a hit would still carry signal.
- **Undocumented endpoints:** none needed — feed URLs are the documented public surface.

---

## Summary table

| Service | Anonymous URL/domain search? | Markers run | Result |
|---|---|---|---|
| Hatching Triage | No (login + Researcher key) | — | Gated |
| URLhaus / ThreatFox / MalwareBazaar | No (free Auth-Key now required) | — | Gated (was anonymous; key is free at auth.abuse.ch) |
| YARAify | Hash-only; `lookup_hash` anonymously OK | N/A (no URL search) | Not a URL surface; anon hash oracle noted |
| PhishTank | Web search exists but Cloudflare-walled; API needs free key | — | Gated (browser or signup) |
| PhishStats | **Yes** — public read API, 50/day anon | uqscan/uqcors/lhr.life (url+title) | **Clean negatives** |
| Kaspersky OpenTIP | No (free token via registration) | — | Gated |
| MetaDefender Cloud | No (free key via signup) | — | Gated |
| ThreatBook | No (JS-challenge web UI; API needs registered key) | — | Gated (browser or signup) |
| Tencent Habo | Unknown (empty body to non-browser clients) | — | Blocked, browser needed |
| VirSCAN | No URL search exists (file+hash only) | N/A | Clean negative by design |
| MISP public feeds | **Yes** — open static feeds | 293 CIRCL 2026 events grepped | **2 hits: `<hex>.lhr.life` in Maltrail batches, May 2026 (lead above)** |

## Lead: `<hex>.lhr.life` tunnel infra independently sighted in Maltrail trails (May 2026)
CIRCL OSINT feed, org **Krawczyk Industries Limited**, `tlp:clear`, event type `observation`:
- Event `50844ee8-3e79-4e60-a7c4-a98f68856e9b` ("Maltrail IOC for 2026-05-18", date 2026-05-17): `domain | 87e0bbc636999b.lhr.life` and `domain | b94b6bcfa27554.lhr.life`, both comment **`hacked_npmrepos`**.
- Event `6b353c07-62b4-4e43-8c4b-44bf0e52f2fe` ("Maltrail IOC for 2026-05-17", date 2026-05-16): `domain | lhr.life`, `domain | d8b498f1781bc2.lhr.life` (comment **`metasploit`**), `domain | bbc45e9f547785.lhr.life` + `domain | edcf8b03c84634.lhr.life` (comment **`hacked_npmrepos`**), plus `url | https://www.virustotal.com/gui/domain/lhr.life/relations` (someone pivoted the domain in VT).
- Same trail family/timeframe also lists random-subdomain `*.oastify.com` OOB domains (e.g. `g1i0b9xx6mira6mal5yv02n6pxvouck09.oastify.com`, 2026-06-06 batch) under `hacked_npmrepos`.

Reading (per anomaly doctrine — lead, not negative): the known Amap fleet's `<hex>.lhr.life` tunnel shape appears in an **independent sensor** (Maltrail network trails, May 2026) classified under `hacked_npmrepos`/`metasploit` trail tags. That does not fit the "map data-collection" frame — it suggests either (a) the same tunnel infra is shared/reused by other activity Maltrail buckets as hacked-npm/metasploit, or (b) trail-tag misclassification. Either way it is a corroborating independent sighting of the tunnel infrastructure with first-seen context May 2026. No `uqscan=`/`uqcors` strings in any of the 293 events.

## Leads / follow-ups for parent
1. **Highest-value unlocks (all free, need human or browser action):** abuse.ch Auth-Key (auth.abuse.ch, self-service, unlocks URLhaus/ThreatFox/MalwareBazaar bulk APIs), PhishTank free API key (signup), Kaspersky OpenTIP token (web UI registration), MetaDefender Cloud key (signup), ThreatBook key (may need CN phone).
2. **Browser-session targets:** PhishTank phish_archive.php search (Cloudflare), ThreatBook x.threatbook.com (JS challenge), Tencent Habo (empty-body bot wall).
3. **YARAify anomaly (lead, not negative):** `lookup_hash` answers without Auth-Key despite docs — worth a deeper probe of which other query types are anonymously accessible (e.g. `get_yara` by rule name); not URL-huntable but a possible hash-pivot surface.
4. No new agent/swarm fleet found in this trick class beyond the known Amap fleet context. PhishStats — the only fully open URL-searchable intel DB in the set — is clean on all markers.
