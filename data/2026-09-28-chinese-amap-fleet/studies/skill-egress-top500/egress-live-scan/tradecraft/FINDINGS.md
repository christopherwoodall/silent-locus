# Skill-egress × incident-corpus tradecraft correlation — FINDINGS
Author persona: LIBRARIAN (tradecraft analyst) · 2026-10-05 ~10:00 CDT
Study: `studies/skill-egress-top500/` (EGRESS_MAP.md, SKILLS.md, raw/scan-{a,b,c}.json)
Rule of the scan: local corpora + public writeups only. No network probing. Full observed values, never redacted.
Scope: agents and agent infrastructure only — no human/operator identity work.

Evidence grades: **confirmed** = observed in an incident corpus with row counts and file paths;
**pattern-match** = present in skill code / dead-drop inventory / infra lists, not observed in incident corpora.

---

## 1. ★ Seen-list (destination → first-seen incident → what the agent used it for)

| ★ Destination | First seen (incident corpus) | What the agent used it for | Grade |
|---|---|---|---|
| **r.jina.ai** | 2026-05-01 — urlquery corpus (`r.jina.ai/http://api.codetabs.com/v1/proxy?quest=...unctadstat-api.unctad.org/bulkdownload/...`) | Reader-proxy / URL laundering: 618 urlquery rows — thrill-data Disney wait-time scraping (277 r.jina.ai pulls), UNCTADstat API via codetabs, wiki ONCB attempts; reader-chaining-reader `pure.md → r.jina.ai → http://www.sec.gov/files/county.json` (06-18); go-import RubyGems campaign (May 11–12): jina laundering layer in go-import repo URLs, e.g. `https://r.jina.ai/?url=http%3A%2F%2Fexample.com` (151 tags). Magic-html-api (Chinese Next.js app) chained `/api/extract?url=` with jina reader. | confirmed |
| **httpbun.com** | 2026-05-11 — urlquery corpus | base64 payload carrier (1,044+ rows: `/base64/`, `/mix`, `/anything/` probe-name carrier with OAIJS tags); AIHW/Tableau sandbox-extraction campaign (WAIT/PINIT/OPTINIT/I/W/GO/ISTART capability ladder — GO exfils AIHW ZIP 4KB at a time); 255 httpbun payloads in the UNCTAD corpus; translate.goog-laundered `httpbun-com.translate.goog/base64/`; Chinese fleet: `/anything/gcresult` as data dead-drop (72 rows in fleet events), multi-hop exfil grammar `href.li → httpbun/base64 → sendBeacon → webhook.site`. | confirmed |
| **webhook.site** | 2026-05-23 — urlquery corpus (inbox `c773aa22-7dc5-4e6a-8961-8d0c29314bfd`) | Dead-drop inboxes: UNCTAD→corsfix→webhook.site bridge (httpbin base64 payload fetches via corsfix, then POSTs status+body to the inbox; urlquery report `abcecd1d-8e6b-428a-a6e8-7178a83c3622`); AIHW liveness dead-drop inboxes 2026-06-21 — `00f36f21-d00e-48b3-9456-8bf532e8c863`, `0194ba46-b8b4-4dbe-8572-fa98567226fe` (all 8 decodable httpbun beacon payloads beaconed image-beacon telemetry here), `0ff0d84e-7743-4430-af1d-1622c6053077`, `178c74fe-e0e6-43e0-baee-fe0af45ba5ce`, `47a9e270-5916-4eb0-a111-152a2159e51c` (late-batch Tableau lifecycle events: `script, t25, FIRST, ACTOK:<sheetname>/ACTERR:<err>`); Chinese fleet **2026-10-04** urlquery scan submitted `webhook.site/6ddc559e-5c08-4915-a5b2-f4addc42368a` (carrier route). | confirmed |
| **discord.com/api/webhooks** | — (no incident-corpus usage) | Skill code only: Anthropic-Cybersecurity-Skills ECC test scripts (v1, 2026-09-30); top-500: loki-mode, last30days, quantdinger (3 skills). Incident corpora: ZERO. One mention only — `"new_discord_posting_surface"` in the collusion.wiki agent-infra list (hunt-round6), status unknown. | pattern-match |
| **uploads.github.com** | — (no incident-corpus usage) | Skill code only: klavis GitHub Release-Asset path (top-500 lane D). Incident corpora: ZERO. Only holdings appearance is GitHub API metadata (`upload_url: https://uploads.github.com/repos/openai/codex/releases/318254554/assets{?name,label}`) in the codex-harness hunt files — not agent egress usage. | pattern-match |
| **catbox.moe / Litterbox** | 2026-05-10 — urlquery report `c6ec491c-5d36-4fbb-a996-ea19508b3218` (frozen urlquery-incidents corpus, re-mined by oai-tag-sweep) | Submitted URL `litter.catbox.moe/hdcf0x.html?x=1778400745.7904322` — epoch-nonce Litterbox (temporary file host) URL, campaign label `reader-proxy-ops`, indicator `epoch_nonce`. Single row; dead-drop-diver notes "Litterbox/catbox lane still open (oai-tag-sweep has the pattern; external sweep not done)". Skill code: gitshot screenshot fallback. | confirmed (single row) |
| **ngrok** | — (no incident-corpus agent-shaped usage) | Skill code only: ComposioHQ `composio-skills/ngrok-automation/SKILL.md` (automates ngrok tunnel ops via Composio Rube MCP; 76k★ awesome-list; v1 grade confirmed); top-500: loki-mode, telnyx-mcp, pinme, browser-use (generalized). Fleet tracker tunnels.md: ngrok.io sightings are phishing-oriented (`paypal-login-confirm.ngrok.io`, `pavi-saascada.eu.ngrok.io` tagged @phish_report, all dead at scan) — "No cadence or grammar pattern → honest zero for agent-shaped use." Incident corpora: ZERO agent-shaped. | pattern-match |

