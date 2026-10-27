---
library_name: transformers
license: apache-2.0
pipeline_tag: text-generation
language:
- en
- zh
tags:
- qwen3_5_moe
- qwen-agentworld
- world-model
- agentic-environment-simulation
- mtp
- abliterix
- apex
- quantization
- gguf
- multimodal
base_model:
- Qwen/Qwen-AgentWorld-35B-A3B
---

<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin-bottom: 24px;">
<div style="background: #f5f7fb; border-radius: 20px; padding: 36px 32px; margin-bottom: 20px; text-align: center; position: relative; overflow: hidden;">
<div style="position: absolute; top: -34px; right: -30px; width: 130px; height: 130px; background: #dbeafe; border-radius: 50%;"></div>
<div style="position: absolute; bottom: -24px; left: 34px; width: 92px; height: 92px; background: #bfdbfe; border-radius: 50%;"></div>
<div style="position: absolute; top: 50%; left: -20px; width: 64px; height: 64px; background: #dcfce7; border-radius: 50%;"></div>
<div style="display: inline-flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-bottom: 16px; position: relative; z-index: 1;">
<span style="background: #007aff; color: white; font-size: 11px; font-weight: 700; padding: 5px 14px; border-radius: 20px;">APEX-I</span>
<span style="background: #af52de; color: white; font-size: 11px; font-weight: 700; padding: 5px 14px; border-radius: 20px;">MTP</span>
<span style="background: #ff6b35; color: white; font-size: 11px; font-weight: 700; padding: 5px 14px; border-radius: 20px;">Abliterix</span>
<span style="background: #30d158; color: white; font-size: 11px; font-weight: 700; padding: 5px 14px; border-radius: 20px;">GGUF</span>
</div>
<h1 style="margin: 0 0 8px 0; font-size: 32px; font-weight: 800; color: #1d1d1f; letter-spacing: -0.5px; border: none; position: relative; z-index: 1;">Qwen-AgentWorld-35B-A3B-MTP-Uncensored-APEX</h1>
<p style="margin: 8px 0 0 0; font-size: 14px; position: relative; z-index: 1;"><span style="color: #86868b;">English</span> | <a href="https://huggingface.co/SC117/Qwen-AgentWorld-35B-A3B-MTP-Uncensored-GGUF/blob/main/README_zh.md" style="color: #007aff; text-decoration: none;">Chinese README</a></p>
<p style="margin: 10px 0 0 0; font-size: 15px; color: #64748b; position: relative; z-index: 1;">AgentWorld world model · Abliterix uncensored · native MTP injected · APEX-I GGUFs</p>
</div>
</div>

<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; display: flex; flex-direction: column; gap: 20px; margin-bottom: 30px;">

<div style="border: 1px solid #cbd5e1; border-radius: 12px; overflow: hidden; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
<div style="background: linear-gradient(135deg, #dc2626 0%, #f97316 100%); padding: 12px 16px; color: white; font-weight: 800; font-size: 14px;">Important Warning</div>
<div style="padding: 16px; font-size: 13px; color: #334155; line-height: 1.7;">
<p style="margin: 0;"><b>Qwen-AgentWorld is designed as an agentic environment simulation / language world model.</b> It is intended to simulate agent-environment interactions and predict environment states from actions and history. It is <b>not recommended</b> as a general daily assistant, coding model, or autonomous Agent backbone unless you specifically need this world-model behavior.</p>
</div>
</div>

<div style="border: 1px solid #cbd5e1; border-radius: 12px; overflow: hidden; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
<div style="background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); padding: 12px 16px; color: white; font-weight: 800; font-size: 14px;">About This Release</div>
<div style="padding: 16px; font-size: 13px; color: #334155; line-height: 1.7;">
<p style="margin: 0 0 12px 0;">This package contains GGUF releases of <a href="https://huggingface.co/Qwen/Qwen-AgentWorld-35B-A3B" target="_blank" style="color: #2563eb; text-decoration: none; font-weight: 700;">Qwen-AgentWorld-35B-A3B</a>, a Qwen3.5 MoE world model for agentic environment simulation.</p>
<p style="margin: 0 0 12px 0;">The model was modified with an Abliterix uncensored LoRA, stream-merged into safetensors, injected with one native MTP layer from a compatible Qwen3.5-35B-A3B MTP shard, converted to BF16 GGUF, and quantized into APEX-I tiers using a model-specific imatrix.</p>
<p style="margin: 0;">The release keeps the BF16 GGUF, imatrix, and <code>mmproj-F16.gguf</code> for reproducibility and multimodal llama.cpp use.</p>
</div>
</div>

