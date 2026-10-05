# Agent-Harness Log/Trace Storage Map — Part 1 (of 2)

Research date: 2026-10-05. Scope: Claude Code, Cursor, Windsurf, OpenClaw, Aider — public docs and public source only. No installs, no execution, no endpoint probing. Every factual claim carries a source link or is marked **INFERENCE** / **NULL** (docs silent).

## 1. Claude Code (Anthropic CLI)

| Item | Detail | Source |
|---|---|---|
| Session transcripts | `~/.claude/projects/<project>/<session-id>.jsonl`, JSONL; `<project>` = cwd with non-alphanumerics → `-` (truncated at 200 chars + path hash) | https://code.claude.com/docs/en/sessions#where-transcripts-are-stored |
| Transcript retention | Deleted after 30 days by default; `cleanupPeriodDays` in `~/.claude/settings.json` | https://code.claude.com/docs/en/sessions#where-transcripts-are-stored (retention table); https://dev.to/heylittlepan/claude-code-conversation-history-where-it-lives-how-to-search-it-how-to-get-it-back-4lc8 |
| Prompt history | `~/.claude/history.jsonl` — every typed prompt; NOT touched by the 30-day cleanup | https://dev.to/heylittlepan/claude-code-conversation-history-where-it-lives-how-to-search-it-how-to-get-it-back-4lc8 |
| Debug logs | `~/.claude/debug/<session-uuid>.txt` + `latest` symlink; runtime internals (MCP/plugin loading, hooks), NOT conversation content | https://github.com/aaarrrccc/vault-context/blob/HEAD/archive/v1/CLAUDE-CODE-SESSION-LOGS.md |
| Additional local dirs (community-verified, format changes between releases) | `~/.claude/projects/<project>/sessions-index.json`; subagent transcripts `~/.claude/projects/<project>/<session>/subagents/agent-<id>.jsonl`; `paste-cache/`, `image-cache/`, `tool-results/`, `memory/` (project auto-memory) | https://github.com/heiervang-technologies/unleash/blob/HEAD/docs/internal/claude-code/CLI_FORMAT.md |
| Override knobs | `CLAUDE_CONFIG_DIR` (move `~/.claude` root), `CLAUDE_CODE_PROJECT_DIR_NAME` (override project dir), `CLAUDE_CODE_SKIP_PROMPT_HISTORY` (suppress transcript writes), `CLAUDE_CODE_TRANSCRIPT_LOCAL_GC` (cap `-p` transcript size), `--no-session-persistence` (single `-p` run) | https://code.claude.com/docs/en/sessions#where-transcripts-are-stored |
| OAuth credentials | `~/.claude/.credentials.json` | **INFERENCE** — widely documented publicly; not re-verified from an official page this session |
| Per-OS | `~/.claude` on all platforms (docs give no per-OS distinction) | https://code.claude.com/docs/en/sessions#where-transcripts-are-stored |
| Phones home | (a) All prompts/outputs → Anthropic API (or Bedrock/Vertex/Foundry) over TLS — required for inference. (b) Operational metrics (latency, reliability, usage; NEVER code, prompts, or file paths) → Statsig; opt out `DISABLE_TELEMETRY=1`. (c) Error reports (redacted stack traces) → Sentry; opt out `DISABLE_ERROR_REPORTING=1`. (d) Optional user-initiated OTel: `CLAUDE_CODE_ENABLE_TELEMETRY=1` + `OTEL_*` vars export to a user-configured collector; prompt/tool content gates (`OTEL_LOG_*`) are opt-in only. | https://code.claude.com/docs/en/data-usage.md ; https://github.com/speednet-software/speedwave/blob/HEAD/docs/adr/ADR-076-mdm-enforceable-otlp-telemetry.md |
| Feedback/bug path | `/bug` and `/feedback` send a copy of full conversation history **including code** to Anthropic (GCS bucket + optional public GitHub issue); transcript-share follow-up after quality surveys uploads session + subagent transcripts to Anthropic unless declined (key patterns redacted; code/file contents uploaded as-is). Opt out `DISABLE_FEEDBACK_COMMAND=1` / `DISABLE_BUG_COMMAND` | https://code.claude.com/docs/en/data-usage.md ; https://github.com/paddychief92/claude-code-docs/blob/HEAD/docs/docs__en__data-usage.md |
| Cloud/Remote Control | Remote Control sessions: transcript also stored on Anthropic servers to sync across devices | https://code.claude.com/docs/en/data-usage.md |
| Cloud dashboard | No hosted log dashboard. Consumer privacy controls at `claude.ai/settings/data-privacy-controls` (training opt-out, retention) | https://code.claude.com/docs/en/data-usage.md |
| Server-side retention | Consumer (training opt-in): 5y; consumer opt-out: 30d; commercial: 30d (ZDR available per-org) | https://code.claude.com/docs/en/data-usage.md |

