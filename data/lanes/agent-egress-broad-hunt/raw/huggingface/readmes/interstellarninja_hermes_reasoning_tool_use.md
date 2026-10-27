---
dataset_info:
  features:
  - name: conversations
    list:
    - name: from
      dtype: string
    - name: value
      dtype: string
  - name: tools
    dtype: string
  - name: task
    dtype: string
  - name: category
    dtype: string
  - name: source
    dtype: string
  - name: scenario_category
    dtype: string
  splits:
  - name: train
    num_bytes: 392580349
    num_examples: 51004
  download_size: 130992200
  dataset_size: 392580349
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
license: apache-2.0
task_categories:
- question-answering
language:
- en
tags:
- tool-use
- json-mode
- reasoning
- rl
size_categories:
- 10K<n<100K
---

## TL;DR
**51 004 ShareGPT conversations** that teach LLMs *when*, *how* and **whether** to call tools.  
Built with the **Nous Research Atropos** RL stack in [Atropos](https://github.com/NousResearch/atropos) using a custom `MultiTurnToolCallingEnv`, and aligned with **BFCL v3** evaluation scenarios.  
Released by **@interstellarninja** under **Apache-2.0**.

---

## 1 Dataset Highlights

| Count  | Split  | Scenarios covered                               | Size |
|-------:|:------:|-------------------------------------------------|------|
| 51 004 | train  | single-turn · multi-turn · multi-step · relevance | 392 MB |

* Each row: OpenAI-style `conversations`, per-episode `tools` schema, scenario label, source tag.  
* Stored as ShareGPT conversations format for finetuning for tool-use with libraries such as axolotl.

---

## 2 Scenario Taxonomy (BFCL v3)

| `scenario_category` | Definition (BFCL)                                               | Manifestation here |
|---------------------|-----------------------------------------------------------------|--------------------|
| `single_turn`       | 1 user request → **1** valid tool call                          | Assistant emits exactly one `<tool_call>` block |
| `multi_turn`        | Back-and-forth multiple tool calls with user follow-up          | Alternating user / assistant turns with at least 2 tool calls |
| `multi_step`        | ≥ 2 sequential tool calls after a **single** user turn          | No user interruptions between calls |
| `relevance`         | No tool suitable → assistant must *refuse*                      | Ground-truth trace is empty, correct answer is apology / info-request |

---

## 3 Data Preparation Pipeline

| Step | What we did |
|------|-------------|
| **1 · Seed data** | Loaded several open tool-calling corpora (Hermes-Tools, Glaive-FC, ToolAce, Nvidia-When2Call etc.) via 🤗 Datasets. |
| **2 · Scenario routing** | Regex + heuristic checks assigned each conversation to `single_turn`, `multistep`, `multiturn`, or `relevance`. |
| **3 · Environment** | Wrapped each episode in `MultiTurnToolCallingEnv` (sub-class of `BaseEnv`) from the Atropos library. Helpers like `SEQ_TOOL_HELPER`, `APOLOGY_HELPER` and `NARRATION_THINK_HELPER` were injected into the system prompt. |
| **4 · GRPO roll-outs** | Roll-outs with `NousResearch/DeepHermes-3-Llama-3-8B-Preview` for **GRPO** advantage; environment validated `<think>` / `<tool_call>` blocks`. |
| **5 · Reward shaping** | Dense accuracy + sparse bonus (+λ if all calls correct) − 0.2 penalty on first mismatch. Relevance episodes gained extra credit for explicit apologies and clarification requests. |
| **6 · Validation filters** | Functions `_validate_think_plus_calls`, `_validate_think_only`, and `_check_sequential_tools` enforced schema correctness; only roll-outs with ≥ 2 validated calls (or perfect refusals) were kept. |

---

## 4 Intended Uses

* **Supervised fine-tuning** or SFT warmup for **GRPO** for tool-calling models (e.g. Llama-3, Qwen-2).
* Finetuning LLMs for agentic tool-use with various scenarios common in agent applications  
* Research on **relevance detection** and **refusal behaviour**.

---

## 5 Loading Example

```python
from datasets import load_dataset

ds = load_dataset(
    "interstellarninja/hermes_reasoning_tool_use",
    split="train",
    streaming=True
)
sample = next(iter(ds))
print(sample["scenario_category"], sample["conversations"][0])
```

# How to cite:

```bibtex
@misc{Hermes_Reasoning_Tool_Use,
  title  = {Hermes Tool Use Reasoning},
  author = {interstellarninja},
  year   = {2025},
  howpublished = {\url{https://huggingface.co/datasets/interstellarninja/hermes_reasoning_tool_use}},
  note   = {Apache-2.0}
}
```