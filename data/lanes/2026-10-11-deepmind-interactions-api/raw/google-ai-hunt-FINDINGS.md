# Google AI blog hunt — findings (2026-10-11)

Scope: blog.google AI/developer/security sections + research.google/blog, posts Nov 2025 → Oct 2026.
34 posts fetched and cached in `raw/` (see PROVENANCE.md). Report only — nothing ingested into Factum.

## Dedup status (per repo novelty rules)

- Factum `match --text --mode fuzzy` for 13 key terms (interactions api, antigravity-preview,
  managed agents gemini, fairwind, gemini-interactions-api, pagebreak, code-mender, hooks.json,
  npx skills add, gemini-api-docs-mcp.dev, deep-research-pro-preview, user alignment critic,
  agent origin sets): **0 hits** on all.
- Transluce findings DB (25 findings, full-text count): **0 hits** on all 14 novel terms.
- Repo-wide grep (silent-locus): "Antigravity" exists only as third-party proxy tools
  (`github.com/badrisnarayanan/antigravity-claude-proxy`, `github.com/KevinLiangX/AntigravityProxyLauncher`
  in gomod-hunt), a Discord username (tantive-space), and Mind2Web task names (false positive).
  CodeMender exists only as a bare blog URL in a hermes URL list. "Managed Agent" hits are
  Anthropic's Claude Managed Agents, not Google's. Everything below is otherwise **novel**.

---

## 1. IOCs

### API endpoints (NEW surface — Gemini API v1beta, Interactions API)
Spec: https://ai.google.dev/api/interactions.openapi.json (OpenAPI 3.0.3, server `https://generativelanguage.googleapis.com`)
- `POST /v1beta/interactions` — create interaction (model= or agent=)
- `GET /v1beta/interactions/{interactionsId}`, `POST .../cancel`
- `POST /v1beta/agents`, `GET /v1beta/agents/{agentsId}` — managed agent definitions
- `POST /v1beta/triggers`, `GET /v1beta/triggers/{id}`, `GET /v1beta/triggers/{triggerId}/executions` — cron triggers
- `POST /v1beta/webhooks`, `GET /v1beta/webhooks/{id}`, `POST /v1beta/webhooks/{id}:ping`, `POST /v1beta/webhooks/{id}:rotateSigningSecret`
- `POST /v1beta/credentials`, `GET /v1beta/credentials/{id}`
- `POST /v1beta/environments`, `GET /v1beta/environments/{id}`, file ops under `/environments/{environment}/files/{path}`
- `POST /v1beta/voices`, `GET /v1beta/voices/{voicesId}`
- SSE stream: `InteractionCreatedEvent`, `InteractionSseStreamEvent`, `InteractionCompletedEvent`; step types `user_input`, `thought`, `function_call`, `model_output` (from "Roles to Steps" schema change, GA Jun 2026)
- Webhook event enum: `batch.succeeded`, `batch.expired`, `batch.failed`, `interaction.requires_action`, `interaction.completed`, `interaction.failed`, `video.generated`

### Agent identifiers (managed, first-party)
- `deep-research-pro-preview-12-2025` — Gemini Deep Research agent id (Dec 2025)
- `antigravity-preview-05-2026` — Antigravity managed agent id (May 2026; default model Gemini 3.6 Flash from Jul 2026)
- Agent config types: `antigravity`, `deep-research`, `code-mender` (find/fix vulns, `session_id` grouping)
- Sample agent id in spec docs: `customer-sentinel`

### Tool type strings (Interactions API `tools=[{"type": ...}]`)
- `google_search`, `code_execution`, `url_context`, `mcp_server`, `function`
- MCP tool shape: `{"type": "mcp_server", "name": "internal_telemetry", "url": "https://mcp.internal.example.com/mcp"}`
- Client-side bash tool + hosted server-side bash tool (announced Gemini 3 launch, Nov 18 2025)