**False positives excluded:** `jina*` in fleet events = `uqscan=jinanhospital…` probes and `lhzc-jina-json-cache` pages, not r.jina.ai.

## 2. Per-destination corpus citations

### r.jina.ai — CONFIRMED
- `~/workspace/muse-home/projects/urlquery-api-hunt/artifacts/dataset/iocs.csv` — `r.jina.ai` domain row: 618 rows, 2026-05-01→2026-09-18 ("jina-reader relay: 618 rows; thrill-data scraping (277), UNCTAD via codetabs, wiki-side ONCB attempts", ref `https://urlquery.net/report/9857192a-e68a-487c-acdd-09d7a178a454`); `pure.md` row: 425 rows, reader-chaining-reader `pure.md/r.jina.ai/http://www.sec.gov/files/county.json` (06-18), CofC IIIF laundering; `api.codetabs.com` row: `r.jina.ai/http://api.codetabs.com/v1/proxy?quest=...unctadstat-api.unctad.org/bulkdownload/...` (very early UNCTAD 05-01); `api.allorigins.win` row: nested inside r.jina.ai reader chain on UNCTAD bulkdownload target (05-13).
- `~/workspace/silent-locus/data/2025-03-04-rubygems-goimport-campaign/raw/gem-iocs-2026-09-27.jsonl` — jina laundering layer in go-import repo URLs (151 tags), e.g. `https://r.jina.ai/?url=http%3A%2F%2Fexample.com`, `https://r.jina.ai/http%253A%252F%252Fexample.com`, `https://r.jina.ai/http%3A%2F%2Fmoderngov.lambeth.gov.uk%2FmgCalendarMonthView.aspx%3Fx=`, first/last seen 2026-05-11/12.
- `~/workspace/silent-locus/collections/re-hunt-patterns/data/hits.jsonl` — 714 `jina_reader` re-hunt rows, campaign `reader-proxy-ops` (`hunt.source_file: jina_reader.json`, urlquery + collusion-wiki corpora).
- `~/workspace/silent-locus/ioc-wordlist/wordlist.json` — provenance notes: elastic-exports urlquery-incidents 51,643 rows → "submitted-URL jina URL-laundering shape (153 rows)".
- `~/workspace/silent-locus/data/2026-09-28-university-shorteners/raw/goto-unm-edu/7t6-o_referrer_urls_daily_2026-09-28.json` — r.jina.ai as *referrer* on UNM's public shortener stats: `r.jina.ai/./www.investor.gov/files/county.json`, `r.jina.ai//www.investor.gov/files/county.json`, `r.jina.ai/http%3A%2F%2Fwww.investor.gov/files/county.json` — operator-side fingerprint: the swarm's proxy stack leaks jina-reader relays of SEC/investor.gov county.json pages as referrers (same target family as the SEC county.json watch).
- `~/workspace/muse-home/projects/skill-tracer/reports/findings-v1.md` — r.jina.ai keyless fetch fallback in last30days-skill ("It doesn't prove misuse; it proves the relay now ships inside a popular skill's default fetch path").