<div style="border: 1px solid #cbd5e1; border-radius: 12px; overflow: hidden; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
<div style="background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); padding: 12px 16px; color: white; font-weight: 800; font-size: 14px;">Model Details</div>
<div style="padding: 16px;">
<table style="width: 100%; border-collapse: collapse; font-size: 13px;"><tbody>
<tr><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); font-weight: bold; color: #334155;">Base model</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); color: #4b5563;"><code>Qwen/Qwen-AgentWorld-35B-A3B</code></td></tr>
<tr><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); font-weight: bold; color: #334155;">Architecture</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); color: #4b5563;">Qwen3.5 MoE</td></tr>
<tr><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); font-weight: bold; color: #334155;">Parameters</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); color: #4b5563;">35B total, around 3B active per token</td></tr>
<tr><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); font-weight: bold; color: #334155;">Experts</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); color: #4b5563;">256 routed experts, 8 active per token</td></tr>
<tr><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); font-weight: bold; color: #334155;">Context</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); color: #4b5563;">262,144 tokens</td></tr>
<tr><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); font-weight: bold; color: #334155;">MTP</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); color: #4b5563;">1 injected MTP layer, 785 tensors</td></tr>
<tr><td style="padding: 7px 10px; font-weight: bold; color: #334155;">License</td><td style="padding: 7px 10px; color: #4b5563;">Apache-2.0</td></tr>
</tbody></table>
</div>
</div>

<div style="border: 1px solid #cbd5e1; border-radius: 12px; overflow: hidden; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
<div style="background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); padding: 12px 16px; color: white; font-weight: 800; font-size: 14px;">Abliterix Build</div>
<div style="padding: 16px; font-size: 13px; color: #334155; line-height: 1.7;">
<p style="margin: 0 0 12px 0;">The uncensored variant was produced with <a href="https://github.com/wuwangzhang1216/abliterix" target="_blank" style="color: #2563eb; text-decoration: none; font-weight: 700;">Abliterix</a>. The selected search result was trial 54 out of 110.</p>
<table style="width: 100%; border-collapse: collapse; font-size: 13px;"><tbody>
<tr><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); font-weight: bold;">KL divergence</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">0.0163</td></tr>
<tr><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); font-weight: bold;">Response length deviation</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">0.04 std devs</td></tr>
<tr><td style="padding: 7px 10px; font-weight: bold;">Refusals</td><td style="padding: 7px 10px;">21 / 100</td></tr>
</tbody></table>
<p style="margin: 12px 0 0 0;">The exported Abliterix LoRA was stream-merged into the full safetensors model before MTP injection and GGUF conversion.</p>
</div>
</div>

<div style="border: 1px solid #cbd5e1; border-radius: 12px; overflow: hidden; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
<div style="background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); padding: 12px 16px; color: white; font-weight: 800; font-size: 14px;">MTP Extraction And Injection</div>
<div style="padding: 16px; font-size: 13px; color: #334155; line-height: 1.7;">
<p style="margin: 0 0 12px 0;">The MTP layer was extracted from a compatible Qwen3.5-35B-A3B MTP shard and injected into the uncensored AgentWorld safetensors model.</p>
<table style="width: 100%; border-collapse: collapse; font-size: 13px;"><tbody>
<tr><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); font-weight: bold;">Tensor prefix</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);"><code>mtp.*</code></td></tr>
<tr><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); font-weight: bold;">Tensor count</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">785</td></tr>
<tr><td style="padding: 7px 10px; font-weight: bold;">Injected shard</td><td style="padding: 7px 10px;"><code>model-00022-of-00022.safetensors</code></td></tr>
</tbody></table>
</div>
</div>

