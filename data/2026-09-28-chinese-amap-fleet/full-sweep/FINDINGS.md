# Full-Court Press Sweep — FINDINGS (running synthesis, 2026-10-05)

**Objective**: hunt EVERYTHING we know for signs of undiscovered agent/swarm fleets.
**Doctrine**: metadata tells the story; agents and swarms only; misfits are leads, never negatives.
**Known/excluded**: Amap/`uq` operator (mapped); tronzap campaign (noted lead, not a track).

## Lead-deepening follow-ups (2026-10-05, post-sweep — coordinator fan-out, all 3 lanes complete)

### Lead A: ZeroSSL programmatic issuance — INDEPENDENT, not fleet-adjacent
`full-sweep/raw/lead-zerossl-followup.md` (CertSpotter JSON: `raw/ct_zerossl_certspotter_2026-10-05.json`)
- crt.sh was down for the whole run (6 attempts, backend-wide 502s/timeouts) — pivoted to CertSpotter's keyless CT API (`/v1/issuances?domain=lhr.life&include_subdomains=true&expand=dns_names&expand=issuer`; dedupe by `tbs_sha256`; history only to 2026-05-31). **Reusable endpoint documented in the file.**
- **7 ZeroSSL tunnel names in 2026-05-31→10-03 window** (9 unique ZeroSSL certs), incl. **2 the prior sweep missed**: `a7bfa19dd56391` (2026-09-10), `ca990e9a89525d` (2026-09-22). Minimum 11 distinct ZeroSSL names total incl. the 4 pre-2026 ones whose names are unrecoverable while crt.sh is down.
- **Programmatic fingerprints**: `deab0fff603d04` (Oct 2) and `0418f1e395a48e` (Oct 3) each got dual RSA+ECC ZeroSSL certs same-day; `92f1f5cd378431` switched LE→ZeroSSL overnight; `93ca25e80716ce` (Oct 3) got **3 certs from 3 CAs in one day** (LE YE2 + LE YR1 + SSL.com). ECC intermediates appear only from Oct 2 — a tooling/config change.
- urlquery (keyless htmx): **0 reports for all 8 names**; 0 local corpus hits; 0 indexed-web hits. **Zero overlap** with the 78 fleet tunnel names from `writeup-lhr-life.md`; names are uniform random 14-hex, no fleet grammar markers.
- **Verdict: INDEPENDENT.** Same tunnel service, zero shared names, zero urlquery presence (fleet tunnels *do* get scanned — that's where the 78 names came from), and the fleet rides the `*.lhr.life` edge wildcard so it has no use for per-subdomain certs. Shape reads as one actor's ongoing ACME-tooling experimentation (~1–2 certs/week since Aug, RSA+ECC/multi-CA tests Oct 2–3), active since at least 2023.
- Infra note from this lane: `uq_htmx.py` is broken on this VM (python urllib dies in the proxy CONNECT tunnel) — curl against the same htmx endpoint works; VM egress proxy intercepts DNS (198.18.0.x), so liveness checks were inconclusive, recorded as unanswered.

### Lead B: urlscan-as-fetch-engine tronzap — different eval/task family, shared provider toolkit
`full-sweep/raw/lead-urlscan-tronzap.md`
- **38 scans confirmed**, 7 distinct tunnel hosts, 16:44–18:27 UTC 2026-09-26. Tunnel pages are exploit-module test names: `o-rc-{semi,php,nl,dollar}` (orders RCE payload encodings), `c-rc-{php,mustache}` (calculate RCE), `k-ext-{semi,ssti}` (SSTI on check), `ev/ev2/e0/e1/e3/e4` (eval-stdin iterations), plus interleaved direct probes: CVE-2017-9841 path variants **incl. IDN-homoglyph WAF bypass** `vendor/phpunıt/` (U+0131), Laravel Ignition `execute-solution` (CVE-2021-3129), Livewire, source-disclosure (`?-s`, `composer.lock`, `.git/config`, `laravel.log`), `phpinfo.php`, `_debugbar`, `.env`.
- **Sep-29 follow-on found**: direct subdomain enum (`bo`, `dev-bo`, `devbo`, `ref`, `dev`, `dev-dash`, `dev-api`) self-tagged **`87270ca9ac10`** — same actor back 3 days later; 2 fresh tunnels liveness-checked (503).
- **Fleet overlap: 0/7 Sep-26 hosts and 0/3 Sep-29 hosts** vs the 78 known fleet hosts. Zero fleet markers in any name or tag.
- **Verdict: different eval/task family on shared provider toolkit** ("same provider, different agents, different evals") — identical tunnel grammar, server banner, AWS pool, and urlscan-fetch-engine technique; exploit (not map-collection) task family; disjoint tunnel sets. Same-operator vs different-actor unresolvable on current evidence.
- Gaps: urlscan result-detail API 403s from this fetch path (payload bytes unread — **highest-EV follow-up: needs browser-capable agent or urlscan account**); ~305 of 405 `domain:tronzap.com` results unseen anonymously; Sep-29 tunnels + `87270ca9ac10` are watch items.

### Lead C: Dream Security Taiwan swarm — cleanly separate operation
`full-sweep/raw/lead-dreamsec-crosscheck.md`
- Incident confirmed across 7 sources: Jul 1–4, 2026, 12 attack waves, up to 8 parallel sub-agents (self-labeled A–Q), Hermes + OpenClaw, DeepSeek-V4-Flash implicated, 160MB/1,395-file operator workspace recovered, disclosed Aug 12; 85 accounts compromised, 2,500+ personnel records exfiltrated, expansion to nuclear safety agency + 7+ energy companies. **Dream published no IOCs/hashes** — cross-check was string-level by necessity.
- **15 corpus indicators → 0 hits** in 2,141 records (controls healthy: amap 2,141, uqscan 1,136). Corpus window (Sep 28–Oct 5) doesn't cover the incident window anyway; Historian lane already ran a narrower version with the same negative.
- **Verdict: separate operation.** Zero TTP/infra/string overlap; disjoint missions (offensive intrusion + persistence vs bulk Amap map collection); Dream reporting mentions no tunnel providers; no `oai*`/epoch-nonce provider markers linking it to the OpenAI-attributed swarm either. Chinese attribution + commodity open-source frameworks are the only shared dimensions — and Hermes recurs across ≥5 separate Jul–Sep 2026 campaigns, arguing against framework-as-linkage.
- **Naming trap flagged**: three distinct "Hermes" labels in reporting (open-source framework, hackathon's hermes-agent host, Telegram-controlled "Hermes Agent" in Unit 42's Jul 30 report) — do not merge.
- ntfy.sh: still blocked from this VM (curl timeout, `ir_blackhole_ntfy_sh` policy) — open lead for an unblocked network. Confirmed via GitHub that `valenvivaldi/friendlyagents` is a real Claude Code hook publishing to the public topic.

### Lead refinement (coordinator, local verification): CIRCL/Maltrail sightings = known fleet, independently observed
- Of the 5 May-2026 Maltrail-trail `<hex>.lhr.life` names, exactly **1 (`87e0bbc636999b.lhr.life`) is a known fleet tunnel** — sighted in our corpus 2026-05-19 and in the CIRCL trail 2026-05-16/17 (contemporaneous). Fleet tunnel reference list: 78 names extracted from `writeup-lhr-life.md` (note: `events.jsonl` carries zero `lhr.life` entries — it holds venue findings only; the writeup is the authoritative tunnel list).
- **Revised reading**: Maltrail independently sighted the known fleet's May-2026 tunnel set (plus possibly fleet tunnels our corpus missed), classified under `hacked_npmrepos`/`metasploit` trail tags. Independent corroborating sighting of the KNOWN fleet — not a new fleet. Zero overlap with the ZeroSSL names above.

## Completed surfaces

### Paste services — CLEAN NEGATIVE (2/19)
`full-sweep/raw/paste-services.md`
- rentry.co (no search API; site: searches), pastebin.com, ix.io/termbin/0x0.st, paste.rs/hastebin: zero hits on `uqscan`, `pandalegacy`, `lhr.life`, `sub_poi_navi`.
- pastebin `webhook.site agent harness` → 11 noise pastes. `r.jina.ai agent` → 1 hit: spam-wrapped copy of public OpenDeepResearcher (Matt Shumer) harness — known public tooling, not a fleet.
- **Marker caution**: `pandalegacy` is a hard name collision (Fortnite Creative creator) — keep service-scoped only.
- Blind spot: Privatebin (encrypted-by-default, unsearchable).

### Social search — CLEAN NEGATIVE + 1 LEAD (3/19)
`full-sweep/raw/social-search.md`
- `social.search` backend timed out; reran via `browser.search` (web, not native social — recommend native re-run later).
- `uqscan`, `uqcors`, `pandalegacy`, `sub_poi_navi`, `tronzap`: clean negatives. Amap fleet has ZERO public echo — the swarmcha.se report is unreferenced anywhere.
- `lhr.life`: commodity agent infra (kolonie-ai issue #585, pokemon-player SKILL.md files instruct agents to open localhost.run tunnels). Adjacent, not a fingerprint — zero Amap/uqscan co-occurrence.
- **LEAD — Dream Security / Dream Research Labs separate Chinese-attributed agent swarm**: 8 agents, July 1–4, Hermes + OpenClaw frameworks, Simplified/Traditional Chinese log split, recon on 21 Taiwan government systems, 160MB workspace recovered (via webpronews.com). Offensive tradecraft, NO Amap-marker overlap. Naming caution: "Hermes" = open-source framework, not the hackathon's hermes-agent. **Action**: cross-check against our urlquery corpus for shared infra.

## All 19 surfaces complete.

### Trick: url scanners + intel DBs — CIRCL sights fleet tunnel shape (14/19)
`full-sweep/raw/trick-url-scanners.md`
- **Lead**: CIRCL OSINT MISP feed (open, no account) independently sights the known fleet's tunnel shape — two May-2026 Maltrail daily-IOC events list `87e0bbc636999b.lhr.life`, `b94b6bcfa27554.lhr.life`, `d8b498f1781bc2.lhr.life`, `bbc45e9f547785.lhr.life`, `edcf8b03c84634.lhr.life` — tagged `hacked_npmrepos`/`metasploit`, not map-collection. Infra reuse or tag misclassification; no `uqscan=`/`uqcors` in 293 CIRCL 2026 events.
- Open+clean: PhishStats (50/day anon), MISP feeds. YARAify `lookup_hash` unexpectedly answers WITHOUT Auth-Key (anonymous hash oracle — documented). Gated: abuse.ch family (401, free key at auth.abuse.ch — highest-value unlock), Kaspersky OpenTIP, MetaDefender, PhishTank, ThreatBook. Hard-gated: Hatching Triage.

---

## Final tally (updated 2026-10-05 after lead-deepening)

**New species found: 0.** No undiscovered agent/swarm fleet surfaced on any of the 19 surfaces, and all 3 lead-deepening follow-ups resolved WITHOUT a new species:
1. **ZeroSSL issuance (Lead A)** → INDEPENDENT actor's ACME-tooling experimentation, not fleet-adjacent (zero name/urlquery/corpus overlap; fleet rides the edge wildcard).
2. **urlscan tronzap-as-fetch-engine (Lead B)** → different eval/task family on the shared provider toolkit ("same provider, different agents, different evals"): exploit-module testing (PHPUnit RCE incl. IDN-homoglyph WAF bypass, Laravel Ignition, source-disclosure), 0/10 host overlap with the 78 fleet names, Sep-29 follow-on self-tagged `87270ca9ac10`. Same-operator vs different-actor unresolvable; payload bytes unread (urlscan 403) — highest-EV follow-up needs a browser-capable agent or urlscan account.
3. **Dream Security Taiwan swarm (Lead C)** → cleanly separate operation (0/15 corpus indicators; no shared TTP/infra; no provider markers). Hermes-recurrence across ≥5 campaigns argues against framework-as-linkage.
4. **CIRCL/Maltrail lead REFINED** → 1 of 5 trail names is a known fleet tunnel (corpus 05-19 / trail 05-16–17, contemporaneous): independent corroborating sighting of the KNOWN fleet's May-2026 tunnels, misclassified under `hacked_npmrepos`/`metasploit` trail tags — not a new fleet.

**What the sweep actually yielded:**
1. **Operator timeline extension** (corpus re-mine): June 2026 AIHW strand (`uqtag=AGEDATA23`, `vizprod.aihw.gov.au`) — R&D predates Amap by 3.5 months. Single pipeline confirmed via exit_node (2 values, 2,159 reports).
2. **New infrastructure for known swarm** (shorteners): tinyurl.com as live swarm storage (Korenblit link-list burst).
3. **Leads (resolved 2026-10-05)**: (a) CIRCL Maltrail May-2026 tunnel sightings → independent corroborating sighting of the KNOWN fleet (1 of 5 names matches; misclassified under `hacked_npmrepos`/`metasploit` tags); (b) ZeroSSL-issued tunnel certs → independent ACME-tooling experimentation, not fleet-adjacent; (c) urlscan-as-fetch-engine tronzap PHPUnit-RCE probing (38 scans, 09-26; IDN-homoglyph WAF bypass; Sep-29 follow-on self-tagged `87270ca9ac10`) → different eval/task family on shared provider toolkit, payload bytes unread (urlscan 403); (d) Dream Security Taiwan-gov 8-agent swarm (Jul 1–4) → cleanly separate operation, 0/15 corpus indicators; (e) Cloudflare Radar 16-hex tunnel (08-01) — still open; (f) ntfy.sh/friendlyAgents public agent-status topic — still blocked from this VM; (g) PHPUnit-RCE tronzap follow-up: pull result pages for POST payload grams via browser-capable agent or urlscan account; (h) same-minute casino cluster at ltzh burst — open, needs keyed API.
4. **Structural findings**: CT blind to fleet tunnels (wildcard edge cert); lhr.life is default agent dev-tunneling (grammar, not domain, discriminates); 106.11.226.79/47.246.165.44 are Amap's own ingress (targets, not C2); Glitch + transfer.sh dead; YOURLS instances gating stats post-CVE-2026-63135.
5. **Reusable endpoints** (XHR doctrine): urlquery htmx, Sourcegraph SSE search, s.id keyless shorten, da.gd/clck.ru/t.ly/bit.ly reveals, Gist search, archive.today URL-search, ghostarchive WARC endpoint, Megalodon `?url=`, crt.sh params, Yandex suggest API, GreyNoise community, ip-api, YARAify anonymous lookup_hash.

**Open gaps needing live-browser or creds**: Naver search, Megalodon free-word search, ZoomEye/Quake/ThreatBook accounts, abuse.ch Auth-Key, Kaspersky OpenTIP free token, PhishTank archive, urlscan wildcard search (account), Baidu session, ntfy.sh poll (runtime blackhole).

### Web archives — CLEAN NEGATIVE (1/19)
`full-sweep/raw/archives.md`
- Wayback CDX + Arquivo.pt (CDX + full-text) + Common Crawl: `uqscan=`, `uqcors.html`, `sub_poi_navi`, is.gd slugs, `webhook.site`+amap → clean negatives. `pandalegacy` = Fortnite noise only.
- `lhr.life` → 100 captures, 4 hex subdomains — all consumer exposures (Stable Diffusion WebUI 2023, Snapchat cookie page, Hikka userbot panel, qBittorrent login), none in fleet window. Proves the surface has recall for tunnel-using fleets.
- Endpoint inventory: Wayback CDX (1 req/45s budget), arquivo.pt/wayback/cdx (`filter=` silently ignored), arquivo.pt/textsearch, CC Index (regex filter unreliable). Megalodon still needs live-browser.

### Trick: pastes/gists + extra archives — CLEAN NEGATIVE (17/19)
`full-sweep/raw/trick-pastes-archives.md`
- Gists (content search — strong negatives): `uqscan`, `uqcors`, `pandalegacy`, `sub_poi_navi` zero; `lhr.life` ~700 triaged to 12, all benign. pastebin archive, PrivateBin (structural negative), hastebin (dead): clean.
- archive.today: 37 `lhr.life` subdomains archived — all benign user tunnels (torrent indexes, mirrors, blogs), including Oct 2026 captures. ghostarchive: 1 capture (meme-media server, pulled raw WARC). cachedview: dead.
- Takeaway: fleet markers appear in zero public pastes/gists/archive captures — consistent with ephemeral tunnels + unpublished configs.
- Undocumented endpoints documented: Gist search pagination, archive.today URL-search + offset, ghostarchive `/chimurai4/<id>.warc`.

### GitHub code — CLEAN NEGATIVE (3/19)
`full-sweep/raw/github-code.md`
- No public code contains fleet markers (`uqscan=` zero; `uqcors` = base64-blob false positives; `pandalegacy`, `sub_poi_navi` zero). GitHub code search UI is sign-in gated with no unauthenticated XHR path.
- **Reusable endpoint**: Sourcegraph public search stream (`sourcegraph.com/.api/search/stream?q=…&v=V3`, SSE) — unauthenticated code search. grep.app 429'd (hard stop, documented retry).
- Adjacent: `zhouyoukang1234-spec/devin-remote` (Chinese-authored agent remote-access app with Go SSH reverse-tunnel provisioning `*.lhr.life`); `messageboardauditbench` documents agents hitting a wiki board via `504c4580fe50f1.lhr.life` (2026-06-17).

### Russia surfaces — CLEAN NEGATIVE (12/19)
`full-sweep/raw/russia-surfaces.md`
- Yandex SERP anti-bot gated (not bypassed); fell back to public Yandex Suggest API — zero completions for all markers (no Russian search footprint). Telegram (SecLabNews etc.): zero marker hits. RU forums/pastebins/media: clean; media covers only known Transluce/OpenAI incidents.
- Adjacent: Russian Telegram-bot devs use lhr.life for Mini App webhooks (commodity, not fleet-shaped). Reusable endpoints documented (Yandex suggest API).

### Certificate Transparency — structural blind spot + live lead (5/19)
`full-sweep/raw/cert-transparency.md`
- **CT is structurally blind to this fleet's tunnels**: localhost.run terminates TLS at its edge with a wildcard `*.lhr.life` cert (Amazon ACM, renewed annually). 0 of 83 known fleet subdomains in CT (verified real zeros). Absence of certs ≠ absence of activity.
- **Live lead**: 9 tunnel names with ZeroSSL-issued certs (API-driven, anomalous vs LE norm), 3 in the last 3 days (10-02, 10-03), ZERO overlap with known 83 — someone is programmatically issuing certs for tunnel subdomains right now. Needs urlquery/DNS cross-check.
- trycloudflare: 2021 burst (fleet-shaped, historical), dead since 2021-07. ngrok per-tunnel certs ended 2019. Tailscale: internal CA, not publicly logged (second blind spot). `%.amap.com`: clean negative (all Alibaba first-party).
- crt.sh machine interface documented: `GET crt.sh/?q=<pattern>&output=json`, 5,000-row cap, 8–15s pacing.

### Trick: fetch proxies — CLEAN NEGATIVE + tronzap lead deepens (13/19)
`full-sweep/raw/trick-fetch-proxies.md`
- All 10 proxies clean on public logs (none keep any; corsproxy.io now key-gated). codetabs documented as agent Jina-fallback in browser-agent-skills. Full endpoint/param map in file.
- **LEAD**: 38 urlscan scans (2026-09-26) probing tronzap.com for **PHPUnit RCE** (`vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php` — classic CVE-2017-9841 vector), submitted as `<hex>.lhr.life` tunnel pages POSTing from urlscan's browsers — **urlscan.io used as the fetch engine**. Same tunnel grammar as known fleet, exploit targets not map collection. Follow-ups: pull result pages for POST payload grams, diff tunnel hosts, urlscan account for wildcard searches.

### Trick: dead-drops + messaging — CLEAN NEGATIVE, 2 actionable (19/19)
`full-sweep/raw/trick-deaddrops.md`
- No new agent/swarm hits. Pipedream/RequestBin now need signup; requestcatcher public-by-subdomain (no index); Beeceptor/mocky/jsonblob no public logs; telegra.ph marker searches 0; Gotify no public instance; Discord no public webhook log.
- **Lead**: `ntfy.sh/friendlyAgents` — PUBLIC topic where `friendlyagents`/`agent-deck` Claude Code tooling publishes structured agent status messages. Blocked from this VM (runtime blackhole) — poll path for unblocked network: `https://ntfy.sh/friendlyAgents/json?poll=1`.
- **New surface**: `stash.legible.sh` — "topic-addressed artifact mailbox" (soft-launched ~Jul 2026), public-by-topic, no auth, purpose-built for agent-to-agent drops. Zero corpus hits today — add to watched surfaces.
- Marker greps across all four corpora: 0 for every trick-class marker (absences genuine).

### Shodan/FOFA — IPs are Amap's own, not operator boxes (7/19)
`full-sweep/raw/shodan-fofa.md`
- **106.11.226.79** → `ea119-static.wagbridge.ingress.amap.com.gds.`, AS37963 (Alibaba). **47.246.165.44** → `os30.wagbridge.ingress.amap.com.gds.`, AS45102 (Alibaba US/SG); Tengine 404 leaks `gaode-aserver-ingress…` (高德=Amap). These are the fleet's TARGETS (urlquery IP/ASN = target's resolved IP), not C2. Consistent with data-collection thesis.
- GreyNoise: neither IP scanning. No harness traits. localhost.run exits are AWS — no match; tunnels are the operator surface, Alibaba IPs the scrape targets.
- Blocked-not-negative: Shodan /search login-walled, FOFA fully auth-walled. Reusable no-key endpoints documented (Shodan host pages, GreyNoise community, ip-api, HackerTarget, urlscan ip: search, DoH, crt.sh).

### Regional surfaces — CLEAN NEGATIVE (10/19)
`full-sweep/raw/regional-surfaces.md`
- 8 regional sandboxes checked: virscan (file/hash only), ThreatBook (JS WAF), habo.qq.com (unreachable), Kaspersky OpenTIP (needs free registration — **recommended follow-up**, only non-Western URL index found), Dr.Web/dfndr/Intezer/Axur (no minable index). Regional pastebins + threat intel: clean.
- **Key insight**: lhr.life is DEFAULT AI-agent dev tunneling (godot-mcp v5.0.33 markets "Unblocked for External AI Agents" via localhost.run; pokemon-agent skill forks instruct `ssh -R … nokey@localhost.run`). The fleet's tunnels blend into heavy benign agent traffic — **the `uq` query grammar, not the tunnel domain, is the discriminating marker**.

### Trick: screenshots + staged programs — CLEAN NEGATIVE (16/19)
`full-sweep/raw/trick-screenshots-staged.md`
- No screenshot service has a public gallery/searchable history (screenshotone, urlbox, browshot, thum.io, WP mshots — all forward-addressable only). CodePen/Observable searchable without account (no keyless JSON API); JSFiddle/StackBlitz/Replit/Vercel/Netlify not searchable. All marker searches clean.
- **Glitch is DEAD** (hosting ended 2025-07-08) — archival surfaces only.
- Corroboration: `injectPageScript` is a documented Jina Reader API parameter — matches ltzh-family TTP.

### Corpus re-mine — ONE operator + timeline extension (6/19)
`full-sweep/raw/corpus-remine.md`
- **Single pipeline confirmed**: only 2 `settings.exit_node` values across 2,159 reports; every exotic UA and all 36 `uq*` param names sit on the same node, interleaved in the same hours. No second fleet hiding in our corpus. Bursts: clean negative. Integration: 0 gaps.
- **PAYOFF — 9 unseen `uqtag` reports via htmx**: (1) **June 2026 AIHW strand** — 4 reports (2026-06-20), httpbun/base64 payloads embedding a Tableau module from `vizprod.aihw.gov.au` (Australian gov health) with `uqtag=AGEDATA23` — operator's R&D dates to June, 3.5 months before Amap. (2) `probe2-start` / `qjprobe-start` siblings with XOR-obfuscated Image-beacon exfil.
- **Open lead**: 6 casino domains at the exact ltzh burst minutes (12:58/13:08/13:15) — bare domains, no grammar, attribution needs keyed API.
- Follow-ups: keyed-API settings pull for the 9 (UA/exit_node match = same operator), wider htmx sweep of `uqtag`/`probe2`/`qjprobe` titles, resolve casino cluster.

### Trick: shorteners — NEW FOOTPRINT for known swarm (18/19)
`full-sweep/raw/trick-shorteners.md`
- **Confirmed: tinyurl.com is live swarm storage.** `tinyurl.com/2xz74jv4` → Wayback clarku.edu PDFs, matching the Korenblit link-list's 2026-06-18 storage burst (`2xz74jv4`/`2xhcux8g` → pure.md relay → Wayback PDFs). Known swarm's shortener usage extends beyond is.gd/v.gd. Not a new species — new infrastructure for a known swarm.
- YOURLS: uoft.me (Univ. of Toronto) new — agent keywords `maagentxyz99999` (1,784 hits), `zzagent740558`, 2026-06-18; stats now login-gated. 12 instances mapped; goto.unm.edu remains the open Rosetta stone. Trend: instances gating stats post-CVE-2026-63135.
- **7 undocumented/keyless endpoints**: s.id `POST /api/public/link/shorten` (keyless XHR), da.gd `/<slug>+` reveal (live), clck.ru `POST /--` (no-key shorten), t.ly `<slug>+`, bit.ly `<slug>+` stats, preview.tinyurl.com.
- Markers (`uqscan`/`uqcors`) × 5 shorteners = 0 hits. chilp.it pivoted (no stats API), gg.gg defunct, CN shorteners unverified (egress-limited).

### Japan archives — CLEAN NEGATIVE + 1 lead (9/19)
`full-sweep/raw/japan-archives.md`
- Megalodon (`?url=` lookups for uqcors.html, probe pages, Amap uqscan URLs) + gyo.tc (alias backend): zero captures. Japanese web: no researcher coverage of the fleet.
- **Lead**: Cloudflare Radar's public URL-scanner feed shows `91b9ec611bbd73.lhr.life` — 16-hex tunnel, operator's shape — scanned 2026-08-01, US/AS14618, bare root, no uq markers. Attribution open; needs Radar detail-page follow-up.
- Reusable endpoints documented: `GET megalodon.jp/?url=<encoded>`, `GET gyo.tc/<full-url>` (no auth on lookups).
- Blockers: curl egress dead for this agent; Megalodon free-word keyword search needs live-browser delegation (spec in file).

### China surfaces — BLOCKED mostly, 1 harness lead (8/19)
`full-sweep/raw/china-surfaces.md`
- ZoomEye, Quake, ThreatBook: all login/token-gated, no unauthenticated XHR found. Baidu: 1 query OK (`uqscan` → clean negative), then anti-bot wall. Weibo/Zhihu: JS/403 walls; site: searches → zero marker hits.
- **Lead**: `github.com/bebabinlarsson-blip/Godot-MCP` v5.0.33 — AI-agent MCP harness with `*.lhr.life` as DEFAULT tunnel provider ("Unblocked for External AI Agents"), 25s keep-alive daemon. Same infra family, different operator. Suggest: sweep GitHub/MCP repos pinning lhr.life.
- Needs: ZoomEye/Quake/ThreatBook creds, live Baidu session, VM curl-egress repair (this agent's direct curl was dead).

### Trick: tunnels + file drops — CLEAN NEGATIVE, intel yield (15/19)
`full-sweep/raw/trick-tunnels-filedrops.md`
- No public index of active/past tunnel URLs exists for ngrok, cloudflared quick tunnels, bore/bore.pub, zrok, inlets, sish — by design. No public file listing for file.io, 0x0.st, catbox.moe/litterbox. All markers clean in web search.
- Intel: **transfer.sh is DEAD** (down Jul→Oct 2026, shutdown noted Sep 2026). Agent skill repos document tunnel/drop affinity: bore.pub for TCP (dodge ngrok card requirement), litterbox baked into agent temp-file skills, cloudflared emits agent-parseable JSON URLs, `themajc/agent-skills` publish-to-trycloudflare.
- Caveat: this agent's VM curl egress was broken (even google.com timed out); crt.sh, Common Crawl, Wayback CDX queries couldn't complete — retry leads noted in file.

### Korea surfaces — CLEAN NEGATIVE (11/19)

## Undocumented endpoints found
(None yet — trick agents carry the XHR-hunting doctrine.)