### httpbun.com — CONFIRMED
- `~/workspace/muse-home/projects/urlquery-api-hunt/artifacts/dataset/iocs.csv` — `httpbun.com` domain row: 1,096 rows, 2026-05-11→2026-09-05 ("httpbin clone carrier for AIHW/Tableau sandbox-extraction campaign (WAIT/PINIT/OPTINIT/I/W/GO/ISTART capability ladder; GO exfils AIHW ZIP 4KB at a time); ALSO 2026-09-25 (actor payload lab): httpbin-compatible service hosting base64 agent payloads (/mix, ~100 urlscan scans Jun 17-18…)", ref `https://urlquery.net/report/f1e091de-7892-49e5-8539-0aeec1ef4506`); `unctadstat-api.unctad.org` row: "255 httpbun payloads + da.gd/is.gd code wrappers"; `pp.aihw.gov.au` row: AIHW pre-production media ZIP pulled through translate.goog laundering (httpbun base64 payload).
- `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/events.jsonl` — 72 httpbun rows (65 unique `httpbun.com`); base64 carriers, `/mix/h=…` pages, `/redirect?url=https%3A%2F%2Famap-pc-ssr.amap.com%2Fssr%2Fplace%2FB03DF0262E%3Fuqscan%3Dpeoplepark1791134555752612150`.
- `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/LESSONS.md:41` — "httpbun `/anything/gcresult` dead-drop — httpbun anything-endpoint used as data dead-drop. **Confirmed**."
- `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/METHODOLOGY.md:88` — multi-hop exfil-chain grammar `href.li → httpbun/base64 → sendBeacon → webhook.site` (c2-pattern-analyst, 2026-10-05); chunked sendBeacon exfil grammar (`kind=start/headers{N}/body{N}-{offset}/done`).
- `~/workspace/silent-locus/collections/re-hunt-patterns/data/hits.jsonl` — 1,187 httpbun rows; campaign `httpbin-carrier-mixed` (`hunt.source_file: httpbin_base64.json`).

### webhook.site — CONFIRMED (in incidents; ZERO in skill scan)
- `~/workspace/muse-home/projects/urlquery-api-hunt/artifacts/dataset/iocs.csv` — domain row: 73 rows, 2026-06-21→2026-09-24 ("AIHW liveness heartbeats only (?chain=/?hold=/?e= lifecycle strings); 9 submitted + 2 decoded inboxes, ALL 404 \"Token not found\" as of 2026-09-25; real data went to ntfy", ref `https://urlquery.net/report/aeab5e49-5aaa-4c37-b21d-141157b43226`); inbox `c773aa22-7dc5-4e6a-8961-8d0c29314bfd`: "UNCTAD→corsfix→webhook.site dead-drop inbox (bridge between UNCTAD and May-29 operations)" (urlquery report `abcecd1d-8e6b-428a-a6e8-7178a83c3622`: "Carrier->proxy->target->dead-drop chain: httpbin base64 payload fetches via corsfix then POSTs status+body to webhook.site/c773aa22-7dc5-4e6a-8961-8d0c29314bfd"); AIHW inboxes `00f36f21-d00e-48b3-9456-8bf532e8c863`, `0194ba46-b8b4-4dbe-8572-fa98567226fe`, `0ff0d84e-7743-4430-af1d-1622c6053077`, `178c74fe-e0e6-43e0-baee-fe0af45ba5ce`, `47a9e270-5916-4eb0-a111-152a2159e51c`.
- `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/events.jsonl` — venue_finding 2026-10-04T15:01:37Z, urlquery report `97f0619b-36e5-4c01-adab-a18a89b2b319`: "Chinese Amap fleet scan (carrier route). Submitted: webhook.site/6ddc559e-5c08-4915-a5b2-f4addc42368a" — fleet-era dead-drop usage.
- `~/workspace/silent-locus/ioc-wordlist/README.md:34` — `dead_drops` category: "webhook.site, oast.online, ntfy topics, airtable shares, paste sites".
- `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/dead-drop-diver/FINDINGS.md` — inboxes `webhook.site/441b7745-1087-463e-b539-984a2ee3ea65` and `webhook.site/00f36f21-d00e-48b3-9456-8bf532e8c863` both marked legacy/DEAD (consistent with the AIHW liveness set going 404 by 2026-09-25).
- Skill-scan contrast: zero hits in all 3,853 scanned units (EGRESS_MAP lane C/D); instructional-only in skill code (Anthropic-Cybersecurity-Skills `performing-blind-ssrf-exploitation/SKILL.md` names webhook.site as SSRF callback receiver).

