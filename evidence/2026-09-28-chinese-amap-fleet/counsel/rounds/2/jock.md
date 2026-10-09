# COUNSEL Round 2 — JOCK (harness-log red-team + exposed-instance re-grade)

*Filed 2026-10-05. Persona: JOCK — sweep energy, high-coverage boring queries.*
*Scope: the 10-harness leak-by-default map + the 6 exposed-instance leads. Passive only: our corpora, public indexes/snippets, Shodan stored observations. No candidate was connected to, probed, or fetched.*
*Classification per finding: Novelty OURS (in our corpora/files already) / KNOWN (publicly documented) / GENUINELY NEW (neither); Evidence OBSERVED (our bytes) / PUBLIC SOURCE (cited) / INFERENCE (labeled).*

## Corpus census (OBSERVED — the boring ground, counted)

Searched `data/2026-10-01-oai-tag-sweep/events.jsonl` (96,353 events) + `openai-agent-traces/data/traces.jsonl` (589,972 events) = **686,325 events**.

| Query class | Pattern | tag-sweep | traces | Total |
|---|---|---|---|---|
| Lead IPs | 128.140.75.138 / 149.130.187.39 / 100.29.190.103 / 75.146.94.94 / 119.91.57.121 / 1.92.91.104 | 0 each | 0 each | **0 / 6** |
| Lead hostnames | smartpromotion / agendatucitavisual / quycapp | 0 | 0 | **0 / 3** |
| Map grammars | `.claude/projects` / `.continue/sessions` / `.gemini/tmp` / `.codex/sessions` / `saoudrizwan.claude-dev` / `.openclaw/agents` / `.aider.chat.history` | 0 | 0 | **0 / 7** |
| Broad harness names (case-insensitive) | openclaw / aider / windsurf / codeium / rollout- / .gemini/ / .continue/ / claude-dev / .codex/ / kilocode / roo-cline | 0 | 0 | **0 / 11** |
| | openhands | **1** | 0 | **1** |

The single `openhands` hit: urlquery report `c92092b5-6746-41e7-943a-b4db8a9b6bb7` (event 2026-05-07T05:41:47Z), URL `openhands-eval-monitor.vercel.app/?run=commit0/litellm_proxy-openai-gpt-5-5/1778132350/`, indicator epoch_nonce, tags urlquery-hunt/agent-activity. **Already claimed** by the scavenger lane (`personas/scavenger/FINDINGS.md:67`, `infra-watchlist/INFRASTRUCTURE-WATCHLIST.md:334` — "OpenHands eval monitor (litellm proxy, gpt-5-5), attribution FOREIGN (OpenHands)"). Independent re-find, no new claim.

**Net: of 13 harness/file-grammar queries over 686,325 events, 12 are absolute zero and the 13th is an already-attributed foreign eval-infra URL. No harness names, no transcript-path grammars, no lead IPs/hostnames appear in agent-traffic URLs.**

---

## FINDING 1 — Aider "YES (git-remote risk)" is OVER-RATED: current Aider auto-gitignores by default → recommend PARTIAL

**Claim:** HARNESS_LOG_MAP.md grades Aider **YES (local/git)**, mechanism: "it is only excluded from git if the user manually adds the aider history patterns to `.gitignore`."

**Evidence (PUBLIC SOURCE, Sep–Oct 2026, two independent):**
- `amelnagdy/delegate-skills` (39d): "the relay passes `--no-gitignore`, these show up as untracked entries in `touchedFiles` rather than being hidden by a **`.gitignore` Aider wrote itself**."
- `dmore/cl-agent-continual-learning-substrate-for-coding-agents` adapters/aider/README.md (7d): "`--no-gitignore` avoids modifying `.gitignore` just to add `.aider*`."

Both treat Aider writing `.aider*` into `.gitignore` as the DEFAULT behavior that adapters must explicitly suppress. The map's mechanism rests on a 350-day-old community sample (`igamenovoer/quicknote`) predating the auto-gitignore default.

**Residual risk is real but conditional (PUBLIC SOURCE):**
- Bug report `ita-dnipro/pl4847#139` (66d): "`.aider.chat.history.md` … currently appears in Git and can be **accidentally included** in commits" — already-tracked files / `git add -f` / `--no-gitignore` users.
- `zsxh1990/misakanet` lesson (2026-08-22, evidence E2): history file "written to the project directory and **may** be committed to version control"; also notes `--api-key` on the CLI leaks the key into the history file itself.

