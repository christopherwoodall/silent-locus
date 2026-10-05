# Lane E — Marketplace batch (scan-c): notes

Subagent session 9e9b3f91-3090-42ff-a9d8-73ab6231f632 · 2026-10-05.
Scanner: `~/workspace/muse-home/projects/skill-tracer/scan/egress_scan.py` (taxonomy `egress-taxonomy.md`).
Sources staged in `~/workspace/skill-egress-work/lane-e/` (fetch log `fetch-manifest.tsv`; fetched code is scratch, never committed).

## Method

Lane B's `raw/enum-marketplaces.md` did not exist, so the target list was built from live
marketplace data on 2026-10-05:

- Smithery registry API (`https://api.smithery.ai/servers/<name>`, keyless) for listing
  metadata: qualifiedName, useCount, remote flag, deploymentUrl. Resolved via a vendored
  copy of `websentry-ai/mcp-lookup`'s `SmitheryClient` (wheel downloaded, read statically,
  endpoint queried directly with curl/python — package never installed).
- Cross-checks: `https://mcpso.cc/server/popular-mcp-servers` (Smithery usage ranking),
  the `recodeeai/skills` smithery-usage SKILL.md (recent use counts), and the bawbel
  top-100 Smithery security scan (dev.to) for the current top-100 set.
- `npm view <pkg> repository.url dist.tarball` (read-only) for npm-only servers.

Key structural finding: the current top Smithery listings (`exa` 28K uses, `brave` 13K,
`context7` 11K, `gmail`/`googledrive`/`googlesheets`, `jina` 5K, `github` 6K,
`Tavily` 3.8K, `parallel/search` 6K, `reddit`, `slack`, `deepwiki`) are **remote,
vendor-hosted servers** (`remote: true`, `bySmithery: true`) with **no public source
repo** (e.g. `gmail` → `https://gmail.run.tools`; `parallel/search` →
`https://search.parallel.ai/mcp`). For these, the public upstream project repo was
cloned instead (the same code the vendor deploys), and the remote-only status is noted
per server below. Remote-only = no client-side source to scan; server-side code is
opaque by construction.

Fetch rules honored: public repos/tarballs only; shallow clones (`--depth 1`),
sequential with ~2s pacing; npm tarballs inspected statically (never `npm install`,
no install scripts run); no accounts; secrets noted, never used.

## Source inventory (33 units)

