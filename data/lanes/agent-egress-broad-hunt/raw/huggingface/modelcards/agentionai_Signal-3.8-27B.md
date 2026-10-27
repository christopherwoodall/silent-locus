---
base_model:
- Qwen/Qwen3.8-27B
base_model_relation: finetune
license: apache-2.0
license_link: LICENSE
library_name: transformers
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

> [!IMPORTANT]
> **Update 2026-09-13 — use these settings for stable, short reasoning**
> Temperature 0.6, min-p 0.05 (top-p 0.95, top-k 20), KV cache q8_0 or f16, and the MTP draft head on.
> Without min-p, long answers can run away into repetition on some draws; a 4-bit value cache makes that
> deterministic. Both are fixed by the settings above, on Signal and on the base model alike.

> [!WARNING]
> The weights in this repository were updated on 2026-09-13 (the GGUF tiers were rebuilt from them). The first release's tiers could, rarely,
> repeat an answer line when sampling without the draft head; the rebuilt tiers showed no loop or cap
> in 55 traces under the same conditions. If you downloaded before that date, re-download.


This is Qwen3.8-27B that gets to the answer faster.

AgentionAI Signal is a minimally invasive fine-tune of Qwen3.8-27B designed for lower generation latency and better token efficiency. On our held-out general-prompt evaluation, Signal produces **57% fewer answer tokens** and uses **52% fewer thinking tokens**, while matching or improving the measured answer quality of the base model.

*The percentages above were measured on the first release. The weights updated on 2026-09-13 trade a little of that reduction for stability; their re-measurement on the same prompt set is in progress and will replace these numbers.*

The result is substantially faster end-to-end generation: on typical chat prompts, Signal can finish in less than **half the wall time** of the untouched Qwen3.8-27B on the same hardware.

Signal gets there by being more direct rather than by truncating answers. It removes unnecessary preambles, excessive formatting, sign-offs, and explanatory narration while preserving the substance of the response. In thinking mode, it keeps the useful reasoning steps while spending fewer tokens describing the process.

Signal is trained by self-distillation: on Qwen3.8-27B's own answers, generated under an instruction to be direct that the released model no longer needs. No external data and no other model's outputs went into it, which is why it keeps the base model's knowledge and voice intact.

These are the full BF16 weights in Hugging Face format, a drop-in replacement for Qwen3.8-27B in transformers, vLLM, SGLang and any quantization pipeline. Quantized GGUF tiers from IQ4_XS to Q8_0 are in [agentionai/Signal-3.8-27B-GGUF](https://huggingface.co/agentionai/Signal-3.8-27B-GGUF).

## What changes, measured

We evaluated Signal against the untouched Qwen3.8-27B, both at Q8_0 in llama.cpp, using the same server, sampling settings, prompts, and otherwise identical model file. All prompts in these evaluations were held out from tuning.


| | base Q8_0 | Signal | change |
|---|---|---|---|
| general answers, median tokens | 243 | 104 | **-57%** |
| answers opening with a preamble ("Sure!", "Great question") | 13% | 0% | **gone** |
| answers with markdown headers | 47% | 18% | -62% |
| answers with bold | 85% | 52% | -39% |
| coding answers, median tokens | 159 | 142 | -11% |
| coding answers, p90 tokens | 1026 | 914 | -11% |

Thinking mode, same prompts with reasoning on:

| | base Q8_0 | Signal | change |
|---|---|---|---|
| reasoning tokens, general prompts, median | 153 | 74 | **-52%** |
| reasoning tokens, coding prompts, median | 225 | 166 | -26% |
| reasoning tokens, GSM8K, median | 119 | 81 | -32% |

Quality, exact match on GSM8K:

| | base Q8_0 | Signal |
|---|---|---|
| thinking off, 60 problems | 98.3% | 98.3% |
| thinking on, 40 problems | 92.5% | **95.0%** |

Shorter is not cheaper: no answer in the 100-prompt style set was cut off early (0 answers
ending on a header or a colon, 0 unclosed code blocks), and no reasoning trace in 50
thinking-mode outputs looped or hit the token cap.

## Faster with speculative decoding

Qwen3.8-27B carries a built-in multi-token-prediction draft head. Signal's answers are more predictable, so the drafter agrees with the model more often:

Draft acceptance and decode speed with `--spec-type draft-mtp`, both models Q8_0 on the same
machine (Strix Halo, Vulkan), 200-token greedy runs for the fixed-draft rows:

| prompt / draft length | base acceptance | Signal acceptance | decode speed vs base |
|---|---:|---:|---:|
| prose, draft 3 | 39% | 47% | **+10%** |
| prose, draft 4 | 35% | 28% | -9% |
| structured output (JSON), draft 3 | 72% | 94% | **+20%** |
| structured output (JSON), draft 4 | 66% | 87% | **+22%** |
| chat prompts, sampled at 0.7, adaptive draft ≤4 (40 prompts) | 57% | 60% | — |

## What is in the repository

The complete Qwen3.8-27B checkpoint, 18 safetensors shards in BF16, with one tensor replaced: `lm_head.weight`. Every other tensor, the vision encoder, the projector, the MTP draft head, the tokenizer and the chat template are byte-identical to `Qwen/Qwen3.8-27B`. The head delta has a norm of 4.1% of the original head. Vision input works as in the base model.

Because only the output layer differs, any quantization recipe, LoRA, or serving setup that works on Qwen3.8-27B works on Signal unchanged.

## Running

Thinking on and off both work; the chat template is the original Qwen3.8 template.

**Sampling:** temperature 0.7, top-p 0.95, top-k 20, min-p 0. Use sampling rather than greedy
decoding. We saw a single loop at temperature 0.

<details open>
<summary>transformers</summary>

```python
from transformers import AutoProcessor, AutoModelForImageTextToText

model_id = "agentionai/Signal-3.8-27B"
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForImageTextToText.from_pretrained(model_id, dtype="bfloat16", device_map="auto")

messages = [{"role": "user", "content": "Explain how a hash map works."}]
inputs = processor.apply_chat_template(messages, add_generation_prompt=True, tokenize=True,
                                       return_dict=True, return_tensors="pt").to(model.device)
out = model.generate(**inputs, max_new_tokens=1024, do_sample=True, temperature=0.7, top_p=0.95, top_k=20)
print(processor.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True))
```

Thinking is on by default. Pass `enable_thinking=False` to `apply_chat_template` to turn it off.
</details>

<details>
<summary>vLLM</summary>

```bash
vllm serve agentionai/Signal-3.8-27B --dtype bfloat16 --max-model-len 65536 --reasoning-parser qwen3
```

Then call the OpenAI-compatible endpoint with the sampling settings above. Send
`"chat_template_kwargs": {"enable_thinking": false}` to turn thinking off per request.
</details>

<details>
<summary>llama.cpp</summary>

Use the prebuilt tiers in [agentionai/Signal-3.8-27B-GGUF](https://huggingface.co/agentionai/Signal-3.8-27B-GGUF), which include the vision projector and the multi-token-prediction draft head, or convert this checkpoint with `convert_hf_to_gguf.py`.
</details>

### Support AgentionAI
Signal3.8 is released freely. If it saves you compute or makes Qwen more useful, you can sponsor continued tuning, quantization and benchmarking on [GitHub](https://github.com/sponsors/agentionai).