**Leak-by-default:** **YES.** Transcripts are stored in **plaintext JSONL** locally by default (`~/.claude/projects/`), explicitly acknowledged in official docs: "Claude Code clients store session transcripts locally in plaintext under `~/.claude/projects/` for 30 days by default". They contain full prompts, file contents read via tools, and tool outputs — any secret pasted in chat or read from disk is on disk in the clear. **INFERENCE** risk note: no disk encryption is provided by the tool itself.

## 2. Cursor (Anysphere IDE, VS Code fork)

| Item | Detail | Source |
|---|---|---|
| Chat/composer history | SQLite `state.vscdb`: macOS `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`; Windows `%APPDATA%/Cursor/User/globalStorage/state.vscdb`; Linux `~/.config/Cursor/User/globalStorage/state.vscdb` — chat under keys `composer.composerData` / `composer.composerHeaders` | https://github.com/mbjorke/timelog-extract/blob/HEAD/docs/specs/cursor-evidence-ceiling.md ; https://github.com/Veverke/ChatWizard ; https://github.com/blueplane-ai/bp-telemetry-core/blob/HEAD/README.md (platform paths) |
| Per-workspace DBs | `User/workspaceStorage/<hash>/` per workspace (chat/checkpoint DBs); IDE logs at `<data-dir>/logs/` | https://github.com/lolai-project/lolai-project.github.io/blob/HEAD/_agents/cursor-ai.md ; https://github.com/mbjorke/timelog-extract/blob/HEAD/docs/specs/cursor-evidence-ceiling.md |
| Config/codebase dirs | Project rules in `.cursor/rules/` (committed to repo); index exclusions via `cursor.excludeFromIndexing` / `cursor.excludeFromContext` | https://github.com/depalmar/ai_for_the_win/blob/HEAD/docs/guides/cursor-ide-guide.md |
| Auth token storage | `cursor.auth.token` in settings DB (sensitive) | https://github.com/lolai-project/lolai-project.github.io/blob/HEAD/_agents/cursor-ai.md |
| Phones home | (a) All AI features send prompt + code context to Cursor servers then to model providers (OpenAI, Anthropic, Google, xAI) — required. (b) Codebase index: embeddings → Cursor embedding API / Turbopuffer vector DB (vectors only, code looked up locally). (c) Wire endpoints (from bundle RE): `api2.cursor.sh` (IDE gRPC/Connect API), `api3.cursor.sh` (telemetry), `api.cursor.com` (cloud agents REST), `agent.api5.cursor.sh` | https://forum.cursor.com/t/local-mode-is-misleading-even-with-byo-openai-key/837 (Anysphere staff); https://github.com/jeremylongshore/claude-code-plugins-plus-skills/blob/HEAD/./skills/.curated/cursor-privacy-settings/SKILL.md ; https://github.com/taucad/tau/blob/HEAD/docs/research/cursor-sdk-openai-compat.md |
| Privacy Mode | ON = zero data retention at providers, no training, anonymous telemetry only. **OFF by default for Free/Pro individuals** (must enable manually: Settings → General → Privacy Mode). ON by default + enforceable for teams/enterprise. With Privacy Mode OFF: providers may retain per their policies; code "may be used to improve AI models"; telemetry "may include code snippets" | https://www.arsturn.com/blog/cursor-ai-privacy-is-it-training-on-your-codebase ; https://github.com/annablume/llm-security-framework/blob/HEAD/docs/LLM-Security-Guidelines.md ; https://github.com/jeremylongshore/claude-code-plugins-plus-skills/blob/HEAD/./skills/.curated/cursor-privacy-settings/SKILL.md |
| Telemetry opt-out | Settings → Telemetry (crash reports + feature analytics), orthogonal to Privacy Mode; newer Ghost Mode (Settings → Advanced) intercepts all outbound chat/telemetry locally | https://github.com/aixlehq/insights/blob/HEAD/docs/data-pipeline/DATA-CURSOR.md |
| Cloud dashboard | `https://cursor.com/dashboard` (team admin dashboard, usage + privacy enforcement); `https://cursor.com/settings` (account privacy status) | https://github.com/grcengineering/how-to-harden/blob/HEAD/docs/_guides/cursor.md ; https://github.com/jeremylongshore/claude-code-plugins-plus-skills/blob/HEAD/./skills/.curated/cursor-privacy-settings/SKILL.md |