<div style="border: 1px solid #cbd5e1; border-radius: 12px; overflow: hidden; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
<div style="background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); padding: 12px 16px; color: white; font-weight: 800; font-size: 14px;">BenchLocal Results</div>
<div style="padding: 16px;">
<table style="width: 100%; border-collapse: collapse; font-size: 13px;"><thead><tr style="background: rgba(37,99,235,0.06);"><th style="padding: 8px 10px; border-bottom: 2px solid #2563eb; text-align: left; color: #1d4ed8;">Model</th><th style="padding: 8px 10px; border-bottom: 2px solid #2563eb; text-align: left; color: #1d4ed8;">TC</th><th style="padding: 8px 10px; border-bottom: 2px solid #2563eb; text-align: left; color: #1d4ed8;">BF</th><th style="padding: 8px 10px; border-bottom: 2px solid #2563eb; text-align: left; color: #1d4ed8;">HA</th><th style="padding: 8px 10px; border-bottom: 2px solid #2563eb; text-align: left; color: #1d4ed8;">Ceiling</th><th style="padding: 8px 10px; border-bottom: 2px solid #2563eb; text-align: left; color: #1d4ed8;">Practical</th><th style="padding: 8px 10px; border-bottom: 2px solid #2563eb; text-align: left; color: #1d4ed8;">Retry</th></tr></thead><tbody>
<tr><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); font-weight: bold;">Original, thinking</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">100</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">87</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">81</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">88.5</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); font-weight: bold; color: #15803d;">87.5</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">1</td></tr>
<tr><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); font-weight: bold;">Uncensored + MTP, thinking</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">93</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">87</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">79</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">85.6</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); font-weight: bold; color: #1d4ed8;">81.6</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">4</td></tr>
<tr><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15); font-weight: bold;">Uncensored + MTP, no thinking</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">83</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">83</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">63</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">75.0</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">75.0</td><td style="padding: 7px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">0</td></tr>
<tr><td style="padding: 7px 10px; font-weight: bold;">Qwen3.6-35B thinking baseline</td><td style="padding: 7px 10px;">97</td><td style="padding: 7px 10px;">88</td><td style="padding: 7px 10px;">85</td><td style="padding: 7px 10px;">89.5</td><td style="padding: 7px 10px;">81.5</td><td style="padding: 7px 10px;">8</td></tr>
</tbody></table>
<p style="margin: 12px 0 0 0; font-size: 12px; color: #64748b; font-style: italic;">Thinking mode is strongly recommended for this model family.</p>
</div>
</div>

<div style="border: 1px solid #cbd5e1; border-radius: 12px; overflow: hidden; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
<div style="background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); padding: 12px 16px; color: white; font-weight: 800; font-size: 14px;">Usage</div>
<div style="padding: 16px; font-size: 13px; color: #334155; line-height: 1.7;">
<p style="margin: 0 0 8px 0; font-weight: bold;">llama.cpp server</p>
<p style="margin: 0; font-family: monospace; background: #f8fafc; padding: 10px 14px; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 12px; color: #1e293b; white-space: pre-wrap;">hf download SC117/Qwen-AgentWorld-35B-A3B-MTP-Uncensored-GGUF --include "*.gguf" --local-dir ./models/qwen-agentworld-mtp-uncensored
./llama-server -m ./models/qwen-agentworld-mtp-uncensored/Qwen-AgentWorld-35B-A3B-MTP-Uncensored-APEX-I-Compact.gguf -ngl 99 -c 131072</p>
<p style="margin: 12px 0 8px 0; font-weight: bold;">vision + text</p>
<p style="margin: 0; font-family: monospace; background: #f8fafc; padding: 10px 14px; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 12px; color: #1e293b; white-space: pre-wrap;">./llama-server -m ./models/qwen-agentworld-mtp-uncensored/Qwen-AgentWorld-35B-A3B-MTP-Uncensored-APEX-I-Compact.gguf --mmproj ./models/qwen-agentworld-mtp-uncensored/mmproj-F16.gguf -ngl 99 -c 131072</p>
</div>
</div>

