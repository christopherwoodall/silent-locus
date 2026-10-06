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

## Run 2026-10-05 ~07:00 UTC — ACTIVE CAMPAIGN + webhook.site inbox pull (LIVE dead-drops)

**Egress recovered** (direct + proxied curl 200; the 05:00 UTC 407 outage cleared).
**OTX still hard-stopped**: `passive_dns` → 429 on all 4 overlap subdomains (2h+
of throttling). OTX deep lane stays parked per policy.

**MAJOR: the fleet is running an ACTIVE campaign right now.** urlquery htmx
`uqscan` offsets 0–75 (~94 unique rows) show continuous activity 2026-10-04
~19:20 UTC → 2026-10-05 04:11 UTC. Full detail: `webhook-inbox-pull.md`;
raw: `raw/2026-10-05-inbox-pull/`.

- **New task family: cultural/landmark POI collection across Chinese provinces**
  (museums, zoos, hospitals, bazaars, monasteries, film studios). New tag
  grammars: `<city>museum<date><letter>` (`qingdaomuseum20261005b`,
  `henanmuseum_page_20261005a`, `gxmuseum`, `fujianmuseum`, `nanhaimuseum`,
  `jxmuseum-mobile-detail`, `qdmuseum20261005a/b/c`), `wuxizoo`, `taiyuan`,
  `taersi`, `zhenbeibao`, `anhui-famous-direct`, plus `research/target/direct/
  mobileapi/mobilerich` + date API-surface labels.
- **`claude20261005<target>` model-attribution labels** (`mobile1/2`, `ditussr`,
  `dituold`, `bazaar`, `hospital2/3`, `gxzyy`, `claudeprime` on Amap's own
  Next.js chunks) — the harness A/B-tests Claude-family agents against Amap
  surfaces (SSR web, mobile web, legacy ditu, service APIs, `pre-amap-pc-ssr`
  staging host, `user_loc` geo-spoofing).
- **11 LIVE webhook.site inboxes pulled via the no-auth token API** (14 UUIDs
  harvested from decoded beacon programs; 1 expired). Beacon bodies expose the
  operator's TRUE agent stack: **`Firefox 134 / Windows` from 195.64.118.152
  (Norway)** — full harness lifecycle `boot→bxinit→xdcinit→capture×5→error×5→done`
  in 29s. Operator provisioning tooling: `python-requests/2.32.5` + `curl/8.14.1`
  from Tencent Cloud IPs (`?verify=1`/`?hello=world`/`?headers=1`).
- **Campaign objective = Amap "Baxia" (霸下) anti-bot reverse-engineering.**
  Beacon programs call `baxiaCommon.init({uabOptions:{location:'cn'/'us'},
  appendTo:'header'/'querystring', needUmidToken:true, paramsType:['uab','umid',
  'et']})` and harvest freshly-minted `bx-ua` tokens; "Baxia signed navigation"
  program exfils live signed URLs (confirmed working, `ccad3060` inbox).
  Amap fights back: `FAIL_SYS_USER_VALIDATE` + `x5secdata` punish URLs in `load`
  beacons.
- **`r.jina.ai` CONFIRMED as a working Amap anti-bot bypass**: `jina-cache`
  test fetched `amap-pc-ssr.amap.com/ssr/place/B001C8MXRO` (Chengdu Zoo) → HTTP
  200 markdown exfiltrated in chunks (`cbcb10de` inbox). Connects to the
  skill-tracer lane's r.jina.ai keyless-fetch finding.
- **New utility services**: livecodes.io (beacon/redirect program host),
  href.li (referrer-hiding wrapper for httpbun programs).
- `palacelegacy1791142556` (livecodes.io redirect chain) — same
  `<word>legacy<epoch>` label family as `pandalegacy`; treat new `<word>legacy`
  labels as operator tests.
