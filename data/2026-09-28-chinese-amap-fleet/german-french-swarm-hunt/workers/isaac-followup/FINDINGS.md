# ISAAC-FOLLOWUP findings — isaac-cli footprint, deployment traces, mirror divergence, zcode SOUL.md, forge visibility

**Worker:** ISAAC-FOLLOWUP (wave-2, EUROSWARM) · **Date:** 2026-10-05
**Method:** passive public OSINT only — web-search snippets + unauthenticated raw.githubusercontent.com fetches (public repos) + passive page reads of git.saillant.cc public pages. No logins, no auth bypass, no probing beyond public pages/docs. No human/operator identity work.
**Conventions:** OBSERVED = byte-level public evidence, quoted/cited. INFERENCE = analytic judgment, labeled. Full observed values kept (no redaction).

---

## 0. Repo identity map (OBSERVED, reconciled)

The lineage is a rebrand chain, not three independent projects:

| Handle | URL (verbatim) | Identity at HEAD |
|---|---|---|
| Canonical | https://github.com/ailiance/ailiance-agent | ISAAC, CLI `isaac`, badge `release-v0.9.5--beta`, Apache-2.0 |
| Old canonical URL (redirects) | `ailiance/isaac-cli` | kept as repository URL per CHANGELOG "[Unreleased] — Rebrand → ISAAC" |
| Mirror | https://github.com/L-electron-Rare/agent-kiki | README byte-identical to canonical at HEAD (972 lines rendered, same content incl. `# ISAAC` header and `CLI : isaac`) |
| Fork (older snapshot) | https://github.com/ebii/agent-ailiance | `# agent-kiki`, CLI `aki` (alias `agent-kiki`), gateway branding `eu-kiki`, trace dir `.agent-kiki/runs/` — the pre-rebrand naming era |
| Primary forge (claimed) | `git.saillant.cc/ailiance/isaac-cli` (from README quickstart) | NOT publicly visible on forge index (see §5) |

CHANGELOG (root `CHANGELOG.md`, fetched) confirms the rebrand: "[Unreleased] — Rebrand → ISAAC — Product rebrand `aki` → `ISAAC` (Intelligence Souveraine Ailiance Agent Codeur). The CLI command is now `isaac` (the `aki` and `ailiance-agent` bin names are dropped — no alias). npm package `ailiance-agent` → `isaac`, `ailiance-agent-cli` → `isaac-cli` … Env vars `AKI_STRICT_PROVIDER`/`AKI_WEBUI_URL` → `ISAAC_*`. Stack dir `~/.aki/` → `~/.isaac/`."

Version trail (CHANGELOG, all dated 2026-05-12): 0.6.0 → 0.6.1 → 0.7.0 → 0.7.1 → 0.7.2 → 0.8.0 → 0.8.1 → 0.8.2 → 0.8.3 → 0.9.0 → 0.9.1 → [Unreleased] ISAAC rebrand.

---

## 1. What the Jina :5050 / LiteLLM :4000 stack actually does (OBSERVED — docs/local-stack.md)

**Jina is NOT a web-fetch/reader egress primitive here. It is a local embeddings model used for intent classification → model routing.**

Observed from `docs/local-stack.md` (raw fetch, canonical repo):

- Pipeline: `isaac → Jina router (:5050) → LiteLLM proxy (:4000) → endpoints`
- **Jina semantic router (:5050):** "Embeds incoming queries via `jinaai/jina-embeddings-v2-small-en` (~80 MB model, ~150 MB RAM)" — downloaded from HuggingFace on first start ("Slow first start of router: it downloads the embeddings model from Hugging Face (~80 MB)"). "Classifies intent into: `code`, `chat`, `search`, `agent`. Picks the preferred model per category (configurable). Forwards to LiteLLM with the chosen model. Routes config: `~/.isaac/jina-router/routes.json`."
- **LiteLLM proxy (:4000):** "Multiplexing across providers (Anthropic, OpenAI, Ollama, ailiance workers). Native fallback, retry, cost tracking, response cache. Config: `~/.isaac/litellm/config.yaml`."
- Managed via `isaac stack {install,start,stop,status}` (creates Python venvs in `~/.isaac/`); auto-detect gated on the `useLocalStack` setting; detection results cached 30 s. Alternative in-process `LocalRouter` (heuristic code/fr/reason/general classifier, LRU cache, 30 s worker health pings) avoids the Python stack entirely.

