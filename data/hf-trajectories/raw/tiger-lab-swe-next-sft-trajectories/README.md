---
pretty_name: SWE-Next SFT Trajectories
license: mit
task_categories:
- text-generation
language:
- en
size_categories:
- 1K<n<10K
configs:
- config_name: default
  data_files:
  - split: train
    path: SWE_Next_SFT_Trajectories.jsonl
---

<div align="center">
  <h1>SWE-Next: Scalable Real-World Software Engineering Tasks for Agents</h1>
</div>

<div align="center">
  <a href="https://arxiv.org/abs/2603.20691"><img alt="Paper" src="https://img.shields.io/badge/Paper-arXiv-b31b1b?style=for-the-badge&logo=arxiv&logoColor=white"></a>
  <a href="https://tiger-ai-lab.github.io/SWE-Next/"><img alt="Project Page" src="https://img.shields.io/badge/Project%20Page-Website-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white"></a>
  <a href="https://github.com/TIGER-AI-Lab/SWE-Next"><img alt="Code" src="https://img.shields.io/badge/Code-GitHub-181717?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="https://huggingface.co/datasets/TIGER-Lab/SWE-Next"><img alt="Dataset" src="https://img.shields.io/badge/Base%20Dataset-HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=000"></a>
  <a href="https://huggingface.co/TIGER-Lab/SWE-Next-7B"><img alt="Model 7B" src="https://img.shields.io/badge/Model%207B-HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=000"></a>
  <a href="https://huggingface.co/TIGER-Lab/SWE-Next-14B"><img alt="Model 14B" src="https://img.shields.io/badge/Model%2014B-HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=000"></a>
</div>

# SWE-Next SFT Trajectories

SWE-Next SFT Trajectories is the supervised fine-tuning dataset released with **SWE-Next: Scalable Real-World Software Engineering Tasks for Agents**. It contains **3,693** ShareGPT-style multi-turn training examples collected from expert agent rollouts on **2,308** execution-grounded SWE tasks synthesized from real merged pull requests.

The dataset is designed for training repository-level SWE agents rather than isolated code generators. Each example is a cleaned interaction trace with roles such as `system`, `user`, `assistant`, and `tool`, suitable for direct use in LLaMA-Factory and similar chat-style SFT pipelines.

<div align="center">
  <img src="https://raw.githubusercontent.com/TIGER-AI-Lab/SWE-Next/main/docs/static/images/teaser.png" alt="SWE-Next teaser" width="100%" style="max-width: 900px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
</div>

## Dataset Overview

SWE-Next first mines real merged PRs, executes candidate base/merged commit pairs, and retains only commit pairs that yield strict test improvements without regressions. Expert models then interact with these self-verifying tasks under a fixed repository-level interface. From the resulting rollouts, we keep two buckets for SFT:

- **Clean successes**: final verification passes, a real code edit is made, and earlier test evidence remains consistently parseable.
- **Recovery successes**: final verification passes after at least one earlier failing test, capturing repair trajectories with meaningful debugging evidence.

This filtering yields a compact but high-signal SFT corpus for downstream SWE-agent training.

## Format

The dataset contains one training split with **3,693** rows.

Each row is a JSON object of the form:

```json
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, ...]}
```

The `messages` field follows a ShareGPT-style schema:

- `system`: agent setup and high-level instructions
- `user`: task statement and repository-level problem context
- `assistant`: the model's intermediate reasoning/actions
- `tool`: tool outputs such as shell execution, file inspection, and test feedback

## Files

- `SWE_Next_SFT_Trajectories.jsonl`: the released ShareGPT-style SFT corpus

## Usage

Load the dataset with Hugging Face Datasets:

```python
from datasets import load_dataset

ds = load_dataset("TIGER-Lab/SWE-Next-SFT-Trajectories")
print(ds["train"][0].keys())
```

It can also be used directly with LLaMA-Factory-style training configs by pointing the training pipeline to `SWE_Next_SFT_Trajectories.jsonl`.

## Relationship to the SWE-Next Release

This repo contains only the released SFT trajectories. Related artifacts are available separately:

- **Base task dataset**: `TIGER-Lab/SWE-Next`
- **Released models**: `TIGER-Lab/SWE-Next-7B`, `TIGER-Lab/SWE-Next-14B`
- **Project code**: `github.com/TIGER-AI-Lab/SWE-Next`

## Citation

```bibtex
@misc{liang2026swenextscalablerealworldsoftware,
      title={SWE-Next: Scalable Real-World Software Engineering Tasks for Agents},
      author={Jiarong Liang and Zhiheng Lyu and Zijie Liu and Xiangchao Chen and Ping Nie and Kai Zou and Wenhu Chen},
      year={2026},
      eprint={2603.20691},
      archivePrefix={arXiv},
      primaryClass={cs.SE},
      url={https://arxiv.org/abs/2603.20691},
}
```
