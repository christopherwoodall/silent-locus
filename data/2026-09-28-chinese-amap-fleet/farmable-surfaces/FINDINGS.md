# Farmable Surfaces — Findings (2026-10-05)

Two-part mission: (1) enumerate every farmable surface for agent-trace hunting with UA-logging assessment; (2) pull from the top 3 new surfaces.

## PART 1 — Surface inventory

| Surface | Logs UA? | Searchable? | Agent-trace potential | Status |
|---|---|---|---|---|
| urlquery.net (API) | Scanner UA only (not submitter's) | Yes — farmed heavily | Primary source; fleet hides behind default FF 134 | Farmed |
| urlquery.net (htmx endpoint) | Same | Yes — recent-biased | Live sweeping; can't reach historical | Farmed |
| **webhook.site token API** | **YES — sender's true UA, IP, headers, content** | **Yes, no auth: `/token/<uuid>/requests`** | Dead-drop contents readable; fleet inboxes now dead | **PULLED (new)** |
| urlscan.io | Scanner UA | Yes | Same scanner-UA limitation | Farmed |
| Wayback CDX / WARC | Sometimes (request records) | CDX yes | UA in WARC request records when archived | Farmed (CDX) |
| Common Crawl | **Only CCBot's own UA (verified from WARC bytes)** | Index API, free | Dead end — 10 clean "No Captures"; crawl gap over Jun-21 burst | **DONE — dead end** |
| OTX (AlienVault) | No (dates + URLs only) | **Yes — no-auth API** | URL lists w/ first-seen dates; passive DNS | **PULLED — 4/79 lhr.life overlap** |
| Pulsedive | No (risk + seen dates) | **Yes — no-auth community API** | IOC risk/seens metadata | **PULLED — markers absent** |
| ANY.RUN / Hybrid Analysis / CheckPhish / urlscore.ai / ThreatMiner | Varies | **JS-walled — needs browser** | Sandbox analyses, phishing verdicts | Blocked — needs browser lane |
| AbuseIPDB | Reporter history (no UA) | JS-walled; API needs key | Operator IP reporter history | Blocked — no key |
| Shodan | N/A (banner data) | **Needs API key** (401 without) | Infra fingerprinting | Blocked — no key |
| FOFA | N/A | **Needs API key** (invalid without) | Same | Blocked — no key |
| VirusTotal | Submissions + vendors; no public UA | **Needs API key**; web UI needs JS | Submission timestamps | Blocked — no key |
| crt.sh | No (certs only) | Yes, free | Operator-owned domains (not tunnels) | Lane running |
| pastebin.com/archive | No | Scrapable, no auth | Program drops | Lane running |
| ix.io / termbin | No | Check manually | curl drops | Lane running |
| HuggingFace | No | API, free | Datasets/spaces/model cards | **PULLED — clean negative** |
| Bing / Brave / Mojeek / Marginalia | No (indexed content) | HTML endpoints | Markers Google missed | Lane running |
| AI Village (local) | Tool-call records may include UA | **GONE from VM** — needs HF token re-supply | Browser/request UAs by agent | **Blocked — needs user token** |
| openai-agent-traces | Zero UA fields (synthesized) | Local | None for UA | **PULLED — zero fields** |
| DseWiki | No | Existing collection | Coordination chatter | Checked — no marker hits |
| Reddit / HN / X | No | Light touch | Operator tooling discussion | Deprioritized |

## PART 2 — Top-3 pulls

### Pull 1: webhook.site token API (NEW surface, proven farmable)
- `GET https://webhook.site/token/<uuid>/requests` returns inbox contents as JSON **with no authentication**: per-request IP, country, **true sender User-Agent**, headers, query, body.
- Pulled all 23 fleet inbox UUIDs from our collection. **All dead**: 0–1 requests each, the few hits being random scanners (e.g. KH IP, generic Chrome UA). Fleet inboxes expired/wiped.
- Verdict: surface is farmable and should be checked for EVERY future fleet — dead-drop contents (including the sender's real UA) are public until expiry. The fleet's true exfil UA is unrecoverable from these inboxes now.

### Pull 2: is.gd short-link resolution (NEW traces)
Resolved all 5 June-burst slugs via redirect-following. Full detail in `isgd-resolutions.md`. Headlines:
- `is.gd/3JlIp7` → auto-submitting CORS-bypass form via **pingllo.com/api/proxy** targeting AIHW Tableau (`vizprod.aihw.gov.au`) — new proxy service in the operator's kit
- `is.gd/mf075827`, `is.gd/sum074114` → httpbun base64 Tableau-scraping programs for AIHW PBS dashboards, image-beacon exfil
- **`is.gd/kf073634` → auto-submitting form to `urlcap.com/account/api-keys` creating an API key named `scankey`** — the operator minting API keys on a URL-scanning service. Infrastructure provisioning, not just scanning.
- `is.gd/AGE115EXTRACT1` → AIHW AGE115 mental-health Tableau program with `?mark=AGE115EX1781972899` (IDPH-family tag grammar)
- June 2026 task family fully characterized: AIHW Tableau scraping + CORS-bypass proxies + API-key provisioning.

### Pull 3: UA inventory from our corpora (user's key ask)
Full table in `ua-inventory.md`. Headlines:
- Amap fleet: **98.9% use urlquery's default Firefox 134 UA** — they never customize `settings.useragent`. The UA field records the SCANNER, not the agent.
- **Zero custom agent UAs** anywhere organic: no python-requests, curl, GPTBot, ChatGPT-User. Agents hide behind platform defaults; the fingerprint is the *absence* of customization.
- One organic anomaly: Android WebView UA (Chrome/74, `wv` token) with `soteria` submit tag on `eseblt.click` — resolved as Soteria Cloud (email-security vendor) mobile scanning pipeline, unrelated to our operator.
- openai-agent-traces: zero UA fields (synthesized corpus, no request headers).
- AI Village: local copy gone from VM; re-mining needs the user's HF token re-supplied (streaming grep path documented in ua-inventory.md).

## Lane results (children)

### Common Crawl — DONE, dead end (`cc-hunt.md`)
- 10 genuine index answers across CC-MAIN-2026-39/30/25/21: every one `{"message": "No Captures found"}` for is.gd operator slugs + lhr.life tunnel hosts/paths (`uqcors.html`, `probe.html`, `probe2.html`, `combo.html`).
- Why the negative is expected: (a) lhr.life tunnels are ephemeral (hours); CC crawls monthly from a fixed seed list; (b) the Jun-21 probe.html/is.gd burst falls in a **crawl gap** — no CC crawl covers Jun 19–Jul 9, 2026; (c) is.gd slugs are permanent and still uncrawled.
- UA finding (verified from raw WARC bytes): CC request records carry exactly one UA — **CCBot/2.0's own**. The operator's UA can never appear in CC; only query strings, response bodies, and redirect Location headers could hold traces.
- Bottom line: CC is a dead end for this operator. Right archives for ephemeral tunnels: urlquery/urlscan (captured live).

### urlquery alternatives — DONE (`urlscan-alternatives.md`)
Surfaces from the user's sources (zeltser.com, postmodernsecurity.com), assessed for AGENT traces:
- **OTX**: no-auth API works. 132 lhr.life subdomains; **4 overlap with our operator's 79** (`5ede92286ebdfd`, `820eea12fec476`, `98a8e091083f27`, `c2679a7c8e852b`; first-seen Jun 25–Sep 9). 4,309 is.gd URLs scanned — zero of our 5 slugs.
- **Pulsedive**: no-auth community API. lhr.life + is.gd in DB (medium risk, seen dates); `uqscan` = 0.
- **urlscan.io**: `uqscan=`/`uqcors.html`/`pandalegacy` = 0 (parent's 90-result lhr.life find stands).
- Blocked: VirusTotal (API key), ANY.RUN / Hybrid Analysis / CheckPhish / urlscore.ai / ThreatMiner (JS-walled — browser lane), AbuseIPDB (key).
- Sucuri SiteCheck "malware" hits on an overlap subdomain were SEO meta-text, not a verdict (false alarm).
- User correction applied: agent/swarm BEHAVIOR is the filter, not generic IOC hunting. Cross-surface confirmations = supporting evidence, not the objective.

### Foreign-TLD sweep — DONE (`foreign-tld-sweep.md`)
- Our operator uses **zero foreign-TLD infrastructure**: no .cn, no punycode, no Chinese shorteners. `.cn` urlquery hits were `zh-CN` translate.goog artifacts.
- Chinese shorteners (`t.cn`, `url.cn`, `dwz.cn`, `suo.im`, `985.so`): no agent grammars, no bursts, no uq markers.
- One other-operator agent-shaped lead (noted, not tracked): OTX shows tunnel `02e18ab88f2ece.lhr.life` with `/c/01`–`/c/20` numbered-endpoint enumeration in ~15 min (2026-08-16) — systematic, agent-shaped, not our operator.
- 378 is.gd slugs in one hour (2026-01-31): random 6-char, zero grammar — filtered as noise per the user's rule.
### Search engines (Bing/Brave/Mojeek/Marginalia) — DONE, no new traces
- Bing: anti-bot decoy SERPs (unusable). Brave: 429 on first request. Mojeek: JS CAPTCHA. Marginalia: 5/11 dorks answered, all honest zeros (`sub_poi_navi`, `is.gd "uqscan"`, `lhr.life "probe.html"`, `AGE115EXTRACT1`, `MassCountyData`); 6 high-value dorks blocked by adaptive gate.
- Nothing indexed anywhere that Google missed. Full detail: `engine-dorks.md` (+ runner script for later retry).
### crt.sh + pastebins — DONE, both honest zeros
- crt.sh: every campaign marker (`uqprobe`, `uqscan`, `sub_poi`, `httpbun`) = zero certs. Operator mints no certs (ephemeral tunnels + public utilities) — CT is a dead end by construction.
- pastebin.com/archive: zero marker content (spam-dominated listing). ix.io is DOWN. termbin.com has no indexable surface. Prior paste corpora also zero.
- Full detail: `ct-paste.md`
### HuggingFace — DONE, clean negative
- Zero marker hits across datasets/models/spaces. Fleet's Amap entrance dataset NOT published on HF (closest: `Stephen3zero24/amap-2000-candidates-v1`, explicitly synthetic mock benchmark — watchlisted, not a hit). 6 new generic proxy/webhook spaces shape-matched, no campaign tie.

### Native-tongue × UA-evasion wildcard — DONE (folded into `ua-inventory.md` §6)
- Context: `pandalegacy`/`mochou`/`customua` retracted as our probes → confirmed **operator UA-evasion tests** (2026-10-04): systematic UA A/B testing (`taersi-mobile-ua`, `uqcustomua` + Googlebot spoof, bare `Mozilla/5.0`/`mobile`/`desktop`/`0`) targeting `m.amap.com`/`pre-lbs-m.amap.com` mobile endpoints.
- Crossed the 9-language translation table (mobile/browser/custom/test words) against `uqscan` via htmx: **all native-tongue crosses = 0** (`shouji`, `yidong`, `liulanqi`, `ceshi`, `mobilny`, `keitai`, `handy`, `movil`, `celular`, `portable`). No other operator runs UA-evasion tests in their own language.
- Distinct-submitter detector: 189 non-Amap reports in local collection — **zero non-standard `settings.useragent` values**. No second submitter.
- Verdict: UA-evasion behavior is exclusive to the `uq`-grammar operator, in English + pinyin only.

## Open follow-ups
- AI Village UA mining — blocked on HF token re-supply (user action)
- Shodan/FOFA/VirusTotal/AbuseIPDB — blocked on API keys (user supplies)
- ANY.RUN / Hybrid Analysis / CheckPhish / Zscaler Zulu — browser lane (JS-walled)
- webhook.site — re-check for NEW fleet inboxes (ltzh family, future task families); method documented
- `v.gd/MassCountyData007` lead — sweep label variants
- urlcap.com `scankey` — operator provisions API keys there; urlcap submission history may hold more
- pingllo.com — new CORS-bypass proxy in operator's kit; farm its usage
- OTX deep lane: full lhr.life pull + passive_dns on the 4 overlap subdomains; mine all 4,309 is.gd URLs for other agent-shaped short links

## Addendum: urlcap.com bot directory (UA reference surface)
- `https://urlcap.com/bots` — 173-entry public known-bot directory (no auth needed for listing)
- Includes Chinese-lab bots: DeepSeekBot, ChatGLM-Spider (Zhipu), Qwenbot, KimiBot, Kimi-SearchBot, MoonshotBot, plus ClaudeBot/Claude-User/GPTBot/Bytespider
- Per-bot UA strings are JS-rendered (not in static HTML) — needs live-browser extraction
- Use: reference UAs for what Chinese-lab crawlers self-identify as; cross-check against any future UA-bearing trace
- Note: the operator minted a `scankey` API key on urlcap.com (see isgd-resolutions.md) — they use this service's infrastructure

---

## Run 2026-10-05 ~05:00 UTC — OTX lhr.life deep pull + urlscan behavior sweep

**INFRA ALERT: VM direct egress is DOWN.** All curl HTTPS fails; egress proxy
`hatch-egress-proxy:3128` returns `407 Proxy Authentication Required` for the
env-baked credential (DNS resolves, TCP to proxy connects — the credential
itself is rejected). This run's network work used the runtime's browser-fetch
path (`browser.open`/`browser.search`) as fallback. Flagging for parent:
every curl-based hunt lane is stalled until the proxy credential is fixed.

### OTX lhr.life url_list pages 1–5 (Oct 2 → Jun 22; raw: `raw/otx-lhrlife-2026-10-05.md`)
- **Other-operator `/c/NN` payload campaign fully characterized** (NOT ours):
  `02e18ab88f2ece.lhr.life/883120a1824c6dce00679806/c/NN-<12hex>/downloads/payload-<12hex>.zip`,
  NN=01..20, ~60 URLs in 63s on 2026-08-16. Per-slot payload zips = campaign
  panel / malware staging. Prior note said "41 URLs, paths /c/01../c/20" —
  corrected: fuller grammar with per-slot hex IDs and `downloads/payload-*.zip`.
- **`/c` + `/r` tunnel family** (shared toolkit, not ours): `b6c89c319da971.lhr.life/c`
  (Sep 30), `a329f5f3e67568.lhr.life/c` + `/r` (Aug 30, 54s apart).
- **Agent-server via tunnel** (not ours): `48e0cb905290ad.lhr.life/agents.json` +
  `/llms.txt` + `/openapi.yaml` within 22s on Aug 24 — an agent framework's API
  surface exposed through localhost.run. Watch for recurrence.
- **API recon**: `2580d75923f5e1.lhr.life/api/changelog` + `/api/manifest`, 7s apart (Aug 16).
- **OUR operator cross-confirmation**: OTX's `c2679a7c8e852b.lhr.life/login.html`
  (Jun 25) matches our corpus urlquery report (same URL, same day) — the fleet's
  tunnel served a phishing-shaped login page, not just scraping probes.
- **Third-party fuzzing of OUR tunnel**: `a35c2e7d29722e.lhr.life` (in our 78)
  hit with ~30 short garbage paths (`/dll`, `/result`, `/ll`, `/dows`, `/~H`,
  `/;.EXI`, …) over Jun 22–25. Same fuzzer pattern on non-fleet host
  `2d5f8eb0b18e42.lhr.life`. Attribution unknown; logged as observed behavior.
- OTX zeros: `pingllo.com` and `urlcap.com` url_lists both empty — operator's
  CORS proxy and the urlcap service are invisible to OTX. Pulsedive: `pingllo.com`
  404 (unknown indicator).
- OTX `passive_dns` → HTTP 429: **OTX polling hard-stopped for this run per policy.**
  Resume OTX (passive_dns for the 4 overlaps, is.gd full pull) next run after backoff.

### urlscan behavior sweep (no-auth API via fetch fallback; note: anonymous search is 30-day-windowed)
- Markers all zero: `uqscan`, `uqcors.html`, `pandalegacy`, `scankey`, `pingllo`
  (weak negatives for June activity given the 30-day window; genuine for recent).
- `domain:lhr.life` (100 results): **daily API re-scans of `90667af7b6a9f1.lhr.life`**
  Sep 27–Oct 4 (`method: api`) — unknown party monitoring a persistent tunnel;
  one scan tagged `hybridanalysis`.
- `filename:agents.json` global → 100 results, all legit sites (llms.txt-era
  convention) — too noisy, honest negative for tunnel-agent-server hunting.
- `domain:clck.ru` → 100 results: Yandex affiliate marketing + re-scanned shorts,
  no agent grammar — foreign-TLD continuation negative (30-day window).
- Documented limitation for future: urlscan anonymous search returns
  `search_date_limit_days: 30` — historical (June) negatives from urlscan are weak.

### Endpoints confirmed/working this run (for reuse)
- `GET https://urlscan.io/api/v1/search/?q=<es-query>&size=N` — no auth; anonymous = 30-day window; `search_after` for paging.
- `GET https://otx.alienvault.com/api/v1/indicators/domain/<d>/url_list?limit=50&page=N` — no auth; date-desc; 429s easily — pace gently.
- `GET https://pulsedive.com/api/info.php?indicator=<ioc>` — no auth; risk/WHOIS/DNS; 404 = unknown indicator.
- `GET https://urlquery.net/api/htmx/search/?q=&limit=&offset=` — needs `HX-Request: true` + `HX-Current-URL` headers; returns 204 without them (runtime fetch can't set headers — curl path only, currently blocked by egress outage).
