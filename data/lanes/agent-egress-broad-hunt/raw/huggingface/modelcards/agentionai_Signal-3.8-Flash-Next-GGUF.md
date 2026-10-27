---
base_model:
- Qwen/Qwen3.8-Flash-Next
base_model_relation: finetune
license: other
license_name: qwen-community-1.0
license_link: LICENSE
library_name: gguf
pipeline_tag: image-text-to-text
tags:
  - token-efficient
  - efficient-thinking
  - qwen3.8-flash-next
  - qwen4exp
  - terse
  - agentionai
---
<a href="https://www.agention.ai/"><img src="signal-flash-next.png" alt="AgentionAI — Signal Flash Next" width="100%"></a>

# Signal 3.8 Flash Next

Qwen3.8-Flash-Next, tuned for speed and efficiency.

AgentionAI Signal is a minimally invasive fine-tune of Qwen3.8-Flash-Next for lower latency and
better token efficiency. On MATH-500 it spends **26% fewer reasoning tokens** than the base model
with **half as many hesitation markers**, and scores higher (99.2% against 97.5%). As a coding agent
on Terminal-Bench 2.0 it finishes the same tasks in **25% less wall time**. With speculative decoding
it is faster still: the multi-token-prediction drafter agrees with Signal 90% of the time against
69% for the base model, so more tokens are accepted per forward pass.

Signal gets there by being direct, not by cutting corners. Reasoning models spend a large share of
their tokens on hesitation and re-checking rather than on new steps. Signal keeps every step that
does work and drops the ones that only describe the process, and in answers it drops preambles,
sign-offs, excess formatting and narration while keeping the substance. The 177B mixture-of-experts
backbone, the vision encoder and the multi-token-prediction draft head all work exactly as in the
base model, so it is a drop-in replacement.

Signal is trained by self-distillation, on Qwen3.8-Flash-Next's own answers generated under an
instruction to be direct that the released model no longer needs. No external data and no other
model's outputs went into it, so it keeps the base model's knowledge and voice intact.

## What changes, measured

**Speculative decoding gets faster.** Flash-Next drafts with a separate multi-token-prediction head.
Signal's answers are more predictable, so the drafter agrees more often. On coding output with
`--spec-type draft-mtp`, both at this Q4_K_XL tier on the same machine:

| | base | Signal |
|---|---|---|
| MTP draft acceptance | 69% | **90%** |

Higher acceptance means more tokens verified per forward pass, so decoding is faster on top of the
shorter answers.

