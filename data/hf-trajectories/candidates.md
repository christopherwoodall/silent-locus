# HF trajectory/eval-run dataset candidates (2026-10-07)

Hunt for agent trajectory datasets on HuggingFace Hub beyond the three swept WildClaw sets
(internlm/WildClawBench-Trajectories 8.7GB, NAIL-Group/ClawBenchV1Trace 30.2GB, TIGER-Lab/ClawBenchV2Trace 18.9GB).

Method: curl-only Hub API (python huggingface_hub broken on this VM, see ~/TOOLS.md).
7 search terms x 100/page ("trajectories", "traces", "agent logs", "web agent", "computer use",
"claw", "agentic eval") -> 494 unique candidates -> heuristic scoring -> 41 card pulls ->
sizes via paths-info API (exact for <=1000 files, random-300-file extrapolate otherwise).
No downloads. Read-only.

Priority: P1 = direct audit (<~500MB, agent action trajectories with tool calls, model-labeled).
P2 = audit with sampling plan or >500MB. P3 = background/low-fit.

## P1 — direct audit candidates

| # | id | size | why it ranks |
|---|----|------|--------------|
| 1 | `0xSero/glm-5.2-nf3-hybrid-terminal-bench-2.1-traces` | 85.2MB exact (948 files: json/txt/log/cast) | Full agent traces, Terminal-Bench 2.1 x 89 tasks, **GLM-5.2** via Terminus-2/Harbor. Same model as the new GSMArena Turnstile defeat (GLM 5.2) found in the WildClaw audit. Model-labeled, 2026-09-01. |
| 2 | `TIGER-Lab/SWE-Next-SFT-Trajectories` | 205.8MB exact (jsonl) | Same org as ClawBenchV2Trace. SWE-Next (arXiv 2603.20691), 1K<n<10K rows, 2026. |
| 3 | `yoonholee/terminalbench-trajectories` | 210.8MB exact (2 parquet) | 10K<n<100K rows, per-trial fields: task_name, **agent, model**, reward, tokens, cost. Direct model comparison possible. |
| 4 | `TIGER-Lab/BrowserAgent-Data` | 394.1MB exact (jsonl x2) | Same org as ClawBenchV2Trace. Browser/web-agent trajectory data, 2025-10-31. |
| 5 | `DJLougen/hermes-agent-traces-filtered` | 349.1MB exact (jsonl) | 3,679 hermes-agent reasoning traces with tool calls (quality-filtered subset of lambda set). EUROSWARM cross-lane: hermes-agent cert burst (July). |
| 6 | `Crownelius/GPT-5.6-Sol-Luna-Terra-Traces` | 284.7MB exact (1 parquet) | GPT-5.6 Sol/Terra/Luna coding-agent traces, tool-use + CoT, 10K<n<100K, 2026-07-29. |
| 7 | `TIGER-Lab/SWE-QA-Pro-SFT-Trajectories` | 62.2MB exact (jsonl) | Same org, 2026-06-24, recent SWE trajectory set. Cheap pull. |
| 8 | `TIGER-Lab/BrowserAgent-SeedData` | 36.2MB exact (10 parquet) | Same org, web-agent seed trajectories. Cheap pull. |

## P2 — audit with sampling plan / over budget