INFERENCE: wave-1's "Jina baked into its runtime" concern is resolved as **benign**: the bake-in is a small local embedding model for semantic routing of LLM requests (cost/latency optimization), executed entirely on localhost. There is no observed use of the jina.ai Reader/Search hosted APIs, no URL-fetch primitive in the router, and no evidence of it serving as an exfil relay. The wave-1 LEAD tag on this pattern should be **downgraded to a characterized/benign pattern** — still worth keeping as a vocabulary reference when scanning other DE/FR repos, but not an egress signal.

### 1b. Egress primitives the harness actually ships (OBSERVED)

Sourced from README + docs (public), all observed values:

- **No webhook receiver/sender, no ngrok, no dead-drop primitives** in the agent's shipped surface. Targeted search (`github ailiance ailiance-agent OR isaac-cli webhook OR ngrok OR tunnel code`) returned zero repo-specific hits.
- **Tunnels in their own ops docs (not agent egress primitives):**
  - `docs/local-stack.md` "Qwen3-Next 80B-A3B (kxkm-ai, port 18888 → gateway :8002)": "Tunnel: autossh `electron-server:8002` → `kxkm-ai:18888`" — documented infra plumbing for their inference worker, presented as ops notes in public docs.
  - CHANGELOG v0.6.1 (2026-05-12): "Default gateway URL `http://electron-server:9300/v1` → `https://gateway.ailiance.fr/v1`. **The Cloudflare Tunnel now exposes the FastAPI gateway publicly** with auto-terminated TLS" — inbound Cloudflare Tunnel for their public gateway. Tailscale still used for admin/internal hosts (`admin.ailiance.fr` DNS-only via Tailscale; `http://electron-server:9300/v1` on-tailnet override).
- **Proxies:** local LiteLLM proxy :4000 (above); Web UI at `http://127.0.0.1:25463` "with worker status dashboard, SPA standalone on `/spa`, gRPC HTTP backend on `/grpc/StackService/*`."
- **Browser control:** `useBrowser` is a first-class auto-approve action (`autoApprovalSettings.actions.{readFiles, editFiles, executeCommands, useBrowser}`); yolo mode "Approuve TOUT (read + write + bash + browser)". Browser tool exists in the agent's action set.
- **MCP + plugin marketplace:** `isaac plugin install` installs Claude Code plugins; "MCP integration: discover and use MCP servers from installed plugins"; `enabledMcpServers` / `mcpToolDenylist` / `mcpToolAllowlist` filtering — **default is allow-all** ("Omit or set `null` to load all (default)").
- **Shell egress posture** (`src/core/safety/zoneClassifier.ts`, README): `curl / wget / ssh / scp / rsync (network egress)` are in the `confirm` zone — "toujours approbation explicite" — but yolo/autoApproveAll approves them if `autoApprovalSettings.actions.executeCommands` is true. `hard_deny` covers `rm -rf`, fork bombs, `curl … | sh` pipe-to-shell, raw disk writes, sudo — "Yolo mode ne déverrouille **pas** cette zone."
- **Scriptable non-interactive modes** (agent CAN be driven unattended): `isaac "<prompt>"` (one-shot, no TTY), `echo … | isaac`, `isaac t -y "<prompt>"` (yolo task subcommand), `isaac --acp` (Agent Client Protocol). The bare interactive TUI refuses non-TTY ("Bail clair si lancé en pipe / subprocess / CI") but the one-shot paths are explicitly built for script invocation. v0.7.1 documented the 7 launch modes.
- **Telemetry posture:** PostHog disabled; "Aucune donnée ne sort de l'hôte" claimed; per-task JSONL traces in `.ailiance-agent/runs/<task_id>/` with a secret scrubber (AWS keys, PEM, URLs, password/apiKey/secret fields). v0.9.0/0.9.1 added cross-task memory at `~/.ailiance-agent/memory/` (markdown + YAML frontmatter, `MEMORY.md` index, auto-injection at turn-1).

INFERENCE: this is a standard interactive coding-agent harness with a competent security-zone model and above-average audit posture. It has the usual agent egress surface (bash with network tools, MCP, browser, one-shot scriptability) — i.e., it *could* be driven as a fleet worker by any operator — but it ships no fleet/orchestration/multi-agent machinery, no webhook coordination, no C2. Nothing in the public code distinguishes it from Claude Code/Cline-class tools on egress capability.

---

## 2. Deployment traces: writeups, demos, scan telemetry, dashboards (OBSERVED)

**Honest negative: zero public traces of isaac-cli/agent-kiki running as an unattended agent fleet.**

