---
license: mit
library_name: transformers
datasets:
- AI-MO/NuminaMath-CoT
- KbsdJames/Omni-MATH
- RUC-AIBOX/STILL-3-Preview-RL-Data
- hendrycks/competition_math
language:
- en
base_model:
- deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
pipeline_tag: text-generation
---

<div align="center">
<span style="font-family: default; font-size: 1.5em;">DeepScaleR-1.5B-Preview</span>
<div>
🚀 Democratizing Reinforcement Learning for LLMs 🌟
</div>
</div>
<br>
<div align="center" style="line-height: 1;">
  <a href="https://github.com/agentica-project/rllm" style="margin: 2px;">
    <img alt="Code" src="https://img.shields.io/badge/DeepScaleR-000000?style=for-the-badge&logo=github&logoColor=000&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://pretty-radio-b75.notion.site/DeepScaleR-Surpassing-O1-Preview-with-a-1-5B-Model-by-Scaling-RL-19681902c1468005bed8ca303013a4e2" target="_blank" style="margin: 2px;">
    <img alt="Blog" src="https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://x.com/Agentica_/status/1889006266661617779" style="margin: 2px;">
    <img alt="X.ai" src="https://img.shields.io/badge/Agentica-white?style=for-the-badge&logo=X&logoColor=000&color=000&labelColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://huggingface.co/agentica-org" style="margin: 2px;">
    <img alt="Hugging Face" src="https://img.shields.io/badge/Agentica-fcd022?style=for-the-badge&logo=huggingface&logoColor=000&labelColor" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>
</div>
</div>

## DeepScaleR Overview
DeepScaleR-1.5B-Preview is a language model fine-tuned from DeepSeek-R1-Distilled-Qwen-1.5B using distributed reinforcement learning (RL) to scale up to long context lengths. The model achieves 43.1% Pass@1 accuracy on AIME 2024, representing a 15% improvement over the base model (28.8%) and surpassing OpenAI's O1-Preview performance with just 1.5B parameters.

## Data
Our training dataset consists of approximately 40,000 unique problem-answer pairs compiled from:
- AIME problems (1984-2023)
- AMC problems (prior to 2023)
- Omni-MATH dataset
- Still dataset

## Training Recipe
We employ Deepseek's Group Relative Policy Optimization (GRPO), a simplified RL algorithm that extends PPO by:
- Normalizing advantage function over all samples generated from the same prompt.
- Applying KL divergence regularization on top of PPO's surrogate loss to prevent significant policy drift.

**Reward Function**: Our reward function is simple but effective:
- 1 for correct answers passing LaTeX/Sympy checks
- 0 for incorrect or improperly formatted answers
- Note: No partial rewards (such as PRMs) or intermediate feedback.

**Iterative Context Lengthening**: A key challenge in scaling RL for reasoning is compute cost. Our approach trains models with progressively longer contexts as the model improves, thus saving monetary costs and end2end training time: 
- Initial 8K Context (0-1040 steps):
    - 22.9% -> 33% Pass@1 on AIME 2024
    - Trained on 8 A100-80GB GPUs, BS= (Prompts) * (Samples/Prompt) = 128 * 8 = 1024
- Extended to 16K (steps 1040-1520):
    - 33% -> 43% Pass@1 on AIME 2024
    - Trained on 32 A100-80GB GPUs, BS= (Prompts) * (Samples/Prompt) = 128 * 16 = 2048
- Further extended to 24K (step 1520+):
    - 38% -> 43% Pass@1 on AIME 2024
    - Trained on 32 A100-80GB GPUs, BS= (Prompts) * (Samples/Prompt) = 128 * 16 = 2048
    - Significant improvements within <200 steps

A more detailed description of the training recipe can be found in our [blog post](https://pretty-radio-b75.notion.site/DeepScaleR-Surpassing-O1-Preview-with-a-1-5B-Model-by-Scaling-RL-19681902c1468005bed8ca303013a4e2).

## Evaluation
We report Pass@1 accuracy averaged over 16 samples for each problem.
| Model | AIME 2024 | MATH 500 | AMC 2023 | Minerva Math | OlympiadBench | Avg. |
|-------|-----------|-----------|-----------|--------------|---------------|------|
| Qwen-2.5-7B-Instruct | 13.3 | 79.8 | 50.6 | 34.6 | 40.7 | 43.8 |
| rStar-Math-7B | 26.7 | 78.4 | 47.5 | - | 47.1 | - |
| Eurus-2-7B-PRIME | 26.7 | 79.2 | 57.8 | 38.6 | 42.1 | 48.9 |
| Qwen2.5-7B-SimpleRL | 26.7 | 82.4 | 62.5 | <strong>39.7</strong> | 43.3 | 50.9 |
| DeepSeek-R1-Distill-Qwen-1.5B | 28.8 | 82.8 | 62.9 | 26.5 | 43.3 | 48.9 |
| Still-1.5B | 32.5 | 84.4 | 66.7 | 29.0 | 45.4 | 51.6 |
| <strong>DeepScaleR-1.5B-Preview</strong> | <strong>43.1</strong> | <strong>87.8</strong> | <strong>73.6</strong> | 30.2 | <strong>50.0</strong> | <strong>57.0</strong> |
| O1-Preview | 40.0 | 81.4 | - | - | - | - |

## Serving DeepScaleR
Our model can be served using popular high-performance inference systems:
- vLLM
- Hugging Face Text Generation Inference (TGI)
- SGLang
- TensorRT-LLM

All these systems support the OpenAI Chat Completions API format.

## License
This project is released under the MIT License, reflecting our commitment to open and accessible AI development.
We believe in democratizing AI technology by making our work freely available for anyone to use, modify, and build upon.
This permissive license ensures that researchers, developers, and enthusiasts worldwide can leverage and extend our work without restrictions, fostering innovation and collaboration in the AI community.

## Acknowledgement
- Our training experiments are powered by our heavily modified fork of [Verl](https://github.com/agentica-project/verl), an open-source RLHF library.
- Our model is trained on top of [`DeepSeek-R1-Distill-Qwen-1.5B`](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B).
- Our work is done as part of  [Berkeley Sky Computing Lab](https://skycomputing.berkeley.edu/) and [Berkeley AI Research](https://bair.berkeley.edu/).

## Citation 
```bibtex
@misc{deepscaler2025,
  title={DeepScaleR: Surpassing O1-Preview with a 1.5B Model by Scaling RL},
  author={Michael Luo and Sijun Tan and Justin Wong and Xiaoxiang Shi and William Y. Tang and Manan Roongta and Colin Cai and Jeffrey Luo and Li Erran Li and Raluca Ada Popa and Ion Stoica},
  year={2025},
  howpublished={\url{https://pretty-radio-b75.notion.site/DeepScaleR-Surpassing-O1-Preview-with-a-1-5B-Model-by-Scaling-RL-19681902c1468005bed8ca303013a4e2}},
  note={Notion Blog}
  year={2025}
}