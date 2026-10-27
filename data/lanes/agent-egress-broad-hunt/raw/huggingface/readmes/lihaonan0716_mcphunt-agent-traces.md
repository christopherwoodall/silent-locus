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
Total: 6,786 traces in main, mitigation, and supplemental strata.

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
  `guarded_run_provenance.json`,
  `live_guard_deepseek_v4_flash_paired.json`, and
  `hard_negative_ci.json` (the risky-vs-hard-negative matched 2x2, its Tango
  score interval, and the exact McNemar p-value).
- **`recall_evaluation/`** — `recall_estimation.json`, a single-record
  detector-clean miss-prevalence diagnostic (paper Appendix T) over a seeded
  simple random sample (n=150, seed=20260729) of the 698 risky-environment,
  no-defense main-benchmark traces that read a canary but were not flagged by
  the exact-substring detector. One LLM judge (Claude Opus), given each
  environment's canary values, flagged traces whose outbound events contain a
  canary, a fragment of one, or a description of one. The result is a
  rubric-positive prevalence over the detector's own clean output (Wilson 95%
  interval, sampling error only). It is **not** a recall, a false-negative
  rate, or a credential-propagation miss rate, and it does not modify any
  per-trace label in the other splits. The directory and file names are kept
  for compatibility with earlier releases.
- **`crs_audit/`** — raw labels (`annotation_1.csv`, `annotation_2.csv`) and
  protocol (`README.md`) of the post-submission blind CRS audit by two
  non-author annotators. The same files are in the code repository under
  `artifacts/release/crs_audit/`; `scripts/score_annotation.py` recomputes the
  reported agreement and Cohen's kappa from them.

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
@inproceedings{mcphunt2026,
  title={{MCPH}unt: An Evaluation Framework for Cross-Boundary Data Propagation
         in Multi-Server {MCP} Agents},
  author={Li, Haonan and Sun, Tianjun and Wang, Yongqing and Zhang, Qisheng},
  booktitle={The Fortieth Annual Conference on Neural Information Processing
             Systems Evaluations and Datasets Track},
  year={2026},
  eprint={2604.27819},
  archivePrefix={arXiv},
  primaryClass={cs.AI},
  url={https://openreview.net/forum?id=9mPzIg8uil}
}
```

## License

CC-BY-4.0
