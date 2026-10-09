---
license: apache-2.0
task_categories:
- text-generation
tags:
- coding-agents
- trajectories
- terminal-bench
- benchmark
size_categories:
- 10K<n<100K
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
dataset_info:
  features:
  - name: task_name
    dtype: string
  - name: agent
    dtype: string
  - name: model
    dtype: string
  - name: reward
    dtype: int64
  - name: duration_seconds
    dtype: float64
  - name: input_tokens
    dtype: float64
  - name: output_tokens
    dtype: float64
  - name: cache_tokens
    dtype: float64
  - name: cost_cents
    dtype: float64
  - name: trial_name
    dtype: string
  - name: trial_id
    dtype: string
  - name: started_at
    dtype: string
  - name: ended_at
    dtype: string
  - name: steps
    dtype: string
  splits:
  - name: train
    num_bytes: 939348659
    num_examples: 52104
  download_size: 220993900
  dataset_size: 939348659
---

# Terminal-Bench 2.0 Trajectories

Full agent trajectories from [Terminal-Bench 2.0](https://www.tbench.ai/leaderboard/terminal-bench/2.0), a benchmark that evaluates AI coding agents on real-world terminal tasks. Each row is one trial: an agent attempting a task, with the complete step-by-step trace of messages, tool calls, and observations.

**Explorer:** [yoonholee.com/web-apps/terminal-bench](https://www.yoonholee.com/web-apps/terminal-bench/)

## Quick start

```python
from datasets import load_dataset
import json

ds = load_dataset("yoonholee/terminalbench-trajectories", split="train")

# Filter to a specific agent
opus_runs = ds.filter(lambda x: x["model"] == "claude-opus-4-6@anthropic")

# Parse steps from JSON string
row = ds[0]
steps = json.loads(row["steps"])
print(f"Task: {row['task_name']}, Agent: {row['agent']}/{row['model']}, Reward: {row['reward']}")
print(f"Steps: {len(steps)}")
```

## Dataset summary

| Stat | Value |
| --- | --- |
| Total trajectories | 52,104 |
| Tasks | 89 |
| Agent/model combos | 109 |
| Scaffolds (agents) | 26 |
| Underlying models | 49 |
| Overall pass rate | 39.6% |
| Median steps per trajectory | 21 |
| Mean steps per trajectory | 47.1 |
| Trials with trajectory steps | 34,462 |
| Trials per (task, agent) | typically 5 |

## Schema

Each row represents one trial (one agent attempting one task).

| Column | Type | Description |
| --- | --- | --- |
| `task_name` | string | Task identifier (e.g. `"chess-best-move"`) |
| `agent` | string | Agent scaffold (e.g. `"claude-code"`, `"terminus-2"`) |
| `model` | string | Underlying LLM (e.g. `"claude-opus-4-6@anthropic"`, `"gpt-5@openai"`) |
| `reward` | int64 | 1 if the agent solved the task, 0 otherwise |
| `duration_seconds` | float64 | Wall-clock duration in seconds (null for some agents) |
| `input_tokens` | float64 | Input tokens consumed (null for some agents) |
| `output_tokens` | float64 | Output tokens generated (null for some agents) |
| `cache_tokens` | float64 | Cached tokens (null for some agents) |
| `cost_cents` | float64 | Cost in cents (null for some agents) |
| `trial_name` | string | Human-readable trial name |
| `trial_id` | string | UUID for this specific trial |
| `started_at` | string | Trial start timestamp |
| `ended_at` | string | Trial end timestamp |
| `steps` | string | JSON-serialized list of step objects (see below) |

### Step format

The `steps` column is a JSON string. Each step has:

```json
{
  "src": "agent",
  "msg": "Let me check the file structure first.",
  "tools": [{ "fn": "Bash", "cmd": "ls -la" }],
  "obs": "total 42\ndrwxr-xr-x ..."
}
```

| Field | Description |
| --- | --- |
| `src` | `"user"`, `"agent"`, or `"system"` |
| `msg` | The agent's message or reasoning text |
| `tools` | List of tool calls (`null` if none). Each has `fn` (function name) and `cmd` (command/argument). |
| `obs` | Tool output / observation (`null` if none). Truncated to 5,000 chars. |

## Scaffolds

| Scaffold | Combos | Trajectories | Pass rate |
| --- | --- | --- | --- |
| terminus-2 | 32 | 17,431 | 33.6% |
| mini-swe-agent | 13 | 6,663 | 22.8% |
| openhands | 12 | 6,198 | 28.2% |
| codex | 8 | 3,532 | 45.2% |
| claude-code | 7 | 3,092 | 40.3% |
| Factory Droid | 5 | 2,224 | 67.3% |
| gemini-cli | 4 | 1,766 | 33.5% |
| mux | 4 | 1,068 | 66.2% |
| letta-code | 3 | 1,335 | 56.2% |
| goose | 3 | 1,332 | 44.2% |
| ruley | 2 | 890 | 66.3% |
| terminus-3-3 | 2 | 887 | 74.9% |

Plus 14 more single-combo agents (forge, judy, spoox-m, TerminalBenchAgent, Junie, ii-agent-simple, sage, ante, simple_codex, aone-agent, deepagent-harbor, claude-code-enhanced, final, opencode).

## Top agents by pass rate

| Agent | Pass rate |
| --- | --- |
| forge/gemini-3.1-pro-preview@Google | 78.4% |
| Factory Droid/gpt-5.3-codex@openai | 77.3% |
| simple_codex/gpt-5.3-codex@openai | 74.9% |
| terminus-3-3/claude-opus-4-6@anthropic | 74.9% |
| terminus-3-3/gemini-3.1-pro-preview@Google | 74.8% |
| judy/claude-opus-4.6@anthropic | 71.9% |
| ruley/gpt-5.3-codex@OpenAI | 70.3% |
| Factory Droid/claude-opus-4-6@anthropic | 69.9% |
| mux/gpt-5.3-codex@openai | 68.5% |
| deepagent-harbor/gpt-5.2-codex@openai | 67.7% |
| mux/claude-opus-4-6@anthropic | 66.5% |
| claude-code-enhanced/claude-opus-4-6@anthropic | 66.1% |
| sage/gemini-3-pro-preview@Google | 65.2% |
| Factory Droid/gpt-5.2@openai | 65.1% |
| ante/gemini-3-pro-preview@Google | 64.9% |

## Top agents on hard tasks

Pass rates on the official Terminal-Bench 2.0 hard split (30 tasks tagged `difficulty:hard`): bn-fit-modify, cancel-async-tasks, circuit-fibsqrt, configure-git-webserver, dna-assembly, extract-moves-from-video, feal-differential-cryptanalysis, feal-linear-cryptanalysis, fix-code-vulnerability, fix-ocaml-gc, gpt2-codegolf, install-windows-3.11, llm-inference-batching-scheduler, make-doom-for-mips, make-mips-interpreter, mcmc-sampling-stan, model-extraction-relu-logits, password-recovery, path-tracing, path-tracing-reverse, polyglot-rust-c, protein-assembly, regex-chess, sam-cell-seg, sparql-university, torch-pipeline-parallelism, torch-tensor-parallelism, train-fasttext, video-processing, write-compressor.

| Agent | Pass / Total | Pass rate |
| --- | --- | --- |
| terminus-3-3/claude-opus-4-6@anthropic | 99/147 | 67.3% |
| Factory Droid/claude-opus-4-6@anthropic | 95/150 | 63.3% |
| Factory Droid/gpt-5.3-codex@openai | 94/150 | 62.7% |
| forge/gemini-3.1-pro-preview@Google | 93/150 | 62.0% |
| terminus-3-3/gemini-3.1-pro-preview@Google | 89/150 | 59.3% |
| simple_codex/gpt-5.3-codex@openai | 85/149 | 57.0% |
| ruley/gpt-5.3-codex@OpenAI | 85/150 | 56.7% |
| judy/claude-opus-4.6@anthropic | 84/150 | 56.0% |
| mux/claude-opus-4-6@anthropic | 82/150 | 54.7% |
| claude-code-enhanced/claude-opus-4-6@anthropic | 73/134 | 54.5% |
| mux/gpt-5.3-codex@openai | 80/150 | 53.3% |
| Junie/gemini-3-flash-preview@gemini | 78/150 | 52.0% |
| deepagent-harbor/gpt-5.2-codex@openai | 68/141 | 48.2% |
| ante/gemini-3-pro-preview@Google | 72/150 | 48.0% |
| Factory Droid/claude-opus-4-5-20251101@anthropic | 72/150 | 48.0% |

## Data source

Trajectories were scraped from [tbench.ai](https://www.tbench.ai/) using the publicly available leaderboard data.

## License

Apache 2.0.
