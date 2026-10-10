# GITHUB-SEARCHER findings — German/French agent skill/harness code footprint

**Worker:** GITHUB-SEARCHER · **Date:** 2026-10-05 · **Method:** web-search snippets only (browser.search, passive). No fork-network/contributor analysis performed — code CONTENT only. No candidate infrastructure fetched or probed.

## Queries run

| # | Query (angle) | Result |
|---|---|---|
| Q1 | `site:github.com SKILL.md agent "Schritt" OR "Werkzeug" OR "Aufgabe" Anthropic` | 7 hits |
| Q2 | `site:github.com SKILL.md agent "étape" OR "outil" OR "tâche" Mistral` | 6 hits |
| Q3 | `site:github.com agent framework README "German" KI-Agent "Aufgaben" autonomous` | 7 hits |
| Q4 | `site:github.com Mistral agent harness python français commentaires webhook` | 8 hits |
| Q5 | `site:github.com agent "webhook" python "# Die" OR "# Die Aufgabe" OR "# Schritt" agent harness` | 0 |
| Q6 | `site:github.com agent python "jina.ai" OR "webhook.site" OR "ngrok" commentaire "# Envoie" OR "# Récupère"` | 0 |
| Q7 | `site:github.com "agent de" OR "agent francophone" Mistral "Le Chat" skill développeur outils autonomes` | 0 |
| Q8 | `site:github.com ki-agent harness python "Werkzeuge" "Schritte" autonom kommentare tool loop` | 0 |
| Q9 | `site:github.com SKILL.md "base64" agent "exfiltrate" OR "exfiltration" OR "Envoie" OR "Récupère"` | 0 |
| Q10 | `site:github.com python agent "def agent_loop" "# Erstelle" OR "# Hole" OR "# Sende" github` | 0 |
| Q11 | `site:github.com Mistral "agent" python "# Crée" OR "# Exécute" OR "# Envoie" requests` | 5 hits |
| Q12 | `site:github.com "KI-Agent" OR "KI-Agenten" ReAct loop tools python autonomous coding comments` | 6 hits |
| Q13 | `site:github.com agent harness français python jina webhook tunnel base64 commentaires` | 7 hits (mixed) |
| Q14 | `site:github.com KI-Agent harness deutsch python webhook tunnel base64 kommentare` | 6 hits (mixed) |
| Q15 | `site:github.com "webhook" "Agent" python "# " commentaire "tâche" agent boucle outils autonomes` | 0 |
| Q16 | `site:github.com agent "SKILL.md" français "multi-agent" OR "agents autonomes" compétences outils egress` | 3 hits |
| Q17 | `site:github.com skills agent "Deutsch" webhook tunnel jina ngrok "AGENTS.md"` | 0 |

## Findings (graded)

### CONFIRMED — German-language agent skill/harness code exists on GitHub (general, benign-so-far)

**F1.** `mberto10/mberto-compound` — `plugins/langdock-dev/skills/assistant-prompt-craft/SKILL.md`
German skill for crafting agent prompts. Observed snippet: `Du bist [ROLLE] mit Zugriff auf spezialisierte Werkzeuge für [ZWECK]` and template sections `## Deine Aufgaben`, `## Verfügbare Werkzeuge`, `## Arbeitsweise`. Uses exactly the German agent-grammar terms (Werkzeug, Aufgabe, Schritt).
URL: https://github.com/mberto10/mberto-compound/blob/HEAD/plugins/langdock-dev/skills/assistant-prompt-craft/SKILL.md

**F2.** `toqsick/my-agent-tools` — multiple German SKILL.md files (`library/yuno-user-preferences/SKILL.md`, `library/note-taking/system-documentation/SKILL.md`)
Fully German agent-skill content: tables with "Phase / Zweck / Werkzeug / Output", instruction `Nutze die Exa-Suche für:`, templates with `## Vorgehen` numbered steps. Personal-assistant skill set, not tradecraft.
URL: https://github.com/toqsick/my-agent-tools/blob/HEAD/library/yuno-user-preferences/SKILL.md

