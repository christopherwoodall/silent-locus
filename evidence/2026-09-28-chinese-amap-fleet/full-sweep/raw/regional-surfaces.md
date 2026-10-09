# Regional surfaces sweep — global-south / non-Western sandboxes, pastebins, threat intel

Date: 2026-10-04. Hunt: undiscovered agent/swarm fleets on surfaces the Western sweep missed.
Markers probed: `uqscan` (incl. `uqscan=<word><date>` tag grammar), `uqcors`, `lhr.life` / `<hex>.lhr.life` tunnels.
Known operator (exclude from "new"): Chinese Amap-map data-collection fleet, `uqscan=<word><date>` tags, `<hex>.lhr.life` tunnels, Jan–Oct 2026.

Method note: global web searches for `"uqscan"`, `"uqcors"`, `"uqscan="`, `"lhr.life"` were run first — they set the baseline
(zero relevant hits for uqscan/uqcors outside our own context; lhr.life hits are generic scam-checkers, urlscan, GitHub).
Per-surface work below is what the global index could NOT answer. Per standing doctrine, "no API key is not a stop":
page sources were fetched and frontend JS read for XHR endpoints where egress allowed.

EGRESS CAVEAT (2026-10-04 ~22:50 CDT): the VM egress proxy currently completes plain-HTTP requests but HTTPS CONNECT
tunnels are flaky — most hosts time out; a few (www.virscan.org, x.threatbook.com, www.axur.com) succeeded intermittently.
Several "blocked" verdicts below are proxy failures, not site denials, and are marked as such. browser.search worked throughout.

---

## 1. Regional URL scanners / sandboxes

### virscan.org — China (Beijing; "VirSCAN - Multi-Engine Online File Scanner") — CLEAN NEGATIVE (for our markers)
- What it is: free multi-engine FILE scanner (37–47 AV engines), Chinese-operated (hosted CN, beian/MIIT links, Geetest captcha).
- Probed: fetched homepage HTML + Next.js page bundle (`/_next/static/chunks/pages/index-182d8791aec563f3.js`, build `ls0oZwcLw6tIZkGF3I5BS`).
- Finding: the frontend offers exactly two modes — **file upload** and **hash query (SHA256/MD5/SHA1)**. There is NO URL
  submission and NO URL search index. Hash query calls an internal API client then routes to `/report/<links-id>`.
  Geetest captcha (`/js/gt4.js`) gates queries; error code -98 triggers captcha display.
- Verdict: structurally incapable of carrying our URL markers. Clean negative. A fleet would only appear here if it
  dropped binaries — nothing in our marker set is a file hash.
- Undocumented-endpoint notes (for reuse): Next.js app; report pages at `/report/<id>`; hash lookup is a JS API-client
  call (webpack module, exact XHR path not extracted — chunk fetches were flaky); legacy report URL pattern seen in
  search index: `https://sha1.virscan.org/<sha1>.html`.

### x.threatbook.com — China (微步在线 ThreatBook, X threat-intel community) — BLOCKED (JS-challenge WAF)
- `http://x.threatbook.com/` → 301 → `https://x.threatbook.com/` returned HTTP 200, but the body is an anti-bot
  JS challenge page (`X-AA-Challenge`, `X-AA-Challenge-ID`, `X-AA-Challenge-Result` headers; `X-AA-Cookie-Value`
  response cookie; classic Knownsec-style challenge). No content readable without executing the challenge.
- Verdict: blocked. Needs a live-browser pass (the challenge is what a real browser solves automatically).
  ThreatBook's sandbox/intel search is account-gated behind this.

### habo.qq.com — China (Tencent Habo file-analysis platform) — BLOCKED (unreachable)
- Both `http://` and `https://` fetches timed out through the egress proxy; browser text-fetch also failed
  (empty response). Cannot confirm reachability from this VM. No verdict possible — retry when egress is healthy
  or via live browser. (Habo is file-report oriented; historically reports are hash-addressed, low prior for URL markers.)

### opentip.kaspersky.com — Russia (Kaspersky Threat Intelligence Portal, free tier) — BLOCKED (needs registration; fetch failed)
- Page/API fetches failed from this VM (proxy timeouts; browser text-fetch also failed). From documentation in the
  search index:
  - Web UI lookup exists for hash / IP / domain / **web address** (URL), but submissions hit a CAPTCHA ("I'm not a robot").
  - REST API is documented and free but requires a registered API token (`x-api-key` header):
    - `GET https://opentip.kaspersky.com/api/v1/search/url?request=<web address>` (needs a path, not a bare host)
    - `GET https://opentip.kaspersky.com/api/v1/search/domain?request=<domain>`
    - `GET https://opentip.kaspersky.com/api/v1/search/hash?request=<hash>`
    - `GET https://opentip.kaspersky.com/api/v1/search/ip?request=<ip>`
  - There is a community Python client (`seifreed/opentip` on GitHub) wrapping these.
