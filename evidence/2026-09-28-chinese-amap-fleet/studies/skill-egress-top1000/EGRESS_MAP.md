# Top-1000 AI Skills Egress Study — EGRESS MAP (extension: identities 359–1013)

Generated 2026-10-05. Method: skill-tracer scanner + taxonomy, unmodified (same as top-500).
Evidence grades: confirmed (bytes present) / pattern-match (corpus tradecraft grammar).
A high score is NOT an accusation — dual-use network surface on legitimate tools.
Raw evidence: `raw/scan-d1.json`, `raw/scan-d2.json`, `raw/scan-d3.json`, `raw/scan-f1.json`, `raw/scan-f2.json`.
Known-URL hunt: `raw/known-url-hunt.md`. Novel-domain extraction: `raw/new-urls.md`.
Top-500 verdicts are referenced, not re-derived (`../skill-egress-top500/EGRESS_MAP.md`).

## Headline counts
- Skills enumerated: **655 new identities** (lane A-ext 450 + lane B-ext 205); **1,013 combined**
- Repos/packages fetched: **260 new** (F1 46 · F2 88 · F3 59 · H1 16 · H2 51); **437 combined**
- Skill units scanned: **2,490 new** (F1 1,772 · F2 304 · F3 343 · H1 27 · H2 44); **6,343 combined**
- Units with egress hits: **741 new** (F1 411 · F2 153 · F3 122 · H1 17 · H2 38); **1,541 combined**
- Total hits (new): **57,352** (CRITICAL 1,564 · HIGH 17,586 · MEDIUM 38,202)
- By category (new, raw): netcall/MEDIUM 31,290 · img_upload/HIGH 7,931 · browser/HIGH 7,717 · gitwrite/MEDIUM 2,555 · email/HIGH 1,276 · tunnel/CRITICAL 1,195 · dns/MEDIUM 1,006 · creds/HIGH 441 · img_upload/CRITICAL 369 · webhook/HIGH 197

## Top destinations, ranked by confirmed primitive utility (extension)