**F3.** `thomasschmiegelt/ai_framework` — `CLAUDE.md`
German agent-harness docs (tool loop in German). Observed: `Autonomer Coding-Agent (Agent-Harness, „🤖 Agent"): SSE-Endpoint POST /api/code/agent ... = eigener Werkzeug-Loop (Muster wie der Chat-Tool-Loop) mit list_files/read_file/write_file/run_python ... iteriert bis max_steps`.
URL: https://github.com/thomasschmiegelt/ai_framework/blob/HEAD/CLAUDE.md

**F4.** `jnsfhrmnn/jf-agentic-coding-starter-kit` — `docs/git-basics.md`
German orchestrator/worker agent workflow docs. Observed: `Ein Agent ist der Orchestrator (Dirigent)... Jeder weitere Agent ist ein Worker mit eigenem, dauerhaftem Worktree und Branch.`
URL: https://github.com/jnsfhrmnn/jf-agentic-coding-starter-kit/blob/HEAD/docs/git-basics.md

**F5.** `fpeterma/intentron` — bilingual agent governance framework README ("INTENTRON — Governance für KI-gestützte Entwicklung", PolyForm Perimeter license).
URL: https://github.com/fpeterma/intentron

**F6.** `janschachtschabel/lehrtoolkit` — German education SKILL.md project (teacher skills, OER search). INFERENCE: benign ed-tech, not tradecraft.
URL: https://github.com/janschachtschabel/lehrtoolkit

### CONFIRMED — French-language agent skill/harness code exists on GitHub (general, benign-so-far)

**F7.** `mwanaitech/zcode-skills` — `skills/multi-agent-orchestration/SKILL.md`
French multi-agent orchestration skill. Observed: `### Formation des Agents ... 1. **Tâche 1** : Description. ... ## 🛠️ Outils Autorisés - outil1 : Description.` Uses French agent-grammar terms (tâche, outil, étape). Notable: references Hermes-style artifacts (`~/.hermes/profiles/<agent>/SOUL.md`, Hermes crons) — same SOUL.md pattern seen in the user's own Hermes stack. INFERENCE: community pattern reuse, not necessarily a link.
URL: https://github.com/mwanaitech/zcode-skills/blob/HEAD/skills/multi-agent-orchestration/SKILL.md

**F8.** `paaaddy/lns-skill-copilot-agent-builder` — `SKILL.md` (French agent-builder skill with numbered Étapes).
URL: https://github.com/paaaddy/lns-skill-copilot-agent-builder/blob/HEAD/SKILL.md

**F9.** `mbrandone/book-creator` — `.claude/skills/technical-scoping/SKILL.md`
French procedural content (`### IMPORTANT : Créer les Tâches dans Claude Code`, TaskCreate usage). Benign coding-assistant skill.
URL: https://github.com/mbrandone/book-creator/blob/HEAD/.claude/skills/technical-scoping/SKILL.md

**F10.** `prendstapart/plugin-claude-mcp-braindcode-` — `rapidorh/skills/job-post-builder/SKILL.md`
French adaptation of an Anthropic knowledge-work skill to a French HRIS (RapidoRh) via MCP tools. Observed: tool-mapping table `Outil cité dans ce skill | Équivalent à utiliser ici` with French MCP tool names (`get-users-list-tool`, `create-task-list-tool`, ...).
URL: https://github.com/prendstapart/plugin-claude-mcp-braindcode-/blob/HEAD/./rapidorh/skills/job-post-builder/SKILL.md

**F11.** `calopsys/baudrier` — `skills/add-agent/SKILL.md`
French SKILL.md for a Mistral-default agent generator. Observed: `J'utilise mistral-small-3.2-24b-instruct-2506 par défaut` on Scaleway Generative APIs — direct Mistral-ecosystem agent project in French.
URL: https://github.com/calopsys/baudrier/blob/HEAD/skills/add-agent/SKILL.md

**F12.** `franckolv-dev/elyagent` — French agent harness. Observed from commit message text (commit 3e1a91ca10868b5bffc90f8dd99f0007c52b56d3): a tool-call keyword regex with French read/action verbs (regarde, consulte, vérifie, ouvre, envoie, exécute, tâche), Gemma 4 E4B local inference, Chrome-extension browser tools. INFERENCE: French homebrew agent harness with French-language trigger logic.
URL: https://github.com/franckolv-dev/elyagent/commit/3e1a91ca10868b5bffc90f8dd99f0007c52b56d3

### LEAD — French EU-sovereign agent harness with Jina egress reference

