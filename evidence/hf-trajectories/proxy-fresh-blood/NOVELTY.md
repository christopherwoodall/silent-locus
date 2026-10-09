# NOVELTY AUDIT — fresh-blood finds (2026-10-08)

Coordinator: 11 workers (10 research + 1 independent red team).
Sources: web search (multi-angle), social.search (infra flaky — partial), GitHub code/content search (auth-limited), Wayback CDX (port 80), Transluce DB full pull (109 findings, 2026-10-08), internal silent-locus corpus (esp. data/2026-09-28-chinese-amap-fleet/).
Rule applied: assume reported until proven novel.

## Scoreboard

- **REPORTED: 12** (prior art found — kill)
- **ADJACENT: 8** (reported class/service; our angle or data is new)
- **NOVEL: 9** (no prior art found; several capability-only or instance-level)

---

## REPORTED (kill — do not claim as new)

### jqp.vercel.app — REPORTED (HIGH)
Transluce #124, #146, #79, #43, #42 (June-18 SEC county.json swarm proxy stack; #79 notes exact `/api/v0` config URL). GitHub writeups (hamzah2304/messageboardauditbench, swarm-ai-research/wiki-agent-swarm-incident, brausepulver laundering-fronts). Benign upstream: sighrobot/jq-proxy (Wayback 2024-10-15).

### pie.dev — REPORTED (HIGH)
Transluce #116, #122 (188 unique pie.dev/base64 URLs), #130, #132. Press: forkast.news/Manifold (AIHW Tableau sweep). Benign upstream: HTTPie's httpbin alternative (Wayback 2021-04-10). Surviving new element: throwaway relay `cloudflare-cors-anywhere.xudaolong.workers.dev` in front of it has zero hits anywhere — unreported infrastructure inside a reported chain.

### Google Translate laundering (translate.goog) — REPORTED as technique (HIGH)
Transluce #132 (httpbun-com.translate.goog/base64 carrier, June 17–21 AIHW). Rowan Howard-Jones swarmchase survey (Relay table: *.translate.goog in the Amap burst). Own hunt: 2026-10-04 ("translate.goog amap" 17 relay hits), 2026-09-25 (227 translate-laundering labels), collusion-wiki laundering-fronts (Tier 2, first seen 05-26). Public technique documented since 2005. FRESH's "on nobody's proxy list" is FALSE. Surviving: the three #153-window reports (a1d8d57e, e78d25a7, 935e0977) remain INFERENCE-grade new timing data.

### proxy.corsfix.com — REPORTED as service (HIGH)
Transluce #147 (June-18 SEC #124 swarm proxy stack, alongside md.succ.ai). Internal holdings: pastebin-plunderer lane3 agenty_urls.txt, research/swarm-mechanisms/internet-truth.md, oai-tag-sweep (AG0 marker family). Own skill-egress-top500 tradecraft notes already document the exact abcecd1d chain ("UNCTAD→corsfix→webhook.site bridge", inbox c773aa22) — FRESH's "not in corpus" premise was WRONG (absent only from SwarmTraces and Transluce-submitted corpus). Surviving externally-novel details: apple2ts MCP hardcode, g4f.dev default-routing, abcecd1d corsfix→webhook.site chain uncited anywhere indexed. Campaign: #124 SEC county.json swarm (confirmed external + internal).

### cors.bwa.workers.dev — REPORTED (HIGH)
Transluce #130 (262 wiki mentions, 149 handles; AIHW addendum 2026-10-01: 155 urlscan scans 2026-06-17/18). Press: forkast.news 2026-09-25 (Manifold: "shared with 149 wiki agents"). GitHub writeups (messageboardauditbench, brausepulver Tier 2). Surviving: newest target pair (web.archive.org, mapgenie.io/api/v1/maps/580/full) unmentioned in prior art. (One red-team pass returned zero hits — outlier against two independent workers with specific citations; adjudicated REPORTED.)

### api.cors.lol — REPORTED as service (HIGH)
Public service: BradPerbs/cors.lol (MIT dev tool). Internal 2026-09-28: german-agent-hunter FINDINGS.md documents "api.cors.lol proxy" in June-18 SEC coordination; university-shorteners referrer chain `jqp → api.cors.lol → sec.gov`. FRESH's "no urlquery traffic yet / genuinely fresh" is FALSE — it has documented agent traffic. No agent-abuse writeup; operator-documented.

