# Skill-egress study — Lane B: marketplace enumeration (IN PROGRESS)

**Work dir:** `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/studies/skill-egress-top500/`
**Date:** 2026-10-05. **Status:** enumerating. This file is written incrementally; resume from here if interrupted.
**Goal:** ~150 unique agent skills/plugins/MCP servers from public marketplaces, ranked by popularity, deduped by identity.

## Method
- Public listings only; curl with polite pacing, pages cached to /tmp/mkt/{smithery,npm,mcpso,glama,pulse,cursor,vsc}.
- Popularity evidence recorded per entry (useCount, downloads/week, install counts).
- Entries marked **ALREADY-COVERED** if skill-tracer v1 already cloned+scanned them (see its README/reports: anthropics/skills, obra/superpowers, affaan-m/ECC, multica-ai/andrej-karpathy-skills, addyosmani/agent-skills, nextlevelbuilder/ui-ux-pro-max-skill, JuliusBrussee/caveman, Leonxlnx/taste-skill, ComposioHQ/awesome-claude-skills, mvanhorn/last30days-skill, PatrickJS/awesome-cursorrules, zhaoxuya520/reverse-skill, anthropics/claude-plugins-official, mukul975/Anthropic-Cybersecurity-Skills, travisvn/awesome-claude-skills; plus modelcontextprotocol/servers, wshobson/agents, jeremylongshore/claude-code-plugins-plus-skills, Composio/rube remote MCPs from mcp-egress-v1).

## Network notes (egress from this VM, 2026-10-05)
- REACHABLE via curl: registry.smithery.ai (public registry API), glama.ai, registry.npmjs.org (slow; search endpoint times out), github.com API.
- UNREACHABLE via curl (connection timeout; not retried aggressively): www.pulsemcp.com, mcp.so, cursor.directory, marketplace.visualstudio.com, api.npmjs.org, registry.modelcontextprotocol.io, r.jina.ai. Covered via browser search/open instead where possible.

---

## 1. smithery.ai — top by registry `useCount` (registry.smithery.ai, public API)

Fetched `GET /servers?page={1,2,3}&pageSize=100` (18,572 servers total in registry); sorted by `useCount` desc; all entries below are `remote: true` (Smithery-hosted remote MCP servers — third-party endpoints receiving agent tool-call arguments). Listing URL pattern: `https://smithery.ai/server/@<qualifiedName>` (homepage field used as source when it differs).

