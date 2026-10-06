# Skill-Egress Study — Lane D: fetch + scan (cursor rules + MCP servers batch)

Date: 2026-10-05. Operator: lane-d subagent. Status: COMPLETE.
Method: skill-tracer (`scan/egress_scan.py` + `egress-taxonomy.md`), run unmodified.
Scanner run: `python3 ~/workspace/muse-home/projects/skill-tracer/scan/egress_scan.py ~/workspace/skill-egress-work/lane-d --out raw/scan-b.json`
→ `scanned 317 skill units, 91 with egress hits -> scan-b.json`
Clones: shallow (`git clone --depth 1`), public repos only, never committed (scratch only, `~/workspace/skill-egress-work/lane-d/`, 2.0G, 65 dirs).
Pacing: sequential sweep first (4 repos), then 6-way parallel (GitHub tolerated it); 5 transient `Proxy CONNECT aborted` failures retried sequentially — all recovered. Final: 65/65 complete.
Grading per taxonomy: confirmed (bytes present) / pattern-match (corpus tradecraft grammar). Score = 3×critical + 2×high + 1×medium → CRITICAL ≥10, HIGH ≥6, MEDIUM ≥3, LOW ≥1, NONE 0.
A high score is NOT an accusation — dual-use network surface on legitimate tools. Corpus matches flagged separately.
Evidence policy: full observed values retained in scan-b.json (never redacted); secrets noted, never used.

## Fetch log — 65 repos, all fetched

### A. Cursor rules (8)
| repo | stars | result |
|------|-------|--------|
| PatrickJS/awesome-cursorrules | 40,878 | ok — 150+ .mdc rules; README links no external rules repos (only claire-gong-18 mirror) |
| grapeot/devin.cursorrules | 5,965 | ok |
| kinopeee/cursorrules | 1,111 | ok |
| s-smits/agentic-cursorrules | 646 | ok |
| holtwood/awesome-cursorrules-zh | 236 | ok |
| BlueBirdBack/godot-cursorrules | 119 | ok |
| ali-abassi/OpenAI_Assistant_API_Boilerplate_CursorRules | 52 | ok |
| nedcodes-ok/cursorrules-collection | 37 | ok |

### B. modelcontextprotocol/servers (1)
| repo | stars | result |
|------|-------|--------|
| modelcontextprotocol/servers | 91,012 | ok — network-capable subdirs scanned as units: fetch, github, gitlab, brave-search, slack, google-maps, perplexity-ask, everart, postgres, puppeteer (+ local-only: filesystem, sqlite, memory, sequential-thinking) |

### C. Top community MCP servers (44)
| repo | stars | repo | stars |
|------|-------|------|-------|
| D4Vinci/Scrapling | 85,734 | upstash/context7 | 62,688 |
| sansan0/TrendRadar | 62,676 | ChromeDevTools/chrome-devtools-mcp | 52,904 |
| microsoft/playwright-mcp | 37,827 | github/github-mcp-server | 33,373 |
| feder-cr/invisible_playwright_mcp | 31,776 | ComposioHQ/composio | 30,441 |
| oraios/serena | 29,996 | assafelovic/gpt-researcher | 29,920 |
| czlonkowski/n8n-mcp | 22,900 | Evil0ctal/Douyin_TikTok_Download_API | 20,469 |
| wanshuiyin/Auto-claude-code-research-in-sleep | 16,468 | xpzouying/xiaohongshu-mcp | 16,110 |
| yusufkaraaslan/Skill_Seekers | 13,519 | JoeanAmier/XHS-Downloader | 12,474 |
| OpenByteInc/QuantDinger | 12,453 | tadata-org/fastapi_mcp | 12,317 |
| 0x4m4/hexstrike-ai | 12,017 | mcp-use/mcp-use | 10,722 |
| 0xJacky/nginx-ui | 10,731 | apify/apify-mcp-server | 9,577 |
| awslabs/mcp | 9,646 | firecrawl/firecrawl-mcp-server | 7,553 |
| devlikeapro/waha | 7,546 | AgentDeskAI/browser-tools-mcp | 7,329 |
| BrowserMCP/mcp | 7,159 | Klavis-AI/klavis | 5,808 |
| KnockOutEZ/wigolo | 5,444 | FunnyWolf/Viper | 5,232 |
| exa-labs/exa-mcp-server | 5,079 | atilaahmettaner/tradingview-mcp | 4,914 |
| u14app/deep-research | 4,694 | makenotion/notion-mcp-server | 4,660 |
| cloudflare/mcp-server-cloudflare | 4,352 | browserbase/mcp-server-browserbase | 3,410 |
| taylorwilsdon/google_workspace_mcp | 3,281 | tavily-ai/tavily-mcp | 2,418 |
| korotovsky/slack-mcp-server | 1,854 | Flux159/mcp-server-kubernetes | 1,595 |
| suekou/mcp-notion-server | 918 | jerhadf/linear-mcp-server | 346 |
| zapier/zapier-mcp | 426 | triggerdotdev/trigger.dev | 16,468 |