- Verdict: blocked without a free registration (creating accounts is out of scope for this subagent). **Recommended
  follow-up:** register a free OpenTIP token and query `lhr.life` domain + a sample `uqscan=` URL through
  `/api/v1/search/url` and `/api/v1/search/domain` — Kaspersky's URL corpus is one of the few non-Western URL-lookup
  indexes that could plausibly hold our markers.

### vms.drweb.com — Russia (Dr.Web online link/file scanner) — CLEAN NEGATIVE
- "Check link" form at `https://vms.drweb.com/online/?lng=en` scans a submitted URL against Dr.Web's malicious-site list
  and unpacks linked EXEs. It is a **lookup tool, not a published index**: scan results are not persisted to public,
  searchable report pages.
- Verdict: no searchable submission index → cannot be mined for our markers. Clean negative.

### dfndr lab (psafe.com/dfndr-lab) — Brazil — CLEAN NEGATIVE
- PSafe's "suspicious link checker" (dfndrlab.com): paste-a-URL verdict service using ML + partner phishing feeds +
  analyst review. No public archive or search over past submissions; verdicts are per-query only.
- Verdict: no minable index. Clean negative.

### Axur (axur.com / blog.axur.com) — Brazil (digital risk protection / CTI vendor) — CLEAN NEGATIVE
- Commercial threat-intel platform; homepage (fetched, Webflow) shows product pages (`/en-us/cyber-threat-intelligence`,
  `/en-us/threat-hunting`) but **no public IOC/URL lookup or searchable report index**.
- `site:blog.axur.com "lhr.life"` → zero results.
- Verdict: clean negative for markers. (Their takedown/phishing data is commercial-only.)

### analyze.intezer.com — Israel (Intezer Analyze, Genetic Malware Analysis) — CLEAN NEGATIVE
- File-oriented (code-DNA / code-reuse analysis); public reports are hash-addressed (`/#/analyses/<uuid>`); community API
  needs a key. No URL-scan submission surface found — URL analysis is not its product surface.
- Verdict: file-only, no URL index → clean negative for our markers.

---

## 2. Regional pastebins

### justpasteit.in — India — CLEAN NEGATIVE
- Free pastebin (`/publish/<slug>` URLs, SEO-farm style, account-optional). Homepage shows no search feature; pastes are
  discoverable only via Google index.
- `site:justpasteit.in "lhr.life"` → zero results. Global `"uqscan"` search → zero relevant hits anywhere.
- Verdict: clean negative for markers. (Most pastebins noindex by default, so absence in Google is weak evidence —
  noted, not overstated.)

### telegra.ph — (Telegram; Dubai/RU infra, global user base) — CLEAN NEGATIVE
- `site:telegra.ph "lhr.life"` → zero results. Telegraph pages are Google-indexed, so a marker-bearing page would likely
  surface. No Telegraph API content-search exists without an access token.
- Verdict: clean negative for markers.

### General pastebin note
- The global `"uqscan"` / `"uqcors"` searches returned zero relevant hits across the entire indexed web (only noise:
  TON address prefixes, OCR garbage, a TikTok URL param). Our tag grammar appears in no indexed paste anywhere —
  consistent with urlquery tags never being web-crawled. Regional paste discovery (BR/IN/CN-specific services) turned up
  no service with a public search API worth probing beyond justpasteit.in. Long-tail unindexed pastes remain a blind
  spot by construction.

---

## 3. Regional threat intel (vendor blogs / reports)

### Group-IB (Singapore HQ; blogs + Jan-2026 whitepaper) — CONTEXT, no marker hits
- **"Weaponized AI: Inside the criminal ecosystem fuelling the fifth wave of cybercrime"** (whitepaper, launched Dubai,
  Jan 20 2026): 371% surge in dark-web AI-keyword posts since 2019; "agentic AI" phishing kits automating victim
  targeting, lure generation, campaign adaptation for ~Netflix-subscription monthly fees; proprietary "dark LLMs"
  (e.g. "Nytheon AI") sold from ~$30.
- **"Stranger Threats Are Coming: Group-IB Cyber Predictions for 2026"** (group-ib.com/blog/cyber-predictions-2026/):
  predicts "autonomous AI agents will increasingly be capable of managing the entire kill chain: vulnerability
  discovery, exploitation, lateral movement, and orchestration at scale" → "the first truly AI-driven worm epidemic."
- Verdict: no mention of our markers (expected — markers are ours), but this is the strongest regional-vendor
  confirmation that **agentic-AI fleet tradecraft is industrializing in 2026**, which is the exact phenomenon class
  we're hunting. Worth citing as backdrop, not evidence.

### Seqrite Labs / Quick Heal (Pune, India) — CONTEXT, no marker hits
- **India Cyber Threat Report 2026** (announced Jan 5 2026, seqrite.com): "2026 will be the year of cognitive threats" —
  AI-augmented attacks mimicking human behavior; hyper-personalized AI phishing ("digital twins" of contacts);
  AI-enhanced mobile banking malware "capable of autonomously filling credentials, bypassing biometric authentication,
  and executing fraud without human intervention."
