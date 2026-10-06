# skill-tracer findings

144 skill units scanned; 84 with ≥1 egress hit.

Risk tiers: CRITICAL ≥10 · HIGH ≥6 · MEDIUM ≥3 · LOW ≥1 · NONE 0
(3 pts per CRITICAL hit, 2 per HIGH, 1 per MEDIUM).

## Summary

| skill | risk | score | why |
|---|---|---|---|
| [medplum_medplum/medplum_medplum](https://github.com/medplum/medplum) | **CRITICAL** | 1002 | GitHub user-attachments image host; tunnel tools; browser automation libs; SMTP/sendmail usage [746 egress primitives across 9 categories: browser, dns, email, gitwrite, img_upload, netcall, relay, tunnel, webhook] |
| [executeautomation__mcp-playwright/executeautomation__mcp-playwright](https://github.com/executeautomation/mcp-playwright) | **CRITICAL** | 825 | browser automation libs; multipart file upload call; browser navigation calls; shell HTTP client [425 egress primitives across 3 categories: browser, img_upload, netcall] |
| [cloudflare__mcp-server-cloudflare/cloudflare__mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare) | **CRITICAL** | 716 | GitHub user-attachments image host; browser automation libs; SMTP/sendmail usage; multipart file upload call [483 egress primitives across 5 categories: browser, email, img_upload, netcall, registry] |
| [getsentry__sentry-mcp/getsentry__sentry-mcp](https://github.com/getsentry/sentry-mcp) | **CRITICAL** | 631 | browser automation libs; hardcoded secret-shaped token; SMTP/sendmail usage; multipart file upload call [595 egress primitives across 8 categories: browser, creds, dns, email, gitwrite, img_upload, netcall, webhook] |
| [microsoft__playwright-mcp/microsoft__playwright-mcp](https://github.com/microsoft/playwright-mcp) | **CRITICAL** | 507 | browser automation libs; browser navigation calls; git push from skill; gh CLI create (issue/PR/release/gist) [263 egress primitives across 3 categories: browser, gitwrite, netcall] |
| [team-telnyx_telnyx-mcp-server](https://github.com/team-telnyx/telnyx-mcp-server) | **CRITICAL** | 446 | GitHub user-attachments image host; tunnel tools; shell HTTP client [150 egress primitives across 3 categories: img_upload, netcall, tunnel] |
| [bhromecevsools_chrome-devtools-mcp/bhromecevsools_chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | **CRITICAL** | 377 | browser automation libs; multipart file upload call; browser navigation calls; shell HTTP client [217 egress primitives across 3 categories: browser, img_upload, netcall] |
| [browser-use_browser-use/skills/cloud](https://github.com/browser-use/browser-use) | **CRITICAL** | 326 | browser automation libs; browser navigation calls; shell HTTP client [177 egress primitives across 2 categories: browser, netcall] |
| [mongodb-js_mongodb-mcp-server/mongodb-js_mongodb-mcp-server](https://github.com/mongodb-js/mongodb-mcp-server) | **CRITICAL** | 259 | tunnel tools; browser automation libs; multipart file upload call; curl multipart upload [169 egress primitives across 8 categories: browser, creds, dns, gitwrite, img_upload, netcall, relay, tunnel] |
| [neondatabase__mcp-server-neon/neondatabase__mcp-server-neon](https://github.com/neondatabase/mcp-server-neon) | **CRITICAL** | 164 | browser automation libs; SMTP/sendmail usage; multipart file upload call; browser navigation calls [98 egress primitives across 5 categories: browser, email, gitwrite, img_upload, netcall] |
| [_tomic-lail_atomic-mail-agentic/_tomic-lail_atomic-mail-agentic](https://github.com/Atomic-Mail/atomic-mail-agentic) | **CRITICAL** | 162 | browser automation libs; SMTP/sendmail usage; multipart file upload call; git push from skill [118 egress primitives across 5 categories: browser, email, gitwrite, img_upload, netcall] |
| [hamid-vakilzadeh__mcpsemanticscholar/hamid-vakilzadeh__mcpsemanticscholar](https://github.com/hamid-vakilzadeh/mcpsemanticscholar) | **CRITICAL** | 131 | tunnel tools; multipart file upload call; HTTP client call [46 egress primitives across 3 categories: img_upload, netcall, tunnel] |
| [browser-use_browser-use/skills/open-source](https://github.com/browser-use/browser-use) | **CRITICAL** | 129 | browser automation libs; browser navigation calls; shell HTTP client [66 egress primitives across 2 categories: browser, netcall] |
| [browser-use_browser-use/skills/qa](https://github.com/browser-use/browser-use) | **CRITICAL** | 108 | tunnel tools; browser automation libs; shell HTTP client; HTTP client call [50 egress primitives across 3 categories: browser, netcall, tunnel] |
| [apify__actors-mcp-server/apify__actors-mcp-server](https://github.com/apify/actors-mcp-server) | **CRITICAL** | 65 | tunnel tools; browser automation libs; multipart file upload call; DNS lookup tools (exfil shape) [44 egress primitives across 7 categories: browser, dns, gitwrite, img_upload, netcall, relay, tunnel] |
| [browser-use_browser-use/browser_use/skills/browser-use](https://github.com/browser-use/browser-use) | **CRITICAL** | 57 | browser automation libs; shell HTTP client [29 egress primitives across 2 categories: browser, netcall] |
| [browser-use_browser-use/skills/browser-use](https://github.com/browser-use/browser-use) | **CRITICAL** | 57 | browser automation libs; shell HTTP client [29 egress primitives across 2 categories: browser, netcall] |
| [makenotion__notion-mcp-server/makenotion__notion-mcp-server](https://github.com/makenotion/notion-mcp-server) | **CRITICAL** | 57 | GitHub user-attachments image host; browser automation libs; multipart file upload call; git push from skill [30 egress primitives across 4 categories: browser, gitwrite, img_upload, netcall] |
| [mendableai__firecrawl-mcp-server/mendableai__firecrawl-mcp-server](https://github.com/mendableai/firecrawl-mcp-server) | **CRITICAL** | 53 | multipart file upload call; shell HTTP client; HTTP client call [51 egress primitives across 2 categories: img_upload, netcall] |
| [supabase-community__supabase-mcp/supabase-community__supabase-mcp](https://github.com/supabase-community/supabase-mcp) | **CRITICAL** | 48 | GitHub user-attachments image host; SMTP/sendmail usage; multipart file upload call; HTTP client call [30 egress primitives across 3 categories: email, img_upload, netcall] |
| [agentmail-to__agentmail-mcp/agentmail-to__agentmail-mcp](https://github.com/agentmail-to/agentmail-mcp) | **CRITICAL** | 38 | multipart file upload call; shell HTTP client; HTTP client call [37 egress primitives across 2 categories: img_upload, netcall] |
| [runpod_runpod-mcp/runpod_runpod-mcp](https://github.com/runpod/runpod-mcp) | **CRITICAL** | 33 | multipart file upload call; DNS lookup tools (exfil shape); git push from skill; HTTP client call [31 egress primitives across 4 categories: dns, gitwrite, img_upload, netcall] |
| [mzxrai__mcp-webresearch/mzxrai__mcp-webresearch](https://github.com/mzxrai/mcp-webresearch) | **CRITICAL** | 30 | browser automation libs; multipart file upload call; browser navigation calls; npm postinstall hook [16 egress primitives across 3 categories: browser, img_upload, registry] |
| [browser-use_browser-use/skills/x402](https://github.com/browser-use/browser-use) | **CRITICAL** | 29 | browser automation libs; shell HTTP client [15 egress primitives across 2 categories: browser, netcall] |
| [containers_kubernetes-mcp-server/test/browser](https://github.com/containers/kubernetes-mcp-server) | **CRITICAL** | 26 | browser automation libs; browser navigation calls; shell HTTP client [16 egress primitives across 2 categories: browser, netcall] |
| [docfork__docfork/docfork__docfork](https://github.com/docfork/docfork) | **CRITICAL** | 26 | browser automation libs; multipart file upload call; shell HTTP client; HTTP client call [19 egress primitives across 3 categories: browser, img_upload, netcall] |
| [modelcontextprotocol__servers/modelcontextprotocol__servers](https://github.com/modelcontextprotocol/servers) | **CRITICAL** | 26 | browser automation libs; multipart file upload call; git push from skill; gh CLI create (issue/PR/release/gist) [17 egress primitives across 4 categories: browser, gitwrite, img_upload, netcall] |
| [heroku_heroku-mcp-server/heroku_heroku-mcp-server](https://github.com/heroku/heroku-mcp-server) | **CRITICAL** | 24 | multipart file upload call; git push from skill; HTTP client call; shell HTTP client [23 egress primitives across 3 categories: gitwrite, img_upload, netcall] |
| [stripe__agent-toolkit/benchmarks/furever/environment](https://github.com/stripe/agent-toolkit) | **CRITICAL** | 24 | browser automation libs; HTTP client call [22 egress primitives across 2 categories: browser, netcall] |
| [adamamer20__paper-search-mcp-openai](https://github.com/adamamer20/paper-search-mcp-openai) | **CRITICAL** | 19 | TLS verification disabled; shell HTTP client; HTTP client call [19 egress primitives across 2 categories: creds, netcall] |
| [browser-use_browser-use/skills/remote-browser](https://github.com/browser-use/browser-use) | **CRITICAL** | 18 | browser automation libs [9 egress primitives across 1 category: browser] |
| [veirdarains_onesignal-mcp](https://github.com/WeirdBrains/onesignal-mcp) | **CRITICAL** | 17 | HTTP client call [17 egress primitives across 1 category: netcall] |
| [burtthecoder__mcp-shodan/burtthecoder__mcp-shodan](https://github.com/burtthecoder/mcp-shodan) | **CRITICAL** | 11 | multipart file upload call; git push from skill; shell HTTP client; HTTP client call [10 egress primitives across 3 categories: gitwrite, img_upload, netcall] |
| [bitwarden_mcp-server/bitwarden_mcp-server](https://github.com/bitwarden/mcp-server) | **HIGH** | 9 | multipart file upload call; HTTP client call; shell HTTP client [8 egress primitives across 2 categories: img_upload, netcall] |
| [stripe__agent-toolkit/providers/agent-plugins/plugin/skills/connect-required-verification-information](https://github.com/stripe/agent-toolkit) | **HIGH** | 9 | shell HTTP client [9 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/providers/claude/plugin/skills/connect-required-verification-information](https://github.com/stripe/agent-toolkit) | **HIGH** | 9 | shell HTTP client [9 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/providers/codex/plugin/skills/connect-required-verification-information](https://github.com/stripe/agent-toolkit) | **HIGH** | 9 | shell HTTP client [9 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/providers/cursor/plugin/skills/connect-required-verification-information](https://github.com/stripe/agent-toolkit) | **HIGH** | 9 | shell HTTP client [9 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/providers/grok/plugin/skills/connect-required-verification-information](https://github.com/stripe/agent-toolkit) | **HIGH** | 9 | shell HTTP client [9 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/skills/connect-required-verification-information](https://github.com/stripe/agent-toolkit) | **HIGH** | 9 | shell HTTP client [9 egress primitives across 1 category: netcall] |
| [exa-labs__exa-mcp-server/exa-labs__exa-mcp-server](https://github.com/exa-labs/exa-mcp-server) | **HIGH** | 8 | browser automation libs; multipart file upload call; shell HTTP client [5 egress primitives across 3 categories: browser, img_upload, netcall] |
| [LinkupPlatform__linkup-mcp-server/LinkupPlatform__linkup-mcp-server](https://github.com/LinkupPlatform/linkup-mcp-server) | **HIGH** | 7 | multipart file upload call; shell HTTP client; HTTP client call [5 egress primitives across 2 categories: img_upload, netcall] |
| [brave__brave-search-mcp-server/brave__brave-search-mcp-server](https://github.com/brave/brave-search-mcp-server) | **HIGH** | 7 | multipart file upload call; git push from skill; shell HTTP client; HTTP client call [6 egress primitives across 3 categories: gitwrite, img_upload, netcall] |
| [gologinapp_gologin-mcp/gologinapp_gologin-mcp](https://github.com/gologinapp/gologin-mcp) | **HIGH** | 7 | multipart file upload call; shell HTTP client; HTTP client call [6 egress primitives across 2 categories: img_upload, netcall] |
| [sjh110007__mcp-jina-ai/sjh110007__mcp-jina-ai](https://github.com/sjh110007/mcp-jina-ai) | **HIGH** | 7 | multipart file upload call; fetch-relay/laundering domains; HTTP client call [5 egress primitives across 3 categories: img_upload, netcall, relay] |
| [clay-inc__clay-mcp](https://github.com/clay-inc/clay-mcp) | **HIGH** | 6 | GitHub user-attachments image host [2 egress primitives across 1 category: img_upload] |
| [grafana_mcp-grafana/ui/mcp-apps](https://github.com/grafana/mcp-grafana) | **HIGH** | 6 | browser automation libs; multipart file upload call [3 egress primitives across 2 categories: browser, img_upload] |
| [localcan_localcanapp](https://github.com/localcan/localcanapp) | **HIGH** | 6 | tunnel tools; shell HTTP client [4 egress primitives across 2 categories: netcall, tunnel] |
| [AudienseCo__mcp-audiense-insights/AudienseCo__mcp-audiense-insights](https://github.com/AudienseCo/mcp-audiense-insights) | **MEDIUM** | 5 | multipart file upload call; HTTP client call [4 egress primitives across 2 categories: img_upload, netcall] |
| [blockscout__mcp-server/.agents/skills/gh-safe](https://github.com/blockscout/mcp-server) | **MEDIUM** | 5 | gh CLI create (issue/PR/release/gist) [5 egress primitives across 1 category: gitwrite] |
| [blockscout__mcp-server/.agents/skills/sepolia-foundry-tx](https://github.com/blockscout/mcp-server) | **MEDIUM** | 5 | shell HTTP client [5 egress primitives across 1 category: netcall] |
| [blockscout__mcp-server/.cursor/rules](https://github.com/blockscout/mcp-server) | **MEDIUM** | 3 | shell HTTP client [3 egress primitives across 1 category: netcall] |
| [e2b-dev__mcp-server/e2b-dev__mcp-server](https://github.com/e2b-dev/mcp-server) | **MEDIUM** | 3 | multipart file upload call; git push from skill [2 egress primitives across 2 categories: gitwrite, img_upload] |
| [grafana_mcp-grafana/.claude/skills/draft-release](https://github.com/grafana/mcp-grafana) | **MEDIUM** | 3 | git push from skill; gh CLI create (issue/PR/release/gist) [3 egress primitives across 1 category: gitwrite] |
| [stripe__agent-toolkit/benchmarks/saas-starter-embedded-checkout/environment](https://github.com/stripe/agent-toolkit) | **MEDIUM** | 3 | HTTP client call [3 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/benchmarks/saas-starter-partial-payments/environment](https://github.com/stripe/agent-toolkit) | **MEDIUM** | 3 | HTTP client call [3 egress primitives across 1 category: netcall] |
| [blockscout__mcp-server/.agents/skills/gh-issue-publish](https://github.com/blockscout/mcp-server) | **LOW** | 2 | gh CLI create (issue/PR/release/gist) [2 egress primitives across 1 category: gitwrite] |
| [f4ww4z__mcp-mysql-server/f4ww4z__mcp-mysql-server](https://github.com/f4ww4z/mcp-mysql-server) | **LOW** | 2 | multipart file upload call [1 egress primitives across 1 category: img_upload] |
| [ferrislucas__iterm-mcp/ferrislucas__iterm-mcp](https://github.com/ferrislucas/iterm-mcp) | **LOW** | 2 | multipart file upload call [1 egress primitives across 1 category: img_upload] |
| [kazuph__mcp-taskmanager/kazuph__mcp-taskmanager](https://github.com/kazuph/mcp-taskmanager) | **LOW** | 2 | multipart file upload call [1 egress primitives across 1 category: img_upload] |
| npm__mcp-obsidian/npm__mcp-obsidian | **LOW** | 2 | multipart file upload call [1 egress primitives across 1 category: img_upload] |
| [stripe__agent-toolkit/llm/ai-sdk](https://github.com/stripe/agent-toolkit) | **LOW** | 2 | multipart file upload call [1 egress primitives across 1 category: img_upload] |
| [stripe__agent-toolkit/llm/token-meter](https://github.com/stripe/agent-toolkit) | **LOW** | 2 | multipart file upload call [1 egress primitives across 1 category: img_upload] |
| [stripe__agent-toolkit/providers/agent-plugins/plugin/skills/stripe-docs](https://github.com/stripe/agent-toolkit) | **LOW** | 2 | shell HTTP client [2 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/providers/agent-plugins/plugin/skills/upgrade-stripe](https://github.com/stripe/agent-toolkit) | **LOW** | 2 | shell HTTP client [2 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/providers/claude/plugin/skills/stripe-docs](https://github.com/stripe/agent-toolkit) | **LOW** | 2 | shell HTTP client [2 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/providers/claude/plugin/skills/upgrade-stripe](https://github.com/stripe/agent-toolkit) | **LOW** | 2 | shell HTTP client [2 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/providers/codex/plugin/skills/stripe-docs](https://github.com/stripe/agent-toolkit) | **LOW** | 2 | shell HTTP client [2 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/providers/codex/plugin/skills/upgrade-stripe](https://github.com/stripe/agent-toolkit) | **LOW** | 2 | shell HTTP client [2 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/providers/cursor/plugin/skills/stripe-docs](https://github.com/stripe/agent-toolkit) | **LOW** | 2 | shell HTTP client [2 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/providers/cursor/plugin/skills/upgrade-stripe](https://github.com/stripe/agent-toolkit) | **LOW** | 2 | shell HTTP client [2 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/providers/grok/plugin/skills/stripe-docs](https://github.com/stripe/agent-toolkit) | **LOW** | 2 | shell HTTP client [2 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/providers/grok/plugin/skills/upgrade-stripe](https://github.com/stripe/agent-toolkit) | **LOW** | 2 | shell HTTP client [2 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/skills/stripe-docs](https://github.com/stripe/agent-toolkit) | **LOW** | 2 | shell HTTP client [2 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/skills/upgrade-stripe](https://github.com/stripe/agent-toolkit) | **LOW** | 2 | shell HTTP client [2 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/tools/modelcontextprotocol](https://github.com/stripe/agent-toolkit) | **LOW** | 2 | multipart file upload call [1 egress primitives across 1 category: img_upload] |
| [stripe__agent-toolkit/tools/typescript](https://github.com/stripe/agent-toolkit) | **LOW** | 2 | multipart file upload call [1 egress primitives across 1 category: img_upload] |
| [tavily-ai__tavily-mcp/tavily-ai__tavily-mcp](https://github.com/tavily-ai/tavily-mcp) | **LOW** | 2 | multipart file upload call [1 egress primitives across 1 category: img_upload] |
| [stripe__agent-toolkit/providers/agent-plugins/plugin/skills/stripe-apps](https://github.com/stripe/agent-toolkit) | **LOW** | 1 | HTTP client call [1 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/providers/claude/plugin/skills/stripe-apps](https://github.com/stripe/agent-toolkit) | **LOW** | 1 | HTTP client call [1 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/providers/codex/plugin/skills/stripe-apps](https://github.com/stripe/agent-toolkit) | **LOW** | 1 | HTTP client call [1 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/providers/cursor/plugin/skills/stripe-apps](https://github.com/stripe/agent-toolkit) | **LOW** | 1 | HTTP client call [1 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/providers/grok/plugin/skills/stripe-apps](https://github.com/stripe/agent-toolkit) | **LOW** | 1 | HTTP client call [1 egress primitives across 1 category: netcall] |
| [stripe__agent-toolkit/skills/stripe-apps](https://github.com/stripe/agent-toolkit) | **LOW** | 1 | HTTP client call [1 egress primitives across 1 category: netcall] |

## Findings

### medplum_medplum/medplum_medplum — CRITICAL (score 1002)
Repo: https://github.com/medplum/medplum
Why: GitHub user-attachments image host; tunnel tools; browser automation libs; SMTP/sendmail usage [746 egress primitives across 9 categories: browser, dns, email, gitwrite, img_upload, netcall, relay, tunnel, webhook]

- **img_upload** (CRITICAL, confirmed): `user-images.githubusercontent.com` — [README.md:121](https://github.com/medplum/medplum/blob/HEAD/README.md#L121) — GitHub user-attachments image host
- **img_upload** (CRITICAL, confirmed): `user-images.githubusercontent.com` — [examples/medplum-client-external-idp-demo/README.md:7](https://github.com/medplum/medplum/blob/HEAD/examples/medplum-client-external-idp-demo/README.md#L7) — GitHub user-attachments image host
- **img_upload** (CRITICAL, confirmed): `user-images.githubusercontent.com` — [packages/docs/blog/2022-02-11-soc2.mdx:25](https://github.com/medplum/medplum/blob/HEAD/packages/docs/blog/2022-02-11-soc2.mdx#L25) — GitHub user-attachments image host
- **img_upload** (CRITICAL, confirmed): `user-images.githubusercontent.com` — [packages/fhirtypes/README.md:39](https://github.com/medplum/medplum/blob/HEAD/packages/fhirtypes/README.md#L39) — GitHub user-attachments image host
- **img_upload** (CRITICAL, confirmed): `user-images.githubusercontent.com` — [packages/fhirtypes/README.md:43](https://github.com/medplum/medplum/blob/HEAD/packages/fhirtypes/README.md#L43) — GitHub user-attachments image host
- **tunnel** (CRITICAL, confirmed): `ngrok` — [packages/server/src/oauth/README.md:92](https://github.com/medplum/medplum/blob/HEAD/packages/server/src/oauth/README.md#L92) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [packages/server/src/oauth/README.md:94](https://github.com/medplum/medplum/blob/HEAD/packages/server/src/oauth/README.md#L94) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [packages/server/src/oauth/README.md:96](https://github.com/medplum/medplum/blob/HEAD/packages/server/src/oauth/README.md#L96) — tunnel tools

### executeautomation__mcp-playwright/executeautomation__mcp-playwright — CRITICAL (score 825)
Repo: https://github.com/executeautomation/mcp-playwright
Why: browser automation libs; multipart file upload call; browser navigation calls; shell HTTP client [425 egress primitives across 3 categories: browser, img_upload, netcall]

- **browser** (HIGH, confirmed): `Playwright` — [CHANGELOG.md:3](https://github.com/executeautomation/mcp-playwright/blob/HEAD/CHANGELOG.md#L3) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [CHANGELOG.md:13](https://github.com/executeautomation/mcp-playwright/blob/HEAD/CHANGELOG.md#L13) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [CHANGELOG.md:22](https://github.com/executeautomation/mcp-playwright/blob/HEAD/CHANGELOG.md#L22) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [CHANGELOG.md:23](https://github.com/executeautomation/mcp-playwright/blob/HEAD/CHANGELOG.md#L23) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [CHANGELOG.md:24](https://github.com/executeautomation/mcp-playwright/blob/HEAD/CHANGELOG.md#L24) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [CHANGELOG.md:25](https://github.com/executeautomation/mcp-playwright/blob/HEAD/CHANGELOG.md#L25) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [CHANGELOG.md:26](https://github.com/executeautomation/mcp-playwright/blob/HEAD/CHANGELOG.md#L26) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [CHANGELOG.md:34](https://github.com/executeautomation/mcp-playwright/blob/HEAD/CHANGELOG.md#L34) — browser automation libs

### cloudflare__mcp-server-cloudflare/cloudflare__mcp-server-cloudflare — CRITICAL (score 716)
Repo: https://github.com/cloudflare/mcp-server-cloudflare
Why: GitHub user-attachments image host; browser automation libs; SMTP/sendmail usage; multipart file upload call [483 egress primitives across 5 categories: browser, email, img_upload, netcall, registry]

- **img_upload** (CRITICAL, confirmed): `github.com/user-attachments` — [README.md:65](https://github.com/cloudflare/mcp-server-cloudflare/blob/HEAD/README.md#L65) — GitHub user-attachments image host
- **browser** (HIGH, confirmed): `playwright` — [pnpm-lock.yaml:4944](https://github.com/cloudflare/mcp-server-cloudflare/blob/HEAD/pnpm-lock.yaml#L4944) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [pnpm-lock.yaml:4960](https://github.com/cloudflare/mcp-server-cloudflare/blob/HEAD/pnpm-lock.yaml#L4960) — browser automation libs
- **browser** (HIGH, confirmed): `puppeteer` — [apps/ai-gateway/worker-configuration.d.ts:10630](https://github.com/cloudflare/mcp-server-cloudflare/blob/HEAD/apps/ai-gateway/worker-configuration.d.ts#L10630) — browser automation libs
- **browser** (HIGH, confirmed): `puppeteer` — [apps/ai-gateway/worker-configuration.d.ts:10639](https://github.com/cloudflare/mcp-server-cloudflare/blob/HEAD/apps/ai-gateway/worker-configuration.d.ts#L10639) — browser automation libs
- **browser** (HIGH, confirmed): `puppeteer` — [apps/ai-gateway/worker-configuration.d.ts:10645](https://github.com/cloudflare/mcp-server-cloudflare/blob/HEAD/apps/ai-gateway/worker-configuration.d.ts#L10645) — browser automation libs
- **browser** (HIGH, confirmed): `puppeteer` — [apps/ai-gateway/worker-configuration.d.ts:10650](https://github.com/cloudflare/mcp-server-cloudflare/blob/HEAD/apps/ai-gateway/worker-configuration.d.ts#L10650) — browser automation libs
- **browser** (HIGH, confirmed): `puppeteer` — [apps/ai-gateway/worker-configuration.d.ts:10669](https://github.com/cloudflare/mcp-server-cloudflare/blob/HEAD/apps/ai-gateway/worker-configuration.d.ts#L10669) — browser automation libs

### getsentry__sentry-mcp/getsentry__sentry-mcp — CRITICAL (score 631)
Repo: https://github.com/getsentry/sentry-mcp
Why: browser automation libs; hardcoded secret-shaped token; SMTP/sendmail usage; multipart file upload call [595 egress primitives across 8 categories: browser, creds, dns, email, gitwrite, img_upload, netcall, webhook]

- **browser** (HIGH, confirmed): `playwright` — [pnpm-lock.yaml:8055](https://github.com/getsentry/sentry-mcp/blob/HEAD/pnpm-lock.yaml#L8055) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [pnpm-lock.yaml:8071](https://github.com/getsentry/sentry-mcp/blob/HEAD/pnpm-lock.yaml#L8071) — browser automation libs
- **creds** (HIGH, confirmed): `sk-abc123def456ghi789jkl012mno345pqr678stu901vwx234` — [packages/mcp-core/src/telem/sentry.test.ts:10](https://github.com/getsentry/sentry-mcp/blob/HEAD/packages/mcp-core/src/telem/sentry.test.ts#L10) — hardcoded secret-shaped token
- **creds** (HIGH, confirmed): `sk-abc123def456ghi789jkl012mno345pqr678stu901vwx234` — [packages/mcp-core/src/telem/sentry.test.ts:20](https://github.com/getsentry/sentry-mcp/blob/HEAD/packages/mcp-core/src/telem/sentry.test.ts#L20) — hardcoded secret-shaped token
- **creds** (HIGH, confirmed): `sk-abc123def456ghi789jkl012mno345pqr678stu901vwx234` — [packages/mcp-core/src/telem/sentry.test.ts:32](https://github.com/getsentry/sentry-mcp/blob/HEAD/packages/mcp-core/src/telem/sentry.test.ts#L32) — hardcoded secret-shaped token
- **creds** (HIGH, confirmed): `sk-abc123def456ghi789jkl012mno345pqr678stu901vwx234` — [packages/mcp-core/src/telem/sentry.test.ts:69](https://github.com/getsentry/sentry-mcp/blob/HEAD/packages/mcp-core/src/telem/sentry.test.ts#L69) — hardcoded secret-shaped token
- **creds** (HIGH, confirmed): `sk-abc123def456ghi789jkl012mno345pqr678stu901vwx234` — [packages/mcp-core/src/telem/sentry.test.ts:94](https://github.com/getsentry/sentry-mcp/blob/HEAD/packages/mcp-core/src/telem/sentry.test.ts#L94) — hardcoded secret-shaped token
- **creds** (HIGH, confirmed): `sk-abc123def456ghi789jkl012mno345pqr678stu901vwx234` — [packages/mcp-core/src/telem/sentry.test.ts:122](https://github.com/getsentry/sentry-mcp/blob/HEAD/packages/mcp-core/src/telem/sentry.test.ts#L122) — hardcoded secret-shaped token

### microsoft__playwright-mcp/microsoft__playwright-mcp — CRITICAL (score 507)
Repo: https://github.com/microsoft/playwright-mcp
Why: browser automation libs; browser navigation calls; git push from skill; gh CLI create (issue/PR/release/gist) [263 egress primitives across 3 categories: browser, gitwrite, netcall]

- **browser** (HIGH, confirmed): `playwright` — [.gitignore:3](https://github.com/microsoft/playwright-mcp/blob/HEAD/.gitignore#L3) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [CLAUDE.md:14](https://github.com/microsoft/playwright-mcp/blob/HEAD/CLAUDE.md#L14) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [CLAUDE.md:18](https://github.com/microsoft/playwright-mcp/blob/HEAD/CLAUDE.md#L18) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [CLAUDE.md:24](https://github.com/microsoft/playwright-mcp/blob/HEAD/CLAUDE.md#L24) — browser automation libs
- **browser** (HIGH, confirmed): `Playwright` — [CLAUDE.md:32](https://github.com/microsoft/playwright-mcp/blob/HEAD/CLAUDE.md#L32) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [CLAUDE.md:34](https://github.com/microsoft/playwright-mcp/blob/HEAD/CLAUDE.md#L34) — browser automation libs
- **browser** (HIGH, confirmed): `Playwright` — [CLAUDE.md:37](https://github.com/microsoft/playwright-mcp/blob/HEAD/CLAUDE.md#L37) — browser automation libs
- **browser** (HIGH, confirmed): `Playwright` — [CONTRIBUTING.md:5](https://github.com/microsoft/playwright-mcp/blob/HEAD/CONTRIBUTING.md#L5) — browser automation libs

### team-telnyx_telnyx-mcp-server — CRITICAL (score 446)
Repo: https://github.com/team-telnyx/telnyx-mcp-server
Why: GitHub user-attachments image host; tunnel tools; shell HTTP client [150 egress primitives across 3 categories: img_upload, netcall, tunnel]

- **img_upload** (CRITICAL, confirmed): `github.com/user-attachments` — [README.md:271](https://github.com/team-telnyx/telnyx-mcp-server/blob/HEAD/README.md#L271) — GitHub user-attachments image host
- **tunnel** (CRITICAL, confirmed): `ngrok` — [README.md:193](https://github.com/team-telnyx/telnyx-mcp-server/blob/HEAD/README.md#L193) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `Ngrok` — [README.md:197](https://github.com/team-telnyx/telnyx-mcp-server/blob/HEAD/README.md#L197) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [README.md:202](https://github.com/team-telnyx/telnyx-mcp-server/blob/HEAD/README.md#L202) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [README.md:212](https://github.com/team-telnyx/telnyx-mcp-server/blob/HEAD/README.md#L212) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `Ngrok` — [README.md:216](https://github.com/team-telnyx/telnyx-mcp-server/blob/HEAD/README.md#L216) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [README.md:218](https://github.com/team-telnyx/telnyx-mcp-server/blob/HEAD/README.md#L218) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [README.md:220](https://github.com/team-telnyx/telnyx-mcp-server/blob/HEAD/README.md#L220) — tunnel tools

### bhromecevsools_chrome-devtools-mcp/bhromecevsools_chrome-devtools-mcp — CRITICAL (score 377)
Repo: https://github.com/ChromeDevTools/chrome-devtools-mcp
Why: browser automation libs; multipart file upload call; browser navigation calls; shell HTTP client [217 egress primitives across 3 categories: browser, img_upload, netcall]

- **browser** (HIGH, confirmed): `puppeteer` — [.npmrc:3](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/HEAD/.npmrc#L3) — browser automation libs
- **browser** (HIGH, confirmed): `puppeteer` — [.npmrc:4](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/HEAD/.npmrc#L4) — browser automation libs
- **browser** (HIGH, confirmed): `puppeteer` — [.npmrc:5](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/HEAD/.npmrc#L5) — browser automation libs
- **browser** (HIGH, confirmed): `Puppeteer` — [AGENTS.md:27](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/HEAD/AGENTS.md#L27) — browser automation libs
- **browser** (HIGH, confirmed): `Puppeteer` — [AGENTS.md:32](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/HEAD/AGENTS.md#L32) — browser automation libs
- **browser** (HIGH, confirmed): `Puppeteer` — [AGENTS.md:33](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/HEAD/AGENTS.md#L33) — browser automation libs
- **browser** (HIGH, confirmed): `Puppeteer` — [AGENTS.md:42](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/HEAD/AGENTS.md#L42) — browser automation libs
- **browser** (HIGH, confirmed): `Puppeteer` — [CHANGELOG.md:35](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/HEAD/CHANGELOG.md#L35) — browser automation libs

### browser-use_browser-use/skills/cloud — CRITICAL (score 326)
Repo: https://github.com/browser-use/browser-use
Why: browser automation libs; browser navigation calls; shell HTTP client [177 egress primitives across 2 categories: browser, netcall]

- **browser** (HIGH, confirmed): `browser-use` — [skills/cloud/SKILL.md:6](https://github.com/browser-use/browser-use/blob/HEAD/skills/cloud/SKILL.md#L6) — browser automation libs
- **browser** (HIGH, confirmed): `Browser-Use` — [skills/cloud/SKILL.md:7](https://github.com/browser-use/browser-use/blob/HEAD/skills/cloud/SKILL.md#L7) — browser automation libs
- **browser** (HIGH, confirmed): `Playwright` — [skills/cloud/SKILL.md:12](https://github.com/browser-use/browser-use/blob/HEAD/skills/cloud/SKILL.md#L12) — browser automation libs
- **browser** (HIGH, confirmed): `Puppeteer` — [skills/cloud/SKILL.md:13](https://github.com/browser-use/browser-use/blob/HEAD/skills/cloud/SKILL.md#L13) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/cloud/SKILL.md:28](https://github.com/browser-use/browser-use/blob/HEAD/skills/cloud/SKILL.md#L28) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/cloud/SKILL.md:30](https://github.com/browser-use/browser-use/blob/HEAD/skills/cloud/SKILL.md#L30) — browser automation libs
- **browser** (HIGH, confirmed): `Playwright` — [skills/cloud/SKILL.md:43](https://github.com/browser-use/browser-use/blob/HEAD/skills/cloud/SKILL.md#L43) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/cloud/SKILL.md:52](https://github.com/browser-use/browser-use/blob/HEAD/skills/cloud/SKILL.md#L52) — browser automation libs

### mongodb-js_mongodb-mcp-server/mongodb-js_mongodb-mcp-server — CRITICAL (score 259)
Repo: https://github.com/mongodb-js/mongodb-mcp-server
Why: tunnel tools; browser automation libs; multipart file upload call; curl multipart upload [169 egress primitives across 8 categories: browser, creds, dns, gitwrite, img_upload, netcall, relay, tunnel]

- **tunnel** (CRITICAL, confirmed): `ngrok` — [packages/eval-tests/scripts/evalDb.sh:44](https://github.com/mongodb-js/mongodb-mcp-server/blob/HEAD/packages/eval-tests/scripts/evalDb.sh#L44) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [packages/eval-tests/scripts/evalDb.sh:45](https://github.com/mongodb-js/mongodb-mcp-server/blob/HEAD/packages/eval-tests/scripts/evalDb.sh#L45) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [packages/eval-tests/scripts/evalDb.sh:47](https://github.com/mongodb-js/mongodb-mcp-server/blob/HEAD/packages/eval-tests/scripts/evalDb.sh#L47) — tunnel tools
- **browser** (HIGH, confirmed): `playwright` — [THIRD_PARTY_NOTICES.md:186](https://github.com/mongodb-js/mongodb-mcp-server/blob/HEAD/THIRD_PARTY_NOTICES.md#L186) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [THIRD_PARTY_NOTICES.md:561](https://github.com/mongodb-js/mongodb-mcp-server/blob/HEAD/THIRD_PARTY_NOTICES.md#L561) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [THIRD_PARTY_NOTICES.md:562](https://github.com/mongodb-js/mongodb-mcp-server/blob/HEAD/THIRD_PARTY_NOTICES.md#L562) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [THIRD_PARTY_NOTICES.md:1701](https://github.com/mongodb-js/mongodb-mcp-server/blob/HEAD/THIRD_PARTY_NOTICES.md#L1701) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [THIRD_PARTY_NOTICES.md:3593](https://github.com/mongodb-js/mongodb-mcp-server/blob/HEAD/THIRD_PARTY_NOTICES.md#L3593) — browser automation libs

### neondatabase__mcp-server-neon/neondatabase__mcp-server-neon — CRITICAL (score 164)
Repo: https://github.com/neondatabase/mcp-server-neon
Why: browser automation libs; SMTP/sendmail usage; multipart file upload call; browser navigation calls [98 egress primitives across 5 categories: browser, email, gitwrite, img_upload, netcall]

- **browser** (HIGH, confirmed): `playwright` — [.gitignore:14](https://github.com/neondatabase/mcp-server-neon/blob/HEAD/.gitignore#L14) — browser automation libs
- **browser** (HIGH, confirmed): `Playwright` — [AGENTS.md:69](https://github.com/neondatabase/mcp-server-neon/blob/HEAD/AGENTS.md#L69) — browser automation libs
- **browser** (HIGH, confirmed): `Playwright` — [AGENTS.md:119](https://github.com/neondatabase/mcp-server-neon/blob/HEAD/AGENTS.md#L119) — browser automation libs
- **browser** (HIGH, confirmed): `Playwright` — [AGENTS.md:137](https://github.com/neondatabase/mcp-server-neon/blob/HEAD/AGENTS.md#L137) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [AGENTS.md:140](https://github.com/neondatabase/mcp-server-neon/blob/HEAD/AGENTS.md#L140) — browser automation libs
- **browser** (HIGH, confirmed): `Playwright` — [AGENTS.md:304](https://github.com/neondatabase/mcp-server-neon/blob/HEAD/AGENTS.md#L304) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [AGENTS.md:354](https://github.com/neondatabase/mcp-server-neon/blob/HEAD/AGENTS.md#L354) — browser automation libs
- **browser** (HIGH, confirmed): `Playwright` — [README.md:470](https://github.com/neondatabase/mcp-server-neon/blob/HEAD/README.md#L470) — browser automation libs

### _tomic-lail_atomic-mail-agentic/_tomic-lail_atomic-mail-agentic — CRITICAL (score 162)
Repo: https://github.com/Atomic-Mail/atomic-mail-agentic
Why: browser automation libs; SMTP/sendmail usage; multipart file upload call; git push from skill [118 egress primitives across 5 categories: browser, email, gitwrite, img_upload, netcall]

- **browser** (HIGH, confirmed): `stagehand` — [integrations/n8n/atomicmail/package-lock.json:67](https://github.com/Atomic-Mail/atomic-mail-agentic/blob/HEAD/integrations/n8n/atomicmail/package-lock.json#L67) — browser automation libs
- **browser** (HIGH, confirmed): `stagehand` — [integrations/n8n/atomicmail/package-lock.json:69](https://github.com/Atomic-Mail/atomic-mail-agentic/blob/HEAD/integrations/n8n/atomicmail/package-lock.json#L69) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [integrations/n8n/atomicmail/package-lock.json:81](https://github.com/Atomic-Mail/atomic-mail-agentic/blob/HEAD/integrations/n8n/atomicmail/package-lock.json#L81) — browser automation libs
- **browser** (HIGH, confirmed): `stagehand` — [integrations/n8n/atomicmail/package-lock.json:88](https://github.com/Atomic-Mail/atomic-mail-agentic/blob/HEAD/integrations/n8n/atomicmail/package-lock.json#L88) — browser automation libs
- **browser** (HIGH, confirmed): `stagehand` — [integrations/n8n/atomicmail/package-lock.json:1036](https://github.com/Atomic-Mail/atomic-mail-agentic/blob/HEAD/integrations/n8n/atomicmail/package-lock.json#L1036) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [integrations/n8n/atomicmail/package-lock.json:1126](https://github.com/Atomic-Mail/atomic-mail-agentic/blob/HEAD/integrations/n8n/atomicmail/package-lock.json#L1126) — browser automation libs
- **browser** (HIGH, confirmed): `puppeteer` — [integrations/n8n/atomicmail/package-lock.json:1128](https://github.com/Atomic-Mail/atomic-mail-agentic/blob/HEAD/integrations/n8n/atomicmail/package-lock.json#L1128) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [integrations/n8n/atomicmail/package-lock.json:1448](https://github.com/Atomic-Mail/atomic-mail-agentic/blob/HEAD/integrations/n8n/atomicmail/package-lock.json#L1448) — browser automation libs

### hamid-vakilzadeh__mcpsemanticscholar/hamid-vakilzadeh__mcpsemanticscholar — CRITICAL (score 131)
Repo: https://github.com/hamid-vakilzadeh/mcpsemanticscholar
Why: tunnel tools; multipart file upload call; HTTP client call [46 egress primitives across 3 categories: img_upload, netcall, tunnel]

- **tunnel** (CRITICAL, confirmed): `ngrok` — [package-lock.json:946](https://github.com/hamid-vakilzadeh/mcpsemanticscholar/blob/HEAD/package-lock.json#L946) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [package-lock.json:948](https://github.com/hamid-vakilzadeh/mcpsemanticscholar/blob/HEAD/package-lock.json#L948) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [package-lock.json:956](https://github.com/hamid-vakilzadeh/mcpsemanticscholar/blob/HEAD/package-lock.json#L956) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [package-lock.json:957](https://github.com/hamid-vakilzadeh/mcpsemanticscholar/blob/HEAD/package-lock.json#L957) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [package-lock.json:958](https://github.com/hamid-vakilzadeh/mcpsemanticscholar/blob/HEAD/package-lock.json#L958) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [package-lock.json:959](https://github.com/hamid-vakilzadeh/mcpsemanticscholar/blob/HEAD/package-lock.json#L959) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [package-lock.json:960](https://github.com/hamid-vakilzadeh/mcpsemanticscholar/blob/HEAD/package-lock.json#L960) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [package-lock.json:961](https://github.com/hamid-vakilzadeh/mcpsemanticscholar/blob/HEAD/package-lock.json#L961) — tunnel tools

### browser-use_browser-use/skills/open-source — CRITICAL (score 129)
Repo: https://github.com/browser-use/browser-use
Why: browser automation libs; browser navigation calls; shell HTTP client [66 egress primitives across 2 categories: browser, netcall]

- **browser** (HIGH, confirmed): `browser-use` — [skills/open-source/SKILL.md:4](https://github.com/browser-use/browser-use/blob/HEAD/skills/open-source/SKILL.md#L4) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/open-source/SKILL.md:10](https://github.com/browser-use/browser-use/blob/HEAD/skills/open-source/SKILL.md#L10) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/open-source/SKILL.md:13](https://github.com/browser-use/browser-use/blob/HEAD/skills/open-source/SKILL.md#L13) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/open-source/SKILL.md:19](https://github.com/browser-use/browser-use/blob/HEAD/skills/open-source/SKILL.md#L19) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [skills/open-source/SKILL.md:32](https://github.com/browser-use/browser-use/blob/HEAD/skills/open-source/SKILL.md#L32) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/open-source/SKILL.md:40](https://github.com/browser-use/browser-use/blob/HEAD/skills/open-source/SKILL.md#L40) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/open-source/SKILL.md:42](https://github.com/browser-use/browser-use/blob/HEAD/skills/open-source/SKILL.md#L42) — browser automation libs
- **browser** (HIGH, confirmed): `Playwright` — [skills/open-source/references/actor.md:3](https://github.com/browser-use/browser-use/blob/HEAD/skills/open-source/references/actor.md#L3) — browser automation libs

### browser-use_browser-use/skills/qa — CRITICAL (score 108)
Repo: https://github.com/browser-use/browser-use
Why: tunnel tools; browser automation libs; shell HTTP client; HTTP client call [50 egress primitives across 3 categories: browser, netcall, tunnel]

- **tunnel** (CRITICAL, confirmed): `ngrok` — [skills/qa/references/browser-use-v2.md:206](https://github.com/browser-use/browser-use/blob/HEAD/skills/qa/references/browser-use-v2.md#L206) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [skills/qa/references/browser-use-v2.md:207](https://github.com/browser-use/browser-use/blob/HEAD/skills/qa/references/browser-use-v2.md#L207) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [skills/qa/references/methodology.md:23](https://github.com/browser-use/browser-use/blob/HEAD/skills/qa/references/methodology.md#L23) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [skills/qa/references/methodology.md:24](https://github.com/browser-use/browser-use/blob/HEAD/skills/qa/references/methodology.md#L24) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `cloudflared` — [skills/qa/references/methodology.md:25](https://github.com/browser-use/browser-use/blob/HEAD/skills/qa/references/methodology.md#L25) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [skills/qa/references/methodology.md:28](https://github.com/browser-use/browser-use/blob/HEAD/skills/qa/references/methodology.md#L28) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [skills/qa/references/methodology.md:29](https://github.com/browser-use/browser-use/blob/HEAD/skills/qa/references/methodology.md#L29) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `cloudflared` — [skills/qa/references/methodology.md:30](https://github.com/browser-use/browser-use/blob/HEAD/skills/qa/references/methodology.md#L30) — tunnel tools

### apify__actors-mcp-server/apify__actors-mcp-server — CRITICAL (score 65)
Repo: https://github.com/apify/actors-mcp-server
Why: tunnel tools; browser automation libs; multipart file upload call; DNS lookup tools (exfil shape) [44 egress primitives across 7 categories: browser, dns, gitwrite, img_upload, netcall, relay, tunnel]

- **tunnel** (CRITICAL, confirmed): `ngrok` — [DEVELOPMENT.md:260](https://github.com/apify/actors-mcp-server/blob/HEAD/DEVELOPMENT.md#L260) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [DEVELOPMENT.md:262](https://github.com/apify/actors-mcp-server/blob/HEAD/DEVELOPMENT.md#L262) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [DEVELOPMENT.md:269](https://github.com/apify/actors-mcp-server/blob/HEAD/DEVELOPMENT.md#L269) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [DEVELOPMENT.md:275](https://github.com/apify/actors-mcp-server/blob/HEAD/DEVELOPMENT.md#L275) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [DEVELOPMENT.md:278](https://github.com/apify/actors-mcp-server/blob/HEAD/DEVELOPMENT.md#L278) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [DEVELOPMENT.md:284](https://github.com/apify/actors-mcp-server/blob/HEAD/DEVELOPMENT.md#L284) — tunnel tools
- **tunnel** (CRITICAL, confirmed): `ngrok` — [DEVELOPMENT.md:287](https://github.com/apify/actors-mcp-server/blob/HEAD/DEVELOPMENT.md#L287) — tunnel tools
- **browser** (HIGH, confirmed): `playwright` — [pnpm-lock.yaml:4395](https://github.com/apify/actors-mcp-server/blob/HEAD/pnpm-lock.yaml#L4395) — browser automation libs

### browser-use_browser-use/browser_use/skills/browser-use — CRITICAL (score 57)
Repo: https://github.com/browser-use/browser-use
Why: browser automation libs; shell HTTP client [29 egress primitives across 2 categories: browser, netcall]

- **browser** (HIGH, confirmed): `browser-use` — [browser_use/skills/browser-use/SKILL.md:2](https://github.com/browser-use/browser-use/blob/HEAD/browser_use/skills/browser-use/SKILL.md#L2) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [browser_use/skills/browser-use/SKILL.md:4](https://github.com/browser-use/browser-use/blob/HEAD/browser_use/skills/browser-use/SKILL.md#L4) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [browser_use/skills/browser-use/SKILL.md:9](https://github.com/browser-use/browser-use/blob/HEAD/browser_use/skills/browser-use/SKILL.md#L9) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [browser_use/skills/browser-use/SKILL.md:15](https://github.com/browser-use/browser-use/blob/HEAD/browser_use/skills/browser-use/SKILL.md#L15) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [browser_use/skills/browser-use/SKILL.md:16](https://github.com/browser-use/browser-use/blob/HEAD/browser_use/skills/browser-use/SKILL.md#L16) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [browser_use/skills/browser-use/SKILL.md:26](https://github.com/browser-use/browser-use/blob/HEAD/browser_use/skills/browser-use/SKILL.md#L26) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [browser_use/skills/browser-use/SKILL.md:30](https://github.com/browser-use/browser-use/blob/HEAD/browser_use/skills/browser-use/SKILL.md#L30) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [browser_use/skills/browser-use/SKILL.md:39](https://github.com/browser-use/browser-use/blob/HEAD/browser_use/skills/browser-use/SKILL.md#L39) — browser automation libs

### browser-use_browser-use/skills/browser-use — CRITICAL (score 57)
Repo: https://github.com/browser-use/browser-use
Why: browser automation libs; shell HTTP client [29 egress primitives across 2 categories: browser, netcall]

- **browser** (HIGH, confirmed): `browser-use` — [skills/browser-use/SKILL.md:2](https://github.com/browser-use/browser-use/blob/HEAD/skills/browser-use/SKILL.md#L2) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/browser-use/SKILL.md:4](https://github.com/browser-use/browser-use/blob/HEAD/skills/browser-use/SKILL.md#L4) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/browser-use/SKILL.md:9](https://github.com/browser-use/browser-use/blob/HEAD/skills/browser-use/SKILL.md#L9) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/browser-use/SKILL.md:15](https://github.com/browser-use/browser-use/blob/HEAD/skills/browser-use/SKILL.md#L15) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/browser-use/SKILL.md:16](https://github.com/browser-use/browser-use/blob/HEAD/skills/browser-use/SKILL.md#L16) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/browser-use/SKILL.md:26](https://github.com/browser-use/browser-use/blob/HEAD/skills/browser-use/SKILL.md#L26) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/browser-use/SKILL.md:30](https://github.com/browser-use/browser-use/blob/HEAD/skills/browser-use/SKILL.md#L30) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/browser-use/SKILL.md:39](https://github.com/browser-use/browser-use/blob/HEAD/skills/browser-use/SKILL.md#L39) — browser automation libs

### makenotion__notion-mcp-server/makenotion__notion-mcp-server — CRITICAL (score 57)
Repo: https://github.com/makenotion/notion-mcp-server
Why: GitHub user-attachments image host; browser automation libs; multipart file upload call; git push from skill [30 egress primitives across 4 categories: browser, gitwrite, img_upload, netcall]

- **img_upload** (CRITICAL, confirmed): `github.com/user-attachments` — [README.md:37](https://github.com/makenotion/notion-mcp-server/blob/HEAD/README.md#L37) — GitHub user-attachments image host
- **img_upload** (CRITICAL, confirmed): `github.com/user-attachments` — [README.md:41](https://github.com/makenotion/notion-mcp-server/blob/HEAD/README.md#L41) — GitHub user-attachments image host
- **img_upload** (CRITICAL, confirmed): `github.com/user-attachments` — [README.md:327](https://github.com/makenotion/notion-mcp-server/blob/HEAD/README.md#L327) — GitHub user-attachments image host
- **browser** (HIGH, confirmed): `playwright` — [package-lock.json:4165](https://github.com/makenotion/notion-mcp-server/blob/HEAD/package-lock.json#L4165) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [package-lock.json:4185](https://github.com/makenotion/notion-mcp-server/blob/HEAD/package-lock.json#L4185) — browser automation libs
- **img_upload** (HIGH, confirmed): `multipart/form-data` — [src/openapi-mcp-server/client/__tests__/http-client-upload.test.ts:50](https://github.com/makenotion/notion-mcp-server/blob/HEAD/src/openapi-mcp-server/client/__tests__/http-client-upload.test.ts#L50) — multipart file upload call
- **img_upload** (HIGH, confirmed): `multipart/form-data` — [src/openapi-mcp-server/client/__tests__/http-client-upload.test.ts:81](https://github.com/makenotion/notion-mcp-server/blob/HEAD/src/openapi-mcp-server/client/__tests__/http-client-upload.test.ts#L81) — multipart file upload call
- **img_upload** (HIGH, confirmed): `multipart/form-data` — [src/openapi-mcp-server/client/__tests__/http-client-upload.test.ts:133](https://github.com/makenotion/notion-mcp-server/blob/HEAD/src/openapi-mcp-server/client/__tests__/http-client-upload.test.ts#L133) — multipart file upload call

### mendableai__firecrawl-mcp-server/mendableai__firecrawl-mcp-server — CRITICAL (score 53)
Repo: https://github.com/mendableai/firecrawl-mcp-server
Why: multipart file upload call; shell HTTP client; HTTP client call [51 egress primitives across 2 categories: img_upload, netcall]

- **img_upload** (HIGH, confirmed): `"files"` — [.eslintrc.json:28](https://github.com/mendableai/firecrawl-mcp-server/blob/HEAD/.eslintrc.json#L28) — multipart file upload call
- **img_upload** (HIGH, confirmed): `"files"` — [package.json:10](https://github.com/mendableai/firecrawl-mcp-server/blob/HEAD/package.json#L10) — multipart file upload call
- **netcall** (MEDIUM, confirmed): `curl` — [Dockerfile.service:27](https://github.com/mendableai/firecrawl-mcp-server/blob/HEAD/Dockerfile.service#L27) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [.github/workflows/publish.yml:96](https://github.com/mendableai/firecrawl-mcp-server/blob/HEAD/.github/workflows/publish.yml#L96) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [.github/workflows/publish.yml:107](https://github.com/mendableai/firecrawl-mcp-server/blob/HEAD/.github/workflows/publish.yml#L107) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [.github/workflows/publish.yml:155](https://github.com/mendableai/firecrawl-mcp-server/blob/HEAD/.github/workflows/publish.yml#L155) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/index.ts:564](https://github.com/mendableai/firecrawl-mcp-server/blob/HEAD/src/index.ts#L564) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/index.ts:1731](https://github.com/mendableai/firecrawl-mcp-server/blob/HEAD/src/index.ts#L1731) — HTTP client call

### supabase-community__supabase-mcp/supabase-community__supabase-mcp — CRITICAL (score 48)
Repo: https://github.com/supabase-community/supabase-mcp
Why: GitHub user-attachments image host; SMTP/sendmail usage; multipart file upload call; HTTP client call [30 egress primitives across 3 categories: email, img_upload, netcall]

- **img_upload** (CRITICAL, confirmed): `github.com/user-attachments` — [README.md:7](https://github.com/supabase-community/supabase-mcp/blob/HEAD/README.md#L7) — GitHub user-attachments image host
- **email** (HIGH, confirmed): `SMTP` — [supabase/config.toml:139](https://github.com/supabase-community/supabase-mcp/blob/HEAD/supabase/config.toml#L139) — SMTP/sendmail usage
- **email** (HIGH, confirmed): `smtp` — [supabase/config.toml:140](https://github.com/supabase-community/supabase-mcp/blob/HEAD/supabase/config.toml#L140) — SMTP/sendmail usage
- **email** (HIGH, confirmed): `smtp` — [supabase/config.toml:142](https://github.com/supabase-community/supabase-mcp/blob/HEAD/supabase/config.toml#L142) — SMTP/sendmail usage
- **img_upload** (HIGH, confirmed): `"files"` — [biome.json:8](https://github.com/supabase-community/supabase-mcp/blob/HEAD/biome.json#L8) — multipart file upload call
- **img_upload** (HIGH, confirmed): `"files"` — [packages/mcp-server-postgrest/package.json:22](https://github.com/supabase-community/supabase-mcp/blob/HEAD/packages/mcp-server-postgrest/package.json#L22) — multipart file upload call
- **img_upload** (HIGH, confirmed): `"files"` — [packages/mcp-server-supabase/package.json:31](https://github.com/supabase-community/supabase-mcp/blob/HEAD/packages/mcp-server-supabase/package.json#L31) — multipart file upload call
- **img_upload** (HIGH, confirmed): `multipart/form-data` — [packages/mcp-server-supabase/src/management-api/types.ts:11885](https://github.com/supabase-community/supabase-mcp/blob/HEAD/packages/mcp-server-supabase/src/management-api/types.ts#L11885) — multipart file upload call

### agentmail-to__agentmail-mcp/agentmail-to__agentmail-mcp — CRITICAL (score 38)
Repo: https://github.com/agentmail-to/agentmail-mcp
Why: multipart file upload call; shell HTTP client; HTTP client call [37 egress primitives across 2 categories: img_upload, netcall]

- **img_upload** (HIGH, confirmed): `"files"` — [packages/npm-stdio-bridge/package.json:20](https://github.com/agentmail-to/agentmail-mcp/blob/HEAD/packages/npm-stdio-bridge/package.json#L20) — multipart file upload call
- **netcall** (MEDIUM, confirmed): `curl` — [.github/workflows/publish-pypi.yml:36](https://github.com/agentmail-to/agentmail-mcp/blob/HEAD/.github/workflows/publish-pypi.yml#L36) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `fetch(` — [packages/server/src/index.ts:453](https://github.com/agentmail-to/agentmail-mcp/blob/HEAD/packages/server/src/index.ts#L453) — HTTP client call
- **netcall** (MEDIUM, confirmed): `urllib.request` — [scripts/audit-public-surfaces.py:11](https://github.com/agentmail-to/agentmail-mcp/blob/HEAD/scripts/audit-public-surfaces.py#L11) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [scripts/audit-public-surfaces.py:45](https://github.com/agentmail-to/agentmail-mcp/blob/HEAD/scripts/audit-public-surfaces.py#L45) — HTTP client call
- **netcall** (MEDIUM, confirmed): `urllib.request` — [scripts/audit-public-surfaces.py:46](https://github.com/agentmail-to/agentmail-mcp/blob/HEAD/scripts/audit-public-surfaces.py#L46) — HTTP client call
- **netcall** (MEDIUM, confirmed): `urllib.request` — [scripts/audit-public-surfaces.py:48](https://github.com/agentmail-to/agentmail-mcp/blob/HEAD/scripts/audit-public-surfaces.py#L48) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [scripts/audit-public-surfaces.py:57](https://github.com/agentmail-to/agentmail-mcp/blob/HEAD/scripts/audit-public-surfaces.py#L57) — HTTP client call

### runpod_runpod-mcp/runpod_runpod-mcp — CRITICAL (score 33)
Repo: https://github.com/runpod/runpod-mcp
Why: multipart file upload call; DNS lookup tools (exfil shape); git push from skill; HTTP client call [31 egress primitives across 4 categories: dns, gitwrite, img_upload, netcall]

- **img_upload** (HIGH, confirmed): `"files"` — [package.json:13](https://github.com/runpod/runpod-mcp/blob/HEAD/package.json#L13) — multipart file upload call
- **img_upload** (HIGH, confirmed): `multipart/form-data` — [tests/credential-check.test.ts:1121](https://github.com/runpod/runpod-mcp/blob/HEAD/tests/credential-check.test.ts#L1121) — multipart file upload call
- **dns** (MEDIUM, confirmed): `dig` — [src/specgen/tools/jobs.ts:530](https://github.com/runpod/runpod-mcp/blob/HEAD/src/specgen/tools/jobs.ts#L530) — DNS lookup tools (exfil shape)
- **gitwrite** (MEDIUM, confirmed): `git push` — [.github/CONTRIBUTING.md:98](https://github.com/runpod/runpod-mcp/blob/HEAD/.github/CONTRIBUTING.md#L98) — git push from skill
- **netcall** (MEDIUM, confirmed): `fetch (` — [THIRD_PARTY_NOTICES.txt:27](https://github.com/runpod/runpod-mcp/blob/HEAD/THIRD_PARTY_NOTICES.txt#L27) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [api/index.ts:181](https://github.com/runpod/runpod-mcp/blob/HEAD/api/index.ts#L181) — HTTP client call
- **netcall** (MEDIUM, confirmed): `curl` — [scripts/check-spec-drift.ts:6](https://github.com/runpod/runpod-mcp/blob/HEAD/scripts/check-spec-drift.ts#L6) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `fetch(` — [scripts/check-spec-drift.ts:22](https://github.com/runpod/runpod-mcp/blob/HEAD/scripts/check-spec-drift.ts#L22) — HTTP client call

### mzxrai__mcp-webresearch/mzxrai__mcp-webresearch — CRITICAL (score 30)
Repo: https://github.com/mzxrai/mcp-webresearch
Why: browser automation libs; multipart file upload call; browser navigation calls; npm postinstall hook [16 egress primitives across 3 categories: browser, img_upload, registry]

- **browser** (HIGH, confirmed): `Playwright` — [README.md:118](https://github.com/mzxrai/mcp-webresearch/blob/HEAD/README.md#L118) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [index.ts:22](https://github.com/mzxrai/mcp-webresearch/blob/HEAD/index.ts#L22) — browser automation libs
- **browser** (HIGH, confirmed): `Puppeteer` — [index.ts:191](https://github.com/mzxrai/mcp-webresearch/blob/HEAD/index.ts#L191) — browser automation libs
- **browser** (HIGH, confirmed): `Playwright` — [index.ts:247](https://github.com/mzxrai/mcp-webresearch/blob/HEAD/index.ts#L247) — browser automation libs
- **browser** (HIGH, confirmed): `Puppeteer` — [index.ts:718](https://github.com/mzxrai/mcp-webresearch/blob/HEAD/index.ts#L718) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [package.json:19](https://github.com/mzxrai/mcp-webresearch/blob/HEAD/package.json#L19) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [package.json:35](https://github.com/mzxrai/mcp-webresearch/blob/HEAD/package.json#L35) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [pnpm-lock.yaml:14](https://github.com/mzxrai/mcp-webresearch/blob/HEAD/pnpm-lock.yaml#L14) — browser automation libs

### browser-use_browser-use/skills/x402 — CRITICAL (score 29)
Repo: https://github.com/browser-use/browser-use
Why: browser automation libs; shell HTTP client [15 egress primitives across 2 categories: browser, netcall]

- **browser** (HIGH, confirmed): `browser-use` — [skills/x402/SKILL.md:3](https://github.com/browser-use/browser-use/blob/HEAD/skills/x402/SKILL.md#L3) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/x402/SKILL.md:9](https://github.com/browser-use/browser-use/blob/HEAD/skills/x402/SKILL.md#L9) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/x402/SKILL.md:42](https://github.com/browser-use/browser-use/blob/HEAD/skills/x402/SKILL.md#L42) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/x402/SKILL.md:43](https://github.com/browser-use/browser-use/blob/HEAD/skills/x402/SKILL.md#L43) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/x402/SKILL.md:190](https://github.com/browser-use/browser-use/blob/HEAD/skills/x402/SKILL.md#L190) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/x402/SKILL.md:192](https://github.com/browser-use/browser-use/blob/HEAD/skills/x402/SKILL.md#L192) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/x402/SKILL.md:224](https://github.com/browser-use/browser-use/blob/HEAD/skills/x402/SKILL.md#L224) — browser automation libs
- **browser** (HIGH, confirmed): `Browser-Use` — [skills/x402/SKILL.md:235](https://github.com/browser-use/browser-use/blob/HEAD/skills/x402/SKILL.md#L235) — browser automation libs

### containers_kubernetes-mcp-server/test/browser — CRITICAL (score 26)
Repo: https://github.com/containers/kubernetes-mcp-server
Why: browser automation libs; browser navigation calls; shell HTTP client [16 egress primitives across 2 categories: browser, netcall]

- **browser** (HIGH, confirmed): `playwright` — [test/browser/basic-host.spec.mjs:1](https://github.com/containers/kubernetes-mcp-server/blob/HEAD/test/browser/basic-host.spec.mjs#L1) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [test/browser/package.json:6](https://github.com/containers/kubernetes-mcp-server/blob/HEAD/test/browser/package.json#L6) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [test/browser/run.sh:7](https://github.com/containers/kubernetes-mcp-server/blob/HEAD/test/browser/run.sh#L7) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [test/browser/run.sh:19](https://github.com/containers/kubernetes-mcp-server/blob/HEAD/test/browser/run.sh#L19) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [test/browser/run.sh:20](https://github.com/containers/kubernetes-mcp-server/blob/HEAD/test/browser/run.sh#L20) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [test/browser/run.sh:21](https://github.com/containers/kubernetes-mcp-server/blob/HEAD/test/browser/run.sh#L21) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [test/browser/run.sh:68](https://github.com/containers/kubernetes-mcp-server/blob/HEAD/test/browser/run.sh#L68) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [test/browser/run.sh:69](https://github.com/containers/kubernetes-mcp-server/blob/HEAD/test/browser/run.sh#L69) — browser automation libs

### docfork__docfork/docfork__docfork — CRITICAL (score 26)
Repo: https://github.com/docfork/docfork
Why: browser automation libs; multipart file upload call; shell HTTP client; HTTP client call [19 egress primitives across 3 categories: browser, img_upload, netcall]

- **browser** (HIGH, confirmed): `playwright` — [packages/dgrep/src/lib/dep-filter.ts:21](https://github.com/docfork/docfork/blob/HEAD/packages/dgrep/src/lib/dep-filter.ts#L21) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [packages/dgrep/src/lib/dep-filter.ts:52](https://github.com/docfork/docfork/blob/HEAD/packages/dgrep/src/lib/dep-filter.ts#L52) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [packages/dgrep/test/lib/dep-filter.test.ts:50](https://github.com/docfork/docfork/blob/HEAD/packages/dgrep/test/lib/dep-filter.test.ts#L50) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [packages/dgrep/test/lib/dep-filter.test.ts:54](https://github.com/docfork/docfork/blob/HEAD/packages/dgrep/test/lib/dep-filter.test.ts#L54) — browser automation libs
- **img_upload** (HIGH, confirmed): `"files"` — [packages/dgrep/package.json:16](https://github.com/docfork/docfork/blob/HEAD/packages/dgrep/package.json#L16) — multipart file upload call
- **img_upload** (HIGH, confirmed): `"files"` — [packages/mcp/package.json:38](https://github.com/docfork/docfork/blob/HEAD/packages/mcp/package.json#L38) — multipart file upload call
- **img_upload** (HIGH, confirmed): `"files"` — [packages/sdk/package.json:41](https://github.com/docfork/docfork/blob/HEAD/packages/sdk/package.json#L41) — multipart file upload call
- **netcall** (MEDIUM, confirmed): `curl` — [.github/workflows/release.yml:100](https://github.com/docfork/docfork/blob/HEAD/.github/workflows/release.yml#L100) — shell HTTP client

### modelcontextprotocol__servers/modelcontextprotocol__servers — CRITICAL (score 26)
Repo: https://github.com/modelcontextprotocol/servers
Why: browser automation libs; multipart file upload call; git push from skill; gh CLI create (issue/PR/release/gist) [17 egress primitives across 4 categories: browser, gitwrite, img_upload, netcall]

- **browser** (HIGH, confirmed): `Puppeteer` — [README.md:49](https://github.com/modelcontextprotocol/servers/blob/HEAD/README.md#L49) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [package-lock.json:3655](https://github.com/modelcontextprotocol/servers/blob/HEAD/package-lock.json#L3655) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [package-lock.json:3675](https://github.com/modelcontextprotocol/servers/blob/HEAD/package-lock.json#L3675) — browser automation libs
- **img_upload** (HIGH, confirmed): `"files"` — [package.json:14](https://github.com/modelcontextprotocol/servers/blob/HEAD/package.json#L14) — multipart file upload call
- **img_upload** (HIGH, confirmed): `"files"` — [src/everything/package.json:18](https://github.com/modelcontextprotocol/servers/blob/HEAD/src/everything/package.json#L18) — multipart file upload call
- **img_upload** (HIGH, confirmed): `"files"` — [src/filesystem/package.json:18](https://github.com/modelcontextprotocol/servers/blob/HEAD/src/filesystem/package.json#L18) — multipart file upload call
- **img_upload** (HIGH, confirmed): `"files"` — [src/git/src/mcp_server_git/server.py:517](https://github.com/modelcontextprotocol/servers/blob/HEAD/src/git/src/mcp_server_git/server.py#L517) — multipart file upload call
- **img_upload** (HIGH, confirmed): `"files"` — [src/memory/package.json:18](https://github.com/modelcontextprotocol/servers/blob/HEAD/src/memory/package.json#L18) — multipart file upload call

### heroku_heroku-mcp-server/heroku_heroku-mcp-server — CRITICAL (score 24)
Repo: https://github.com/heroku/heroku-mcp-server
Why: multipart file upload call; git push from skill; HTTP client call; shell HTTP client [23 egress primitives across 3 categories: gitwrite, img_upload, netcall]

- **img_upload** (HIGH, confirmed): `"files"` — [package.json:60](https://github.com/heroku/heroku-mcp-server/blob/HEAD/package.json#L60) — multipart file upload call
- **gitwrite** (MEDIUM, confirmed): `git push` — [CONTRIBUTING.md:74](https://github.com/heroku/heroku-mcp-server/blob/HEAD/CONTRIBUTING.md#L74) — git push from skill
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/resources/dev-center-resource.ts:22](https://github.com/heroku/heroku-mcp-server/blob/HEAD/src/resources/dev-center-resource.ts#L22) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/services/app-service.ts:20](https://github.com/heroku/heroku-mcp-server/blob/HEAD/src/services/app-service.ts#L20) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/services/app-setup-service.ts:139](https://github.com/heroku/heroku-mcp-server/blob/HEAD/src/services/app-setup-service.ts#L139) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/services/app-setup-service.ts:171](https://github.com/heroku/heroku-mcp-server/blob/HEAD/src/services/app-setup-service.ts#L171) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/services/build-service.ts:79](https://github.com/heroku/heroku-mcp-server/blob/HEAD/src/services/build-service.ts#L79) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/services/build-service.ts:113](https://github.com/heroku/heroku-mcp-server/blob/HEAD/src/services/build-service.ts#L113) — HTTP client call

### stripe__agent-toolkit/benchmarks/furever/environment — CRITICAL (score 24)
Repo: https://github.com/stripe/agent-toolkit
Why: browser automation libs; HTTP client call [22 egress primitives across 2 categories: browser, netcall]

- **browser** (HIGH, confirmed): `playwright` — [benchmarks/furever/environment/package-lock.json:8085](https://github.com/stripe/agent-toolkit/blob/HEAD/benchmarks/furever/environment/package-lock.json#L8085) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [benchmarks/furever/environment/package-lock.json:8094](https://github.com/stripe/agent-toolkit/blob/HEAD/benchmarks/furever/environment/package-lock.json#L8094) — browser automation libs
- **netcall** (MEDIUM, confirmed): `fetch(` — [benchmarks/furever/environment/app/(dashboard)/finances/page.tsx:41](https://github.com/stripe/agent-toolkit/blob/HEAD/benchmarks/furever/environment/app/(dashboard)/finances/page.tsx#L41) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [benchmarks/furever/environment/app/components/BrandSettingsModal.tsx:85](https://github.com/stripe/agent-toolkit/blob/HEAD/benchmarks/furever/environment/app/components/BrandSettingsModal.tsx#L85) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [benchmarks/furever/environment/app/components/BrandSettingsModal.tsx:93](https://github.com/stripe/agent-toolkit/blob/HEAD/benchmarks/furever/environment/app/components/BrandSettingsModal.tsx#L93) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [benchmarks/furever/environment/app/components/BrandSettingsModal.tsx:107](https://github.com/stripe/agent-toolkit/blob/HEAD/benchmarks/furever/environment/app/components/BrandSettingsModal.tsx#L107) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [benchmarks/furever/environment/app/components/BrandSettingsModal.tsx:156](https://github.com/stripe/agent-toolkit/blob/HEAD/benchmarks/furever/environment/app/components/BrandSettingsModal.tsx#L156) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [benchmarks/furever/environment/app/components/DataRequest.tsx:21](https://github.com/stripe/agent-toolkit/blob/HEAD/benchmarks/furever/environment/app/components/DataRequest.tsx#L21) — HTTP client call

### adamamer20__paper-search-mcp-openai — CRITICAL (score 19)
Repo: https://github.com/adamamer20/paper-search-mcp-openai
Why: TLS verification disabled; shell HTTP client; HTTP client call [19 egress primitives across 2 categories: creds, netcall]

- **creds** (MEDIUM, confirmed): `verify=False` — [paper_search_mcp/academic_platforms/sci_hub.py:54](https://github.com/adamamer20/paper-search-mcp-openai/blob/HEAD/paper_search_mcp/academic_platforms/sci_hub.py#L54) — TLS verification disabled
- **creds** (MEDIUM, confirmed): `verify=False` — [paper_search_mcp/academic_platforms/sci_hub.py:86](https://github.com/adamamer20/paper-search-mcp-openai/blob/HEAD/paper_search_mcp/academic_platforms/sci_hub.py#L86) — TLS verification disabled
- **netcall** (MEDIUM, confirmed): `curl` — [README.md:98](https://github.com/adamamer20/paper-search-mcp-openai/blob/HEAD/README.md#L98) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `fetch(` — [paper_search_mcp/server.py:283](https://github.com/adamamer20/paper-search-mcp-openai/blob/HEAD/paper_search_mcp/server.py#L283) — HTTP client call
- **netcall** (MEDIUM, confirmed): `requests.get` — [paper_search_mcp/academic_platforms/arxiv.py:32](https://github.com/adamamer20/paper-search-mcp-openai/blob/HEAD/paper_search_mcp/academic_platforms/arxiv.py#L32) — HTTP client call
- **netcall** (MEDIUM, confirmed): `requests.get` — [paper_search_mcp/academic_platforms/arxiv.py:61](https://github.com/adamamer20/paper-search-mcp-openai/blob/HEAD/paper_search_mcp/academic_platforms/arxiv.py#L61) — HTTP client call
- **netcall** (MEDIUM, confirmed): `requests.get` — [paper_search_mcp/academic_platforms/iacr.py:251](https://github.com/adamamer20/paper-search-mcp-openai/blob/HEAD/paper_search_mcp/academic_platforms/iacr.py#L251) — HTTP client call
- **netcall** (MEDIUM, confirmed): `requests.get` — [paper_search_mcp/academic_platforms/pubmed.py:32](https://github.com/adamamer20/paper-search-mcp-openai/blob/HEAD/paper_search_mcp/academic_platforms/pubmed.py#L32) — HTTP client call

### browser-use_browser-use/skills/remote-browser — CRITICAL (score 18)
Repo: https://github.com/browser-use/browser-use
Why: browser automation libs [9 egress primitives across 1 category: browser]

- **browser** (HIGH, confirmed): `browser-use` — [skills/remote-browser/SKILL.md:4](https://github.com/browser-use/browser-use/blob/HEAD/skills/remote-browser/SKILL.md#L4) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/remote-browser/SKILL.md:14](https://github.com/browser-use/browser-use/blob/HEAD/skills/remote-browser/SKILL.md#L14) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/remote-browser/SKILL.md:15](https://github.com/browser-use/browser-use/blob/HEAD/skills/remote-browser/SKILL.md#L15) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/remote-browser/SKILL.md:18](https://github.com/browser-use/browser-use/blob/HEAD/skills/remote-browser/SKILL.md#L18) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/remote-browser/SKILL.md:25](https://github.com/browser-use/browser-use/blob/HEAD/skills/remote-browser/SKILL.md#L25) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/remote-browser/SKILL.md:31](https://github.com/browser-use/browser-use/blob/HEAD/skills/remote-browser/SKILL.md#L31) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/remote-browser/SKILL.md:39](https://github.com/browser-use/browser-use/blob/HEAD/skills/remote-browser/SKILL.md#L39) — browser automation libs
- **browser** (HIGH, confirmed): `browser-use` — [skills/remote-browser/SKILL.md:53](https://github.com/browser-use/browser-use/blob/HEAD/skills/remote-browser/SKILL.md#L53) — browser automation libs

### veirdarains_onesignal-mcp — CRITICAL (score 17)
Repo: https://github.com/WeirdBrains/onesignal-mcp
Why: HTTP client call [17 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `requests.get` — [debug_api_key.py:49](https://github.com/WeirdBrains/onesignal-mcp/blob/HEAD/debug_api_key.py#L49) — HTTP client call
- **netcall** (MEDIUM, confirmed): `requests.get` — [debug_api_key.py:72](https://github.com/WeirdBrains/onesignal-mcp/blob/HEAD/debug_api_key.py#L72) — HTTP client call
- **netcall** (MEDIUM, confirmed): `requests.get` — [debug_api_key.py:94](https://github.com/WeirdBrains/onesignal-mcp/blob/HEAD/debug_api_key.py#L94) — HTTP client call
- **netcall** (MEDIUM, confirmed): `requests.get` — [onesignal_server.py:245](https://github.com/WeirdBrains/onesignal-mcp/blob/HEAD/onesignal_server.py#L245) — HTTP client call
- **netcall** (MEDIUM, confirmed): `requests.post` — [onesignal_server.py:247](https://github.com/WeirdBrains/onesignal-mcp/blob/HEAD/onesignal_server.py#L247) — HTTP client call
- **netcall** (MEDIUM, confirmed): `requests.get` — [test_api_key_validity.py:56](https://github.com/WeirdBrains/onesignal-mcp/blob/HEAD/test_api_key_validity.py#L56) — HTTP client call
- **netcall** (MEDIUM, confirmed): `requests.get` — [test_api_key_validity.py:83](https://github.com/WeirdBrains/onesignal-mcp/blob/HEAD/test_api_key_validity.py#L83) — HTTP client call
- **netcall** (MEDIUM, confirmed): `requests.get` — [test_api_key_validity.py:103](https://github.com/WeirdBrains/onesignal-mcp/blob/HEAD/test_api_key_validity.py#L103) — HTTP client call

### burtthecoder__mcp-shodan/burtthecoder__mcp-shodan — CRITICAL (score 11)
Repo: https://github.com/burtthecoder/mcp-shodan
Why: multipart file upload call; git push from skill; shell HTTP client; HTTP client call [10 egress primitives across 3 categories: gitwrite, img_upload, netcall]

- **img_upload** (HIGH, confirmed): `"files"` — [package.json:25](https://github.com/burtthecoder/mcp-shodan/blob/HEAD/package.json#L25) — multipart file upload call
- **gitwrite** (MEDIUM, confirmed): `git push` — [README.md:294](https://github.com/burtthecoder/mcp-shodan/blob/HEAD/README.md#L294) — git push from skill
- **gitwrite** (MEDIUM, confirmed): `git push` — [.github/workflows/npm-publish.yml:40](https://github.com/burtthecoder/mcp-shodan/blob/HEAD/.github/workflows/npm-publish.yml#L40) — git push from skill
- **gitwrite** (MEDIUM, confirmed): `git push` — [.github/workflows/npm-publish.yml:41](https://github.com/burtthecoder/mcp-shodan/blob/HEAD/.github/workflows/npm-publish.yml#L41) — git push from skill
- **netcall** (MEDIUM, confirmed): `curl` — [README.md:243](https://github.com/burtthecoder/mcp-shodan/blob/HEAD/README.md#L243) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [README.md:245](https://github.com/burtthecoder/mcp-shodan/blob/HEAD/README.md#L245) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `axios.get` — [src/helpers.ts:11](https://github.com/burtthecoder/mcp-shodan/blob/HEAD/src/helpers.ts#L11) — HTTP client call
- **netcall** (MEDIUM, confirmed): `axios.get` — [src/helpers.ts:25](https://github.com/burtthecoder/mcp-shodan/blob/HEAD/src/helpers.ts#L25) — HTTP client call

### bitwarden_mcp-server/bitwarden_mcp-server — HIGH (score 9)
Repo: https://github.com/bitwarden/mcp-server
Why: multipart file upload call; HTTP client call; shell HTTP client [8 egress primitives across 2 categories: img_upload, netcall]

- **img_upload** (HIGH, confirmed): `"files"` — [package.json:41](https://github.com/bitwarden/mcp-server/blob/HEAD/package.json#L41) — multipart file upload call
- **netcall** (MEDIUM, confirmed): `fetch(` — [.claude/CLAUDE.md:609](https://github.com/bitwarden/mcp-server/blob/HEAD/.claude/CLAUDE.md#L609) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/utils/api.ts:26](https://github.com/bitwarden/mcp-server/blob/HEAD/src/utils/api.ts#L26) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/utils/api.ts:137](https://github.com/bitwarden/mcp-server/blob/HEAD/src/utils/api.ts#L137) — HTTP client call
- **netcall** (MEDIUM, confirmed): `wget` — [tests/security.spec.ts:247](https://github.com/bitwarden/mcp-server/blob/HEAD/tests/security.spec.ts#L247) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [tests/security.spec.ts:248](https://github.com/bitwarden/mcp-server/blob/HEAD/tests/security.spec.ts#L248) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [tests/security.spec.ts:290](https://github.com/bitwarden/mcp-server/blob/HEAD/tests/security.spec.ts#L290) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `wget` — [tests/security.spec.ts:291](https://github.com/bitwarden/mcp-server/blob/HEAD/tests/security.spec.ts#L291) — shell HTTP client

### stripe__agent-toolkit/providers/agent-plugins/plugin/skills/connect-required-verification-information — HIGH (score 9)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [9 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [providers/agent-plugins/plugin/skills/connect-required-verification-information/SKILL.md:161](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/agent-plugins/plugin/skills/connect-required-verification-information/SKILL.md#L161) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/agent-plugins/plugin/skills/connect-required-verification-information/SKILL.md:176](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/agent-plugins/plugin/skills/connect-required-verification-information/SKILL.md#L176) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/agent-plugins/plugin/skills/connect-required-verification-information/SKILL.md:182](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/agent-plugins/plugin/skills/connect-required-verification-information/SKILL.md#L182) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/agent-plugins/plugin/skills/connect-required-verification-information/SKILL.md:194](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/agent-plugins/plugin/skills/connect-required-verification-information/SKILL.md#L194) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/agent-plugins/plugin/skills/connect-required-verification-information/SKILL.md:197](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/agent-plugins/plugin/skills/connect-required-verification-information/SKILL.md#L197) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/agent-plugins/plugin/skills/connect-required-verification-information/SKILL.md:214](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/agent-plugins/plugin/skills/connect-required-verification-information/SKILL.md#L214) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/agent-plugins/plugin/skills/connect-required-verification-information/SKILL.md:222](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/agent-plugins/plugin/skills/connect-required-verification-information/SKILL.md#L222) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/agent-plugins/plugin/skills/connect-required-verification-information/SKILL.md:240](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/agent-plugins/plugin/skills/connect-required-verification-information/SKILL.md#L240) — shell HTTP client

### stripe__agent-toolkit/providers/claude/plugin/skills/connect-required-verification-information — HIGH (score 9)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [9 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [providers/claude/plugin/skills/connect-required-verification-information/SKILL.md:161](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/claude/plugin/skills/connect-required-verification-information/SKILL.md#L161) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/claude/plugin/skills/connect-required-verification-information/SKILL.md:176](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/claude/plugin/skills/connect-required-verification-information/SKILL.md#L176) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/claude/plugin/skills/connect-required-verification-information/SKILL.md:182](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/claude/plugin/skills/connect-required-verification-information/SKILL.md#L182) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/claude/plugin/skills/connect-required-verification-information/SKILL.md:194](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/claude/plugin/skills/connect-required-verification-information/SKILL.md#L194) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/claude/plugin/skills/connect-required-verification-information/SKILL.md:197](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/claude/plugin/skills/connect-required-verification-information/SKILL.md#L197) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/claude/plugin/skills/connect-required-verification-information/SKILL.md:214](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/claude/plugin/skills/connect-required-verification-information/SKILL.md#L214) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/claude/plugin/skills/connect-required-verification-information/SKILL.md:222](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/claude/plugin/skills/connect-required-verification-information/SKILL.md#L222) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/claude/plugin/skills/connect-required-verification-information/SKILL.md:240](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/claude/plugin/skills/connect-required-verification-information/SKILL.md#L240) — shell HTTP client

### stripe__agent-toolkit/providers/codex/plugin/skills/connect-required-verification-information — HIGH (score 9)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [9 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [providers/codex/plugin/skills/connect-required-verification-information/SKILL.md:161](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/codex/plugin/skills/connect-required-verification-information/SKILL.md#L161) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/codex/plugin/skills/connect-required-verification-information/SKILL.md:176](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/codex/plugin/skills/connect-required-verification-information/SKILL.md#L176) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/codex/plugin/skills/connect-required-verification-information/SKILL.md:182](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/codex/plugin/skills/connect-required-verification-information/SKILL.md#L182) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/codex/plugin/skills/connect-required-verification-information/SKILL.md:194](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/codex/plugin/skills/connect-required-verification-information/SKILL.md#L194) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/codex/plugin/skills/connect-required-verification-information/SKILL.md:197](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/codex/plugin/skills/connect-required-verification-information/SKILL.md#L197) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/codex/plugin/skills/connect-required-verification-information/SKILL.md:214](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/codex/plugin/skills/connect-required-verification-information/SKILL.md#L214) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/codex/plugin/skills/connect-required-verification-information/SKILL.md:222](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/codex/plugin/skills/connect-required-verification-information/SKILL.md#L222) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/codex/plugin/skills/connect-required-verification-information/SKILL.md:240](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/codex/plugin/skills/connect-required-verification-information/SKILL.md#L240) — shell HTTP client

### stripe__agent-toolkit/providers/cursor/plugin/skills/connect-required-verification-information — HIGH (score 9)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [9 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [providers/cursor/plugin/skills/connect-required-verification-information/SKILL.md:161](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/cursor/plugin/skills/connect-required-verification-information/SKILL.md#L161) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/cursor/plugin/skills/connect-required-verification-information/SKILL.md:176](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/cursor/plugin/skills/connect-required-verification-information/SKILL.md#L176) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/cursor/plugin/skills/connect-required-verification-information/SKILL.md:182](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/cursor/plugin/skills/connect-required-verification-information/SKILL.md#L182) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/cursor/plugin/skills/connect-required-verification-information/SKILL.md:194](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/cursor/plugin/skills/connect-required-verification-information/SKILL.md#L194) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/cursor/plugin/skills/connect-required-verification-information/SKILL.md:197](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/cursor/plugin/skills/connect-required-verification-information/SKILL.md#L197) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/cursor/plugin/skills/connect-required-verification-information/SKILL.md:214](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/cursor/plugin/skills/connect-required-verification-information/SKILL.md#L214) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/cursor/plugin/skills/connect-required-verification-information/SKILL.md:222](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/cursor/plugin/skills/connect-required-verification-information/SKILL.md#L222) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/cursor/plugin/skills/connect-required-verification-information/SKILL.md:240](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/cursor/plugin/skills/connect-required-verification-information/SKILL.md#L240) — shell HTTP client

### stripe__agent-toolkit/providers/grok/plugin/skills/connect-required-verification-information — HIGH (score 9)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [9 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [providers/grok/plugin/skills/connect-required-verification-information/SKILL.md:161](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/grok/plugin/skills/connect-required-verification-information/SKILL.md#L161) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/grok/plugin/skills/connect-required-verification-information/SKILL.md:176](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/grok/plugin/skills/connect-required-verification-information/SKILL.md#L176) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/grok/plugin/skills/connect-required-verification-information/SKILL.md:182](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/grok/plugin/skills/connect-required-verification-information/SKILL.md#L182) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/grok/plugin/skills/connect-required-verification-information/SKILL.md:194](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/grok/plugin/skills/connect-required-verification-information/SKILL.md#L194) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/grok/plugin/skills/connect-required-verification-information/SKILL.md:197](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/grok/plugin/skills/connect-required-verification-information/SKILL.md#L197) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/grok/plugin/skills/connect-required-verification-information/SKILL.md:214](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/grok/plugin/skills/connect-required-verification-information/SKILL.md#L214) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/grok/plugin/skills/connect-required-verification-information/SKILL.md:222](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/grok/plugin/skills/connect-required-verification-information/SKILL.md#L222) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/grok/plugin/skills/connect-required-verification-information/SKILL.md:240](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/grok/plugin/skills/connect-required-verification-information/SKILL.md#L240) — shell HTTP client

### stripe__agent-toolkit/skills/connect-required-verification-information — HIGH (score 9)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [9 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [skills/connect-required-verification-information/SKILL.md:161](https://github.com/stripe/agent-toolkit/blob/HEAD/skills/connect-required-verification-information/SKILL.md#L161) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [skills/connect-required-verification-information/SKILL.md:176](https://github.com/stripe/agent-toolkit/blob/HEAD/skills/connect-required-verification-information/SKILL.md#L176) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [skills/connect-required-verification-information/SKILL.md:182](https://github.com/stripe/agent-toolkit/blob/HEAD/skills/connect-required-verification-information/SKILL.md#L182) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [skills/connect-required-verification-information/SKILL.md:194](https://github.com/stripe/agent-toolkit/blob/HEAD/skills/connect-required-verification-information/SKILL.md#L194) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [skills/connect-required-verification-information/SKILL.md:197](https://github.com/stripe/agent-toolkit/blob/HEAD/skills/connect-required-verification-information/SKILL.md#L197) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [skills/connect-required-verification-information/SKILL.md:214](https://github.com/stripe/agent-toolkit/blob/HEAD/skills/connect-required-verification-information/SKILL.md#L214) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [skills/connect-required-verification-information/SKILL.md:222](https://github.com/stripe/agent-toolkit/blob/HEAD/skills/connect-required-verification-information/SKILL.md#L222) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [skills/connect-required-verification-information/SKILL.md:240](https://github.com/stripe/agent-toolkit/blob/HEAD/skills/connect-required-verification-information/SKILL.md#L240) — shell HTTP client

### exa-labs__exa-mcp-server/exa-labs__exa-mcp-server — HIGH (score 8)
Repo: https://github.com/exa-labs/exa-mcp-server
Why: browser automation libs; multipart file upload call; shell HTTP client [5 egress primitives across 3 categories: browser, img_upload, netcall]

- **browser** (HIGH, confirmed): `playwright` — [package-lock.json:6642](https://github.com/exa-labs/exa-mcp-server/blob/HEAD/package-lock.json#L6642) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [package-lock.json:6662](https://github.com/exa-labs/exa-mcp-server/blob/HEAD/package-lock.json#L6662) — browser automation libs
- **img_upload** (HIGH, confirmed): `"files"` — [package.json:15](https://github.com/exa-labs/exa-mcp-server/blob/HEAD/package.json#L15) — multipart file upload call
- **netcall** (MEDIUM, confirmed): `curl` — [.github/workflows/publish-mcp-registry.yml:51](https://github.com/exa-labs/exa-mcp-server/blob/HEAD/.github/workflows/publish-mcp-registry.yml#L51) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [.github/workflows/publish-mcp-registry.yml:73](https://github.com/exa-labs/exa-mcp-server/blob/HEAD/.github/workflows/publish-mcp-registry.yml#L73) — shell HTTP client

### LinkupPlatform__linkup-mcp-server/LinkupPlatform__linkup-mcp-server — HIGH (score 7)
Repo: https://github.com/LinkupPlatform/linkup-mcp-server
Why: multipart file upload call; shell HTTP client; HTTP client call [5 egress primitives across 2 categories: img_upload, netcall]

- **img_upload** (HIGH, confirmed): `"files"` — [biome.json:14](https://github.com/LinkupPlatform/linkup-mcp-server/blob/HEAD/biome.json#L14) — multipart file upload call
- **img_upload** (HIGH, confirmed): `"files"` — [package.json:41](https://github.com/LinkupPlatform/linkup-mcp-server/blob/HEAD/package.json#L41) — multipart file upload call
- **netcall** (MEDIUM, confirmed): `curl` — [README.md:95](https://github.com/LinkupPlatform/linkup-mcp-server/blob/HEAD/README.md#L95) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [README.md:99](https://github.com/LinkupPlatform/linkup-mcp-server/blob/HEAD/README.md#L99) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/tools/fetch.ts:36](https://github.com/LinkupPlatform/linkup-mcp-server/blob/HEAD/src/tools/fetch.ts#L36) — HTTP client call

### brave__brave-search-mcp-server/brave__brave-search-mcp-server — HIGH (score 7)
Repo: https://github.com/brave/brave-search-mcp-server
Why: multipart file upload call; git push from skill; shell HTTP client; HTTP client call [6 egress primitives across 3 categories: gitwrite, img_upload, netcall]

- **img_upload** (HIGH, confirmed): `"files"` — [package.json:25](https://github.com/brave/brave-search-mcp-server/blob/HEAD/package.json#L25) — multipart file upload call
- **gitwrite** (MEDIUM, confirmed): `git push` — [.github/workflows/build-release.yml:93](https://github.com/brave/brave-search-mcp-server/blob/HEAD/.github/workflows/build-release.yml#L93) — git push from skill
- **netcall** (MEDIUM, confirmed): `curl` — [.github/workflows/build-release.yml:190](https://github.com/brave/brave-search-mcp-server/blob/HEAD/.github/workflows/build-release.yml#L190) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [.github/workflows/build-release.yml:191](https://github.com/brave/brave-search-mcp-server/blob/HEAD/.github/workflows/build-release.yml#L191) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/BraveAPI/index.ts:116](https://github.com/brave/brave-search-mcp-server/blob/HEAD/src/BraveAPI/index.ts#L116) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/protocols/http.test.ts:48](https://github.com/brave/brave-search-mcp-server/blob/HEAD/src/protocols/http.test.ts#L48) — HTTP client call

### gologinapp_gologin-mcp/gologinapp_gologin-mcp — HIGH (score 7)
Repo: https://github.com/gologinapp/gologin-mcp
Why: multipart file upload call; shell HTTP client; HTTP client call [6 egress primitives across 2 categories: img_upload, netcall]

- **img_upload** (HIGH, confirmed): `"files"` — [package.json:7](https://github.com/gologinapp/gologin-mcp/blob/HEAD/package.json#L7) — multipart file upload call
- **netcall** (MEDIUM, confirmed): `curl` — [.github/workflows/publish-mcp.yml:40](https://github.com/gologinapp/gologin-mcp/blob/HEAD/.github/workflows/publish-mcp.yml#L40) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [.github/workflows/publish-mcp.yml:41](https://github.com/gologinapp/gologin-mcp/blob/HEAD/.github/workflows/publish-mcp.yml#L41) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `fetch(` — [scripts/check-registry.mjs:30](https://github.com/gologinapp/gologin-mcp/blob/HEAD/scripts/check-registry.mjs#L30) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/index.ts:181](https://github.com/gologinapp/gologin-mcp/blob/HEAD/src/index.ts#L181) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/index.ts:533](https://github.com/gologinapp/gologin-mcp/blob/HEAD/src/index.ts#L533) — HTTP client call

### sjh110007__mcp-jina-ai/sjh110007__mcp-jina-ai — HIGH (score 7)
Repo: https://github.com/sjh110007/mcp-jina-ai
Why: multipart file upload call; fetch-relay/laundering domains; HTTP client call [5 egress primitives across 3 categories: img_upload, netcall, relay]

- **img_upload** (HIGH, confirmed): `"files"` — [package.json:9](https://github.com/sjh110007/mcp-jina-ai/blob/HEAD/package.json#L9) — multipart file upload call
- **relay** (HIGH, confirmed): `r.jina.ai` — [index.ts:49](https://github.com/sjh110007/mcp-jina-ai/blob/HEAD/index.ts#L49) — fetch-relay/laundering domains
- **netcall** (MEDIUM, confirmed): `fetch(` — [index.ts:49](https://github.com/sjh110007/mcp-jina-ai/blob/HEAD/index.ts#L49) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [index.ts:77](https://github.com/sjh110007/mcp-jina-ai/blob/HEAD/index.ts#L77) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [index.ts:98](https://github.com/sjh110007/mcp-jina-ai/blob/HEAD/index.ts#L98) — HTTP client call

### clay-inc__clay-mcp — HIGH (score 6)
Repo: https://github.com/clay-inc/clay-mcp
Why: GitHub user-attachments image host [2 egress primitives across 1 category: img_upload]

- **img_upload** (CRITICAL, confirmed): `github.com/user-attachments` — [README.md:2](https://github.com/clay-inc/clay-mcp/blob/HEAD/README.md#L2) — GitHub user-attachments image host
- **img_upload** (CRITICAL, confirmed): `github.com/user-attachments` — [README.md:19](https://github.com/clay-inc/clay-mcp/blob/HEAD/README.md#L19) — GitHub user-attachments image host

### grafana_mcp-grafana/ui/mcp-apps — HIGH (score 6)
Repo: https://github.com/grafana/mcp-grafana
Why: browser automation libs; multipart file upload call [3 egress primitives across 2 categories: browser, img_upload]

- **browser** (HIGH, confirmed): `playwright` — [ui/mcp-apps/package-lock.json:3915](https://github.com/grafana/mcp-grafana/blob/HEAD/ui/mcp-apps/package-lock.json#L3915) — browser automation libs
- **browser** (HIGH, confirmed): `playwright` — [ui/mcp-apps/package-lock.json:3935](https://github.com/grafana/mcp-grafana/blob/HEAD/ui/mcp-apps/package-lock.json#L3935) — browser automation libs
- **img_upload** (HIGH, confirmed): `"files"` — [ui/mcp-apps/package.json:52](https://github.com/grafana/mcp-grafana/blob/HEAD/ui/mcp-apps/package.json#L52) — multipart file upload call

### localcan_localcanapp — HIGH (score 6)
Repo: https://github.com/localcan/localcanapp
Why: tunnel tools; shell HTTP client [4 egress primitives across 2 categories: netcall, tunnel]

- **tunnel** (CRITICAL, confirmed): `ngrok` — [README.md:5](https://github.com/localcan/localcanapp/blob/HEAD/README.md#L5) — tunnel tools
- **netcall** (MEDIUM, confirmed): `cURL` — [README.md:25](https://github.com/localcan/localcanapp/blob/HEAD/README.md#L25) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [README.md:40](https://github.com/localcan/localcanapp/blob/HEAD/README.md#L40) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [llms-install.md:12](https://github.com/localcan/localcanapp/blob/HEAD/llms-install.md#L12) — shell HTTP client

### AudienseCo__mcp-audiense-insights/AudienseCo__mcp-audiense-insights — MEDIUM (score 5)
Repo: https://github.com/AudienseCo/mcp-audiense-insights
Why: multipart file upload call; HTTP client call [4 egress primitives across 2 categories: img_upload, netcall]

- **img_upload** (HIGH, confirmed): `"files"` — [package.json:13](https://github.com/AudienseCo/mcp-audiense-insights/blob/HEAD/package.json#L13) — multipart file upload call
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/audienseClient.ts:24](https://github.com/AudienseCo/mcp-audiense-insights/blob/HEAD/src/audienseClient.ts#L24) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/audienseClient.ts:63](https://github.com/AudienseCo/mcp-audiense-insights/blob/HEAD/src/audienseClient.ts#L63) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [src/audienseClient.ts:162](https://github.com/AudienseCo/mcp-audiense-insights/blob/HEAD/src/audienseClient.ts#L162) — HTTP client call

### blockscout__mcp-server/.agents/skills/gh-safe — MEDIUM (score 5)
Repo: https://github.com/blockscout/mcp-server
Why: gh CLI create (issue/PR/release/gist) [5 egress primitives across 1 category: gitwrite]

- **gitwrite** (MEDIUM, confirmed): `gh pr create` — [.agents/skills/gh-safe/SKILL.md:5](https://github.com/blockscout/mcp-server/blob/HEAD/.agents/skills/gh-safe/SKILL.md#L5) — gh CLI create (issue/PR/release/gist)
- **gitwrite** (MEDIUM, confirmed): `gh release create` — [.agents/skills/gh-safe/SKILL.md:7](https://github.com/blockscout/mcp-server/blob/HEAD/.agents/skills/gh-safe/SKILL.md#L7) — gh CLI create (issue/PR/release/gist)
- **gitwrite** (MEDIUM, confirmed): `gh pr create` — [.agents/skills/gh-safe/SKILL.md:63](https://github.com/blockscout/mcp-server/blob/HEAD/.agents/skills/gh-safe/SKILL.md#L63) — gh CLI create (issue/PR/release/gist)
- **gitwrite** (MEDIUM, confirmed): `gh issue create` — [.agents/skills/gh-safe/SKILL.md:74](https://github.com/blockscout/mcp-server/blob/HEAD/.agents/skills/gh-safe/SKILL.md#L74) — gh CLI create (issue/PR/release/gist)
- **gitwrite** (MEDIUM, confirmed): `gh release create` — [.agents/skills/gh-safe/SKILL.md:82](https://github.com/blockscout/mcp-server/blob/HEAD/.agents/skills/gh-safe/SKILL.md#L82) — gh CLI create (issue/PR/release/gist)

### blockscout__mcp-server/.agents/skills/sepolia-foundry-tx — MEDIUM (score 5)
Repo: https://github.com/blockscout/mcp-server
Why: shell HTTP client [5 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [.agents/skills/sepolia-foundry-tx/references/pro-api-auth.md:142](https://github.com/blockscout/mcp-server/blob/HEAD/.agents/skills/sepolia-foundry-tx/references/pro-api-auth.md#L142) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [.agents/skills/sepolia-foundry-tx/scripts/deploy.sh:224](https://github.com/blockscout/mcp-server/blob/HEAD/.agents/skills/sepolia-foundry-tx/scripts/deploy.sh#L224) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [.agents/skills/sepolia-foundry-tx/scripts/deploy.sh:230](https://github.com/blockscout/mcp-server/blob/HEAD/.agents/skills/sepolia-foundry-tx/scripts/deploy.sh#L230) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [.agents/skills/sepolia-foundry-tx/scripts/deploy.sh:236](https://github.com/blockscout/mcp-server/blob/HEAD/.agents/skills/sepolia-foundry-tx/scripts/deploy.sh#L236) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [.agents/skills/sepolia-foundry-tx/scripts/deploy.sh:303](https://github.com/blockscout/mcp-server/blob/HEAD/.agents/skills/sepolia-foundry-tx/scripts/deploy.sh#L303) — shell HTTP client

### blockscout__mcp-server/.cursor/rules — MEDIUM (score 3)
Repo: https://github.com/blockscout/mcp-server
Why: shell HTTP client [3 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [.cursor/rules/200-development-testing-workflow.mdc:104](https://github.com/blockscout/mcp-server/blob/HEAD/.cursor/rules/200-development-testing-workflow.mdc#L104) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [.cursor/rules/800-api-documentation-guidelines.mdc:42](https://github.com/blockscout/mcp-server/blob/HEAD/.cursor/rules/800-api-documentation-guidelines.mdc#L42) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [.cursor/rules/800-api-documentation-guidelines.mdc:49](https://github.com/blockscout/mcp-server/blob/HEAD/.cursor/rules/800-api-documentation-guidelines.mdc#L49) — shell HTTP client

### e2b-dev__mcp-server/e2b-dev__mcp-server — MEDIUM (score 3)
Repo: https://github.com/e2b-dev/mcp-server
Why: multipart file upload call; git push from skill [2 egress primitives across 2 categories: gitwrite, img_upload]

- **img_upload** (HIGH, confirmed): `"files"` — [packages/js/package.json:14](https://github.com/e2b-dev/mcp-server/blob/HEAD/packages/js/package.json#L14) — multipart file upload call
- **gitwrite** (MEDIUM, confirmed): `git push` — [.github/workflows/publish_packages.yml:89](https://github.com/e2b-dev/mcp-server/blob/HEAD/.github/workflows/publish_packages.yml#L89) — git push from skill

### grafana_mcp-grafana/.claude/skills/draft-release — MEDIUM (score 3)
Repo: https://github.com/grafana/mcp-grafana
Why: git push from skill; gh CLI create (issue/PR/release/gist) [3 egress primitives across 1 category: gitwrite]

- **gitwrite** (MEDIUM, confirmed): `git push` — [.claude/skills/draft-release/SKILL.md:142](https://github.com/grafana/mcp-grafana/blob/HEAD/.claude/skills/draft-release/SKILL.md#L142) — git push from skill
- **gitwrite** (MEDIUM, confirmed): `gh pr create` — [.claude/skills/draft-release/SKILL.md:147](https://github.com/grafana/mcp-grafana/blob/HEAD/.claude/skills/draft-release/SKILL.md#L147) — gh CLI create (issue/PR/release/gist)
- **gitwrite** (MEDIUM, confirmed): `gh pr create` — [.claude/skills/draft-release/SKILL.md:173](https://github.com/grafana/mcp-grafana/blob/HEAD/.claude/skills/draft-release/SKILL.md#L173) — gh CLI create (issue/PR/release/gist)

### stripe__agent-toolkit/benchmarks/saas-starter-embedded-checkout/environment — MEDIUM (score 3)
Repo: https://github.com/stripe/agent-toolkit
Why: HTTP client call [3 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `fetch(` — [benchmarks/saas-starter-embedded-checkout/environment/app/(dashboard)/layout.tsx:19](https://github.com/stripe/agent-toolkit/blob/HEAD/benchmarks/saas-starter-embedded-checkout/environment/app/(dashboard)/layout.tsx#L19) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [benchmarks/saas-starter-embedded-checkout/environment/app/(dashboard)/dashboard/page.tsx:28](https://github.com/stripe/agent-toolkit/blob/HEAD/benchmarks/saas-starter-embedded-checkout/environment/app/(dashboard)/dashboard/page.tsx#L28) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [benchmarks/saas-starter-embedded-checkout/environment/app/(dashboard)/dashboard/general/page.tsx:14](https://github.com/stripe/agent-toolkit/blob/HEAD/benchmarks/saas-starter-embedded-checkout/environment/app/(dashboard)/dashboard/general/page.tsx#L14) — HTTP client call

### stripe__agent-toolkit/benchmarks/saas-starter-partial-payments/environment — MEDIUM (score 3)
Repo: https://github.com/stripe/agent-toolkit
Why: HTTP client call [3 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `fetch(` — [benchmarks/saas-starter-partial-payments/environment/app/(dashboard)/layout.tsx:19](https://github.com/stripe/agent-toolkit/blob/HEAD/benchmarks/saas-starter-partial-payments/environment/app/(dashboard)/layout.tsx#L19) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [benchmarks/saas-starter-partial-payments/environment/app/(dashboard)/dashboard/page.tsx:28](https://github.com/stripe/agent-toolkit/blob/HEAD/benchmarks/saas-starter-partial-payments/environment/app/(dashboard)/dashboard/page.tsx#L28) — HTTP client call
- **netcall** (MEDIUM, confirmed): `fetch(` — [benchmarks/saas-starter-partial-payments/environment/app/(dashboard)/dashboard/general/page.tsx:14](https://github.com/stripe/agent-toolkit/blob/HEAD/benchmarks/saas-starter-partial-payments/environment/app/(dashboard)/dashboard/general/page.tsx#L14) — HTTP client call

### blockscout__mcp-server/.agents/skills/gh-issue-publish — LOW (score 2)
Repo: https://github.com/blockscout/mcp-server
Why: gh CLI create (issue/PR/release/gist) [2 egress primitives across 1 category: gitwrite]

- **gitwrite** (MEDIUM, confirmed): `gh issue create` — [.agents/skills/gh-issue-publish/SKILL.md:34](https://github.com/blockscout/mcp-server/blob/HEAD/.agents/skills/gh-issue-publish/SKILL.md#L34) — gh CLI create (issue/PR/release/gist)
- **gitwrite** (MEDIUM, confirmed): `gh issue create` — [.agents/skills/gh-issue-publish/script/gh-issue-publish.sh:75](https://github.com/blockscout/mcp-server/blob/HEAD/.agents/skills/gh-issue-publish/script/gh-issue-publish.sh#L75) — gh CLI create (issue/PR/release/gist)

### f4ww4z__mcp-mysql-server/f4ww4z__mcp-mysql-server — LOW (score 2)
Repo: https://github.com/f4ww4z/mcp-mysql-server
Why: multipart file upload call [1 egress primitives across 1 category: img_upload]

- **img_upload** (HIGH, confirmed): `"files"` — [package.json:9](https://github.com/f4ww4z/mcp-mysql-server/blob/HEAD/package.json#L9) — multipart file upload call

### ferrislucas__iterm-mcp/ferrislucas__iterm-mcp — LOW (score 2)
Repo: https://github.com/ferrislucas/iterm-mcp
Why: multipart file upload call [1 egress primitives across 1 category: img_upload]

- **img_upload** (HIGH, confirmed): `"files"` — [package.json:19](https://github.com/ferrislucas/iterm-mcp/blob/HEAD/package.json#L19) — multipart file upload call

### kazuph__mcp-taskmanager/kazuph__mcp-taskmanager — LOW (score 2)
Repo: https://github.com/kazuph/mcp-taskmanager
Why: multipart file upload call [1 egress primitives across 1 category: img_upload]

- **img_upload** (HIGH, confirmed): `"files"` — [package.json:11](https://github.com/kazuph/mcp-taskmanager/blob/HEAD/package.json#L11) — multipart file upload call

### npm__mcp-obsidian/npm__mcp-obsidian — LOW (score 2)
Why: multipart file upload call [1 egress primitives across 1 category: img_upload]

- **img_upload** (HIGH, confirmed): `"files"` — package.json:11 — multipart file upload call

### stripe__agent-toolkit/llm/ai-sdk — LOW (score 2)
Repo: https://github.com/stripe/agent-toolkit
Why: multipart file upload call [1 egress primitives across 1 category: img_upload]

- **img_upload** (HIGH, confirmed): `"files"` — [llm/ai-sdk/package.json:39](https://github.com/stripe/agent-toolkit/blob/HEAD/llm/ai-sdk/package.json#L39) — multipart file upload call

### stripe__agent-toolkit/llm/token-meter — LOW (score 2)
Repo: https://github.com/stripe/agent-toolkit
Why: multipart file upload call [1 egress primitives across 1 category: img_upload]

- **img_upload** (HIGH, confirmed): `"files"` — [llm/token-meter/package.json:33](https://github.com/stripe/agent-toolkit/blob/HEAD/llm/token-meter/package.json#L33) — multipart file upload call

### stripe__agent-toolkit/providers/agent-plugins/plugin/skills/stripe-docs — LOW (score 2)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [2 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [providers/agent-plugins/plugin/skills/stripe-docs/SKILL.md:5](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/agent-plugins/plugin/skills/stripe-docs/SKILL.md#L5) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/agent-plugins/plugin/skills/stripe-docs/SKILL.md:16](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/agent-plugins/plugin/skills/stripe-docs/SKILL.md#L16) — shell HTTP client

### stripe__agent-toolkit/providers/agent-plugins/plugin/skills/upgrade-stripe — LOW (score 2)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [2 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [providers/agent-plugins/plugin/skills/upgrade-stripe/SKILL.md:21](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/agent-plugins/plugin/skills/upgrade-stripe/SKILL.md#L21) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/agent-plugins/plugin/skills/upgrade-stripe/SKILL.md:179](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/agent-plugins/plugin/skills/upgrade-stripe/SKILL.md#L179) — shell HTTP client

### stripe__agent-toolkit/providers/claude/plugin/skills/stripe-docs — LOW (score 2)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [2 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [providers/claude/plugin/skills/stripe-docs/SKILL.md:5](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/claude/plugin/skills/stripe-docs/SKILL.md#L5) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/claude/plugin/skills/stripe-docs/SKILL.md:16](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/claude/plugin/skills/stripe-docs/SKILL.md#L16) — shell HTTP client

### stripe__agent-toolkit/providers/claude/plugin/skills/upgrade-stripe — LOW (score 2)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [2 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [providers/claude/plugin/skills/upgrade-stripe/SKILL.md:21](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/claude/plugin/skills/upgrade-stripe/SKILL.md#L21) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/claude/plugin/skills/upgrade-stripe/SKILL.md:179](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/claude/plugin/skills/upgrade-stripe/SKILL.md#L179) — shell HTTP client

### stripe__agent-toolkit/providers/codex/plugin/skills/stripe-docs — LOW (score 2)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [2 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [providers/codex/plugin/skills/stripe-docs/SKILL.md:5](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/codex/plugin/skills/stripe-docs/SKILL.md#L5) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/codex/plugin/skills/stripe-docs/SKILL.md:16](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/codex/plugin/skills/stripe-docs/SKILL.md#L16) — shell HTTP client

### stripe__agent-toolkit/providers/codex/plugin/skills/upgrade-stripe — LOW (score 2)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [2 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [providers/codex/plugin/skills/upgrade-stripe/SKILL.md:21](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/codex/plugin/skills/upgrade-stripe/SKILL.md#L21) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/codex/plugin/skills/upgrade-stripe/SKILL.md:179](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/codex/plugin/skills/upgrade-stripe/SKILL.md#L179) — shell HTTP client

### stripe__agent-toolkit/providers/cursor/plugin/skills/stripe-docs — LOW (score 2)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [2 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [providers/cursor/plugin/skills/stripe-docs/SKILL.md:5](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/cursor/plugin/skills/stripe-docs/SKILL.md#L5) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/cursor/plugin/skills/stripe-docs/SKILL.md:16](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/cursor/plugin/skills/stripe-docs/SKILL.md#L16) — shell HTTP client

### stripe__agent-toolkit/providers/cursor/plugin/skills/upgrade-stripe — LOW (score 2)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [2 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [providers/cursor/plugin/skills/upgrade-stripe/SKILL.md:21](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/cursor/plugin/skills/upgrade-stripe/SKILL.md#L21) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/cursor/plugin/skills/upgrade-stripe/SKILL.md:179](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/cursor/plugin/skills/upgrade-stripe/SKILL.md#L179) — shell HTTP client

### stripe__agent-toolkit/providers/grok/plugin/skills/stripe-docs — LOW (score 2)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [2 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [providers/grok/plugin/skills/stripe-docs/SKILL.md:5](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/grok/plugin/skills/stripe-docs/SKILL.md#L5) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/grok/plugin/skills/stripe-docs/SKILL.md:16](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/grok/plugin/skills/stripe-docs/SKILL.md#L16) — shell HTTP client

### stripe__agent-toolkit/providers/grok/plugin/skills/upgrade-stripe — LOW (score 2)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [2 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [providers/grok/plugin/skills/upgrade-stripe/SKILL.md:21](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/grok/plugin/skills/upgrade-stripe/SKILL.md#L21) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [providers/grok/plugin/skills/upgrade-stripe/SKILL.md:179](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/grok/plugin/skills/upgrade-stripe/SKILL.md#L179) — shell HTTP client

### stripe__agent-toolkit/skills/stripe-docs — LOW (score 2)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [2 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [skills/stripe-docs/SKILL.md:5](https://github.com/stripe/agent-toolkit/blob/HEAD/skills/stripe-docs/SKILL.md#L5) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [skills/stripe-docs/SKILL.md:16](https://github.com/stripe/agent-toolkit/blob/HEAD/skills/stripe-docs/SKILL.md#L16) — shell HTTP client

### stripe__agent-toolkit/skills/upgrade-stripe — LOW (score 2)
Repo: https://github.com/stripe/agent-toolkit
Why: shell HTTP client [2 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `curl` — [skills/upgrade-stripe/SKILL.md:21](https://github.com/stripe/agent-toolkit/blob/HEAD/skills/upgrade-stripe/SKILL.md#L21) — shell HTTP client
- **netcall** (MEDIUM, confirmed): `curl` — [skills/upgrade-stripe/SKILL.md:179](https://github.com/stripe/agent-toolkit/blob/HEAD/skills/upgrade-stripe/SKILL.md#L179) — shell HTTP client

### stripe__agent-toolkit/tools/modelcontextprotocol — LOW (score 2)
Repo: https://github.com/stripe/agent-toolkit
Why: multipart file upload call [1 egress primitives across 1 category: img_upload]

- **img_upload** (HIGH, confirmed): `"files"` — [tools/modelcontextprotocol/package.json:7](https://github.com/stripe/agent-toolkit/blob/HEAD/tools/modelcontextprotocol/package.json#L7) — multipart file upload call

### stripe__agent-toolkit/tools/typescript — LOW (score 2)
Repo: https://github.com/stripe/agent-toolkit
Why: multipart file upload call [1 egress primitives across 1 category: img_upload]

- **img_upload** (HIGH, confirmed): `"files"` — [tools/typescript/package.json:95](https://github.com/stripe/agent-toolkit/blob/HEAD/tools/typescript/package.json#L95) — multipart file upload call

### tavily-ai__tavily-mcp/tavily-ai__tavily-mcp — LOW (score 2)
Repo: https://github.com/tavily-ai/tavily-mcp
Why: multipart file upload call [1 egress primitives across 1 category: img_upload]

- **img_upload** (HIGH, confirmed): `"files"` — [package.json:14](https://github.com/tavily-ai/tavily-mcp/blob/HEAD/package.json#L14) — multipart file upload call

### stripe__agent-toolkit/providers/agent-plugins/plugin/skills/stripe-apps — LOW (score 1)
Repo: https://github.com/stripe/agent-toolkit
Why: HTTP client call [1 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `fetch(` — [providers/agent-plugins/plugin/skills/stripe-apps/references/ui-extensions.md:23](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/agent-plugins/plugin/skills/stripe-apps/references/ui-extensions.md#L23) — HTTP client call

### stripe__agent-toolkit/providers/claude/plugin/skills/stripe-apps — LOW (score 1)
Repo: https://github.com/stripe/agent-toolkit
Why: HTTP client call [1 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `fetch(` — [providers/claude/plugin/skills/stripe-apps/references/ui-extensions.md:23](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/claude/plugin/skills/stripe-apps/references/ui-extensions.md#L23) — HTTP client call

### stripe__agent-toolkit/providers/codex/plugin/skills/stripe-apps — LOW (score 1)
Repo: https://github.com/stripe/agent-toolkit
Why: HTTP client call [1 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `fetch(` — [providers/codex/plugin/skills/stripe-apps/references/ui-extensions.md:23](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/codex/plugin/skills/stripe-apps/references/ui-extensions.md#L23) — HTTP client call

### stripe__agent-toolkit/providers/cursor/plugin/skills/stripe-apps — LOW (score 1)
Repo: https://github.com/stripe/agent-toolkit
Why: HTTP client call [1 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `fetch(` — [providers/cursor/plugin/skills/stripe-apps/references/ui-extensions.md:23](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/cursor/plugin/skills/stripe-apps/references/ui-extensions.md#L23) — HTTP client call

### stripe__agent-toolkit/providers/grok/plugin/skills/stripe-apps — LOW (score 1)
Repo: https://github.com/stripe/agent-toolkit
Why: HTTP client call [1 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `fetch(` — [providers/grok/plugin/skills/stripe-apps/references/ui-extensions.md:23](https://github.com/stripe/agent-toolkit/blob/HEAD/providers/grok/plugin/skills/stripe-apps/references/ui-extensions.md#L23) — HTTP client call

### stripe__agent-toolkit/skills/stripe-apps — LOW (score 1)
Repo: https://github.com/stripe/agent-toolkit
Why: HTTP client call [1 egress primitives across 1 category: netcall]

- **netcall** (MEDIUM, confirmed): `fetch(` — [skills/stripe-apps/references/ui-extensions.md:23](https://github.com/stripe/agent-toolkit/blob/HEAD/skills/stripe-apps/references/ui-extensions.md#L23) — HTTP client call