**Leak-by-default:** **YES.** Privacy Mode is off by default for individual plans, so default config sends prompts/code to Cursor servers and providers with possible retention and training use, and telemetry may include code snippets. Locally, full chat content persists in `state.vscdb` regardless of privacy switches (aixlehq: "The local SQLite rows are written regardless of all of them (until Ghost Mode)").

## 3. Windsurf (Exafunction/Codeium IDE, acquired by Cognition July 2025)

| Item | Detail | Source |
|---|---|---|
| Cascade trajectories | `~/.codeium/windsurf/cascade/` and `~/.codeium/windsurf/cascade/implicit/` — per-session `*.pb` protobuf files, AES-256-GCM encrypted (per community RE, with a key shipped in the `language_server` binary) | https://github.com/ottorgb/windsurf-local-user-data-decryption ; https://github.com/yawlabs/ctxlint/blob/HEAD/AGENT_SESSION_LINT_SPEC.md |
| Chat in workspaceStorage | `<data-dir>/User/workspaceStorage/<hash>/state.vscdb` under key `cascade.sessionData` (VS Code-fork layout like Cursor) | https://github.com/Veverke/ChatWizard |
| Auto-generated memories | `~/.codeium/windsurf/memories/` — workspace-scoped | https://github.com/sliamh11/deus/blob/HEAD/docs/research/cli-mode-data-management.md |
| Transcripts (alternate) | `~/.windsurf/transcripts/*.jsonl` (reported in one inventory; may be version-dependent) | https://github.com/yawlabs/ctxlint/blob/HEAD/AGENT_SESSION_LINT_SPEC.md |
| App/config dirs (macOS) | `~/.windsurf/` (extensions); `~/Library/Application Support/Windsurf/` (app data, logs, workspace history); `~/.codeium/` (AI engine data, incl. `~/.codeium/config.json` device_id) | https://github.com/verthon/portfolio/blob/HEAD/src/routes/dev-bites/fully-removing-windsurf-on-macos/index.mdx ; https://github.com/fotedev/unban-machine-id/blob/HEAD/docs/AGENTS.md |
| Phones home | All AI features send prompt + code context to Windsurf/Exafunction servers then to model providers (OpenAI, Anthropic, Vertex, xAI) — required. Embeddings computed remotely then stored locally. Windsurf (now Cognition) ToS: may use Autocomplete/Chat user content to improve discriminative/generative models; cognition.ai privacy policy describes training/fine-tuning on user content | https://github.com/nyosegawa/nyosegawa.github.io/blob/HEAD/en/posts/coding-agent-terms-investigation.md ; https://harini.blog/2025/07/02/windsurf-detailed-enterprise-security-readiness-report/ |
| Zero-data-retention mode | Default ON for Teams/Enterprise (code processed in memory only, never written to disk/DB at Windsurf, not used to train). Individual users: opt-in; toggle at `windsurf.com/settings` ("Disable Telemetry"); `windsurf.privacyMode` setting | https://github.com/defra/ai-sdlc-tool-guidance/blob/HEAD/tool-guidance/windsurf-summary.md ; https://github.com/nyosegawa/nyosegawa.github.io/blob/HEAD/en/posts/coding-agent-terms-investigation.md ; https://github.com/dandgabr/hardening-ia/blob/HEAD/docs/tools/codeium/windsurf/windsurf.md |
| NOTE — dead security page | `codeium.com/security` now redirects to **Cognition (Devin)** security docs — the standalone Windsurf/Codeium security page is gone post-acquisition | https://codeium.com/security (fetched 2026-10-05: "Security at Cognition - Devin Docs") |
| Cloud dashboard | `windsurf.com/settings` (telemetry toggle). Team dashboard: **NULL** — no publicly verified URL this session | https://github.com/nyosegawa/nyosegawa.github.io/blob/HEAD/en/posts/coding-agent-terms-investigation.md |

