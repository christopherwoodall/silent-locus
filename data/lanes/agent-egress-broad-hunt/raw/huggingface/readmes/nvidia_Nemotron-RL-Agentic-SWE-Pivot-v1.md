---
license: cc-by-4.0
tags:
- nemo-gym
---
## Dataset Description:

The SWE-RL dataset provides GitHub issues for training and validating real-world software engineering agents using the OpenHands environment in NeMo Gym. The dataset is a refactored version of the SWE-Gym and R2E-Gym datasets to support the NeMo Gym input format.

This dataset is released as part of NVIDIA [NeMo Gym](https://github.com/NVIDIA-NeMo/Gym), a framework for building reinforcement learning environments to train large language models. NeMo Gym contains a growing collection of training environments and datasets to enable Reinforcement Learning from Verifiable Reward (RLVR). This dataset was utilized in the development of the [NVIDIA Nemotron](https://www.nvidia.com/en-us/ai-data-science/foundation-models/nemotron/) family of models.

NeMo Gym is an open-source library within the [NVIDIA NeMo framework](https://github.com/NVIDIA-NeMo/), NVIDIA's GPU-accelerated, end-to-end training framework for large language models (LLMs), multi-modal models, and speech models.

This dataset is part of the https://huggingface.co/collections/nvidia/nemo-gym/ collection

This dataset is ready for commercial use.

## Dataset Owner(s):
NVIDIA Corporation

## Dataset Creation Date:
03/11/2026

## License/Terms of Use: 
This dataset is licensed under Creative Commons Attribution 4.0 International (CC-BY 4.0).

## Intended Usage:
To be used with [NeMo Gym](https://github.com/NVIDIA-NeMo/Gym) for post-training LLMs. 

## Dataset Characterization
* Data Collection Method<br>
  * [Automated] <br>
Derived from SWE-Gym and R2E-Gym

* Labeling Method<br>
  * [Not Applicable] <br>

## Dataset Format
Codebase compatible with https://github.com/NVIDIA-NeMo/Gym

## Dataset Quantification

Train Samples - 6436

2 top-level features
responses_create_params, agent_ref

Train ~4.25GB

## Reference(s):
[NeMo Gym](https://github.com/NVIDIA-NeMo/Gym)<br>
SWE-Gym - https://arxiv.org/pdf/2412.21139<br>
R2E-Gym - https://arxiv.org/pdf/2504.07164

## Ethical Considerations:
NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications.  When downloaded or used in accordance with our terms of service, developers should work with their internal teams to ensure this dataset meets requirements for the relevant industry and use case and addresses unforeseen product misuse.   
Please report quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).