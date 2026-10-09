---
license: cc-by-4.0
pretty_name: GPT-5.6 Sol · Terra · Luna Library
language:
- en
task_categories:
- text-generation
size_categories:
- 10K<n<100K
tags:
- agent-traces
- gpt-5.6
- gpt-5.6-sol
- gpt-5.6-terra
- gpt-5.6-luna
- openai
- codex
- tool-use
- coding-agent
- chain-of-thought
- sft
- content-verified
- maintained-mirror
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train.parquet
---
<p align="center">
  <img src="https://huggingface.co/datasets/Crownelius/GPT-5.6-Sol-Luna-Terra-Traces/resolve/main/assets/stl_banner.png" alt="GPT-5.6 Sol Terra Luna Library" width="100%">
</p>

<div align="center">

# GPT-5.6 — Sol · Terra · Luna Library

<strong>A maintained mirror of <em>every</em> GPT-5.6 Sol / Terra / Luna dataset on Hugging Face — content-verified, attributed, in one place.</strong>

<img src="https://img.shields.io/badge/rows-15%2C353-ff7a1a?style=for-the-badge&labelColor=120a04">
<img src="https://img.shields.io/badge/variants-Sol%20·%20Terra%20·%20Luna-ffb020?style=for-the-badge&labelColor=120a04">
<img src="https://img.shields.io/badge/type-maintained%20mirror-39ff14?style=for-the-badge&labelColor=120a04">
<img src="https://img.shields.io/badge/license-CC--BY--4.0-c9b489?style=for-the-badge&labelColor=120a04">

