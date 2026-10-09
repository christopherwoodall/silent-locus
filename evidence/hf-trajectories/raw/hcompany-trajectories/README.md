---
license: apache-2.0
pretty_name: Holo4 Trajectories
language:
  - en
tags:
  - agents
  - computer-use
  - trajectories
  - benchmark
size_categories:
  - 1K<n<10K
---

# Holo4 Trajectories

Every run behind the [Holo4](https://hcompany.ai/newsroom/holo4) benchmark scores: 7,366 agent trajectories from Holo4 27B and Holo4 35B-A3B, with each step's reasoning, actions, tool results and screenshots.

Browse them at **[trajectories.hcompany.ai](https://trajectories.hcompany.ai)**. This dataset is the same bundle the site serves.

| Benchmark | Holo4 27B | Holo4 35B-A3B | Upstream | License |
| :-- | --: | --: | :-- | :-- |
| OSWorld | 1,096 | 1,102 | [xlang-ai/OSWorld](https://github.com/xlang-ai/OSWorld) | Apache 2.0 |
| OSWorld 2 | 106 | 106 | [xlang-ai/OSWorld-V2](https://github.com/xlang-ai/OSWorld-V2) | Apache 2.0 |
| AndroidWorld | 344 | 347 | [google-research/android_world](https://github.com/google-research/android_world) | Apache 2.0 |
| AutomationBench | 1,600 | 1,598 | [zapier/AutomationBench](https://github.com/zapier/AutomationBench) | MIT |
| PinchBench | 429 | 429 | [pinchbench/skill](https://github.com/pinchbench/skill) | MIT |
| Agents' Last Exam | 104 | 105 | [rdi-berkeley/agents-last-exam](https://github.com/rdi-berkeley/agents-last-exam) | Apache 2.0 |

## Layout

```
data/index.json        benchmarks and one summary row per trajectory
data/t/<id>.json       full trajectory: task, steps, verifier result, token usage
img/<id>/<step>.webp   screenshots, referenced from the steps
```

Each row in `data/index.json` has `id`, `model`, `benchmark`, `run`, `task`, `instruction`, `success`, `score`, `duration_s` and `steps`.

## Notes

- Task instructions and environments belong to the upstream benchmarks, under their own licenses listed above.
- Credentials, internal hosts and personal data are masked as `<PII removed>`. Screenshots that showed them are replaced by a placeholder, and a few tasks are left out.

## License

Apache 2.0. Upstream task content keeps its original license.
