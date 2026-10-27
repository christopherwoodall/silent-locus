---
license: apache-2.0
base_model: InternScience/Agents-A1
tags:
  - gguf
  - quantized
  - apex
  - moe
  - mixture-of-experts
  - qwen3
  - vlm
  - vision
  - agentic
---

<!-- apex-banner-v2 -->
<div style="background-color: #f59e0b; color: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">
<h2 style="color: white; margin: 0 0 10px 0;">⚡ Each donation = another big MoE quantized</h2>
<p style="font-size: 18px; margin: 0 0 15px 0;">I host <b>30+ free APEX MoE quantizations</b> as independent research. My only local hardware is an <b>NVIDIA DGX Spark</b> (122 GB unified memory), enough for ~30-50B-class MoEs, but <b>bigger ones (200B+) require rented compute</b> on H100/H200/Blackwell, typically $20-100 per quant.<br>If APEX quants are useful to you, your support directly funds those bigger runs.</p>
<p style="font-size: 20px; margin: 0;">
<a href="https://www.patreon.com/cw/mudler" style="color: white; text-decoration: underline;">🎉 Patreon (Monthly)</a> &nbsp;|&nbsp;
<a href="https://www.buymeacoffee.com/mudler" style="color: white; text-decoration: underline;">☕ Buy Me a Coffee</a> &nbsp;|&nbsp;
<a href="https://github.com/sponsors/mudler" style="color: white; text-decoration: underline;">⭐ GitHub Sponsors</a>
</p>
</div>

# Agents-A1 — APEX GGUF

**APEX (Adaptive Precision for EXpert Models)** quantizations of [InternScience/Agents-A1](https://huggingface.co/InternScience/Agents-A1) — a 35B Mixture-of-Experts agentic model built to scale heterogeneous agentic abilities across long-horizon search, engineering, scientific research, instruction following, and tool calling.

**Brought to you by the [LocalAI](https://github.com/mudler/LocalAI) team** | [APEX Project](https://github.com/mudler/apex-quant) | [Technical Report](https://github.com/mudler/apex-quant/blob/main/paper/APEX_Technical_Report.pdf)

## Available Files

| File | Profile | Best For |
|------|---------|----------|
| Agents-A1-APEX-I-Balanced.gguf | I-Balanced | Best overall — imatrix-enhanced, lowest worst-case divergence |
| Agents-A1-APEX-I-Quality.gguf | I-Quality | Highest quality with imatrix |
| Agents-A1-APEX-Quality.gguf | Quality | Highest quality (no imatrix) |
| Agents-A1-APEX-Balanced.gguf | Balanced | General purpose |
| Agents-A1-APEX-I-Compact.gguf | I-Compact | Consumer GPUs, imatrix-enhanced |
| Agents-A1-APEX-Compact.gguf | Compact | Consumer GPUs |
| Agents-A1-APEX-I-Mini.gguf | I-Mini | Smallest viable, fastest inference |
| mmproj.gguf | Vision projector | Required for image understanding |

## What is APEX?

APEX is a quantization strategy for Mixture-of-Experts (MoE) models. It classifies tensors by role (routed expert, shared expert, attention) and applies a layer-wise precision gradient — edge layers (first/last 5) get higher precision, middle layers get more aggressive compression. I-variants use diverse imatrix calibration (chat, code, reasoning, tool-calling, agentic traces, Wikipedia).

The key insight: in MoE models, expert FFN tensors make up the bulk of model weight but only ~8/256 experts activate per token. APEX compresses middle-layer experts more aggressively while preserving edge layers and keeping attention, SSM/Mamba, and shared-expert tensors at higher precision.

See the [APEX project](https://github.com/mudler/apex-quant) for full details, technical report, and scripts.

## Architecture

- **Model**: Agents-A1 (Qwen3_5MoeForConditionalGeneration, Qwen3.5 35B-A3B MoE base)
- **Layers**: 40
- **Experts**: 256 routed + 1 shared (8 active per token)
- **Total Parameters**: ~35B
- **Active Parameters**: ~3B per token
- **Attention**: Hybrid (full attention every 4th layer, linear otherwise)
- **Vision**: Built-in vision encoder (mmproj included)
- **APEX Config**: 5+5 symmetric edge gradient across 40 layers
- **Calibration**: v1.3 diverse dataset (chat, code, reasoning, multilingual, tool-calling, agentic traces, Wikipedia)

## Run with LocalAI

```bash
local-ai run mudler/Agents-A1-APEX-GGUF@Agents-A1-APEX-I-Balanced.gguf
```

## Credits

APEX is brought to you by the [LocalAI](https://github.com/mudler/LocalAI) team. Developed through human-driven, AI-assisted research. Built on [llama.cpp](https://github.com/ggerganov/llama.cpp). Base model by [InternScience](https://huggingface.co/InternScience).
