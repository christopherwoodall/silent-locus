---
license: apache-2.0
task_categories:
  - text-generation
language:
  - en
tags:
  - tool-calling
  - function-calling
  - agent
  - hermes
  - reasoning
  - sharegpt
  - sft
  - traces
size_categories:
  - 10K<n<100K
configs:
  - config_name: kimi
    data_files:
      - split: train
        path: data/kimi/train.parquet
  - config_name: glm-5.1
    data_files:
      - split: train
        path: data/glm-5.1/train.parquet
---

# Hermes Agent Reasoning Traces

Multi-turn tool-calling trajectories for training AI agents using the [Hermes Agent](https://github.com/nousresearch/hermes-agent) harness. Each sample is a real agent conversation with step-by-step reasoning (`<think>` blocks) and actual tool execution results.

This dataset has two configs, one per source model:

| Config | Model | Samples |
|--------|-------|---------|
| **kimi** | Moonshot AI Kimi-K2.5 | 7,646 |
| **glm-5.1** | ZhipuAI GLM-5.1-FP8 | 7,055 |

## Loading

```python
from datasets import load_dataset

# Kimi-K2.5 traces
ds = load_dataset("lambda/hermes-agent-reasoning-traces", "kimi", split="train")

# GLM-5.1 traces
ds = load_dataset("lambda/hermes-agent-reasoning-traces", "glm-5.1", split="train")
```

## Schema

Both configs share the same schema:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | UUID identifier |
| `conversations` | list | Multi-turn dialogue (system, human, gpt, tool messages) |
| `tools` | string | JSON tool definitions available to the agent |
| `category` | string | High-level task category |
| `subcategory` | string | Fine-grained task type |
| `task` | string | Task description (from user prompt) |

Conversation messages use ShareGPT format:

```json
{"from": "system|human|gpt|tool", "value": "..."}
```

- `<think>` blocks contain chain-of-thought reasoning
- `<tool_call>` blocks contain function invocations
- `<tool_response>` blocks contain real execution results

## Statistics

| Metric | kimi | glm-5.1 |
|--------|------|---------|
| Samples | 7,646 | 7,055 |
| Total turns | 185,798 | 134,918 |
| Total tool calls | 106,222 | 68,328 |
| Avg turns per sample | 24.3 | 19.1 |
| Avg tool calls per sample | 13.9 | 9.7 |
| Avg `<think>` depth (words) | 414 | 70 |

## Categories

Both configs use a shared 9-category taxonomy:

| Category | kimi | glm-5.1 |
|----------|-----:|--------:|
| Terminal & Coding | 2,010 | 2,237 |
| Agent Tools | 1,474 | 2,775 |
| Repository Tasks | 1,109 | 1,022 |
| Browser Automation | 1,048 | 639 |
| Multi-Tool | 807 | 52 |
| File Operations | 757 | 134 |
| Scheduling | 204 | 104 |
| Planning & Organization | 201 | 92 |
| Conversational | 36 | 0 |

## Generation Details

### Kimi-K2.5
- **Model:** `moonshotai/Kimi-K2.5` (MoE)
- **Inference:** vLLM with `--tool-call-parser kimi_k2 --reasoning-parser kimi_k2 --enable-auto-tool-choice`

### GLM-5.1
- **Model:** `zai-org/GLM-5.1-FP8`
- **Inference:** vLLM with `--tool-call-parser glm47 --reasoning-parser glm45 --enable-auto-tool-choice`
- **Serving:** 3x 8xH100 nodes via load-balanced gateway
- **Context:** 202,752 tokens max, MTP speculative decoding

Both datasets were generated using the [hermes-agent-generator](https://github.com/nousresearch/hermes-agent) pipeline with **real tool execution** (terminal commands, file operations, browser actions) — not synthetic outputs.

## Data Sources

Both datasets include trajectories across the same task categories:

- **Terminal & Coding** — script writing, debugging, environment setup, data processing, testing, documentation
- **Browser Automation** — Playwright-based navigation, scraping, form filling, screenshot analysis
- **Agent Tools** — Hermes-specific capabilities: memory persistence, task delegation, skill management, todo planning, code execution, session recall
- **Repository Tasks** — real codebase work across GitHub repos: bug fixes, feature implementation, test writing, code review, refactoring

## License

Apache 2.0
