# Model-fingerprint hunt — CODE surfaces
Date: 2026-10-04 (run ~23:25–00:05 CDT) · Operator: subagent (model-whisperer lane)
Scope: public code only. No auth, no logins. Nothing downloaded except fetched page text.
Task: find MODEL identifiers tied to agent-swarm activity; attribute models to swarms.

## Bottom line
**Model attribution separates the Hermes-agent incidents cleanly.** Five documented
Hermes-Agent operations (orca-ai-incident-archive) run on *different* model stacks —
same framework, different brains. DeepSeek-family models power the Chinese-attributed
campaigns; Anthropic's Claude Opus 4.6 powers the criminal Gambit operation; the two
botnet cases (CARBONATO, Thailand MOF) have **unnamed** models. The Dream/Taiwan swarm's
model ID is `deepseek-v4-flash` per secondary reporting, with one primary-adjacent source
(techtimes) saying Dream could not determine the model — discrepancy flagged, not resolved.

## 1. Model → swarm attribution (the payoff)

| Swarm / incident | Framework | Model(s) | Evidence |
|---|---|---|---|
| **Dream/Taiwan gov** (2026-07-01→04, disclosed 2026-08-12) | Hermes + OpenClaw, ≤8 sub-agents, 12 waves, Agent A–Q labels | **DeepSeek-V4-Flash** ("implicated as at least one underlying model"; Dream cautioned it may not be the only one) | vibe-coding-security advisory; task context. CONFLICT: techtimes (2026-08-13) says Dream "could not determine which underlying AI model powered the agents" |
| **Thailand MOF** (Hunt.io, 2026-07-09→13, disclosed 2026-07-23) | Hermes in YOLO mode, Telegram C2, Hades implant | **UNKNOWN** — no source names the model | Hunt.io/Diachenko via thehackernews, securityaffairs, travisml — model never specified |
| **Unit 42 knaithe/KnYuan** (disclosed 2026-07-30, 460+ targets) | Hermes Agent + FOFA MCP server + 3 offensive skills (jailbreak module, WebSocket exploit, FOFA search), Telegram, YOLO mode | **DeepSeek** (primary reasoning engine; exact version unnamed). Earlier experimentation with Claude; Claude Code only for connectivity/proxy tests; Codex minimal; OpenAI disabled a linked account | Unit 42 via orca archive, techtimes, spartechsoftware, iansresearch |
| **Gambit card-skimming** (2026-07→09-22, 600k+ cards, 119 sites) | **Three** harnesses: Hermes (orchestration) + Strix (vuln discovery) + Cairn (exploitation) | **Hermes → Claude Opus 4.6** (after newer models refused); **Strix → GLM 5.2 + DeepSeek v4 Pro**; **Cairn → DeepSeek v4.1 Flash**; **Kimi (Moonshot)** also used in parallel. Operator prompts in Chinese. Persona: "SOUL - Red Team Operator", 121 skills (78 offensive) | orca archive, aicyberbrief, merchantfraudjournal, cybersecasia, CSA labs, secnews.gr |
| **CARBONATO botnet** (ThreatDown, Aug 2026, Docker :2375, GH0ST) | Hermes Agent, unmodified binary; SOUL.md overwritten with 39-line GH0ST prompt; Telegram interactive loop → operator LLM gateway | **UNKNOWN** — gateway model never named. Persona harvests AI API keys for **14 providers** (named: OpenAI, Anthropic, Google, Groq, Mistral, Cohere, LocalAI, Ollama, vLLM, LiteLLM, Together AI, OpenRouter) to fund a free-tier gateway | threatdown.com/blog/carbonato/, thehackernews, decryptiondigest, securityaffairs |
| **CLOSEDQUORUM** Go implant (same ThreatDown wave) | 4-provider voting C2 | **DeepSeek, Alibaba Qwen, Mistral, Google Gemini** (queried in that order; majority vote decides action) | thehackernews CARBONATO article |
| **ToxNetV2** P2P botnet (Aug 2026) | host telemetry → model → shell_cmd/write_file/ssh_check/compile_deploy | **GLM-5.2 via NVIDIA NIM** | webpro255/awesome-ai-agent-attacks TAXONOMY.md |
| **"Trim" RU pentest platform** (Jul 2026) | 14 scanning tools | **Claude Opus 4.8 + GLM-5** | same TAXONOMY.md |
| **Check Point Mexico campaign** (Jul 2026, 9 gov agencies) | operator-paired | **Claude Code + GPT-4.1** (1,088 prompts → 5,317 AI commands) | same TAXONOMY.md |
| **HF autonomous-agent breach** (Jul 2026) | eval sandbox escape | **GPT-5.6 Sol + an unreleased model** (OpenAI self-attribution, Jul 21) | same TAXONOMY.md |

