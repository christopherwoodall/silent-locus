# Known-URL Hunt — New Batches (skill-egress-top1000)

Worker: KNOWN-URL. Date: 2026-10-05.
Scope: the KNOWN egress-URL set from the top-500 study (EGRESS_MAP.md top-10 + corpus-verdict table),
hunted across the NEW scan batches only — scan-d1.json (lane-f1, 46 Claude-skill repos, 1,772 units),
scan-d2.json (lane-f2, 88 MCP repos, 304 units), scan-d3.json (lane-f3, 59 triaged repos, 343 units),
scan-f1.json (lane-h1, 16 marketplace, 27 units), scan-f2.json (lane-h2, 51 marketplace, 44 units).
Method: case-insensitive text search over each scan unit's `hits[].match` (actual matched bytes) and
`hits[].file` path — NOT the scanner's `pattern`/`note` fields (those contain the scanner's own regex
text and contaminate counts; a first pass over all fields was discarded for this reason).
Ambiguous hits were verified by reading file:line in the staged sources under
`~/workspace/skill-egress-work-1000/lane-{f1,f2,f3,h1,h2}/`.
Static analysis only. No code executed, no URL probed.

Grades follow the study schema: confirmed (bytes present) / pattern-match (corpus tradecraft grammar).
"Runtime" = executable code path that performs the egress; "docs" = markdown/docs/examples;
"test" = test fixtures. Dual-use surface on legitimate tools is NOT an accusation.

## Verdict table