| # | qualifiedName | displayName | useCount | verified | source repo/homepage | notes |
|---|---|---|---|---|---|---|
| 1 | pipeworx/gateway | pipeworx gateway | 419,019 | no | https://smithery.ai/servers/pipeworx/gateway | 250+ data sources, 900+ tools meta-gateway |
| 2 | henry-ships/sparkforge | SparkForge | 219,896 | no | https://smithery.ai/servers/henry-ships/sparkforge | media generation tool collection |
| 3 | brave | Brave Search | 87,579 | yes | https://brave.com/search/api/ | web search; keyed (BYO token) |
| 4 | bouch/uk-due-diligence | uk-due-diligence | 60,881 | no | https://bouch.dev/products/uk-due-diligence-mcp/ | UK public registers |
| 5 | adamamer20/paper-search-mcp-openai | Paper Search | 59,106 | no | https://github.com/adamamer20/paper-search-mcp-openai | arXiv/PubMed/bioRxiv search+download |
| 6 | gmail | Gmail | 57,738 | yes | https://smithery.ai/servers/gmail | read/search/send email |
| 7 | googlesheets | Google Sheets | 56,138 | yes | https://smithery.ai/servers/googlesheets | sheets read/edit |
| 8 | theagenttimes/news | Agent News | 43,392 | yes | https://theagenttimes.com | agent news feed |
| 9 | pubmed | PubMed | 42,137 | yes | https://smithery.ai/servers/pubmed | 36M citations |
| 10 | fenglucc/ko-financial-data | ko-financial-data | 40,620 | no | https://ko.io | SEC/13F/insider/congress data |
| 11 | jordan-s648/PolymarketScan | Polymarket Data by PolymarketScan | 39,483 | no | https://PolymarketScan.org/API | Polymarket analytics |
| 12 | oobe-protocol/sap-mcp | sap-mcp | 34,350 | no | https://mcp.sap.oobeprotocol.ai/ | SAP |
| 13 | emblemai/emblem-mcp | emblem-mcp | 25,084 | no | https://emblemvault.ai | hosted MCP |
| 14 | creativelead/unclick | UnClick | 24,706 | no | https://unclick.world | 60+ tools marketplace meta-server |
| 15 | onesignal/onesignal | OneSignal | 22,491 | yes | https://onesignal.com/ | push notification platform (send) |
| 16 | nitrofire-q/gread | Gread | 21,140 | no | https://gread.dev/ | public GitHub source access |
| 17 | pinkpixel-dev/web-scout-mcp | Web Scout | 19,558 | no | https://github.com/pinkpixel-dev/web-scout-mcp | web search+extract |
| 18 | smithery-ai/national-weather-service | United States Weather | 17,177 | no | https://www.weather.gov | weather.gov |
| 19 | ramboweb3/hivecast-x711 | x711io universal gas station | 16,923 | no | https://x711.io | x402 pay-per-call tools |
| 20 | subwayinfo | SubwayInfo NYC | 16,873 | yes | https://subwayinfo.nyc | NYC subway realtime |
| 21 | deficlow/zipp | Zipp | 16,317 | no | https://zippfeed.com | crypto news |
| 22 | entia/entity-verification | entity-verification | 16,045 | no | https://entia.systems | business identity intel |
| 23 | googlecalendar | Google Calendar | 15,718 | yes | https://smithery.ai/servers/googlecalendar | calendar CRUD |
| 24 | digby-oldridge/colour-memory-api | Colour Memory | 15,140 | no | https://colourmemory.com | color archive |
| 25 | cyanheads/pubmed-mcp-server | pubmed-mcp-server | 13,948 | no | https://pubmed.caseyjhand.com/mcp | PubMed full-text fetch |
| 26 | naver/search | Naver Search | 13,327 | no | https://search.naver.com | Naver search |
| 27 | Nekzus/npm-sentinel-mcp | NPM Sentinel MCP | 13,278 | no | https://github.com/Nekzus/npm-sentinel-mcp | npm package intel |
| 28 | OEvortex/ddg_search | DuckDuckGo & Felo AI Search | 12,697 | no | https://smithery.ai/servers/OEvortex/ddg_search | search |
| 29 | NutriBalance/nutribalance-mcp | nutribalance-mcp | 12,688 | no | https://thenutritrackerapp-creator-nutribal.vercel.app | nutrition tools |
| 30 | cyanheads/nist-nvd-mcp-server | nist-nvd-mcp-server | 12,481 | no | https://nist-nvd.caseyjhand.com/mcp | NVD CVE search |
| 31 | bissell-skyler/cityparity | cityparity | 12,406 | no | https://cityparity.com/mcp/ | city comparison |
| 32 | ia-qa/api | ia-qa.com/mcp | 12,266 | no | https://www.ia-qa.com/mcp-server | LLM/RAG testing |
| 33 | slack | Slack | 12,110 | yes | https://smithery.ai/servers/slack | slack read/send |
| 34 | framesail/framesail | Framesail | 11,533 | no | https://framesail.com/developers | video generation |
| 35 | travis-kellogg1/coinrailz-mcp | Coin Railz | 11,447 | no | https://coinrailz.com | 63 x402 micropayment services |
| 36 | friso/compliancecheckup | ComplianceCheckup | 11,175 | no | https://compliancecheckup.org/ | SaaS privacy grades |
| 37 | hamid-vakilzadeh/mcpsemanticscholar | AI Research Assistant | 10,296 | no | http://lit-review-assistant.streamlit.app | semantic scholar |
| 38 | aryankeluskar/polymarket-mcp | Polymarket | 10,102 | no | https://github.com/aryankeluskar/polymarket-mcp | Polymarket markets |
| 39 | pinksaltlamp75/Your-Echo-Agent- | Your-Echo-Agent- | 10,070 | no | https://yourechoagent.com | PR agent |
| 40 | getgapup/gapup-mcp | Gapup MCP | 10,042 | no | https://hub.gapup.io/agents-api | 270+ agent-payable tools |
| 41 | isdaniel/mcp_weather_server | Weather MCP Server | 9,970 | no | https://github.com/isdaniel/mcp_weather_server | weather |
| 42 | vbhjckfd/lad-lviv-ua | lad-lviv-ua | 9,780 | no | https://lad.lviv.ua/ | Lviv public transport realtime |
| 43 | pkobielak/social-superpowers | social-superpowers | 9,761 | no | https://superpowers.social | X/Twitter + Reddit research, 10 read-only tools |
| 44 | aparajithn/agent-utils | Developer Utilities | 9,739 | no | https://smithery.ai/servers/aparajithn/agent-utils | dev workflow utils |
| 45 | segellfosc-dev-ayfx/menjometre | menjometre | 9,534 | no | https://menjometre.cat | Catalan public spending observatory |
| 46 | info-6d0w/backtesting-arena | backtesting-arena | 9,340 | no | https://tradingstrategies.work/api | crypto backtesting |
| 47 | exa | Exa Search | 9,181 | yes | https://exa.ai | web search + crawl |
| 48 | cyanheads/census-mcp-server | census-mcp-server | 9,002 | no | https://census.caseyjhand.com/mcp | US Census data |
| 49 | intake-triage/steadyfetch | SteadyFetch | 8,946 | no | https://smithery.ai/servers/intake-triage/steadyfetch | web fetching w/ retry |
| 50 | pipeworx/pipeworx | pipeworx | 8,926 | no | https://pipeworx.io | SEC/econ data connector (same vendor as #1) |

