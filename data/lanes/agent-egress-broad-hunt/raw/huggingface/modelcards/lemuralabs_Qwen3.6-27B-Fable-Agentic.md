---
license: apache-2.0
language:
- en
base_model:
- Jackrong/Qwopus3.6-27B-v2
pipeline_tag: text-generation
library_name: transformers
tags:
- agentic
- tool-calling
- function-calling
- reasoning
---

<p align="center">
  <img src="logo.png" alt="Lemura Labs" width="110"/>
</p>

<div align="center">

# Qwen3.6-27B-Fable-Agentic

![Format](https://img.shields.io/badge/Format-Safetensors-0b7285?style=flat) ![Task](https://img.shields.io/badge/Task-Text%20Generation-5f3dc4?style=flat) ![Params](https://img.shields.io/badge/Params-27B-1864ab?style=flat) ![Type](https://img.shields.io/badge/Type-Agentic-862e9c?style=flat) ![License](https://img.shields.io/badge/License-apache--2.0-6c757d?style=flat)


### Agentic - Reasoning - Tool-Calling - Top-Tier Knowledge

![MMLU-Pro](https://img.shields.io/badge/MMLU--Pro-88.29%25-2ea44f?style=flat) ![GSM8K](https://img.shields.io/badge/GSM8K-97.33%25-2ea44f?style=flat) ![GPQA](https://img.shields.io/badge/GPQA--Diamond-57.07%25-2ea44f?style=flat) ![Tool Calling](https://img.shields.io/badge/Tool--Calling-enabled-1f6feb?style=flat)
*Beats its base model on knowledge - and acts like an agent.*

</div>

---

**Qwen3.6-27B-Fable-Agentic** is a powerful 27B agentic model that reasons step-by-step and operates tools across multi-turn sessions, while delivering top-tier general knowledge. Fine-tuned from [Jackrong/Qwopus3.6-27B-v2](https://huggingface.co/Jackrong/Qwopus3.6-27B-v2).

## Benchmarks

Evaluated head-to-head against the base model on identical questions, with an 8192-token budget so step-by-step reasoning is never truncated.

| Benchmark | Base | **This model** |
|:---|:---:|:---:|
| MMLU-Pro (350 Q) | 86.86% | **88.29%** |
| GSM8K (300 Q) | 98.00% | 97.33% |
| GPQA-Diamond (198 Q) | 57.58% | **57.07%** |

> **Knowledge improved, hard reasoning preserved:** +1.43 over base on MMLU-Pro, matching it on GSM8K math and on GPQA-Diamond (graduate-level science, ~frontier-class for a 27B) - with agentic tool-calling added on top.

<details>
<summary><b>MMLU-Pro by category</b></summary>

| Category | Base | This model |
|:---|:---:|:---:|
| Biology | 96.0% | 94.0% |
| Business | 78.0% | **88.0%** |
| Chemistry | 84.0% | 80.0% |
| Computer Science | 84.0% | 84.0% |
| Health | 82.0% | **86.0%** |
| Math | 94.0% | 94.0% |
| Physics | 90.0% | **92.0%** |
| **Overall** | 86.86% | **88.29%** |

</details>

## Highlights

- **Top-tier knowledge** - 88.29% MMLU-Pro, above the base model
- **Strong math** - 97.33% GSM8K
- **Agentic tool-calling** across multi-turn sessions
- **Step-by-step reasoning** built in

## Capabilities

- Agentic, multi-turn tool-calling
- Chain-of-thought reasoning
- Top-tier general knowledge and math
- Multimodal (vision + text) architecture

## Usage (vLLM)

```bash
vllm serve lemuralabs/Qwen3.6-27B-Fable-Agentic --trust-remote-code --reasoning-parser qwen3 --enable-auto-tool-choice --tool-call-parser qwen3_coder --max-model-len 16384
```

> Tip: this model reasons before answering - give it a generous max_tokens so it can finish its chain of thought.

## License

Apache 2.0
