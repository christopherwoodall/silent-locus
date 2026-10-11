# RECON: lay of the land in public datasets

Scout date: 2026-10-03. All keyless, read-only, metadata/catalog only — no dataset downloads.
Scope: agents and agent infrastructure only; dataset metadata, never humans.

## Kaggle (keyless API works)

| Dataset | Owner | Date | Size | DL | Relevance |
|---|---|---|---|---|---|
| AI Agent Cybersecurity Dataset 2026 | Uneeb Zulfiqar | 2026-06-25 | 1.4 MB | 2,314 | MEDIUM — likely synthetic benchmark rows; contents unverified |
| Agentic Tool-Use & Multi-API Orchestration 2026 | beatsprom | 2026-09-04 | 363 KB | 313 | MEDIUM — tool-use shaped; synthetic probable |
| LLM Agent Failure Analysis Benchmark Dataset | sunil kumar | 2026-06-27 | 106 KB | 238 | LOW-MEDIUM — failure analysis, not traces |
| AI Agent Attack-to-Mitigation Knowledge Graph | — | 2026 | 27 KB | — | LOW — knowledge graph, not behavior |
| AI Agent Observability Dataset | — | 2026 | 418 KB | — | LOW-MEDIUM — observability telemetry shape |
| Mind2Web | — | — | 468 MB | — | LOW — web-task benchmark, pre-incident era |

Verdict: Kaggle's agent datasets are individual-uploader benchmark/synthetic sets. Nothing with real 2026 incident traces. Not a trace source; possibly useful as eval-shape reference only.

## HuggingFace (keyless API)

| Dataset | Date | DL | Gated | Relevance |
|---|---|---|---|---|
| thomasmustier/pi-computer-use-sessions | 2026-06-18 | 223 | open | MEDIUM-HIGH — real computer-use session JSONLs (Apr 2026), tagged `format:agent-traces`; coding-agent population, not web, but genuine tool-use traces in-window |
| youdotcom/minimax-m3-deepsearchqa-skill-eval | 2026-09-11 | 377 | open | MEDIUM-HIGH — `trajectories.jsonl` + `graded.jsonl` for a DeepSearchQA skill eval; directly relevant to our eval-attribution machinery |
| Tevatron/BrowseComp-Plus-results | 2026-09-24 | 888 | open | MEDIUM — `agent_results.csv` for BrowseComp runs; may show tool-use patterns |
| taejoon89/Ko-Agent-Trajectories-1.0 | 2026-09-23 | 289 | open | LOW-MEDIUM — Korean agent trajectories, coding-flavored |
| rogue-security/coding-agent-security-benchmark | 2026-07-28 | 256 | open | MEDIUM — prompt-injection/red-team agent safety benchmark; eval-breakout shape adjacent |
| nebius/SWE-agent-traces etc. | 2024–2025 | — | open | LOW — SWE coding agents, wrong population and era |

Verdict: no HF dataset holds 2026 web-agent incident traces. Closest real-behavior items are pi-computer-use-sessions and the minimax DeepSearchQA trajectories — worth a peek for relay/proxy tool-use if we ever need a control population.

## Internet Archive advancedsearch (keyless)

- `identifier:*agent*` year 2026: 436 hits, all noise (movies, TV rips, podcasts, spam uploads). No incident datasets.
- `transluce`: 3 hits, all irrelevant (old books, CIA reading room).
- `title:(rogue agent)` 2026: 0 hits.
- Notable absence: nobody has archived incident datasets, Transluce's releases, or swarm corpora as IA items. The IA *item* layer is empty for this topic (the IA *web* layer is where our traces live — different thing).

Verdict: dead end as a catalog; no new datasets.

## GitHub (keyless search API)

| Repo | Created | What |
|---|---|---|
| **sage-princeton/swarmchaser** | 2026-09-25 | **HIGH** — Princeton team systematizing published incident datasets into one canonical provenance-preserving event format; extracting shared identifiers (handles, naming conventions, relay/proxy/shortener services, egress networks, timelines); staged branches stage-2 (collusion-wiki) through stage-10 (enrichment) covering transluce, swarmtraces, rubyhack; explicit "hunt for more" phase. Direct parallel effort — cross-reference their indicators against ours |
| kmad/agent-swarm-forensics | 2026-09-05 | MEDIUM — forensic reproduction of the collusion.wiki incident: runnable scripts, verified dataset, live-state audit |
| Continuum-AI-Corp/Orca-AI-Incident-Archive | 2026-09-18 | Known — already in our watch set |
| Edimah/agentic-collusion-detector-in-public-logs | 2026-09-14 | LOW-MEDIUM — hackathon submission repo |

## The 3 most hunt-relevant finds

1. **sage-princeton/swarmchaser** — a Princeton team running the same systematization play we are (canonical event format, shared-identifier extraction across handles/relays/timelines, active hunt phase). Their staged pipeline already covers collusion-wiki, Transluce, swarmtraces, and rubyhack. Watch/cross-reference: if their indicators match ours independently, that's corroboration; where they differ, that's a lead.
2. **thomasmustier/pi-computer-use-sessions** (HF, open) — real April-2026 computer-use traces tagged agent-traces. Wrong population (coding agents) but the only open, in-era, genuine tool-use trace dataset found. Control-population candidate.
3. **Kaggle's AI Agent Cybersecurity Dataset 2026** (2,314 DL, June 2026) — the most-downloaded agent dataset on Kaggle; likely synthetic but unexamined. Low cost to rule in/out later.

## Surprises
- Kaggle's API is fully keyless and queryable — a usable future sweep surface.
- Nobody has put incident datasets on IA as items, and Transluce hasn't archived their releases there either — the "publish the data" norm hasn't reached IA.
- The parallel-effort density is high: Princeton (swarmchaser), orca archive, kmad forensics, Edimah detector — at least four independent teams systematizing the same incidents in Sep 2026. The field is converging; our differentiator remains the machinery-first inversion (nobody else is hunting by toolkit grammar).
