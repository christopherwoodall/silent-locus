---
configs:
- config_name: default
  data_files:
  - split: webshop
    path: data/webshop_*
  - split: scienceworld
    path: data/sciworld_*
  - split: alfworld
    path: data/alfworld_*
dataset_info:
  features:
  - name: id
    dtype: string
  - name: conversations
    list:
    - name: from
      dtype: string
    - name: value
      dtype: string
  splits:
  - name: webshop
    num_examples: 1823
  - name: scienceworld
    num_examples: 1482
  - name: alfworld
    num_examples: 3118
language:
- en
pretty_name: ETO-SFT-Trajectory
license: apache-2.0
size_categories:
- 1K<n<10K
---

# Expert Trajectories for ETO


<p align="center">
<img src=https://raw.githubusercontent.com/Yifan-Song793/ETO/main/assets/main.png width=700/>
</p>

[**🌐 Homepage**](https://huggingface.co/spaces/agent-eto/Agent-ETO) | [**🐍 GitHub**](https://github.com/Yifan-Song793/ETO) | [**📖 arXiv**](https://arxiv.org/abs/2403.02502)

Expert trajectories for [Trial and Error: Exploration-Based Trajectory Optimization for LLM Agents](https://arxiv.org/abs/2403.02502)

Authors: [Yifan Song](https://github.com/Yifan-Song793), [Da Yin](https://wadeyin9712.github.io/), [Xiang Yue](https://xiangyue9607.github.io/), [Jie Huang](https://jeffhj.github.io/), [Sujian Li](http://123.56.88.210/), [Bill Yuchen Lin](https://yuchenlin.xyz/).

We introduce **ETO** (Exploration-based Trajectory Optimization), an agent learning framework inspired by "trial and error" process of human learning.
ETO allows an LLM agent to iteratively collect failure trajectories and updates its policy by learning from contrastive failure-success trajectory pairs.

**ETO** has following features:
- 🕹️ **Learning by Trial and Error**
  - 🎲 **Learning from Failure Trajectories.** Contrary to previous approaches that exclusively train on successful expert trajectories, ETO allows agents to learn from their exploration failures.
  - 🎭 **Contrastive Trajectory Optimization.** ETO applies DPO loss to perform policy learning from failure-success trajectory pairs.
  - 🌏 **Iterative Policy Learning.** ETO can be expanded to multiple rounds for further policy enhancement.
- 🎖️ **Superior Performance**
  - ⚔️ **Effectiveness on Three Datasets.** ETO significantly outperforms strong baselines, such as RFT, PPO, on [WebShop](https://webshop-pnlp.github.io/), [ScienceWorld](https://sciworld.apps.allenai.org/), and [ALFWorld](https://alfworld.github.io/).
  - 🦾 **Generalization on Unseen Scenarios.** ETO demonstrates an impressive performance improvement of 22% over SFT on the challenging out-of-distribution test set in ScienceWorld.
  - ⌛ **Task-Solving Efficiency.** ETO achieves higher rewards within fewer action steps on ScienceWorld.
  - 💡 **Potential in Extreme Scenarios.** ETO shows better performance in self-play scenarios where expert trajectories are not available.


## Expert Trajectories

This dataset contains expert trajectories for three agent environments:
- **WebShop**: We preprocess the official [human demonstrations](https://github.com/princeton-nlp/WebShop/issues/21) provided by authors of WebShop. We also employ GPT-4 to explore in the environment and select trajectories with rewards greater than 0.7.
- **ScienceWorld**: The environment provides heuristic algorithm to generate golden trajectories.
- **ALFWorld**: The authors provide a few human-annotated trajectories for imitation learning.

Since the original trajectories do not contain CoT information for each action step, we utilize GPT-4 to generate the corresponding rationales.

## 🛠️ Setup & Evaluation

Please see our [GitHub Repo](https://github.com/Yifan-Song793/ETO).


## 📑 The Data Format for Training the Agent


```json
[
  {
    "id": "example_0",
    "conversations": [
      {
        "from": "human",
        "value": "Who are you?"
      },
      {
        "from": "gpt",
        "value": "I am Vicuna, a language model trained by researchers from Large Model Systems Organization (LMSYS)."
      },
      {
        "from": "human",
        "value": "Have a nice day!"
      },
      {
        "from": "gpt",
        "value": "You too!"
      }
    ]
  }
]
```


## 📖 Citation

If you find this dataset helpful, please cite out paper:

```
@article{song2024trial,
    author={Yifan Song and Da Yin and Xiang Yue and Jie Huang and Sujian Li and Bill Yuchen Lin},
    title={Trial and Error: Exploration-Based Trajectory Optimization for LLM Agents},
    year={2024},
    eprint={2403.02502},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```
