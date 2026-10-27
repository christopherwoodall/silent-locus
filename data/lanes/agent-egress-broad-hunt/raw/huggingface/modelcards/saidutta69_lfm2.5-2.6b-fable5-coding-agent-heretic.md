---
license: other
license_link: https://huggingface.co/LiquidAI/LFM2.5-2.6B/blob/main/LICENSE
base_model: AyoubChLin/lfm2.5-2.6b-fable5-coding-agent
tags:
  - lfm2
  - heretic
  - uncensored
  - decensored
  - abliterated
  - coding-agent
  - tool-use
  - conversational
  - text-generation-inference
language:
  - en
pipeline_tag: text-generation
---

# LFM2.5-2.6B-Fable5-Coding-Agent-heretic

<div align="center">
  <img src="https://photu.kashyalabanavli.site/racer-is-op.png" alt="RACER IS OP" width="100%">
</div>

<br>

A decensored variant of [AyoubChLin/lfm2.5-2.6b-fable5-coding-agent](https://huggingface.co/AyoubChLin/lfm2.5-2.6b-fable5-coding-agent) (full-parameter SFT of [LiquidAI/LFM2.5-2.6B](https://huggingface.co/LiquidAI/LFM2.5-2.6B) on [saidutta69/fable-5-premium](https://huggingface.co/datasets/saidutta69/fable-5-premium)), produced with [Heretic](https://github.com/p-e-w/heretic) v1.4.0 (directional ablation / "abliteration"). Refusal behavior is suppressed via targeted weight edits to the attention output and MLP down-projections rather than fine-tuning, so the base model's coding-agent capabilities, tool-use patterns, and instruction-following are left largely intact.

**Abliteration results:** KL divergence 0.014 · Refusals reduced from 96/100 → 7/100.

**Who this is for:** developers who want a compact 2.6B coding agent with LFM2's hybrid conv+attention architecture — fast inference, tool-call generation, code generation, and multi-turn assistant behavior — without refusal guardrails. Not a capability upgrade over the base model — same model, refusal guardrails removed.


<!-- racer-gpu-matrix -->
## Runs on your gaming PC

Full GGUF ladder included — pick the quant that fits your card:

| Your GPU | Recommended quant | Weights |
| :--- | :--- | :--- |
| RTX 3090 / 4090 / 5090 (24 GB) | Q8_0 | ~2.9 GB |
| RTX 4080 / 5080 / 4060 Ti 16G (16 GB) | Q6_K | ~2.3 GB |
| RTX 3060 / 4070 / 5070 (12 GB) | Q5_K_M | ~2.0 GB |
| RTX 4060 / 3070 (8 GB) | Q4_K_M | ~1.8 GB |
| GTX 1660 Super / 2060 / 3050 laptop (6 GB) | IQ4_XS | ~1.6 GB |
| CPU-only / Apple Silicon | Q4_K_M | fits in system RAM |

Weights only, at this model's 2.7B native size; add ~1 GB for context.
OOM? Drop one quant level. Headroom to spare? Go one up.

## Why abliteration instead of fine-tuning

Fine-tuning a "helpful" persona on top of RLHF'd refusals fights the base model's training and tends to degrade coherence. Abliteration instead finds and edits the specific weight directions responsible for refusal, leaving the rest of the network (and its capabilities) untouched. See the [Heretic repo](https://github.com/p-e-w/heretic) and the [original abliteration writeup](https://huggingface.co/blog/mlabonne/abliteration) for the mechanism.

## Files

### GGUF quantizations
Full quantization set (14 quants + F16) produced with [llama.cpp](https://github.com/ggml-org/llama.cpp).

| File | Format | Size |
|---|---|---|
| `lfm2.5-2.6b-fable5-coding-agent-heretic-F16.gguf` | GGUF F16 | 5.03 GB |
| `lfm2.5-2.6b-fable5-coding-agent-heretic-Q2_K.gguf` | GGUF Q2_K | 1.02 GB |
| `lfm2.5-2.6b-fable5-coding-agent-heretic-IQ3_S.gguf` | GGUF IQ3_S | 1.18 GB |
| `lfm2.5-2.6b-fable5-coding-agent-heretic-Q3_K_S.gguf` | GGUF Q3_K_S | 1.18 GB |
| `lfm2.5-2.6b-fable5-coding-agent-heretic-Q3_K_M.gguf` | GGUF Q3_K_M | 1.27 GB |
| `lfm2.5-2.6b-fable5-coding-agent-heretic-Q3_K_L.gguf` | GGUF Q3_K_L | 1.35 GB |
| `lfm2.5-2.6b-fable5-coding-agent-heretic-IQ4_XS.gguf` | GGUF IQ4_XS | 1.42 GB |
| `lfm2.5-2.6b-fable5-coding-agent-heretic-Q4_K_S.gguf` | GGUF Q4_K_S | 1.49 GB |
| `lfm2.5-2.6b-fable5-coding-agent-heretic-Q4_0.gguf` | GGUF Q4_0 | 1.48 GB |
| `lfm2.5-2.6b-fable5-coding-agent-heretic-Q4_1.gguf` | GGUF Q4_1 | 1.63 GB |
| `lfm2.5-2.6b-fable5-coding-agent-heretic-Q4_K_M.gguf` | GGUF Q4_K_M | 1.56 GB |
| `lfm2.5-2.6b-fable5-coding-agent-heretic-Q5_K_S.gguf` | GGUF Q5_K_S | 1.77 GB |
| `lfm2.5-2.6b-fable5-coding-agent-heretic-Q5_K_M.gguf` | GGUF Q5_K_M | 1.81 GB |
| `lfm2.5-2.6b-fable5-coding-agent-heretic-Q6_K.gguf` | GGUF Q6_K | 2.07 GB |
| `lfm2.5-2.6b-fable5-coding-agent-heretic-Q8_0.gguf` | GGUF Q8_0 | 2.68 GB |

LFM2 hybrid conv+attention architecture — loads natively in llama.cpp (arch `lfm2`).

Run `llama serve -hf saidutta69/lfm2.5-2.6b-fable5-coding-agent-heretic` to pull the default quant.

## Quickstart

### llama.cpp

```bash
# defaults to the Q4_K_M quant
llama serve -hf saidutta69/lfm2.5-2.6b-fable5-coding-agent-heretic:Q4_K_M
```

### Ollama

```bash
ollama run hf.co/saidutta69/lfm2.5-2.6b-fable5-coding-agent-heretic:Q4_K_M
```

### LM Studio

1. Open LM Studio and click the search icon to open the Model Search panel.
2. Type "lfm2.5-2.6b-fable5-coding-agent-heretic" and click the download button marked **GGUF**.
3. Pick your quant, load the model, and start chatting.

### Transformers

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "saidutta69/lfm2.5-2.6b-fable5-coding-agent-heretic"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    dtype=torch.bfloat16,
    device_map="auto",
)

messages = [
    {"role": "system", "content": "You are a helpful coding assistant."},
    {"role": "user", "content": "Write a Python function that merges overlapping intervals."},
]

inputs = tokenizer.apply_chat_template(
    messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
).to(model.device)

with torch.inference_mode():
    output = model.generate(**inputs, max_new_tokens=512, temperature=0.1)

print(tokenizer.decode(output[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True))
```

## Responsible use

Refusal suppression is deliberate and works as intended: this model will comply with requests the base model would refuse, including some it shouldn't. There is no safety filtering layered on top. You are responsible for how you deploy it.

> Made with ❤️ by **RACER IS OP** — follow for more uncensored models

## License

Inherits the [LFM Open License v1.0](https://huggingface.co/LiquidAI/LFM2.5-2.6B/blob/main/LICENSE) from the base model.