*trigger.dev star count from topic search (16,110 page-1 value; API recheck not repeated — treat as ~16k).
Dropped after verification: stripe/agent-toolkit (404), supabase-community/supabase-mcp (404), jlowin/fastmcp (404), ahujasid/blender-mcp (404), n8n-io/n8n + activepieces (platform monorepos, out of skill scope), getsentry/MobileBuildMCP + MinishLab/semble (lower network signal, budget).

### D. Roo / Cline modes + rules (8)
getzenai/feature-roo-configs, christianbaumann/feature, feature-foundation/feature (one lineage), xavier-arosemena/custom-modes-roo-code (290-mode fork), jtgsystems/Custom-Modes-Roo-Code (upstream), cline/clinerules (official Cline rules/skills/workflows), blitzingminty/clinerules, henryalps/vscode-clinerules — all ok.

### E. aider conventions (4)
Aider-AI/conventions (official org), avicennasis/conventions, vloddos/conventions, delphoa/study-aider-conventions — all ok.

## Scan results (raw/scan-b.json)

317 skill units; 91 with ≥1 hit. Risk tiers (raw score): CRITICAL 47 · HIGH 12 · MEDIUM 15 · LOW 17 · NONE 226.
Raw hits: 7,639 total — MEDIUM 4,352 · HIGH 3,154 · CRITICAL 133.
By (category, severity), raw: netcall/MEDIUM 3,767 · browser/HIGH 2,082 · img_upload/HIGH 530 · email/HIGH 468 · gitwrite/MEDIUM 250 · browser/MEDIUM 197 · img_upload/CRITICAL 75 · dns/MEDIUM 71 · tunnel/CRITICAL 58 · creds/HIGH 40 · email/MEDIUM 26 · creds/MEDIUM 24 · webhook/HIGH 24 · relay/MEDIUM 10 · relay/HIGH 10 · registry/MEDIUM 3 · webhook/MEDIUM 2 · paste/MEDIUM 1 · corpus/MEDIUM 1.

**Code-only filter** (excluded tests/docs/examples/vendor/minified/svg/css/go.sum/go.mod — the honest signal): 3,613 hits — HIGH 1,631 · MEDIUM 1,970 · CRITICAL 12.
Code-only CRITICAL = 7 tunnel + 5 img_upload, and **every one was verified by hand** (see false-positive log). Code-only by category: netcall 1,684 · browser/HIGH 992 · img_upload/HIGH 330 · email/HIGH 281 · gitwrite 167 · dns 51 · browser/MEDIUM 37 · creds/MEDIUM 16 · creds/HIGH 13 · webhook/HIGH 9 · email/MEDIUM 8 · tunnel/CRITICAL 7 · relay/HIGH 6 · img_upload/CRITICAL 5 · registry 2 · relay/MEDIUM 2 · webhook/MEDIUM 2 · paste 1.

Top units by code-only score: klavis/mcp_servers 720 · cloudflare-mcp 701 · wigolo 548 · triggerdev 419 · composio 264 · custom-modes-roo-code-upstream 204 · quantdinger 202 · mcp-use 200 · nginx-ui 198 · chrome-devtools-mcp 176 · playwright-mcp 169 · n8n-mcp 154 · browserbase-mcp 150 · gpt-researcher 145 · trendradar 121 · awesome-cursorrules 111/124 (unit naming) · openai-assistant-cursorrules 100 · aris-skills/paper-poster-html 98 · waha 96 · hexstrike-ai 73.

