---
library_name: transformers
license: apache-2.0
pipeline_tag: text-generation
tags:
  - vlm
  - vision
  - agentic
---

# Agents-A1: Scaling the Horizon, Not the Parameters: Reaching Trillion-Parameter Performance with a 35B Agent

<div style="display: flex; flex-direction: column; align-items: center; line-height: 1.2;">
  <div style="display: flex; justify-content: center; align-items: center; gap: 10px; height: 30px;">
    <span style="font-size: 16px;" role="img" aria-label="Homepage">🏠</span>
    <a href="https://internscience.github.io/Agents-A1/"><b>Homepage</b></a>
    <span style="color: #ccc;">|</span>
    <img src="./figures/24px.svg" width="16" height="16" alt="Technical Report" style="filter: invert(0.5);">
    <a href="https://arxiv.org/abs/2606.30616"><b>Technical Report</b></a>
  </div>

  <div style="display: flex; justify-content: center; align-items: center; gap: 10px; height: 30px; margin-top: 2px;">
    <img src="./figures/hf-logo.svg" width="16" height="16" alt="Hugging Face">
    <a href="https://huggingface.co/InternScience/Agents-A1"><b>Hugging Face</b></a>
    <span style="color: #ccc;">|</span>
    <img src="./figures/github-logo.svg" width="16" height="16" alt="GitHub">
    <a href="https://github.com/InternScience/Agents-A1"><b>Github</b></a>
    <span style="color: #ccc;">|</span>
    <img src="./figures/modelscope-logo.svg" width="16" height="16" alt="Model Scope">
    <a href="https://modelscope.cn/models/InternScience/Agents-A1"><b>ModelScope</b></a>
  </div>
</div>

> [!Note]
> This repository contains model weights and configuration files for Agents-A1 in the Hugging Face Transformers format.
>
> These artifacts are compatible with Hugging Face Transformers, vLLM, SGLang, etc.


---

## 🔥 News
- **2026.7.14**: 🔥🔥 The 4B model has been released.

- **2026.7.8**: 🔥🔥 By popular demand from the community, our 4B model is coming in the next few days — making it faster and easier to build your own local AI assistant.

