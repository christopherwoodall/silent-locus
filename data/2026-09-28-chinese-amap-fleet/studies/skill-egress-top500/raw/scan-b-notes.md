# Skill-Egress Study — Lane D: fetch + scan (cursor rules + MCP servers batch)

Date: 2026-10-05. Operator: lane-d subagent. Method: skill-tracer (`scan/egress_scan.py` + `egress-taxonomy.md`).
Scanner run: `python3 ~/workspace/muse-home/projects/skill-tracer/scan/egress_scan.py ~/workspace/skill-egress-work/lane-d --out raw/scan-b.json`
Clones: shallow (`git clone --depth 1`), polite pacing (~2s between), public repos only, never committed (scratch only, `~/workspace/skill-egress-work/lane-d/`).
Grading per taxonomy: confirmed (bytes present) / pattern-match (corpus tradecraft grammar). Score = 3×critical + 2×high + 1×medium → CRITICAL ≥10, HIGH ≥6, MEDIUM ≥3, LOW ≥1, NONE 0.
A high score is NOT an accusation — dual-use network surface on legitimate tools. Corpus matches flagged separately.

## Fetch log (66 targets)

### A. Cursor rules (8)
| # | repo | stars | notes |
|---|------|-------|-------|
| 1 | PatrickJS/awesome-cursorrules | 40,878 | 150+ .mdc rules corpus; README has no external rules links (only claire-gong-18 mirror) |
| 2 | grapeot/devin.cursorrules | 5,965 | "turn Cursor/Windsurf into 90% of Devin" |
| 3 | kinopeee/cursorrules | 1,111 | |
| 4 | s-smits/agentic-cursorrules | 646 | multi-agent Cursor management |
| 5 | holtwood/awesome-cursorrules-zh | 236 | Chinese 132+ rules |
| 6 | nedcodes-ok/cursorrules-collection | 37 | 110+ .mdc/.cursorrules |
| 7 | BlueBirdBack/godot-cursorrules | 119 | Godot 4.4 |
| 8 | ali-abassi/OpenAI_Assistant_API_Boilerplate_CursorRules | 52 | OpenAI Assistant API + cursor rules |

### B. modelcontextprotocol/servers (1)
| # | repo | stars | notes |
|---|------|-------|-------|
| 9 | modelcontextprotocol/servers | 91,012 | reference servers; network-capable subdirs prioritized: fetch, github, gitlab, brave-search, slack, google-maps, perplexity-ask, everart, postgres, puppeteer; local-only deprioritized: filesystem, sqlite, memory, sequential-thinking, time |