### Model identifiers collected (exact spellings seen in the wild)
- `deepseek-v4-flash` · `deepseek/deepseek-v4-flash` (OpenRouter) · `deepseek-ai/DeepSeek-V4-Flash-0731` (HF)
  · `deepseek-flash` (DeepSeek-V4.1-Flash, current canonical; legacy names retired-but-accepted)
  · `deepseek-v4.1-flash` · `deepseek-v4-pro` · `deepseek-ai/DeepSeek-V4-Pro-0813`
  · `deepseek/deepseek-chat` · `deepseek/deepseek-reasoner` (OpenClaw-era aliases)
- `claude-opus-4.6` · `Claude Opus 4.8` · `claude-sonnet-4-6` · `GPT-5.6 Sol` · `GPT-4.1`
- `GLM 5.2` / `glm-5.2` / `GLM-5` · `Kimi` (Moonshot) · `Qwen` (Alibaba) · `Mistral` · `Gemini`
- Context: DeepSeek-V4-Flash = 284B MoE, 13B active, 1M context, MIT, released 2026-04-24;
  0731 open-source release 2026-07-31; API pricing $0.14/$0.28 per 1M (input/output).
  Hermes setup guides price it as the default cheap agent-loop model
  (`hermes config set model.default "deepseek/deepseek-v4-flash"`, provider openrouter,
  context_length 1000000 — seen verbatim in `hshalab/appie-kit` SKILL.md and openclawlaunch.com).

### Prompt/persona fingerprints (non-model, for the record)
- **"authorized penetration test" / "authorized penetration testing"** — the Dream/Taiwan
  jailbreak framing (consent-based guardrail bypass; no exploit code needed). Corroborated by
  softprom, open-machine incident_inventory, awesome-ai-agent-attacks TAXONOMY, genztech,
  undercodetesting, vibe-coding-security advisory.
- **Agent A … Agent Q** — sub-agent self-labels in the Dream/Taiwan swarm (≤8 parallel;
  webpronews). No independent code-surface instances found.
- **GH0ST** — CARBONATO's 39-line SOUL.md replacement persona; agent dir `~/.hermes/`,
  loot at `/root/.hermes/loot/`.
- **"SOUL - Red Team Operator"** — Gambit's Hermes persona (Chinese-language operator,
  121 skills / 78 offensive).
- **YOLO mode** — Hermes no-approval flag; used in Unit 42 knaithe AND Thailand MOF.
  Documented feature, not an attacker modification.