- Chrome/116/X11-Linux beacons from PL/CZ/US/IN/BD/HK/NL/DE (07:07–07:22, 4 min
  after the operator's run) assessed as third-party scanners tripping the public
  beacon page (`xdcerr: webTracker is not defined`); attribution uncertain,
  logged as observed.

### Endpoints confirmed/working this run (for reuse)

- `GET https://webhook.site/token/<uuid>/requests` — no auth; returns inbox
  JSON incl. per-request IP/country/UA/headers/query/body. Inboxes are public
  until expiry; fleet rotates UUIDs per program — re-sweep htmx `webhook.site`
  each run for new ones.

## Open follow-ups (updated 2026-10-05 ~07:00 UTC)

- AI Village UA mining — blocked on HF token re-supply (user action)
- Shodan/FOFA/VirusTotal/AbuseIPDB — blocked on API keys (user supplies)
- ANY.RUN / Hybrid Analysis / CheckPhish / Zscaler Zulu — browser lane (JS-walled)
- webhook.site — DONE this run (11 live inboxes pulled, protocol decoded);
  **standing: re-sweep for NEW fleet inboxes every run** (UUIDs rotate per program)
- `v.gd/MassCountyData007` lead — sweep label variants (still open)
- OTX deep lane — **hard-stopped on 429s (2h+)**; resume `passive_dns` (4 overlaps)
  + full `is.gd` pull next run after longer backoff
- New leads this run: monitor `r.jina.ai/https://amap-*.amap.com` usage (working
  bypass); watch for new `<word>legacy<epoch>` redirect-chain labels; the
  `claude*` tag family may grow per-model variants (other model names?)
- `urlcap.com scankey` / `pingllo.com` — still open (OTX showed zero; Pulsedive
  404)

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

---

## Run 2026-10-05 ~12:55 UTC — respawn sweep (campaign still live; OTX parked; urlscan tronzap lead; foreign-TLD zeros)

Raw: `raw/2026-10-05-respawn-sweep/`. Egress recovered (direct + proxy curl both 200;
the 05:00 UTC 407 outage cleared).

### 1. Campaign is STILL ACTIVE — new `vfy` verification phase + `nested` flow test
htmx `uqscan` offset 0 shows operator activity through **2026-10-05 12:19 UTC**
(minutes before this run), continuing the museum/POI campaign:
- New tag grammar **`vfy20261005<letter>`** (verify phase, a–f observed) on a NEW POI
  `B024F04YSV`, hit across all four surfaces in 8 minutes (12:11–12:19 UTC):
  `ditu.amap.com/ssr/place` + `/detail/get/detail` (SSR web + legacy ditu),
  `www.amap.com/place`, `amap-pc-ssr.amap.com/ssr/api/getPoiInfo` — one with
  `user_loc=119.303,26.085` (Fujian geo-spoof, same technique as before).
- **`nested2026100…`** (01:47 UTC): `amap-pc-ssr.amap.com/ssr/search/poi_detail`
  with `source=poi_search` — a nested search→detail flow test on POI B01FE16U78
  (Wuxi Zoo). Label-family watch: `vfy*`, `nested*` now join `claude*`, `*museum*`,
  `<word>legacy<epoch>`.
- Note: htmx keyword search for the bare tags (`vfy`, `nested`) returns only
  unrelated noise — size new phases via the `uqscan` search, not bare keywords.

### 2. webhook.site re-sweep — NO new inboxes since 03:19 UTC
Recent-window pull (`webhook.site`, limit 50): 5 reports, all UUIDs already pulled
in the 07:00 UTC run. Deeper window (offset 50): 19 reports going back to June 21 —
14 "new" UUIDs vs the Oct-05 list, but cross-check shows 9 already in-corpus
(metronome htmx + ghost-hunter deaddrops, all assessed expired) and 5 truly
unseen (`bda06178`, `f9c24dca`, `178c74fe`, `0ff0d84e`, `980e5c81` — June 21
18:43–19:37 burst). **All 5 pulled via no-auth token API → HTTP 404 (expired)**,
confirming the ghost-hunter expiry assessment. Clean verification receipts kept in
`raw/2026-10-05-respawn-sweep/` (empty JSONs removed after check).
- New shape noted from the June-21 burst: `178-63-67-153.sslip.io/<uuid>?retry=3`
  (×3 reports, `?x=0/1/2` beacon protocol) — the operator's old campaign also used
  **sslip.io wildcard-DNS tunnel hosts as exfil receivers**, not just lhr.life
  and webhook.site. Standing: sweep `sslip.io`/`nip.io` UUID-pathed URLs in future
  runs.
- **Standing verdict holds: re-sweep `webhook.site` every run; fleet inboxes are
  live only during a campaign and expire within days.**

### 3. OTX — STILL 429, parked per policy
First `passive_dns` request (of the 4 overlap subdomains) → HTTP 429 immediately.
Lane stays parked; retry next run after longer backoff. No OTX data this run.

### 4. urlscan sweep — new "TronZap" infrastructure cluster (LEAD for new-fleets)
`domain:lhr.life` (89 total, 30-day window): the `90667af7b6a9f1.lhr.life`
daily API re-scan continues (Oct 4 latest). NEW: a Sep-26 17:00–18:30 UTC burst
mixing `api.tronzap.com`/`dash.tronzap.com` (v1/orders, /orders/calculate,
/orders/check — a Tron-payment API; dash is Livewire/Laravel) with lhr.life
tunnels serving payment-flow pages (`/calc3.html`, `/calc4.html`, `/ig.html`,
`/lw.html`, `/cancel.html`, `/app.html`, `/chk2.html`, `/e3.html`) from the
*same API submitter session*. `dash.tronzap.com/eval-stdin.php` scanned 5× in
~2 min (Sep 26 18:18–18:20) — eval-stdin is a webshell-shaped endpoint. No
uqscan/agent grammar; not our operator's shape. **Recorded as a lead for the
new-fleets lane** (misfit, not a negative); result-detail API now requires
login, so characterization is search-level only.
- Our 4 OTX-overlap subdomains: no urlscan hits in the 30-day window.
- `filename:agents.json` recurrence: not re-run this pass (prior honest negative stands).
- livecodes.io on urlscan: 1 result (unrelated vitepress page, Oct 3) — fleet's
  livecodes beacon programs invisible here (weak negative, 30-day window).
- `r.jina.ai amap` on urlscan: **0** — the operator's working jina-cache bypass
  leaves no urlscan trace. Cross-surface blind spot confirmed.

### 5. Foreign-TLD continuation — honest zeros
htmx `vk.cc` (16 reports), `clck.ru` (20), `t.ly` (20), `s.id` (18): zero
uqscan/agent grammar hits. Content is marketing/phishing/gambling spam
(`steamcommunity.click`, `susampazari.com`, `joki188.click`). Operator's
zero-foreign-TLD profile holds.

### Endpoints confirmed/working this run (for reuse)
- `GET https://urlscan.io/api/v1/search/?q=<es-query>&size=N` — no auth; `/api/v1/result/<uuid>/` now returns `{"warning":"You're not logged in!"}` anonymously (changed — was open).
- `GET https://webhook.site/token/<uuid>/requests` — 404 = expired inbox (clean negative, cheap to check).

## Open follow-ups (updated 2026-10-05 ~12:55 UTC)
- AI Village UA mining — blocked on HF token re-supply (user action)
- Shodan/FOFA/VirusTotal/AbuseIPDB — blocked on API keys (user supplies)
- ANY.RUN / Hybrid Analysis / CheckPhish / Zscaler Zulu — browser lane (JS-walled)
- webhook.site — standing re-sweep every run; **also sweep `sslip.io`/`nip.io` UUID-pathed beacon URLs** (new shape from June-21 corpus)
- `v.gd/MassCountyData007` lead — still open
- OTX deep lane — **still 429**; retry next run after longer backoff (passive_dns 4 overlaps + is.gd full pull)
- New grammar watch: `vfy20261005*` (verify phase), `nested2026100*` (nested-flow), `claude*` per-model variants; new POI `B024F04YSV`; new `<word>legacy` watchlist unchanged
- **New lead → new-fleets lane**: tronzap.com + lhr.life tunnel cluster (Sep 26 API-submit burst, eval-stdin.php on the dashboard) — payment-infra shape, unknown operator
- `urlcap.com scankey` / `pingllo.com` — still open (OTX zero, Pulsedive 404)
