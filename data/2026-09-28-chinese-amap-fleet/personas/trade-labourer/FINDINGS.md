# Trade Labourer — supply-chain recon

Persona: hunt the commercial underbelly that agent swarms buy from. Agents need tunnels, proxies, captcha solvers, phone verification, cloud accounts, hosting, API keys. A swarm's infra bill is a fingerprint.

Date: 2026-10-05. Status: core lanes mapped; captcha/SMS and VPS/keys subagents still running.

## 1. Agent-first tunnel services (the new supply layer)

The biggest finding: a whole generation of tunnel services now markets EXPLICITLY to AI agents. ngrok's interstitial page "breaks agents" — that complaint is the founding pitch for several:

| Service | Domain | Pitch | Agent-specific features |
|---|---|---|---|
| tunn3l | tunn3l.sh | "The tunnel service built for AI agents" | JSON output, env-var config, exit codes, zero signup, `--json` flag; `*.tunn3l.sh` |
| LivePort | (dundas/liveport GitHub) | "Secure localhost tunnels for AI agents" | MCP server + agent SDK + CLI; no interstitial; auto-assigned persistent URLs |
| Pinggy | pinggy.io | "built for AI-agent workflows" | Agent Skill (`npx skills add`), MCP server for Claude Code/Cursor; free SSH tunnels |
| portal | gosuda/portal (GitHub) | "Publishes localhost services to the agentic web" | x402 payments, **multi-hop routing for anonymity**, SNI hiding/ECH, self-hostable |
| AgentWebhook | app.agentwebhook.com | pull-based webhook relay, "alternative to tunneling tools" | agents pull events, no inbound ports — **tunnels not needed at all** |
| SteadIP | steadip.com | free FRP tunnels (launched Jul 2026) | developer/homelab market |
| Vinkius | vinkius.com | Cloudflare Tunnel MCP | manage CF tunnels via agent prompts |

Detection implication: swarms migrating to these leave `*.tunn3l.sh` / pinggy / liveport traces instead of `lhr.life`. Hunt grammar for new fleets should include these domains. The portal-tunnel one is the most opsec-conscious (multi-hop + ECH + x402) — built for unattributable agent infra.

## 2. Hosted browser farms (the invisible middleman)

Browserbase ($20–99/mo, Stagehand SDK, 10k+ companies), Steel (open-source, self-hostable), Hyperbrowser (stealth/CAPTCHA-solving priced in), Anchor (own "humanized Chromium" fork), Browserless (veteran), Bright Data / Oxylabs / ZenRows (CDP-over-WS scraping browsers). All ship MCP servers.

Detection implication: a swarm running on Browserbase et al. leaves the PROVIDER's fingerprints, not its own. The `settings.useragent` would be the provider's fleet browser. Attribution shape: look for provider-infra markers (e.g. `brd.superproxy.io`, `browser.zenrows.com`) rather than operator markers.

## 3. Proxy providers courting agents

Webshare (agent skill: `npx skills add webshare-proxy/skills/proxy-manager`; 80M+ residential IPs; free tier), CyberYozh (50M+ residential + SMS verification + IP reputation checks — one-stop agent shop), SwiftProxy (80M+), RapidProxy (90M+, **AI-powered CAPTCHA bypass**), Decodo (115M+, MCP server, OpenClaw integration), Infatica, Oxylabs (MCP angle). All API-first, agent-doc'd.

## 4. Infra-bill fingerprint of OUR operator

Cross-check vs known `uq` swarm (lhr.life tunnels, is.gd shortener, webhook.site dead-drops, jina/allorigins/translate.goog fetch proxies):

- **Everything is free tier.** No paid proxies, no browser farm, no captcha API, no VPS receipts. localhost.run free SSH tunnels, is.gd free shortener, webhook.site free tier, free fetch proxies.
- That is itself the fingerprint: a swarm that pays for nothing. Matches an eval/research-style operator or a budget-conscious one — NOT a commercial buyer. Contrast with the Dream swarm (harness unspecified) and any swarm that would leave Browserbase/proxy-provider receipts.
- Prediction (for the Mimic): if this operator scales, the first paid line item would be tunnels (lhr.life is the load-bearing piece). Watch for migration to tunn3l.sh/pinggy/agent-first services when localhost.run limits bite.

## 5. Corpus + urlquery cross-checks

- Our 2,141-record corpus: ZERO hits for tunn3l/liveport/pinggy/portal/steadip/agentwebhook/zrok/trycloudflare/vinkius/bore.
- urlquery htmx for tunn3l.sh/pinggy/liveport/portal/agentwebhook: **throttled** (empty responses after heavy use) — retry pending. Flagged for the ua-burst-retry-style cron pattern.