## Hunt-corpus toolkit matches (all hand-verified)

- **r.jina.ai — CONFIRMED live relay usage (3):**
  - `trendradar/mcp_server/tools/article_reader.py:18` — `JINA_READER_BASE = "https://r.jina.ai"`; `ArticleReaderTools.__init__(..., jina_api_key=None)` — the MCP article-reader tool fetches article bodies *through the jina reader relay*. Real laundering-stack primitive in a 62k-star MCP server.
  - `deep-research-mcp/src/utils/crawler.ts:22` — `fetch("https://r.jina.ai", {...})` in the crawler — same pattern.
  - `gpt-researcher/deep_agents/drb_harness.patch:36,62` — r.jina.ai in a harness patch (historical/auxiliary).
  - **Negative (verified):** `wigolo/src/agent/relevance.ts:13,22` lists r.jina.ai in a `REDIRECT_HOSTS` *blocklist* — wigolo explicitly rejects jina URLs as candidates, does not use it.
- **discord.com/api/webhooks + hooks.slack.com — CONFIRMED (1):**
  - `quantdinger/backend_api_python/app/services/signal_notifier.py:12` (`"discord": "https://discord.com/api/webhooks/..."`), `:121` (`if "discord.com/api/webhooks" in raw:`), `:129`, `:720` hooks.slack.com, plus `notifications/webhook.py:21` — a trading-signal notifier that POSTs signals to Discord/Slack webhooks; `:967` `https://api.telegram.org/bot{token}/sendMessage` — same notifier, Telegram leg. Webhook dead-drop grammar, live in an agent-trading OS.
  - n8n-mcp: discord/slack/webhook matches are in test fixtures (`tests/extracted-nodes-db/*`, `workflow-sanitizer.test.ts`) and the `webhook_processing.md` skill doc — documentation/test, not runtime.
- **webhook.site — docs only:** waha `.env.example:143` (`# WHATSAPP_HOOK_URL=https://webhook.site/11111111-...`), `webhooks.config.dto.ts:74,77` (OpenAPI example) — placeholder documentation, not a live dead-drop.
- **uploads.github.com — CONFIRMED code paths (2):**
  - `klavis/mcp_servers/github_mcpmark/internal/ghmcp/server.go:290` and `github_official/pkg/utils/api.go:66` — `uploadURL, err := url.Parse("https://uploads.github.com")` in the GitHub MCP server's API-host config: the MCP GitHub tool can push attachments through GitHub's upload endpoint (the gitshot exfil grammar, in a 5.8k-star MCP server).
  - triggerdev `webhook-sources/.../hookdeck-samples.json:7577`, klavis `howtocook/.../all_recipes.json:31502` (user-images), n8n-mcp `.github/workflows/release.yml:266` — fixtures/CI, not runtime.
- **ngrok — NO live tunnel usage.** klavis `slack_atlas/go.mod|go.sum` = dependency files; `*_test.go` = tests; composio `toolkit-slugs.ts:978` = `'ngrok'` is a *toolkit slug* (Composio ships an ngrok API integration users can invoke — integration surface, not a tunnel opened by the skill); gpt-researcher eval JSONL + fontawesome `bore` CSS class = noise.
- **cloudflared — docs only:** wigolo `src/daemon/admin-token.ts:8`, `http-server.ts:299` are comments describing a `cloudflared remote-serve` deployment pattern; no tunnel code.
- **httpbun/httpbin — zero hits** across all 65 repos.
- **verify=False — CONFIRMED (3 code sites):** `gpt-researcher/gpt_researcher/scraper/pymupdf/pymupdf.py:53` (`http.get(self.link, ..., verify=False)` — PDF fetch); `hexstrike-ai/hexstrike_server.py:13766,13844` (pentest header-check fetches); `xhs-downloader/source/application/request.py:84`, `source/module/manager.py:102,109` (Xiaohongshu downloader — TLS verification disabled on a mass-download tool). google-workspace-mcp `verify=False` is an unrelated function parameter in a test — false positive.
- **zz labels / epoch nonces — 1 hit, FALSE POSITIVE:** `composio/docs/public/images/clients/cursor.svg:12` matched `/zz/` inside a base64 image blob. No agent-grammar `zz=` params, no epoch-nonce params, no `A000`/`ZZEND` markers anywhere in lane D.
- **paste dead-drops:** 1 code hit (paste category) — low signal, details in scan-b.json.
- **registry:** 2 code hits (go-import/postinstall patterns) — details in scan-b.json.