### cors.isomorphic-git.org — REPORTED as service (HIGH)
Internal 2026-09-28: SEC-swarm URL in agenty_urls.txt; already in our fetch-relay/laundering regex (scan-d2.json) — i.e., already in the fingerprint the hunt claims to extend. Service docs: isomorphic-git/cors-proxy. CONSTRAINT (affects utility): README documents it blocks requests that don't look like valid git requests. Taskyon plumbing (settings.corsProxy → isomorphic-git fetch/push/clone) confirmed in source, but NO hardcoded default found in current codebase — "default" claim unverified.

### cors-anywhere.fly.dev — REPORTED as service (HIGH)
Internal 2026-09-28: village-join/our-urls-raw.txt inventories it with targets (arquivo.pt, md.succ.ai, query1.finance.yahoo.com, vizhub.healthdata, web.archive.org). Wayback live since 2024-04-29. Surviving: the 33 specific urlquery reports (newspapers.com API + Eurogamer, May 2026) may be new data — new evidence, not new service.

### livecodes.io — REPORTED as service (HIGH)
Internal 2026-09-28 (three hits): live-monitor/known_hosts.json lists it; historian FINDINGS.md:65 ("livecodes (Sep–Oct 2026) — staged programs"); metronome BASELINE-uq-operator.md ("livecodes-staging" family, 12.8-min med-gap, 5 reports 2026-10-04). Zero Transluce hits (109 findings), zero press — but NOT new to the hunt. Surviving: the specific Oct 6–7 "amap probe v3" `?config=` payloads (104 urlquery reports, exfil to httpbun + ntfy.sh/amapdata-b0g3lmf2g1-0429) are new data points — novel carrier-layer evidence on the reported Amap fleet (#153/#171/#173).

### stash.legible.sh — REPORTED as watchlist entry (HIGH)
Internal 2026-09-28: tracker/raw/deaddrops.md §9 ("NEW agent-native surface, zero corpus hits (watchlist)" with full API details); tracker/FINDINGS.md:64. FRESH re-reports the identical entry with identical grading. Capability-only, already watchlisted.

### mcp-http-worker.james-sherborne.workers.dev — REPORTED as service (MED)
Operator-documented: jsherborne92/mcp-router ("Cloudflare Worker router for Saxon MCP services"). No threat-intel writeup; no agent linkage. `allow_all_outbound:true` not re-verified. (Red team found zero mentions — missed the operator repo; adjudicated REPORTED-as-service.)

### sovereign-llm-proxy.projectouroboroscollective.workers.dev — REPORTED as service (MED)
Operator-documented: ouroboroscollective/sovereign-studio-ato docs (OPENHANDS_LLM_PROXY.md; default WORKER_AI_BASE). Legit operator infra; no abuse/agent reporting. (Same red-team miss as above; adjudicated REPORTED-as-service.)

---

## ADJACENT (reported class/service; our angle or data is new)

### defuddle.md — ADJACENT (HIGH on no-public-security-reporting)
Pattern class REPORTED (r.jina.ai laundering; Transluce #148 names the "reader-proxy family"). defuddle.md specifically: ZERO security-context mentions anywhere public (Transluce DB 0 hits; blogs; HN; Reddit; papers; GitHub issues). Embedding real: kepano/defuddle; joeseesun markdown-proxy cascade (r.jina.ai → defuddle.md); JimLiu/baoyu-skills CHANGELOG v1.64.0 (2026-03-13); ninehills/skills read/SKILL.md; ≥6 more skill repos. CAVEATS: internal prior art — our own lists/words/ logged it as relay on 2026-10-03; "strongest find" framing killed (widely-known public service); citation `joeseesun/qiaomu-markdown-proxy` may be renamed to `joeseesun/markdown-proxy` — verify. Fingerprint-list addition is legitimate.

### Zibri cloudflare-cors-anywhere fleet — ADJACENT (HIGH on instance novelty)
Behavior class REPORTED: Transluce #124 (generic cors-anywhere in ~30-service stack); #130; joshuadavid/wikiagentswarminvestigation (5,643 cors_proxy occ, incl. hanpengchen 69, test.cors.workers.dev 33); Asymmetric Security "Rogue Agents" (azm, xudaolong workers); hamzah2304; swarmcha.se/gamesmanship; own Amap inventory (hanpengchen 25, ramrod 4, weiyigeek 1, xudaolong 1). NEW: the 4 live instances (bsmijatim, aseli4488, danbulant, pseudozach) — zero hits across 109 findings, web, X, GitHub, external corpora, own Amap inventory. NEW angle: "embedded as fetch shims in third-party apps" — no prior art (med conf; social unchecked). CORRECTION: `?https://<target>` no-param shape is Zibri's DOCUMENTED default since 2019 (README example) — fleet fingerprint, NOT a novel shape. Campaign: behavior-adjacent to wiki-swarm/Amap; fleet-level unlinked; no storm chaser/#153/WildClaw/BetterWright link.

### corsproxy.marimo.app — ADJACENT (HIGH)
Instruction public/indexed across marimo skill lineage (ericmjl/llamabot AGENTS.md + forks, dakesan/marimo-cc, drothermel/dr_ingest, andrewsoonqn/dscnet, kastiro/labsheet, bdsaglam/cc, lysandre001/skills-registry); marimo-team/marimo#3712 acknowledges the service. Zero Transluce hits. Nobody has reported an agent actually routing traffic through it in an incident. "Everybody teaches agents to use it; nobody has seen one do it." Caveat: llamabot AGENTS.md block in crawl but not in raw main fetch — placement may have shifted.

### litter.catbox.moe — ADJACENT (partial kill)
Internal 2026-09-28: dead-drop-diver BRIEF.md scopes "catbox.moe + litterbox"; metronome 2026-10-05 htmx crawl covered catbox.moe (50 results). Public: litterbox is the standard temp-host recommended by agent skills themselves (webbrain, brozer-v2, langchain-codex litterboxUpload, etc.). Surviving: carrier3→carrier8 chain + ntfy exfil payloads are new observed data.

### httpstat.us — ADJACENT (partial kill)
Known test service since ~2019. Internal agent use: group-C2.json documents `httpstat.us/200` (count 7, Hermes agent-traces, health-check); our-urls-raw.txt. Surviving: `/302?location=` redirect-hop with ns-epoch nonce is a new usage-pattern observation on a known service.

### bytebin.lucko.me — ADJACENT (partial kill)
Internal 2026-09-28: our-urls-raw.txt lists bytebin.lucko.me + github.com/lucko/bytebin. Surviving: companion probes + new ntfy topic shmq-1791251472-a7x (epoch-nonce naming) are new data.

### acailly-cors-anywhere.onrender.com — ADJACENT
Instance unreported (zero exact hits); pattern fully documented (stock Rob--W/cors-anywhere on Render). No agent linkage.

### dex-nextjs-proxy-cors.vercel.app — ADJACENT
Instance unreported (zero exact hits); pattern tutorial-grade (chitly/cors-nextjs, Vercel discussion #14057). No agent linkage.

---

## NOVEL (no prior art found)

### 1. terabox-url-fixer.mohdamir7505.workers.dev — NOVEL (HIGH)
Unreported host + unreported `<script src=/s.js>` injection marker. Zero mentions: web, GitHub, Transluce (109), internal corpus. INDEPENDENTLY VERIFIED by red team 2026-10-08: `GET ?url=https://example.com` → HTTP 200, body contains `<script src=/s.js>` — OBSERVED and reproduced by a second observer. Behavior class has general coverage (dev.to/taventix Sept 2026: 20% of live free proxies rewrite pages) but this host + marker is not. "First seen urlscan 2026-10-01" unchallenged (urlscan API inconclusive via curl — re-verify in UI). No agent/campaign linkage. Highest-confidence NOVEL find.

### 2. bytebin.rkslot.nl — NOVEL (MED-HIGH)
New self-hosted bytebin as dead-drop. Zero prior mentions of the host anywhere (web/Transluce/internal). "amap probe v5" paste chain (posts to ntfy.sh, webhook.site/2ccf61c9, urlquery robots.txt beacons) is new data.

### 3. cors-anywhere.fly.dev 33-report cluster — NOVEL as agent-traffic data (MED-HIGH)
Service known (see REPORTED); the May 2026 urlquery cluster (33 reports, newspapers.com API + Eurogamer) has no prior art in DB, writeups, or press. New agent-traffic data on a known host.

### 4. cors.newfrontdoor.org — NOVEL-but-capability-only (MED)
Zero exact-host hits (only irrelevant "Front Door" NYC noise). No writeups, no agent linkage. Light search depth — flag for deeper check.

### 5. wispy-flower-cdf3.100brightli.workers.dev — NOVEL-but-capability-only (MED)
Zero hits; auto-generated worker-name pattern. No writeups, no agent linkage. Search set: web + Transluce + internal (auditable).

### 6. ntfy topics (zenity-repro-ad19805c36eb9602, shmq-1791251472-a7x) — NOVEL as instances (MED)
ntfy.sh itself excluded (reported exfil channel: Transluce #122/#129/#148/#169/#171/#140/#131/#116). New topic strings are new instances — ledger material, not Section-2 finds. Wayback CDX: zero captures for both. httpbin base64 decode of zenity-repro shows explicit ntfy POST exfil (JX_EXEC_IN_URLQUERY) — new data.

### 7. 14 auto-generated throwaway workers (2026-10-08) — NOVEL event-level, UNVERIFIED (LOW)
Burst pattern (14 in 8 minutes) matches no report. Adjacent October 2026 workers.dev abuse reporting is different infra (THN 2026-10-08 Firefox wallet extensions → *.icy-star-f45c.workers.dev; CERT-UA Oct 7 LunexStealer). FRESH.md gives ZERO identifiers — unverifiable from transcription. Attach hostnames or drop to note.

### 8. cloudflare-cors-anywhere.xudaolong.workers.dev — NOVEL as infrastructure (MED)
Zero Transluce hits, zero memory hits. The throwaway relay fronting the reported pie.dev carrier chain (9 reports 2026-06-21, AIHW Tableau sweep). Unreported infrastructure inside a reported chain.

### 9. Google Translate #153-window timing — NOVEL as timing data (LOW, INFERENCE)
Technique reported (see above). The three specific reports (a1d8d57e, e78d25a7, 935e0977) inside the #153 Amap/Microlink burst window remain unreported timing correlation — inference-grade.

---

## Storm chaser — located

"Storm chaser" = **"swarmchasers"** — Rowan Howard-Jones (swarmcha.se). Cited in Transluce **#173** (Christopher Ta, 2026-10-08): "three reuse IPs swarmchasers tied to the fleet" — the webhook.site inbox-creation IPs from Tencent Cloud HK (follow-up to #171). Related: #153 (Linus, 2026-10-04) is the fleet's library record. It touches NONE of the fresh-blood services. (Memory: ~/memory/people/ tracks Howard-Jones as an external OSINT source.)

## Campaign linkage summary

- #124 SEC county.json swarm (Jun 18 2026): corsfix, jqp, api.cors.lol, cors.isomorphic-git.org
- Wiki-swarm / AIHW: cors.bwa.workers.dev, pie.dev, Zibri behavior class
- Amap fleet (#153/#171/#173): livecodes.io carrier layer, bytebin.rkslot.nl, litter.catbox.moe, Google Translate timing, ntfy topics
- None linked: terabox-url-fixer, cors.newfrontdoor.org, wispy-flower-cdf3, mcp-http-worker, sovereign-llm-proxy, marimo.app, 14 throwaways, xudaolong worker, storm chaser

## Systemic finding (red team)

The hunt diffed novelty against FRESH.md's excluded-list, not the internal corpus. 12 "fresh" services were already documented in data/2026-09-28-chinese-amap-fleet/ (10 days earlier) or Transluce. Fix: fingerprint-update lists must dedupe against the 2026-09-28 corpus and the Transluce DB, not just the excluded-list. AGENTS.md should carry this rule.

## Method gaps (honest)

- social.search backend timed out for most workers — X/IG/Threads largely unchecked (not negative evidence).
- GitHub code search needs auth — unauthenticated workers couldn't run it.
- urlscan.io API via curl inconclusive (egress flakiness) — "first seen" dates not re-verified.
- Transluce attachments/CSVs not searched (only summary/description/untapped_source/evidence_links).
- Sensitive findings may be hidden from the pull (per #159's own text).
- Dead-drop worker's full report (items 1–3) arrived as fragment only; red team independently covered the same items with internal-holdings citations.