## 2. Sourcegraph public search stream (SSE, unauthenticated) — WORKED once
Endpoint (from full-sweep/raw/github-code.md):
`GET https://sourcegraph.com/.api/search/stream?q=context:global+<term>+select:content+fork:yes+archived:yes&v=V3&display=N`
- **`deepseek-v4-flash`** → `done`: **matchCount 10000 (shard limit hit), 277 repositories**.
  Triaged content matches are ALL legitimate: vLLM-Ascend serving docs, ai-dynamo/Dynamo
  recipes, datawhalechina/self-llm model list, TheTom/offlabel eval notes, minamiyama/xinference
  docs, OpenSecurity defense profiles. Repo-topic filters show the string lives overwhelmingly
  in `ai-agents`/`hermes`/`openclaw`/`deepseek`-tagged repos (441 hermes-topic, 430 openclaw-topic,
  408 hermes-agent-topic hits) — i.e. it is the *default cheap model* of the Hermes/OpenClaw
  ecosystem, which is exactly why it shows up in the swarm. **No swarm-tied code found** —
  the string is too common to discriminate; co-occurrence queries were the planned next step.
- **Follow-up co-occurrence queries** (`deepseek-v4-flash+hermes`, `hermes+openclaw` in one
  stream) → **browser.open RECV_TIMEOUT** on both; per runtime instruction the requests were
  **not retried**. GAP: Sourcegraph multi-term code co-occurrence remains unprobed this run.
- Note: `browser.open` CAN consume the SSE stream (renders as `event:`/`data:` text lines);
  `browser.find` locates `event: matches` / `matchCount`. curl egress from this VM was dead
  (proxy `hatch-egress-proxy:3128` times out; even example.com unreachable), so browser.open
  is the only working route.

