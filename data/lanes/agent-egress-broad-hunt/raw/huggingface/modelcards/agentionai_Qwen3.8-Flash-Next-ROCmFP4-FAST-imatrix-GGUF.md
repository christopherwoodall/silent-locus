---
base_model:
- Qwen/Qwen3.8-Flash-Next
base_model_relation: quantized
license: other
license_name: qwen-community-1.0
license_link: LICENSE
library_name: gguf
pipeline_tag: text-generation
tags:
- gguf
- rocmfp4
- rocmfpx
- vulkan
- strix-halo
- qwen4exp
- imatrix
---

# Qwen3.8-Flash-Next ROCmFP4-FAST imatrix GGUF

A 180 B model that runs **entirely on the GPU** of a 128 GB unified-memory box —
87.06 GiB at 4.23 bpw, within 2.5% perplexity of the unquantized model. Sized for the
96 GiB VRAM carve-out of a Strix Halo (Ryzen AI MAX+ 395 / Radeon 8060S).

Built and published by [Agention](https://agention.ai).

![Prefill and generation throughput against context depth, for this file on the fork and AP-IQ4_XS on both the fork and mainline](https://huggingface.co/agentionai/Qwen3.8-Flash-Next-ROCmFP4-FAST-imatrix-GGUF/resolve/main/assets/throughput-vs-depth.png)

*Throughput against context depth, against our closest mainline-compatible quant run on both this fork and stock llama.cpp — numbers and discussion under [Holding up at long context](#holding-up-at-long-context).*

**Why this one**

- **Everything stays on the GPU.** Not the experts, not the 51.2 B-parameter n-gram
  table. No host-RAM fallback, no CPU compute in the hot path.
- **Fast prefill that holds at depth** — 423 t/s at 512 tokens, 357 t/s at 8k, still
  245 t/s at 32k and 138 t/s at 128k. Prefill is compute-bound and the ROCmFP4 types
  are cheaper to dequantize. Matters most for long prompts, agentic loops, and
  anything that re-reads a large context.
- **Better perplexity than that same mainline tier**, by about two standard errors,
  and better than AesSedai's IQ4_XS and IQ3_S at 20–30 GB smaller.
- **Vision included** — the model's own tower, at f16, losslessly converted.
- **Speculative decoding included** — the model's own MTP head. Up to **40 tok/s
  generation** observed on a Strix Halo with adaptive drafting; acceptance is
  content-dependent, so the rate moves with what you are generating.
- **imatrix-calibrated** on 1540 chunks from two corpora, so the low-bit tensors are
  fitted to real activations rather than assumed.

**Two layouts**, identical weights and identical size (splitting the n-gram table per
head is a byte-for-byte restructuring, not a re-quantize):

- **root** — table split per head, fully VRAM-resident. *Use this one.*
- **`v2/`** — table as a single tensor; portable, but needs `--ngram-on-disk` or host
  RAM for it, since one tensor that size exceeds what most Vulkan devices accept as a
  single buffer.

## Setup

Qwen3.8-Flash-Next itself is upstream ([ggml-org/llama.cpp#27742](https://github.com/ggml-org/llama.cpp/pull/27742)).
Our fork, [agentionai/llama.cpp](https://github.com/agentionai/llama.cpp) (default branch `main`), is still needed for the ROCmFPx quant types and the per-head PLE layout as well as the performance improvements listed above.

```bash
git clone https://github.com/agentionai/llama.cpp
cd llama.cpp
cmake -B build -DGGML_VULKAN=ON -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
```

### Docker

Prefer not to build? Our server image has the fork with Vulkan built in:
`ghcr.io/agentionai/agention-llama:server` (also on Docker Hub as `agentionai/agention-llama:server`).

```bash
hf download agentionai/Qwen3.8-Flash-Next-ROCmFP4-FAST-imatrix-GGUF \
  Qwen3.8-Flash-Next-ROCmFP4-FAST-v2-ple16.gguf --local-dir ~/models

# AMD (and Intel) GPUs
docker run --rm -it --device /dev/dri --group-add "$(getent group render | cut -d: -f3)" \
  -v ~/models:/models -p 8080:8080 ghcr.io/agentionai/agention-llama:server \
  -m /models/Qwen3.8-Flash-Next-ROCmFP4-FAST-v2-ple16.gguf \
  -ngl 99 -ctk q8_0 -ctv q8_0 -fa on --jinja
```

**NVIDIA:** replace `--device /dev/dri --group-add ...` with `--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all`.
Web chat at http://127.0.0.1:8080, OpenAI-compatible API at `http://127.0.0.1:8080/v1`.

## Run

```bash
# recommended: per-head table, everything on the GPU
./build/bin/llama-server \
  -m Qwen3.8-Flash-Next-ROCmFP4-FAST-v2-ple16.gguf \
  -ngl 99 -ctk q8_0 -ctv q8_0 -fa on

# joined table, kept off the GPU and off host RAM
./build/bin/llama-server \
  -m v2/Qwen3.8-Flash-Next-ROCmFP4-FAST-imatrix-v2.gguf \
  -ngl 99 --ngram-on-disk --ngram-cache 8192
```

`--ngram-cache` defaults to 256 MiB; raise it for long generations, or throughput drops
off over the course of a conversation.

**Quantized KV (`-ctk q8_0 -ctv q8_0 -fa on`) is worth using.** Only 12 of the 48 layers
are full-attention, so the cache is small to begin with -- about 12.75 KiB/token at q8_0
against 24 KiB at f16. That is ~3.2 GiB for the model's full 262144-token context instead
of ~6 GiB, which is what makes long context fit next to 87 GiB of weights in a 96 GiB
carve-out. Measured no throughput cost.

### Vision

`mmproj/mmproj-Qwen3.8-Flash-Next-f16.gguf` is the model's own vision tower (f16, lossless —
the vision weights were excluded from the upstream FP8 release, so nothing was
re-quantized). Add it and send images through the OpenAI-compatible endpoint:

```bash
./build/bin/llama-server \
  -m Qwen3.8-Flash-Next-ROCmFP4-FAST-v2-ple16.gguf \
  --mmproj mmproj/mmproj-Qwen3.8-Flash-Next-f16.gguf \
  -ngl 99
```

### Speculative decoding (MTP)

The model ships its own multi-token-prediction head, packaged separately as
[`Qwen3.8-Flash-Next-MTP-ROCmFP4-FAST-GGUF`](https://huggingface.co/agentionai/Qwen3.8-Flash-Next-MTP-ROCmFP4-FAST-GGUF)
(2.28 GiB). Let the draft length adapt -- acceptance varies a lot with content, and a
fixed depth is either too shallow on code or too greedy on prose:

```bash
./build/bin/llama-server \
  -m Qwen3.8-Flash-Next-ROCmFP4-FAST-v2-ple16.gguf \
  -md Qwen3.8-Flash-Next-MTP-ROCmFP4-FAST.gguf \
  --spec-type draft-mtp --spec-draft-adaptive \
  --spec-draft-n-min 2 --spec-draft-n-max 4 \
  -ngl 99 --n-gpu-layers-draft 99 \
  -ctk q8_0 -ctv q8_0 -fa on
```

### Sampling

Qwen's recommended settings:

| parameter | thinking mode | instruct (non-thinking) |
|---|---|---|
| temperature | 1.0 | 0.7 |
| top_p | 0.95 | 0.80 |
| top_k | 20 | 20 |
| min_p | 0.0 | 0.0 |
| presence_penalty | 0.0 | 1.5 |
| repetition_penalty | 1.0 | 1.0 |

## Perplexity

wikitext-2 raw, 145 chunks at `-c 2048`.

| build | PPL | vs. reference |
|---|---|---|
| unquantized reference (as reported in PR 27742) | 4.0068 +/- 0.02271 | - |
| **this file** | **4.1062 +/- 0.02329** | **+2.48%** |

Against [AesSedai](https://huggingface.co/AesSedai/Qwen3.8-Flash-Next-GGUF)'s quants,
compared the fair way (each build's PPL against its own measured reference, since their
test methodology differs from ours):

| build | size | PPL ratio vs. own reference |
|---|---|---|
| AesSedai IQ3_S | 107.38 GiB | +6.10% |
| **this file** | **87.06 GiB** | **+2.48%** |
| AesSedai IQ4_XS | 117.13 GiB | +3.12% |
| AesSedai Q4_K_M | 135.38 GiB | +0.61% |

Beats their IQ4_XS and IQ3_S on quality at a smaller size.

## Holding up at long context

A separate, deeper sweep — same box, `q8_0` KV, arms interleaved — against `AP-IQ4_XS`
([Qwen3.8-Flash-Next-AP-GGUF](https://huggingface.co/agentionai/Qwen3.8-Flash-Next-AP-GGUF))
run two ways: on this fork, and on stock llama.cpp (30 August 2026 build). Numbers are relative and exclude MTP.

The chart at the top of this card plots these figures.

**Prefill (t/s)**

| depth | this file | AP-IQ4_XS (fork) | AP-IQ4_XS (mainline) |
|---|---|---|---|
| 512 | **423.3** | 315.9 | 245.6 |
| 2048 | **406.5** | 302.8 | 219.7 |
| 8192 | **357.2** | 275.1 | 153.0 |
| 16384 | **301.0** | 232.4 | 107.4 |
| 32768 | **245.5** | 194.2 | 70.6 |
| 65536 | **188.0** | 150.9 | — |
| 131072 | **137.7** | 122.3 | — |

**Generation (t/s) no MTP**

| depth | this file | AP-IQ4_XS (fork) | AP-IQ4_XS (mainline) |
|---|---|---|---|
| 512 | **27.77** | 25.05 | 26.39 |
| 2048 | **27.36** | 24.75 | 22.70 |
| 8192 | **26.67** | 25.07 | 18.67 |
| 16384 | **25.54** | 22.91 | 16.22 |
| 32768 | **24.67** | 22.46 | 11.85 |
| 65536 | **23.09** | 21.08 | — |
| 131072 | **19.70** | 18.10 | — |

The mainline column stops at 32k. Run abandoned early.

Two separate things are visible here, and they are worth keeping apart:

- **The layout, more than the quant.** This file prefills 12-34% faster than
  `AP-IQ4_XS` on the same binary, but the two differ in more than their quant type:
  this one splits the n-gram table per head so it lives in VRAM, while `AP-IQ4_XS`
  keeps it as one 28.8 GiB tensor in host RAM. Some of the gap is the ROCmFP4 types
  being cheaper to dequantize and some is that table placement — this comparison does
  not separate them.
- **The fork.** The same `AP-IQ4_XS` file on stock llama.cpp is the bottom line on both
  panels, and the gap widens with depth: 1.3x slower prefill at 512, 2.8x at 32k. Decode
  falls off harder still — 11.85 t/s against 22.46 at 32k. Shallow, mainline is
  competitive and actually wins decode at 512 (26.39 vs 25.05); the fork's long-context
  work costs a little there and pays for itself by 8k.

At 128k this file still generates at 19.7 t/s, 71% of its 512-depth speed.

## 🛠️ 7. Method and tooling
The tiers are built with our own Rust tooling. `gguf-pack` for
byte-exact, content-addressed tier builds and validation, `gguf-info` for inspection, and a per-tensor
distortion solver behind the Agention Precision recipes. Every tier is measured against BF16 on a held-out 
2026 corpus before it ships.

## Credits

`qwen4exp` support is the work of **Daniel Han**
([@danielhanchen](https://github.com/danielhanchen)), from
[ggml-org/llama.cpp#27742](https://github.com/ggml-org/llama.cpp/pull/27742), merged
upstream. This fork is only still needed for what's listed under Setup above.

Quant formats hand-ported from [ciru-ai/ROCmFPX](https://github.com/ciru-ai/ROCmFPX).
The ROCmFP4 format was created by [charlie12345](https://github.com/charlie12345) in
[charlie12345/ROCmFPX](https://github.com/charlie12345/ROCmFPX), which ciru-ai's tree forks.
Both upstream projects are MIT-licensed.
Calibration corpora from bartowski and Thireus, credited above. Base model by the Qwen
team.

Quantized and published by [Agention](https://agention.ai).

## License

Qwen Community License 1.0, included as `LICENSE`.

### Support AgentionAI
This quant is released freely. If it saves you compute or makes Qwen more useful, you can sponsor continued tuning, quantization and benchmarking on [GitHub](https://github.com/sponsors/agentionai).