<div style="border: 1px solid #cbd5e1; border-radius: 12px; overflow: hidden; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
<div style="background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); padding: 12px 16px; color: white; font-weight: 800; font-size: 14px;">APEX Quantization Tiers</div>
<div style="padding: 16px;">
<table style="width: 100%; border-collapse: collapse; font-size: 13px;"><thead><tr style="background: rgba(37,99,235,0.06);"><th style="padding: 8px 10px; border-bottom: 2px solid #2563eb; text-align: left; color: #1d4ed8;">File</th><th style="padding: 8px 10px; border-bottom: 2px solid #2563eb; text-align: left; color: #1d4ed8;">Size</th><th style="padding: 8px 10px; border-bottom: 2px solid #2563eb; text-align: left; color: #1d4ed8;">Profile</th><th style="padding: 8px 10px; border-bottom: 2px solid #2563eb; text-align: left; color: #1d4ed8;">Best For</th></tr></thead><tbody>
<tr><td style="padding: 8px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);"><code>*-APEX-I-Balanced.gguf</code></td><td style="padding: 8px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">24.14 GB</td><td style="padding: 8px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">I-Balanced</td><td style="padding: 8px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">Highest-retention all-rounder</td></tr>
<tr><td style="padding: 8px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);"><code>*-APEX-I-Quality.gguf</code></td><td style="padding: 8px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">21.68 GB</td><td style="padding: 8px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">I-Quality</td><td style="padding: 8px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">Quality-focused, IQ4_XS middle experts</td></tr>
<tr><td style="padding: 8px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);"><code>*-APEX-I-Compact.gguf</code></td><td style="padding: 8px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">15.75 GB</td><td style="padding: 8px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">I-Compact</td><td style="padding: 8px 10px; box-shadow: 0 1px 0 0 rgba(128,128,128,0.15);">Recommended quality/size ratio</td></tr>
<tr><td style="padding: 8px 10px;"><code>*-APEX-I-Mini.gguf</code></td><td style="padding: 8px 10px;">12.80 GB</td><td style="padding: 8px 10px;">I-Mini</td><td style="padding: 8px 10px;">Smallest practical tier</td></tr>
</tbody></table>
<p style="margin: 12px 0 0 0; font-size: 12px; color: #64748b;">The model-specific imatrix was generated from cleaned AgentWorld calibration text: <code>PPL = 4.5880 +/- 0.01173</code>.</p>
</div>
</div>

</div>

## Links

- **Original Model**: https://huggingface.co/Qwen/Qwen-AgentWorld-35B-A3B
- **Qwen-AgentWorld Project**: https://github.com/QwenLM/Qwen-AgentWorld
- **Abliterix**: https://github.com/wuwangzhang1216/abliterix
- **APEX Quantization**: https://github.com/mudler/apex-quant
- **BenchLocal Thinking**: https://scorp1o117.github.io/benchlocal-results/models/qwen-agentworld-35b-thinking.html
- **BenchLocal No Thinking**: https://scorp1o117.github.io/benchlocal-results/models/qwen-agentworld-35b.html

## Citation

```bibtex
@misc{qwen-agentworld-2026,
  title = {Qwen-AgentWorld: Language World Models for General Agents},
  author = {Qwen Team},
  year = {2026},
  url = {https://github.com/QwenLM/Qwen-AgentWorld}
}
```

<!-- SC117_SUPPORT_START -->
<div align="center">
  <a href="https://ko-fi.com/sc117">
    <img
      src="https://huggingface.co/SC117/Qwen3.8-Flash-Next-GSQ-RCO-abliterated-GGUF/resolve/main/assets/support-sc117.png"
      alt="Support SC117 on Ko-fi — support is optional and all releases remain freely available."
      width="100%"
    />
  </a>
</div>
<!-- SC117_SUPPORT_END -->