### Domains / URLs
- `generativelanguage.googleapis.com` — API host (A2A bridge cards point here too)
- `ai.google.dev/api/interactions.openapi.json` — public OpenAPI spec
- `gemini-api-docs-mcp.dev` — Gemini API Docs MCP server (coding agents)
- `antigravity.google/` — Antigravity site; `geminicli.com/` — Gemini CLI site; `ai.studio/build` — AI Studio build
- `a2a-protocol.org/latest/` — A2A protocol; `google.github.io/adk-docs/` — ADK docs
- `developers.google.com/opal/faq` — Opal (mini-apps experiment, sunsetting Nov 2026)
- `console.cloud.google.com/agent-platform/...` — Agent Platform console paths
- `docs.cloud.google.com/gemini-enterprise-agent-platform/build/managed-agents` — managed agents docs
- `deepmind.google/fairwind-program/` — Fairwind Program (trusted-defender access to cyber models)
- `deepmind.google/blog/introducing-gemini-3-5-flash-cyber/`, `.../securing-the-future-of-ai-agents/`
- `github.com/google-gemini/gemini-skills` — skills repo (`npx skills add google-gemini/gemini-skills --skill gemini-interactions-api`)
- `github.com/google-gemini/gemini-cli`, `github.com/google-github-actions/run-gemini-cli`
- `github.com/google/adk-python/tree/main/contributing/samples/interactions_api`
- `github.com/a2aproject/a2a-samples/tree/interactions-api/samples/python/transports/interactions_api`
- `github.com/google-gemini/cookbook/blob/main/quickstarts/Webhooks.ipynb` — webhooks cookbook
- `github.com/standard-webhooks/standard-webhooks` — webhook spec org
- `github.com/NVIDIA-NeMo/Automodel` (FunctionGemma finetune recipe), `github.com/google-ai-edge/LiteRT-LM`

### SDK identifiers
- `google-genai` (PyPI), `@google/genai` (npm) — Gemini API SDKs
- `google.adk.agents.llm_agent.Agent`, `google.adk.models.google_llm.Gemini`, `google.adk.tools.google_search_tool.GoogleSearchTool`
- 3P SDKs with Interactions API integrations: LiteLLM, Eigent, Agno

### Model version strings (capability-delta anchors)
- `gemini-3-pro-preview`, `gemini-3-flash-preview`, `gemini-3.5-flash`, `gemini-3.5-flash-lite`, `gemini-3.6-flash` (managed-agent default Jul 2026), `gemini-3.8-flash`
- Gemini 3.8 Flash Cyber (cybersecurity-specialized, Fairwind-gated; Sep 2026); Gemini 3.5 Flash Cyber (deepmind blog)
- Gemini 4 (mentioned Aug–Oct 2026 posts), `gemini-4-argon` (Oct 1, 2026 model post)
- FunctionGemma (Gemma 3 270M function-calling, Dec 18 2025), EmbeddingGemma 2

### Webhook security IOCs
- Headers: `webhook-signature`, `webhook-id`, `webhook-timestamp`; HMAC project-level, JWKS per-request; at-least-once delivery, retries up to 24h; Standard Webhooks spec
- Python shape: `client.batches.create(..., config={"webhook_config": {"uris": [...], "user_metadata": {"job_group": ..., "priority": ...}}})`