### C. Top community MCP servers (46)
| # | repo | stars | why network-relevant |
|---|------|-------|----------------------|
| 10 | upstash/context7 | 62,688 | docs-fetch service |
| 11 | sansan0/TrendRadar | 62,676 | multi-platform news aggregation |
| 12 | ChromeDevTools/chrome-devtools-mcp | 52,904 | browser automation (HIGH per taxonomy) |
| 13 | microsoft/playwright-mcp | 37,827 | browser automation |
| 14 | github/github-mcp-server | 33,373 | GitHub API (git writes) |
| 15 | feder-cr/invisible_playwright_mcp | 31,776 | Playwright "undetected by anti-bots and captchas" |
| 16 | oraios/serena | 29,996 | coding toolkit |
| 17 | assafelovic/gpt-researcher | 29,920 | autonomous deep-research agent |
| 18 | ComposioHQ/composio | 30,441 | 1000+ toolkits platform |
| 19 | czlonkowski/n8n-mcp | 22,900 | build n8n workflows |
| 20 | Evil0ctal/Douyin_TikTok_Download_API | 20,469 | TikTok data scraping + MCP |
| 21 | wanshuiyin/Auto-claude-code-research-in-sleep | 16,468 | Markdown-only agent skills |
| 22 | xpzouying/xiaohongshu-mcp | 16,110 | xiaohongshu.com MCP |
| 23 | yusufkaraaslan/Skill_Seekers | 13,519 | docs/GitHub/PDF → Claude skills converter |
| 24 | JoeanAmier/XHS-Downloader | 12,474 | Xiaohongshu link extraction |
| 25 | OpenByteInc/QuantDinger | 12,453 | agent trading OS |
| 26 | tadata-org/fastapi_mcp | 12,317 | FastAPI → MCP |
| 27 | 0x4m4/hexstrike-ai | 12,017 | pentest MCP agents |
| 28 | 0xJacky/nginx-ui | 10,731 | nginx WebUI |
| 29 | mcp-use/mcp-use | 10,722 | fullstack MCP framework |
| 30 | awslabs/mcp | 9,646 | AWS MCP servers |
| 31 | apify/apify-mcp-server | 9,577 | web-scraping actors |
| 32 | openstatusHQ/openstatus | 9,168 | uptime monitoring as code |
| 33 | D4Vinci/Scrapling | 85,734 | adaptive web-scraping framework |
| 34 | firecrawl/firecrawl-mcp-server | 7,553 | web scraping + search |
| 35 | devlikeapro/waha | 7,546 | WhatsApp HTTP API |
| 36 | AgentDeskAI/browser-tools-mcp | 7,329 | browser logs → IDE |
| 37 | BrowserMCP/mcp | 7,159 | browser control |
(dropped from sweep: getsentry/MobileBuildMCP, MinishLab/semble — lower network signal, kept count in budget)
| 40 | Klavis-AI/klavis | 5,808 | MCP integration platform |
| 41 | KnockOutEZ/wigolo | 5,444 | local-first search/fetch/crawl |
| 42 | FunnyWolf/Viper | 5,232 | adversary simulation / red team |
| 43 | exa-labs/exa-mcp-server | 5,079 | web search + crawl |
| 44 | atilaahmettaner/tradingview-mcp | 4,914 | market data |
| 45 | u14app/deep-research | 4,694 | deep research |
| 46 | makenotion/notion-mcp-server | 4,660 | official Notion server |
| 47 | cloudflare/mcp-server-cloudflare | 4,352 | Cloudflare |
| 48 | browserbase/mcp-server-browserbase | 3,410 | browser via Browserbase + Stagehand |
| 49 | taylorwilsdon/google_workspace_mcp | 3,281 | Gmail/Calendar/Docs/Sheets/Drive |
| 50 | tavily-ai/tavily-mcp | 2,418 | search/extract/crawl |
| 51 | korotovsky/slack-mcp-server | 1,854 | Slack, "no permission requests" |
| 52 | Flux159/mcp-server-kubernetes | 1,595 | k8s management |
| 53 | suekou/mcp-notion-server | 918 | community Notion server |
| 54 | jerhadf/linear-mcp-server | 346 | Linear (stale since May 2025 per ranking) |
| 55 | zapier/zapier-mcp | 426 | official plugin dist for hosted Zapier MCP |

### D. Roo / Cline modes + rules (7)
| # | repo | notes |
|---|------|-------|
| 56 | getzenai/feature-roo-configs | Roo modes + rules (fork lineage of christianbaumann/feature) |
| 57 | christianbaumann/feature | "roo code rules, modes and best practices" |
| 58 | feature-foundation/feature | same lineage |
| 59 | xavier-arosemena/custom-modes-roo-code | 290-mode collection (fork of jtgsystems) |
| 60 | jtgsystems/Custom-Modes-Roo-Code | upstream 290-mode collection |
| 61 | cline/clinerules | official Cline rules/skills/workflows library |
| 62 | blitzingminty/clinerules | .clinerules sets/templates |
| 63 | henryalps/vscode-clinerules | VSCode plugin to configure Cline/Roo rules |

### E. aider conventions (4)
| # | repo | notes |
|---|------|-------|
| 64 | Aider-AI/conventions | official org collection |
| 65 | avicennasis/conventions | community fork |
| 66 | vloddos/conventions | community fork |
| 67 | delphoa/study-aider-conventions | community fork |

(Target #s 1–67 with awesome-cursorrules counted once = 67 clone dirs; getsentry/semble kept from ranking but are secondary.)

## Scan results

*Pending — scanner run after clone sweep completes.*

## Hunt-corpus toolkit matches

*Pending — r.jina.ai, webhook.site/discord/slack, httpbun/httpbin, uploads.github.com, ngrok, epoch nonces, zz labels, verify=False.*

## Top-5 riskiest

*Pending.*

## Secrets / anomalies

*None used. No secrets recorded. Public repos only.*
