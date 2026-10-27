---
base_model:
- Qwen/Qwen3.8-Flash-Next
base_model_relation: quantized
license: other
license_name: qwen-community-1.0
library_name: gguf
pipeline_tag: text-generation
tags:
- gguf
- qwen3.8-flash-next
- qwen4exp
- code
- experimental
- agentionai
---

<img src="gyro-coder-header.png" alt="AgentionAI — Gyro Coder 3.8 Flash Next" width="100%">

# Qwen3.8-Flash-Next Gyro-Coder — GGUF

**A 125B-parameter coding model on one 24 GB card.**

Qwen3.8-Flash-Next is a 125B mixture-of-experts model, the kind that normally needs a workstation full of GPUs.
Gyro-Coder brings it to a single RTX 3090, 4090 or 7900 XTX: 19.9 GiB of GPU memory.

**New: Gyro-Coder-L for 32 GB cards.** The same experts at about 3.2 bits per weight: 27.5 GiB of GPU memory, and
closer to the full model than Gyro-Coder on every set we measure. On C++ it is closer than Gyro-M, which keeps all 512 experts.

**Preview: Gyro-Coder-L v1.1** (`Qwen3.8-Flash-Next-Gyro-Coder-L-TQ3_0-v1.1.gguf`, same size): an improved encode of the
same experts. A tester found that v1.0 writes some Roman numerals wrong (900, 500, 400) and
then rewrites the same file in a loop. v1.1 writes a correct `int_to_roman` in 5 of 5 runs (v1.0: 3 of 5, one loop); asked
for the bare 13-pair table in one greedy request it still writes 500 as `V`. Code and bash gates are running; v1.1
replaces v1.0 as the main file if they pass.

Two things make that possible:
- **Only the experts that code.** Each layer keeps the 256 of its 512 experts that matter for programming, picked by
  an evolutionary search over a space of 10⁷³²⁸ possible combinations (see below). That leaves 65B parameters on the GPU.
- **2.125 bits per weight, without the usual damage.** The experts are stored with our own trellis encoder, the
  same one that puts Gyro-M ahead of IQ3_XXS and UD-Q2_K_XL quants that need 20-25% more memory.

