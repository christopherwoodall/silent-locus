---
language:
- en
license: apache-2.0
task_categories:
- text-generation
tags:
- tool-calling
- function-calling
- agent
- hermes
- reasoning
- sharegpt
- sft
- quality-filtered
- agentic
size_categories:
- 1K<n<10K
---

# Hermes Agent Reasoning Traces - Quality Filtered

A structurally filtered subset of [lambda/hermes-agent-reasoning-traces](https://huggingface.co/datasets/lambda/hermes-agent-reasoning-traces), pruned from 7,646 to **3,679 rows** using automated quality analysis targeting reasoning depth, structural integrity, and tool-call validity.

## Why This Matters for Agent Training

Most agentic datasets teach models *what tool to call* but not *how to reason about tool selection*. The difference matters in production: an agent that dispatches tools without reasoning will chain incorrect calls, miss edge cases, and fail to recover from errors. An agent that thinks before acting will catch parameter mismatches, consider alternative approaches, and adapt when tools return unexpected results.

The original dataset has the right format - full multi-turn trajectories with `<think>` blocks, `<tool_call>` invocations, and `<tool_response>` results. But roughly half the rows contain shallow or absent reasoning traces that teach the model to skip the thinking step entirely. Training on those rows actively degrades agentic capability by reinforcing "call first, think never."

This filtered version keeps only rows where the model demonstrates genuine deliberation before acting:

- **Self-correction**: The model catches its own mistakes mid-reasoning ("wait, that parameter isn't right", "actually I should check X first")
- **Verification**: The model validates tool responses before proceeding ("does this result make sense?", "let me confirm before the next step")
- **Alternative exploration**: The model considers multiple tool strategies before committing ("I could use search_files or grep the terminal directly")
- **Error recovery**: When a tool fails, the model reasons about why and adapts its approach rather than retrying blindly

These are the patterns that separate a reliable agent from a brittle one.

This filtered set is designed to be used as a high-quality Stage 2 dataset on top of strong reasoning models, helping them develop deliberate tool selection, verification, and error recovery behaviors. A model that already reasons well from Stage 1 training will carry that depth into its tool-calling behavior when fine-tuned on this data - thinking carefully before acting rather than dispatching tools reflexively.

## What Was Filtered

Every row was scored across multiple quality dimensions using automated structural analysis. Rows were kept only if they met minimum thresholds across all dimensions simultaneously. The filtering removed:

- Rows with empty or trivially short thinking traces
- Rows with malformed JSON in tool calls (100% valid JSON in filtered set)
- Rows lacking evidence of deliberate tool selection reasoning
- Rows without self-correction or verification patterns in thinking
- Rows with uniform or absent reasoning flow (no structural progression)

No rows were modified - this is a strict subset of the original data.

## Key Metrics

| Metric | Original (7,646) | Filtered (3,679) | Change |
|---|---|---|---|
| Thinking depth (words/row) | 416 | **581** | +40% |
| Self-correction present | 6.0% | **63.0%** | +10.5x |
| Verification present | 26.5% | **95.9%** | +3.6x |
| Alternative exploration | 3.1% | **43.7%** | +14x |
| Valid JSON (all tool calls) | ~87% | **100%** | clean |
| Error recovery patterns | 93.2% | **99.4%** | +6.7% |
| Multi-turn (>5 messages) | 95.2% | **97.8%** | +2.7% |
| Tool calls per conversation | 15.9 | **18.5** | +16% |
| Messages per conversation | - | **32.1 avg** | deep trajectories |

## Quality Comparison

![Quality Comparison](quality_comparison.png)

The filtering shifts the thinking depth distribution rightward (shallow traces removed) while dramatically increasing self-correction and alternative exploration density across all rows.

## Reasoning Flow Analysis

![Reasoning Flow](reasoning_flow.png)

Marker density measured across 20 equal segments of each thinking trace (left = start of thinking, right = end). The filtered set shows a tighter standard deviation band, meaning more consistent reasoning structure across rows. Both sets show the characteristic ramp-up pattern where reasoning intensifies as the model approaches a tool call decision.


## Metrics Summary

![Metrics Summary](metrics_summary.png)

## Category Distribution

![Categories](categories.png)

9 categories maintained with coverage across Repository Tasks, Agent Tools, Terminal & Coding, Browser Automation, Multi-Tool, File Operations, Scheduling, Planning, and Conversational scenarios.

## Conversation Structure

![Conversation Structure](conversation_structure.png)

Conversations average 32 messages and 18 tool calls per trajectory. These are complete agentic sessions - not single-shot dispatches.

## How This Compares to Other Agentic Datasets

| Metric | **This Dataset** | **Carnice GLM-5** ([kai-os](https://huggingface.co/datasets/kai-os/carnice-glm5-hermes-traces)) |
|---|---|---|
| **Rows** | 3,679 | 1,627 |
| **Source model** | Multiple frontier models | GLM-5 via OpenRouter |
| **Think block depth** | **581 words avg** | 40 words avg |
| **Self-correction** | **63.0%** | 29.7% |
| **Verification** | **95.9%** | 63.7% |
| **Alternative exploration** | **43.7%** | 51.3% |
| **Valid JSON (all tool calls)** | **100%** | 100% |
| **Tool calls per conversation** | **18.5** | 5.4 |
| **Messages per conversation** | **32.1** | 12.1 |
| **Multi-turn (>5 messages)** | **97.8%** | 89.6% |

The critical difference is reasoning depth before action. This dataset contains **14x deeper think blocks** with nearly universal verification and twice the self-correction rate. Carnice traces learn tool-call formatting; this dataset teaches deliberation.

## Format

ShareGPT format compatible with Hermes/NousResearch tooling:

```json
{
  "id": "uuid",
  "conversations": [
    {"from": "system", "value": "You are a function calling AI model... <tools>[...]</tools>"},
    {"from": "human", "value": "User request..."},
    {"from": "gpt", "value": "<think>\nReasoning about which tools...\n</think>\n<tool_call>\n{\"name\": \"...\", \"arguments\": {...}}\n</tool_call>"},
    {"from": "tool", "value": "<tool_response>\n{...}\n</tool_response>"},
    {"from": "gpt", "value": "Final response based on tool results..."}
  ],
  "tools": "[tool definitions JSON]",
  "category": "...",
  "subcategory": "...",
  "task": "..."
}
```

## Tools Covered

55 unique tools including `terminal`, `write_file`, `read_file`, `search_files`, `browser_navigate`, `browser_click`, `browser_snapshot`, `patch`, `todo`, `execute_code`, and more.

## Usage

```python
from datasets import load_dataset

ds = load_dataset("DJLougen/hermes-agent-traces-filtered", split="train")
```

## Recommended Use

- **Stage 2 fine-tuning** after reasoning SFT - the model already knows how to think, this teaches it when and how to use tools
- **LoRA training** with lower learning rate (5e-5) and rank (16) to preserve base reasoning capabilities
- **Sequence length**: 16384 tokens recommended (80%+ of rows fit within this)
- **1 epoch** to avoid overwriting base model capabilities

## Source & License

Filtered from [lambda/hermes-agent-reasoning-traces](https://huggingface.co/datasets/lambda/hermes-agent-reasoning-traces). Apache 2.0 license.

## Citation

If you use this dataset, please cite both the original and this filtered version:

```
@misc{hermes-agent-traces-filtered,
  author = {DJLougen},
  title = {Hermes Agent Reasoning Traces - Quality Filtered},
  year = {2026},
  publisher = {Hugging Face},
  url = {https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered}
}
```
