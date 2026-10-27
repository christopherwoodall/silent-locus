---
dataset_info:
  features:
  - name: task_id
    dtype: string
  - name: messages
    dtype: string
  - name: tools
    dtype: string
  - name: num_turns
    dtype: int64
  splits:
  - name: train
    num_bytes: 964972196
    num_examples: 7777
  download_size: 300179898
  dataset_size: 964972196
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---

# Agentic coding trajectories of GLM-5.1

We collected 7,777 successful multi-turn trajectories by running
[GLM-5.1](https://huggingface.co/zai-org/GLM-5.1) with the
[PI agent](https://pi.dev/) on
[nebius/SWE-rebench-V2](https://huggingface.co/datasets/nebius/SWE-rebench-V2).

## Configuration

Each SWE-rebench-V2 task is an issue of a public repository. An agent has to
implement a fix that is then validated by unit tests.

The model was run on 3,837 issues from Python repositories, with 4 rollouts
per issue. The task list is available as the `train` split of
[whitecircle/swe-rebench-v2-clean-python-tasks](https://huggingface.co/datasets/whitecircle/swe-rebench-v2-clean-python-tasks).

## GLM-5.1 scores

| Metric | Score |
| --- | --- |
| pass@1 | 0.5067 |
| pass@2 | 0.5646 |
| pass@4 | 0.6070 |

## PI Agent

We ran GLM-5.1 inside PI — a lightweight agent harness with four tools:
`bash`, `read`, `edit`, `write`.

![Turns and tokens distribution](turns_tokens_distribution.png)

```python
import json
from datasets import load_dataset

ds = load_dataset('whitecircle/swe-rebench-v2-glm-5.1-pi-agent-successful-traces', split='train')
messages = json.loads(ds[0]['messages'])
tools = json.loads(ds[0]['tools'])
```

## Use

This dataset was used to train
[GLM-4.7-Flash-Coder](https://huggingface.co/whitecircle/GLM-4.7-Flash-Coder).