On held-out Python it picks the same next token as the full model 93% of the time. Give it clear instructions
(implement this, fix that, refactor, explain) and it delivers. For open-ended work and general knowledge,
[Gyro-S](https://huggingface.co/agentionai/Qwen3.8-Flash-Next-Gyro-GGUF) or Gyro-M is the better pick.

Runs in our llama.cpp build (Docker, see Quick start). [Strata](https://github.com/Niko1221/Strata) support is coming.

| Headline | Detail |
|---|---|
| **19.92 GiB of GPU weights** | 21.1 GiB with 64k context (q8_0 KV): fits a 24 GB card |
| **94.5% top-1 agreement on C++** | KLD 0.118 (Python 93.1%, 0.165) |
| **13/16 coding tasks passed** | auto-graded, 8 tasks x 2 seeds; the same experts at 8 bits pass 15/16 |
| **Gyro-Coder-L: 95.5% top-1 on C++** | KLD 0.077 in 27.54 GiB (Gyro-M, all 512 experts: 0.082 in 34.98 GiB) |

## Pick your file

| Your hardware | File | GPU memory (weights) |
|---|---|---:|
| 24 GB card (RTX 3090 / 4090, 7900 XTX) | **`Qwen3.8-Flash-Next-Gyro-Coder-TQ2_0.gguf`** | 19.92 GiB |
| 32 GB card (RTX 5090, R9700), code | **`Qwen3.8-Flash-Next-Gyro-Coder-L-TQ3_0.gguf`** | 27.54 GiB |
| 32 GB, general use as well as code | [Gyro-S](https://huggingface.co/agentionai/Qwen3.8-Flash-Next-Gyro-GGUF) | 27.64 GiB |
| 48 GB+, general use as well as code | [Gyro-M](https://huggingface.co/agentionai/Qwen3.8-Flash-Next-Gyro-GGUF) | 34.98 GiB |

The `TQ2_0` / `TQ3_0` in the names are only size classes for the Hub: **stock llama.cpp cannot load this file.**

## A needle in a very large haystack

Each layer keeps 256 of its 512 experts. That is about 10¹⁵² possible choices for one layer, and about **10⁷³²⁸**
for the whole model: written out, the number fills about four pages. If you had tested a billion candidate models
every second since the Big Bang, you would have covered about 10⁻⁷³⁰¹ of them.

The layers don't act alone either: what one layer keeps changes what every later layer sees, and each candidate is
a full model that has to be built and tested before you know whether it is any good.

We started by mapping which experts carry which domains. From there, an evolutionary search proposed and scored
about 2,200 candidate expert sets across 14 runs. The best were built as full models and put through coding, loop
and knowledge tests. This is the one that passed.

## Quality

KL divergence and top-1 agreement against the full model (Q8_0, all 512 experts), `-c 2048`.

| Set | Gyro-Coder KLD ↓ | top-1 ↑ | Gyro-Coder-L KLD ↓ | top-1 ↑ |
|---|---:|---:|---:|---:|
| C++ (held-out source files) | 0.118 | 94.5% | **0.077** | **95.5%** |
| web (TypeScript / JS) | 0.142 | 92.5% | **0.108** | **93.7%** |
| SQL | 0.145 | 92.7% | **0.114** | **93.6%** |
| Python | 0.165 | 93.1% | **0.132** | **94.0%** |
| Rust | 0.223 | 88.7% | **0.189** | **89.5%** |
| shell | 0.417 | 80.9% | **0.371** | **82.3%** |
| knowledge (descriptions of everyday things) | 0.301 | 80.8% | **0.237** | **83.6%** |
| held-out (2026 technical writing and code) | 0.579 | 70.8% | **0.521** | **72.0%** |

Half the experts are gone, so general text and knowledge lose the most (Gyro-M: held-out 0.291); code stays close
to the full model.

**Coding tests:** 13 of 16 passed (8 auto-graded tasks: LRU cache, interval merging, bug fix from a trace, refactor,
bash script, SQL, CSV parsing in JS, multi-file change; 2 seeds each, thinking on, 64k tokens). The same expert set at
8 bits passes 15 of 16. Gyro-Coder-L passes 15 of 16.

## Speed

Strix Halo (Vulkan, MTP draft): 11–22 tok/s per stream with two streams running at once (measured while
generating long answers).

## Quick start

**1. Download Gyro-Coder** (70.6 GiB on disk; Gyro-Coder-L 78.2 GiB; put it on a fast NVMe drive):

```bash
pip install -U huggingface_hub
hf download agentionai/Qwen3.8-Flash-Next-Gyro-Coder-GGUF Qwen3.8-Flash-Next-Gyro-Coder-TQ2_0.gguf --local-dir ~/models
# 32 GB card: Qwen3.8-Flash-Next-Gyro-Coder-L-TQ3_0.gguf (and use that name below)
```

**2. Run it** with our [llama.cpp build](https://gitlab.com/agentionai-group/llama.cpp) (Vulkan, in Docker):

```bash
# AMD (and Intel) GPUs
docker run --rm -it --device /dev/dri --group-add "$(getent group render | cut -d: -f3)" \
  -v ~/models:/models -p 8080:8080 agentionai/agention-llama:server \
  -m /models/Qwen3.8-Flash-Next-Gyro-Coder-TQ2_0.gguf -ngl 999 -fa on --jinja --ngram-on-disk \
  -c 65536 -ctk q8_0 -ctv q8_0 --temp 0.6 --top-p 0.95 --top-k 20 --min-p 0.05
```

**NVIDIA:** replace `--device /dev/dri --group-add ...` with `--gpus all -e NVIDIA_DRIVER_CAPABILITIES=all`.

Web chat at http://127.0.0.1:8080, OpenAI-compatible API at `http://127.0.0.1:8080/v1`: point your coding agent or
editor plugin there.

**Strata:** support is coming. Strata 0.2.2 does not know this file yet (Gyro-S and Gyro-M already run there); we will
update this card when it does.

## Recommended settings

- Sampling: `--temp 0.6 --top-p 0.95 --top-k 20 --min-p 0.05` (the settings all our tests used).
- Keep `--ngram-on-disk`, with the model on fast NVMe: the 50.7 GiB n-gram table stays on disk, which is why the file
  (70.6 GiB) is much larger than its GPU footprint.
- Give it clear instructions; it does best on well-specified tasks.


## Credits

Built and tested on AMD Ryzen AI Max (Strix Halo). Hardware supported by AMD

Tensor format: trellis-coded quantization with Hadamard rotation, in the family of QTIP (Tseng et al., 2024). Encoder, trellis types and kernels: AgentionAI. Base model: Qwen/Qwen3.8-Flash-Next. Runtimes: llama.cpp, Strata, strix-llama.cpp.

The Gyro format is open: specification, reference decoder and encoder, and bit-exact tests (Apache 2.0) at [agentionai-group/agention-gyro](https://gitlab.com/agentionai-group/agention-gyro). The released files come from our own production encoder.


### Support AgentionAI

These quants are released freely. If they save you VRAM or make Qwen more useful, you
can buy me a coffee or some GPU time and sponsor continued quantization and benchmarking on
[Buy Me A Coffee](https://buymeacoffee.com/agentionai). AgentionAI is a one-person team and can use your help.