- Web searches (`"isaac" OR "agent-kiki" OR "aki" ailiance demo writeup fleet deployment`; French: `isaac ailiance agent de code souverain article blog vidéo démo`) returned no writeups, demos, videos, or articles about the agent itself. Only their own repos and generic French AI-sovereignty pieces (Les-Tilleuls.coop blog on sovereign agentic AI, 2026-09-07 — no mention of isaac).
- **Their own "fleet" is an LLM-serving fleet, not an agent swarm.** `l-electron-rare/kiki-cockpit` (README = `ailiance-demo`): "Vitrine publique + console d'admin de la **flotte LLM ailiance** — 5 workers, provenance EU AI Act, chat live." Architecture (observed): FastAPI :9100 serving public React SPA + Tailscale-only admin; probes 5 inference workers (studio: Apertus/EuroLLM, macm1: Devstral, tower: Gemma 3, kxkm-ai: Qwen3-Next 80B via autossh tunnel) every 30 s; public endpoints `/api/public/healthz|models|status|router-stats` and `POST /api/public/chat` (SSE proxy to gateway :9300, rate-limited 30 req/min/IP); admin (`/api/admin/*`) gated by Tailscale header auth. Deployed via docker compose on electron-server behind Traefik. Sister projects: `ailiance` (gateway), `agent-kiki` (CLI). Public: https://www.ailiance.fr · status https://home.saillant.cc · HF orgs `electron-rare` (IP source-of-truth) + `Ailiance-fr` (distribution).
  - INFERENCE: the cockpit evidences a small, publicly-showcased **inference** fleet (5 GPU workers, EU AI Act provenance pages, EU AI Act validators at `github.com/ailiance/iact-bench`, benches at `github.com/ailiance/ailiance-bench`). Nothing in it shows agent *runs* — it dashboards worker health, model cards, chat proxy, training/eval runs. No scan telemetry or third-party dashboards referencing isaac agent deployments were found.
- No npm-download anomaly, no Shodan/Censys-style telemetry surfaced in public search for `isaac`/`aki` agent deployments (and I did not probe any host — per hard rules).

---

## 3. Mirror vs primary divergence (OBSERVED)

- `L-electron-Rare/agent-kiki` README at HEAD renders **identical** to `ailiance/ailiance-agent` README at HEAD (both 972 lines, `# ISAAC` header, `CLI : isaac`, same v0.5.0-beta / v0.4 sections, same local-stack docs refs). → the mirror is a synced copy of the post-rebrand tree; no tradecraft-relevant divergence in the README surface.
- `ebii/agent-ailiance` is the divergent one: it is frozen in the **pre-rebrand era** — `# agent-kiki`, CLI `aki` (alias `agent-kiki`), gateway `eu-kiki`, trace dir `.agent-kiki/runs/`, install via `npm install -g agent-kiki`, `.vsix` named `agent-kiki-0.3.1.vsix`. Same v0.5.0-beta/v0.4 content otherwise, same Jina :5050 / LiteLLM :4000 local-stack design, same tool set.
- INFERENCE: no tradecraft divergence between mirror and primary — the only differences are branding snapshots of the same codebase at different rename stages (agent-kiki/aki → ailiance-agent → ISAAC/isaac). Code-level comparison of tool handlers would require the authenticated GitHub code-search surface; from public docs, the tool inventory (27 `IsaacDefaultTool`: read_file/write_to_file/execute_command primary) is unchanged across variants.

---

## 4. zcode-skills `~/.hermes/profiles/SOUL.md` — assessment (content analysis only)

Fetched: `https://raw.githubusercontent.com/mwanaitech/zcode-skills/HEAD/skills/multi-agent-orchestration/SKILL.md` (882 lines).

**OBSERVED — the skill is written explicitly FOR a public "Hermes" agent platform:**
- Frontmatter: `description: Install SkillHub skill packs, create specialized Hermes profiles, …`; tags include `hermes`.
- References throughout: `hermes` CLI (`hermes profile create --clone`, `hermes cron sync`, `hermes kanban assignees`, `hermes kanban run`, `hermes mcp list`, `hermes config set kanban.dispatch_in_gateway true`); paths `~/.hermes/orchestration/trinity/`, `~/.hermes/crons.yaml`, `~/.hermes/skills/`, `~/.hermes/profiles/<agent>/SOUL.md` (e.g. `~/.hermes/profiles/prime/SOUL.md`); `~/.hermes/daily-bilan/`; a `memory()` action interface with a 2200-char cap; Kanban dispatch; a `TRINITY` Fast Coordinator (sep-CMA-ES trained head, qwen2.5-0.5b-instruct meta-router on Cloudflare Workers AI, llama-3.1-8b-instruct workers, claude-sonnet-4 PRIME on AWS Bedrock); SkillHub marketplace (skillhub.cn slugs); and a pitfalls section referencing `metadata: {"clawdbot":...}` frontmatter from other SkillHub skills.
- Public corroboration that "Hermes Agent" is a known public ecosystem: a public LinkedIn post (Alexander Mamaev, ~2026-08) describes a sovereign stack using "**Hermes Agent as the orchestrator**" with LiteLLM routing between local Qwen3-Coder-30B and cloud pools. URL: https://www.linkedin.com/posts/sashamamaev_agenticai-localllm-sovereignai-activity-7455714749402763265-iNDe

