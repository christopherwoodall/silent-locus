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
- qwen3.8-flash-next
- qwen4exp
- imatrix
- agentionai
---

# Qwen3.8-Flash-Next AP GGUF

[Agention Precision](https://agention.ai/models/qwen3.8-flash-next/) (AP) quants of
[Qwen/Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next).
Mainline llama.cpp compatible — standard quant types only, no fork required.

> **Updated 2026-10-13: `AP-Q5_K_M`.** Same file name, size and tensor types, better weights from an improved encode:
> KL divergence **0.0771** and top-1 agreement **86.95 %** on held-out text, **0.0181** on code:
> level with unsloth's UD-Q4_K_XL on held-out text and ahead on code, in the same VRAM. Download the file again.
>
> **Updated 2026-10-12: `AP-Q4_K_XL`.** KL divergence **0.0886** and top-1 agreement **86.14 %** on held-out text,
> **0.0206** on code. 0 loops in a 45-run loop stress test.

<div align="left">
  <p>
    <em>Quantized for accuracy per gigabyte of VRAM, and measured — every tier below is
    scored against the same reference on a held-out corpus.
    <a href="https://agention.ai/models/qwen3.8-flash-next/">Method and full results</a>.</em>
  </p>
</div>


Each tier varies the quant type per tensor group rather than using one type throughout, to get the most accuracy per gigabyte of VRAM.


## Tiers

| tier | VRAM | n-gram table (host) | download size | eff. bpw | experts (gate/up) | KL div | top-1 agree |
|---|---:|---:|---:|--:|---|---|---|
| `AP-Q5_K_XL` | **76.75** | 35.76 | 112.51 | 5.46 | Q5_K 5.5 | 0.0839 ± 0.0008 | 86.63 ± 0.14 % |
| `AP-Q5_K_M` (updated 2026-10-13) | **76.75** | 26.82 | 103.57 | 5.03 | Q5_K 5.5 | 0.0771 ± 0.0007 | 86.95 ± 0.14 % |
| `AP-Q4_K_XL` (updated 2026-10-12) | **67.38** | 26.82 | 94.20 | 4.57 | Q4_K 4.5 | 0.0886 ± 0.0008 | 86.14 ± 0.14 % |
| `AP-Q4_K_M` | **61.22** | 26.82 | 88.04 | 4.27 | IQ4_XS 4.25 + IQ3_S 3.44 | 0.1243 ± 0.0011 | 84.22 ± 0.15 % |
| `AP-IQ4_XS` | **57.42** | 26.82 | 84.24 | 4.09 | IQ3_S 3.44 | 0.1584 ± 0.0014 | 82.89 ± 0.15 % |
| `AP-IQ3_XXS` | **53.90** | 26.82 | 80.72 | 3.92 | IQ3_XXS 3.06 | 0.1844 ± 0.0016 | 81.85 ± 0.16 % |
| `AP-IQ2_S` | **49.21** | 26.82 | 76.03 | 3.69  | IQ2_S 2.5 | 0.2657 ± 0.0022 | 79.14 ± 0.16 % |


Sizes in GiB. **VRAM** is what the GPU must hold; the 51.2B-parameter n-gram table
(`per_layer_token_embd`) is offloadable to system RAM with
`-ot "per_layer_token_embd=CPU"`, so plan around the VRAM column, not the download.

**Tier names follow the base ftype convention** (as unsloth's do) and do not describe the
experts — the `experts` column does.

### Against unsloth at the same quant level

Same reference, same corpora, same llama.cpp build for every row.

| file | VRAM | download | KL div held-out | top-1 held-out | KL div code | top-1 code |
|---|---:|---:|---:|---:|---:|---:|
| **`AP-Q5_K_M`** | **76.75** | **103.57** | 0.0771 | 86.95 % | 0.0181 | 97.69 % |
| **`AP-Q4_K_XL`** | **67.38** | **94.20** | 0.0886 | 86.14 % | 0.0206 | 97.38 % |
| unsloth `UD-Q4_K_XL` | 76.86 | 103.69 | 0.0778 | 87.21 % | 0.0192 | 97.36 % |

At the same VRAM, `AP-Q5_K_M` matches unsloth's `UD-Q4_K_XL` on held-out KL divergence and is closer to the source on code;
unsloth keeps a slightly higher top-1 on held-out text. `AP-Q4_K_XL` needs 9.5 GiB less VRAM.

## Which one should I use?

- **`AP-Q5_K_M`** — the most accurate file here, if you have 77 GiB of VRAM.
- **`AP-Q4_K_XL`** — the default if 77 GiB doesn't fit: 9.4 GiB less VRAM for a KL divergence of 0.0886 instead of 0.0771.
- **`AP-Q4_K_M`** — 6 GiB less VRAM for 1.9 points of top-1. Take it if 67 GiB doesn't fit.
- **`AP-IQ2_S`** — the floor. Usable at 49 GiB, and 2.8 points ahead of the nearest
  2-bit alternative at comparable size, but the gap to Q4 is large. Take it only if you must.

`AP-Q5_K_M` and `AP-Q5_K_XL` need identical VRAM (76.75 GiB). The updated `AP-Q5_K_M` is the more accurate
of the two; the XL's extra 9 GiB is n-gram-table precision only. Prefer `AP-Q5_K_M`.

## Quality methodology

All figures are KL divergence and top-1 agreement against the same source, measured
on a **held-out corpus** the model has not memorised, `-c 2048`, via
`llama-perplexity --kl-divergence`. This means that numbers can't be directly compared with other measurements.
The code column uses a held-out code corpus the same way.

**Why not wikitext.** This architecture carries a 51.2B-parameter n-gram lookup table, and
wikitext is inside its memorised set. The same file scores **6.9–8.6 points higher top-1 on
wikitext than on held-out text**, and the inflation *grows* as the quant gets smaller — so
wikitext compresses exactly the differences you are choosing between. It is vendor-
independent; other publishers' quants of this model show it too. For reference, `AP-Q4_K_M`
scores 84.22 % held-out and 91.82 % on wikitext.

**Behaviour.** `AP-Q4_K_XL` ran a loop stress test: 45 generations on prompts that provoke runaway reasoning (thinking on, `--min-p 0.05`, 12k-token cap). 0 loops; 44 of 45 finished within the cap.

## Running

```bash
llama-cli -hf agentionai/Qwen3.8-Flash-Next-AP-GGUF:AP-Q4_K_XL \
  -ngl 999 -fa 1 -ot "per_layer_token_embd=CPU"
```

Qwen's recommended settings:

| parameter | thinking mode | instruct (non-thinking) |
|---|---|---|
| temperature | 1.0 | 0.7 |
| top_p | 0.95 | 0.80 |
| top_k | 20 | 20 |
| min_p | 0.0 | 0.0 |
| presence_penalty | 0.0 | 1.5 |
| repetition_penalty | 1.0 | 1.0 |

Our behaviour tests run with `--min-p 0.05`, which we recommend for the smaller tiers.

The `-ot` flag keeps the 51.2B-parameter n-gram table in system RAM.

## Vision

The vision projector is `mmproj-F16.gguf` at the repository root. Download it alongside any
tier to enable image input:

```bash
llama-cli -hf agentionai/Qwen3.8-Flash-Next-AP-GGUF:AP-Q4_K_XL \
  --mmproj-hf agentionai/Qwen3.8-Flash-Next-AP-GGUF:mmproj-F16.gguf \
  -ngl 999 -fa 1 -ot "per_layer_token_embd=CPU"
```

## Changelog

- **2026-10-13: `AP-Q5_K_M` updated.** Same file name, size, VRAM and tensor types; better weights from an improved encode.
  KL divergence 0.0771 (held-out), 0.0181 (code).
  Download the file again; the first release stays available as revision `86a35a81`.
- **2026-10-12: `AP-Q4_K_XL` updated.** Same file name, size, VRAM and speed; better weights from an improved encode.
  KL divergence 0.0886 (held-out), 0.0206 (code). 0 loops in a 45-run loop stress test.
  Download the file again; the first release stays available as revision `0061a60e`.


## Credits and license

Built and tested on AMD Ryzen AI Max (Strix Halo). Hardware supported by AMD


### Support AgentionAI

These quants are released freely. If they save you VRAM or make Qwen more useful, you
can buy me a coffee or some GPU time and sponsor continued quantization and benchmarking on
[Buy Me a Coffee](https://buymeacoffee.com/agentionai). AgentionAI is a one-person team and can use your help.