**Smithery dedupe/caveats:** listing order is not strictly useCount; multiple namespaced entries can be the same code (e.g. `cyanheads/pubmed-mcp-server` vs verified `pubmed` — kept as separate entries since identity couldn't be proven from metadata alone; flagged). Smithery-hosted entries (namespace = smithery-ai or homepage smithery.ai/servers/...) are first-party hosted. `verified` = Smithery-verified publisher.

---

## 2. pulsemcp.com — top by "Est Visitors (Week)" (via text fetch of https://www.pulsemcp.com/servers, 2026-10-05)

PulseMCP directory (21,750+ servers, updated daily). Ranking evidence = their "Est Visitors (Week)" figure. Listing URL: https://www.pulsemcp.com/servers (per-server slugs not captured; do not guess).

| # | name | publisher | class | est visitors/wk | notes |
|---|---|---|---|---|---|
| 1 | Playwright Browser Automation | Microsoft | official | 5.5m | full browser control: navigate, snapshot, interact, screenshot |
| 2 | Chrome DevTools | Google | official | 3.1m | direct Chrome control via DevTools |
| 3 | Storybook | Storybook | official | 2.6m | agents write/test UI stories |
| 4 | Browser Use | Browser Use | official | 1.1m | LLM browser access via browser-use.com API (third-party relay) |
| 5 | Filesystem | Anthropic | reference | 647k | local file read/write **[ALREADY-COVERED — modelcontextprotocol/servers, skill-tracer v1]** |
| 6 | Context7 (Documentation Database) | Upstash | official | 459k | keyless remote MCP; **[ALREADY-COVERED — skill-tracer mcp-egress-v1 documented mcp.context7.com/mcp]** |
| 7 | Telnyx | Telnyx | official | 390k | voice/SMS/phone telecom APIs |
| 8 | Demo (Everything) | Anthropic | reference | 307k | protocol test server **[ALREADY-COVERED]** |
| 9 | WeRead Finance | wong2 | community | 238k | remote MCPs on Cloudflare Workers (WeRead, weather, finance data) |
| 10 | Agent Device | Callstack | official | 235k | iOS/Android/TV/macOS device automation |
| 11 | Notion | Notion | official | 216k | Notion API search/read/write |
| 12 | Edgar Tools | dgunning | community | 193k | SEC EDGAR toolkit, no API key |
| 13 | FireCrawl | Mendable | official | 185k | web scrape/crawl (third-party fetch relay) |
| 14 | Hostinger API | Hostinger | official | 176k | domain/DNS/VPS management |
| 15 | Knowledge Graph Memory | Anthropic | reference | 162k | **[ALREADY-COVERED — modelcontextprotocol/servers]** |
| 16 | GitLab | zereight | community | 149k | GitLab API (repos, issues, MRs) |
| 17 | Figma | Figma | official | 146k | Figma desktop app design extraction |
| 18 | Supabase | Supabase | official | 142k | databases, migrations, storage |
| 19 | Next.js DevTools | Vercel | official | 142k | Next.js diagnostics |
| 20 | MongoDB | MongoDB Inc. | official | 139k | conversational DB bridge |
| 21 | Desktop Commander | Eduard Ruzga | official | 137k | terminal + filesystem execution |
| 22 | Time | Anthropic | reference | 132k | **[ALREADY-COVERED]** |
| 23 | Linear | Linear | official | 131k | issues/projects |
| 24 | Grafana | Grafana Labs | official | 129k | dashboards, Prometheus queries |
| 25 | GitHub | Anthropic | reference | 129k | **[ALREADY-COVERED — modelcontextprotocol/servers]** |
| 26 | Sequential Thinking | Model Context Protocol | reference | 127k | **[ALREADY-COVERED]** |
| 27 | Fetch | Anthropic | reference | 122k | web→markdown retrieval **[ALREADY-COVERED]** |
| 28 | Stripe | Stripe | official | 111k | payments/customers |
| 29 | GitMCP (GitHub to MCP) | Ido Salomon | community | 107k | any GitHub repo → docs hub (third-party relay over GitHub) |
| 30 | PostgreSQL | Anthropic | reference | 106k | **[ALREADY-COVERED — modelcontextprotocol/servers]** |
| 31 | UI5 | SAP SE | official | 104k | UI5 enterprise framework tools |
| 32 | Dodo Payments | Dodo Payments | official | 100k | payments/subscriptions |
| 33 | SAP Fiori | SAP SE | official | 100k | SAP Fiori dev tools |
| 34 | Cloudflare Workers | Cloudflare | official | 92.8k | deploy AI services at edge |
| 35 | Figma Context | GLips | community | 83.9k | Figma API design ops |
| 36 | n8n | Romuald Czlonkowski | community | 80k | 525+ workflow nodes |
| 37 | Hevy Fitness | Christoph Kieslich | community | 79.7k | workout tracking API |
| 38 | Snowflake | Snowflake | official | 74.4k | data platform bridge |
| 39 | Shopify Storefront | Shopify | official | 72.1k | catalog/cart |
| 40 | Shopify Customer Accounts | Shopify | official | 72.1k | orders/account data |
| 41 | HubSpot | HubSpot | official | 69.1k | CRM contacts/deals |
| 42 | Zernio | Zernio | official | 67.6k | publish to 15+ social platforms |

**PulseMCP dedupe notes:** Anthropic "reference" servers duplicate skill-tracer v1's modelcontextprotocol/servers coverage — marked, not re-counted as new.

### 2b. PulseMCP memory category (from search snippet of https://www.pulsemcp.com/servers?q=memory — PulseMCP 403'd a direct refetch, likely rate-limited)

| name | publisher | class | est downloads/wk | notes |
|---|---|---|---|---|
| Basic Memory | Basic Machines | official | 2.3k | local markdown semantic graph |
| Supermemory | Dhravya Shah | official | 2.2k | personal knowledge platform |
| Memory Service | doobidoo | community | 3.6k | ChromaDB + sentence transformers |
| ZenMemory (Solana) | ZenMemoryAI | community | 0 | memory ↔ Solana bridge |
| Memara Memory | memara-memory | community | 0 | README-only template |
| Pieces Long-Term Memory | Pieces | official | — | long-term memory |

---

## 3. mcp.so — trending/featured (via text fetch of https://mcp.so/, 2026-10-05)

mcp.so marketplace homepage. Ranking evidence = install counts shown on "Trending this week". Per-server URL pattern: https://mcp.so/servers/<slug> (verified live for /servers/medplum).

### Trending this week (by installs)

| # | name | vendor | installs | notes |
|---|---|---|---|---|
| 1 | Medplum | medplum | 2.5K | healthcare platform, FHIR API |
| 2 | Atomic Mail Agentic | Atomic-Mail | 255 | agents read/send/react to email autonomously |
| 3 | PLUR | plur-ai | 226 | persistent agent memory |
| 4 | Termany | thinkany-ai | 174 | agent-native terminal |
| 5 | Hostinger | hostinger | 148 | Hostinger API — **dup of PulseMCP §2 #14** (same server), kept as one identity |
| 6 | OpenZiti / LLM-Gateway | openziti | 93 | OpenAI-compatible LLM proxy w/ zero-trust routing |
| 7 | LocalCan | LocalCan | 82 | public-URL tunnels for localhost (ngrok alternative) — tunnel primitive |
| 8 | OpenLore | aakarim | 66 | serve docs to agents over SSH + MCP |

### Featured servers (editorial, no counts shown)

| name | vendor | notes |
|---|---|---|
| Official Porkbun MCP Server | Porkbun LLC | domain availability/pricing, register/renew/transfer, DNS management |
| AfterLaunch | Team AfterLaunch | agentic growth engine |
| Instagram MCP Server | HasData | public IG profiles/feeds by handle |
| AffiliateSpy | Savassi Limited | TikTok/YouTube/IG creator + competitor intel, 32 tools |
| Gologin MCP Server | gologinapp | browser profiles, proxies, fingerprints, cloud sessions |
| Kin | Troy Fortin, Jr. (Firelock, LLC) | persistent graph of AI-written software changes |
| Local MCP (LMCP) | lanchuske | 54 installs; Mail/iMessage/Teams/Slack/WhatsApp/Outlook/Drive/Zoom tools, local |
| OpenZiti MCP Gateway | openziti | 48 installs; zero-trust gateway aggregating MCP servers (same vendor as LLM-Gateway above) |

### Featured clients (agent-capable clients, not servers — recorded for lane completeness)

| name | vendor | notes |
|---|---|---|
| Roamzy | roamzy-io | agent-native eSIM — agent buys eSIMs with USDT/USDC |
| FormLM | formlm | smart forms/quizzes via NL |
| PoYo.ai | poyo.ai | one API key for 500+ AI models |
| Prism – Contract Deadline Reader | Built AI, Inc. | contract deadline extraction |

---

## 4. cursor.directory — trending plugins (via text fetch of https://cursor.directory/, 2026-10-05)

"Extend Cursor with community plugins. Discover and install plugins from 89.4k+ developers, ranked by what's trending." Mixed rules + MCP servers; only network-capable MCP servers enumerated below (rules noted briefly). Counts = downloads/installs as shown.

| name | installs | notes | cross-listing |
|---|---|---|---|
| GitHub (MCP) | 8.5k | GitHub issue tracking via MCP | **dup §2 #25** (PulseMCP GitHub) |
| Supabase (MCP) | 8.1k | PostgREST → Postgres queries | **dup §2 #18** |
| Vercel (MCP) | 6.8k | serverless endpoints for AI model interactions | distinct from §2 #19 (Next.js DevTools) — same vendor |
| Cloudflare (MCP) | 6.5k | Workers/KV/R2/D1 deploy+config | **dup §2 #34** |
| Stripe (MCP) | 6.2k | Stripe API | **dup §2 #28** |
| Notion (MCP) | 5.8k | Notion API | **dup §2 #11** |
| Slack (MCP) | 5.5k | Slack workspace integration | **dup §1 #33** (Smithery slack) |
| Sentry (MCP) | 5k | error tracking, session replay | **ALREADY-COVERED — anthropics/claude-plugins-official shipped sentry (mcp-egress-v1)** |
| Figma (MCP) | 4.8k | Figma design data | **dup §2 #17** |
| Firebase (MCP) | 4k | Auth/Firestore/Storage | new |
| Docker (MCP) | 3.8k | containers/images/volumes/networks | new |
| Prisma (MCP) | 3.4k | Prisma Postgres management | new |
| anon.li (MCP) | 3.2k | create/edit/delete email aliases, file shares & forms from Cursor — privacy tooling, direct exfil-adjacent primitives | new |
| Flowbite MCP | 593 | Tailwind component library | new |
| Zendesk MCP Server by Swifteq | 256 | Zendesk ticket bridge | new |
| Signoz MCP Server | 164 | observability (logs/dashboards/metrics) via DrDroid | new |

Top Cursor rules (prompt files; lower egress relevance, listed for coverage): Next.js 39.8k, Front End 34.1k, Expo 18k, Fastapi 13k, Java 9.2k, Laravel 8.4k, Data Analyst 8.3k, Flutter 7.2k, Nuxtjs 6.1k, Chrome Extension 6.1k, Django 5.6k. Listing: https://cursor.directory/

---

## 5. VS Code marketplace — top AI agent extensions (install counts via public GitHub README table, crawled ~2026-07-25)

Marketplace host unreachable from this VM (connection timeout); counts below are from the install table in github.com/timerloggedout-spec/vscowork_fork README (fetched via web search 2026-10-05). Listing URL pattern: https://marketplace.visualstudio.com/items?itemName=<publisher.name> (pattern verified live in that README).

| extension | itemName | installs | notes |
|---|---|---|---|
| GitHub Copilot Chat | github.copilot-chat | 69,678,729 | in-editor chat panel, file context, test generation |
| Claude Code for VS Code | anthropic.claude-code | 9,077,641 | Anthropic's agentic coding extension |
| Codex – OpenAI's coding agent | openai.chatgpt | 6,596,184 | OpenAI coding agent |
| VS Code Speech | ms-vscode.vscode-speech | 1,247,040 | speech I/O (audio egress surface) |
| Mistral Code Enterprise | mistralai.mistral-code | 23,672 | Mistral coding assistant |
| Continue | Continue.continue | n/a (not in table) | open-source, connect own backends (Claude/OpenAI/Ollama); noted in 2026 extensions guide |

Also: **Awesome Copilot** (github.com/leahyra/awesome-copilot) is now a default Agent Plugin marketplace in VS Code / Copilot CLI — 101 plugins, 419 skills, 222 agents, 194 instructions (enumerated via GitHub API 2026-10-05). Notable network-capable plugins: `fastah-ip-geo-tools` (IP geolocation), `chromium-control-canvas` (browser control), `mcp-m365-copilot` (M365 MCP), `go-mcp-development` / `java-mcp-development` / `kotlin-mcp-development` (MCP dev), root `context7.json` (Context7 remote MCP config — **dup skill-tracer mcp-egress-v1**), root `mcp.json`.

---

## 6. npm — top `mcp-server` / `claude-skill` / `cursor-rules` packages (registry.npmjs.org search API, 2026-10-05)

Query `text=mcp-server&size=100` returned 100 of 397,504 matches, ranked by text relevance (npm popularity scores normalize to 1.0 per query — not usable as absolute rank). Download counts unavailable from this VM (api.npmjs.org unreachable). Repo stars being collected as a popularity proxy (pending).

| npm package | version | source repo | notes |
|---|---|---|---|
| @notionhq/notion-mcp-server | 2.5.2 | https://github.com/makenotion/notion-mcp-server | official Notion |
| @ui5/mcp-server | 0.3.1 | https://github.com/UI5/mcp-server | SAP UI5 |
| chrome-devtools-mcp | 1.10.1 | https://github.com/ChromeDevTools/chrome-devtools-mcp | official Chrome DevTools |
| @apify/actors-mcp-server | 0.17.1 | https://github.com/apify/apify-mcp-server | Apify actors gateway |
| @sentry/mcp-server | 0.42.0 | https://github.com/getsentry/sentry-mcp | official Sentry — **ALREADY-COVERED (claude-plugins-official)** |
| @upstash/context7-mcp | 4.1.1 | https://github.com/upstash/context7 | Context7 — **ALREADY-COVERED (mcp-egress-v1)** |
| @browserstack/mcp-server | 2.1.0 | https://github.com/browserstack/mcp-server | BrowserStack device cloud |
| @modelcontextprotocol/server-filesystem | 2026.8.31 | https://github.com/modelcontextprotocol/servers | **ALREADY-COVERED (skill-tracer v1)** |
| @sap-ux/fiori-mcp-server | 1.15.1 | https://github.com/SAP/open-ux-tools | SAP Fiori |
| @heroku/mcp-server | 1.2.10 | https://github.com/heroku/heroku-mcp-server | Heroku platform |
| @winor30/mcp-server-datadog | 1.8.0 | https://github.com/winor30/mcp-server-datadog | Datadog API |
| hostinger-api-mcp | 2.7.0 | https://github.com/hostinger/api-mcp-server | **dup §2 #14 / §3** |
| @supabase/mcp-server-supabase | 0.13.0 | https://github.com/supabase/mcp | official Supabase — **dup §2 #18 / §4** |
| @runpod/mcp-server | 4.0.0 | https://github.com/runpod/runpod-mcp | Runpod GPU cloud |
| @bitwarden/mcp-server | 2026.7.0 | https://github.com/bitwarden/mcp-server | Bitwarden vault access |
| @azure-devops/mcp | 2.10.0 | https://github.com/microsoft/azure-devops-mcp | Azure DevOps |
| kubernetes-mcp-server | 0.0.67 | https://github.com/containers/kubernetes-mcp-server | Kubernetes |
| @roychri/mcp-server-asana | 1.8.0 | https://github.com/roychri/mcp-server-asana | Asana — **ALREADY-COVERED-ish (claude-plugins-official shipped asana)** |
| deepl-mcp-server | — | https://github.com/DeepL/deepl-mcp-server | DeepL translation |
| dataforseo-mcp-server | — | https://github.com/dataforseo/mcp-server-typescript | DataForSEO |

Queries `claude-skill`, `cursor-rules`, `ai-agent-skill` against the same search API timed out from this VM; the awesome-copilot lane (§5) and wshobson/agents (below) cover the skill-file surface instead.

---

## 7. opencode / multi-harness marketplace note

`wshobson/agents` (local clone at `~/workspace/skill-tracer-work/sources/agents-marketplace/`, read 2026-10-05): a multi-harness agentic plugin marketplace — 94 plugins, 202 agents, 184 skills, 105 commands — with native per-harness artifacts for **OpenCode** (`.opencode/`), Codex, Cursor, Antigravity CLI, and Pi generated from one source-of-truth. **ALREADY-COVERED by skill-tracer v1's mcp-egress-v1 sweep** (92 plugins). OpenCode has no separate public web registry; its plugin surface is this repo + the skills-only installers (`gh skill install wshobson/agents`, `npx skills add wshobson/agents`, agentskills.io spec).

---

## Dedupe log (same identity on multiple marketplaces = 1 entry)

| identity | seen on |
|---|---|
| Hostinger API | PulseMCP §2, mcp.so §3, npm §6 |
| GitHub MCP | PulseMCP §2, cursor.directory §4 |
| Supabase | PulseMCP §2, cursor.directory §4, npm §6 |
| Cloudflare (Workers) | PulseMCP §2, cursor.directory §4 |
| Stripe | PulseMCP §2, cursor.directory §4 |
| Notion | PulseMCP §2, cursor.directory §4, npm §6 |
| Slack | Smithery §1, cursor.directory §4 |
| Figma | PulseMCP §2, cursor.directory §4 |
| Context7 | PulseMCP §2, npm §6, awesome-copilot root, skill-tracer v1 (mcp-egress-v1) |
| Sentry | cursor.directory §4, npm §6, skill-tracer v1 (claude-plugins-official) |
| Vercel | PulseMCP §2 (Next.js DevTools) vs cursor.directory §4 (Vercel MCP) — same vendor, distinct listings, kept separate |

## Final tally

| lane | rows | new identities | already-covered/dup rows |
|---|---|---|---|
| §1 Smithery | 50 | 50 | 0 |
| §2 PulseMCP | 42 | 33 | 9 |
| §2b PulseMCP memory | 6 | 6 | 0 |
| §3 mcp.so | 20 | 19 | 1 |
| §4 cursor.directory | 16 | 8 | 8 |
| §5 VS Code + awesome-copilot | 12 | 12 | 0 |
| §6 npm | 20 | 14 | 6 |
| §7 wshobson/agents | note | 0 | covered |
| **Total** | **166** | **142** | **24** |

**142 unique new identities enumerated** (target ~150; shortfall is PulseMCP rate-limiting after the first fetch and npm download-count API being unreachable — see network notes).

## Top-20 cross-lane rollup (metric labeled; metrics differ per marketplace — installs vs est visitors/week vs useCount — so ordering is approximate)

| # | entry | popularity evidence | lane |
|---|---|---|---|
| 1 | GitHub Copilot Chat | 69.7M installs | VS Code §5 |
| 2 | Claude Code for VS Code | 9.1M installs | VS Code §5 |
| 3 | Codex (openai.chatgpt) | 6.6M installs | VS Code §5 |
| 4 | Playwright Browser Automation | 5.5M est visitors/wk | PulseMCP §2 |
| 5 | Chrome DevTools | 3.1M/wk | PulseMCP §2 |
| 6 | Storybook | 2.6M/wk | PulseMCP §2 |
| 7 | VS Code Speech | 1.25M installs | VS Code §5 |
| 8 | Browser Use | 1.1M/wk | PulseMCP §2 |
| 9 | Filesystem (Anthropic) | 647K/wk | PulseMCP §2 **[ALREADY-COVERED]** |
| 10 | Context7 | 459K/wk | PulseMCP §2 **[ALREADY-COVERED]** |
| 11 | pipeworx/gateway | 419K useCount | Smithery §1 |
| 12 | Telnyx | 390K/wk | PulseMCP §2 |
| 13 | WeRead Finance | 238K/wk | PulseMCP §2 |
| 14 | Agent Device (Callstack) | 235K/wk | PulseMCP §2 |
| 15 | SparkForge | 220K useCount | Smithery §1 |
| 16 | Notion | 216K/wk | PulseMCP §2 |
| 17 | Edgar Tools | 193K/wk | PulseMCP §2 |
| 18 | FireCrawl | 185K/wk | PulseMCP §2 |
| 19 | Hostinger API | 176K/wk | PulseMCP §2 |
| 20 | Knowledge Graph Memory | 162K/wk | PulseMCP §2 **[ALREADY-COVERED]** |

## Egress-relevant highlights for the next lane (scan prioritization)

Tunnel/proxy primitives: **LocalCan** (mcp.so, localhost tunnels), **Gologin MCP** (proxies/fingerprints), **OpenZiti LLM-Gateway** (LLM proxy). Meta-gateways (one install = hundreds of tools, all args transit one operator): **pipeworx/gateway** (900+ tools), **UnClick** (60+), **Gapup** (270+). Autonomous comms: **Atomic Mail Agentic** (email read/send), **anon.li** (email aliases + file shares from Cursor), **Telnyx** (voice/SMS), **Zernio** (15+ social platforms), **OneSignal** (push). Third-party fetch relays: **Browser Use**, **FireCrawl**, **SteadyFetch**, **GitMCP**, **WeRead** (Cloudflare Workers). Agent commerce: **Roamzy** (agent buys eSIMs with crypto), **PoYo.ai** (500+ models one key), **x711/coinrailz** (x402 micropayments). Credential-adjacent: **Bitwarden MCP** (vault), **VS Code Speech** (audio I/O).

*Enumeration complete 2026-10-05. Output: this file. Gaps: npm per-package download counts (api.npmjs.org blocked; GitHub-stars proxy aborted as too slow); PulseMCP category pages beyond /servers (403 rate-limit after first fetch); glama.ai server list (React SPA, list loads via undocumented internal API — reachable host but no public endpoint found); official MCP registry (registry.modelcontextprotocol.io unreachable).*