[`Dataset Viewer`](https://huggingface.co/datasets/Crownelius/GPT-5.6-Sol-Luna-Terra-Traces/viewer/default/train) | [`Parquet`](data/train.parquet)

</div>

<div style="background:#160e06;border:1px solid #d39a13;border-radius:12px;padding:16px 18px;margin:18px 0;color:#fff5df;">
  <div style="font-size:12px;text-transform:uppercase;letter-spacing:.2em;color:#39ff14;">// what this is</div>
  <p style="margin:8px 0 0;"><strong>This is a maintained library — a community mirror of every publicly-available GPT-5.6 Sol / Terra / Luna dataset on Hugging Face</strong>, aggregated, validity-filtered, and content-verified with per-row source attribution. <strong>It is not Crownelius' own data.</strong> Every row credits its original uploader in <code>first_source_dataset</code>, and each contributing author is cited below. New verified sources — and new uploads to existing sources — are pulled in as they appear.</p>
</div>

## The three variants

| Variant | Rows | Source (original author) | Notes |
| --- | ---: | --- | --- |
| 🟠 **Sol** | 14,467 | [`greghavens/gpt-5.6-sol-coding-and-debugging-traces`](https://huggingface.co/datasets/greghavens/gpt-5.6-sol-coding-and-debugging-traces) | Codex-CLI agentic coding &amp; debugging rollouts; `teacher_model: gpt-5.6-sol`, xhigh reasoning, acceptance-test verified. |
| 🟢 **Terra** | 0 | — | **No public GPT-5.6-Terra dataset exists on Hugging Face yet.** Terra is named here as intended scope; verified Terra sources will be added the moment they appear. |
| 🔵 **Luna** | 886 | [`empero-ai/gpt-5.6-luna-sft-900x`](https://huggingface.co/datasets/empero-ai/gpt-5.6-luna-sft-900x) | Diverse synthetic SFT distilled from `openai/gpt-5.6-luna`. Note: the assistant is given a "Qwythos / Empero AI" persona — genuine gpt-5.6-luna output, but a persona-injected distill, not raw traces. |

**Total: 15,353 content-verified rows.**

## Changelog

- **2026-07-28** — Refreshed from upstream: **+9,065** new Sol rows as greghavens expanded their dataset (8,697 re-serialized rows were correctly rejected as payload-duplicates). Sol 5,402 → 14,467; library 6,288 → 15,353.
- **2026-07-16** — Library created: Sol (greghavens) + Luna (Empero AI), Terra listed at 0.

## Provenance &amp; honesty

Every retained row is **content-verified** as genuine GPT-5.6 output — Sol rows carry `teacher_model: gpt-5.6-sol` + Codex `call_…` tool-IDs; Luna rows carry `model: openai/gpt-5.6-luna`. Neither carries Anthropic (`toolu_`/`claude`) or foreign-model signals. This provenance is **source-asserted and content-verified — it is not, and cannot be, cryptographically certified by OpenAI**, and this dataset claims no OpenAI endorsement. Terra is listed at **0 rows** rather than filled with anything unverified — a title should not promise data that isn't here.

Rows are deduplicated by **both** `sha256(row_json)` and a **payload fingerprint** (content hashed independently of metadata wrappers), so re-serialized or re-chunked copies of rows already held cannot re-enter the library.

> Sibling library (Anthropic models): [`Crownelius/Complete-FABLE.5-traces-2M`](https://huggingface.co/datasets/Crownelius/Complete-FABLE.5-traces-2M). Kept in separate repos so each holds one honest model lineage.

<details>
<summary><strong>&#127760;&nbsp; The Trace Atlas — how these model families actually differ</strong> <sub>(a Fable-authored comparison across all five libraries · click to expand)</sub></summary>

<div style="background:linear-gradient(135deg,#050a0c 0%,#0a1418 55%,#050708 100%);border:1px solid #1f7f83;border-radius:14px;padding:18px 20px;margin:14px 0;color:#dffcff;">
  <div style="font-size:11px;text-transform:uppercase;letter-spacing:.26em;color:#39ff14;margin-bottom:6px;">// written by fable · trace atlas v1</div>
  <p style="margin:0;font-size:14px;line-height:1.65;">Five libraries now mirror five different lineages. They are <em>not</em> interchangeable corpora — each family leaves a different fingerprint in its traces, and if you train on them as if they were the same thing, you inherit the wrong habits. Here is what actually separates them.</p>
</div>

<div style="display:flex;flex-wrap:wrap;gap:12px;margin:16px 0;">

  <div style="flex:1 1 300px;min-width:280px;background:#04202a;border:1px solid #1f7f83;border-left:4px solid #7fe7ff;border-radius:12px;padding:14px 16px;">
    <div style="font-size:11px;letter-spacing:.2em;color:#7fe7ff;">ANTHROPIC</div>
    <div style="font-size:19px;font-weight:600;color:#dffcff;margin:2px 0 8px;">Fable 5 · Opus · Sonnet</div>
    <p style="margin:0;font-size:13px;line-height:1.6;color:#a8d4da;"><strong style="color:#7fe7ff;">Signature:</strong> the trace <em>is</em> the work. Long agentic sessions where the model reads files, runs commands, reads the error, and revises — <code>toolu_…</code> IDs, tool_result envelopes, self-correction mid-session. Opus/Sonnet rows are the opposite shape: single-turn, dense reasoning with no tools.</p>
    <p style="margin:8px 0 0;font-size:12px;color:#6fa8b0;"><strong>Use for:</strong> agentic coding, tool-use discipline, long-horizon recovery.</p>
  </div>

  <div style="flex:1 1 300px;min-width:280px;background:#160e06;border:1px solid #8a5a1f;border-left:4px solid #ffb020;border-radius:12px;padding:14px 16px;">
    <div style="font-size:11px;letter-spacing:.2em;color:#ffb020;">OPENAI</div>
    <div style="font-size:19px;font-weight:600;color:#fff5df;margin:2px 0 8px;">GPT-5.6 Sol · Luna</div>
    <p style="margin:0;font-size:13px;line-height:1.6;color:#d6c4a4;"><strong style="color:#ffb020;">Signature:</strong> verifier-shaped. Sol rows are Codex-CLI rollouts carrying <code>reasoning_effort: xhigh</code> and an explicit <code>verifier: acceptance-tests+quality-review</code> — the work was <em>graded</em> before it was published. Luna is a different animal: persona-injected chat distillation, not raw capture.</p>
    <p style="margin:8px 0 0;font-size:12px;color:#b09a72;"><strong>Use for:</strong> test-passing code, security review, graded outcomes.</p>
  </div>

  <div style="flex:1 1 300px;min-width:280px;background:#04141f;border:1px solid #1f6f8a;border-left:4px solid #28b7ff;border-radius:12px;padding:14px 16px;">
    <div style="font-size:11px;letter-spacing:.2em;color:#28b7ff;">ZHIPU AI</div>
    <div style="font-size:19px;font-weight:600;color:#dff4ff;margin:2px 0 8px;">GLM-5.2</div>
    <p style="margin:0;font-size:13px;line-height:1.6;color:#a3c8d6;"><strong style="color:#28b7ff;">Signature:</strong> the most <em>subject-partitioned</em> corpus here — conversation, science and logic-puzzle sets arrive as separate, deliberately-built slices rather than one undifferentiated dump. Nearly all of it is explicit chain-of-thought; very little is agentic.</p>
    <p style="margin:8px 0 0;font-size:12px;color:#7fa3b0;"><strong>Use for:</strong> structured CoT, science QA, formal logic.</p>
  </div>

  <div style="flex:1 1 300px;min-width:280px;background:#1e0608;border:1px solid #8a3229;border-left:4px solid #ff5a4d;border-radius:12px;padding:14px 16px;">
    <div style="font-size:11px;letter-spacing:.2em;color:#ff5a4d;">ALIBABA · TONGYI</div>
    <div style="font-size:19px;font-weight:600;color:#ffe9e4;margin:2px 0 8px;">Qwen</div>
    <p style="margin:0;font-size:13px;line-height:1.6;color:#d6b0a8;"><strong style="color:#ff5a4d;">Signature:</strong> the widest <em>version spread</em> — Qwen3, 3.5 and 3.8-Max sit side by side, so the same prompt style appears at several capability levels. Heavily distillation-oriented, and the most internally duplicated ecosystem we measured (one set was an exact 2× copy of itself).</p>
    <p style="margin:8px 0 0;font-size:12px;color:#b0857c;"><strong>Use for:</strong> distillation baselines, cross-version comparison.</p>
  </div>

  <div style="flex:1 1 300px;min-width:280px;background:#150a24;border:1px solid #6b46a8;border-left:4px solid #a06bff;border-radius:12px;padding:14px 16px;">
    <div style="font-size:11px;letter-spacing:.2em;color:#a06bff;">MOONSHOT AI</div>
    <div style="font-size:19px;font-weight:600;color:#efe4ff;margin:2px 0 8px;">Kimi K3</div>
    <p style="margin:0;font-size:13px;line-height:1.6;color:#bfb0d6;"><strong style="color:#a06bff;">Signature:</strong> scarce and new. Only two genuine public K3 datasets exist, so this is the smallest library by an order of magnitude — an honest snapshot of a frontier that hasn't been mirrored yet, not a shortfall in curation.</p>
    <p style="margin:8px 0 0;font-size:12px;color:#9285a8;"><strong>Use for:</strong> early K3 signal; treat as a seed, not a corpus.</p>
  </div>

</div>

### The three axes that actually matter

| Axis | What it separates | Where each family sits |
| --- | --- | --- |
| **Capture vs. distillation** | Was the session recorded, or was it re-generated? | Fable 5 & Sol are *captured* (harness transcripts). Opus, Sonnet, GLM, Qwen, Luna are *distilled* — cleaner, but one step removed from real behaviour. |
| **Agentic vs. single-turn** | Does the model act, or just answer? | Fable 5 / Sol / Kimi K3 carry tool calls and their results. Opus, Sonnet, GLM and Qwen are overwhelmingly one prompt → one long reasoned answer. |
| **Verifiability of origin** | Can you tell which model wrote it? | Strongest where rows carry an in-row `model` / `teacher_model` field (greghavens sets, Roman1111111, r0b0tlab). Weakest for reasoning distills, which never self-identify — those are card-asserted only, and labelled as such. |

<div style="background:#1a1204;border:1px solid #d39a13;border-radius:12px;padding:14px 16px;margin:16px 0;color:#fff5df;">
  <div style="font-size:11px;text-transform:uppercase;letter-spacing:.22em;color:#ffd479;">&#9888; the trap these libraries exist to avoid</div>
  <p style="margin:8px 0 0;font-size:13.5px;line-height:1.6;">Cross-model contamination is <strong>rampant</strong> and almost always invisible from the title. Verified examples caught while building these: a GLM-5.2 set carrying Anthropic <code>toolu_</code> IDs; a "Claude Sonnet" set whose reasoning was rewritten by <strong>Gemma-4-31B</strong>; a <code>claude-fable-5</code>-tagged set that was actually <strong>MiniMax MiMo</strong>; a Sonnet corpus silently blended with <strong>Gemini 3.1 Pro</strong>; and a "Fable5" dataset that turned out to be <strong>Sumerian cuneiform OCR</strong>. Every library here lists what it rejected, and why.</p>
</div>

<p align="center" style="font-size:12px;color:#7fa0a6;">
<a href="https://huggingface.co/datasets/Crownelius/Complete-FABLE.5-traces-2M">Claude</a> &#183;
<a href="https://huggingface.co/datasets/Crownelius/GPT-5.6-Sol-Luna-Terra-Traces">GPT-5.6</a> &#183;
<a href="https://huggingface.co/datasets/Crownelius/GLM-5.2-CoT-Library">GLM-5.2</a> &#183;
<a href="https://huggingface.co/datasets/Crownelius/Qwen-CoT-Library">Qwen</a> &#183;
<a href="https://huggingface.co/datasets/Crownelius/Kimi-K3-CoT-Library">Kimi K3</a>
</p>

</details>


## Schema

| Column | Type | Meaning |
| --- | --- | --- |
| `row_hash` | string | `sha256(row_json)` — stable de-duplication key |
| `first_source_dataset` | string | Upstream dataset / original author (also identifies the variant) |
| `first_source_config` / `first_source_split` | string | Upstream config / split |
| `first_source_row_index` | int64 | Index within the upstream source |
| `seen_count` | int64 | Times this canonical row was seen during aggregation |
| `row_json` | string | The full source row as JSON — parse for `messages`, `tools`, `model` / `teacher_model`, etc. |

## Citations &amp; attribution

All content belongs to its original uploaders and is re-hosted under their licenses, with full credit:

| Rows | Original author / dataset | License |
| ---: | --- | --- |
| 14,467 | **greghavens** — [`gpt-5.6-sol-coding-and-debugging-traces`](https://huggingface.co/datasets/greghavens/gpt-5.6-sol-coding-and-debugging-traces) | CC-BY-4.0 |
| 886 | **Empero AI** — [`gpt-5.6-luna-sft-900x`](https://huggingface.co/datasets/empero-ai/gpt-5.6-luna-sft-900x) | see upstream card |

If you use this library, please cite the original authors above — not this mirror.

## Loading

```python
from datasets import load_dataset
ds = load_dataset("Crownelius/GPT-5.6-Sol-Luna-Terra-Traces", split="train")

# filter to a variant via provenance:
sol  = ds.filter(lambda r: "gpt-5.6-sol"  in r["first_source_dataset"])
luna = ds.filter(lambda r: "gpt-5.6-luna" in r["first_source_dataset"])
```