**Leak-by-default:** **YES for individuals** — zero-retention is enterprise/team default only; individual ToS permits Chat/Autocomplete content use for model improvement. Even at rest, Cascade trajectories sit on disk per session under `~/.codeium/windsurf/cascade/` (encrypted but with a reportedly shared binary-shipped key per community RE — treat the key claim as RE-sourced, not vendor-confirmed).

## 4. OpenClaw (open-source agent gateway)

| Item | Detail | Source |
|---|---|---|
| State root | `~/.openclaw` (move with `OPENCLAW_STATE_DIR`) | https://github.com/openclaw/docs/blob/HEAD/docs/automation/tasks.md |
| Global control plane | `~/.openclaw/state/openclaw.sqlite` — shared config state, registries, approvals, plugin state (replaced `tasks/runs.sqlite` + `flows/registry.sqlite` sidecars in v2026.6.1) | https://github.com/openclaw/docs/blob/HEAD/docs/automation/tasks.md ; https://github.com/jackwarr72/openclaw/blob/HEAD/docs/reference/database-schemas.md (fork of openclaw/docs) |
| Per-agent data plane | `~/.openclaw/agents/<agentId>/agent/openclaw-agent.sqlite` — sessions, transcripts, memory indexes, auth state, conversation state, runtime trajectory events | https://github.com/jackwarr72/openclaw/blob/HEAD/docs/reference/database-schemas.md (fork of openclaw/docs) |
| Legacy session store | `~/.openclaw/sessions.json` (older releases; JSON file-based KV with atomic writes) | https://github.com/aterrylu/autonomos/blob/HEAD/docs/research/openclaw/sessions-and-memory.md |
| Config / secrets | `~/.openclaw/openclaw.json` — holds plugin config including API keys (e.g. `plugins.entries.manifest.config.apiKey`); plugin-local `~/.openclaw/manifest/config.json` (mode 0600 in local mode) | https://github.com/dvcrn/openclaw-skills-marketplace/blob/HEAD/plugins/brunobuddy--manifest-build/skills/manifest/SKILL.md |
| Per-OS | Docs default `~/.openclaw` with no per-OS distinction | **NULL** — docs silent on Windows/macOS/Linux variants |
| Phones home (core) | Only a **daily update check** by default: carries nothing but version, OS, CPU arch. Anonymous feature statistics (channels/providers configured) are **off by default, never self-enable**, ride along with the update check when opted in; aggregates published at `telemetry.openclaw.ai`. Disable-the-check knob exists per docs ("every privacy control") — exact env var not captured | https://github.com/nathan-lim-hiya/openclaw/blob/HEAD/docs/gateway/telemetry.md (fork of openclaw/docs; canonical repo openclaw/docs) |
| Plugin telemetry (not core) | Third-party plugins can add their own phone-home: e.g. memos plugin → PostHog (anonymous, opt-out via `telemetry.enabled: false` / `TELEMETRY_ENABLED=false`); manifest plugin → PostHog product analytics (opt-out `MANIFEST_TELEMETRY_OPTOUT=1`) and OTLP spans to a user-configured endpoint (user prompts/responses/tool args explicitly NOT collected per its privacy doc) | https://github.com/memtensor/memos/blob/HEAD/apps/memos-local-openclaw/README.md ; https://github.com/dvcrn/openclaw-skills-marketplace/blob/HEAD/plugins/brunobuddy--manifest-build/skills/manifest/SKILL.md |
| Cloud dashboard | **None** — fully self-hosted; no vendor account, no hosted history view | https://github.com/openclaw/docs/blob/HEAD/docs/automation/tasks.md (self-hosted state model) |