| # | marketplace rank / listing | source fetched | how |
|---|---|---|---|
| 1 | smithery `github` (6,059 uses, remote-only) | modelcontextprotocol/servers | git shallow clone — covers src/github, fetch, memory, time, sequentialthinking, git, gitlab, postgres, sqlite, brave-search, slack, google-maps, sentry, filesystem, etc. |
| 2 | smithery `exa` (28K, remote-only) | exa-labs/exa-mcp-server | git shallow clone |
| 3 | smithery `brave` (13K, remote-only) | brave/brave-search-mcp-server | git shallow clone |
| 4 | smithery `@upstash/context7-mcp` (11K, remote-only) | upstash/context7 | git shallow clone |
| 5 | smithery `Tavily` (3.8K, remote-only) | tavily-ai/tavily-mcp | git shallow clone |
| 6 | smithery `LinkupPlatform/linkup-mcp-server` (2.9K) | LinkupPlatform/linkup-mcp-server | git shallow clone |
| 7 | smithery `docfork/docfork` (2.5K) | docfork/docfork | git shallow clone |
| 8 | smithery `gmail`/`googledrive`/`googlesheets` (remote-only, no repo) | — | NO SOURCE: remote-only at gmail.run.tools etc. (documented, not scanned) |
| 9 | smithery `jina` 5K (remote-only, no repo) | sjh110007/mcp-jina-ai | git shallow clone (community Jina MCP as proxy; noted) |
| 10 | smithery `parallel/search` 6K (remote-only, no repo) | — | NO SOURCE: vendor-hosted https://search.parallel.ai/mcp (documented, not scanned) |
| 11 | smithery `reddit` (remote-only, no repo) | — | NO SOURCE: remote-only (documented, not scanned) |
| 12 | smithery `slack` (remote-only, no repo) | modelcontextprotocol/servers src/slack | covered by #1 |
| 13 | mcpso #1 sequential-thinking 5.5K | smithery-ai/server-sequential-thinking | REPO NOT FOUND (remote-only listing); covered by modelcontextprotocol/servers src/sequentialthinking |
| 14 | mcpso #2 wcgw 4.9K | microsoft/wcgw | NOT FETCHED — full coding-agent repo, out of scope for egress-lane batch; noted |
| 15 | mcpso #5 @mzxrai/mcp-webresearch | mzxrai/mcp-webresearch | git shallow clone |
| 16 | mcpso #6 iterm-mcp 402 | ferrislucas/iterm-mcp | git shallow clone |
| 17 | mcpso #7 @kazuph/mcp-taskmanager | kazuph/mcp-taskmanager | git shallow clone |
| 18 | mcpso #8 mcp-server-sqlite-npx | npm tarball mcp-server-sqlite-npx@0.8.0 | curl + static unpack |
| 19 | mcpso #10 @smithery-ai/memory | modelcontextprotocol/servers src/memory | covered by #1 |
| 20 | mcpso #11 @executeautomation/playwright-mcp-server | executeautomation/mcp-playwright | git shallow clone (repo renamed from playwright-mcp-server) |
| 21 | mcpso #12 mcp-dice | — | NOT FOUND on npm or smithery API — tiny demo server, noted |
| 22 | mcpso #13 @wonderwhy-er/desktop-commander | wonderwhy-er/DesktopCommanderMCP | git shallow clone |
| 23 | mcpso #15 mcp-obsidian | npm tarball mcp-obsidian@1.0.0 | curl + static unpack |
| 24 | mcpso #16 @f4ww4z/mcp-mysql-server | f4ww4z/mcp-mysql-server | git shallow clone |
| 25 | mcpso #17 @burtthecoder/mcp-shodan | burtthecoder/mcp-shodan | git shallow clone |
| 26 | mcpso #18 @AudienseCo/mcp-audiense-insights | AudienseCo/mcp-audiense-insights | git shallow clone |
| 27 | bawbel top-100: clay-inc/clay-mcp | clay-inc/clay-mcp | git shallow clone |
| 28 | bawbel top-100: Supabase | supabase-community/supabase-mcp | git shallow clone |
| 29 | bawbel top-100: microsoft/learn_mcp | — | REPO NOT FOUND under microsoft/; listing appears stale — noted |
| 30 | bawbel top-100: agentmail | agentmail-to/agentmail-mcp | git shallow clone |
| 31 | bawbel top-100: blockscout/mcp-server | blockscout/mcp-server | git shallow clone |
| 32 | bawbel top-100: hamid-vakilzadeh/mcpsemanticscholar | hamid-vakilzadeh/mcpsemanticscholar | git shallow clone |
| 33 | bawbel top-100: adamamer20/paper-search-mcp-openai | adamamer20/paper-search-mcp-openai | git shallow clone |
| 34 | browser lane | microsoft/playwright-mcp | git shallow clone |
| 35 | search lane | mendableai/firecrawl-mcp-server | git shallow clone |
| 36 | automation lane | apify/actors-mcp-server | git shallow clone |
| 37 | productivity lane | makenotion/notion-mcp-server | git shallow clone |
| 38 | payments lane | stripe/agent-toolkit | git shallow clone |
| 39 | infra lane | cloudflare/mcp-server-cloudflare | git shallow clone (OAuth/token-handling focus) |
| 40 | db lane | neondatabase/mcp-server-neon | git shallow clone |
| 41 | code-exec lane | e2b-dev/mcp-server | git shallow clone |
| 42 | observability lane | getsentry/sentry-mcp | git shallow clone |

Remote-only (server-side opaque, no public source): smithery `gmail`, `googledrive`,
`googlesheets`, `reddit`, `slack`, `jina`, `brave`, `exa`, `Tavily`,
`parallel/search`, `context7`(@upstash), `sequential-thinking`(@smithery-ai),
`github`(bySmithery). Where an upstream public repo exists it was scanned as proxy.