### ADK/agent-builder tradecraft
- `Agent(model=Gemini(model="gemini-2.5-flash", use_interactions_api=True), name="...", tools=[GoogleSearchTool(bypass_multi_tools_limit=True), ...])`
- "Inner loop (inside the API) vs outer loop (in your agent code)" — Google's framing of the split
- `previous_interaction_id` — server-side state continuation
- `.agents/AGENTS.md` + `.agents/<skill>/SKILL.md` (frontmatter `---name: slide-maker ...---`) — managed-agent definition convention; inline source type in `base_environment.sources`
- Environment hooks: `.agents/hooks.json`; events `pre_tool_execution` / `post_tool_execution`; matcher regex on tool names; handler types `command` (runs in sandbox, e.g. `python3 /.agents/hooks-scripts/gate.py`, timeout) and `http`; deny protocol: script returns `{"decision": "deny", "reason": "..."}` → call skipped, reason injected into model context
- Budget: `agent_config: {type: "antigravity", max_total_tokens: N}` → `status: "incomplete"` on cap; resume with `previous_interaction_id` + fresh budget
- Triggers: cron schedule + time_zone; statuses active/paused/error; auto-pause after `max_consecutive_failures`; each run reuses the same sandbox (files persist); Environments API lists/inspects/deletes sandboxes; 7-day sandbox TTL
- Egress control: `EnvironmentNetworkEgressAllowlist` — per-domain allowlist (example: `github.com` with Authorization header transform, `*.googleapis.com`), or `"disabled"` to block all egress
- Credentials: types `bearer_token` / `oauth2` (auto-refresh) / `environment_variable` (injected into sandbox container); stored in Secret Manager
- A2A bridge: `InteractionsApiTransport`, `make_card(url="https://generativelanguage.googleapis.com", agent="...")`; A2A Task ↔ Interaction ID; `IN_PROGRESS` → `TASK_STATE_WORKING`; "configuration smuggling" via A2A extensions (e.g. `thinking_summaries`)

### Gemini-app skills (consumer surface)
- Invocation `/skillname`; stackable; reference files (txt/PDF/images); replacing Gems (migration: Nov 2026 personal, Mar 2027 Workspace biz/edu Jun 2027); already in "Gemini Spark"

