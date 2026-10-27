---
base_model:
- huihui-ai/Huihui-Qwen3.8-Flash-Next-abliterated
base_model_relation: quantized
license: other
license_name: qwen-community-1.0
library_name: gguf
pipeline_tag: image-text-to-text
tags:
- gguf
- qwen3.8-flash-next
- qwen4exp
- abliterated
- uncensored
- experimental
- agentionai
---

# Qwen3.8-Flash-Next Gyro, abliterated by huihui-ai — GGUF (experimental)

**The abliterated Qwen3.8-Flash-Next on a single GPU, in two sizes.**

> **Updated 2026-10-13: both files.** Same file names, sizes and tensor types, better weights from an improved encode.

This is [huihui-ai/Huihui-Qwen3.8-Flash-Next-abliterated](https://huggingface.co/huihui-ai/Huihui-Qwen3.8-Flash-Next-abliterated)
encoded the same way as our [Gyro](https://huggingface.co/agentionai/Qwen3.8-Flash-Next-Gyro-GGUF) files. Abliteration
is huihui-ai's work: it removes the refusal direction from the model's weights. We only quantized it.

| File | For | GPU memory (64k context) | KLD vs the original model |
|---|---|---:|---:|
| **`Qwen3.8-Flash-Next-Gyro-S-abliterated-TQ1_0.gguf`** | 32 GB cards | **28.8 GiB** | 0.397 |
| **`Qwen3.8-Flash-Next-Gyro-M-abliterated-TQ2_0.gguf`** | 48 GB: 2×24 GB cards, 64 GB unified-memory machines | ~37 GiB | 0.295 |

**Which setup fits your hardware, NVIDIA and AMD instructions, context limits, vision and speculative decoding are
all on the main [Gyro card](https://huggingface.co/agentionai/Qwen3.8-Flash-Next-Gyro-GGUF) and apply unchanged here;
only the file names differ.**

Same architecture, size, speed and runtime as Gyro-S and Gyro-M. Abliteration changes 144 of the model's 1,224
weight tensors (the ones that write into the residual stream: attention and linear-attention outputs, and the down
projections of the shared and routed experts); everything else is byte-identical to the Gyro files. The `TQ1_0` /
`TQ2_0` suffix is a size class for the Hub's file browser, not the format: the experts use the trellis types TQK6/TQK7
(Gyro-S) and TQ2_T (Gyro-M), the same as the Gyro files. Upstream llama.cpp cannot load them yet; they run in
[Strata](https://github.com/Niko1221/Strata) 0.2.0 or newer (NVIDIA, AMD RX 7000 / RX 9000 / R9700),
[halo-box/strix-llama.cpp](https://github.com/halo-box/strix-llama.cpp) master (AMD Strix Halo; CPU, Vulkan, HIP) and
[agentionai/llama.cpp](https://gitlab.com/agentionai-group/llama.cpp) (CPU, Vulkan, CUDA).

## Usage warning

Abliteration removes most of the model's refusals. Like huihui-ai's original, this model can produce harmful,
offensive or inappropriate content, and it is not suitable for public-facing or unsupervised use. You are
responsible for how you use it and for complying with the law where you are. See huihui-ai's model card for their
full warnings.

## Quick start (Docker)

Our container has [agentionai/llama.cpp](https://gitlab.com/agentionai-group/llama.cpp) ready (Vulkan; CUDA when built
yourself). Strata and strix-llama.cpp: see the [Gyro card](https://huggingface.co/agentionai/Qwen3.8-Flash-Next-Gyro-GGUF).

```bash
hf download agentionai/Qwen3.8-Flash-Next-Gyro-abliterated-Huihui-GGUF Qwen3.8-Flash-Next-Gyro-S-abliterated-TQ1_0.gguf \
  mtp-Qwen3.8-Flash-Next-draft.gguf mmproj-F16.gguf --local-dir ~/models

docker run --rm -it --device /dev/dri --group-add "$(getent group render | cut -d: -f3)" \
  -v ~/models:/models -p 8080:8080 agentionai/agention-llama:server \
  -m /models/Qwen3.8-Flash-Next-Gyro-S-abliterated-TQ1_0.gguf -ngl 999 -fa on --jinja --ngram-on-disk \
  -c 65536 -ctk q8_0 -ctv q8_0 --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.05 \
  --mmproj /models/mmproj-F16.gguf
```

Or with `-hf agentionai/Qwen3.8-Flash-Next-Gyro-abliterated-Huihui-GGUF:Gyro-S` in a native build, which also fetches the
vision projector and, with `--spec-type draft-mtp`, the MTP draft. NVIDIA, vision on/off, speculative decoding and
memory per context length: exactly as on the [Gyro card](https://huggingface.co/agentionai/Qwen3.8-Flash-Next-Gyro-GGUF).
The MTP draft (updated 2026-10-05 to upstream llama.cpp's tensor names, weights unchanged; use agentionai/llama.cpp main
or the container from 2026-10-05 or later) was made from the original model; it still drafts well for the abliterated weights (81% of drafted
tokens accepted on a code prompt in a first check).


## Quality

KL divergence and top-1 agreement, measured against the **original** (not abliterated) Qwen3.8-Flash-Next. These numbers therefore include the
abliteration itself, not only the quantization.

| File | GPU weights | KLD vs original | top-1 vs original | code KLD | code top-1 |
|---|---:|---:|---:|---:|---:|
| **abliterated Gyro-S** | 27.64 GiB | **0.397** | **75.3 %** | **0.111** | **94.3 %** |
| **abliterated Gyro-M** | 34.98 GiB | **0.295** | **78.6 %** | **0.066** | **95.5 %** |

Abliteration costs little here: the abliterated files are within 0.005 KL divergence of Gyro-S (0.401) and
Gyro-M (0.291). That is expected for technical text and code, which barely touch the refusal direction abliteration
removes. It says nothing about refusals themselves; for that, see huihui-ai's card.

## Throughput

Same as the Gyro files, which have identical tensor types and sizes: Gyro-S on one AMD Radeon AI PRO R9700 32 GB,
prefill 1,246 / decode 57.8 tok/s; on AMD Strix Halo (Radeon 8060S), decode 31.7 tok/s; Gyro-M on Strix Halo, decode 26.4
(`llama-bench`, batch 1, no drafting). With strix-llama.cpp master (Vulkan) on Strix Halo: Gyro-S 700 / 36.1,
Gyro-M 738 / 30.1.

## Status

Experimental, like the Gyro files: the format and kernels may change. Runs in agentionai/llama.cpp (Vulkan, CUDA), Strata and strix-llama.cpp; tested on AMD Strix Halo.
The weights come from our own encoder, which we are not publishing at this stage.

## Changelog

- **2026-10-19: more engines.** The files also run in [Strata](https://github.com/Niko1221/Strata) 0.2.0 and in
  [halo-box/strix-llama.cpp](https://github.com/halo-box/strix-llama.cpp) master. Files unchanged.
- **2026-10-13: both files updated.** Same file names, sizes and tensor types; better weights from an improved encode.

## Credits and license

Built and tested on AMD Ryzen AI Max (Strix Halo). Hardware supported by AMD

Base model: Qwen/Qwen3.8-Flash-Next (Qwen community license 1.0, see LICENSE). Abliteration: huihui-ai. Quantization:
AgentionAI. Tensor format: trellis-coded quantization with Hadamard rotation, in the family of QTIP (Tseng et al., 2024). Encoder, trellis types and kernels: AgentionAI.

The Gyro format is open: specification, reference decoder and encoder, and bit-exact tests (Apache 2.0) at [agentionai-group/agention-gyro](https://gitlab.com/agentionai-group/agention-gyro). The released files come from our own production encoder.


### Support AgentionAI

These quants are released freely. If they save you VRAM or make Qwen more useful, you
can buy me a coffee or some GPU time and sponsor continued quantization and benchmarking on
[Buy Me a Coffee](https://buymeacoffee.com/agentionai). AgentionAI is a one-person team and can use your help.





