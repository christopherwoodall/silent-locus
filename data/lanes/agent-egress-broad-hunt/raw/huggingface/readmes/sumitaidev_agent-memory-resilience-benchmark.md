---
license: apache-2.0
task_categories:
  - reinforcement-learning
  - tabular-classification
tags:
  - agent-memory
  - bayesian-inference
  - llm-agents
  - negative-transfer
  - reliability
  - benchmark
pretty_name: Agent Memory Resilience & Poisoning Benchmark
size_categories:
  - 1K<n<10K
configs:
  - config_name: telemetry_traces
    data_files: "telemetry_traces.csv"
  - config_name: memory_bank_experiences
    data_files: "memory_bank_experiences.csv"
---

# Agent Memory Resilience & Poisoning Benchmark

## Dataset Summary

This benchmark dataset evaluates resilience, negative transfer, and memory poisoning mitigation in autonomous LLM agent architectures (such as LangGraph, AutoGen, and CrewAI).

When autonomous agents record distilled self-reflections after attempting tasks, external stochastic failures or subtle API deprecations often cause agents to commit defective strategies into episodic memory. Under standard retrieval pipelines using unweighted cosine similarity, flawed memories are repeatedly retrieved due to high prompt keyword similarity, resulting in runaway catastrophic degradation.

This repository provides 1,200 empirical execution traces across four controlled ablation conditions, alongside a verified 100-memory experiential bank containing Bayesian posterior distributions and quarantine status.

---

## Dataset Structure

### Configuration: `telemetry_traces`
File: `telemetry_traces.csv` (1,200 rows)

Contains chronological execution steps evaluating task completion rates across four experimental conditions under an adversarial noise injection regime (steps 60 to 140).

| Column | Type | Description |
|---|---|---|
| `trial_id` | int | Unique global trial index. |
| `ablation_condition` | string | One of `vanilla_baseline`, `naive_vector_rag`, `symmetric_reflexion`, `adaptive_bayesian_lcb`. |
| `step_index` | int | Sequential step number (1 to 300). |
| `task_domain` | string | Operational domain (`coding`, `research`, `analysis`, `planning`). |
| `cosine_similarity` | float | Semantic cosine similarity between query and retrieved memory vector. |
| `observed_reward` | float | Execution reward score in [0.0, 1.0]. |
| `task_success` | int | Binary indicator (1 = success, 0 = failure). |
| `cumulative_accuracy` | float | Running task success rate up to the current step. |
| `in_poison_injection_regime` | bool | True if the step falls within the adversarial poisoning window. |
| `quarantine_triggered` | bool | True if the reliability pruning threshold is triggered. |

### Configuration: `memory_bank_experiences`
File: `memory_bank_experiences.csv` (100 rows)

Structured experiential memory records containing conjugate Beta-Bernoulli update parameters and quarantine tags.

| Column | Type | Description |
|---|---|---|
| `experience_id` | string | Unique memory identifier. |
| `task_domain` | string | Domain classification (`coding`, `research`, `analysis`, `planning`). |
| `trigger_condition` | string | Applicability predicate describing when this memory should be recalled. |
| `strategy_lesson` | string | Distilled positive operational strategy directive. |
| `negative_pitfall` | string | Anti-pattern or failure mode to avoid. |
| `initial_confidence` | float | Initial reflection confidence score. |
| `successes_count` | int | Count of empirical task completions utilizing this memory ($n_s$). |
| `failures_count` | int | Count of empirical task failures utilizing this memory ($n_f$). |
| `total_uses` | int | Total executions ($n_s + n_f$). |
| `posterior_mean_trust` | float | Expectation $\mathbb{E}[\theta \mid n_s, n_f] = \frac{\alpha_0 + n_s}{\alpha_0 + \beta_0 + n_s + n_f}$ under prior $\operatorname{Beta}(3, 1)$. |
| `posterior_variance` | float | Epistemic variance $\operatorname{Var}[\theta \mid n_s, n_f]$. |
| `pessimistic_lcb_score` | float | Lower Confidence Bound retrieval score ($\mu - 1.0 \times \sigma$). |
| `quarantine_status` | string | Status tag: `active` or `deprecated`. |
| `is_adversarial_sample` | bool | True if synthesized with flawed anti-patterns. |

---

## Experimental Conditions

1. **Vanilla Baseline (Condition A)**: Zero inter-task episodic memory. Agent approaches every task independently.
2. **Naive Vector RAG (Condition B)**: Standard cosine similarity retrieval without reliability tracking. Vulnerable to runaway negative transfer.
3. **Symmetric Reflexion (Condition C)**: Exponential Moving Average trust updates ($S_t = 0.8 S_{t-1} + 0.2 r_t$). Lacks statistical confidence bounds.
4. **Adaptive Bayesian LCB (Condition D - Proposed)**: Conjugate Beta-Bernoulli updating ($\alpha_0=3.0, \beta_0=1.0$), epistemic uncertainty quantification, Pessimistic Lower Confidence Bound (LCB) composite retrieval, and Theorem 1 statistical quarantine ($t^* = 4$ consecutive failures for $>95\%$ confidence of degradation).

---

## Usage with Hugging Face Datasets

```python
from datasets import load_dataset
import pandas as pd

# Load telemetry traces
traces_ds = load_dataset("sumitaidev/agent-memory-resilience-benchmark", data_files="telemetry_traces.csv")
df_traces = traces_ds["train"].to_pandas()
print(f"Loaded traces: {df_traces.shape}")

# Load experiential memory bank
memory_ds = load_dataset("sumitaidev/agent-memory-resilience-benchmark", data_files="memory_bank_experiences.csv")
df_memories = memory_ds["train"].to_pandas()
print(f"Loaded memories: {df_memories.shape}")

# Inspect mean reliability across conditions
summary = df_traces.groupby("ablation_condition")["task_success"].mean()
print(summary)
```

---

## Citation

```bibtex
@article{das2026adaptive,
  title={Adaptive Agent Memory Resilience: Mitigating Negative Transfer and Memory Poisoning via Bayesian Trust Updating and Pessimistic Lower Confidence Bound Retrieval},
  author={Das, Sumit},
  journal={arXiv preprint},
  year={2026}
}
```
