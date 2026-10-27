---
license: mit
task_categories:
- text-generation
language:
- en
tags:
- swe-bench
- code
- agent-trajectories
- mixed-teachers
pretty_name: Agent Trajectories on SWE-bench Test \ Verified (Mixed Teachers)
size_categories:
- 1K<n<10K
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
dataset_info:
  features:
  - name: messages
    list:
    - name: content
      dtype: string
    - name: role
      dtype: string
  - name: instance_id
    dtype: string
  - name: n_turns
    dtype: int64
  - name: n_messages
    dtype: int64
  - name: selected_models
    sequence: string
  - name: resolved
    dtype: 'null'
  - name: exit_status
    dtype: string
  splits:
  - name: train
    num_bytes: 102279077
    num_examples: 1785
  download_size: 40000657
  dataset_size: 102279077
---

# Agent Trajectories: SWE-bench Test \ Verified — Mixed Teachers (gpt-5.2 / gpt-5-mini)

## Summary

Full multi-turn agent trajectories collected from the **SWE-bench Test minus Verified** split
(i.e., SWE-bench Test instances that are **not** part of SWE-bench Verified).
Intended for SFT of agent models on coding tasks.

## Data Collection

Each trajectory was produced by a **GT-aware lookahead agent** that, at every turn:

1. Sampled a candidate response from **both** `gpt-5.2` and `gpt-5-mini`.
2. Had a **gemini-3-pro-preview** router evaluate both candidates and select the better one.
3. Executed the selected step in the environment and appended the observation.

This "best-of-two" selection is oracle-informed (access to the ground-truth patch during routing),
producing near-optimal mixed-teacher trajectories.

## Format

Each row contains a single complete trajectory in **OpenAI messages format**:

```json
{
  "messages": [
    {"role": "system",    "content": "You are a helpful assistant..."},
    {"role": "user",      "content": "<pr_description>...</pr_description>"},
    {"role": "assistant", "content": "THOUGHT: ...\nACTION: ..."},
    {"role": "user",      "content": "<returncode>0</returncode>..."},
    "...",
    {"role": "assistant", "content": "...submit..."}
  ],
  "instance_id": "sympy__sympy-24152",
  "n_turns": 8,
  "n_messages": 17,
  "selected_models": ["litellm_proxy/openai/gpt-5.2", "litellm_proxy/openai/gpt-5-mini", "..."],
  "resolved": true,
  "exit_status": "Submitted"
}
```

## Statistics

| Split      | Instances |
|------------|-----------|
| train      | 1607      |
| validation | 178       |
| **total**  | **1785**  |

## Source

- **SWE-bench subset**: SWE-bench Test \ Verified (instances in Test that are not in Verified)
- **Candidate models**: `gpt-5.2`, `gpt-5-mini`
- **Router (step selector)**: `gemini-3-pro-preview` (GT-aware lookahead routing)
- **Langfuse session**: `data-collection-run_id-2eb77197e7c72634d36b53890e775004-gt_aware_llm-2026-03-13_11-14-52`