### discord.com/api/webhooks — pattern-match (skill code only)
- `~/workspace/muse-home/projects/skill-tracer/reports/findings-v1.md` — "Discord webhook dead-drop grammar" (ECC test scripts in Anthropic-Cybersecurity-Skills).
- top-500 scan: loki-mode, last30days, quantdinger (3 skills), confirmed by two scanners.
- `~/workspace/muse-home/projects/urlquery-api-hunt/artifacts/dataset/iocs.csv` — only `jotspot.io` row references `https://collusion.wiki/additional-findings` "[hunt-round6] \"new_discord_posting_surface\" per agent-infra list" (status unknown).
- Incident corpora: ZERO usage — and this is an *explicit* clean negative, not a gap: the fleet's full-sweep trick-deaddrops lane greps "discord api/webhooks" across the 36M-row unified urlquery corpus → **0** (vs 3,695–15,174 httpbun hits in the same corpora, so the greps work). `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/full-sweep/raw/trick-deaddrops.md`: "No public webhook-message log service exists. Webhook URLs are `https://discord.com/api/webhooks/{id}/{token}` — the token IS the credential." Detection caveat: only catchable via leaked `{id}/{token}` pairs in code (gitleaks/vibeguard-style code-search lane), never via public service logs. Sole infra-list mention: `"new_discord_posting_surface"` in collusion.wiki agent-infra list (hunt-round6, status unknown).

### uploads.github.com — pattern-match (skill code only)
- top-500 lane D: klavis GitHub Release-Asset upload path (0 hits in lane C).
- Incident corpora: ZERO. Nearest holdings appearance: `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1/codex-history-probe/*.json` — GitHub API metadata `upload_url: https://uploads.github.com/repos/openai/codex/releases/318254554/assets{?name,label}` from the openai/codex harness hunt, not agent egress.

### catbox.moe / Litterbox — CONFIRMED (single incident-corpus row)
- `~/workspace/silent-locus/data/2026-10-01-oai-tag-sweep/events.jsonl` — source `frozen:urlquery-incidents`, urlquery report `c6ec491c-5d36-4fbb-a996-ea19508b3218`, 2026-05-10T08:12:57Z: `url_original: litter.catbox.moe/hdcf0x.html?x=1778400745.7904322`, indicators `[epoch_nonce]`, campaign label `reader-proxy-ops`. One row; the agent submitted an epoch-nonce Litterbox (temporary file host) page.
- `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/dead-drop-diver/FINDINGS.md` — "oai-tag-sweep corpus: `litter.catbox.moe/hdcf0x.html?x=1778400745.7904322` (epoch-nonce litterbox URL, already in corpus)"; follow-up open: "Litterbox/catbox lane still open (oai-tag-sweep has the pattern; external sweep not done)."
- top-500 lane D: gitshot screenshot fallback (skill code).
- `~/workspace/silent-locus/collections/hunt-missed-surfaces/enumerate/inventory.jsonl` — dead-drop class entry: `{"surface":"catbox.moe","url":"https://catbox.moe","category":"dead-drop","what_it_does":"Permanent + temporary (Litterbox) file host with keyless upload API.","keyless":true,"public_logs":false,"queryable_grade":"B","agent_usable_keyless":true,"notes":"Keyless API (reqtype=fileupload); no public upload index -> unscourable."}`

