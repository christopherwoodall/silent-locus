---
base_model:
- Qwen/Qwen3.8-27B
base_model_relation: finetune
license: apache-2.0
license_link: LICENSE
library_name: gguf
pipeline_tag: image-text-to-text
tags:
  - token-efficient
  - efficient-thinking
  - qwen3.8
  - qwen3.8-27b
  - terse
  - agentionai
---

<a href="https://www.agention.ai/"><img src="signal27b.png" alt="AgentionAI — Signal 3.8 27B" width="100%"></a>

# Signal 3.8 27B

This is Qwen3.8-27B that gets to the answer faster.

> [!IMPORTANT]
> **Recommended settings**
> Temperature 0.6, top-p 0.95, top-k 20, min-p 0.05, **presence_penalty 1.0**, KV cache q8_0 or f16.
> Keep min-p and presence_penalty on: without them, long generations can run into repetition on some
> draws (a 4-bit value cache makes that deterministic). If you enable the MTP draft head on recent
> mainline llama.cpp, also pass **`--no-spec-draft-backend-sampling`** — the default backend draft
> sampling does not apply your sampler to accepted draft tokens, which can let repetition run away
> regardless of the settings above.

> [!WARNING]
> The tiers in this repository were rebuilt on 2026-09-13. The first release's tiers could, rarely,
> repeat an answer line when sampling without the draft head; the rebuilt tiers showed no loop or cap
> in 55 traces under the same conditions. If you downloaded before that date, re-download.

AgentionAI Signal is a minimally invasive fine-tune of Qwen3.8-27B designed for lower generation latency and better token efficiency. On our held-out general-prompt evaluation, Signal produces **25% fewer answer tokens** and uses **41% fewer thinking tokens**, while matching or improving the measured answer quality of the base model.

The result is faster end-to-end generation. On 40 chat prompts with the draft head on, same hardware and sampling, Signal finished the batch in **19% less total wall time** and **28% less median wall time** than the untouched Qwen3.8-27B, from fewer answer tokens and higher draft acceptance.

Signal gets there by being more direct rather than by truncating answers. It removes unnecessary preambles, excessive formatting, sign-offs, and explanatory narration while preserving the substance of the response. In thinking mode, it keeps the useful reasoning steps while spending fewer tokens describing the process.

Signal is trained by self-distillation: on Qwen3.8-27B's own answers, generated under an instruction to be direct that the released model no longer needs. No external data and no other model's outputs went into it, which is why it keeps the base model's knowledge and voice intact.

It is a drop-in GGUF replacement for llama.cpp setups that already run Qwen3.8-27B.

## What changes, measured

We evaluated Signal against the untouched Qwen3.8-27B, both at Q8_0 in llama.cpp, using the same server, sampling settings and prompts: 60 general and 40 coding prompts with thinking off, 30 and 20 of them with thinking on, plus GSM8K. All prompts were held out from tuning. The numbers are for the tiers rebuilt on 2026-09-13.

| | base Q8_0 | Signal | change |
|---|---|---|---|
| general answers, median tokens | 243 | 183 | **-25%** |
| answers opening with a preamble ("Sure!", "Great question") | 13% | 3% | **-77%** |
| answers with markdown headers | 47% | 37% | -21% |
| answers with bold | 85% | 75% | -12% |
| coding answers, median tokens | 159 | 153 | -4% |
| coding answers, p90 tokens | 1026 | 963 | -6% |

Thinking mode, same prompts with reasoning on:

| | base Q8_0 | Signal | change |
|---|---|---|---|
| reasoning tokens, general prompts, median | 153 | 91 | **-41%** |
| reasoning tokens, coding prompts, median | 225 | 158 | -30% |
| reasoning tokens, GSM8K, median | 119 | 90 | -24% |

Quality, exact match on GSM8K:

| | base Q8_0 | Signal |
|---|---|---|
| thinking off, 60 problems | 98.3% | **100%** |
| thinking on, 40 problems | 92.5% | **95.0%** |

Signal was also run on 100 problems in each mode: 98.0% with thinking off, 96.0% with thinking on. The table uses the problems the base model was run on.

Shorter is not cheaper: no answer in the 150-prompt style set was cut off early (0 answers
ending on a header or a colon, 0 unclosed code blocks). With reasoning on at a 6,000-token budget,
6 of Signal's 250 traces ran to the budget against 3 of the base model's 90, the same rate. On a
separate loop check of 55 thinking-mode traces (math, GSM8K, coding and general prompts, Q5_K_M on
mainline llama.cpp with and without the draft head, q8_0 KV cache) no trace looped or hit the cap.

## Faster with speculative decoding

Qwen3.8-27B carries a built-in multi-token-prediction draft head. Signal's answers are more predictable, so the drafter agrees with the model more often:

Draft acceptance and decode speed with `--spec-type draft-mtp`, both models Q8_0 on the same
machine (Strix Halo, Vulkan), 200-token greedy runs for the fixed-draft rows:

| prompt / draft length | base acceptance | Signal acceptance | decode speed vs base |
|---|---:|---:|---:|
| prose, draft 3 | 39% | 45% | **+9%** |
| prose, draft 4 | 35% | 41% | **+14%** |
| structured output (JSON), draft 3 | 72% | 94% | **+20%** |
| structured output (JSON), draft 4 | 66% | 87% | **+24%** |
| chat prompts, sampled at 0.7, adaptive draft ≤4 (40 prompts) | 57% | 56% | — |

Combined with the shorter answers, the measured batch above finishes in about **four fifths of the total wall
time** (and under three quarters of the median) of the base model on the same hardware, with the draft head on.

## Why shorter is not worse

Chain-of-thought length is not mostly a function of problem difficulty. A recent study of
reasoning models (Lotfi, Kirichenko, Li and Liu, *Quantized Reasoning Models Think They Need to
Think Longer, but They Do Not*, [arXiv:2606.00206](https://arxiv.org/abs/2606.00206)) finds that
a small set of hesitation and branching tokens ("Wait", "But", "Alternatively", "maybe") drives
most of the excess: they are sampled at the positions where the model is least certain, each one
opens a new line of reasoning, and in up to half of the failures the model had already reached
the right answer before branching away from it. Suppressing those fifty tokens at decode time cut
reasoning length by 12 to 23 percent across five models without hurting accuracy.

Signal reaches the same place from the opposite side. The penalty method tells the model what not
to say, with a fixed bias on a fixed word list at every step. Signal was taught by example: it
learned from the base model's own answers where it went straight to the point, so nothing is
banned and nothing is penalised at decode time. The model still branches where a branch does
work; it has simply stopped preferring the detour where the direct continuation was as good. 

## Using it as an agent

Signal works as a coding/agent model, and the terseness is an asset there: it spends fewer tokens
per step, so tool-driven loops run faster and cost less. On [Terminal-Bench 2.0](https://www.tbench.ai/)
(real fix-a-repo and sysadmin tasks scored by each task's own test suite), Signal solved **8 of 10**
tasks at `AP-Q4_K_XL`, finishing most shared tasks faster than the base model. Single trial per task,
so treat that as "handles real agentic work and is terser/faster," not a precise pass rate. It is also
strong on long-input, short-output work — reviewing or auditing a large codebase, where it reads the
whole context and returns focused findings instead of a wall of prose.

**One limitation to design around.** Signal is tuned to be concise, so it is not the right tool for a
single very long *generation* — asking it to emit one file of tens of thousands of tokens in one shot,
where it can lapse into repeating itself. Two easy mitigations, both good agent practice anyway:

- **Structure work as multiple manageable files** rather than one giant file. Each step stays in the
  length range where Signal is at its best.
- For a genuinely large single artifact, **use the base model** (or Signal with a capped output length
  and an explicit "write it out in full" instruction).

Keeping `presence_penalty 1.0` and `min-p 0.05` (above) also suppresses the repetition on longer
outputs; raising `presence_penalty` much higher is not recommended, as it can degrade very long
generations.

## Files

Nine tiers from IQ3_XXS to Q8_0, one folder each. AP = [Agention Precision](https://agention.ai/models/): tier
names refer to the base ftype, the per-tensor types are chosen for accuracy per gigabyte using Agention Precision recipes. All built from Signal's BF16 (rebuilt 2026-09-13) using our custom imatrix; KLD and top-1 are against that BF16 on a held-out 2026 corpus and wikitext-2, -c 2048. VRAM is the file size: this is a dense model,
nothing offloads.

| tier | size | eff. bpw | KLD held-out | top-1 | KLD wikitext | what |
|---|---:|---:|---:|---:|---:|---|
| `Q8_0` | 27.05 GiB | 8.26 | 0.0040 | 94.7% | 0.0046 | reference quality; every number below was measured on this file |
| `AP-Q6_K` | 20.89 GiB | 6.57 | 0.0055 | 94.5% | 0.0075 | Q6_K with imatrix |
| `AP-Q5_K_M` | 18.19 GiB | 5.72 | 0.0081 | 94.0% | 0.0093 | Q5_K_M with imatrix |
| `AP-Q4_K_XL` | 16.35 GiB | 5.14 | 0.0124 | 93.3% | 0.0148 | **precision tier** — matched unsloth's UD-Q4_K_XL on the base model at the same size |
| `AP-Q4_K_M` | 15.83 GiB | 4.98 | 0.0184 | 92.3% | 0.0218 | **fast tier** — +20% prefill over UD-Q4_K_M on the base model at the same size, some quality traded |
| `AP-IQ4_XS` | 13.27 GiB | 4.17 | 0.0287 | 90.9% | 0.0327 | UD-IQ4_XS per-tensor map with our imatrix — same size |
| `AP-Q3_K_XL` | 14.05 GiB | 4.41 | 0.0595 | 88.1% | 0.0562 | 3-bit body, Q6_K output + Q5_K embeddings — the 16 GB slot with headroom |
| `AP-IQ3_S` | 12.38 GiB | 3.89 | 0.0661 | 87.9% | 0.0655 | i-quant 3-bit body, protected head — the value pick under 4-bit |
| `AP-IQ3_XXS` | 11.39 GiB | 3.58 | 0.1003 | 85.7% | 0.1008 | smallest tier, most aggressive; quality traded for a long context in 16 GB |

**Which one:** `AP-Q4_K_XL` if 16.5 GiB fits, `AP-IQ4_XS` for the 13 GiB slot, `AP-Q4_K_M` when prefill
speed matters more than the last bit of quality, `AP-Q6_K` or `Q8_0` when memory is no object. For a
**16 GB card**, the three-bit tiers leave room for a long context plus the MTP draft head or the vision
projector: `AP-IQ3_XXS` (11.4 GiB) fits 100K+ context with extras, `AP-IQ3_S` (12.4 GiB) is the value
pick with a protected head, and `AP-Q3_K_XL` (14.1 GiB) trades context room for a little more margin.

## Running

Thinking on and off both work; the chat template is the original Qwen3.8 template.

**Sampling:** temperature 0.6, top-p 0.95, top-k 20, min-p 0.05, presence_penalty 1.0, as in the
commands below. The min-p cuts the low-probability tail that reasoning runaways are sampled from: on
five prompts that had run away at temperature 0.7 without min-p, Signal answered 14 of 15 draws at this
setting within an 8k budget, the base model 9 of 15 on the same prompts and settings. presence_penalty
1.0 further suppresses repetition on long outputs; keep it around 1.0 — much higher can degrade very
long generations. Use sampling rather than greedy decoding (we saw a single loop at temperature 0), and
do not raise the temperature to 1.0: on the smallest tier (`AP-IQ3_XXS`, 40 level-5 MATH-500 problems)
1.0 doubled the 90th-percentile reasoning length to the token cap and cost 12 points of accuracy
against 0.7.

**KV cache:** keep the cache at q8_0 or f16 for both K and V. A 4-bit value cache (`-ctv q4_1` or
`q4_0`) makes long reasoning traces degenerate into a repeated phrase; we reproduced a user's
loop report with exactly that setting, and the same prompt is clean at q8_0.

<details open>
<summary>llama.cpp</summary>

```bash
llama-server -hf agentionai/Signal-3.8-27B-GGUF:AP-Q4_K_XL \
  --jinja -ngl 999 -fa on -c 65536 -ctk q8_0 -ctv q8_0 \
  --temp 0.6 --top-p 0.95 --top-k 20 --min-p 0.05 --presence-penalty 1.0
```

Add the built-in draft head for the throughput above (needs a build with `--spec-type draft-mtp`):

```bash
  --spec-type draft-mtp --spec-draft-n-max 4 --no-spec-draft-backend-sampling
```

> [!IMPORTANT]
> On recent mainline llama.cpp, pass `--no-spec-draft-backend-sampling` whenever you enable the draft
> head. The default offloads draft sampling to the backend, which does not apply min-p (or the rest of
> the sampler) to accepted draft tokens — so a repetition can run away regardless of your sampling
> settings. This flag routes draft verification back through the sampler and keeps the MTP speedup.
> Builds without the flag are unaffected (they never had backend draft sampling).

Thinking is on by default. To turn it off per request, send
`"chat_template_kwargs": {"enable_thinking": false}` with the chat completion.
</details>

<details>
<summary>vLLM (NVIDIA Blackwell)</summary>

A community NVFP4 (W4A16) build for vLLM, MTP included, is at
[Shockem/Signal-3.8-27B-NVFP4](https://huggingface.co/Shockem/Signal-3.8-27B-NVFP4): 2x RTX 5060 Ti
16 GB, TP=2, 200k context, FP8 KV, ~50-70 tok/s, total solution wall time roughly half of the stock
model. The BF16 source for your own quants is
[agentionai/Signal-3.8-27B](https://huggingface.co/agentionai/Signal-3.8-27B).
</details>

<details>
<summary>Ollama / LM Studio</summary>

Import the GGUF as any Qwen3.8-27B file. Use the sampling settings above; the template is
embedded in the file.
</details>

## Method and tooling
Signal is trained by self-distillation on the base model's own answers; no external data. The tiers are
built with our own Rust tooling, [agention-infer](https://github.com/agentionai): `gguf-pack` for
byte-exact, content-addressed tier builds and validation, `gguf-info` for inspection, and a per-tensor
distortion solver behind the Agention Precision recipes. Every tier is measured against Signal's own
BF16 on a held-out 2026 corpus before it ships.

## Vision

Signal keeps Qwen3.8-27B's image input. The vision encoder and projector are untouched by the
tune, so the base model's own `mmproj-BF16.gguf` is at
the repository root, 0.87 GiB. Download it alongside any tier:

### Support AgentionAI
Signal3.8 is released freely. If it saves you compute or makes Qwen more useful, you can sponsor continued tuning, quantization and benchmarking on [GitHub](https://github.com/sponsors/agentionai).