**Agentic coding: same work, fewer tokens.** We ran Signal and the untouched Qwen3.8-Flash-Next as
the coding agent behind [marshall](https://github.com/agentionai) on ten tasks from
[Terminal-Bench 2.0](https://www.tbench.ai/), real fix-a-repo and sysadmin tasks scored by each
task's own test suite. Both at this `AP-Q4_K_XL` tier, same machine, MTP on, one trial per task.

| | base | Signal |
|---|---|---|
| tasks solved | 8 / 10 | **10 / 10** |
| wall time, tasks both solved | — | **25% less** |
| output tokens, tasks both solved | — | **15% fewer** |

Signal solved every task and used a quarter less wall time and 15% fewer tokens on the tasks both
solved, biggest on the long ones (`sanitize-git-repo` 254 s vs 901 s, `crack-7z-hash` 336 s vs
707 s). Single trial per task, so treat the pass counts as indicative rather than a rigorous rate.

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
work; it has simply stopped preferring the detour where the direct continuation was as good. On
120 MATH-500 problems at the recommended sampling, both at `AP-Q4_K_XL`:

| | base | Signal |
|---|---|---|
| hesitation markers per 1,000 reasoning tokens | 11.9 | **5.6** |
| reasoning tokens, median | 242 | **228** |
| reasoning tokens, mean | 1,240 | **919** |
| accuracy | 97.5% | **99.2%** |

The median barely moves: easy problems were already short. The mean drops by a quarter because the
long tail does, which is where the hesitation lived. The same effect is what makes speculative
decoding faster. The draft head misses exactly at the uncertain positions where hesitation tokens
live, so fewer of them means longer accepted drafts, which is the 69% to 90% acceptance above. It
is also why we recommend temperature 0.6 with min-p 0.05: sampling hotter puts probability back on
those tokens, and the acceptance gain shrinks with it.

The flip side follows from the same mechanism. Branching is how a model backtracks when
backtracking is needed, so on problems that genuinely reward exhaustive search Signal can run
out of budget where the base model would have found its way. That is the tradeoff described next.

## Where the tradeoff shows

Signal moves the point where the model commits to an answer.

**It decides sooner when it can.** On MATH-500 it answers 99.2% of the problems correctly at a
median of 228 reasoning tokens, and as a coding agent it finishes the same Terminal-Bench tasks
in a quarter less wall time. Problems the model can see through get a short trace and a committed
answer.

**When it cannot, it keeps working rather than guess.** On AIME 2025, 30 problems at a 32k-token
budget, Signal answered **23 correctly and 0 wrongly**; the seven misses were still working when
the budget ran out. The base model at the same budget answers 25 of the 30, also with no wrong
answers, so on competition mathematics at a fixed budget the base model finishes more problems.

| AIME 2025, 32k budget, one sample | base | Signal |
|---|---|---|
| correct | 25 / 30 | 23 / 30 |
| wrong answers | 0 | 0 |
| unanswered at the budget | 5 | 7 |

One sample per problem, so a difference of a problem or two is within noise. The base run used the
recommended sampling with the draft head; the Signal run used temperature 0.7 without it.

**Adaptive reasoning.** Signal spends the reasoning budget where the question asks for it rather
than on every question. Told to think carefully, check each step and verify the answer, it reasons
about half again as long on hard MATH-500 problems (median reasoning tokens +46%), because the tune
changed what the model prefers by default, not what it can do when asked. So the practical setting
for a hard problem is not a different model but a different request: ask it to verify, or raise
the effort, and it will.

**Pick by task.** Agentic and tool-driven work, and anything where a confident wrong answer costs
more than a missing one, favor Signal. Long exhaustive reasoning or brute-force enumeration at a
fixed token budget favors the base model, or Signal with a larger budget and an explicit request to
verify.


## Files

[Agention Precision](https://agention.ai/models/qwen3.8-flash-next/) recipes: per-tensor quant types
chosen for accuracy per gigabyte, built on the same recipes as the measured base
`Qwen3.8-Flash-Next-AP` tiers.

| tier | download | VRAM | experts (gate/up) |
|---|---:|---:|---|
| `Q8_0` | 175.3 GiB | ~135 GiB | Q8_0 8.5 bpw — reference quality |
| `AP-Q4_K_XL` | 94.2 GiB | ~67 GiB | Q4_K 4.5 bpw |
| `AP-IQ4_XS` | 84.2 GiB | ~57 GiB | IQ3_S 3.44 bpw |

VRAM is with the n-gram table offloaded to disk. More tiers to follow.

**Vision:** Signal keeps Qwen3.8-Flash-Next's image input. The projector `mmproj-F16.gguf` is at the
repository root — download it alongside the tier.

## Running

Thinking on and off both work; the chat template is the original Qwen3.8-Flash-Next template.

**Sampling:** temperature 0.6, top-p 0.95, top-k 20, min-p 0.05. The min-p trims the low-probability
tail that long reasoning traces branch from; on AIME it turned two budget misses into answers and cost
nothing on the problems already solved. Keep the KV cache at q8_0 or f16; a 4-bit value cache makes
long traces degenerate.

```bash
llama-server -hf agentionai/Signal-3.8-Flash-Next-GGUF:AP-Q4_K_XL \
  --jinja -ngl 999 -fa on --lazy-mode on -c 65536 -ctk q8_0 -ctv q8_0 \
  --temp 0.6 --top-p 0.95 --top-k 20 --min-p 0.05
```

Add the multi-token-prediction draft head for the acceptance above (needs a build with
`--spec-type draft-mtp`); the draft is a separate GGUF,
[agentionai/Qwen3.8-Flash-Next-MTP-Q8_0-GGUF](https://huggingface.co/agentionai/Qwen3.8-Flash-Next-MTP-Q8_0-GGUF):

```bash
  --spec-type draft-mtp --model-draft Qwen3.8-Flash-Next-MTP-Q8_0.gguf \
  --spec-draft-n-max 4 --no-spec-draft-backend-sampling
```

> [!IMPORTANT]
> On recent mainline llama.cpp, pass `--no-spec-draft-backend-sampling` whenever you enable the draft
> head. The default offloads draft sampling to the backend, which does not apply min-p (or the rest of
> the sampler) to accepted draft tokens — so a repetition can run away regardless of your sampling
> settings. This flag routes draft verification back through the sampler and keeps the MTP speedup.
> Builds without the flag are unaffected (they never had backend draft sampling).

Thinking is on by default. To turn it off per request, send
`"chat_template_kwargs": {"enable_thinking": false}` with the chat completion.

## 🛠️ 7. Method and tooling
Signal is trained by self-distillation on the base model's own answers; no external data. The tiers are
built with our own Rust tooling, [agention-infer](https://github.com/agentionai): `gguf-pack` for
byte-exact, content-addressed tier builds and validation, `gguf-info` for inspection, and a per-tensor
distortion solver behind the Agention Precision recipes. Every tier is measured against Signal's own
BF16 on a held-out 2026 corpus before it ships.

### Support AgentionAI

Signal is released freely. If it saves you compute or makes Qwen more useful, you can sponsor
continued tuning, quantization and benchmarking on [GitHub](https://github.com/sponsors/agentionai).