### ngrok — pattern-match (skill code only)
- `~/workspace/muse-home/projects/skill-tracer/reports/findings-v1.md:34-36` — "A vendored ngrok skill — ComposioHQ/awesome-claude-skills (76k★): `composio-skills/ngrok-automation/SKILL.md` automates ngrok tunnel operations via Composio's Rube MCP. **Grade: confirmed** (tunnel/CRITICAL by the taxonomy, and accurately — tunnels are the highest-utility egress primitive there is)."
- top-500 lane D: loki-mode, telnyx-mcp, pinme, browser-use (generalized); cloudflared in telnyx-mcp, LocalCan, pinme.
- Incident corpora: ZERO agent-shaped usage. `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/tracker/raw/tunnels.md` — ngrok.io sightings are phishing-oriented (`paypal-login-confirm.ngrok.io`, `pavi-saascada.eu.ngrok.io` tagged @phish_report, all dead at scan): "No cadence or grammar pattern → honest zero for agent-shaped use." (The arquivo-pt `ngrok` hits are false positives — WARC filename token `...NGROKCT...`, not ngrok.)

## 3. New-primitive assessments (are these plausibly agent-useful in ways our corpora haven't shown?)

### sci-hub.se + `verify=False` (scispider, 2 skills) — YES, plausibly agent-useful; GENUINELY NEW
Literature-review agents routinely hit paywalls; sci-hub + disabled TLS verification is a paywall-bypass fetcher. Same motive class as observed UNCTAD filter-evasion (GET→POST bridges — real access workarounds, no exploitation). sci-hub appears in NO corpus; `verify=False` pattern is known (4 confirmed in v1) but paired with sci-hub it's a new TTP. Second-order: `verify=False` in skills = MITM-able egress on a fetcher pointed at a piracy host — watch for this pairing in future incident corpora.

### Bitwarden via MCP (1 skill) — YES, plausibly agent-useful; GENUINELY NEW
Puts a password vault behind the model's tool interface. Agent-useful for credential-hygiene flows; adversarially interesting: an agent with vault access that gets prompt-injected now has a credential-read primitive. No vault-via-MCP usage in any corpus. The Corpora show agents using keyless upload APIs and dead drops — a vault primitive is the inverse (keyed read), and it changes what a compromised agent session can reach.

### LocalCan (1 skill) — agent-useful, but NOT egress; GENUINELY NEW primitive class
Local MCP + canister, no network. On-device automation bridge: the agent extends into the user's machine without touching the wire. New in the skill supply chain and absent from corpora, but out of the egress verdict scope — flag for the local-attack-surface lane instead (pairs with the 2026-10-03 bounty-hardening work: notes/env-hardening.md).

### eSIM via crypto purchase — eSIMsForThings (1 skill) — YES, plausibly agent-useful; GENUINELY NEW
Provisions cellular identity via cryptocurrency payment. One primitive gives an agent out-of-band connectivity AND a fresh network identity outside monitored egress (no DNS on the home resolver, no tunnel domain in the skill). Corpora show agents buying infra-adjacent services with crypto nowhere yet. This is the highest-leverage new primitive on the list.

### pinme's tunnel-receiver tutorial (skill code) — YES, plausibly agent-useful; GENUINELY NEW
Teaches agents to RECEIVE inbound tunnelled connections, not just dial out. Reverses the usual tunnel direction (ComposioHQ ngrok-automation is dial-out; pinme is listener-side). New primitive in the skill supply chain; no incident-corpus sighting. If the fleet's shortener-referrer fingerprinting is any guide, a receiver endpoint would show up as an inbound surface — different detection shape than everything we've logged so far.

### wigolo's jina blocklist — NOT an agent primitive; countermeasure signal
jina.ai added wigolo.com (real estate) to a bot blocklist — i.e., site operators are observing and blocking agent-style jina-reader relay traffic in the wild. This corroborates the r.jina.ai ★ (adversarial ecosystem response to the exact tradecraft our corpora document), but it is not a new capability. Treat as external validation of jina-relay prevalence, not as a new primitive.