**Classification:** GENUINELY NEW correction to our files (the auto-gitignore default is not in the map). **Actionability:** downgrade Aider YES→**PARTIAL** (local plaintext by default, no cloud channel — now structurally identical to Continue's PARTIAL); correct the mechanism line; keep the residual-risk note. Open question (INFERENCE, not asserted): whether Aider's default-on auto-commits can race the `.gitignore` write on first run.

---

## FINDING 2 — Headline count correction: 7-of-10 becomes 6-of-10

**Claim:** Map bottom line: "7 of 10 harnesses are leak-by-default, 2 partial, 1 (OpenClaw core) no."

**Evidence:** Finding 1 (Aider→PARTIAL) is the only verdict change; all other six YES verdicts re-verified this round (Findings 3–6). **Corrected tally: 6 YES / 3 PARTIAL / 1 NO.** The six YES: Claude Code, Cursor, Windsurf (individuals), Gemini CLI, Codex CLI, OpenHands. The three PARTIAL: Aider, Cline, Continue.

**Classification:** GENUINELY NEW (derived). **Actionability:** amend the map's bottom line and summary table.

---

## FINDING 3 — Gemini CLI YES *strengthened*: `usageStatisticsEnabled=true` (default) collects prompts+answers for Login-with-Google users

**Claim:** Map grades Gemini CLI YES on three compounding defaults, #1 being "`logPrompts` defaults to true."

**Evidence (PUBLIC SOURCE):**
- `logPrompts` wound: config docs (multiple forks, incl. `handlehim/gemini-cli` 12d) show default `{"enabled": false, "target": "local", "otlpEndpoint": "http://localhost:4317", "logPrompts": true}` — i.e. `logPrompts=true` is the default *inside a telemetry block that is itself default-off*. The map's framing as a compounding *default* overstates it; content exfil via OTel requires the user to enable telemetry. (Wound, not kill.)
- The missing, stronger leg — `privacy.usageStatisticsEnabled` **default `true`** (same config ref, 12d). Per the official FAQ quoted on HN (`news.ycombinator.com/item?id=44376919`): "The 'Usage Statistics' setting is the single control for all optional data collection in the Gemini CLI… **Auth method 1 [Login with Google]: When enabled, this setting allows Google to collect both anonymous telemetry (like commands run and performance metrics) and your prompts and answers for model improvement.**" Login-with-Google is the default OAuth path; `~/.gemini/oauth_creds.json` holds the refresh token.
- Supporting: `google-gemini/gemini-cli#21101` (214d) confirms the setting is first-class, default true; PR #2593 added obfuscated GAIA IDs to Clearcut logs.

**Classification:** GENUINELY NEW to our files (the usageStatistics→prompt-collection path is not in the map). **Actionability:** replace the wounded `logPrompts` framing with the usageStatistics leg; YES verdict stands, now on firmer ground. Note: "model improvement" use vs "anonymous telemetry" depends on auth method — keep the qualifier.

---

## FINDING 4 — Cursor YES re-verified against current vendor language; map's binary framing slightly stale

**Claim:** Map: "Privacy Mode OFF by default for Free/Pro individuals → code to servers/providers with possible retention/training."

**Evidence (PUBLIC SOURCE, current):**
- `cursor.com/data-use` via `nyosegawa` terms investigation (23d): "If you choose to turn off 'Privacy Mode': **we may use and store codebase data, prompts, editor actions, code snippets**, and other code data and actions **to improve our AI features and train our models**." Stronger than the map's paraphrase ("providers may retain per their policies") — it is *Cursor itself* training, not just provider retention.
- `defra/ai-sdlc-tool-guidance` (crawled 4d): Cursor now has **three** stances — Privacy Mode (Legacy, zero storage), Privacy Mode (new: zero-retention at providers but encrypted narrowly-scoped code storage on Cursor servers for Background Agents/Memories), Standard (privacy off, broad telemetry/retention). "Individual developers on Free and Pro plans **must manually select** their preferred privacy stance" — default is not a privacy stance.
- One conflicting anecdote (`mvolkmann/blog`): "It seems this is enabled by default, but double-check it" — outweighed by vendor docs + defra.
- Local leg unchanged: `state.vscdb` writes regardless (map's aixlehq citation); corroborated by `chaybits/ectype` inventory (6d): `cursorDiskKV` rows `composerData:`/`bubbleId:`.

**Classification:** KNOWN publicly; the vendor-language upgrade and three-stance model are GENUINELY NEW to our files. **Actionability:** KEEP the YES verdict; update the mechanism to quote cursor.com/data-use and note the three-stance model (map's binary ON/OFF framing is stale).

---

## FINDING 5 — Windsurf YES (individuals) freshly corroborated post-Cognition

**Claim:** Map: "YES for individuals — zero-retention is enterprise/team default only; individual ToS permits Chat/Autocomplete content use for model improvement."

**Evidence (PUBLIC SOURCE):**
- `katagun/ai-systems-atlas` ADR (5d): "The former Windsurf security page now redirects to Cognition's security page, which states **'By default, we may use your data for model training purposes** to improve and enhance the Services' and offers the **opt-out only on paid plans**."
- `plucins/ai-tools-radar` (129d): "Privacy policy states Windsurf may use Log and Usage Information and Prompts/Outputs to train, develop, and improve models/services; security docs add zero-data-retention defaults for Teams/Enterprise and optional ZDR for individual users."

**Classification:** KNOWN publicly; the 5-day-old Cognition-policy confirmation is GENUINELY NEW to our files. **Actionability:** KEEP verdict; cite the current Cognition policy. Note (INFERENCE): the map's cascade-`.pb` AES key-shipped-in-binary claim remains community-RE-sourced, correctly flagged as such — no change.

---

## FINDING 6 — Codex CLI YES and Claude Code YES re-verified from primary sources; OpenClaw NO (core) confirmed

**Codex (PUBLIC SOURCE, official docs fetched 2026-10-05):** `learn.chatgpt.com/docs/config-file/config-advanced` L662–664: "**By default**, Codex periodically sends a small amount of **anonymous usage and health data back to OpenAI**… Metrics collection is independent of OTel log/trace export." Opt-out `[analytics] enabled = false`. Storage legs corroborated by third-party tools reading live paths: `Loongphy/codex-auth` (19d) reads "the newest `~/.codex/sessions/**/rollout-*.jsonl`"; `aidenlyu/codexbar-linux` (13d) scans "`CODEX_HOME` (or `~/.codex`) `sessions` and sibling `archived_sessions` JSONL files"; `nicechencs/workforce` (18d) confirms "`auth.json` present with `auth_mode=chatgpt`". **YES stands** (load-bearing legs are local plaintext rollout files + plaintext auth.json; the metrics channel is anonymous per docs).

**Claude Code (PUBLIC SOURCE, official docs):** `code.claude.com/docs/en/data-usage` (crawled 3h ago): "Local caching: Claude Code clients **store session transcripts locally in plaintext under `~/.claude/projects/` for 30 days by default** to enable session resumption." Verbatim vendor admission. **YES stands**, rock solid.

**OpenClaw NO (core) (PUBLIC SOURCE):** telemetry doc via three mirrors (`rstar327/openclaw` 41d, `jibon4201/openclaw` 24d, `openclaw-android-assistant` FAQ 18d): "**The only thing OpenClaw sends on its own is a daily update check**… carries nothing but the version, operating system, and CPU architecture." Disable knob the map missed: `update.checkOnStart: false`. **NO (core) stands** — but see Finding 7.

**Classification:** KNOWN (all three confirm map's existing claims). **Actionability:** no verdict changes; add the `update.checkOnStart` knob to the map.

---

## FINDING 7 — UNDER-RATED: OpenClaw is the most *exposed* agent control surface in the wild despite "NO (core)"

**Claim:** Map's bottom line reads "1 (OpenClaw core) no" — true on the telemetry axis, misleading on the exposure axis.

**Evidence:**
- OBSERVED (our hunt, `exposed-instances.md`): `http.title:"OpenClaw"` = **33,669** Shodan-indexed instances — the largest clean agent-control-surface population found; `port:18789` raw = 198,478.
- PUBLIC SOURCE: dev.to exposure-wave report — researchers scanned **18,000 exposed OpenClaw instances**; **~900 malicious skills** in the registry; Kaspersky/Bitdefender advisories. NemoClaw CVE-2026-65105 (cyera.com): OpenClaw deployer binding Ollama to **0.0.0.0:11434**, exploitable via DNS rebinding.
- OBSERVED: lead 75.146.94.94 — OpenClaw control-UI on a **residential Comcast** IP, i.e. the exposure reaches consumer ISP space.

**Classification:** GENUINELY NEW synthesis (the map and the exposed-instances hunt never reconciled). **Actionability:** the map's single-axis taxonomy (telemetry/local-storage) misses the network-exposure axis. Recommend splitting the verdict: **NO (core telemetry) / YES (network exposure by deployment)** — OpenClaw's gateway binds a port and 33.7k instances are indexed. The `.openclaw/agents/` grammar stays on the watchlist; ADD the control-UI exposure (port 18789, title grammar) as the highest-priority *live* exposure surface, above the filesystem grammars (which have zero observed exposures — Finding 9).

---

## FINDING 8 — Coverage gap: the map's 10 harnesses miss live grammars (Cline modern path, Antigravity, Qwen, Roo/Kilo, SpecStory, Copilot CLI, Goose, Crush, LM Studio)

**Claim:** Map covers 10 harnesses; its "highest-value directory grammars" list has 7 entries.

**Evidence (PUBLIC SOURCE):**
- **Cline modern path missing from map:** `ddarmon/sesh` (31d), `wolfbomb/deja-vu` registry (10d), `missuo/tokens#52` (58d), `agitHQ/agit` 0.11.0 (22d) all confirm **two generations**: modern CLI/SDK → `~/.cline/data/sessions/<id>/<id>.messages.json` (+ `~/.cline/data/tasks/` in 3.x); legacy VS Code extension → `saoudrizwan.claude-dev/tasks/`. The map documents ONLY the legacy path. **The map's Cline grammar is version-partial** — current installs write to the unlisted path.
- **Entirely missing harnesses with known transcript stores** (`chaybits/ectype` inventory 6d; `maximilianfeix/spillage` 7d):
  - **Google Antigravity** (agentic IDE, major 2025-2026 surface): `~/.gemini/antigravity-cli/brain/<id>/…/transcript_full.jsonl`
  - **Qwen Code** (Alibaba, Gemini-CLI fork): `~/.qwen/tmp/*/chats/` — same family as the `.gemini/tmp` grammar
  - **Roo Code / Kilo Code** (Cline forks): `…/roo-cline/tasks/<id>/`, `kilocode` equivalents — same family as the cline grammar
  - **SpecStory** (repo-local, aider-like): `.specstory/history/*.md` **in the project dir** — same git-exposure shape as aider
  - **GitHub Copilot CLI**: `~/.copilot/session-state/`
  - **Goose**: `~/.local/share/goose/sessions/sessions.db`
  - **Crush**: `.crush/crush.db` per project
  - **LM Studio**: `~/.lmstudio/conversations/<epoch>.conversation.json`
  - VS Code Copilot Chat: `Code/User/**/chatSessions/*.jsonl`
- Minor: ectype notes Codex rollout files now carry **encrypted reasoning** in newer builds — map doesn't mention it (does not change the YES; tool outputs remain plaintext).

**Classification:** GENUINELY NEW to our files. **Actionability:** extend the watchlist grammars with `~/.cline/data/sessions/`, `~/.cline/data/tasks/`, `roo-cline/tasks/`, `.qwen/tmp/`, `~/.gemini/antigravity-cli/`, `.specstory/history/`, `~/.copilot/session-state/`, `.crush/`. The Cline PARTIAL verdict is unaffected (both generations are local-plaintext). Flag the map's harness roster as "10 of N" rather than exhaustive.

---

## FINDING 9 — The 7 map grammars are high-value *watchlist*, zero *observed* exposures — and that null is now triply confirmed

**Claim:** Map: "the highest-value directory grammars to watch in open-directory indexes" (framed as watch, not as observed).

**Evidence:**
- OBSERVED: 0/686,325 corpus hits for all 7 grammars (census above).
- OBSERVED (hunt): `exposed-instances.md` honest nulls — `intitle:"index of" ".claude"` returned only GitHub hits; aider/codex/cline exposure queries polluted; no S3/Docker-Hub agent-state evidence.
- PUBLIC SOURCE (new this round): the exposure-discussion that *does* exist is about **dataset/training-data** channels, not open directories — `GavenXia/agentleak` README cites Truffle Security: **221,303 live credentials in 6,003 public AI datasets**; a single pasted Infura key propagated to **1,131 public datasets** via WildChat; Chaofan Shou/Fuzzland (Sep 2026, reported claim): 6TB of LLM-relay logs with SSH keys, VPN configs, Alibaba Cloud keys, GitLab tokens. Tools `spillage` (7d) and `agentleak` now exist specifically to scrub these local stores — ecosystem acknowledgment of the threat model.
- Method note: `grep.app` API (public code index) returned HTTP 429 + Vercel security checkpoint for all 7 grammar queries — the public-code-index count avenue is **blocked**, recorded as a method null, not an evidence null.

**Classification:** the corpus/index nulls are OURS (observed); the Truffle/agentleak material is KNOWN publicly, GENUINELY NEW to our files. **Actionability:** keep the grammars as WATCHLIST (the map correctly frames them as "to watch"); add the dataset-leak channel as the empirically-observed exfil path for harness transcripts — it vindicates the Cursor/Windsurf/Gemini training-use YES legs more than any open-directory hunt could. Recommend a future lane: query public dataset indexes (not code indexes) for transcript-shaped content.

---

## FINDING 10 — The 6 exposed-instance leads re-graded: none meets the Round 1 upgrade condition; 4→WATCHLIST, 2→OBSERVED (population markers)

**Standard applied:** Round 1 tie-break — "Upgrade condition: **agent-traffic co-occurrence or a second independent pivot**. Until then, do not cite as agent-linked." Plus kill-grounds: (a) base rate — personal devs run identical stacks; (b) corpus-contrary.

**Evidence (OBSERVED):** all 6 IPs 0/686,325; all 3 hostnames 0/686,325. **No lead has agent-traffic co-occurrence. No lead has a second independent pivot** (each is single-source Shodan). The "agent" signal on leads 1–3 and 5 is *naming only* (`sp-agent-2`, `agent.` subdomain, `agente`, bare inference port).

| Lead | Re-grade | Rationale |
|---|---|---|
| 128.140.75.138 Ollama, `sp-agent-2-bzc.kube.smartpromotion.az` (Hetzner) | **WATCHLIST** (was LEAD) | k8s service named "agent" inside a marketing company's cluster — base-rate naming; zero corpus. Infra oddity only. |
| 149.130.187.39 Ollama, `agent.agendatucitavisual.com` (Oracle) | **WATCHLIST** (was LEAD) | Appointment-scheduling company's agent subdomain — product naming, base rate; zero corpus. |
| 100.29.190.103 Flowise, `quycapp-agente.quycapp.co` (AWS) | **WATCHLIST** (was LEAD) | Agent-builder endpoint (Flowise 4,047 indexed) with ES/PT "agente" naming. Most on-point of the six for "agent infra," still single-source + zero corpus. Keep as agent-builder population exemplar. |
| 75.146.94.94 OpenClaw :18789 (Comcast residential) | **WATCHLIST** (was LEAD, keep with caveat) | Full agent control surface on residential ISP — operationally the most interesting (session/memory access if unauthed), but 1 of 33,669 indexed; "LEAD" overstates distinctiveness 33,669-fold. Residential-ISP caveat stands (prior-lane precedent: Vietnam residential kept as LEAD — not re-litigated here). |
| 119.91.57.121 llama.cpp :1234 (Tencent Beijing) | **OBSERVED** (was LEAD — demote) | Bare inference endpoint, llama.cpp banner on LM Studio's port. **No agent-shaped signal at all** beyond "inference endpoint"; weakest of the six. Log as population data point (llama.cpp 1,781 indexed), not watchlist. |
| 1.92.91.104 Dify :80 (Huawei Cloud) | **OBSERVED** (was LEAD — demote) | Explicitly logged as "representative of ~3k indexed Dify population" — a population marker by the author's own description, not a lead. |
| 144.76.75.252 :8000 ("vllm" keyword, no banner) | — | Concur with author's WEAK / not-logged. |

**Corroborating population context (PUBLIC SOURCE):** Mysterium Sep-2026 census — 36,769 self-hosted AI endpoints, **only 2.02% with auth challenges**; SentinelOne/Censys Jan-2026 — ~175k exposed Ollama, ~half with tool-calling; vLLM 4,880 endpoints, **3 with auth**. The population is the story; no single instance is distinctive without co-occurrence.

**Classification:** re-grades are GENUINELY NEW counsel dispositions; population figures KNOWN. **Actionability:** apply the four WATCHLIST / two OBSERVED grades to IP_LOG.md; do not cite any of the six as agent-linked (Round 1 convention).

---

## Method nulls & open threads (honest)

1. `grep.app` API blocked (HTTP 429 → Vercel security checkpoint) for all grammar queries — public-code-index counts unavailable this round.
2. Aider `--gitignore` default confirmed by two independent community sources (Sep–Oct 2026), not re-verified against official Aider docs — official-docs confirmation open.
3. Aider auto-commit vs `.gitignore`-write race on first run — unexamined, flagged not asserted.
4. Gemini `usageStatisticsEnabled` content-collection scope verified via official FAQ quoted on HN; per-auth-method variance noted, not exhaustively mapped.
5. Windsurf cascade-`.pb` key-shipped-in-binary claim remains community-RE-sourced (map already flags this correctly).
6. Live-browser-only avenues untouched per lane rules: Megalodon index probe for our fingerprints, Wayback CDX incident-window sweep (both already open hunt threads).