**F13.** `ailiance/isaac-cli` (mirror of `L-electron-Rare/agent-kiki`)
EU-sovereign autonomous coding agent (fork of Dirac/Cline), French README and French UI strings. OBSERVED (from fetched README):
- `Agent de code souverain — extension VS Code + CLI Ink, audit JSONL EU AI Act`
- Local stack auto-detect: `🏠 Local stack — Jina :5050 / LiteLLM :4000 (auto-detect)` and `useLocalStack` setting `Active l'auto-detect Jina :5050 / LiteLLM :4000`
- v0.4: `Local stack (isaac stack {start,stop,status}): managed LiteLLM proxy + Jina semantic router`
- 27 canonical tools (`IsaacDefaultTool`): `read_file` / `write_to_file` / `execute_command`
- Primary forge: `git.saillant.cc/ailiance/isaac-cli` (GitHub = mirror/backup); 730 commits; created 2026-05-04; gateway `https://gateway.ailiance.fr/v1`
- EU AI Act-compliant JSONL tracing in `.ailiance-agent/runs/<task_id>/`

INFERENCE: this is a declared EU-sovereignty project (open, licensed, EU AI Act posture), not a hidden swarm. However it is the strongest public example of the exact pattern the hunt is after: a French-commented agent harness that bakes Jina into its runtime stack (an egress primitive). Worth keeping as the reference pattern when scanning other DE/FR agent repos for Jina/webhook/tunnel code.

### LEAD — German agent README with webhook architecture (German + webhooks, single data point)

**F14.** `sabriguenes/cursor` — `projects/vinnie-cppalliance-duplicate-detection/CONSULTANT-PAPER-AGENT-ARCHITECTURE.md`
German architecture doc describing a "Webhook Router" between GitHub and KI-Agenten: `Dieser Webhook landet bei unserem FastAPI Server ... FastAPI startet den Review Agent`. Individual architecture note, not a tradecraft kit.
URL: https://github.com/sabriguenes/cursor/blob/HEAD/projects/vinnie-cppalliance-duplicate-detection/CONSULTANT-PAPER-AGENT-ARCHITECTURE.md

### HONEST NEGATIVES

- **N1:** Zero hits for German/French comments co-occurring with exfil-style egress code (webhooks, tunnels, jina, base64 exfil) in agent repos — queries Q5, Q6, Q9, Q10, Q15, Q17 all returned 0 results. OBSERVED: the only intersection found is F13 (French harness referencing Jina as a local semantic-router stack, framed as sovereign-local infra, not exfil).
- **N2:** Zero evidence of German/French "agent supply-chain tradecraft" kits: no DE/FR skill bundles shipping webhook dead-drops, tunnel launchers, or exfil helpers were found. The DE/FR skills found (F1, F2, F6, F7–F11) are benign productivity/HR/dev tooling.
- **N3:** Queries for French-language agent-loop variables/comments (Q7, Q15) returned nothing — French agent authors appear to write identifiers and system prompts in French but code (functions, comments) predominantly in English or mixed.
- **N4:** The Chinese MSS advisory doc found via Q3 (`continuum-ai-corp/orca-ai-incident-archive/.../2026-09-17-china-mss-agent-advisory.md`) describes the DseWiki incident (German programmer wiki turned agent forum, 10k+ messages, OpenAI-attributed agents). OBSERVED: the incident archive itself carries German/French/Japanese/Korean summaries — a multilingual incident-archive artifact, not a DE/FR swarm's code.

## Open items / recommended follow-ups

1. GitHub code search (authenticated `gh api /search/code`) for exact strings `"# Schritt"`, `"# Aufgabe"`, `"tâche"` in `*.py` agent files — search-engine snippets can't see inline code comments reliably; the GitHub code search index would be the direct tool (out of scope for this passive worker).
2. `git.saillant.cc` (F13's primary forge, explicitly "GitHub = miroir") is an unindexed European forge surface — other EUROSWARM workers with browser access should treat it as a frontier, but ONLY passive page reads.
3. The `SOUL.md` / Hermes pattern (F7, zcode-skills) mirrors the user's own agent-stack conventions — coordinator may want to cross-check whether that pattern is a published community template or converging vocabulary.

## Undocumented endpoints found

None. No new XHR/endpoints surfaced; all sources were search snippets plus one fetched public README.