### Batch-2 additions (resume session, 2026-10-05 — prioritized by task list: network tools,
tunnels, configurable endpoints/callbacks, telemetry beacons, update checks, OAuth/token handling)

| # | marketplace rank / listing | source fetched | how |
|---|---|---|---|
| 43 | mcp.so #7 LocalCan (82 installs) | localcan/localcanapp | git shallow clone — tunnel primitive: public URLs for localhost, traffic inspector, agent MCP server |
| 44 | PulseMCP #4 Browser Use (1.1M/wk) | browser-use/browser-use | git shallow clone — browser agent via third-party relay API |
| 45 | PulseMCP #2 Chrome DevTools (3.1M/wk) | ChromeDevTools/chrome-devtools-mcp | git shallow clone — official Chrome control |
| 46 | npm @bitwarden/mcp-server | bitwarden/mcp-server | git shallow clone — vault access (OAuth/token-handling focus) |
| 47 | npm kubernetes-mcp-server | containers/kubernetes-mcp-server | git shallow clone — infra |
| 48 | npm @runpod/mcp-server | runpod/runpod-mcp | git shallow clone — GPU cloud |
| 49 | npm @heroku/mcp-server | heroku/heroku-mcp-server | git shallow clone — platform |
| 50 | PulseMCP #24 Grafana (129K/wk) | grafana/mcp-grafana | git shallow clone — observability/telemetry beacon |
| 51 | PulseMCP #20 MongoDB (139K/wk) | mongodb-js/mongodb-mcp-server | git shallow clone — db |
| 52 | mcp.so #1 Medplum (2.5K installs) | medplum/medplum | git shallow clone — healthcare FHIR (large monorepo) |
| 53 | mcp.so featured Gologin MCP | gologinapp/gologin-mcp | git shallow clone — proxies/fingerprints/browser profiles |
| 54 | PulseMCP #7 Telnyx (390K/wk) | team-telnyx/telnyx-mcp-server | git shallow clone — voice/SMS telecom |
| 55 | mcp.so #2 Atomic Mail Agentic (255 installs) | Atomic-Mail/atomic-mail-agentic | git shallow clone — autonomous email read/send/react |
| 56 | OneSignal (smithery 22K useCount) | WeirdBrains/onesignal-mcp | git shallow clone — community proxy for official OneSignal MCP (push notifications) |

Remote-only, no public source (documented, not scanned): `anon.li` (cursor.directory 3.2k;
vendor-hosted OAuth MCP per anon.li homepage — aliases + encrypted file shares + forms),
smithery `pipeworx/gateway` (419K useCount), `henry-ships/sparkforge` (220K),
`creativelead/unclick`, `getgapup/gapup-mcp`, `WeRead Finance` (Cloudflare Workers remote).

## Scan results

(TBD — scanner run in progress at time of writing; results land in raw/scan-c.json.)

### Egress hits by severity

TBD

### Top-5 riskiest

TBD

### Hunt-corpus toolkit matches

TBD — watchlist: `r.jina.ai`, `webhook.site`/`discord.com/api/webhooks`/`hooks.slack.com`,
`httpbun.com`/`httpbin.org`, `uploads.github.com`, `ngrok`/`cloudflared`/`localtunnel`,
`verify=False`, epoch nonces (`?x=17…`), `zz` path labels, `oai-`/`zz-` identifiers,
`A000`/`ZZEND` markers.

## Caveats

- The scanner is regex/static: grades are `confirmed` (bytes present) vs `pattern-match`
  (corpus grammar). A high score is dual-use surface, not an accusation.
- Remote-only top listings dominate current Smithery usage; their server-side code cannot
  be scanned — the scan covers what a self-hoster would actually run.
- `wcgw` (microsoft) excluded: full coding-agent repo, outside this lane's batch scope.
- `microsoft/learn_mcp` and `maximumsats/maximumsats` repos not found (listings stale/renamed).
- `mcp-dice` not found on npm or the Smithery API.
