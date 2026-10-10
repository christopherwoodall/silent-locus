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

### Lead D: Cloudflare Radar 16-hex tunnel — UNRESOLVED, fleet-adjacent, not attributable
`full-sweep/raw/lead-radar-tunnel.md`
- Scan row re-verified: `https://91b9ec611bbd73.lhr.life/`, no classification, **2026-08-01 11:34 UTC** (frontend hardcodes UTC — corrects japan-archives.md's "likely JST" guess), US/AS14618, Finished. Surfaced only on ~64-day-old Google-indexed Radar listing snapshots.
- **Fits operator's tunnel convention** (16-hex `lhr.life`, 2026 window, US cloud egress); lands 8 days after the known fleet's Jun 21–Jul 24 sighting cluster. But: disjoint from all 78 known fleet names and every corpus inventory (repo-wide greps: name exists nowhere else in silent-locus except the two lead records); scanned URL is bare `/` with no `uq`-grammar markers; marker sweep of Google-indexed Radar pages (`uqscan`/`uqcors`/`uqtag`, `pandalegacy`, `sub_poi_navi`) → 0 (index-coverage caveat).
- **Verdict: fleet-adjacent, not attributable.** Scan detail page unreachable without a live browser or Cloudflare API token: the widget-data XHR (`GET /charts/<WidgetId>/fetch`) 403s to curl/text-fetch behind a bot-wall. Documented endpoints for reuse: `/scan?url=`, `/scan/search?q=&type=`, `/scan/<uuid>/summary`, and the account-gated `.../accounts/{id}/urlscanner/v2/search` (ElasticSearch-ish syntax). Browser-capable delegation spec written in the file (pass bot check → `/scan/search?q=91b9ec611bbd73.lhr.life&type=url` → `/scan/<uuid>/summary`, then run fleet markers against the `/charts/` XHR).

### Corpus-remine corrections (2026-10-05, from htmx-extended lane)
- The AIHW-sibling title is **`qprobe-start`**, not `qjprobe-start` (decoded from base64 payload); "qjprobe" appears nowhere in corpus or htmx — honest zero. The claimed 09-01 `probe2-start` was vimeo spam (no such report).
- `uqtag=` is a URL query param appended AFTER the payload, not inside it. The prior sweep's 300-char anchor regex under-surfaced the AIHW series (4 of 27); the fixed regex recovers all 27.
- htmx search is a partial recent-window view (`q=uqscan` returned only the newest ~45 hits) — corpus remains the source of truth for Amap terms.

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

## Coverage map — 23 lanes (2026-10-05)

**Covered (clean negative or resolved):** web archives (1), paste services (2), GitHub code (3), social search (4), Certificate Transparency (5), corpus re-mine (6), Shodan/FOFA (7), China surfaces (8), Japan archives (9), regional surfaces (10), Korea surfaces (11), Russia surfaces (12), trick: fetch proxies (13), trick: url scanners + intel DBs (14), trick: tunnels + file drops (15), trick: screenshots + staged programs (16), trick: pastes/gists + extra archives (17), trick: shorteners (18), trick: dead-drops + messaging (19), trick: stash.legible.sh (20), htmx extended sweep (21).

**Partial (real signal but follow-up open):** corpus re-mine (keyed `settings` pull + casino cluster still keyed-only), Kaspersky OpenTIP (22 — surface mapped, gated; markers queued for keyed run), Radar 16-hex tunnel lead (fleet-adjacent, detail bot-walled), urlscan tronzap lead (payload bytes unread).

**Gap (no coverage — needs delegation):** Naver search (text-fetch anti-bot wall; browser-capable agent needed); Megalodon free-word search (live-browser); ntfy.sh poll (VM runtime blackhole — needs unblocked network); ZoomEye/Quake/ThreatBook (accounts); urlscan wildcard search (account); abuse.ch Auth-Key (free registration); PhishTank archive; Baidu session; `lhr.life` subdomain htmx search (done 2026-10-05: 216 subdomains, 4 candidate-grade Jan-2026 bare-root tunnels); legible.sh primitives sweep (`slate`/`relay`/`gate`/`bigred` first — done 2026-10-05: all 9 clean negative; re-probe slate/mutex/quorum/relay when a topic name is recovered); devin-remote disappearance check (browser-capable delegation); `c7a1f824a6efc4.lhr.life` deployment watch; `domain:onlytron.com` pre-Sep-29 lookback (30-day urlscan anonymous window); corpus integration of 9 new candidates (AGEOUT1B + 4 uqtarget + 4 Jan-2026 tunnels); Common Crawl 9×504 retry (inconclusive, not negative).

### Trick: url scanners + intel DBs — CIRCL sights fleet tunnel shape (14/19)
`full-sweep/raw/trick-url-scanners.md`
- **Lead**: CIRCL OSINT MISP feed (open, no account) independently sights the known fleet's tunnel shape — two May-2026 Maltrail daily-IOC events list `87e0bbc636999b.lhr.life`, `b94b6bcfa27554.lhr.life`, `d8b498f1781bc2.lhr.life`, `bbc45e9f547785.lhr.life`, `edcf8b03c84634.lhr.life` — tagged `hacked_npmrepos`/`metasploit`, not map-collection. Infra reuse or tag misclassification; no `uqscan=`/`uqcors` in 293 CIRCL 2026 events.
- Open+clean: PhishStats (50/day anon), MISP feeds. YARAify `lookup_hash` unexpectedly answers WITHOUT Auth-Key (anonymous hash oracle — documented). Gated: abuse.ch family (401, free key at auth.abuse.ch — highest-value unlock), Kaspersky OpenTIP, MetaDefender, PhishTank, ThreatBook. Hard-gated: Hatching Triage.

---

## Final tally (updated 2026-10-05 after lead-deepening + respawn lanes)

**New species found: 0.** No undiscovered agent/swarm fleet surfaced on any of the 28 lanes, and all 4 lead-deepening follow-ups + the 5 post-sweep fan-out lanes resolved WITHOUT a new species:
1. **ZeroSSL issuance (Lead A)** → INDEPENDENT actor's ACME-tooling experimentation, not fleet-adjacent.
2. **urlscan tronzap-as-fetch-engine (Lead B)** → different eval/task family on the shared provider toolkit.
3. **Dream Security Taiwan swarm (Lead C)** → cleanly separate operation.
4. **CIRCL/Maltrail lead REFINED** → independent corroborating sighting of the KNOWN fleet's May-2026 tunnels (1 of 5 names matches).
5. **Cloudflare Radar 16-hex tunnel (Lead D)** → UNRESOLVED: fleet-adjacent (shape/window/egress fit) but not attributable — disjoint from all 78 fleet names, bare-root scan, detail bot-walled.

**What the sweep actually yielded (cumulative):**
1. **Operator timeline extension** (corpus re-mine): June 2026 AIHW strand (`uqtag=AGEDATA23`, `vizprod.aihw.gov.au`) — R&D predates Amap by 3.5 months. Single pipeline confirmed via exit_node (2 values, 2,159 reports).
2. **AIHW strand extended 4 → ~27 reports (respawn lane)**: numbered `uqtag=` R&D sequence AGEMARK3→AGEVS25 against AIHW Tableau modules (2026-06-20), incl. `onmousemove` handler and window.open exfil beacon payloads.
3. **Two new June-2026 `.lhr.life` tunnel lanes**: `7e7ff6dbbe9824.lhr.life` (`uqcors.html?v=1` CORS probes, Jun 18); `91ef9fc4c82a1b.lhr.life` (`probe2.html` nonce probes, Jun 21).
4. **Operator still active**: 12 NEW Oct-05 reports (01:43–04:11 UTC) on Qingdao-museum POIs with fresh tag families (`qingdaomuseum20261005b`, `henanmuseum_20261005a`, …).
5. **New infrastructure for known swarm** (shorteners): tinyurl.com as live swarm storage (Korenblit link-list burst).
6. **New lead**: 9 zero-coverage legible.sh no-auth agent-infra primitives (`slate`, `relay`, `gate`, `bigred` swarm-coordination-shaped) — sweep pending.
7. **Structural findings**: CT blind to fleet tunnels (wildcard edge cert); lhr.life is default agent dev-tunneling (grammar, not domain, discriminates); 106.11.226.79/47.246.165.44 are Amap's own ingress (targets, not C2); Glitch + transfer.sh dead; YOURLS instances gating stats post-CVE-2026-63135; htmx search is a partial recent-window view (corpus = source of truth for Amap terms).
8. **Reusable endpoints** (XHR doctrine): urlquery htmx (curl, not python, on this VM), Sourcegraph SSE search, s.id keyless shorten, da.gd/clck.ru/t.ly/bit.ly reveals, Gist search, archive.today URL-search, ghostarchive WARC endpoint, Megalodon `?url=`, crt.sh params, Yandex suggest API, GreyNoise community, ip-api, YARAify anonymous lookup_hash, stash.legible.sh topic API, Radar `/charts/<WidgetId>/fetch` + `/scan/<uuid>/summary`, OpenTIP `/api/v1` + `x-api-key`.

**Open gaps needing live-browser, creds, or keyed API**: Naver search (anti-bot; prior text-fetch 500s — biggest Korea gap); Megalodon free-word search; ZoomEye/Quake/ThreatBook accounts; OpenTIP token (registration decision pending; markers queued); abuse.ch Auth-Key; Kaspersky anonymous-lookup XHR (live-browser pass); PhishTank archive; urlscan wildcard search (account); Baidu session; ntfy.sh poll (runtime blackhole); Radar scan-detail UUID (browser-capable agent); tronzap PHPUnit-RCE payload bytes (urlscan 403); keyed urlquery `settings` pull for the 47 new htmx reports + 6-casino-domain ltzh burst attribution; legible.sh primitives sweep (`slate`/`relay`/`gate`/`bigred` first); `lhr.life` subdomain search not yet run.

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

## New lanes (2026-10-05, coordinator respawn — post-sweep fan-out, all 4 complete)

### Trick: dead-drop mailbox stash.legible.sh — CLEAN NEGATIVE + 1 lead (20/23)
`full-sweep/raw/trick-stash-legible.md`
- Endpoint inventory audited against the open-source `src/server.mjs` (matches docs; **zero undocumented endpoints**): `PUT`/`POST /{topic}/{filename}` (X-TTL default 24h max 7d, `X-Burn: N`) → 201 + sha256; `GET /{topic}/{filename}` (`?wait=60` long-poll, max 300s); `HEAD` metadata (never burns); `GET /{topic}` (JSON/SSE listing — nonexistent topics return 200-empty, not 404); `DELETE`; `GET /`, `/README.md`, `/llms.txt` (agent docs). Homepage fully static, no scripts/forms/XHR. No enumeration, directory, search, or feed exists by design — topics are unguessable passwords.
- Marker probes (`uqscan`, `uqcors`, `pandalegacy`, `sub_poi_navi`, `uqtag`, `probe2`, `qjprobe`, `AGEDATA23`, `httpbun`) → all 200, all empty, burn counters untouched. Sourcegraph code search: 0 matches for `stash.legible.sh`. URLQuery corpora greps: 0.
- **LEAD — 9 sibling legible.sh primitives, zero coverage**: `gate`, `bigred`, `trail`, `slate`, `relay`, `mutex`, `quorum`, `meter`, `tally` (all `<name>.legible.sh`, soft-launched, no-auth). `slate` (multi-agent blackboard), `relay` (work queue), `gate`, `bigred` are swarm-coordination-shaped fresh surfaces — sweep each with the same marker set.
- Standing watch note: SSE is per-known-topic only — query stash.legible.sh immediately whenever any lane recovers a topic name from code/prompts/telemetry. Caveats: TTL ≤7d and X-Burn mean empty-now ≠ never-used; self-hosted instances invisible.

### urlquery htmx extended sweep — 47 NEW operator-grade reports, operator still active (21/23)
`full-sweep/raw/htmx-extended.md`
- 10 keyless htmx queries via curl (≥13s pacing, no 429s): 55 new unique IDs = **47 operator-grade** + 8 noise. 51 hits already in-corpus.
- **AIHW strand extended 4 → ~27 reports** (2026-06-20, 08:51→12:32 UTC): a numbered R&D sequence of `uqtag=` values (3→25: AGEMARK3/3S, AGEUND4, AGEMARK5, AGEDIALOG7, AGECROSS8, MOUSETEST9, AGEEXCEL10h/10p, AGEEX11, AGETIP12p/12h/12u/12B, AGEHOVER13, AGEFILTER14, AGEOPEN15, FORMTEST123, AGEOBJ18, AGEMSG19/20, AGECROSS22, AGEDATA23/24/24B, AGEVS25) against `vizprod.aihw.gov.au` Tableau modules via pie.dev/httpbin/httpbingo/httpbun echo services. Standout payloads: MOUSETEST9 (`onmousemove` handler), AGEOPEN15 (window.open exfil beacon to `example.com/OPEN15/`). Sequence numbers 1, 2, 6 unaccounted.
- **Two new June-2026 `.lhr.life` tunnel lanes**: 8× `uqcors.html?v=1` CORS probes on `7e7ff6dbbe9824.lhr.life` (Jun 18, 8 submissions in ~60s); 4× `probe2.html?n=1782077001–704` nonce probes on `91ef9fc4c82a1b.lhr.life` (Jun 21).
- **12 NEW Oct-05 operator reports** (01:43–04:11 UTC, past corpus cutoff) with fresh tag families (`qingdaomuseum20261005b`, `henanmuseum_20261005a`, `wuxizoo20261005a`, `qdnewapi20261005a/b`, `qdoldditu20261005a`, `nested20261005b`) — **operator still active on Qingdao-museum POIs**.
- Honest zeros: `qjprobe`, `agedata`, `zz=oai` = 0 htmx hits; `pandalegacy` has in-corpus matches but the htmx tokenizer doesn't surface them.
- Open: keyed `settings` pull for the 47 new reports (would confirm June-2026 strands as same operator); 6-casino-domain ltzh burst attribution unchanged.

### Kaspersky OpenTIP — GATED, mapped (22/23)
`full-sweep/raw/opentip-mapping.md`
- **No keyless/anonymous programmatic path.** REST API `https://opentip.kaspersky.com/api/v1` (`/search/hash`, `/search/ip`, `/search/domain`, `/search/url` with `?request=`, `POST /scan/file`, `POST /getresult/file`) — `x-api-key` auth, strictly 401-gated. Web UI: SPA (4.8MB bundle) with hCaptcha; frontend maps 401=CAPTCHA, 403=RATE_LIMIT. No account created (out of scope).
- Registration requirements (live official docs): Kaspersky Account (My Kaspersky works; or email+password; or Facebook login); accept Terms + Privacy; user menu → Request token (≤1 year, immutable); token in `x-api-key`. Quota 100 req/day per 2019 article (unverified).
- Gaps: web-UI anonymous-lookup XHR unmapped (lazy chunks not served to this egress; hCaptcha unsolvable headless) — needs live-browser pass; registration decision pending. Markers queued for a future keyed run.

## Post-sweep coordinator fan-out (2026-10-05, respawn lanes 24–28)

Coverage is now **28 lanes** (23 from the sweep + 5 fan-out below). New species found: **0**. New leads recorded as leads, not tracks.

### Lane 24 — legible.sh primitives sweep — CLEAN NEGATIVE (all 9)
`full-sweep/raw/trick-legible-primitives.md`
- **All 117 live topic probes (13 topics × 9 hosts) → HTTP 200, empty state**, zero 429/403/timeouts. Marker set (`uqscan`, `uqcors`, `pandalegacy`, `sub_poi_navi`, `uqtag`, `probe2`, `qjprobe`, `AGEDATA23`, `httpbun`) + fleet-flavored names (`87270ca9ac10`, `qingdaomuseum20261005b`, `7e7ff6dbbe9824`, `91ef9fc4c82a1b`) — all empty everywhere. Probes were GET-listing only; mutating verbs deliberately untouched.
- Full route inventory audited against `src/server.mjs` @ main (ports: gate 4180, bigred 4181, trail 4182, slate 4183, relay 4184, mutex 4185, quorum 4186, meter 4187, tally 4189; index at `https://legible.sh/llms.txt`). One doc gap: quorum `GET /healthz → {ok:true}` exists in source but not the README table. Empty-topic semantics per primitive recorded in file.
- Sourcegraph keyless literal searches (`t=literal` — default type silently returns 0 even for control strings) for all 9 `"<name>.legible.sh"`: **0 matches each**. Caveat: the legible-sh org itself is not in Sourcegraph's public index, so these are third-party-only zeros.
- Caveats: empty now ≠ never used (retention: gate 7d, slate hosted keys 30d after last write, tally minute-series 24h, relay dead-letters 1k/topic); self-hosted instances invisible; reads appear to materialize empty topic state (probe footprints — future lanes note marker reuse).
- Standing watch: re-probe **slate/mutex/quorum/relay** whenever any lane recovers a topic name from prompts/skills/telemetry.

### Lane 25 — htmx `lhr.life` subdomain sweep — 141 new names, 4 candidate-grade
`full-sweep/raw/htmx-sublife.md` (34 keyless curl calls, ≥13s pacing, 0 hard stops)
- 243 reports, **216 distinct subdomains**; 75/78 known fleet names present (3 drop off the index tail). **141 new names**: 137 = pre-2026 localhost.run background noise; **4 are January-2026 bare-root tunnels** (`30b7f1be8684bc`, `cbfbac296bddb2`, `47ff7b732b053f`, `838e63e8009d67`; report IDs `ce2a4b53`, `c8462fbe`, `d4dfbf08`, `3b8a6908`; Jan 4–5 2026) — timing matches the operator's Jan-2026 onset window but no `uq` grammar, candidate-grade, unresolvable keylessly. Zero overlap with the ZeroSSL CertSpotter set (10) and the urlscan tronzap set (10) — none of those were ever submitted to urlquery. Bare-`lhr` query = substring noise only, no fallback value.
- **Missing AGE number #1 RECOVERED: `AGEOUT1B`** (`a2384890-2335-4988-81dd-1985eb31df5b`, 2026-06-20 08:39, httpbin base64, series skeleton) — series now **28 reports / 27 distinct tags**, headed by AGEOUT1B. **#2 and #6 verified absent** (8 targeted probes → literal "no reports" or noise) — honest zeros. Extended gap set: 2, 6, 16, 17, 21.
- Grammar-marker sweep: **4 new operator-grade `uqtarget` reports** not in corpus — `40c029b5`/`52f4e3e4` trailing-dot hostname R&D (tags `dot-`/`pd-dot-` on `amap-pc-ssr.amap.com.`); `7f3f95b7`/`161a0441` late-day epoch-nonce uqtarget on `example.com` (11:36, 17:38). `ltzh` "new" = known casino stratum only. **`pandalegacy` tokenizer blind spot confirmed a second time** (0 htmx hits despite in-corpus matches).
- Caveats: htmx row dates drift ~5–20 min earlier than report-page times; index most-recent-weighted, tail may extend past offset 240. Corrected a 35-char UUID typo from the prior sweep (AGEMSG19 = `000f58ed-54fa-4aa1-ab39-f116b9245775`).
- **9 corpus integration candidates** (IDs in file): AGEOUT1B + 4 uqtarget + 4 Jan-2026 tunnels.

### Lane 26 — GitHub/MCP harness sweep — 2 leads, devin-remote vanished
`full-sweep/raw/github-harness-lhrlife.md` (Sourcegraph SSE keyless; grep.app 429 = hard stop, not retried)
- godot-mcp v5.0.33 remains the only repo pinning `*.lhr.life` as default tunnel for external AI agents.
- **LEAD — `useagenthq/useagent`** (created 2026-08-29, inside fleet window): e2e test harness embedding the exact `nokey@localhost.run` → `<hex>.lhr.life` recipe — pattern-match, not attribution.
- **LEAD — `zhouyoukang1234-spec/devin-remote` now 404s** (2026-10-05): deleted/renamed/privatized within ~24h of the prior sighting. The disappearance is the lead; delegation spec for a browser-capable check recorded in file.
- No second fleet; no hex-literal or `uqscan=`/`uqcors` code hits anywhere.
- Method note: Sourcegraph `/.api/search/stream` needs `t=literal` — default type silently returns 0.

### Lane 27 — tronzap + ZeroSSL lead watch — new cert, second self-tagged actor
`full-sweep/raw/lead-watch-2026-10-05.md` (CertSpotter dump + 15 urlscan search JSONs staged in `raw/`)
- **ZeroSSL: nothing new.** One new tunnel-name cert since Oct 3: **`3281cb5f73b0c2.lhr.life`**, **Let's Encrypt YR1** (not ZeroSSL), issued 2026-10-05T09:00:46Z, fresh single-use key. Oct 2–3 multi-CA/RSA+ECC experimentation has not recurred — today's cert matches the baseline single-cert pattern. Pace: ZeroSSL-specific ~1–2/week holds; any-CA issuance has run ~1/day since Sep 28 (elevated vs Aug–Sep ~2–3/week). Name absent from the 78-name fleet list.
- **tronzap: no new activity after Sep 29.** `domain:tronzap.com` = 0 scans/day Sep 30 → Oct 5. Tag `87270ca9ac10` still exactly 7 scans, all Sep 29 — recovered detail: the tagged sweep included **`dev.onlytron.com`**, so the actor's target family is tronzap.com **+ onlytron.com**.
- **Misfit lead (not a negative): second self-tagged actor on the same family.** `domain:onlytron.com` → 25 scans, all Sep 29; tags **`xq-recon` / `xq-recon-probe`** ran a 20-scan Laravel recon sweep (`.env`, `.git/HEAD`, `_ignition/health-check`, Livewire, telescope/horizon — same playbook as the Sep-26 tronzap probes) ending ~70 min before the `87270ca9ac10` actor hit `dev.onlytron.com`. Same-or-different-actor open; target inventory must expand beyond tronzap.com.
- **New tunnel infra: `c7a1f824a6efc4.lhr.life`** — fresh 14-hex tunnel liveness-checked via urlscan on Oct 2 (bare root, untagged), absent from fleet list and all prior sets. Watch for page deployment/target.
- Sep-29 roots (`1881e623217f7c`, `2f102b0544d3b3`): no further scans, no pages deployed yet. Liveness checks unanswered (VM DNS interception, HTTPS 502) — inconclusive per method note.
- crt.sh still 502 (one check); the 4 pre-2026 ZeroSSL names remain unverifiable. CertSpotter healthy (~2 s/call).
- Coverage limits: ~305 of 405 `domain:tronzap.com` unseen (anonymous top-100 cap); CertSpotter `lhr.life` history starts 2026-05-31; urlscan result-detail 403s still block payload reads. New verified syntax: `q=task.tags:<hex>` (bare hex matches nothing).

### Lane 28 — archive resweep on new names — 20/20 honest zeros
`full-sweep/raw/archives-resweep.md`
- All 20 names (8 ZeroSSL, 7 tronzap Sep-26 hosts + 2 Sep-29 hosts, 2 June-2026 tunnels, Radar tunnel): Megalodon 20/20 negative; Wayback CDX 20/20 literal `[]` (45s pacing, ~29 min); archive.today 20/20 "No results" (recall verified on positive control `6e6d931ed3a4a8.lhr.life`, Oct-3 torrent capture); Common Crawl: 11/20 clean 404, **9/20 HTTP 504 = inconclusive, not negatives** (retryable).
- Method traps documented: Megalodon renders the `取得済みの魚拓` section heading even with zero captures — correct rule is heading present AND `見つかりませんでした` absent; archive.today `/search/?q=` answers bare 302 — follow with `-L` to `archive.ph/<host>`.
- Net reading: ephemeral tunnels are essentially never web-archived — expected absence, not evidence against the lane findings.

## Post-sweep open gaps (updated)

- devin-remote disappearance check — browser-capable delegation spec in `raw/github-harness-lhrlife.md`.
- `c7a1f824a6efc4.lhr.life` deployment watch (fresh Oct-2 tunnel, untagged).
- `domain:onlytron.com` pre-Sep-29 lookback (inside 30-day urlscan anonymous window).
- Corpus integration of 9 new candidates (AGEOUT1B + 4 uqtarget + 4 Jan-2026 tunnels; IDs in `raw/htmx-sublife.md`).
- Common Crawl 9×504 retry.
- `pandalegacy` htmx tokenizer blind spot — known, unfixable keylessly; corpus stays source of truth.
- Gated/browser-only items from the sweep stand: Naver, Megalodon free-word search, ZoomEye/Quake/ThreatBook, OpenTIP registration, abuse.ch Auth-Key, urlscan wildcard, Baidu session, ntfy.sh (VM blackhole), Radar detail UUID, tronzap payload bytes.

## Undocumented endpoints found
(2026-10-05 lanes — trick agents carried the XHR-hunting doctrine.)
- **stash.legible.sh**: NONE — audited against open-source `src/server.mjs`, surface matches docs exactly. `PUT`/`POST /{topic}/{filename}`, `GET /{topic}/{filename}?wait=60`, `HEAD /{topic}/{filename}`, `GET /{topic}` (JSON/SSE), `DELETE /{topic}/{filename}`, `/README.md`, `/llms.txt`.
- **Cloudflare Radar**: `GET /charts/<WidgetId>/fetch?<params>` (widget-data XHR; bot-walled to curl/text-fetch — browser session needed); `/scan/search?q=<q>&type=<url|domain|ip>`; `/scan/<uuid>/summary`; account-gated `.../accounts/{id}/urlscanner/v2/search`.
- **Kaspersky OpenTIP**: `https://opentip.kaspersky.com/api/v1` + `x-api-key`: `GET /search/{hash,ip,domain,url}?request=`, `POST /scan/file` (octet-stream + `?filename=`), `POST /getresult/file?request=<hash>`; UI XHR: `GET /ui/checksession`, `POST /ui/login`, app route `/token`.
- **CertSpotter** (keyless CT, healthy ~2 s/call): `GET /v1/issuances?domain=lhr.life&include_subdomains=true&expand=dns_names&expand=issuer`, dedupe by `tbs_sha256`; history starts 2026-05-31.
- **urlscan**: `q=task.tags:<hex>` is the verified self-tag syntax (bare hex matches nothing).
- **Sourcegraph SSE**: `sourcegraph.com/.api/search/stream?q=…&v=V3` requires `t=literal` — default type silently returns 0 even for control strings.
- **legible.sh** (audited vs `src/server.mjs` @ main): index at `https://legible.sh/llms.txt`; ports gate 4180, bigred 4181, trail 4182, slate 4183, relay 4184, mutex 4185, quorum 4186, meter 4187, tally 4189; quorum `GET /healthz → {ok:true}` in source only. Probe hygiene: reads materialize empty topic state (footprints).
- **Megalodon**: the `取得済みの魚拓` section heading renders even with zero captures — correct rule is heading present AND `見つかりませんでした` absent.
- **archive.today**: `/search/?q=<host>` answers bare HTTP 302 — follow with `-L` to `archive.ph/<host>`; positive rows read `3 Oct 2026 07:17 <title>`, negative reads "No results".
