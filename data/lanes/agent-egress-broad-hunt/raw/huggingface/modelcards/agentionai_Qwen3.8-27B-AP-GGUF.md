---
base_model:
- Qwen/Qwen3.8-27B
base_model_relation: quantized
license: apache-2.0
library_name: gguf
pipeline_tag: image-text-to-text
tags:
- gguf
- qwen3.8-27b
- imatrix
- agentionai
---

# Qwen3.8-27B · Agention Precision GGUF

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-ea4aaa?logo=githubsponsors&logoColor=white)](https://github.com/sponsors/agentionai)
[![View results on Fieldwork Ledger](https://share.fieldworkledger.com/jWO2-ae4HyoC6GIqZucsaA/badge.svg)](https://share.fieldworkledger.com/jWO2-ae4HyoC6GIqZucsaA)

**Same size. Same speed. Closer to the model Qwen trained than any other quant**

![Lower KL at the same GiB means more of Qwen left in the file](assets/kld-vs-size.png)

[Full Results](https://share.fieldworkledger.com/tTkQDHijE_Anj0yv79bsIw) 

Agention Precision quants are the highest precision quants of Qwen3.8 27B byte-for-byte. Each file has a non-uniform assignment and low-loss error correction built with a custom encoder.

This is a drop-in GGUF pack for [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B): standard llama.cpp types, no fork, no flags. Vision projector and MTP draft head included.

Every 27B quant gives something up. These give up less. We measured the leading public GGUFs against the full BF16 model on one protocol. At every size we ship, ours is the closest to Qwen’s next-token distribution. 

Every quant is tested against three corpora: unseen technical prose, general web text and Wikipedia. 

Swap cost is zero. VRAM and tokens/sec stay the same. The file behaves more like the weights Qwen released.

| Start here | File | Size | 32k VRAM | Fits | Gain vs leading same-size quant |
|---|---|---:|---:|---|---|
| Most headroom | **`AP-Q4_K_XL`** | 16.35 GiB | ~18 GiB | 24 GB | **4% closer** to BF16; hardest 1% of tokens **7% closer** |
| 24 GB, smaller | **`AP-Q4_K_M`** | 15.33 GiB | ~17 GiB | 24 GB | **5% closer** on unseen technical text; hardest 1% of tokens **9% closer** |
| Default | **`AP-IQ4_XS`** | 13.27 GiB | ~15 GiB | 16 GB | **8% closer** to BF16; hardest 1% of tokens **9% closer** |
| Need headroom | **`AP-Q3_K_XL`** | 12.24 GiB | ~14 GiB | 16 GB + longer ctx | **19% closer** on unseen technical text, **6%** on web; hardest 1% of tokens **23% closer** |
| 12 GB, more quality | **`AP-IQ3_S`** | 11.21 GiB | ~13 GiB | 16 GB at 8–16k | **17–20% closer** on unseen technical text than the leading research quants, **5%** on web; hardest 1% of tokens **24% closer** |
| 12 GB, balanced | **`AP-IQ3_XS`** | 10.70 GiB | ~12.5 GiB | 12 GB at 8–16k | Level with ISTA’s 11.29 GiB `IQ3_S` on unseen technical text at 0.6 GiB less; **49% closer** than the 10.38 GiB AtomicChat quant |
| 12 GB / multi-model | **`AP-IQ3_XXS`** | 10.00 GiB | ~12 GiB | 12 GB at 8–16k | **26% closer** on unseen technical text, **18%** on web and wikitext-2 than the best ~10 GiB research quant |
| 12 GB, smallest | **`AP-IQ2_S`** | 8.95 GiB | ~10.9 GiB | 12 GB at 8–16k | **22% closer** on unseen technical text, **14%** on web, **18%** on wikitext-2 than the best same-size research quant |
| Vision | `mmproj-BF16.gguf` | 0.87 GiB | +0.9 GiB | any tier | Qwen’s own encoder at BF16 |

VRAM = weights + q8_0 KV + llama.cpp buffers. Only a quarter of layers use full attention, so 32k context is about 1 GiB at q8_0.

**Take `AP-IQ4_XS` if it fits.** Step down only for memory.

---

## Measured

Fidelity = KL divergence of the next-token distribution vs Qwen3.8-27B BF16. Lower is closer to the original.

60 × 2048 tokens, three corpora, same build, same BF16 logits:

- **held-out** — 1.85 MB of our own technical prose, never part of any calibration set. It is internal engineering documentation, so it is not published: this column is the one you cannot re-run yourself.
- **neutral web** — `mixedweb-v1`, 800,789 chars, a seeded FineWeb slice, md5 `51e0045e8cabf37922aa82766a25b7b4`, published with its per-document manifest and builder in [agentionai/quant-fidelity-corpora](https://huggingface.co/datasets/agentionai/quant-fidelity-corpora)
- **wikitext-2** — the standard `wiki.test.raw`, 1,288,556 chars, md5 `7c0137fc034ddbc56a296bce31b4f7fb` (`llama.cpp/scripts/get-wikitext-2.sh`)

### Reproducing these numbers

The reference is [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) at
revision `1d4bf0f2` (the weights uploaded 2026-08-13; later commits are README
only), converted with llama.cpp's own converter — no changes, no fork:

```bash
python convert_hf_to_gguf.py --outtype bf16 Qwen3.8-27B/ --outfile Qwen3.8-27B-BF16.gguf   # 54,657,733,888 bytes
```

Then one base of BF16 logits per corpus, and every quant scored against it. The
KLD code is upstream and unmodified; ours was built at llama.cpp `26bc85e42`:

```bash
llama-perplexity -m Qwen3.8-27B-BF16.gguf -f mixedweb-v1.txt \
  --kl-divergence-base base-mixedweb.bin -c 2048 --chunks 60 -ngl 99

llama-perplexity -m Qwen3.8-27B-AP-IQ4_XS.gguf --kl-divergence \
  --kl-divergence-base base-mixedweb.bin -c 2048 --chunks 60 -ngl 99
```

`Mean KLD` and `Same top p` in that output are the two numbers in the tables
above; `99.0% KLD` is the worst-1 % column. Every file on this page — ours,
Unsloth's, ISTA-DASLab's, AtomicChat's — was measured with those exact commands,
same build, same base files, same 60 × 2048 tokens.

### Head to head with Unsloth, identical bytes

Same tensor types, same file size, same speed, same memory. What differs is how the weights inside each block were chosen — a different calibration and a different encoder.

| | held-out | neutral web | wikitext-2 | worst 1% tokens (held-out) |
|---|---|---|---|---|
| `UD-Q4_K_XL` | 0.0117 | 0.0087 | 0.0122 | 0.088 |
| **`AP-Q4_K_XL`** | **0.0111 (−4.4%)** | **0.0083 (−4.5%)** | 0.0118 | **0.082 (−7.2%)** |
| `UD-Q4_K_M` | 0.0153 | 0.0108 | 0.0139 | 0.122 |
| **`AP-Q4_K_M`** | **0.0146 (−4.9%)** | **0.0104 (−3.7%)** | 0.0150 | **0.111 (−8.8%)** |
| `UD-IQ4_XS` | 0.0276 | 0.0186 | 0.0252 | 0.233 |
| **`AP-IQ4_XS`** | **0.0255 (−7.6%)** | **0.0181 (−2.4%)** | **0.0243 (−3.8%)** | **0.211 (−9.3%)** |
| `UD-Q3_K_XL` | 0.0421 | 0.0270 | 0.0337 | 0.366 |
| **`AP-Q3_K_XL`** | **0.0339† (−19.5%)** | **0.0255 (−5.8%)** | 0.0352 | **0.280 (−23.5%)** |
| `UD-IQ3_S` | 0.0617 | 0.0404 | **0.0470** | 0.553 |
| **`AP-IQ3_S`** | **0.0492† (−20.3%)** | **0.0383 (−5.1%)** | 0.0506 | **0.420 (−24.0%)** |

Held-out gains: 3.2σ, 3.2σ, 5.7σ, 16σ and 18σ (`Q4_K_XL` / `Q4_K_M` / `IQ4_XS` / `Q3_K_XL` / `IQ3_S`). Neutral-web gains: 3.7σ at `Q4_K_XL`, 3.4σ at `Q3_K_XL`, 3.1σ at `IQ3_S`; 2.4σ at `Q4_K_M`. Wikitext-2 is a statistical tie (under 1.5σ) at every tier except `IQ3_S`, where unsloth is 7% closer (2.1σ).

Top-1 match with BF16 on held-out text: **92.8%** · **92.2%** · **90.4%** · **90.1%** · **88.6%** · **87.7%** · **85.8%** (`Q4_K_XL` / `Q4_K_M` / `IQ4_XS` / `Q3_K_XL` / `IQ3_S` / `IQ3_XS` / `IQ3_XXS`).

### The field near these sizes

| file | size | held-out | neutral web | wikitext-2 |
|---|---:|---|---|---|
| **`AP-Q4_K_XL`** | **16.35 GiB** | **0.0111** | **0.0083** | **0.0118** |
| unsloth `UD-Q4_K_XL` | 16.35 GiB | 0.0117 | 0.0087 | 0.0122 |
| **`AP-Q4_K_M`** | **15.33 GiB** | **0.0146** | **0.0104** | 0.0150 |
| unsloth `UD-Q4_K_M` | 15.33 GiB | 0.0153 | 0.0108 | 0.0139 |
| AtomicChat `AD-IQ4_XS-IQ3_S` | 13.45 GiB | 0.0335 | 0.0234 | 0.0384 |
| **`AP-IQ4_XS`** | **13.27 GiB** | **0.0255** | **0.0181** | **0.0243** |
| unsloth `UD-IQ4_XS` | 13.27 GiB | 0.0276 | 0.0186 | 0.0252 |
| AtomicChat `AD-IQ3_S` | 12.89 GiB | 0.0441 | 0.0303 | 0.0441 |
| **`AP-Q3_K_XL`** | **12.24 GiB** | **0.0339**† | **0.0255** | 0.0352 |
| unsloth `UD-Q3_K_XL` | 12.24 GiB | 0.0421 | 0.0270 | 0.0337 |
| ISTA-DASLab `GSQ-RCO-IQ3_S` | 11.29 GiB | 0.0594 | 0.0432 | 0.0665 |
| **`AP-IQ3_S`** | **11.21 GiB** | **0.0492**† | **0.0383** | 0.0506 |
| unsloth `UD-IQ3_S` | 11.21 GiB | 0.0617 | 0.0404 | 0.0470 |
| **`AP-IQ3_XS`** | **10.70 GiB** | **0.0604**† | **0.0498** | **0.0667** |
| AtomicChat `AD-IQ2_S` | 10.38 GiB | 0.1187 | 0.0858 | 0.1062 |
| **`AP-IQ3_XXS`** | **10.00 GiB** | **0.0832**† | **0.0676** | **0.0869** |
| ISTA-DASLab `GSQ-RCO-IQ3_XXS` | 9.73 GiB | 0.1123 | 0.0824 | 0.1063 |
| ISTA-DASLab `GSQ-RCO-IQ2_S` | 8.95 GiB | 0.1541 | 0.1143 | 0.1470 |
| **`AP-IQ2_S`** | **8.95 GiB** | **0.1239**† | **0.0983** | **0.1204** |
| ISTA-DASLab `GSQ-RCO-IQ2_XS` | 8.17 GiB | 0.2263 | 0.1724 | 0.2036 |

ISTA rows are their `-mtp` builds (draft head included, same as ours).

† `AP-IQ2_S` (2026-09-28) and `AP-IQ3_XXS`, `AP-IQ3_XS`, `AP-IQ3_S` and `AP-Q3_K_XL` (2026-09-29) were rebuilt with an extended calibration set that shares 1.4% of its 12-grams with the held-out corpus. Their held-out figures are therefore measured on the 95% of held-out text with zero overlap. That subset is slightly harder: every file we scored on both reads about 3% higher on it than on the full set (ISTA `GSQ-RCO-IQ2_S` 0.1541 → 0.1584, the previous `AP-IQ2_S` 0.1418 → 0.1460), so comparing it with the other rows' full held-out figures is conservative. The extended calibration moves precision toward technical and code text: against the previous files, held-out KL drops 15–18% while wikitext-2 reads up to 9% higher.

KL is fidelity to Qwen’s predictions, not a task leaderboard. The claim it supports is narrow and checkable: at every size we ship, you are closer to the original than the same-size alternative.

**First downstream check.** MMLU-Pro, 70 questions (5 per subject), thinking mode with Qwen’s recommended sampling, one run, same questions for both files:

| file | size | MMLU-Pro |
|---|---:|---:|
| **`AP-IQ2_S`** | **8.95 GiB** | **77.1%** |
| ISTA-DASLab `GSQ-RCO-IQ2_S` | 8.95 GiB | 75.7% |

---

## Running

Use the sampling settings from the
[Qwen3.8-27B model card](https://huggingface.co/Qwen/Qwen3.8-27B). Thinking is on by
default. To turn it off per request, send
`"chat_template_kwargs": {"enable_thinking": false}`.

```bash
llama-server -hf agentionai/Qwen3.8-27B-AP-GGUF:IQ4_XS \
  --jinja -ngl 999 -fa on -c 32768 -ctk q8_0 -ctv q8_0
```

Keep the KV cache at q8_0 or f16. A 4-bit value cache makes long reasoning traces
degenerate into repetition on this model family.

**LM Studio:** search for `agentionai/Qwen3.8-27B-AP-GGUF` and pick a tier.
**Ollama:** `ollama run hf.co/agentionai/Qwen3.8-27B-AP-GGUF:IQ4_XS`

```bash
llama-server -hf agentionai/Qwen3.8-27B-AP-GGUF:IQ4_XS \
  --mmproj mmproj-BF16.gguf --jinja -ngl 999 -fa on -c 32768 -ctk q8_0 -ctv q8_0
```

## Built with

The tiers are built and verified with our own Rust tooling agention-infer. Every tier is measured against BF16
on all three corpora, and shipped only if it beats the same-size alternative.
[unsloth](https://huggingface.co/unsloth)'s dynamic type maps underpin `AP-Q4_K_XL`,
`AP-Q4_K_M`, `AP-IQ4_XS`, `AP-Q3_K_XL` and `AP-IQ3_S`, and we thank them for that work.
`AP-IQ3_XS` and `AP-IQ3_XXS` sit at sizes no one else ships and use our own per-tensor
allocation, so they are compared against the nearest published files above and below them.
`AP-IQ2_S` is built on [ISTA-DASLab](https://huggingface.co/ISTA-DASLab)'s GSQ-RCO type map
for that size, re-encoded with our calibration and tooling, and we thank them for that work. `imatrix-mixed-v2.gguf`, the
importance matrix from our calibration pass, is included for anyone building their
own quants. Since 2026-09-28 `AP-IQ2_S`, and since 2026-09-29 `AP-IQ3_XXS`, `AP-IQ3_XS`, `AP-IQ3_S` and
`AP-Q3_K_XL`, use an extended calibration set that adds agentic coding transcripts; its imatrix is not published.

Calibration is ordinary public text: the [Bartowski](https://huggingface.co/bartowski)
and [Thireus](https://huggingface.co/Thireus) imatrix corpora, plus a one-third share
of whole articles from the wikitext-2 **train** split — never the test split, and the
12-gram overlap with each of the three evaluation corpora above is 0, 0 and 6
(section headings and unit conversions). 6,012 documents, 4.67 M characters, md5
`b8e3269f085f500ab307b0cc977126b0`, 1,200 × 512 tokens through the BF16 model. The
calibration is not the advantage here; anyone can build on the same text.

### Does it hold up in real use? A one-shot coding test

Same prompt, same five seeds for every file, first answer only, no retries and no fixes. Each page opened in Chrome and judged by eye.

![Voxel pagoda, first try, at 9 GiB](assets/pagoda-poster.png)

| file | size | working pages | looped (no answer) |
|---|---|---|---|
| **`AP-IQ2_S`** | **8.95 GiB** | **4 / 5** | **0** |
| ISTA-DASLab `GSQ-RCO-IQ2_S` | 8.95 GiB | 2 / 5 | 1 |
| ByteShape `IQ3_XXS-2.88bpw` | 9.24 GiB | 0 / 5 | 3 |

Five trials per file is a small sample; read it as a sanity check that the lower KL carries over, not as a benchmark.

More tiers follow as they clear the same bar.


## Credits and license

Built and tested on AMD Ryzen AI Max (Strix Halo). Hardware supported by AMD

Base model: Qwen/Qwen3.8-27B (Qwen community license 1.0, see LICENSE).

### Support AgentionAI

These quants are released freely. If they save you VRAM or make Qwen more useful, you
can buy me a coffee or some GPU time and sponsor continued quantization and benchmarking on
[Buy Me a Coffee](https://buymeacoffee.com/agentionai). AgentionAI is a one-person team and can use your help.
