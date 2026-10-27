---
license: mit
dataset_info:
  features:
  - name: instance_id
    dtype: string
  - name: messages
    list:
    - name: content
      dtype: string
    - name: role
      dtype: string
  splits:
  - name: train
    num_bytes: 4644348713
    num_examples: 65994
  download_size: 1579055064
  dataset_size: 4644348713
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---

## Dataset: SWE-smith-mini_swe_agent_plus-trajectories-66k


[![GitHub - mini-swe-agent-plus](https://img.shields.io/badge/GitHub-mini--swe--agent--plus-black?logo=github)](https://github.com/Kwai-Klear/mini-swe-agent-plus)
[![Hugging Face - Dataset](https://img.shields.io/badge/Hugging%20Face-Dataset-orange?logo=huggingface)](https://huggingface.co/datasets/Kwai-Klear/SWE-smith-mini_swe_agent_plus-trajectories-66k)
[![Hugging Face - Model](https://img.shields.io/badge/Hugging%20Face-Klear--AgentForge--8B--SFT-blue?logo=huggingface)](https://huggingface.co/Kwai-Klear/Klear-AgentForge-8B-SFT)

A corpus of ~66k issue-solving trajectories collected with [mini-swe-agent-plus](https://github.com/Kwai-Klear/mini-swe-agent-plus) on issues derived from [SWE-smith](https://huggingface.co/datasets/SWE-bench/SWE-smith). Each trajectory records the agent’s end-to-end process.
<p align="left">
  <img
    src="https://huggingface.co/datasets/Kwai-Klear/SWE-smith-mini_swe_agent_plus-trajectories-66k/resolve/main/swe_bench_scaling_grid.svg"
    width="600"
    alt="SWE-bench scaling grid"
  />
</p>

We training the Qwen3-8B model on different sizes of the training data. The results are shown in the figure, it could be observed that the solve rate on SWE-bench Verified improves approximately linearly with the logarithm of the data scale (1k → 66k trajectories).  Klear-Agent-8B (trained on this dataset with mini-swe-agent-plus) signifanctly outperforms other ~8B models and matches several open 32B systems.
| Method/Model            | Params | Agent Framework     | SWE-bench Verified (%) |
|-------------------------|:------:|---------------------|:----------------------:|
| SWE-agent-LM-7B         | 7B     | SWE-agent           | 15.2                   |
| SWE-Mirror-LM-7B        | 7B     | OpenHands           | 22.8                   |
| SWE-gym-32B             | 32B    | OpenHands           | 20.6                   |
| Skywork-SWE-32B         | 32B    | OpenHands           | 38.0                   |
| DeepSWE-32B-Preview     | 32B    | OpenHands           | 42.2                   |
| SWE-Mirror-LM-32B       | 32B    | OpenHands           | 52.2                   |
| SWE-fixer-72B           | 72B    | SWE-Fixer           | 32.8                   |
| Lingma-SWE-GPT-72B      | 72B    | SWE-Syninfer        | 32.8                   |
| **Klear-Agent-8B-SFT**  | 8B     | **mini-swe-agent-plus** | **39.0**          |

### Load with 🤗 Datasets
```python
from datasets import load_dataset

ds = load_dataset(
    "Kwai-Klear/SWE-smith-mini_swe_agent_plus-trajectories-66k",
    split="train"
)
print(ds)
print(ds[0].keys())
```
