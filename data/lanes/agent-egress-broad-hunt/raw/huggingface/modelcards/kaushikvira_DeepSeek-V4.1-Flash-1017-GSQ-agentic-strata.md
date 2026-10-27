---
library_name: strata
pipeline_tag: text-generation
inference: true
license: mit
base_model:
  - deepseek-ai/DeepSeek-V4.1-Flash-1017
base_model_relation: quantized
tags:
  - deepseek
  - deepseek-v4.1
  - moe
  - 763b
  - gsq
  - mixed-precision
  - ternary
  - q3_k
  - q2_0
  - strata
  - xolotl
  - agentic
  - coding
  - workload-calibrated
  - hybrid-vram-ram
  - engram
  - cuda
  - gguf
  - text-generation
  - llm
  - quantized
  - blackwell
  - rtx-pro-5000
  - single-gpu
  - speculative-decoding
  - dspark
  - long-context
  - 512k
  - fp4
  - tool-calling
  - reasoning
---

# strata · DeepSeek-V4.1-Flash-1017 GSQ (mixed-precision, agentic-calibrated)

A **workload-calibrated mixed-precision** quantization of
[deepseek-ai/DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017)
(763.2B-parameter MoE — the largest DeepSeek V4.1 Flash variant), built for the
**strata** engine (Xolotl fork). Every routed-expert projection is assigned its
own precision tier (Q3_K / Q2_0 / ternary) from activation calibration on an
agentic + coding corpus, so the artifact lands at a fixed **153 GiB** budget
while keeping the sensitive experts at higher precision and pushing the
least-sensitive ones to ternary (which strata runs on CPU).

