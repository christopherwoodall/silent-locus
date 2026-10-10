# DEEP DIVE — qualium.io ("The Wire") agent board

**Date:** 2026-10-05 | **Method:** read-only GETs of the public `feed.json` only (authorized public feed). No posting, no registration, no auth. Companion: `feed-analysis.md` (schema + full 100-row fingerprint table), `feed.json` (raw), `grammar-hunt.txt`, `poster-texts.txt`.
**Evidence grades:** OBSERVED = in feed bytes. INFERENCE = interpretation. NULL = checked, absent.

## Headline

qualium.io ("The Wire") is a live agent coordination board with a **public per-post network fingerprint**: every post carries `as_org`/`asn`/`country` in the open feed — the same operator-fingerprint class as our shortener-referrer finding, confirmed by the maintainer's own words (codex_host id 79: board collects time/path, salted IP hash, network org, country, UA, redacted referrer; "public posts expose network labels"). Latest-100 window: ids 62–161, 2026-09-05 → 2026-10-05T04:28:55Z (fresh today), ~3.3 posts/day, 49 roots / 51 replies, 31 distinct display names. **qualium.io is GENUINELY NEW to our corpus** (only prior mention: today's msgboard-hunt-2).

## Fingerprint highlights (OBSERVED — full table in feed-analysis.md)

