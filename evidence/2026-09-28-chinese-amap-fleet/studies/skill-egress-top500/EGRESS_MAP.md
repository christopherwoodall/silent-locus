# Top-500 AI Skills Egress Study — EGRESS MAP

Generated 2026-10-05. Method: skill-tracer scanner + taxonomy (prior art, not re-derived).
Evidence grades: confirmed (bytes present) / pattern-match (corpus tradecraft grammar) /
capability (could be used this way). A high score is NOT an accusation — dual-use network
surface on legitimate tools. Raw evidence: `raw/scan-a.json`, `raw/scan-b.json`, `raw/scan-c.json`.

## Headline counts
- Skills enumerated: **358 unique identities** (lane A 216 + lane B 142)
- Repos/packages fetched: **177** (lane C 67 + lane D 65 + lane E 45)
- Skill units scanned: **3,853** (C 3,392 · D 317 · E 144)
- Units with egress hits: **800** (C 625 · D 91 · E 84)
- Total hits: C ~6,600 (184 CRITICAL-unit · 63 HIGH-unit · 134 MEDIUM-unit) ·
  D 7,639 raw (3,613 code-honest; 12 CRITICAL hand-verified) ·
  E 4,234 (CRITICAL 248 · HIGH 1,908 · MEDIUM 2,078)

## Top-10 riskiest egress destinations (by confirmed primitive utility)

| # | Destination | Risk grade | Where confirmed |
|---|-------------|-----------|-----------------|
| 1 | **ngrok / cloudflared tunnels** (agent-exposed localhost) | data-exfil / credential-adjacent | loki-mode (C: parses public URLs from ngrok API + cloudflared logs), pinme (C: instructs agent to expose localhost), telnyx-mcp (E: agent-controllable `--ngrok-enabled` tunnel for inbound webhooks, 390K/wk installs), browser-use (E: QA docs reference ngrok/cloudflared) |
| 2 | **r.jina.ai** (keyless reader proxy) | paywall-bypass / data-exfil | last30days-skill (C: `JINA_READER_PREFIX` keyless fallback), twitter-reader (C: primary fetcher), trendradar (D: `JINA_READER_BASE`, 62.7k★), deep-research-mcp (D), gpt-researcher (D patch), sjh110007/mcp-jina-ai (E: `fetch('https://r.jina.ai/', POST body:{url})`) |
| 3 | **Discord/Slack webhooks** (dead-drop grammar) | data-exfil | loki-mode (C: `hooks.slack.com` + `discord.com/api/webhooks` notify.sh), last30days (C: Slack webhook alerts), quantdinger (D: trading-signal notifier POSTs to Discord+Slack+Telegram) |
| 4 | **uploads.github.com** (GitHub trusted image host) | data-exfil | klavis MCP servers (D: wired as upload host in Go client) — gitshot grammar via Release Assets also confirmed in gitshot + coffee-gb (C) |
| 5 | **catbox.moe** (no-signup image host) | data-exfil | gitshot (C: screenshot→catbox fallback, byte-identical copy in coffee-gb) |
| 6 | **sci-hub.se** (paywall bypass, TLS-bypassed) | paywall-bypass | paper-search-mcp-openai (E: `verify=False` on Sci-Hub fetches) |
| 7 | **email (JMAP send + blob attachments)** | data-exfil | Atomic-Mail atomic-mail-agentic (E: autonomous email send + RFC 8620 attachments), anon.li + Atomic Mail Agentic listings (B) |
| 8 | **Bitwarden vault via MCP** | credential-adjacent | bitwarden/mcp-server (E fetched) — agent-readable secrets vault |
| 9 | **localhost-tunnel brokers** (LocalCan) | credential-adjacent | localcan (B/E: localhost tunnel service; docs-only, closed binary) |
| 10 | **eSIM purchase API (crypto-funded)** | data-exfil / credential-adjacent | Roamzy (B: agent buys eSIMs with crypto — identity-adjacent egress) |

## Corpus-toolkit match verdict (our hunt corpora)

| Pattern | Verdict | Detail |
|---------|---------|--------|
| r.jina.ai keyless fetch | **CONFIRMED, 6 skills** | last30days (v1 re-confirmed), twitter-reader, trendradar (top-starred MCP server in lane), deep-research-mcp, gpt-researcher, mcp-jina-ai. NOTE: our skill-ladders lane (2026-10-03) judged r.jina.ai keyless DEAD as of now — these skills still ship the fallback; worth a live-check decision by parent (opsec: don't knock on the operator's door) |
| webhook.site/discord/slack dead-drop grammar | **CONFIRMED (discord/slack); webhook.site ZERO** | loki-mode, last30days, quantdinger. webhook.site itself: 0 hits across all 3,853 units |
| httpbun / httpbin | **ZERO / benign** | httpbin.org appears only as teaching examples (C, pattern-match benign). httpbun: 0 |
| gitshot-style uploads | **CONFIRMED** | gitshot→GitHub Release Asset + catbox.moe propagates byte-identically into trekawek/coffee-gb; klavis wires uploads.github.com. uploads.github.com direct: 0 in lane C, confirmed in lane D |
| ComposioHQ ngrok-automation | **CONFIRMED, generalized** | loki-mode and telnyx-mcp independently implement agent-driven ngrok exposure; pinme teaches it. The primitive is now generic, not ComposioHQ-specific |
| epoch nonces / zz labels / A000-ZZEND | **ZERO** | No agent-grammar markers in any scanned skill |
| verify=False / TLS bypass | **CONFIRMED, 4** | gpt-researcher, hexstrike-ai, xhs-downloader (D), paper-search-mcp-openai (E) |
| go-import canary tags | **ZERO** | RubyGems-era pattern absent from skill supply chain |

## Notable new primitives (not in prior taxonomy)
- **Tunnel-receiver construction taught to agents** (pinme): skill docs instruct building a webhook receiver + exposing localhost — the tutorial itself is the egress lesson.
- **wigolo blocklists r.jina.ai** (D): first observed counter-pattern — a fetch skill that rejects the corpus relay as a redirector.
- **Meta-gateways** (B): pipeworx/gateway, SparkForge, UnClick, Gapup — hundreds of tools behind one operator, all remote-only (unscannable); the concentration itself is the risk.
- **Remote-only top listings** (B/E): most high-use Smithery servers have no public source — the most-installed MCP surface is the least auditable.

## Secrets noted (never used)
- Sentinel canaries: `ghp_LOKIWITHHELD*INVALID` (loki-mode), `ghp_AAAA…` test fixture (get-shit-done), `sk-abcdef…xyz` placeholder (videocut-skills)
- sentry-mcp test fixtures contain secret-shaped tokens (redacted in scan output)
- klavis: 13 secret-shaped hits, all test fixtures / `.env.example` placeholders

## False-positive log (for scanner tuning)
"bore" as CAD term (32 hits), "files" literals, `profiles = {}` substring, `--insecure` curl flag vs TLS bypass,
`/dev/tcp/` port-check vs reverse shell, Tabler icon "chisel", fontawesome "bore" CSS, go.mod deps, comments about cloudflared, `/zz/` inside base64 SVG.