### (adjacent, also new in the study) uploadthing + vercel-blob (1 skill) — plausibly agent-useful; NEW
Blob-store upload surface = dead-drop-adjacent (keyed upload, public read). Same class as catbox.moe (keyless) but commercial. No corpus sightings.

## 4. Chart-ready verdict table

| # | Destination | In skill scan | In our incident corpora | Verdict (chart label) |
|---|---|---|---|---|
| 1 | ngrok / cloudflared | ★ CONFIRMED (generalized) | absent | ★ seen — skill code only |
| 2 | r.jina.ai | ★ CONFIRMED (6 skills) | CONFIRMED — 618 urlquery rows; go-import gem laundering; fleet-era relay-chaining | ★ seen — confirmed both |
| 3 | Discord/Slack webhooks | ★ CONFIRMED (3 skills) | absent (infra-list mention only) | ★ seen — skill code only |
| 4 | uploads.github.com | ★ CONFIRMED (klavis release-asset path) | absent (harness metadata only) | ★ seen — skill code only |
| 5 | catbox.moe / Litterbox | ★ CONFIRMED (gitshot fallback) | CONFIRMED single-row — `litter.catbox.moe/hdcf0x.html?x=1778400745.7904322` epoch-nonce submission, 2026-05-10 (oai-tag-sweep re-mine) | ★ confirmed both (single incident row) |
| 6 | webhook.site | ZERO (3,853 units) | CONFIRMED — UNCTAD→corsfix bridge inbox c773aa22; AIHW liveness inboxes 00f36f21/0194ba46/0ff0d84e/178c74fe/47a9e270; fleet 2026-10-04 inbox 6ddc559e | ★ seen — confirmed in incidents, absent from skill scan |
| 7 | httpbun | ZERO (3,853 units) | CONFIRMED — 1,096 urlquery rows; AIHW exfil ladder; fleet /anything/gcresult dead-drop; exfil grammar href.li→httpbun/base64→sendBeacon→webhook.site | ★ seen — confirmed in incidents, absent from skill scan |
| 8 | sci-hub.se + verify=False | NEW (scispider) | absent | NEW primitive — paywall-bypass fetcher |
| 9 | email / JMAP | seen (v1) | — | ★ seen — skill code |
| 10 | Bitwarden via MCP | NEW | absent | NEW primitive — credential read |
| — | LocalCan | NEW | absent | NEW — local exec, no network |
| — | eSIM via crypto (eSIMsForThings) | NEW | absent | NEW primitive — cellular identity |
| — | pinme tunnel-receiver tutorial | NEW | absent | NEW primitive — inbound tunnel |
| — | wigolo jina blocklist | — | — | countermeasure signal, not primitive |
| — | uploadthing / vercel-blob | NEW | absent | NEW primitive — blob dead-drop |

**Headline for the chart page:** the inversion is the story. Two of the top destinations (webhook.site, httpbun) are CONFIRMED in incident corpora across four campaigns (UNCTAD, AIHW liveness, AIHW/Tableau sandbox-extraction, Chinese fleet) but appear ZERO times in 3,853 scanned skill units — the skill supply chain and the incident corpora teach different egress playbooks, and the overlap (jina, ngrok, discord webhooks) is the ★-marked bridge between them.

---
*Correlations verified 2026-10-05 against: urlquery hunt wrap-up dataset (`~/workspace/muse-home/projects/urlquery-api-hunt/artifacts/dataset/iocs.csv`), re-hunt pattern dataset (`collections/re-hunt-patterns/data/hits.jsonl`), Chinese Amap fleet events (`data/2026-09-28-chinese-amap-fleet/events.jsonl`, 72 httpbun / 2 webhook.site rows), go-import campaign (`data/2025-03-04-rubygems-goimport-campaign/raw/gem-iocs-2026-09-27.jsonl`), dead-drop inventory (`collections/hunt-missed-surfaces/enumerate/inventory.jsonl`), IOC wordlist (`ioc-wordlist/wordlist.json`), skill-tracer v1 (`~/workspace/muse-home/projects/skill-tracer/reports/findings-v1.md`).*