**ASSESSMENT: shared/borrowed public pattern, not evidence of a private link.** The skill is community tooling targeting the public Hermes platform's documented conventions (profiles/SOUL.md, crons, kanban, skillhub). Overlap with our stack vocabulary is expected *because the skill is addressed to Hermes users* — it aggregates public patterns (it also borrows from SkillHub/clawdbot conventions and references Gabon regional constraints, i.e. a community author, not a single stack's insider). Borrowing *direction* cannot be established from content alone, and nothing in the skill evidences anything beyond public community reuse. Grade: convergent/borrowed pattern — **not a lead for swarm activity**.

---

## 5. git.saillant.cc public visibility (OBSERVED, read-only)

- Forge root `https://git.saillant.cc/` **is publicly readable**: "L'Électron Rare — Forge — Forge logicielle auto-hébergée — systèmes embarqués, IA & hardware." Gitea-based (Gitea Actions CI/CD, npm/pip/docker packages), **166+ repositories**, self-hosted.
- Public explore index `https://git.saillant.cc/explore/repos` renders repo cards (recently-updated: ESP32/hardware/creative-coding projects — e.g. "Parcours 5 jours Contrôleur Créatif MIDI/OSC/Art-Net", ESP32-S3 firmware, LDraw mirrors; most recent 2026-10-02).
- **The claimed primary repos are NOT in the public index:** `git.saillant.cc/ailiance/isaac-cli` → HTTP 404; `git.saillant.cc/ailiance` → 404; forge search `?q=isaac`, `?q=ailiance`, `?q=kiki` → "No matching results found."
- No login attempted (per hard rules).

INFERENCE: the ailiance org repos on the primary forge are either **private** or live under different slugs; the public GitHub copies are currently the only publicly readable source of the code. Deeper forge mining (authenticated session, org enumeration) requires a browser-equipped worker and is outside this worker's scope — flagged as the open frontier item.

---

## Open items for the coordinator

1. Primary-forge mining of git.saillant.cc needs a browser-equipped worker (passive reads only): the `ailiance` org exists on GitHub but is invisible in the forge's public index — private repos, renamed org, or slug drift. The forge is Gitea; its public API swagger is exposed (`/api/swagger`) but unauthenticated repo listing already shows nothing for isaac/ailiance/kiki.
2. Code-level verification of the tool-handler inventory (27 `IsaacDefaultTool`) and any network-call sites would need authenticated GitHub code search (`gh api /search/code`) — out of scope for this passive worker.
3. `gateway.ailiance.fr` (public since v0.6.1 via Cloudflare Tunnel) was not fetched — flagged, not probed, per hard rules.

## Final grade

**HONEST NEGATIVE on the swarm question; LEAD pattern downgraded to characterized-benign.**

- isaac-cli (aka agent-kiki / ailiance-agent / ISAAC) is a **declared, Apache-2.0, EU-sovereign interactive coding-agent harness** (Dirac/Cline fork lineage, EU AI Act JSONL tracing, telemetry stripped). It does not constitute an agent swarm, and **no public evidence** was found of it being deployed as an unattended agent fleet (no writeups, demos, scan telemetry, or agent-run dashboards; their own "fleet" is a 5-worker LLM *inference* fleet with a public showcase cockpit).
- The wave-1 LEAD on "Jina baked into the runtime" is **resolved as benign**: the Jina component is a local `jina-embeddings-v2-small-en` embeddings model (HuggingFace download, localhost-only) used for intent classification → model routing. No jina.ai Reader API, no web-fetch relay, no exfil primitive. Keep the vocabulary as a scan reference; drop it as an egress signal.
- The harness ships standard agent egress surface (bash incl. curl/ssh in a confirm-zone, MCP allow-all default, browser tool, one-shot scriptable modes) but no fleet/orchestration/C2 machinery. Mirror (`L-electron-Rare/agent-kiki`) is a synced copy of the primary — no tradecraft divergence; the `ebii/agent-ailiance` fork is just an older branding snapshot.
- The `~/.hermes/profiles/SOUL.md` overlap in `mwanaitech/zcode-skills` is **convergent/borrowed public pattern** (community skill targeting the public Hermes platform) — not a link, not a swarm signal.