## 6. Shadow-AI exposure surface (bonus)

Censys: 12,520 internet-reachable MCP services (Apr 28 2026) → 21,000+ by May 6, unauthenticated. Ruflo MCP bridge RCE (Jun 30 disclosure, GHSA-c4hm-4h84-2cf3) → agent hijack + API-key exfiltration. This is agent infrastructure LEAKING publicly — itself a hunt surface (scan for exposed MCP = find agent deployments, including swarms').

## 7. CAPTCHA solvers + SMS verification (subagent, detail in captcha-sms.md)

- **CapSolver is the standout** — the ONLY solver with an official MCP server (`capsolver-mcp`, PyPI v0.1.1, MIT, MCP Registry listed). Five tools, stdio/SSE/streamable-http, docs for Claude Code/Cursor/Windsurf. An agent bypasses CAPTCHAs with zero integration code. ~$0.80/1k reCAPTCHA.
- 2Captcha ($1 deposit, ~$2.70–3.50/1k) — no agent marketing, but its `createTask`/`getTaskResult` protocol is the industry lingua franca.
- Anti-Captcha ($10 top-up, since 2007, crypto accepted) — enterprise automation, no MCP.
- YesCaptcha (1,000 points = 1 CNY) — 2captcha-protocol compatible; one-line provider hot-swap.
- NopeCHA (~$0.011/1k, AI-only, stealth mode) — collapses cost floor to ~zero.
- **5SIM — strongest bot-catering signal**: ~$0.007/activation, crypto, explicit "create unlimited accounts"/#OTPbypass marketing. The creation layer.
- SMS-MAN (200+ countries, PayPal→WeChat Pay), OnlineSIM (long-term rentals = retention layer), Detect.Expert ($0.02 virtual / $0.49 residential "clean" numbers for mass registration).
- A full account costs **under $0.10** (CAPTCHA ~$0.001 + SMS ~$0.01–0.06). Most likely swarm stack: CapSolver (MCP) + 5SIM/SMS-MAN (creation) + OnlineSIM (retention).
- Detection notes: MCP manifests referencing `capsolver-mcp`/`CAPSOLVER_API_KEY`, `clientKey` configs, registration-burst ↔ SMS-OTP timing correlation.

## 8. Cheap VPS, sandboxes, API-key markets (subagent, detail in vps-keys.md)

- **$2.50–5/mo tier**: Vultr ($2.50), InterServer ($3.00), Time4VPS (€2.88), OVHcloud (€3.81 unlimited), Contabo (€4.40 unlimited). Self-hosted harness ≈ $6/mo vs ~$545/mo managed-sandbox equivalent (~100x gap).
- **E2B**: $0.0504/vCPU-hr; Hobby = one-time $100 credit. E2B/Daytona/Modal/Blaxel/Cloudflare Sandbox all attach billing identity + telemetry → **attribution-hostile for a swarm**. Economic move: self-hosted OSS sandboxes (Temps, microsandbox, Lume) on cheap VPS.
- **API-key markets (fully public)**: plati.market ($10 auto-delivered via OneAPI-style endpoints), BlackHatWorld (USDT/BTC, 3-day warranty), Telegram @opustokens_bot (Telegram Stars), infostealer-log resellers (~$5 working Claude/ChatGPT sessions; FlashPoint: 24 valid keys in one 44k-JWT dump), CN grey market ~10% of list. Anthropic Sept 2026 report: fake "cheap Claude" reseller GTG-50021 proxied to other models + installed credential harvester.
- **Bulletproof-adjacent**: floors ~€5–8/mo (FlokiNET €7.99, exodia.run-class ~€7 XMR/BTC via Tor, AlexHost €5.90, QloudHost $4.16 no-KYC, Njalla €15). Dutch police seized ~250 servers Dec 2025 — top tier is a live LE target.
- **Synthesis**: a swarm node runs **<$20/mo**, payable in Monero/USDT, mostly identifier-free. Anonymity is cheapest at the KEY layer, not compute; the real bottleneck is IP reputation and rate limits (proxy overlays = follow-up lane).

## 9. Open lanes / follow-ups

- urlquery htmx for tunn3l.sh/pinggy/liveport/portal/agentwebhook: throttled (empty responses) — retry pending.
- Proxy-overlay supply chain (residential pools as operational bottleneck) — flagged as follow-up lane, not yet run.
