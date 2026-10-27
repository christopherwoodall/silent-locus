---
license: apache-2.0
---
# Data Introduction
This dataset serves as the core training data for Agent Foundation Models (AFMs), specifically designed to elicit end-to-end multi-agent reasoning capabilities in large language models. Built on the novel "Chain-of-Agents (CoA)" paradigm, the dataset leverages a multi-agent distillation framework to transform collaboration processes from state-of-the-art multi-agent systems into trajectory data suitable for supervised fine-tuning (SFT), simulating dynamic activation of tool agents and role-playing agents in collaborative decision-making workflows.​
The dataset consists of two core components:​
- SFT Data: Contains high-quality trajectories distilled from advanced multi-agent systems, enabling models to learn complex problem-solving logic involving multi-turn tool invocation and role collaboration;​
- RL Data: Focuses on verifiable agentic task scenarios, used to further enhance the model's robustness and performance in CoA reasoning through agentic reinforcement learning.​
This dataset has empowered AFMs to achieve new state-of-the-art performance across diverse benchmarks in both web agent and code agent settings. As part of fully open-sourced resources, it provides a high-quality data foundation for researchers exploring agent model training, agentic reinforcement learning, and related fields.

For more details, please refer to our [Projects](https://chain-of-agents-afm.github.io/), [paper](https://arxiv.org/abs/2508.13167) and [GitHub](https://github.com/OPPO-PersonalAI/Agent_Foundation_Models).

# Data Downloads
The sft and rl datasets for Code Agent are from [Skywork-OR1-RL](https://huggingface.co/datasets/Skywork/Skywork-OR1-RL-Data), [livecodebench](https://huggingface.co/datasets/livecodebench/code_generation_lite), [codeforces](https://huggingface.co/datasets/open-r1/codeforces), [retool](https://huggingface.co/datasets/JoeYing/ReTool-SFT), [DAPOMath](https://huggingface.co/datasets/BytedTsinghua-SIA/DAPO-Math-17k), the dowlowd links are as below:
- [AFM-CodeAgent-SFT-Dataset](https://huggingface.co/datasets/PersonalAILab/AFM-CodeAgent-SFT-Dataset)
- [AFM-CodeAgent-RL-Dataset](https://huggingface.co/datasets/PersonalAILab/AFM-CodeAgent-RL-Dataset)

The sft and rl datasets for Web Agent are from [TaskCraft](https://huggingface.co/datasets/PersonalAILab/TaskCraft), the dowlowd links are as below:
- [AFM-WebAgent-SFT-Dataset](https://huggingface.co/datasets/PersonalAILab/AFM-WebAgent-SFT-Dataset)
- [AFM-WebAgent-RL-Dataset](https://huggingface.co/datasets/PersonalAILab/AFM-WebAgent-RL-Dataset)


The sft and rl datasets for MHQA Agent are from [NQ_HotPotQA_train](https://huggingface.co/datasets/PeterJinGo/nq_hotpotqa_train), the dowlowd links are as below:
- [AFM-MHQA-SFT-Dataset](https://huggingface.co/datasets/PersonalAILab/AFM-MHQA-Agent-SFT-Dataset)
- [AFM-MHQA-RL-Dataset](https://huggingface.co/datasets/PersonalAILab/AFM-MHQA-RL-Dataset)


# Model Downloads

| Model       |   Download   |
| --------------------- | ------|
| AFM-CodeAgent-7B-sft  | [🤗 **HuggingFace**](https://huggingface.co/PersonalAILab/AFM-CodeAgent-7B-sft) |
| AFM-CodeAgent-7B-rl   | [🤗 **HuggingFace**](https://huggingface.co/PersonalAILab/AFM-CodeAgent-7B-rl) |
| AFM-CodeAgent-32B-sft | [🤗 **HuggingFace**](https://huggingface.co/PersonalAILab/AFM-CodeAgent-32B-sft) |
| AFM-CodeAgent-32B-rl  | [🤗 **HuggingFace**](https://huggingface.co/PersonalAILab/AFM-CodeAgent-32B-rl) |
| AFM-MHQA-Agent-3B-sft | [🤗 **HuggingFace**](https://huggingface.co/PersonalAILab/AFM-MHQA-Agent-3B-sft) |
| AFM-MHQA-Agent-3B-rl  | [🤗 **HuggingFace**](https://huggingface.co/PersonalAILab/AFM-MHQA-Agent-3B-rl) |
| AFM-MHQA-Agent-7B-sft | [🤗 **HuggingFace**](https://huggingface.co/PersonalAILab/AFM-MHQA-Agent-7B-sft) |
| AFM-MHQA-Agent-7B-rl  | [🤗 **HuggingFace**](https://huggingface.co/PersonalAILab/AFM-MHQA-Agent-7B-rl) |
| AFM-WebAgent-7B-sft   | [🤗 **HuggingFace**](https://huggingface.co/PersonalAILab/AFM-WebAgent-7B-sft) |
| AFM-WebAgent-32B-sft  | [🤗 **HuggingFace**](https://huggingface.co/PersonalAILab/AFM-WebAgent-32B-sft) |
| AFM-WebAgent-7B-rl    | [🤗 **HuggingFace**](https://huggingface.co/PersonalAILab/AFM-WebAgent-7B-rl) |
| AFM-WebAgent-32B-rl   | [🤗 **HuggingFace**](https://huggingface.co/PersonalAILab/AFM-WebAgent-32B-rl) |

## Citation
If you find `AFM` useful in your research or applications, we would appreciate it if you could cite our work:
```bibtex
@misc{li2025chainofagentsendtoendagentfoundation,
      title={Chain-of-Agents: End-to-End Agent Foundation Models via Multi-Agent Distillation and Agentic RL}, 
      author={Weizhen Li and Jianbo Lin and Zhuosong Jiang and Jingyi Cao and Xinpeng Liu and Jiayu Zhang and Zhenqiang Huang and Qianben Chen and Weichen Sun and Qiexiang Wang and Hongxuan Lu and Tianrui Qin and Chenghao Zhu and Yi Yao and Shuying Fan and Xiaowan Li and Tiannan Wang and Pai Liu and King Zhu and He Zhu and Dingfeng Shi and Piaohong Wang and Yeyi Guan and Xiangru Tang and Minghao Liu and Yuchen Eleanor Jiang and Jian Yang and Jiaheng Liu and Ge Zhang and Wangchunshu Zhou},
      year={2025},
      eprint={2508.13167},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2508.13167}, 
}
```