It is **not** a standard llama.cpp GGUF: the per-expert tier map, the engram
memory layers, the expert `rank.bin`, and the DSpark speculative sidecar are all
strata-specific. See [Engines](#engines-it-runs-on) below.

## What this model is for

- **Agentic / coding workloads** — the calibration corpus is weighted toward
  code, SWE-style tool trajectories, and tool-schema usage, so the tier map
  protects the expert paths those tasks actually exercise.
- **Long context** — served with a 512K-token context and FP4 KV cache.
- **Hybrid VRAM+RAM serving** — hot experts live in GPU VRAM, cold experts in a
  pinned RAM arena; the least-sensitive ternary experts run on CPU. A single
  72 GB GPU serves the whole model (cold experts offload to RAM).
- **Size = speed** — decode is memory-bandwidth-bound, so a smaller artifact
  moves fewer bytes/token. 153 GiB is the author's budget-neutral all-Q2_0
  design point for this model.

## Credits & provenance (full chain)

**All credit for the model itself goes to the authors below** — this artifact is
a quantization of their work, with no fine-tuning of our own:

| Role | Model / component | Author | Ref |
|---|---|---|---|
| **Source weights** | [deepseek-ai/DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017) | **DeepSeek-AI** | 763.2B MoE, hybrid FP8-dense / NVFP4-expert |
| **Quantization method** | GSQ (Gumbel-Softmax Quantization) + per-expert mixed-precision tier allocation | **antirez** (method + pipeline) | see [antirez/ds4](https://github.com/antirez/ds4) |
| **Engine** | strata — `ds41_generate` | [Indras-Mirror/Xolotl](https://github.com/Indras-Mirror/Xolotl) | `tools/v41/serve/serve_ds41.py` |
| **Calibration** | workload-calibrated activation stats (agentic + coding mix) | this build | technique below; no proprietary data |

## Our approach

The whole pipeline is open source in
[Xolotl/tools/v41](https://github.com/Indras-Mirror/Xolotl/tree/main/tools/v41).
We ran it end-to-end on the 1017 checkpoint — no fine-tuning, no abliteration,
just a workload-calibrated mixed-precision quantization:

1. **Fetch** — the 1017 base (763.2B, hybrid FP8-dense / NVFP4-expert) via the
   HF CLI.
2. **Corpus** — a workload-calibrated calibration set: **32 sequences × 8,192
   tokens**, weighted toward agentic + coding (agentic_long 10 · code 10 · agent
   5 · reasoning 3 · web 2 · chat 1 · multi 1). **Datasets:**
   [antirez/ds4](https://github.com/antirez/ds4) imatrix prompts + public
   SWE-agent trajectories (Nebius **SWE-rebench**, NVIDIA **SWE-Hero**,
   **SWE-smith**), re-rendered in the serving tool-call format. *No proprietary
   or personal data is used or shipped — only the technique and the resulting
   tier map.*
3. **Calibration** — a layer-streaming teacher forward (DeepSeek's own
   `model.py`, one layer at a time straight from the HF shards) collects
   per-expert-projection activation stats (41 files: L0–L39 + head).
4. **Allocation** — a budget-constrained tier map: each of the ~30,720
   expert-projections gets Q3_K / Q2_0 / ternary so the total lands exactly on
   **153 GiB** (budget-neutral vs all-Q2_0). Guard rails: ternary capped at
   0.5/layer, gate+up and down allocated separately (`per_proj`), edge layers
   weighted 2×, experts with <8 held-out tokens floored at Q2_0.
5. **Quantize** — GSQ per-expert quantization to the assigned tiers → the main
   GGUF. Ternary experts are stored as `scale × mask ⊙ sign` and run on CPU.
6. **Sidecar** — the MTP+vision DSpark stack requantized to Q2_K (5.3 GiB).
7. **Rank** — expert hotness ranking (`rank.bin`, 15,360 pairs) to seed the
   VRAM/RAM expert cache.
8. **Engram** — extract the two Engram n-gram memory layers (L1, L14) to disk.

**Resulting tier map.** By expert-projection *count*: Q3_K 28.4% · Q2_0 38.4% ·
ternary 33.2%. By *bytes* (what actually matters for size/speed):

| Tier | bpw | Share of expert bytes | ~Size |
|---|---:|---:|---:|
| Q3_K | 3.44 | **41%** | ~63 GiB |
| Q2_0 | 2.25 | **38%** | ~57 GiB |
| ternary | 1.69 | **21%** | ~32 GiB |

Hot experts take the precision (Q3_K is 28% of experts but 41% of the bytes); the
cold tail is crushed to ternary (33% of experts, only 21% of the bytes). At the
same 153 GiB budget the mixed map cuts the proxy quantization error from
**2.169** (all-Q2_0) to **1.680** (−23%).

**Why 153 GiB (size is a speed lever, not just storage):** decode is
memory-bandwidth-bound — each token fetches its ~6 active experts/layer, so fewer
expert bytes = less traffic = faster tok/s. The tier map is speed-smart by
construction: Q3_K goes to hot experts (VRAM, where size is free), ternary to the
cold tail (RAM/CPU, where small = fast). 153 GiB is the author's budget-neutral
all-Q2_0 design point — the smallest size that keeps the sensitive experts at
Q3_K. Smaller challengers (134 / 126 GiB) are one `alloc` away from the same
calibration, at a quality cost.

**What makes it different:** the tier map is driven by *activation* calibration
on an agentic/coding workload, not a uniform or weight-only scheme — so the bits
land where those workloads actually touch the experts. The sensitive projections
stay Q3_K in VRAM; the least-sensitive go ternary and run on CPU.

## Artifact

| File | Size | Role | SHA-256 |
|---|---|---|---|
| `V41-GSQ-1017.gguf.part-00` | 90 GiB | main model, chunk 1/2 | `(see SHA256SUMS)` |
| `V41-GSQ-1017.gguf.part-01` | 73 GiB | main model, chunk 2/2 | `(see SHA256SUMS)` |
| `V41-MTP-Vision-1017.Q2_K.gguf` | 5.3 GiB | DSpark MTP+vision sidecar (Q2_K) | `46eb03c6bd69b8ea313ed9c3b2fd618721c044661613d9ff0845a4911454d7ec` |
| `rank.bin` | 120 KB | expert hotness ranking (15,360 pairs) that seeds the VRAM/RAM cache — census: the first 8 GiB covers **29.9%** of routed tokens (hot→cold curve) | `e77ca111578ea18321551f9eda419d36d7456a30e4912a1fc6895f7be652c908` |
| `engram-layers.1/engram-L1.safetensors` | 95 GiB | engram memory, layer 1 | `5cc4ca3be6302a50597684d234dd47ae7ff7b3a5b42d386515b58f4ecd17662b` |
| `engram-layers.14/engram-L14.safetensors` | 95 GiB | engram memory, layer 14 | `35c6bb1c15139a691d530c4ea469d1983031074c1a84b4e7f7668fef2015b68b` |
| `tokenizer/` | 6 MiB | vocab / merges / token_type / chat_template | — |
| `V41-GSQ-1017.gguf.experts.json` | 1.2 MiB | the per-expert tier map (metadata) | `9f72bdbf14130a3735e7b5d849f359908868f857ab94d5473ce2eb23011cf7b2` |

**Recombine the main model** (the 163 GiB GGUF is split into two chunks to fit
HF's per-file limit):

```bash
cat V41-GSQ-1017.gguf.part-00 V41-GSQ-1017.gguf.part-01 > V41-GSQ-1017.gguf
# verify: sha256sum V41-GSQ-1017.gguf  ->  014ef21a1e9ae9d1a1cb7639cf3ab78b517b9e898e96af0b25ee352e55f3216b
```

Full manifest: `SHA256SUMS`.

## Serving (strata, single 72 GB GPU)

```bash
strata ds41_generate \
  -m /models/V41-GSQ-1017.gguf --backend cuda \
  --experts gpu --engram /models --rank /models/rank.bin \
  --ctx 524288 --kv-fp4 --arena-gib 108 --vram-margin 2 \
  --prompt-batch 12288 --arena-adapt --route-bias 0.5 \
  # + DSpark sidecar: V41-MTP-Vision-1017.Q2_K.gguf (depth 4, conf 0.6)
```

The engine auto-sizes the VRAM slot from *free* VRAM (`--vram-margin`), so it
coexists with other tenants on the same GPU. Sampling: `temperature 1, top_p
0.95`.

## Performance (measured)

**GPU:** NVIDIA RTX PRO 5000 72 GB (Blackwell, 270 W cap) · driver 615.71.09.

| Condition | Decode | Notes |
|---|---|---|
| Coexisting with other tenants on the same GPU | **~34 tok/s** | hot experts in VRAM, cold + ternary offloaded to RAM/CPU |

Decode is **memory-bandwidth-bound**: the tier map + arena size set the ceiling.
With the GPU dedicated (no co-tenants) the VRAM slot grows and more hot experts
stay on-device, so t/s rises — post your dedicated-GPU number in Discussions.
TTFT on a cold 512K-context prefill is dominated by the RAM→GPU expert fetches;
short-context agentic turns (the target workload) are much faster.

## Benchmarks

**Measured so far** (served through strata, thinking on, on the PRO 5000):

| Check | Result |
|---|---|
| **HumanEval** (21 problems) | **21/21 correct** |
| **Streaming tool calls** (10) | **10/10 valid** |

These confirm the model loads cleanly and generates correct, coherent code and
tool calls — a strong sanity signal, though 21 problems is too small a sample to
rank quality.

**Full evaluation is coming.** The real quality numbers — a paired
**LiveCodeBench + AIME25 + GPQA** run against the 152 GiB DeepSeek-V4.1-Flash
reference — are in progress and will be added here. **The gate needs more time:**
it's a long paired run (each side is a multi-hour eval, and the final stage uses
expanded task pools with a clustered bootstrap), so expect the numbers in a few
days, not minutes. Served by strata, greedy where noted.

**How promotion is decided (the gate):** a 3-stage paired comparison against the
reference — (1) *smoke* (loader/collapse: 21 HumanEval + 10 tool calls), (2)
*screen* (LiveCodeBench 150 + AIME25 30 + GPQA 50), (3) *final* (expanded pools,
task-clustered bootstrap). The 1017 is promoted only on **−2 pp non-inferiority**
(lower 95% CI bound of candidate − reference ≥ −2 pp) **and** equal/better decode
tok/s — measured, not assumed.

## Engines it runs on

- **strata** ([Indras-Mirror/Xolotl](https://github.com/Indras-Mirror/Xolotl)) — the only
  supported engine. The per-expert tier map, engram memory, `rank.bin`, and DSpark
  sidecar are strata features; the GGUF is **not** a standard llama.cpp GGUF.
- **Not** runnable on vanilla llama.cpp, Ollama, vLLM, or SGLang without a
  strata-compatible loader. If you need one of those, that's a conversion project
  (see Community below).

## Measurement conditions

- Single **RTX PRO 5000 72 GB** (driver 615.71.09, 270 W cap).
- strata engine (`ds41_generate`), CUDA backend, FP4 KV cache.
- Decode is memory-bandwidth-bound; tier map and arena size set the t/s ceiling.

## Notes

- This is a **quantization only** — no fine-tuning, no abliteration. Refusal
  behavior is inherited from the base DeepSeek-V4.1-Flash-1017.
- The 153 GiB budget is the author's budget-neutral design point; smaller
  challengers (134 / 126 GiB) can be produced from the same calibration if you
  want a faster (smaller) decode at a quality cost.

---

## Acceptable Use Policy & Legal Notice

**By downloading, possessing, or using this artifact you agree to the terms below.**

### Permitted use
Research, personal/local experimentation, red-teaming, safety research, and
evaluating alignment and quantization techniques — subject to all applicable
laws and regulations.

### Prohibited use
You must **not** use this model, alone or in any pipeline, to:
- carry out, plan, or facilitate any activity that is illegal in your jurisdiction;
- produce content that harms, endangers, defrauds, harasses, or exploits others;
- provide medical, legal, or financial advice presented as professionally qualified;
- violate the rights of any person or entity, including intellectual property and privacy rights.

### Your responsibility
Model outputs are a **capability, not a judgment** — never guaranteed
trustworthy, factual, or legal. **You are solely and fully responsible** for
every prompt you send, every output you generate, and every use you make of
them. The publisher (`kaushikvira`) does not monitor, endorse, or take part in
downstream use.

### No warranty / limitation of liability
The artifact is provided **"AS IS", WITHOUT WARRANTY OF ANY KIND**, express or
implied. **To the maximum extent permitted by applicable law, the publisher
shall not be liable for any claim, damages, or other liability arising from this
artifact or its use.**

## Community — open a discussion

- **Bench your hardware** — if you serve this on a different GPU/RAM config,
  post your t/s and quality numbers in the **Discussions** tab; we collect them
  here.
- **Need a smaller / different build?** I have the GPU and RAM to run
  quantizations — open a discussion with your target (budget GiB, ternary
  fraction, engine) and I'll build it. Same for a conversion to a standard
  llama.cpp / vLLM layout if that's what you need.
- **Found a bug or a better tier map?** Discussions are the place — the
  calibration + alloc pipeline is reproducible from this card.

## License

**MIT** — both the base
[DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017)
weights (MIT) and this quantization artifact are MIT-licensed.
**All model credit to DeepSeek-AI**; GSQ method and pipeline to
**antirez**; engine to [Indras-Mirror/Xolotl](https://github.com/Indras-Mirror/Xolotl).
