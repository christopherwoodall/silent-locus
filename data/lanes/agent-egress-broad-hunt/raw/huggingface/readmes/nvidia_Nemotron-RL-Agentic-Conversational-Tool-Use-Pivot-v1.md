---
license: cc-by-4.0
tags:
- nemo-gym
---
## Dataset Description:

We created an RL dataset for conversational tool-use by utilizing existing expert tool-use trajectories. We pose each assistant step of the trajectory as a separate behavior cloning problem where the policy model is incentivized to match the tool call choices of the expert model. Each trajectory includes the use of tools for authentication, data lookup, servicing (i.e. booking reservations, changing them, getting discounts, etc), and more across 838 different domains such as EdTech, IT support, travel, etc.

This dataset is released as part of NVIDIA [NeMo Gym](https://github.com/NVIDIA-NeMo/Gym), a framework for building reinforcement learning environments to train large language models. NeMo Gym contains a growing collection of training environments and datasets to enable Reinforcement Learning from Verifiable Reward (RLVR). This dataset was utilized in the development of the [NVIDIA Nemotron](https://www.nvidia.com/en-us/ai-data-science/foundation-models/nemotron/) family of models.

NeMo Gym is an open-source library within the [NVIDIA NeMo framework](https://github.com/NVIDIA-NeMo/), NVIDIA's GPU-accelerated, end-to-end training framework for large language models (LLMs), multi-modal models, and speech models.

This dataset is part of the https://huggingface.co/collections/nvidia/nemo-gym/ collection

This dataset is ready for commercial use.

## Dataset Owner(s):
NVIDIA Corporation

## Dataset Creation Date:
03/11/2026

## License/Terms of Use: 
This dataset is licensed under Creative Commons Attribution 4.0 International (CC-BY 4.0)

## Intended Usage:
To be used with [NeMo Gym](https://github.com/NVIDIA-NeMo/Gym) for post-training LLMs. 

## Dataset Characterization
  Data Collection Method<br>
* [Synthetic] <br>
Using deepseek-ai/DeepSeek-R1-0528, deepseek-ai/DeepSeek-V3.2, Qwen/Qwen3-235B-A22B-Thinking-2507, Qwen/Qwen3-32B


Labeling Method<br>
* [Synthetic] <br>
Using openai/gpt-oss-120b, Qwen/Qwen3-235B-A22B-Instruct-2507

## Dataset Format
Structured JSON, Compatible with https://github.com/NVIDIA-NeMo/Gym

## Dataset Quantification

Train 170320: 

11 top-level fields per record: trajectory_id, responses_create_params, expected_action, scenario, num_unique_actions, meta_info, qwen_235b_info, agent_ref, pass_rate, pass_rate_total, pass_rate_passed.

Train ~3.0GB


## Reference(s):
[NeMo Gym](https://github.com/NVIDIA-NeMo/Gym)

## Ethical Considerations:
NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications.  When downloaded or used in accordance with our terms of service, developers should work with their internal teams to ensure this dataset meets requirements for the relevant industry and use case and addresses unforeseen product misuse.   
Please report quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).