**Leak-by-default:** **NO (core)** — core writes everything to local SQLite under `~/.openclaw` with no analytics phone-home; the weakest default surface is **plaintext API keys and auth state in `~/.openclaw/openclaw.json` + `~/.openclaw/agents/<agentId>/agent/openclaw-agent.sqlite`** (local file-permission protection only). Plugin ecosystem is the real exposure vector: plugins can add PostHog/OTLP egress (documented opt-outs exist but are per-plugin).

## 5. Aider (Aider-AI, open-source CLI)

| Item | Detail | Source |
|---|---|---|
| Chat history | `<repo>/.aider.chat.history.md` — Markdown, full conversation, written to the **project directory** by default (configurable: `--chat-history-file`) | https://github.com/daikidomon/ai-agent-log-formats/blob/HEAD/tools/aider/README.md ; https://github.com/igamenovoer/quicknote/blob/HEAD/dev-guide/aider-project-config.md |
| Input history | `<repo>/.aider.input.history` — readline-format one-entry-per-line (configurable: `--input-history-file`) | https://github.com/daikidomon/ai-agent-log-formats/blob/HEAD/tools/aider/README.md |
| LLM exchange log | `<repo>/.aider.llm.history.json` — optional raw LLM log (`--llm-history-file`) | https://github.com/igamenovoer/quicknote/blob/HEAD/dev-guide/aider-project-config.md |
| Tag cache | `<repo>/.aider.tags.cache.v3/` | https://github.com/daikidomon/ai-agent-log-formats/blob/HEAD/tools/aider/README.md |
| Config | Repo `.aider.conf.yml`; global `~/.aider.conf.yml` or `~/.config/aider/.aider.conf.yml` | https://github.com/daikidomon/ai-agent-log-formats/blob/HEAD/tools/aider/README.md |
| Analytics dir | `~/.aider/` — analytics preferences `analytics.json`; opt-in local event log `~/.aider/analytics.jsonl` (only exists if `--analytics-log` set) | https://github.com/rajbos/ai-engineering-fluency/issues/1492 ; https://github.com/daikidomon/ai-agent-log-formats/blob/HEAD/tools/aider/README.md |
| Per-OS | All-platform `~/.aider` + repo-local files; no per-OS distinction documented | **NULL** — docs silent |
| Phones home | (a) Analytics `--analytics` (env `AIDER_ANALYTICS`); **default: "random"** — prompts user on first run; `--no-analytics` for session, `--analytics-disable` (env `AIDER_ANALYTICS_DISABLE`) permanent; custom destination via `--analytics-posthog-host` / `--analytics-posthog-project-api-key` (i.e. PostHog transport). (b) Version check on launch, default on (`--check-update` / `AIDER_CHECK_UPDATE`). (c) No vendor cloud: LLM calls go directly to the provider the user configures (BYO key) | https://github.com/ryanmckenzie-code/aider/blob/HEAD/aider/website/docs/config/options.md (mirror of official aider docs) ; https://github.com/rajbos/ai-engineering-fluency/issues/1492 |
| Cloud dashboard | **None** — local tool, no vendor-hosted history | **INFERENCE** from architecture (no account system in docs) |