- **2026.7.2**: 🔥🔥 Based on Agents-A1, we have released a series of quantized model variants. Please refer to the [Agents-A1 collection](https://huggingface.co/collections/InternScience/agents-a1). Besides, we’d like to thank the [mlx-community](https://huggingface.co/collections/mlx-community/agents-a1) for providing quantized versions at multiple scales. Try running Agents-A1 on your Mac!

- **2026.6.26**: 🔥🔥 We have open-sourced the Agents-A1 35B-A3B model, along with the evaluation code for selected domains and the technical report.

---

**Agents‑A1** is a long-horizon agentic model from [InternScience](https://huggingface.co/InternScience), built to scale heterogeneous agentic abilities across multiple domains including **Long‑horizon Search, Engineering, Scientific Research, Instruction Following, and Tool-calling**. We investigate agent-horizon scaling from two perspectives: scaling long-horizon trajectories and scaling heterogeneous agent abilities. 

From the scaling of long-horizon trajectories, **Agents‑A1** is trained with the assistance of a domain-grounded knowledge-action infrastructure that jointly constructs actions, observations, and verifier outcomes, turning the agent's process into a trainable target. From the scaling of heterogeneous agent abilities, **Agents‑A1** presents a three-stage training paradigm for building scalable general-purpose agentic model. First, we perform full-domain supervised fine-tuning to align the base model with broad agentic behaviors. Second, we train domain-level teacher models to capture specialized expertise in each domain. Third, we propose multi-teacher multi-domain on-policy distillation with heterogeneity-aware optimization to improve knowledge transfer efficiency across different domains.


## Highlights

- **Agentic Reasoning**: Agents-A1 excels at decomposing complex tasks into executable sub-steps, planning ahead, and adapting its strategy based on intermediate results.
- **Tool Use**: Natively supports function calling and tool integration, enabling seamless interaction with APIs, code interpreters, search engines, and other external tools.
- **Scientific and Professional Reasoning**: Handles tool-integrated scientific reasoning and professional knowledge question answering.
- **Instruction Following**: Precisely follows detailed, multi-constraint instructions across diverse domains.

We welcome developers and enterprises to integrate and try Agents-A1 and share their feedback.

## Performance

We release the dense model Agents-A1-4B with only 4B parameters, yet it delivers impressive performance across long-horizon search, engineering & research, instruction following, and general/scientific agentic tasks. It significantly outperforms similarly-sized models on BrowseComp (66.8), XBench-DS-2510 (90.0), GAIA (95.1), FrontierScience-Research (33.3), and IFEval (94.8), with some scores approaching or even surpassing larger MoE models like Nex-N2-mini and Qwen3.6. Compared to the flagship 35B Agents-A1, the 4B variant achieves strong competitiveness with a fraction of the parameters, demonstrating the series' excellent balance between efficiency and performance, and continuously narrowing the gap between small models and frontier systems.

<p>
🥇 Overall Best Performance Among Models in the Table
</p>

<table>
<thead>
<tr>
<th rowspan="2" align="left">Benchmark</th>
<th colspan="2" align="center" style="text-align:center;">
    🧠 Dense Models (~4B)
</th>
<th colspan="4" align="center" style="text-align:center;">
    🔀 MoE Models (35B-A3B)
</th>

</tr>

<tr>
<th align="center">Qwen3.5-4B</th>
<th align="center">Agents-A1-4B</th>
<th align="center">Qwen3.5</th>
<th align="center">Qwen3.6</th>
<th align="center">Nex-N2-mini</th>

<th align="center">Agents-A1</th>
</tr>
</thead>

<tbody>

<tr>
    <td colspan="7" align="left"><b>🔍 Long-horizon Search</b></td>
</tr>

<tr>
<td align="left">BrowseComp</td>
<td align="center">47.2</td>
<td align="center">66.8</td>
<td align="center">61.0</td>
<td align="center">67.9</td>
<td align="center">74.1</td>
<td align="center">🥇 75.5</td>
</tr>

<tr>
<td align="left">XBench-DS-2510</td>
<td align="center">73.0</td>
<td align="center">🥇 90.0</td>
<td align="center">77.0</td>
<td align="center">71.0</td>
<td align="center">82.0</td>
<td align="center">86.0</td>
</tr>

<tr>
<td align="left">Seal0</td>
<td align="center">31.5</td>
<td align="center">45.8</td>
<td align="center">41.4</td>
<td align="center">38.7</td>
<td align="center">49.6</td>
<td align="center">🥇 56.4</td>
</tr>

<tr>
<td align="left">GAIA</td>
<td align="center">58.3</td>
<td align="center">95.1</td>
<td align="center">59.8</td>
<td align="center">78.6</td>
<td align="center">82.5</td>
<td align="center">🥇 96.0</td>
</tr>

<tr>
    <td colspan="7" align="left"><b>⚙️ Engineering & Research Tasks</b></td>
</tr>

<tr>
<td align="left">SciCode</td>
<td align="center">16.1</td>
<td align="center">29.6</td>
<td align="center">37.7</td>
<td align="center">35.8</td>
<td align="center">29.9</td>
<td align="center">🥇 44.3</td>
</tr>

<tr>
<td align="left">MLE-Lite</td>
<td align="center">7.6</td>
<td align="center">22.7</td>
<td align="center">24.2</td>
<td align="center">34.9</td>
<td align="center">34.9</td>
<td align="center">🥇 43.9</td>
</tr>

<tr>
<td align="left">LiveCodeBench-V6</td>
<td align="center">55.8</td>
<td align="center">59.6</td>
<td align="center">76.2</td>
<td align="center">🥇 78.1</td>
<td align="center">59.1</td>
<td align="center">76.2</td>
</tr>

<tr>
<td align="left">FrontierScience-Research</td>
<td align="center">1.7</td>
<td align="center">33.3</td>
<td align="center">2.5</td>
<td align="center">2.9</td>
<td align="center">5.0</td>
<td align="center">🥇 40.0</td>
</tr>

<tr>
    <td colspan="7" align="left"><b>📋 Instruction Following</b></td>
</tr>

<tr>
<td align="left">IFBench</td>
<td align="center">59.2</td>
<td align="center">69.1</td>
<td align="center">70.2</td>
<td align="center">64.4</td>
<td align="center">54.1</td>
<td align="center">🥇 80.6</td>
</tr>

<tr>
<td align="left">LongBench-v2</td>
<td align="center">50.0</td>
<td align="center">52.1</td>
<td align="center">59.0</td>
<td align="center">57.7</td>
<td align="center">59.6</td>
<td align="center">🥇 60.2</td>
</tr>

<tr>
<td align="left">IFEval</td>
<td align="center">89.8</td>
<td align="center">🥇 94.8</td>
<td align="center">91.9</td>
<td align="center">91.3</td>
<td align="center">88.4</td>
<td align="center">🥇 94.8</td>
</tr>

<tr>
    <td colspan="7" align="left"><b>🤖 General & Scientific Agentic Tasks</b></td>
</tr>

<tr>
<td align="left">τ<sup>2</sup>-Bench</td>
<td align="center">79.9</td>
<td align="center">78.2</td>
<td align="center">🥇 81.2</td>
<td align="center">79.0</td>
<td align="center">74.5</td>
<td align="center">79.8</td>
</tr>

<tr>
<td align="left">VitaBench</td>
<td align="center">22.0</td>
<td align="center">🥇 40.3</td>
<td align="center">31.9</td>
<td align="center">35.6</td>
<td align="center">23.0</td>
<td align="center">38.8</td>
</tr>

<tr>
<td align="left">MatTools</td>
<td align="center">10.9</td>
<td align="center">🥇 49.3</td>
<td align="center">21.0</td>
<td align="center">15.9</td>
<td align="center">34.1</td>
<td align="center">47.1</td>
</tr>

</tbody>
</table>


## Usage

### SGLang

[SGLang](https://github.com/sgl-project/sglang) is a fast serving framework for large language models and vision language models.

Install SGLang with uv:

```shell
uv venv --python 3.12 --seed --managed-python
source .venv/bin/activate

uv pip install sglang
```

See [its documentation](https://docs.sglang.ai/get_started/install.html) for more details.

The following commands create API endpoints at `http://localhost:8000/v1`:

- **Standard Version** (1 GPUs, 262K context):

  ```shell
  python -m sglang.launch_server \
    --model-path InternScience/Agents-A1-4B \
    --port 8000 \
    --tp-size 1 \
    --mem-fraction-static 0.8 \
    --context-length 262144 \
    --reasoning-parser qwen3
  ```
- **Tool Use**:

  ```shell
  python -m sglang.launch_server \
    --model-path InternScience/Agents-A1-4B \
    --port 8000 \
    --tp-size 1 \
    --mem-fraction-static 0.8 \
    --context-length 262144 \
    --reasoning-parser qwen3 \
    --tool-call-parser qwen3_coder
  ```

### vLLM

[vLLM](https://github.com/vllm-project/vllm) is a high-throughput and memory-efficient inference and serving engine for LLMs.

Install vLLM from the main branch via uv:

```shell
uv venv --python 3.12 --seed --managed-python
source .venv/bin/activate

uv pip install vllm --torch-backend=auto
```

See [its documentation](https://docs.vllm.ai/en/stable/getting_started/installation/index.html) for more details.

The following commands create API endpoints at `http://localhost:8000/v1`:

- **Standard Version** (1 GPUs, 262K context):

  ```shell
  vllm serve InternScience/Agents-A1-4B \
    --port 8000 \
    --tensor-parallel-size 1 \
    --max-model-len 262144 \
    --reasoning-parser qwen3
  ```
- **Tool Call**:

  ```shell
  vllm serve InternScience/Agents-A1-4B \
    --port 8000 \
    --tensor-parallel-size 1 \
    --max-model-len 262144 \
    --reasoning-parser qwen3 \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_coder
  ```
- **Text-Only** (skips vision encoder to free KV cache memory):

  ```shell
  vllm serve InternScience/Agents-A1-4B \
    --port 8000 \
    --tensor-parallel-size 1 \
    --max-model-len 262144 \
    --reasoning-parser qwen3 \
    --language-model-only
  ```

### Recommended Sampling Parameters & System Prompt

For the best generation quality and more stable multi-turn behavior, we recommend using the following sampling parameters:

* `temperature`: 0.85
* `top_p`: 0.95
* `top_k`: 20
* `min_p`: 0.0
* `presence_penalty`: 1.1
* `repetition_penalty`: 1.0

We also recommend using the following **system prompt**:

```text
You are Intern-A1, a deep research assistant developed by InternAgent Team, Shanghai Artificial Intelligence Laboratory. 你是Intern-A1， 一个由上海人工智能实验室的InternAgent团队开发的深度研究人工智能助手。 You can have natural multi-turn conversations with users on any topic.

## Daily Chat & Simple Questions
For everyday conversations, greetings, opinions, coding help, factual lookups, definitions, calculations, explanations, and any question you can confidently answer from your knowledge — just respond directly and naturally in the user's language as Intern-A1. Do NOT use any tools for these.

## Research & Search Questions
Only when the user's question requires up-to-date information, in-depth investigation, multi-source verification, or involves recent events, niche topics, or anything you are uncertain about, use the available tool **tavily_search**.

Research strategy:
- Start with a focused search query to get an overview.
- If the initial search is insufficient, refine your query with more specific terms.
- Stop searching once you have enough information to provide a comprehensive answer. Do not over-research.

Current date: 2026-07-13
```

> [!Note]
> The current date should be updated dynamically when possible.


## Agent Capability Evaluation

To provide the community with a unified agent evaluation codebase for fair comparison, we have also open-sourced an evaluation framework for assessing agentic models across core capabilities, including tool use and multi-step reasoning. The evaluation code is included in the [Agents-A1/evaluation](https://github.com/InternScience/Agents-A1/tree/main/evaluation) of this repository.

We use this framework to evaluate the released model under a standardized and reproducible setting. 
Specifically, the model is tested on a set of agent-oriented tasks that require it to understand user goals, decompose complex instructions, interact with tools or environments when necessary, and produce final results. The evaluation results reported in [Model Card](https://huggingface.co/InternScience/Agents-A1) are generated using the open-source framework above, so that users can reproduce the experiments, compare other models under the same protocol, and further extend the benchmark for new agent scenarios. (**Note that:** To ensure a fair comparison, we report the benchmark results from their original technical reports. If a model does not report the corresponding benchmark results, we evaluate it using the same evaluation protocol as our model.)

For detailed evaluation scripts, task definitions, metrics, and reproduction instructions, please refer to the evaluation codebase.

## Citation

If you find our work helpful, feel free to give us a cite.

```
@misc{bai2026scalinghorizonparametersreaching,
      title={Scaling the Horizon, Not the Parameters: Reaching Trillion-Parameter Performance with a 35B Agent}, 
      author={Lei Bai and Zongsheng Cao and Yang Chen and Zhiyao Cui and Shangheng Du and Yue Fan and Shiyang Feng and Zijie Guo and Haonan He and Liang He and Xiaohan He and Shuyue Hu and Yusong Hu and Songtao Huang and Yichen Jiang and Hao Li and Xin Li and Dahua Lin and Weihao Lin and Fenghua Ling and Dongrui Liu and Zhuo Liu and Runmin Ma and Chunjiang Mu and Haoyang Peng and Tianshuo Peng and Jinxin Shi and Luohe Shi and Boyuan Sun and Zelin Tan and Shengji Tang and Qianyi Wang and Yiming Wu and Yi Xie and Xiangchao Yan and Jingqi Ye and Peng Ye and Fangchen Yu and Jiakang Yuan and Bihao Zhan and Bo Zhang and Chen Zhang and Shufei Zhang and Shuaiyu Zhang and Wenlong Zhang and Yiqun Zhang and Junpeng Zhao and Zhijie Zhong and Bowen Zhou and Yuhao Zhou},
      year={2026},
      eprint={2606.30616},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2606.30616}, 
}
```