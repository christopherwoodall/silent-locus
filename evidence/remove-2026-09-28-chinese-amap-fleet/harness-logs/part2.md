# LANE 1 (part 2/2): Agent-harness log/trace storage map

Research date: 2026-10-05. Sources: PUBLIC docs and public source code only.
Nothing installed, nothing run, no endpoints probed.
Scope: agents/infrastructure only. Claims without a cited source are marked INFERENCE or honest null.

---

## 1. Cline (VS Code extension, `saoudrizwan.claude-dev`)

| Item | Detail |
|---|---|
| Log / transcript storage | VS Code globalStorage for the extension id `saoudrizwan.claude-dev`, per-task folders: Windows `%APPDATA%/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/<taskId>/`, macOS `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/<taskId>/`, Linux `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/<taskId>/`. Each task dir holds `api_conversation_history.json` (full API messages incl. `tool_use`/`tool_result`), `ui_messages.json` (chat records), `task_metadata.json`, `context_history.json`. Sources: [chatwizard work plan](https://github.com/veverke/chatwizard/blob/HEAD/docs/done/work-plan-support-additional-ai-coding-extensions.md), [ai-data-extractor README](https://github.com/bawadou/ai-data-extractor/blob/HEAD/README.md) |
| Session state | VS Code workspaceState/globalState for prefs/task history; `.clinerules` / `.clineignore` / `cline_mcp_settings.json` and Memory Bank markdown files in the project. Source: [dwarvesf breakdown](https://github.com/dwarvesf/research/blob/HEAD/breakdown/cline.md) |
| Credential storage | API keys via VS Code Secrets API → OS credential manager (Windows Credential Manager etc.), NOT in files. Source: [privacy audit](https://medium.com/@yurenpai57/i-audited-3-ai-coding-tools-for-privacy-the-difference-is-100x-eac40010381f) |
| Telemetry | PostHog, anonymous, on by default; collects task start/finish, mode/tool usage, token counts, OS/IDE, UI activity — "conversation flow (without content)". Opt out in Cline settings; respects VS Code global telemetry setting. Sources: [Cline telemetry doc (mirror)](https://github.com/rikaaa0928/rikline/blob/HEAD/docs/more-info/telemetry.mdx), [Cline privacy policy (mirror)](https://github.com/opensvm/aingels/blob/HEAD/docs/PRIVACY.md) |
| Cloud dashboard | Honest null — none documented. Local-first extension. |
| Leak-by-default? | **PARTIAL.** Secrets: no (Secrets API is the one harness here that gets credential storage right). Prompts/file contents: **yes** — `api_conversation_history.json` persists the complete API message array incl. `tool_result` payloads in plaintext JSON on disk by default; INFERENCE (grounded on the file capturing full tool I/O): anything the user pastes (keys, tokens, secrets) is written verbatim to these files and survives uninstall (the audit found 19 project dirs / 43MB of conversation data left behind). |

## 2. Continue (IDE extension / hub)

| Item | Detail |
|---|---|
| Log / transcript storage | `~/.continue/` on all platforms. Sessions: `~/.continue/sessions/*.json` (one JSON per session). Config: `~/.continue/config.json`. Index/cache under `~/.continue/index` (INFERENCE from documented `disableIndexing` setting). Sources: [ai-data-extractor README](https://github.com/bawadou/ai-data-extractor/blob/HEAD/README.md), [mindjack](https://github.com/nn1626/mindjack), [hardening-ia guide](https://github.com/dandgabr/hardening-ia/blob/HEAD/docs/tools/continuedev/continue/continue.md) |
| Session state | Same `~/.continue/` tree; LLM/API config in `config.json`. Docs page for session file layout: honest null (no official schema doc found in search). |
| Telemetry | PostHog anonymous usage events (default ON) + Sentry error reports. Docs say: accept/reject of suggestions (never code/prompt), model + command names, token counts, OS/IDE, pageviews. Opt out: `allowAnonymousTelemetry: false` in `~/.continue/config.json` or uncheck "Continue: Telemetry Enabled" in VS Code settings. Sources: [official telemetry doc (mirror)](https://github.com/teslamotors/continue/blob/HEAD/docs/docs/telemetry.md), [agent-snitch-list audit](https://github.com/pwchiefy/agent-snitch-list/blob/HEAD/tools/continue.md) |
| Cloud dashboard | Honest null — none documented for default local usage. (Continue Hub exists as a product; session-sync behavior not established from consulted docs.) |
| Leak-by-default? | **PARTIAL.** `~/.continue/sessions/*.json` stores full session content in plaintext on disk by default (prompts, responses, tool results — grounded on extractors parsing them). Telemetry itself excludes code/prompts per docs. No cloud sync by default (INFERENCE — nothing in the telemetry doc or opt-out flow sends transcripts off-box). No dedicated secrets file; API keys live in `~/.continue/config.json` in plaintext (INFERENCE from config-file model, standard for the project). |

## 3. Gemini CLI

| Item | Detail |
|---|---|
| Log / transcript storage | `~/.gemini/` on all platforms (override via `GEMINI_CLI_HOME`). Per-project temp dirs keyed by project-root hash: `~/.gemini/tmp/<project_hash>/chats/<session>.jsonl` (prompts, responses, tool inputs/outputs, token usage, sessionId; retention via `general.sessionRetention`, 30d default), `~/.gemini/tmp/<project_hash>/checkpoints/` (conversation + pending tool call), `~/.gemini/tmp/<project_hash>/shell_history` (official docs: project-specific shell command history), `~/.gemini/tmp/<project_hash>/logs.json` (append-only prompt log — community-sourced, unverified). Also `~/.gemini/history/`, `projects.json`, `state.json`, `installation_id`. Sources: [elevenpowers research card](https://github.com/satyamsingh-git/elevenpowers/blob/HEAD/docs/research/hosts/gemini-cli.md), [podium harness reference](https://github.com/madeinorbit/podium/blob/HEAD/docs/agent-harness-reference/gemini.md), [geminicli.com configuration docs](https://geminicli.com/docs/reference/configuration/), [rice-aise tool registry](https://github.com/moabualruz/rice-aise/blob/HEAD/docs/tool-registry-reference.md) |
| Session state | `settings.json`, `trustedFolders.json`, `GEMINI.md`, `extensions/`, `mcp-oauth-tokens.json` (auto-managed MCP OAuth tokens). Source: [rice-aise tool registry](https://github.com/moabualruz/rice-aise/blob/HEAD/docs/tool-registry-reference.md) |
| Credential storage | `~/.gemini/oauth_creds.json` (Google OAuth refresh token, file mode 0600 per operator observation), `~/.gemini/google_accounts.json` (account info); API key via `GEMINI_API_KEY` env or `.env`. Sources: [karl-infra gemini-cli notes](https://github.com/karlmarx/karl-infra/blob/HEAD/infra/gemini-cli.md), [rice-aise tool registry](https://github.com/moabualruz/rice-aise/blob/HEAD/docs/tool-registry-reference.md) |
| Telemetry | OpenTelemetry: `telemetry.enabled`, `target: local|gcp`, `otlpEndpoint`, `useCollector`, `outfile` (e.g. `GEMINI_TELEMETRY_OUTFILE` writes spans/logs/metrics to one file), **`logPrompts` defaults to true**; `privacy.usageStatisticsEnabled` for usage stats. Events: `gemini_cli.api_request/api_response` (token counts), `gemini_cli.tool_call`, `gemini_cli.agent.start|finish`, compression events. Sources: [Gemini CLI telemetry doc (mirror)](https://github.com/ashwin3919/gemini-cli-exp/blob/HEAD/docs/cli/telemetry.md), [geminicli.com configuration docs](https://geminicli.com/docs/reference/configuration/), [tokenusage source gate](https://github.com/gvastethecreator/tokenusage/blob/HEAD/docs/source-gates/GEMINI-CLI.md) |
| Cloud dashboard | When `target: gcp`, telemetry lands in Google Cloud Console (Cloud Trace / Monitoring / Logging). No per-user Google-hosted session-history dashboard by default — honest null beyond GCP console. |
| Leak-by-default? | **YES.** Three compounding defaults: (1) `logPrompts` defaults to true — prompt/response content goes into OTel log spans, and token metrics carry session id, installation id, email, auth type (source: tokenusage gate); (2) full chat transcripts incl. tool inputs/outputs persisted as `tmp/<project_hash>/chats/*.jsonl` in plaintext; (3) Google OAuth refresh token in plaintext `oauth_creds.json` (0600, still file-based, exfiltable by anything with user-level read). |

## 4. Codex CLI (OpenAI)

| Item | Detail |
|---|---|
| Log / transcript storage | `CODEX_HOME` (default `~/.codex/`; all platforms, no XDG). Sessions: `~/.codex/sessions/**/<date>/rollout-*.jsonl` — full session rollouts (user prompts, tool calls, token counts, rate-limit records). `history.jsonl` (if history persistence enabled), `log/`, SQLite state DB (per tool-registry inventory). Sources: [official Codex docs — Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced) (L112–122), [toknado README](https://github.com/kaantufan/toknado), [rice-aise tool registry](https://github.com/moabualruz/rice-aise/blob/HEAD/docs/tool-registry-reference.md) |
| Session state | `config.toml` (user) + `.codex/config.toml` (project, trust-gated), `hooks.json`, `AGENTS.md`, `skills/`, `plugins/`. Telemetry keys (`otel`, `notify`, provider keys) are IGNORED in project-local `.codex/config.toml` and only read from user-level `~/.codex/config.toml`. Source: [official docs](https://learn.chatgpt.com/docs/config-file/config-advanced) (L138–159) |
| Credential storage | `~/.codex/auth.json` (OAuth id/access/refresh tokens, ChatGPT login) when file-based storage is used; alternative: OS keyring when `auth_credentials_store_mode = "keyring"`. Source: [official docs](https://learn.chatgpt.com/docs/config-file/config-advanced) (L112–122), [rice-aise tool registry](https://github.com/moabualruz/rice-aise/blob/HEAD/docs/tool-registry-reference.md) |
| Telemetry | Two channels. (a) **OTel log export — opt-in, off by default**: `[otel] exporter = "none"` default; `log_user_prompt = false` redacts prompt content unless explicitly enabled; events `codex.conversation_starts`, `api_request`, `sse_event`, `websocket_request`, `user_prompt` (length only by default), `tool_decision`, `tool_result` (duration, success, **output snippet**). (b) **Anonymous usage/health metrics — ON by default**: "Codex periodically sends a small amount of anonymous usage and health data back to OpenAI", no PII claimed, independent of OTel export; opt out with `[analytics] enabled = false` in `~/.codex/config.toml`. Secondary source note: repo source defaults the metrics exporter to Statsig OTLP pointed at `https://ab.chatgpt.com/otlp/v1/metrics` (per [volli-code research](https://github.com/hussainph/volli-code/blob/HEAD/docs/research/competitor-agent-observability.md), citing `openai/codex` `codex-rs/core/src/config/otel.rs`). Source: [official docs](https://learn.chatgpt.com/docs/config-file/config-advanced) (L560–608, L660–675) |
| Cloud dashboard | Honest null — no documented hosted history view for the CLI itself. (ChatGPT web Codex is a separate product surface, out of scope.) |
| Leak-by-default? | **YES.** `rollout-*.jsonl` files persist complete prompts and tool results in plaintext JSONL by default (third-party tools parse full conversation content from them); `auth.json` holds OAuth tokens in plaintext by default unless keyring mode is enabled. Note: `shell_environment_policy.ignore_default_excludes` defaults to `true`, so env vars containing KEY/SECRET/TOKEN are NOT auto-excluded from tool environment — INFERENCE (from docs wording) that secrets in the environment can reach tool executions. |

## 5. OpenHands

| Item | Detail |
|---|---|
| Log / transcript storage | Two generations: (a) **Local GUI / Docker**: `~/.openhands/` persistence dir (Docker mounts host `~/.openhands` into the container) — settings, secrets, conversation data. (b) **Agent Server / Agent Canvas**: conversations at `~/.openhands/agent-canvas/conversations` (`OH_CONVERSATIONS_PATH` default), bash-event history at `~/.openhands/agent-canvas/bash_events`, workspaces at `~/.openhands/workspaces`, memory at `~/.openhands/memory/MEMORY.md`. V1 event persistence: `{persistence_dir}/{user_id}/v1_conversations/{conversation_id}/{event_id_hex}.json` + `meta.json` (zip exports of the same). Sources: [home-k8s deployment guide](https://github.com/dbirks/home-k8s/blob/HEAD/k8s-deployment-guide.md), [agent-canvas migration issue](https://github.com/openhands/agent-canvas/issues/1054), [elevenpowers card](https://github.com/satyamsingh-git/elevenpowers/blob/HEAD/docs/research/cards/openhands.md), [cl-adapter README](https://github.com/dmore/cl-agent-continual-learning-substrate-for-coding-agents/blob/HEAD/adapters/openhands/README.md) |
| Session state | `settings.json`, `secrets.json` (file store; `OH_SECRET_KEY` enables encryption — absent the key they are plaintext files, INFERENCE from the "secret for settings/secrets encryption" framing), conversation metadata + `base_state.json` + event files per conversation. Source: [agent-canvas migration issue](https://github.com/openhands/agent-canvas/issues/1054) |
| Credential storage | `~/.openhands/auth/` — user-scoped OAuth credential files (e.g. `openai_oauth.json`) in plaintext JSON (deployment guidance explicitly warns against leaving OAuth refresh tokens in agent workspaces: [opensymphony analysis](https://github.com/kumanday/opensymphony/blob/HEAD/docs/openhands_agent_server_subscription_auth_analysis.md)). LLM API keys also in `secrets.json`. |
| Telemetry | GUI: PostHog (`*.posthog.com`) + `z.openhands.dev` analytics, opt-out via `VITE_DO_NOT_TRACK=1` / localStorage flags. Agent-server: **no automatic phone-home** (verified by source search per deployment doc); only opt-in channels: OTEL/Laminar tracing (`OTEL_*` or `LMNR_PROJECT_API_KEY` set), hosted LLM proxy `llm-proxy.app.all-hands.dev` for `openhands/`-prefixed models, outbound webhooks (`OH_WEBHOOKS`). Caveat: bundled litellm may default `telemetry=True` unless blocked by egress policy. Sources: [OpenHands GUI AGENTS.md](https://github.com/noritaka1166/openhands/blob/HEAD/AGENTS.md), [deployment hardening doc](https://github.com/boomerang9/agent-acheevy-009/blob/HEAD/docs/openhands-deployment-hardening.md) |
| Cloud dashboard | **app.all-hands.dev** — OpenHands Cloud SaaS; conversation view at `https://app.all-hands.dev/conversations/<id>`, cloud API at `https://app.all-hands.dev/api/...`. Sources: [openhands-api skill](https://github.com/atineose/skills/blob/HEAD/skills/openhands-api/SKILL.md), [automation PR bot comments](https://github.com/OpenHands/automation/pull/319) |
| Leak-by-default? | **YES (self-hosted default config).** Full conversation events — prompts, tool outputs, file contents — persist as plaintext JSON files by default; LLM API keys / OAuth refresh tokens in plaintext `secrets.json` / `~/.openhands/auth/` unless `OH_SECRET_KEY` encryption is configured (opt-in). The sandbox runs the agent with the whole `~/.openhands` volume mounted in the Docker default. |

---

## Doc links (all public)

- Cline telemetry doc: https://github.com/rikaaa0928/rikline/blob/HEAD/docs/more-info/telemetry.mdx (fork mirror of official cline/cline docs)
- Cline privacy policy: https://github.com/opensvm/aingels/blob/HEAD/docs/PRIVACY.md (fork mirror)
- Cline storage (per-OS): https://github.com/veverke/chatwizard/blob/HEAD/docs/done/work-plan-support-additional-ai-coding-extensions.md
- Cline privacy audit: https://medium.com/@yurenpai57/i-audited-3-ai-coding-tools-for-privacy-the-difference-is-100x-eac40010381f
- Continue telemetry doc: https://github.com/teslamotors/continue/blob/HEAD/docs/docs/telemetry.md (fork mirror of official continuedev/continue docs)
- Continue telemetry audit: https://github.com/pwchiefy/agent-snitch-list/blob/HEAD/tools/continue.md
- Continue hardening settings ref: https://github.com/dandgabr/hardening-ia/blob/HEAD/docs/tools/continuedev/continue/continue.md
- Gemini CLI configuration docs: https://geminicli.com/docs/reference/configuration/
- Gemini CLI telemetry doc (mirror): https://github.com/ashwin3919/gemini-cli-exp/blob/HEAD/docs/cli/telemetry.md
- Gemini CLI storage/sessions survey: https://github.com/satyamsingh-git/elevenpowers/blob/HEAD/docs/research/hosts/gemini-cli.md
- Gemini CLI session-discovery: https://github.com/madeinorbit/podium/blob/HEAD/docs/agent-harness-reference/gemini.md
- Gemini CLI credential-file inventory: https://github.com/karlmarx/karl-infra/blob/HEAD/infra/gemini-cli.md
- Gemini CLI logPrompts default-true gate: https://github.com/gvastethecreator/tokenusage/blob/HEAD/docs/source-gates/GEMINI-CLI.md
- Codex CLI official docs (storage + telemetry + metrics): https://learn.chatgpt.com/docs/config-file/config-advanced
- Codex telemetry source analysis: https://github.com/hussainph/volli-code/blob/HEAD/docs/research/competitor-agent-observability.md
- Codex rollout-file consumers: https://github.com/kaantufan/toknado ; https://github.com/2004lryan/ai-cockpit
- OpenHands deployment hardening (telemetry/no-phone-home): https://github.com/boomerang9/agent-acheevy-009/blob/HEAD/docs/openhands-deployment-hardening.md
- OpenHands persistence/migration findings: https://github.com/openhands/agent-canvas/issues/1054
- OpenHands auth-storage analysis: https://github.com/kumanday/opensymphony/blob/HEAD/docs/openhands_agent_server_subscription_auth_analysis.md
- OpenHands Cloud API/skill: https://github.com/atineose/skills/blob/HEAD/skills/openhands-api/SKILL.md
- Cross-harness path registry: https://github.com/moabualruz/rice-aise/blob/HEAD/docs/tool-registry-reference.md