**Leak-by-default:** **YES (local/git).** `.aider.chat.history.md` is written into the repo working directory **by default** and contains the full prompt history including any secrets pasted into chat and file contents added to context; it is only excluded from git if the user manually adds the aider history patterns to `.gitignore` (community config samples carry exactly that warning: "add these patterns to .gitignore so they are not committed"). An accidental commit pushes the whole conversation to the remote. No cloud leak by default (analytics prompt-gated).

## Cross-harness summary

| Harness | Leak-prone storage (most leak-prone first) | Leak-by-default |
|---|---|---|
| Claude Code | `~/.claude/projects/<project>/<session-id>.jsonl` — plaintext full transcripts incl. secrets/code | **YES (local disk, plaintext)** |
| Cursor | `state.vscdb` (`composer.composerData`) + Privacy Mode OFF default for individuals → cloud retention/training exposure | **YES (cloud for individuals; local DB always)** |
| Windsurf | `~/.codeium/windsurf/cascade/*.pb` trajectories + ToS allows training use for individuals | **YES (individuals; local disk + ToS)** |
| OpenClaw | `~/.openclaw/openclaw.json` (plaintext API keys) + per-agent SQLite | **NO (core); plugins can add egress** |
| Aider | `<repo>/.aider.chat.history.md` — repo-local, one careless commit away from the remote | **YES (git-remote risk by default)** |

## Doc links

- Claude Code sessions (official): https://code.claude.com/docs/en/sessions#where-transcripts-are-stored
- Claude Code data usage / telemetry (official): https://code.claude.com/docs/en/data-usage.md
- OpenClaw task storage (official docs repo): https://github.com/openclaw/docs/blob/HEAD/docs/automation/tasks.md
- OpenClaw DB schemas (forks of openclaw/docs): https://github.com/jackwarr72/openclaw/blob/HEAD/docs/reference/database-schemas.md
- OpenClaw telemetry page (forks of openclaw/docs): https://github.com/nathan-lim-hiya/openclaw/blob/HEAD/docs/gateway/telemetry.md
- Aider options incl. analytics (mirror of official aider docs): https://github.com/ryanmckenzie-code/aider/blob/HEAD/aider/website/docs/config/options.md
- Cursor privacy settings explainer: https://github.com/jeremylongshore/claude-code-plugins-plus-skills/blob/HEAD/./skills/.curated/cursor-privacy-settings/SKILL.md
- Cursor local telemetry/data-flow deep dive: https://github.com/aixlehq/insights/blob/HEAD/docs/data-pipeline/DATA-CURSOR.md
- Cursor endpoints (bundle RE): https://github.com/taucad/tau/blob/HEAD/docs/research/cursor-sdk-openai-compat.md
- Windsurf local storage inventory: https://github.com/verthon/portfolio/blob/HEAD/src/routes/dev-bites/fully-removing-windsurf-on-macos/index.mdx
- Windsurf cascade decryption (community RE): https://github.com/ottorgb/windsurf-local-user-data-decryption
- Windsurf terms/privacy investigation: https://github.com/nyosegawa/nyosegawa.github.io/blob/HEAD/en/posts/coding-agent-terms-investigation.md
- Multi-tool storage inventories: https://github.com/Veverke/ChatWizard ; https://github.com/yawlabs/ctxlint/blob/HEAD/AGENT_SESSION_LINT_SPEC.md
- OpenClaw plugin privacy docs: https://github.com/dvcrn/openclaw-skills-marketplace/blob/HEAD/plugins/brunobuddy--manifest-build/skills/manifest/SKILL.md ; https://github.com/memtensor/memos/blob/HEAD/apps/memos-local-openclaw/README.md
