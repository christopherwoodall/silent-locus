---
language:
- zh
license: cc-by-4.0
pretty_name: Baoyan Benchmark Public Question Bank
size_categories:
- n<1K
task_categories:
- text-generation
tags:
- agent-evaluation
- chinese
- education
- admissions
configs:
- config_name: single-stage
  default: true
  data_files:
  - split: dev
    path: single-stage.jsonl
- config_name: staged
  data_files:
  - split: dev
    path: staged.jsonl
- config_name: rubrics
  data_files:
  - split: dev
    path: rubrics.jsonl
---

# Baoyan Benchmark Public Question Bank

This dataset accompanies 屿智同行's benchmark project for graduate admissions agents, evaluating agent configurations (execution systems paired with models) for admissions advising, application planning and updating advice as student information changes. The current results cover eight agent configurations. [中文说明](README.zh-CN.md).

The current dataset has **70 tasks**, **83 answer stages**, and **23 student case groups**. Related tasks within a case are not independent student samples. The [complete 70-task results](https://github.com/yeyuxin777/baoyan-agent-benchmark/tree/main/experiments/records70) include available answers, reviews, effective scores, and execution metadata. All eight agent configurations completed the 70 selected tasks. Their current mean scores (out of 100) are from the [full leaderboard on GitHub `main`](https://github.com/yeyuxin777/baoyan-agent-benchmark/blob/main/experiments/records70/score-summary-70.json):

The dataset and all three data subsets are public and require no access approval. The 70 task and rubric calibrations are owner-confirmed. Owner-approved difficulty labels are 14 easy (20%), 34 medium (48.57%) and 22 hard (31.43%); this does not imply independent double review.

| Rank | Agent configuration (system + model) | Mean score |
| ---: | --- | ---: |
| 1 | Codex (GPT Sol 6.1) | 79.08 |
| 2 | Codex (GPT Astra 6) | 78.36 |
| 3 | DSH (DeepSeek V4.1 Flash) | 68.16 |
| 4 | Volcengine Managed Agent (GLM 5.3 Flash) | 66.80 |
| 5 | Qwen Code (Qwen 3.8 Max) | 64.24 |
| 6 | Kimi Code (Kimi K3) | 58.96 |
| 7 | Antigravity (Gemini 3.8 Flash) | 58.23 |
| 8 | Antigravity (Gemini 3.1 Pro) | 55.55 |

| Configuration | Split | Rows | Contents |
| --- | --- | ---: | --- |
| `single-stage` (default) | `dev` | 57 | 21 recommendations and 36 planning or decision tasks |
| `staged` | `dev` | 13 | Two stages per task |
| `rubrics` | `dev` | 70 | Public scoring criteria and reference projects; exclude from tested agent inputs |

Load a configuration with `datasets.load_dataset("yuxin7778/baoyan-agent-benchmark", "single-stage", split="dev")` (or `"staged"` / `"rubrics"`). For a single-stage task, send only `input` to the agent. For a staged task, decode `stages_json` with `json.loads` and disclose each stage only when it begins. Never provide future stages, `rubric_json`, or reference projects to the tested agent. Canonical task files are under `tasks/<task_id>/`; `task_json` and `rubric_json` are JSON-encoded strings.

Each task is worth 100 points; a two-stage task receives one combined score. Full recommendation tasks allocate 70 points to program matching and 30 to recommendation quality. Follow the [scoring rules](scoring.md) and [current review interpretation](adjudication-policy-20261012.json). When an admissions threshold falls within the student’s disclosed score interval, verify eligibility or give a conditional recommendation.

`selection-70.json` defines the task selection; `manifest.json` and `checksums.json` identify the dataset files for reproducibility. The manifest records the GitHub source selection hash. Scoring nodes and reference candidates match the selected GitHub source; HF-only rubric metadata gives the full files separate hashes. Historical answers and scores have not been rerun. Report the agent model, tools, execution settings, and dataset hashes with results. The public questions contain privacy redactions; do not attempt to identify students from remaining combinations of information.

[Questions](questions.md) · [Questions and scoring](questions-and-scoring.md) · [GitHub code and results](https://github.com/yeyuxin777/baoyan-agent-benchmark)

## About the project

This is **屿智同行**'s benchmark project for graduate admissions agents.

### Team

**Yonghao Zhang** is CEO and holds a master's degree in Computer Science from Tsinghua University; **Yichen Wang** is CTO and project lead.

## Acknowledgements

We thank 保研岛 for providing data for this benchmark.

## License

Data license: **CC BY 4.0**; see [LICENSE](LICENSE). Cite the [dataset](CITATION.cff) for tasks or rubrics, and the separate [MIT-licensed software](https://github.com/yeyuxin777/baoyan-agent-benchmark/blob/main/CITATION.cff) for code or tooling.