| # | Destination | Risk grade | Where confirmed |
|---|---|---|---|
| 1 | **Discord/Slack/Telegram webhooks** (dead-drop grammar, runtime) | data-exfil | ★ jeremylongshore tons-of-skills `whale-alert-monitor`: runtime `_send_discord` (aiohttp POST), `_send_slack`, Telegram `sendMessage` — complete dead-drop grammar in one shipped skill. hooks.slack.com in 13 skills (runtime also in clawd-on-desk hardened slack-notify-client). discord.com/api/webhooks in 4 |
| 2 | **★ r.jina.ai** (keyless reader relay) | paywall-bypass / data-exfil | 6 skills; **runtime** in glidea-zenfeed (keyless-fallback crawler — exact corpus tradecraft) and Prismer `recover_page.py` |
| 3 | **★ uploads.github.com** (trusted image host) | data-exfil | **runtime** release/pack-asset upload code in 777genius-agent-teams-ai and FailproofAI (3 skills) |
| 4 | **sci-hub.se** (paywall bypass) | paywall-bypass | **runtime**: openags-paper-search-mcp exposes MCP tools `download_scihub` / `download_with_fallback` defaulting to `https://sci-hub.se` — paywall-bypass as a tool primitive. (The scanner MISSED it: scan-d2's unit was scoped to the repo's `claude-code` subdirectory — see coverage gap below.) |
| 5 | **ngrok / cloudflared** (tunnels) | data-exfil / credential-adjacent | 18 / 12 skills — docs/tutorial only. Contrast: top-500 had runtime (loki-mode, telnyx-mcp). No agent-driven tunnel launch in the extension |
| 6 | **smtp/sendmail** (email) | data-exfil | 47 skills — docs/config only, no runtime send path found |
| 7 | **Relay cousins (new)**: **zread.ai** | paywall-bypass / data-exfil | 3 skills reference zread.ai as a developer-documentation reader — first jina-style relay cousin in the skill supply chain |
| 8 | **Tunnel cousins (new)**: **loca.lt**, **ngrok.app** | data-exfil | loca.lt taught as the webhook-receiver exposure path (tons-of-skills vercel-webhooks-events SKILL.md); ngrok.app (ngrok's current endpoint domain) in MCP adapter test fixtures |
| 9 | **File-host cousins (new)**: **r2.dev**, **kleros-ipfs-gateway.fly.dev**, **plannotator.workers.dev** | data-exfil | R2 public buckets (`pub-*.r2.dev`) as no-auth asset hosts (3 skills); Kleros IPFS gateway — crypto-micropayment upload ($0.01 USDC on Base) as a skill's canonical upload path; plannotator's self-hosted encrypted paste (AES-256-GCM, key-in-URL) as default share endpoint |
| 10 | **Email-family (new)**: **mailgun**, **mcpagentmail.com** | data-exfil | mailgun wired as a provider in YaoApp-yao's 8-provider messenger matrix (mailgun, twilio, dingtalk, discord, feishu, telegram, weixin + discord integrations — one skill, send-capability across all); mcpagentmail.com — agent-to-agent email/inbox coordination MCP (34 tools, Russian-language research doc) |

## Corpus-toolkit match verdict (extension)

| Pattern | Verdict | Detail |
|---------|---------|--------|
| r.jina.ai | **CONFIRMED, 6 skills (runtime in 2)** | glidea-zenfeed keyless-fallback crawler; Prismer recover_page.py |
| discord/slack webhooks | **CONFIRMED, runtime** | whale-alert-monitor ships the complete grammar (Discord+Slack+Telegram) |
| webhook.site | **8 hits — docs/test/blocklist only** | No live dead-drop POST code. Consistent with top-500's zero |
| httpbun | **ABSENT** | Consistent with top-500 |
| uploads.github.com | **CONFIRMED, runtime (2 skills)** | 777genius-agent-teams-ai, FailproofAI release-asset upload code |
| ngrok | **18 skills — docs/tutorial only** | No agent-driven launch (top-500 had runtime loki-mode/telnyx-mcp) |
| verify=False / TLS bypass | **18 hits — catalogs/tests/docs** | No runtime TLS-bypass fetch found (top-500 had runtime in 4) |
| catbox.moe | **ABSENT** | Only a YARA signature mention |
| litterbox | **name collision** | BlackSnufkin-LitterBox is a malware-analysis sandbox skill, not the file host |
| bitwarden / localcan / roamzy | **ABSENT** | Incidental mentions / identifier-substring FPs only |
| go-import canary tags | **2 prose mentions** | Not the RubyGems grammar |
| epoch nonces / zz labels / A000-ZZEND | **ZERO** | A000 hits are bio motif IDs / insurance policy numbers / CSS hex / base64 noise. Matches top-500's clean negative |

## Notable new primitives (not in prior taxonomy)
- **Complete runtime dead-drop grammar in one skill** (whale-alert-monitor): crypto whale monitor with configurable Discord/Slack/Telegram notifiers — the top-500 saw the grammar in parts; here it ships whole.
- **Paywall-bypass as an MCP tool** (openags-paper-search-mcp `download_scihub`): the primitive graduates from skill code to tool interface.
- **zread.ai**: first relay cousin of r.jina.ai observed in the supply chain (3 skills).
- **Crypto-micropayment file upload** (kleros-ipfs-gateway.fly.dev): $0.01 USDC per upload on Base — pay-per-upload decentralized hosting as a skill's default.
- **8-provider messenger matrix** (YaoApp-yao): one skill hands an agent send-capability across mailgun/twilio/dingtalk/discord/feishu/telegram/weixin.
- **Agent-to-agent email** (mcpagentmail.com): 34-tool MCP for inter-agent coordination — email-family primitive aimed at swarms.
- **API-key reseller routing** (aihubmix.com, anyrouter.top, agentrouter.org, ai-router.dev, qixing1217.top): a skill ("all-api-hub") routing users to third-party key resellers with affiliate links — supply-chain-adjacent monetization.
- **Tailscale tailnet endpoint** (ts.net): voice skill phoning a tailnet-hosted inference server — network-topology primitive.
- **AI API routers as a sub-family**: models.dev (live model catalog consumed by 3 skills' tooling).

## Scanner coverage gap (methodological finding)
- `openags-paper-search-mcp` (lane-f2): the scan unit was scoped to the repo's `claude-code` subdirectory → 0 hits recorded, but the `download_scihub`/`download_with_fallback` tools live elsewhere in the repo. **Subdirectory-scoped units undercount.** Recommend: when a repo root lacks skill markers but subdirs were cherry-picked, record the scoping decision per unit.

## Secrets noted (never used)
- 441 creds/HIGH raw hits across the new lanes; secret-shaped values retained whole in scan JSONs per evidence policy. Triage of top units: test fixtures, `.env.example` placeholders, and provider-config templates predominate (same pattern as top-500's klavis/sentry findings). None used or transmitted.

## False-positive log (for scanner tuning)
- `slack.com.co`, `hooks-slack.com`, `evilslack.com`: lookalike-domain *rejection* tests, not egress.
- `reasonix.io`: matched `ix.io` substring — actually the Reasonix CLI company.
- `ifttd.io`: "If This Then Dev" podcast, not IFTTT.
- `wormholescan.io`: Wormhole blockchain-bridge explorer, not the file-transfer Wormhole.
- `omb-u-*.fly.dev`: OpenMausBot cloud-instance fixtures (one realistic-looking docs entry).
- tons-of-skills mega-catalog dominates volume counts (unit score 21,003 — size-inflated; occurrence ranking is volume-driven, not risk-driven).
- `printer.local`, `100.1`, `1.4`: mDNS/test hosts and version-string FPs in URL extraction.