| # | Hunt item | Verdict | Skills w/ bytes | Role of hits |
|---|-----------|---------|-----------------|--------------|
| 1 | ngrok | CONFIRMED | 18 | docs/dev-reference/tutorial only — NO agent-driven tunnel launch found |
| 2 | cloudflared | CONFIRMED | 12 | docs/dev-reference/tutorial only |
| 3 | r.jina.ai | CONFIRMED | 6 | **runtime code in 2 skills** (keyless fallback + keyed fetch) |
| 4 | jina.ai (bare, non-r.) | ABSENT | 0 | subsumed by r.jina.ai |
| 5 | discord.com/api/webhooks | CONFIRMED | 4 | **runtime notifier in 1 skill** (aiohttp POST), config/docs/test elsewhere |
| 6 | hooks.slack.com | CONFIRMED | 13 | **runtime notifiers in 2 skills**, tests/docs elsewhere |
| 7 | uploads.github.com | CONFIRMED | 3 | **runtime release/pack-asset upload code in 2 skills**, docs in 1 |
| 8 | user-attachments (gitshot grammar) | CONFIRMED | 36 | docs image-embeds (`github.com/user-attachments` URLs); no upload-to-API code found in sampled skills |
| 9 | catbox.moe | ABSENT (signature mention only) | 0 | single staged-file hit is a YARA detection signature `$ = "files.catbox.moe"` (malware-staging indicator), not skill usage |
| 10 | litterbox | ABSENT (name collision) | 0 | "litterbox" = BlackSnufkin-LitterBox, a malware-analysis sandbox skill; NOT the catbox.moe temp-file service |
| 11 | sci-hub.se | **CONFIRMED (scanner miss)** | **1** | **runtime MCP tools** in openags-paper-search-mcp — scan JSON recorded 0 hits because the unit was scoped to the `claude-code` subdirectory |
| 12 | webhook.site | CONFIRMED (bytes) | 8 | docs/test/OOB-testing/blocklist/analysis-comments only — **no live dead-drop POST code** |
| 13 | httpbun.com | ABSENT | 0 | 0 hits in all 5 batches |
| 14 | httpbin | CONFIRMED | 12 | docs/teaching examples only (pattern-match benign, as in top-500) |
| 15 | bitwarden | ABSENT (incidental mentions) | 0 | mentions only: supabase CONTRIBUTING.md ("Download the `domain-verification-key.pem` from Bitwarden"), OpenMausBot ChatView.swift UI copy ("Use Apple Passwords, 1Password, Bitwarden, or paste"), taielab starred-repo lists, zoocode vendored sourcemap — NO Bitwarden MCP/vault integration like top-500's bitwarden/mcp-server |
| 16 | localcan | ABSENT (substring FPs) | 0 | staged-file hits are `localCandidates`/`localCandidate` identifier substrings (MCPJam-inspector, generalaction-emdash) and vendored monaco-editor noise — NOT the LocalCan tunnel service |
| 17 | roamzy | ABSENT | 0 | 0 staged-file hits across all 5 lanes |
| 18 | verify=False | CONFIRMED | 18 | detection-catalog/test/docs occurrences; NO runtime TLS-bypass fetch found in sampled hits |
| 19 | --insecure | CONFIRMED | 9 | detection-catalog/docs/localhost-devtooling; no production TLS-bypass code |
| 20 | NODE_TLS_REJECT_UNAUTHORIZED | CONFIRMED | 3 | troubleshooting docs + remediation guidance (one doc instructs REMOVING it) |
| 21 | go-import meta tags | ABSENT | 0 | 2 natural-language mentions only (go.mod comment, CHANGELOG prose) |
| 22 | epoch nonces (`?x=1…`/`t=1…`) | ABSENT | 0 | 0 hits in all 5 batches |
| 23 | zz labels | ABSENT (pattern mismatch) | 0 | matched `zz_` strings are developer test probes (`zz_planted_pool`, `zz_probe`, `zz_bare_import_probe`), NOT corpus zz=oai labels |
| 24 | A000 | ABSENT (pattern mismatch) | 0 | matched bytes are CSS hex colors (#A000…) in vendored monaco-editor, DLL binary noise, and a session-fixture token |
| 25 | ZZEND | ABSENT | 0 | 0 hits in all 5 batches |
| 26 | api.telegram.org/bot | CONFIRMED | 11 | **runtime send code in 1 skill** (whale-alert monitor), config/validation in 1, docs/teaching elsewhere |
| 27 | smtp/sendmail | CONFIRMED | 47 | docs/config/diagrams/env; no runtime send library found in sampled skills |
| 28 | JMAP | ABSENT | 0 | 0 hits in all 5 batches |

## Per-item evidence (all excerpts ≤200 chars, observed bytes)

### 1. ngrok — CONFIRMED, 18 skills, docs/dev-reference only
No skill in the new batches wires agent-driven ngrok exposure (contrast top-500's loki-mode/telnyx-mcp).
Sampled hits are markdown docs, .env.example comments, troubleshooting, CTF tutorials:
- `lane-f1/jeremylongshore-tons-of-skills-marketplace/plugins/saas-packs/fathom-pack/skills/fathom-webhooks-events/SKILL.md:120` — "# Test with webhook.site … Or use ngrok for local testing / ngrok http 5000" (docs)
- `lane-f1/ljagiello-ctf-skills/ctf-web/client-side.md:504` — "### Step 4 — Host exploit and tunnel / cloudflared tunnel --url http://localhost:8888" (pentest tutorial; also has ngrok mentioned adjacent)
- `lane-f1/tech-leads-club-agent-skills/packages/skills-catalog/skills/(cloud)/cloudflare-deploy/references/tunnel/gotchas.md:136` — "From Ngrok / # Ngrok: ngrok http 8000 / # Cloudflare Tunnel:" (migration docs)
- `lane-f2/jnMetaCode-agency-orchestrator/agency-agents/engineering/engineering-feishu-integration-developer.md:567` — "Deploy to a publicly accessible environment (or use tunneling tools like ngrok for local development)" (agent instructions, dev-only)
- `lane-f2/crbnos-carbon/apps/erp/vite.config.ts:135` — `".ngrok-free.app", ".ngrok-free.dev", ".trycloudflare.com"` in `allowedHosts` (dev server config)
- `lane-f2/inkeep-agents/.env.example:217` — "# SLACK_APP_URL=https://your-app.ngrok.app" (config comment)
Greps over `*.py|*.js|*.ts|*.go|*.sh` in sampled skill dirs returned zero ngrok references in runtime code.

### 2. cloudflared — CONFIRMED, 12 skills, docs/dev-reference only
- `lane-f1/ljagiello-ctf-skills/ctf-web/client-side.md:506` — "```bash / # Cloudflare Tunnel (recommended — no interstitial pages unlike ngrok) / cloudflared tunnel --url http://localhost:8888 / python3 -m http.server 8888 / ```" (pentest tutorial)
- `lane-f3/get-bb-bb/examples/plugins/slack-bot/README.md:53` — "Slack must be able to reach your BB server (use a tunnel such as `cloudflared` or `ngrok` for a local server)." (plugin docs)
- `lane-f3/omnigent-ai-omnigent/deploy/README.md:128` — "| Share a server running on your **laptop**: demo it to teammates, or let remote runners & cloud sandboxes connect back to it (nothing to deploy) | Cloudflare quick tunnel | `cloudflared tunnel --url" (deployment docs)
- `lane-f1/tech-leads-club-agent-skills/packages/skills-catalog/skills/(cloud)/cloudflare-deploy/references/hyperdrive/configuration.md:116` — cloudflared config reference (docs)

### 3. r.jina.ai — CONFIRMED, 6 skills, RUNTIME in 2
- `lane-f2/glidea-zenfeed/pkg/util/crawl/crawl.go:152` (runtime): `proxyURL := "https://r.jina.ai/" + u` inside `func (c *jina) Markdown(...)`; constructor comment: "If token is empty, will not affect to use, but rate limit will be lower." — a keyless fallback crawler, the exact corpus tradecraft grammar from the top-500 verdict.
- `lane-f2/Prismer-AI-PrismerCloud/sdk/cloud/catalog/skills/prismer-blocked-page-recovery/scripts/recover_page.py:59` (runtime): `SERVICE_HOSTS = {'archive.org', 'web.archive.org', 'r.jina.ai', *ARCHIVE_TODAY_HOSTS}`; `:218` `def try_jina(url: str, timeout: int)` fetches `"https://r.jina.ai/" + url` with `JINA_API_KEY` (gated — returns None without key, so keyed not keyless here).
- `lane-f2/heymrun-heym/frontend/frontend/src/docs/content/nodes/http-node.md:59` (docs), `lane-f2/taielab-awesome-hacking-lists/README.md:11809` (docs), backnotprop-plannotator (docs).
Grade: confirmed (bytes present); glidea-zenfeed = pattern-match on the corpus keyless-fetch tradecraft.

### 4. jina.ai (bare) — ABSENT
Every `jina.ai` match contains `r.jina.ai`; no bare-domain hits.

### 5. discord.com/api/webhooks — CONFIRMED, 4 skills, RUNTIME in 1
- `lane-f1/jeremylongshore-tons-of-skills-marketplace/plugins/crypto/whale-alert-monitor/commands/monitor-whales.md:702` (runtime): `async def _send_discord(self, transaction: WhaleTransaction, analysis: Dict, config: Dict) -> None:` / `"""Send Discord webhook notification."""` / `webhook_url = config['webhook_url']` / `async with aiohttp.ClientSession() as session:` `async with session.post(webhook_url, json=payload) as response:` — full alert notifier; config schema at :140 shows `"webhook_url": "https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN"`. The skill instructs an agent to monitor crypto whale transactions and POST embeds to a configured Discord webhook URL (also has `_send_slack` and Telegram `sendMessage` in the same file).
- `lane-f3/builderz-labs-mission-control/src/lib/__tests__/scan-credentials.test.ts:140` (test fixture)
- `lane-f2/heymrun-heym/frontend/frontend/src/components/Credentials/CredentialDialog.vue:2400` (n8n-style node credential UI listing)
- `lane-f2/nitrocloudofficial-nitrostack/sample-apps/Aide/README.md:52` (docs)

### 6. hooks.slack.com — CONFIRMED, 13 skills, RUNTIME in 2
- `lane-f3/rullerzhou-afk-clawd-on-desk/src/slack-notify-client.js:280` (runtime): `const res = await doFetch(url, { method: "POST", headers: { "content-type": "application/json; charset=utf-8", ...headers }, body: JSON.stringify(bodyObject), // The webhook host is pinned to hooks.slack.com, but a redirect would / let the response move the request ... to an arbitrary host. ... treat one as a hard failure instead of following. / redirect: "error",` — a hardened Slack-webhook notifier client (agent completion notifications), docs at `docs/guides/slack-notifications.md:139`.
- `lane-f1/jeremylongshore-tons-of-skills-marketplace/plugins/crypto/whale-alert-monitor/commands/monitor-whales.md` — `_send_slack` sibling of `_send_discord` (runtime; same file as above).
- Test/docs/examples elsewhere: `lane-f2/inkeep-agents/agents-api/src/__tests__/manage/routes/crud/webhookDestinations.test.ts:746` (test, fake `T00000000` URL), `lane-f1/samber-cc-skills-golang/skills/golang-samber-slog/references/backend-handlers.md:171` (docs: `WebhookURL: "https://hooks.slack.com/services/..."`), `lane-f3/FailproofAI-failproofai/__tests__/hooks/semantic/redaction.test.ts:1283` + `docs-old/*/examples.mdx:156` (tests/docs), `lane-f3/builderz-labs-mission-control/src/components/panels/webhook-panel.tsx:542` (UI input placeholder), `lane-f3/mvschwarz-openrig/packages/daemon/test/slack-api.test.ts` (tests), `lane-f3/Observal-Observal/tests/` (tests), `lane-h2/vsc-zoocodeorganization-zoo-code/extension/assets/marketplace/modes.yml:4350` (custom-tool tutorial docs).

### 7. uploads.github.com — CONFIRMED, 3 skills, RUNTIME in 2
- `lane-f2/777genius-agent-teams-ai/scripts/ci/release/github.ts:304` (runtime): `async upload(repository: string, releaseId: number, file: string)` → `await command(['api', \`https://uploads.github.com/repos/${repository}/releases/${releaseId}/assets?name=${encodeURIComponent(path.basename(file))}\`, ...` (release-asset upload pipeline)
- `lane-f3/FailproofAI-failproofai/src/hooks/pack-cli.ts:2035` (runtime): `const GITHUB_UPLOADS = process.env.FAILPROOFAI_GITHUB_UPLOADS ?? "https://uploads.github.com";` (pack asset upload target)
- `lane-f2/Prismer-AI-PrismerCloud/sdk/cloud/catalog/skills/prismer-github/references/github-api-cheatsheet.md:110` (docs: "Upload asset | POST | `https://uploads.github.com/repos/{owner}/{repo}/releases/{id}/assets?name={filename}`")

### 8. user-attachments — CONFIRMED, 36 skills, docs image-embeds
All sampled hits are `github.com/user-attachments` image URLs embedded in READMEs/docs (no API-upload code found in sampled skills): e.g. `lane-f2/zinja-coder-jadx-ai-mcp/README.md`, `TROUBLESHOOTING.md`; BlackSnufkin-LitterBox README images. The gitshot grammar (programmatic upload to user-attachments) is NOT observed here — pattern-match on image-host URLs only.

### 9. catbox.moe — ABSENT
0 hits in all 5 scan JSONs (searched `match`+`file` fields).

### 10. litterbox — ABSENT as egress URL (name collision)
All 65 hits are inside the skill `BlackSnufkin-LitterBox` (lane-f2), whose `GrumpyCats/litterbox_client/__init__.py:1` says: "Python client for the LitterBox payload-analysis sandbox API." It is a malware-analysis sandbox skill, not the catbox.moe temporary-file service. No litterbox.catbox.moe endpoint observed.

### 11. sci-hub.se — CONFIRMED, 1 skill, RUNTIME (scanner miss — see methodology note)
The scan JSONs recorded 0 hits, but the string is present in staged source the scan unit never covered:
- `lane-f2/openags-paper-search-mcp/paper_search_mcp/server.py:1147` (runtime): `async def download_scihub(` / `identifier: str,` / `save_path: str = "./downloads",` / `base_url: str = "https://sci-hub.se",` / `"""Download paper PDF via Sci-Hub (optional fallback connector).` — an MCP tool downloading paper PDFs via Sci-Hub with `https://sci-hub.se` as the DEFAULT mirror.
- `lane-f2/openags-paper-search-mcp/paper_search_mcp/server.py:1173` (runtime): `async def download_with_fallback(` … `use_scihub: bool = False,` / `scihub_base_url: str = "https://sci-hub.se",` / `"""Try source-native download, OA repositories, Unpaywall, then optional Sci-Hub.` (Sci-Hub fallback disabled by default)
- tests: `tests/test_sci_hub.py`, `tests/test_fallback.py` (test)
Grade: confirmed (bytes present); paywall-bypass primitive mirroring the top-500's paper-search-mcp-openai finding, in a different skill.

### 12. webhook.site — CONFIRMED bytes, 8 skills, NO live dead-drop code
Present (a change from top-500, where it was ZERO across all 3,853 units), but every hit is docs/test/reference, not runtime exfil:
- `lane-f1/jeremylongshore-tons-of-skills-marketplace/plugins/saas-packs/fathom-pack/skills/fathom-webhooks-events/SKILL.md:116` — "```bash / # Test with webhook.site / curl -X POST https://webhook.site/your-uuid \\" (docs; same file also teaches `ngrok http 5000`)
- `lane-f2/Vexa-ai-vexa/docs/docs/webhooks.mdx:40` — docs recount a 2026-07-19 production walk that "delivered `meeting.status_change`, `meeting.completed` and `bot.failed` to an external `webhook.site` endpoint" (their own test inbox; "Live delivery — proven" at :118)
- `lane-f1/ljagiello-ctf-skills/ctf-web/auth-jwt.md:74` — CTF tutorial: "POST to webhook.site or attacker server" for JKU injection (teaching)
- `lane-f3/awarexone-Agentic-Bug-Hunter/bughunter/agents/chain-builder.md:68` + `bughunter/mcp/burp-mcp-client/README.md:91` — "For OOB testing, suggest Interactsh (`interactsh-client`) or webhook.site" (bug-hunting methodology)
- `lane-f1/samber-cc-skills-golang/skills/golang-samber-slog/references/backend-handlers.md:202` — docs placeholder `Endpoint: "https://webhook.site/your-id"` (example)
- `lane-f1/tech-leads-club-agent-skills/packages/skills-catalog/skills/(cloud)/cloudflare-deploy/references/pages-functions/patterns.md:15` — docs sample `fetch('https://webhook.site/...', { method: 'POST' })` (example)
- `lane-f2/crbnos-carbon/packages/auth/src/services/self-signup-blocked-domains.txt:8347` — webhook.site sits in a self-signup **blocked-domains** list (counter-pattern: treated as abusable)
- `lane-f2/CYB3RMX-Qu1cksc0pe/Modules/vba_emulator/scoring.py:175` — malware-analysis heuristic comment: "the actual C2/exfil happened inside the spawned batch script (schtasks persistence, webhook.site exfil via a data: URI)" (analysis of a real sample, not agent exfil)

### 13. httpbun.com — ABSENT
0 hits in all 5 scan JSONs.

### 14. httpbin — CONFIRMED, 12 skills, docs/teaching only (benign, as in top-500)
- `lane-f1/jeremylongshore-tons-of-skills-marketplace/plugins/productivity/cli-power-skills/skills/api-testing/SKILL.md:99` — `httpbin.org` (teaching)
- `lane-f1/himself65-finance-skills/plugins/skill-creator/skills/skill-creator/references/dynamic-calling.md:422` (teaching)
- `lane-f2/Prismer-AI-PrismerCloud/sdk/cloud/docs/typescript-samples.ts:53` (sample code)
- `lane-f2/crbnos-carbon/.claude/skills/agent-browser/references/proxy-support.md:155` (docs)
- others: `A9T9-RPA`, `OpenAgentPlatform-Dive`, `circleci-public-mcp-server-circleci`, `fengshao1227-ccg-workflow`, `get-bb-bb`, `omnigent-ai-omnigent`, `silexlabs-Silex`, `nitrocloudofficial-nitrostack/sample-apps/domainexpansion` — all docs/example contexts per scan metadata.

### 15. bitwarden — ABSENT
0 hits in all 5 scan JSONs.

### 16. localcan — ABSENT
0 hits in all 5 scan JSONs.

### 17. roamzy — ABSENT
0 hits in all 5 scan JSONs.

### 18. verify=False — CONFIRMED, 18 skills, NO runtime TLS-bypass fetch found in sampled hits
Sampled occurrences are detection-catalogs, tests, docs, and one commented-out teaching line:
- `lane-f3/Gentleman-Programming-gentle-ai/internal/reviewtransaction/risk_dangerous_sink.go:25` — a security-review skill's detection catalog: `sink("TLS Python", ".py", "\\bverify\\s*=\\s*False\\b|\\bCERT_NONE\\b|\\bcheck_hostname\\s*=\\s*False\\b")` (this catalog is why the scanner flags many of these batches)
- `lane-f1/tech-leads-club-agent-skills/packages/skills-catalog/skills/(quality)/the-judge/references/review-standards.md:110` — code-review standard listing "TLS verification disabled (`rejectUnauthorized: false`, `verify=False`, `InsecureSkipVerify`)" as a bypass example (meta)
- `lane-f1/ljagiello-ctf-skills/ctf-web/python-requests.md:28` — `# sess.verify = False  # self-signed CTF only` (commented-out, teaching)
- `lane-f1/FreedomIntelligence-OpenClaw-Medical-Skills/skills/biomcp-server/repo/tests/tdd/test_connection_pool.py:63` — test parameterizing `verify=True` vs `verify=False` pool settings (test)
- `lane-f1/NVIDIA-skills/skills/amc-run-rtsp-calibration/SKILL.md:341` — `SSL_VERIFY` env var documented (docs)
- `lane-f1/jeremylongshore-tons-of-skills-marketplace/marketplace/src/data/skills-index.json:9872` — catalog index (metadata)
- `lane-f2/BlackSnufkin-LitterBox/GrumpyCats/litterbox_client/base.py:62` — matched `verify = False` (client code; full context not classified further)
No top-500-style `verify=False`-on-paywall-fetch runtime hit (cf. paper-search-mcp-openai/Sci-Hub) observed.

### 19. --insecure — CONFIRMED, 9 skills, docs/localhost-devtooling/detection-catalog
- `lane-f1/tech-leads-club-agent-skills/packages/skills-catalog/skills/(security)/security-best-practices/references/python-django-web-server-security.md:141` — "Search for `manage.py runserver`, `runserver 0.0.0.0`, `--insecure`." (detection guidance; Django's `runserver --insecure` flag, not TLS)
- `lane-f1/jeremylongshore-tons-of-skills-marketplace/plugins/ai-ml/ollama-local-ai/skills/ollama-setup/SKILL.md:74` — "retry with `ollama pull --insecure` behind corporate proxy" (docs)
- `lane-f2/inkeep-agents/package.json:78` — `"spicedb:schema:read": "zed schema read --insecure --endpoint localhost:50051 --token dev-secret-key"` (localhost dev tooling)
- `lane-f3/omnigent-ai-omnigent/justfile:59` — `cockroach sql --insecure --execute="SET CLUSTER SETTING ..."` (localhost dev DB)
- `lane-f3/Gentleman-Programming-gentle-ai/internal/reviewtransaction/risk_dangerous_sink.go:29` — detection catalog: `sink("TLS shell", ".sh .bash .zsh", "\\bcurl\\s+(?:[^;|]*\\s)?(?:--insecure|-k)(?:\\s|$)")` (meta)
- `lane-f3/FailproofAI-failproofai/CHANGELOG.md:681` (changelog mention)
Per the top-500 false-positive log, bare `--insecure` curl flags are not TLS-bypass evidence; nothing here contradicts that.

### 20. NODE_TLS_REJECT_UNAUTHORIZED — CONFIRMED, 3 skills, docs/remediation
- `lane-f1/jeremylongshore-tons-of-skills-marketplace/skills/.curated/detecting-weak-cryptography/references/PLAYBOOK.md:171` — "### Env var TLS bypass — REMOVE / ```bash / # Before — anywhere in startup scripts / export NODE_TLS_REJECT_UNAUTHORIZED=0 / # After: remove the line entirely / ```" (a pentest skill instructing REMOVAL — defensive)
- `lane-f1/jeremylongshore-tons-of-skills-marketplace/plugins/productivity/cli-power-skills/INSTALL.md:98` (troubleshooting docs)
- `lane-f1/foryourhealth111-pixel-Vibe-Skills/bundled/skills/error-resolver/patterns/network.md:442` — `NODE_TLS_REJECT_UNAUTHORIZED = '0` (error-resolver docs)
- `lane-f2/Azure-data-api-builder/docs/testing-guide/mcp-inspector-testing.md:13` (test docs)

### 21. go-import meta tags — ABSENT
The only 2 staged-file hits for the string "go-import" are natural-language mentions, not `<meta name="go-import">` canary tags:
- `lane-f3/awarexone-Agentic-Bug-Hunter/go.mod:1` — "// Canonical Go module path for this repository (matches GitHub's go-…"
- `lane-f3/awarexone-Agentic-Bug-Hunter/CHANGELOG.md:17` — "- **Go / Dependency Graph package identity** — add `go.mod` …"
RubyGems-era go-import canary pattern: absent.

### 22. epoch nonces — ABSENT
0 hits in all 5 scan JSONs. Direct fixed-string sweeps: `?x=17` zero occurrences in lane-f3/h1/h2; `?t=17` 4 occurrences, all Vite dev-server cache-busters in stack-trace test fixtures (e.g. `http://localhost:5173/src/CheckoutPage.tsx?t=17:40:7` — `?t=17` followed by `:40:7` line:col, not an epoch param). No `?x=1…`/`t=1[0-9]{9}` corpus-style nonces observed.

### 23. zz labels — ABSENT (pattern mismatch)
The 3 matched skills contain developer test-probe names, not corpus `zz=oai` labels:
- `lane-f2/Vexa-ai-vexa/scripts/gates.test.mjs:25` — `const TEST_FILE = "core/identity/services/admin-api/tests/test_zz_planted_pool.py";`
- `lane-f3/Gentleman-Programming-gentle-ai/odd/tasks/orchestrator-prompt-install.md:70` — "created+removed temp dir `internal/zz_probe` (nothing left)"
- `lane-h1/samuelgursky-davinci-resolve-mcp/CHANGELOG.md:3050` — "a probe at `resolve-advanced/server/tools/zz_bare_import_probe.mjs`"

### 24. A000 — ABSENT (pattern mismatch)
- `lane-f2/vsc-dbcode-dbcode/extension/out/vendor/monaco-editor/workers/css.worker.js:66` — CSS hex color `#A000…` in vendored editor code
- `lane-f2/vsc-ms-windows-ai-studio-windows-ai-studio/extension/ai-mlstudio/bin/System.Management.dll:14528` — binary noise
- `lane-f2/vsc-augment-vscode-augment/extension/common-webviews/assets/objective-cpp-BKm3FjjW.js:1` — minified bundle hash fragment
- `lane-f2/mohitagw15856-pm-claude-skills/examples/promoter/session-fixture.jsonl:2` — fixture token `a000`

### 25. ZZEND — ABSENT
0 hits in all 5 scan JSONs. A direct staged-source sweep found 2 files (`lane-f2/metatool-ai-metamcp/metamcp.svg`, `docs/images/metamcp.svg`) — both are `zZenD` fragments inside base64 image blobs, not markers.

### 26. api.telegram.org/bot — CONFIRMED, 11 skills, RUNTIME in 1
- `lane-f1/jeremylongshore-tons-of-skills-marketplace/plugins/crypto/whale-alert-monitor/commands/monitor-whales.md:753` (runtime): `url = f"https://api.telegram.org/bot{bot_token}/sendMessage"` / `payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}` via aiohttp (agent whale-alert → Telegram)
- `lane-f1/op7418-Claude-to-IM-skill/scripts/doctor.sh:305` (runtime validation): `TG_RESULT=$(curl -s --max-time 5 "https://api.telegram.org/bot${TG_TOKEN}/getMe" …)`; config at `config.env.example:45`: `CTI_TG_BOT_TOKEN=your-telegram-bot-token` / "Get it: send a message to the bot, then visit https://api.telegram.org/botYOUR_TOKEN/getUpdates"
- Teaching/docs elsewhere: `lane-f1/ljagiello-ctf-skills/ctf-malware/c2-and-protocols.md:135` ("Recover exfiltrated data via bot token" — malware-analysis tutorial using getUpdates/getFile), `lane-f2/mohitagw15856-pm-claude-skills/docs/ACTIVATION.md:22` (Telegram worker deploy docs), plus CYB3RMX-Qu1cksc0pe, builderz-labs-mission-control, eugeniughelbur-obsidian-second-brain, heymrun-heym, kyegomez-swarms, qixing-jk-all-api-hub per scan metadata.

### 27. smtp/sendmail — CONFIRMED, 47 skills, docs/config only in sampled hits
Sampled contexts: `lane-f1/tech-leads-club-agent-skills/packages/marketplace/src/data/skills.json:1068` (skill-catalog metadata), `lane-f1/ljagiello-ctf-skills/ctf-web/SKILL.md:52` + `ctf-forensics/SKILL.md:279` (docs), `lane-f1/samber-cc-skills-golang/skills/golang-samber-slog/SKILL.md:87` (docs), `lane-f2/crbnos-carbon/.env.example:40` (config), `lane-f2/Vexa-ai-vexa/clients/terminal/src/app/api/auth/README.md:11` (docs), `lane-f2/heymrun-heym/frontend/.../CredentialDialog.vue:368` (credential UI), `lane-f2/xpf0000-FlyEnv/docs/deepwiki/mailpit.md:12` (docs), `lane-f2/BlackSnufkin-LitterBox/Scanners/Yara/rules/...` (YARA rules mentioning SMTP in malware signatures). Targeted greps for `smtplib|nodemailer|sendmail(|PHPMailer|django.core.mail|net/smtp` in sampled skills returned no runtime send code.

### 28. JMAP — ABSENT
0 hits in all 5 scan JSONs. Direct staged-source hits for the substring are minified-JS/CSS noise (`toObjMap`, `zZ` identifiers in vendored weaviate-client.js, webview.js bundles, codicon.css) — not JMAP email.

## Notes & caveats
- First-pass counts over all scan fields were inflated by scanner-pattern contamination (the scanner's own regex text appears in `pattern`/`note`); the table above uses `match`+`file` only (actual observed bytes).
- For high-hit items (ngrok 548 hits, smtp 1,246 hits, user-attachments 320 hits) verification was sampled, not exhaustive; per-skill verdicts rest on spot-checked bytes plus scan-category metadata.
- **Scanner coverage gap (methodology finding):** `openags-paper-search-mcp`'s sci-hub.se runtime code was missed because the scan-d2 unit's `path` was the `claude-code` subdirectory — repo-root code (`paper_search_mcp/server.py`) was never scanned. Any subdirectory-scoped unit can hide repo-root egress; recommend re-scoping or flagging units whose path is not the repo root.
- Direct staged-source sweeps corroborated the ABSENT verdicts for: go-import (2 natural-language mentions only), zzend (base64 noise in SVGs), roamzy (0), jmap (minified-JS noise), localcan (identifier substrings), bitwarden (incidental mentions), catbox.moe (YARA signature mention only), epoch nonces (`?x=17` zero; `?t=17` hits are Vite cache-busters).
- Secrets: placeholder-shaped values only in quoted excerpts (YOUR_ID/YOUR_TOKEN, YOUR_BOT_TOKEN, your-telegram-bot-token in-file placeholder); no real credential material used or retained.
- Grade summary: confirmed (bytes present) on 17 of 28 items; 11 absent. Of the confirmed, runtime code paths observed for: r.jina.ai (glidea-zenfeed, Prismer), discord/slack webhooks + telegram (whale-alert-monitor), slack webhooks (rullerzhou-afk-clawd-on-desk), uploads.github.com (777genius, FailproofAI), sci-hub.se (openags-paper-search-mcp).