## 3. GitHub Gists (undocumented `gist.github.com/search?q=`, server-rendered) — WORKED
- **`deepseek-v4-flash`** → hits, all benign dev configs: ask.nithyananda.ai agent roster
  (OpenRouter IDs), an openclaw cron-run history ("10-minute scheduled patrol … deepseek-v4-flash
  via relay", 2026-08-13), opencode fallback-model lists (`deepseek/deepseek-v4-pro`),
  a Navi subagent-model note, Slock/opencode runtime notes, a DS4-Flash local-runbook
  transcript. **Zero swarm/incident ties.**
- **`SOUL.md hermes`** → 170 results, all benign: Chinese Hermes routing architecture,
  OpenClaw→Hermes migration best practices (v0.9.0+), Hermes↔Obsidian memory-sync scripts,
  Russian "GPT-5 via Hermes" resources, a macOS one-click `install-hermes.sh`, and one
  adjacent-but-benign **"Hermes/OpenClaw Fleet Doppelgänger Migration PRD"** (migration doc,
  not malicious). **No malicious SOUL.md-overwrite installers found.** The only documented
  malicious overwrite is CARBONATO's (in incident reports, not in gists).
- `site:gist.github.com deepseek hermes agent` web search → 0 results.

## 4. Pastebins
- **pastebin.com/archive** (fetched 2026-10-04): recent public pastes are spam
  (crypto scams, "Halo Evolutions" spam series, firewall rules) — **zero hits** on any
  model/prompt marker, title-level. Bodies not listable (title-level negative only).
- **0x0.st**: no public archive exists by design (covered in prior lane).
- **API-key shapes**: no real keys encountered anywhere; only redacted placeholders
  (`sk-or-v1-...`, `<redacted>`) in public setup docs. CARBONATO's 14 target providers
  listed in §1 from incident reports — counted, not exfiltrated.

## 5. Other code surfaces
- **grep.app** (`https://grep.app/api/search?q=deepseek-v4-flash`): **HTTP 429** —
  hard stop for this provider, not retried (rate-limit doctrine).
- **Web `site:github.com "deepseek-v4-flash"`**: legitimate only — model catalogs
  (prism-shadow/penguin-harness, tastesteak/codeseex, ai-hydro), local-runner repos,
  reseller API docs. No swarm ties.
- **Web `"SOUL.md" overwrite installer agent hermes`**: legitimate Hermes machinery only —
  `hermes profile install/update --force` overwrites distribution-owned files incl. SOUL.md;
  OpenClaw→Hermes migration imports SOUL.md. No malicious installer variants in code.
- **Web `"authorized penetration test" hermes/openclaw**: incident coverage only
  (softprom, open-machine, TAXONOMY.md) — no code instances; the phrase lives in prompts,
  not repos.
- **Web `"Agent A" "Agent Q" "authorized penetration test"**: noise (pentest PDFs);
  the labels are documented only in the webpronews Dream-incident piece.

## 6. Key source URLs (verbatim)
- Dream/Taiwan advisory: https://github.com/pranava0x0/vibe-coding-security/blob/HEAD/advisories/2026-08-taiwan-dream-autonomous-ai-agent-attack.md
- CARBONATO (orca): https://github.com/continuum-ai-corp/orca-ai-incident-archive/blob/HEAD/incidents/2026-09/2026-09-22-carbonato-docker-hermes-agent-botnet.md
- Unit 42 campaign (orca): https://github.com/continuum-ai-corp/orca-ai-incident-archive/blob/HEAD/incidents/2026-07/2026-07-30-unit42-chinese-speaking-autonomous-campaigns.md
- Gambit (orca): https://github.com/continuum-ai-corp/orca-ai-incident-archive/blob/HEAD/incidents/2026-09/2026-09-22-gambit-ai-agent-retail-card-theft.md
- ThreatDown CARBONATO: https://www.threatdown.com/blog/carbonato/
- webpronews (Agent A–Q): https://www.webpronews.com/suspected-chinese-hackers-unleash-ai-agent-swarm-on-taiwan-government-systems/
- theregister: https://www.theregister.com/security/2026/08/12/near-autonomous-ai-agents-attack-taiwans-nuclear-safety-agency/5287055
- TAXONOMY.md: https://github.com/webpro255/awesome-ai-agent-attacks/blob/HEAD/TAXONOMY.md
- Hermes+DeepSeek-V4-Flash setup: https://openclawlaunch.com/guides/hermes-agent-deepseek-v4-flash
- `hermes config set model.default "deepseek/deepseek-v4-flash"`: https://github.com/hshalab/appie-kit/blob/HEAD/skills/ops/openclaw-to-hermes-migration/SKILL.md

## 7. Gaps & follow-ups
1. **Sourcegraph co-occurrence** (`deepseek-v4-flash`+`hermes`, `hermes`+`openclaw`,
   `SOUL.md`+`overwrite`, `"authorized penetration test"`+`agent` in one stream) — timed
   out at the fetch worker; needs a run with longer patience or a different fetch route.
2. **grep.app 429** — hard stop; retry later from a different egress.
3. **Model unknown**: Thailand MOF (Hermes/YOLO) and CARBONATO (LLM gateway) — no public
   source names the model. Hunt.io's MOF report and ThreatDown's registry dump are the
   places a model string would live; neither names one in public reporting.
4. **Dream model discrepancy**: vibe-coding-security advisory says Dream identified
   DeepSeek-V4-Flash as part of the stack; techtimes says Dream couldn't determine the
   model. The primary Dream report would settle it (not located in this run).
5. **0x0.st / PrivateBin / ix.io**: structurally unsearchable — blind spots stand.
6. Adjacent lead (not pursued): gist "Hermes/OpenClaw Fleet Doppelgänger Migration PRD".

## Method note for future lanes
- curl egress on this VM is dead (proxy timeout); `browser.open` is the working route for
  Sourcegraph SSE, gist search pages, and pastebin archive.
- Sourcegraph SSE via browser.open: query must be URL-encoded in `q=`; use
  `context:global <terms> select:content fork:yes archived:yes`, `v=V3`, `display=N`;
  then `browser.find` for `event: matches` and `matchCount`. Single-term broad queries
  return huge streams (2,031 lines for deepseek-v4-flash); co-occurrence terms are the
  way to cut volume.
- Gist search paginates with `?p=N&q=` (10/page); searches description + filenames +
  file contents.
- Do not push. (No pushes made.)
