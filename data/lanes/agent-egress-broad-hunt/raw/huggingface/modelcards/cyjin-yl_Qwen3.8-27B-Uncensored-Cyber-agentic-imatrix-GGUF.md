---
license: apache-2.0
base_model: philbert440/Qwen3.8-27B-Uncensored-Cyber
tags:
  - gguf
  - imatrix
  - quantized
  - agentic
  - qwen3
  - llama.cpp
  - v100
  - uncensored
  - abliterated
  - cyber
pipeline_tag: image-text-to-text
---

# Qwen3.8-27B-Uncensored-Cyber — GGUF quantized with an **agentic** imatrix

GGUF quantizations of [philbert440/Qwen3.8-27B-Uncensored-Cyber](https://huggingface.co/philbert440/Qwen3.8-27B-Uncensored-Cyber),
calibrated on an importance matrix built from **real agentic-coding traffic** rather than
generic English prose.

**All model weights and behaviour are philbert440's work. This repository contributes
only the quantization and the calibration methodology** — no fine-tuning, no merging, no
behavioural change of any kind was performed here.

Inherited from upstream, and stated plainly so nobody is surprised: this is a
**de-refusal ("abliterated") model specialized for the cyber/offensive-security domain**.
The vision tower and the MTP speculative-decoding head are preserved upstream, which is
what makes the multimodal path and the MTP graft work at all. Read
[the base model's card](https://huggingface.co/philbert440/Qwen3.8-27B-Uncensored-Cyber)
before using it — it documents the recipe and the evaluation.

> **Status (2026-08-20): the imatrix and both IQ4_XS artifacts are uploaded.**
> Sizes and SHA-256 values below are the Hugging Face LFS objects, checked against the
> local production artifact for the MTP build.

## Files

| File | Size | SHA-256 | Intended use |
|---|---:|---|---|
| `imatrix-agentic-v2.gguf` | 13.01 MiB | `a219ff5f3ffabb4a4b7cc644cae3a44f647032e2016b3308843ac8650e59af69` | Published calibration matrix |
| `Qwen3.8-27B-Uncensored-Cyber-IQ4_XS-imatrix-fromq8.gguf` | 14.96 GiB | `d11d28b9b253fb7fc9de277a46af5bbd790c000d6bfdfe5648fd7b62ec2560b7` | IQ4_XS text weights without the grafted MTP tensors |
| `Qwen3.8-27B-Uncensored-Cyber-IQ4_XS-imatrix-fromq8-plus-mtp.gguf` | 15.38 GiB | `da6a418f30a7e6c6669b74179f6d533ca06016e02eba298d2b713a2900d7a1ba` | Current FastLLM production artifact; includes the compatible MTP head |

The two model files have identical IQ4_XS/imatrix text weights. The `plus-mtp` file adds
the MTP tensors from the matching upstream model; use it only with a runtime that
recognizes that graft. For a conventional GGUF loader, use the non-MTP file unless its
MTP support has been verified. The Q5_K_M comparison below was measured locally and is
not published in this repository.

## Why a different calibration corpus

The usual llama.cpp calibration sets (`wiki.train.raw`, `groups_merged.txt`) are generic
prose. The tokens that actually break under quantization in agentic use are a different
population:

- tool-call JSON and tool names (`bash`, `read`, `web_search`)
- chat-template special tokens (`<|im_start|>`, `<tool_call>`)
- long literals that must be reproduced verbatim — repository paths, package names,
  commit hashes, device UUIDs
- mixed Chinese/English (prose in Chinese, paths and code in English)

Those barely occur in generic prose, so a prose-derived imatrix treats their channels as
unimportant and the quantizer spends its error budget there first. The concrete failure
this targets: an agent writing `/home/eze/Documents/PotouI` for
`/home/ezra/Documents/Proto-UI`, then reading its own mangled output back and concluding
its context is inconsistent.

## Calibration corpus

Extracted from real agent session logs (an agent CLI driving coding tasks against this
model) — not synthetic prompts:

| | |
|---|---|
| size | 1.00 MB |
| sessions sampled | 42 |
| dialogue turns | 648 |
| real tool calls | 528 (real arguments, real paths) |
| `<\|im_start\|>` occurrences | 1191 |
| `<tool_call>` occurrences | 547 |
| chunks processed | 584 @ `-c 512` |

**The corpus itself is not published.** It is private working data — real repository
paths, real shell commands, real conversations. The resulting `imatrix-agentic-v2.gguf` is
published so the method is reproducible; rebuild your own corpus from your own traffic to
reproduce it end to end.

## How it was made

```bash
# importance matrix, computed on the Q8_0 release
llama-imatrix -m Qwen3.8-27B-Uncensored-Cyber-Q8_0.gguf \
              -f calib-agentic.txt \
              -o imatrix-agentic-v2.gguf \
              -ngl 99 -c 512 --parse-special

# quantization (IQ4_XS shown; Q5_K_M identical apart from the type)
llama-quantize --allow-requantize --imatrix imatrix-agentic-v2.gguf \
               --output-tensor-type q8_0 --token-embedding-type q8_0 \
               Qwen3.8-27B-Uncensored-Cyber-Q8_0.gguf out.gguf IQ4_XS
```

Three choices worth explaining:

**`--parse-special` is not optional here.** The corpus is rendered with the model's own
chat-template markers. Without that flag llama.cpp tokenizes `<|im_start|>` as *literal
text* — `<`, `|`, `im`, `_start`, … — so the special tokens never enter the statistics at
all, which defeats the point of building this corpus. Measured effect on the same corpus
family: 0.342 → 0.299 tokens per byte (−12.7%), consistent with those markers collapsing
into single tokens.

**Context stayed at 512, deliberately.** The intuitive move is to match the 262 K context
this model is served at. Community testing says the opposite: for a fixed token budget a
small context usually beats 4096, because it yields more and more-diverse samples and a
better-conditioned estimate. 512 is also llama.cpp's long-standing default.

**`--output-tensor-type q8_0 --token-embedding-type q8_0`.** Output-layer quantization
error turns directly into picking the wrong token, which is precisely the verbatim-copy
failure above. Costs roughly 1.5 GB.

## Honest caveats

- **Quantized from the Q8_0 release, not from BF16** (`--allow-requantize`). Q8_0 is
  near-lossless and the error is dominated by the Q5/IQ4 step, but this is still a second
  quantization.
- **Comparison scope is narrow.** The measured numbers below use a held-out agentic
  corpus drawn from different sessions than calibration (verified disjoint). They test
  this deployment shape, not general writing, multilingual knowledge, or safety.
- **imatrix helps most *below* Q5_K_M.** Community consensus puts the large gains in the
  Q3/Q4 range. IQ4_XS is squarely in useful territory; Q5_K_M is near the upper edge
  where the effect gets modest.
- Calibration is domain-matched to *agentic coding*. For creative writing or general
  chat, a generic imatrix may suit you better.

## Context

Built while making this model usable for agentic work on a single **V100 32 GB (SM70)** —
FP16-only tensor cores, no INT8/FP8/FP4 TC, no `cp.async`. On that hardware decode is
memory-bandwidth bound, so IQ4_XS (~4.25 bpw) reads about 26% fewer bytes per token than
Q5_K_M (~5.33 bpw) and frees roughly 4 GB for KV cache — which is why it is the primary
target here rather than the largest quant that fits.

The production configuration used for the measurements below is FastLLM on one V100:
`IQ4_XS-imatrix-fromq8-plus-mtp`, `turbo3` KV cache, batch 4, and a 262,144-token
limit. Multimodal use also requires the matching Qwen3.8 vision projector; it is a
separate artifact and is not embedded in either text-model GGUF here.

## Lineage

```
Qwen3.8-27B                                      — Qwen team
  └─ philbert440/Qwen3.8-27B-Uncensored-Aggressive   α=1.15, recipe-v2 refusal ablation
       └─ philbert440/Qwen3.8-27B-Uncensored-Cyber   residual-cyber peel, β=1.0, apply_from=4
            └─ this repository                       quantization only
```

Quantized from philbert440's own `Qwen3.8-27B-Uncensored-Cyber-Q8_0.gguf` release.

## Credits

- **[philbert440](https://huggingface.co/philbert440)** — the Cyber model, its Aggressive
  base, and the Q8_0 GGUF these quantizations are derived from. Everything this repo is
  useful for is downstream of that work.
- **[Qwen team](https://huggingface.co/Qwen)** — Qwen3.8-27B, the underlying model.
- **[ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)** — `llama-imatrix` and
  `llama-quantize`. The importance-matrix approach itself comes from
  [PR #4861](https://github.com/ggml-org/llama.cpp/pull/4861); the GGUF imatrix format
  from [PR #9400](https://github.com/ggml-org/llama.cpp/pull/9400).
- The llama.cpp community discussions on calibration data and context size
  ([#5006](https://github.com/ggml-org/llama.cpp/discussions/5006)), which are why the
  calibration context here stayed at 512 instead of being naively enlarged.

## License

`apache-2.0`, inherited from the base model. These are quantizations of philbert440's
weights; the upstream terms govern.

---

## 实测数据(2026-08-20)

### 质量: 留出集配对困惑度

留出集与校准语料的 512 字节窗口重叠率 0.00% / 0.11%,是干净评测集。
三组用同一份留出集、同一个 `--chunks 60`。

| 组 | PPL | 体积 |
|---|---|---|
| IQ4_XS + 本 imatrix | 2.6989 ± 0.0471 | 15.0 GiB |
| Q5_K_M + 本 imatrix | 2.6877 ± 0.0470 | 18.6 GiB |

**不要按这两个置信区间去比。** 两组评的是同一批分块,误差高度相关,
按独立区间读会严重低估判别力。做配对比较(逐块还原 NLL 后对差值做检验):

```
IQ4_XS vs Q5_K_M   ΔPPL = +0.417% ± 0.187%   t = 2.22   60 块中 39 块更差
```

也就是说:从 5.33 bpw 降到 4.25 bpw 的代价是 **0.42%**,差异真实、方向一致,
但幅度很小。配对把不确定度从 ±1.74% 压到 ±0.187%,约 9 倍。

### 功能: 走真实推理栈(fastllm on V100)的验收

| 项 | IQ4_XS+imatrix | 对照 Q5_K_M |
|---|---|---|
| 逐字抄写保真(7 条真实字面量) | 7/7 | 7/7 |
| 工具名保真(小写/snake/camel) | 3/3 | — |
| 262K 上下文 | 是 | 是 |
| MTP 接受率(drafts=2) | 92.19% / 85.94% | — |

"逐字抄写"测的是模型把上下文里的路径、UUID、commit 哈希原样复制的能力。
它比困惑度更贴近 agent 的真实失败模式:抄歪一个字符命令就失败,而困惑度
是全词表平均,对这种尾部行为几乎不敏感。

### 速度: 控制上下文长度后的配对结果

早期把不同上下文长度的请求直接比较,一度误判 IQ4_XS 比 Q5_K_M 慢。控制成
相同 token 形状后,8 组端到端配对样本全部同向:IQ4_XS 平均为 Q5_K_M 的
**1.20x**。这是单卡 V100 + FastLLM 的部署结果,不是跨推理栈的通用保证。

当前生产仍有明确的算子余量:decode 的主路径是通用 `mmvq`,而 SM70 IQ4_XS
MMQ 只覆盖较大的 `n`;因此 1.20x 主要来自更低的权重带宽和当前融合路径,
不代表专用 decode kernel 已经用满硬件。