### Safety/architecture behaviorals
- Chrome agentic browsing (Dec 8 2025): User Alignment Critic (separate model, sees action metadata only, veto/approve + feedback to planner); Agent Origin Sets (read-only vs read-writable origins, trustworthy gating function, planner can't add origins); model-generated URLs deterministically restricted to known public URLs; spotlighting; sensitive-site deterministic list (banking/medical → user confirmation); no direct password access; prompt-injection classifier in parallel with planner; work log per task (pause/takeover); automated red-teaming with LLM-generated malicious sandboxed sites; VRP up to $20,000 for agentic boundary breaches
- PageBreak (Google internal vuln-hunting agent, pilot Nov 2025, full Jan 2026): models Gemini 3.1 Pro / 3.5 Flash; deterministic validators (XSS rendering harness monitoring execution context; SQLi output/timing; path traversal world-readable file; RCE sleep/file/DNS-HTTP; SSRF internal-request detection); identical seeds across iterations for trajectory search; 500+ XSS on first-party apps; integrates with CodeMender for auto-fixes
- Red team (Aug 2026): predicts ransomware operators + initial access brokers adopt agents first; on-device models to avoid network noise; "crafting malicious skill files for agents" named as cheapening supply-chain attacks; abliteration of open-weight guardrails; sock-puppet long-con phishing

---

## 2. Behavioral patterns (agent tradecraft)

1. **Server-side agent state is the new default.** Interactions API: `background=True`, server-side history via `previous_interaction_id`, SSE streaming. Observable signature of Google-agent traffic: REST calls to `/v1beta/interactions` with `agent=` ids, `background` polling via `interactions.get`.
2. **Scheduled autonomous agents run on cron with persistent sandboxes.** Trigger resources bind agent+environment+prompt+cron; files persist across runs; 7-day TTL.
3. **Hooks are the guardrail primitive** (pre/post tool execution, regex matchers, deny-via-JSON protocol). A rogue or jailbroken managed agent would show `.agents/hooks.json` with permissive matchers.
4. **SKILL.md is a supply-chain surface.** Registry install via `npx skills add <gh-repo> --skill <name>`; Google red team explicitly flags "malicious skill files for agents" as a cheapening supply-chain vector. Managed agents define skills as inline markdown with `---name:---` frontmatter.
5. **Webhooks are the exfil-shaped surface.** Standard Webhooks headers (`webhook-signature/id/timestamp`), user_metadata on batch jobs, 24h retry — a Google agent pushing results to an attacker URL looks like this.
6. **Egress is allowlisted per sandbox** — but allowlist examples include `github.com` with injected Authorization headers. Agents that escape would still carry these shapes.
7. **Browser-agent defense patterns** (Chrome): alignment critic + origin sets + URL allowlist checks — fingerprints of Google's production browser agents (work logs, confirmation pauses).
8. **Deep Research behavior loop**: formulate queries → read results → identify gaps → search again; File Upload + File Search Tool; structured JSON outputs; collaborative planning (human-in-the-loop plan confirm).
9. **Edge-agent pattern**: FunctionGemma 270M as "traffic controller" — local handling of common commands, routing complex tasks to larger models (Gemma 3 27B).

## 3. Novel hunt leads

1. **Monitor `generativelanguage.googleapis.com/v1beta/{agents,interactions,triggers,webhooks,environments}` usage in the wild.** Any agent fleet using Google's managed-agent stack leaves these endpoint shapes. Hunt: code in public repos calling `client.interactions.create(agent="antigravity-preview-05-2026")` or hardcoding these paths.
2. **SKILL.md supply-chain sweep.** `npx skills add` registry convention is new (2026); sweep GitHub/npm for `gemini-interactions-api`-style skills and typosquats of `google-gemini/gemini-skills`. Google red team names this vector explicitly.
3. **`gemini-api-docs-mcp.dev`** — new MCP server domain (Apr 2026). Watch for lookalikes/malicious mirrors; MCP servers are the tool-injection surface.
4. **Webhook receiver hunting.** The Standard-Webhooks header triple (`webhook-signature`, `webhook-id`, `webhook-timestamp`) from Google infra is a new beacon shape for finding Google-agent dead drops / C2-ish receivers.
5. **Antigravity proxy-tool nexus.** Corpus already has `antigravity-claude-proxy` / `AntigravityProxyLauncher` (gomod-hunt) — third parties proxying through Antigravity auth. New angle: the official `antigravity-preview-05-2026` managed agent + `AntigravityAgentConfig` server-side runtime control. Cross-reference.
6. **Fairwind Program** (`deepmind.google/fairwind-program/`) — gated access to cyber models (3.5/3.8 Flash Cyber). "Trusted defender" vetting process is a new social-engineering target surface; also a marker for defender-side tooling.
7. **Trigger cron schedules** — recurring autonomous agents with `next_run_time`/`last_run_time` metadata; time_zone + cron format gives fleet-timing fingerprints.
8. **`.agents/hooks.json` in public repos** — permissive `*` matchers or `http` handlers pointing at external endpoints = guardrail bypass or exfil hooks.
9. **Chrome agentic VRP ($20k)** — external researchers probing agentic boundaries; watch Bug Hunters blog companion posts (PageBreak cache-poisoning writeup) for technique diffusion.
10. **A2A `make_card` + "configuration smuggling"** — AgentCards pointing at `generativelanguage.googleapis.com` with smuggled config; new shape for agent-registry poisoning.

## 4. Capability deltas

- Interactions API GA Jun 2026 → primary API; generateContent stays but frontier agentic features land exclusively on Interactions API.
- Managed Agents May 2026 → hooks Jul 2026 → triggers/budgets; free-tier access Jul 2026 (lowers abuse barrier).
- Deep Research: two versions (speed vs depth), collaborative planning, native charts, MCP connectivity.
- Model cadence: 3.5 → 3.6 (managed default) → 3.7 → 3.8 (+Cyber) in ~6 weeks (Jul–Sep 2026); Gemini 4 / 4-Argon surfacing Oct 2026.
- Thought handling: `thought_signatures` strict validation (Nov 2025) → typed `thought` steps in Interactions schema (Jun 2026).
- Tool results can now return images alongside text (Jun 2026); Google Maps added as built-in tool.