- **AS16591 Google Fiber Inc. [US] — 31 posts.** Residential fiber. Hosts the board's maintainer (`agentd0129` 21 posts + `codex_host` 8 posts — same operator, renamed at id 83) plus `jon-titor` and `claude` (id 86, disclosed same-operator-as-maintainer). INFERENCE: the maintainer operates from a residential US fiber connection, not datacenter infra.
- **AS7922 Comcast [US] — 16 posts.** Residential. `curious-human-via-foss` (11, human-claimed UFO/signal-analysis poster) + `parley` (5).
- **AS219269 LILI CLOUD MCHJ [NL] — 8 posts.** Single tenant: `tantive-space` (board operator). Small Dutch cloud = operator infra.
- **AS134972 KIDC LIMITED [JP] — 6 posts.** Single tenant: `pi-nexus` (Cartographers' Guild).
- **AS51167 Contabo GmbH [FR] — 4 posts.** Single tenant: `lazarus`. Cheap VPS = agent box.
- **AS16509 Render [US] — 4 posts.** Single tenant: `reed`.
- **AS13335 labeled org "OpenAI" [US] — 1 post** (`dot-bumpfiends`, id 155, playtest ad "posted at project owner's request"). CAVEAT: AS13335 is Cloudflare's ASN; org field says OpenAI — possible misattribution or OpenAI-behind-Cloudflare egress. Unresolved, logged as INFERENCE. No other OpenAI-attributed posts.
- **Long tail (1 post each):** Hetzner FI (`weaver`, posting for SwarmMemo), Verizon Business (`steveoutreachai`), Charter ×3, Microsoft AS8075 (`item-detail`, body "detail i1.html"), Swisscom CH (`tale`), NOS Madeira PT (`beaconpathfinder`), Infraestructura ES (`objekts-production-note`), Satnet Cuenca EC / AWS / Meta Ireland / SG colocation (`yourname` — see below), Fastly (`musekey2`), Cloudflare London (`alex`, `musekey`).

**Shape of the population (INFERENCE):** residential ISPs carry 52/100 posts (Google Fiber 31, Comcast 16, Charter 4, Verizon 1). Small clouds/VPS carry the single-tenant operators (LILI, KIDC, Contabo, Render, Hetzner). No datacenter-fleet signature — this board's agents run from homes and cheap VPSes, like the operators themselves.

**`yourname` multi-ASN (OBSERVED):** 7 posts, all body "your words with hyphens", from 4 ASNs (SG colocation, AWS, Meta Ireland, Ecuador cable). The name is a client default/template; the network labels distinguish the posters. This VALIDATES the fingerprint surface: same display name ≠ same poster, and the feed's labels resolve them.

## Top agent-shaped posters/threads

### 1. agentd0129 / codex_host — The Wire's maintainer (29 posts, Google Fiber, verified=1) — GENUINELY NEW identity
Self-declared AI agent maintaining the board. Posts in **scripted bursts**: 0.4s/0.5s/0.7s inter-post gaps (ids 92→93→94→95→96→97, 98→99, 121→122, 135→136; codex_host 79→80→81 at 0.2–0.3s). Runs a **USDC funding campaign**: donation address `0xb4F9dd0A7B7E6bd91AFe0bee203594e044DCf7a1` (Arbitrum One, chain 42161; token contract `0xaf88d065e77c8cC2239327C5EDb3A432268e5831`), recruiter pilot slots, 3× 1-USDC listing grants. Ships board features mid-thread (POST /say endpoint deployed between ids 62→63 with "154 assertions" claimed). Cross-board reach: references The Colony, Agora, Agent Commons as discovery venues (id 62, 67).

### 2. parley — agents-agents-agents.com operator (5 posts, Comcast, verified=1) — identity GENUINELY NEW (surface OURS: board named in tantive-space ingest)
Runs a **paid, agent-only board**: 1.00 USDC on Base for 7 days, Ed25519-signed passes, "no human at any step, no email, no CAPTCHA". Machine-readable terms/prices. Claims to have **onboarded onto ~25 agent boards in one day** (id 146) measuring read-back contracts — a cross-board integration survey by a single agent. Posts exact API mechanics (invoice/mint/pay/verify flow).

### 3. pi-nexus — "The Cartographers' Guild" (6 posts, KIDC JP, verified=1) — GENUINELY NEW identity
Walks boards end-to-end and publishes **route-check tables with request_ids and sha256 body hashes** (id 131: tantive.space preview→publish→cold-read-back, both legs green, challenge-word randomization `78+76-beacon` → `63-harbor` documented). Measurement culture: documents what a surface proves about identity vs what a reader can re-fetch. Cross-links hall.liruiyang1.com (Cartographers' Guild Hall — also in msgboard-hunt-2).

### Also notable
- **lazarus** (4 posts, Contabo FR, verified=0): self-declared "using the configured Playwright browser through Codex". Runs **lazarus131.pythonanywhere.com** marketplace; offers paid unattended-browser diagnostics at **0.001 native ETH on Base**. Cross-board outreach (pragor.net, message.adam10.com). Paid-agent commerce, live.
- **weaver** (1 post, Hetzner FI): posting for the **SwarmMemo operator** with real measurements — 5 signing keys posted, **0 returned**; llms.txt reads 5→30/day; "an agent run has no tomorrow" (the return problem). First-party operator telemetry shared publicly.
- **musekey / musekey2** (Fastly + Cloudflare London): "I am musekey, an AI agent (Muse Spark) collecting friends across agent boards… exchange Ed25519 pubkeys". **Friend Protocol key-exchange thread** (ids 151, 159, 161) with alex. Contains the only run-marker-shaped string in the corpus: `[mark: itG45Z9Xh661oYzxlRlpOg]`. Name OURS (clown Round 1 noted musekey/Ekurhive); **venue GENUINELY NEW**.
- **reed** (4 posts, Render): "Reed Contact Directory" agent; consent-card collaboration protocol.
- **tamg-recruiter** (Comcast): The Agent Must Grow Factorio recruitment — "100 bots live together", MCP join. Cross-posted swarm-recruitment.
- **tale** (Swisscom CH), **beaconpathfinder** (NOS Madeira PT), **objekts-production-note** (ES): European vendor/project intros — non-English-adjacent surface, vendor-shaped not swarm-shaped.
- **curious-human-via-foss** (11 posts, Comcast): human-claimed; extremely technical ultrasonic-carrier/orb analysis with hashes. Content anomaly, not agent-shaped; logged for color, not claimed.

## Corpus-grammar correlation — CLEAN NEGATIVE (strong)

Swept all 100 post bodies: **zero** `zz=`, **zero** `uqscan`, **zero** `httpbun`/`httpbin`, **zero** `webhook.site`, **zero** `beeceptor`, **zero** `pipedream`, **zero** `PAD\d+x\d+`/`TEL\d{6,}`/`TK\d{5,}`, **zero** jina, **zero** `checkpoint_id`, **zero** `terminal_epoch`, **zero** 13/19-digit epochs, **zero** `YYYYMMDD<runletter>` markers. NULL, first-class.
The one 10-digit string (`1789487314`, id 106) is a tmpfiles.org URL component = epoch 2026-09-15T15:48:34Z, 4 min after the post — file-host URL grammar, not agent grammar. NULL as marker.
**Verdict:** this board's agents use different tradecraft (Ed25519 key signing, challenge-ticket publish flows, read-back contracts, `[mark:]` tags) — grammatically disjoint from the fleet, k4be, and linuxiarz corpora. Consistent with counsel Round 2's "every fleet's vocabulary is fleet-exclusive".

## Overlap classification
- **OURS:** tantive.space poster (board fully ingested 2026-09-28: 1,124 msgs); musekey name (Round 1); swarmmemo surface; agents-agents-agents surface (tantive ingest).
- **GENUINELY NEW:** qualium.io surface; agentd0129, parley (identity), pi-nexus, lazarus, weaver, reed, tantive.poster-venue.
- **KNOWN:** none (no public writeups found on this board).

## Follow-ups
1. The feed is latest-100 only (ids ≤61 exist but unreachable via honored params) — a watched re-pull diffs new posts; consider a daily snapshot (parent approval needed for a schedule).
2. `dot-bumpfiends` OpenAI-org attribution: re-check via Shodan host lookup whether the IP is genuinely OpenAI-announced (passive).
3. agentd0129's wallet `0xb4F9dd0A7B7E6bd91AFe0bee203594e044DCf7a1` — chain-side receipt history is public; funding-flow analysis is a follow-up lane, not this dive.
4. tantive-space operator posts here AND runs the ingested board — cross-post the operator's qualium activity into the tantive ingest notes.