## Top-5 riskiest (verified, ranked by confirmed primitives — NOT raw score)

1. **quantdinger (OpenByteInc/QuantDinger, 12.5k★) — code-only 202, CRITICAL.** Agent-trading OS whose `signal_notifier.py` POSTs trade signals to Discord webhooks (`:12`, `:121`), Slack webhooks (`:129`, `:720`, `webhook.py:21`) and Telegram `sendMessage` (`:967`), with curl multipart upload calls. Webhook+email-HIGH dead-drop grammar, live and runtime. Excerpt: `quantdinger/backend_api_python/app/services/signal_notifier.py:12: "discord": "https://discord.com/api/webhooks/..."`.
2. **klavis/mcp_servers (Klavis-AI/klavis, 5.8k★) — code-only 720, CRITICAL.** MCP integration platform; GitHub MCP servers wire `https://uploads.github.com` as the upload host (`github_mcpmark/internal/ghmcp/server.go:290`, `github_official/pkg/utils/api.go:66`) — agent-driven file upload to GitHub's trusted image host. Also 13 secret-shaped token hits (test fixtures + `.env.example` placeholders; full values retained in scan-b.json, never used).
3. **trendradar (sansan0/TrendRadar, 62.7k★) — code-only 121, CRITICAL.** MCP news-aggregation server whose article reader fetches *through* `https://r.jina.ai` (`mcp_server/tools/article_reader.py:18`, `JINA_READER_BASE`, optional `jina_api_key`) — the corpus relay/laundering primitive, live in the highest-starred MCP server in the lane. Also Telegram bot-send API hits.
4. **deep-research-mcp (u14app/deep-research, 4.7k★) — relay/HIGH.** Research crawler calls `fetch("https://r.jina.ai", {...})` (`src/utils/crawler.ts:22`) — same relay grammar.
5. **xhs-downloader (JoeanAmier/XHS-Downloader, 12.5k★) — creds/MEDIUM + HIGH-adjacent.** Mass Xiaohongshu media downloader with `verify=False` on its HTTP layer (`source/application/request.py:84`, `source/module/manager.py:102,109`) — TLS verification disabled in a bulk exfil-shaped tool.

Honorable mentions: `waha` (WhatsApp HTTP API — webhook *receiver* config surface, HIGH); `invisible_playwright_mcp` (Playwright "undetected by anti-bots and captchas" — browser/HIGH, the anti-detection framing is the notable part); `hexstrike-ai` (pentest MCP, verify=False ×2); `devin.cursorrules` (rules files instructing browser-automation usage — prompt-layer egress); `awesome-cursorrules` (playwright/cloudflare rules carry browser-automation instructions — prompt-layer, not code).

## False-positive log (verified, do not re-report as hits)

- triggerdev `chisel` = Tabler icon name in `tablerIcons.ts`, not the tunnel tool.
- gpt-researcher `bore` = fontawesome CSS class; `nGrok` = eval-record JSONL content.
- klavis ngrok = go.mod/go.sum deps + _test.go.
- wigolo cloudflared = code comments only.
- composio `zz` = base64 blob in an SVG.
- google-workspace-mcp `verify=False` = test function kwarg.
- wigolo r.jina.ai = blocklist, not usage.

## Secrets

13 creds/HIGH hits, all in `klavis/mcp_servers` (github_official middleware test fixtures + slack `.env.example` placeholders). Full observed values retained in scan-b.json per evidence policy (display layers may render them as `<redacted>`; the file bytes are complete). None used, none transmitted. No other secret-shaped values in the lane.

## Coordination note for parent

Sibling lane activity observed in the shared raw/ dir: `scan-c.json` (2.5MB), `scan-c-report.md`, `scan-c-notes.md` were written by another worker (a `lane-e` process was seen launching a scan targeting `scan-c.json`). My outputs are `raw/scan-b.json` + `raw/scan-b-notes.md` only — no writes to scan-a/scan-c. If two workers are both producing scan-c, they will clobber each other; worth confirming lane assignments.