| # | id | size | plan |
|---|----|------|------|
| 9 | `aisa-group/ResearchArena-Trajectories` | ~6.2GB est (37,861 files: json/txt/py) | ResearchArena red-team/control-eval: agent + **malicious side task / covert sabotage** + monitor judgements, arXiv 2607.19321, 2026-09-23. Most on-theme for rogue-agent hunt. Sample: README + a few json trajectory files first (~5MB), then per-file pull. |
| 10 | `Hcompany/trajectories` | ~2.9GB est (56,678 files: webp/json) | 7,366 Holo4 27B/35B computer-use trajectories with reasoning, actions, tool results, screenshots. Sample: json trajectory files only (~50MB), skip webp. |
| 11 | `lambda/hermes-agent-reasoning-traces` | 1.5GB exact (4 parquet) | Parent of #5. 7,646 rows, 382 likes. Pull the 4 parquet files. |
| 12 | `markov-ai/computer-use` | 2.0GB exact (16 parquet + 313 mp4) | 160 OSWorld trajectories (Gemini 3 Flash Preview), 1,378 steps. Pull parquet only (~est 50-150MB), skip mp4. |
| 13 | `greghavens/gpt-5.6-sol-coding-and-debugging-traces` | 1003.2MB exact (single jsonl) | GPT-5.6 Sol coding/debug traces with tool-use. Same bytes as ArkhAngelLifeJiggy mirror below — dedup; pull once. |
| 14 | `Tradefederation/Fable-5-traces` | ~116.6MB est (4,798 jsonl) | Fable-5 pi-agent (claude-code harness) traces, tool-use + CoT, 1K<n<10K. Fits <500MB if estimate holds — verify with a single shard first. |
| 15 | `cfahlgren1/Fable-5-traces` | 59.2MB exact (115 jsonl) | Fable-5 traces, 19 likes. Direct pull. |
| 16 | `Noddybear/computer-use-harmfulness` | 79.2KB exact (jsonl x2) | "Harmfulness" computer-use set. Trivial cost, grab it. |
| 17 | `thomasmustier/pi-computer-use-sessions` | 2.8MB exact (jsonl x7) | Pi computer-use sessions. Trivial. |
| 18 | `egygi/computer-use-large-actions` | 5.8MB exact (jsonl) | Computer-use actions. Trivial. |

## P3 — background / low-fit

| id | size | note |
|----|------|------|
| `webagentlab/webchain` | 359.5GB exact (531 parquet incl. traces/actions/windows) | Human-annotated real-world web trajectories, arXiv 2603.05295. Per-shard sample only: traces.parquet shards individually, or actions.parquet (493MB shard seen). |
| `webagentlab/webchain-legacy` | 779.5GB exact (13 parquet + split zips) | Older WebChain. Same per-shard approach. |
| `internlm/WildClawBench-Harbor` | ~7.8GB est (3,381 files: py/json/md/png) | Harbor-packaged WildClawBench from internlm (5,898 dl). Likely task definitions/harness, not runs — check README before any pull. |
| `taejoon89/Ko-Agent-Trajectories-1.0` | 1.3GB exact (565 .gz) | Korean, GLM-5.1-distilled, DPO. Non-English. |
| `MaxDevv/real-pi-coding-agent-traces-sessions` | ~1.0GB est (1,294 jsonl) | Real human-AI pi coding sessions, aggregated from 21 datasets. |
| `ArkhAngelLifeJiggy/gpt-5.6-sol-coding-and-debugging-traces` | 1003.2MB exact | Byte-size-identical mirror of #13 (greghavens). Dedup. |
| `Anish13/web-agent-graph-dataset` | 52.7MB exact (parquet+jsonl) | Web-navigation preference/reward modeling. Lower fit (no live tool calls). |
| `txchmechanicus/computer-use-large` | ~874.7GB est (48,489 mp4) | Screen recordings. No. |

## Gated (no anonymous access) — needs auth path

- `hkust-nlp/Toolathlon-Verified_Trajectories` (Toolathlon verified trajectories, 2026-08-06)
- `ST-WebAgentBench/st-webagentbench`
- `DatoricAI/computer-use-agent-traces-250k`
- `psdn-ai/computer-use-interface-samples`

## Negative / screened out

- Parquet metadata of `wildclaw_train.parquet` (720 rows, cols: task_id, trajectory, model_name, task_category) carries no dataset references — no pointers elsewhere.
- Known-set cards checked: no "related datasets" field on Hub; linkage via org listings (internlm: 27, NAIL-Group: 3, TIGER-Lab: 93 datasets) yielded the TIGER-Lab/internlm entries above. NAIL-Group has nothing beyond ClawBench/ClawBenchV1Trace/ClawBenchV2Trace.
- Game/RL traces (atari, minecraft, frogger) excluded at scoring.

## Totals

- 494 unique candidates from 7 searches (+6 org-listing adds +1 parent set).
- 41 dataset cards pulled, 41 repos sized via paths-info.
- P1: 8 | P2: 10 | P3: 8 | gated: 4.

## Raw evidence (not committed; /tmp)

- `/tmp/hft/search_*.json` — raw search responses
- `/tmp/hft/scored.txt` — heuristic ranking
- `/tmp/hft/cards.json`, `/tmp/hft/siblings.json`, `/tmp/hft/size_est.json`, `/tmp/hft/size_est2.json`, `/tmp/hft/readmes.json`, `/tmp/hft/descs.json`
