---
license: cc-by-4.0
language:
- en
pretty_name: MCPHunt Agent Traces
size_categories:
- 1K<n<10K
task_categories:
- other
tags:
- agent-safety
- mcp
- model-context-protocol
- data-propagation
- benchmark
- canary-tracking
---

# MCPHunt Agent Traces

Agent execution traces from the MCPHunt evaluation framework, measuring
cross-boundary data propagation in multi-server MCP agents.

## Contents

- **`main/`** — 3,615 traces from 5 models across 147 tasks and 7 environment
  variants (risky_v1/v2/v3, benign, hard_neg_v1/v2/v3). One JSON file per model.
- **`mitigation/`** — 2,706 traces from the prompt-mitigation study (M0--M3
  levels) across 3 models.
- **`live_guard_defense/`** — 387 DeepSeek-V4-Flash traces from the runtime
  taint-guard defense arm (same task/env schedule as the main split for that
  model), paired with the corresponding baseline traces in `main/` so the
  defense-vs-baseline comparison is reproducible per-trace.
- **`browser_replication/`** — 78 DeepSeek-V4-Flash traces (39 baseline + 39
  defense) collected as a same-arm-schedule replication of the
  browser-to-local mechanism, released to support cross-arm reproducibility
  checks for the runtime-guard analysis.
- **`meta/`** — Aggregated results, regression data, and paired-analysis
  summaries for statistical analysis. Includes
  `paired_live_guard_analysis.json`,
  `live_guard_deepseek_v4_flash_paired.json`, and
  `hard_negative_ci.json` (the risky-vs-hard-negative matched 2x2, its Tango
  score interval, and the exact McNemar p-value).
- **`recall_evaluation/`** — `recall_estimation.json`, a single-record
  LLM-judge recall estimate over a seeded SRS sample (n=150, seed=20260729) of
  detector-clean no-defense traces. It estimates the prevalence of secret
  propagation missed by the exact-substring detector within the detector-clean
  pool. Point estimates are judge-estimated (Claude Opus judge), not human
  ground truth; confidence intervals are Wilson score 95%. This quantifies the
  non-verbatim undercount of the conservative, verbatim-only substring detector
  and is diagnostic only — it does not modify any per-trace label in the other
  splits.

## Reproduction

```bash
git clone <repo-url> && cd mcphunt
pip install -e .
make download    # downloads this dataset to results/
make reproduce   # reproduces every number in the paper
make paired      # recomputes the matched-pair analyses from the traces
```

`make download` restores the supplemental arms to the paths the analyses read
(`live_guard_defense/` and `browser_replication/` become
`results/agent_traces/deepseek_v4_flash/agent_traces_deft.json` and
`results/agent_traces_b3_replication/deepseek_v4_flash/`), and fetches the
released `meta/` artifacts as reference copies. `make paired` then recomputes
them from the traces, writing to `results/hard_negative_analysis/` and
`results/live_guard_replication/`; the release build is what copies those
outputs into `meta/`. Each recomputed artifact records the SHA-256 of the trace
file it read, which matches the corresponding file in this bundle.

## Models

| Model | Provider | Traces |
|-------|----------|--------|
| GPT-5.4 | OpenAI | 723 |
| GPT-5.2 | OpenAI | 723 |
| DeepSeek-V4-Flash | DeepSeek | 723 |
| Gemini-3.1-Pro | Google | 723 |
| MiniMax-M2.7 | MiniMax | 723 |

## Schema

Each trace JSON file contains a top-level `traces` array. Per-trace fields:
`task_id`, `env_type`, `risk_mechanism`, `outcome`, `labeling` (with 11 tiered
risk signals plus 1 diagnostic signal), `events` (tool-call log),
`task_completed`, `duration_s`, etc.

## Citation

```bibtex
@misc{mcphunt2026anonymous,
  title={MCPHunt: An Evaluation Framework for Cross-Boundary Data Propagation
         in Multi-Server MCP Agents},
  author={Anonymous},
  year={2026}
}
```

## License

CC-BY-4.0