- Verdict: regional-vendor signal that autonomous agent-like malware is on their 2026 radar. No marker hits.

### 360 Netlab blog (blog.netlab.360.com) — China — CLEAN NEGATIVE
- `site:blog.netlab.360.com AI agent botnet` → only legacy IoT botnet analyses (Ngioweb, TheMoon/GPON). No AI-agent /
  agent-fleet research surfaced.
- Verdict: clean negative for agent-fleet tradecraft coverage (as of index).

### Securelist (Kaspersky, Russia) — CLEAN NEGATIVE
- `site:securelist.com AI agent` → only generic `Trojan.*.Agent.gen` detection-name hits on statistics pages.
  No AI-agent-fleet research surfaced.
- Verdict: clean negative for agent-fleet tradecraft coverage (as of index).

---

## LEAD (doesn't fit the frame — examine on its own terms)

### lhr.life / localhost.run is default agent-dev tunneling — our fleet blends into heavy benign traffic
- **bebabinlarsson-blip/godot-mcp v5.0.33** (2026-09-23, GitHub release): sets `localhost.run` (`*.lhr.life`) as the
  primary default tunnel provider and explicitly markets **"Unblocked for External AI Agents"** — "External ChatGPT,
  OpenAI, and Claude requests pass straight through with 200 OK," eliminating Cloudflare 403/530 blocks. Background
  keepalive pings `/health` every 25s.
- **pokemon-agent skill** (NousResearch lineage) — three independent forks carry identical instructions, including
  **linyq66/kopi-ai-agent** (Kopi Ai Agent Pte Ltd, **Singapore**): agents are told to run
  `ssh -R 80:localhost:9876 nokey@localhost.run` and share the resulting `.lhr.life` URL (+`/dashboard/`) with the user.
- Implication for the hunt: `<hex>.lhr.life` is THE standard primitive AI agents use to expose local servers
  (MCP servers, dashboards). The Amap fleet's tunnel usage is tradecraft-camouflaged inside a large and growing
  benign population. **Any new fleet on lhr.life is indistinguishable from dev tunnels without the `uq`-tag grammar
  or Amap-map URL patterns — which is exactly why the tag grammar, not the tunnel domain, is the discriminating marker.**
  Recommend: future lhr.life sweeps must key on `uqscan=`/`uqcors`-style query grammar, not the domain.

---

## Undocumented-endpoint registry (reuse)

| Surface | Endpoint | Method / params | Auth | Headers / notes |
|---|---|---|---|---|
| virscan.org | `/report/<links-id>` | GET (navigated to after hash query) | none observed | Hash query is a JS API-client call behind Geetest captcha (`/js/gt4.js`); error code -98 = show captcha |
| virscan.org (legacy) | `https://sha1.virscan.org/<sha1>.html` | GET | none | Seen in search index; old report URL scheme |
| Kaspersky OpenTIP | `https://opentip.kaspersky.com/api/v1/search/url?request=<web address>` | GET | free registration token via `x-api-key` header | Bare hosts rejected (400) — URL must include a path; use `/search/domain` for bare domains |
| Kaspersky OpenTIP | `https://opentip.kaspersky.com/api/v1/search/domain?request=<domain>` | GET | `x-api-key` | — |
| Kaspersky OpenTIP | `https://opentip.kaspersky.com/api/v1/search/hash?request=<hash>` | GET | `x-api-key` | MD5/SHA1/SHA256 |
| Kaspersky OpenTIP | `https://opentip.kaspersky.com/api/v1/search/ip?request=<ip>` | GET | `x-api-key` | — |
| x.threatbook.com | `/` (POST challenge) | POST with `X-AA-Challenge-ID`, `X-AA-Challenge`, `X-AA-Challenge-Result` headers | JS-challenge cookie (`X-AA-Cookie-Value`) | Challenge math is in the page's inline JS; NOT solved here (bot-defense) — needs live browser |

## Bottom line
- **No new fleet found.** No regional sandbox, pastebin, or vendor blog surfaced `uqscan`/`uqcors`/`lhr.life` marker hits
  or unknown fleet-shaped activity.
- **Two blocked-but-promising surfaces for a follow-up pass:** Kaspersky OpenTIP (free token → query `lhr.life` +
  `uqscan=` URLs — the only non-Western URL-lookup index found) and ThreatBook X (live-browser to clear the JS challenge).
- **One lead:** lhr.life is default agent-exposure infrastructure (godot-mcp's "Unblocked for External AI Agents"
  marketing; Singapore's Kopi Ai Agent skill) — the tunnel domain alone can't discriminate fleets; the `uq` query
  grammar is the marker that matters.
- **Regional intel context:** Group-IB (SG, Jan 2026) and Seqrite (IN, Jan 2026) both name autonomous/AI-driven
  attack fleets as the 2026 threat — the industry sees the same shape we're hunting, from the criminal side.
