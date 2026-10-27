---
license: apache-2.0
language:
  - en
pretty_name: MCP Agent Trajectory Benchmark (50-Row Free Evaluation)
tags:
  - mcp
  - function-calling
  - tool-use
  - agents
  - synthetic
  - error-recovery
task_categories:
  - text-generation
size_categories:
  - n<1K
configs:
  - config_name: default
    data_files:
      - split: train
        path: data.jsonl
extra_gated_prompt: "This free sample is Apache-2.0. To help us understand who is evaluating agent-reliability data, please share the fields below. Access is granted automatically."
extra_gated_fields:
  Company / Organization: text
  I plan to use this dataset for:
    type: select
    options:
      - Agent evaluation / reliability testing
      - Fine-tuning
      - Research
      - label: Other
        value: other
extra_gated_button_content: "Agree and access the sample"
---
# 🛑 Stop LLM Agent Collapse Caused by State Corruption

**Most agent failures are not tool failures. They are state failures.**
The model believes the world is still valid — when reality has already changed.

<!-- firstview-bridge -->
### 🔎 Explore the Evidence Behind This Dataset

Want to understand the dataset's design, validation, and limitations?

**[Explore the evidence, methodology, and validation results →](https://springofwindslabs.github.io/springofwinds-datasets/?utm_source=huggingface&utm_medium=readme_bridge&utm_campaign=mcp-agent-trajectory-benchmark&utm_content=firstview)**

Review the supporting evidence and intended use before deciding whether this dataset fits your workflow.

---


This MCP trajectory dataset trains **belief revision**, **state recovery**, and **autonomous replanning**:

```text
believed : 45/50 rooms synced       ← agent trusts a stale worker log
tool     : "success", count: 0      ← silent no-op (the worst failure mode)
verify   : GDS reports actual = 40  ← belief revision from live evidence
replan   : re-sync rooms 41–50      ← autonomous recovery, no human in loop
```

**MCP Agent Trajectory Dataset** — Official Enterprise Data Repository by **springofwindslabs**  

> **Full production volumes** (1,000-row standard and 2,300+ row non-overlapping extended lots), commercial licensing, and the measured validation methodology are documented in the [project documentation](https://springofwindslabs.github.io/springofwinds-datasets/?utm_source=huggingface&utm_medium=readme&utm_campaign=mcp-agent-trajectory-benchmark).

---


<!-- commercial-bridge -->
## 🔎 You Have the Trial — Here Is What It Proves, and What It Doesn't

This free trial demonstrates the **failure modes** (the problem). It is fully usable
under Apache-2.0 and validated by the same pipeline as the commercial lots.

What the **full dataset** adds: full failure-class coverage across 6+ turn trajectories — 403 scope, 429 backoff, resource locks, and silent no-op state corruption with verified recovery arcs.

| | Free trial (this repo) | Full dataset |
|---|---|---|
| Purpose | verify schema, quality & failure modes | systematic training / evaluation |
| Volume | sample | 1,000 rows (1K) / 3,300 rows (2K combined) per track |
| Validation | same pipeline | 28,922 rows measured, 100% schema-pass — published |
| Overlap | — | lots are hash / ID / 3-gram audited non-overlapping |

**→ [Verify the measured evidence before you consider anything](https://springofwindslabs.github.io/springofwinds-datasets/?utm_source=huggingface&utm_medium=readme_bridge&utm_campaign=mcp-agent-trajectory-benchmark)**
*(independent evidence hub: full EVALS, row-level sample anatomy, and a reproduction
script you can run against this trial — no signup, no tracking walls)*

---

## 📁 Validated Package Architecture

Every commercial delivery natively bundles the complete execution context stack. These assets are designed for enterprise procurement workflows while remaining fully accessible to research teams evaluating alignment quality:

```text
├── dataset.jsonl   (Strict schema-validated multi-turn tool-use rows)
├── README.md       (Operational constraints, schema docs & license terms)
├── stats.json      (Row counts, turn distribution & QC metrics)
└── SHA256SUMS.txt  (Cryptographic integrity manifest for audit trails)
```

---

## 🧠 Data Philosophy: Why Enterprise LLM Teams Require Production-Grade Trajectories

When evaluating dataset scaling for fine-tuning open-weights models (Llama-3, Qwen-2.5, GLM-5.3, etc.), global AI engineering teams frequently hit major friction with high-volume public synthetic datasets (e.g., TOUCAN with 1.5M tracks) [Github]. 

While public synthetic datasets offer massive footprints, they naturally suffer from **Success-Bias and Model Lock-In**. Generated inside perfect closed environments, those models collapse instantly in production when encountering real-world network friction, state stale latency, or rigid permission controls.

**The Springofwindslabs Baseline is Built for Resilient Production Deployment.**  
Instead of raw unverified entropy, our factory processes high-density, 100% schema-validated unique trajectories pre-loaded with hyper-realistic autonomous error-recovery tracks. Every single row forces the model to master real-world exceptions:
- **403 Insufficient Scope** (Autonomous privilege discovery and token refreshment)
- **429 Rate Limit Backoff** (Dynamic backoff algorithms, jitter injections, and token bucket tracking)
- **Resource Lock Conflicts** (Deterministic state checks and multi-step corrective retries)

---

## 📦 Dataset Structure & Quick Start

This repository ships `data.jsonl` — a 50-row free evaluation subset of the MCP Agent Trajectory Dataset (Strict JSONL, UTF-8, 1 row = 1 sample).

**Schema (per row):**
```json
{
  "id": "unique sample identifier",
  "tools": "JSON string: array of available tool definitions (name, description, parameters)",
  "conversations": [
    {"from": "user",      "value": "task request"},
    {"from": "assistant", "value": "tool call as strict JSON"},
    {"from": "tool",      "value": "tool execution result (incl. 403/429/lock errors)"},
    {"from": "assistant", "value": "recovery step or final answer"}
  ]
}
```

**Load with 🤗 Datasets:**
```python
from datasets import load_dataset
ds = load_dataset("springofwindslabs/mcp-agent-trajectory-benchmark", split="train")
print(ds[0]["conversations"])
```

---

## 📊 Available Packages & Enterprise Procurement Gateways

For production alignment pipelines and commercial system integration, select the specialized trajectory factory branch required for your organization via the project documentation below:

### 🌐 1. MCP Agent Trajectory Dataset (Strict JSONL)
Hyper-specialized for multi-turn Model Context Protocol environments across 38 enterprise domains. Fully aligned with ATIF-v1.2 specifications [Hugging Face].
- **Standard Volume (1,003 High-Fidelity Rows):** Available for immediate production deployment.
- **Extended Volume (2,300+ Non-Overlapping Rows):** Available now. Mutually exclusive production rows.
- ➔ **Commercial licensing & documentation:** https://springofwindslabs.github.io/springofwinds-datasets/?utm_source=huggingface&utm_medium=readme&utm_campaign=mcp-agent-trajectory-benchmark

### 🛠️ 2. Function Calling Dataset for LLM Alignment (English Native)
Engineered for deterministic multi-turn tool execution, hard constraint parameter parsing, and strict execution sandboxing.
- **Standard Volume (1,000 High-Fidelity Rows):** Available for immediate production deployment.
- **Extended Volume (2,300+ Non-Overlapping Rows):** Available now.
- ➔ **Commercial licensing & documentation:** https://springofwindslabs.github.io/springofwinds-datasets/?utm_source=huggingface&utm_medium=readme&utm_campaign=mcp-agent-trajectory-benchmark

### 🇯🇵 3. Japanese Function Calling Dataset (High-Context Domain)
Designed explicitly to solve token efficiency and structural breakdown issues native to Japanese high-context tool routing, honorific variations, and entity double-meanings.
- **Standard Volume (1,000 High-Fidelity Rows):** Available for immediate production deployment.
- **Extended Volume (2,300+ Non-Overlapping Rows):** Available now.
- ➔ **Commercial licensing & documentation:** https://springofwindslabs.github.io/springofwinds-datasets/?utm_source=huggingface&utm_medium=readme&utm_campaign=mcp-agent-trajectory-benchmark

### ⚖️ 4. Regulatory Compliance & Legal CoT (Chain‑of‑Thought) Dataset
Our highest premium asset. Forces frontier-grade models to navigate complex multi-jurisdictional financial compliance, data privacy checks, and structural risk audit trails before emitting tool execution payloads.
- **Standard Volume (1,000 High-Fidelity Rows):** Available for immediate production deployment.
- **Extended Volume (2,300+ Non-Overlapping Rows):** Available now.
- ➔ **Commercial licensing & documentation:** https://springofwindslabs.github.io/springofwinds-datasets/?utm_source=huggingface&utm_medium=readme&utm_campaign=mcp-agent-trajectory-benchmark

---

## 🧪 Open-Source Evaluation Samples (Apache-2.0)
Before procuring our full production-grade volumes, download the official 50-row validation samples to run structural verification within your training framework (Axolotl, Unsloth, etc.):
- ➔ **MCP Free Evaluation Sample:** https://huggingface.co/datasets/springofwindslabs/mcp-agent-trajectory-benchmark
- ➔ **Function Calling Free Evaluation Sample:** https://huggingface.co/datasets/springofwindslabs/function-calling-en-trial
- ➔ **Japanese Function Calling Free Evaluation Sample:** https://huggingface.co/datasets/springofwindslabs/function-calling-ja-trial
- ➔ **Regulatory Compliance & Legal CoT Free Evaluation Sample:** https://huggingface.co/datasets/springofwindslabs/regulatory-compliance-cot-trial

⚖️ **Commercial Terms:** Procurement includes perpetual organizational usage rights. Standalone raw redistribution is strictly prohibited. For corporate NDAs, custom enterprise billing, or direct bank wire transfers, contact our data factory team directly at: `springofwindslabs@gmail.com`

---

## 🧩 Complete springofwindslabs Dataset Family

Enterprise alignment pipelines rarely need just one capability. Teams that procure two or more branches report faster convergence across tool-routing, multilingual execution, and compliance reasoning:

| Capability Branch | Free 50-Row Evaluation (Hugging Face) | Commercial documentation |
|---|---|---|
| 🌐 MCP Agent Trajectories | [mcp-agent-trajectory-benchmark](https://huggingface.co/datasets/springofwindslabs/mcp-agent-trajectory-benchmark) | [Details ➔](https://springofwindslabs.github.io/springofwinds-datasets/?utm_source=huggingface&utm_medium=readme&utm_campaign=mcp-agent-trajectory-benchmark) |
| 🛠️ Function Calling (EN) | [function-calling-en-trial](https://huggingface.co/datasets/springofwindslabs/function-calling-en-trial) | [Details ➔](https://springofwindslabs.github.io/springofwinds-datasets/?utm_source=huggingface&utm_medium=readme&utm_campaign=mcp-agent-trajectory-benchmark) |
| 🇯🇵 Function Calling (JA) | [function-calling-ja-trial](https://huggingface.co/datasets/springofwindslabs/function-calling-ja-trial) | [Details ➔](https://springofwindslabs.github.io/springofwinds-datasets/?utm_source=huggingface&utm_medium=readme&utm_campaign=mcp-agent-trajectory-benchmark) |
| ⚖️ Regulatory Compliance CoT | [regulatory-compliance-cot-trial](https://huggingface.co/datasets/springofwindslabs/regulatory-compliance-cot-trial) | [Details ➔](https://springofwindslabs.github.io/springofwinds-datasets/?utm_source=huggingface&utm_medium=readme&utm_campaign=mcp-agent-trajectory-benchmark) |

💼 **Multi-branch procurement:** for combined multi-dataset licensing or volume terms across two or more branches, contact `springofwindslabs@gmail.com` — consolidated invoicing available.

---

## 🗺 Release Roadmap — Lot 2 & New Reasoning Domains

Our data factory ships on a continuous production cadence. Currently in the pipeline:

- 🏭 **Lot 2 — In Active Production:** a fresh wave of fully non-overlapping production rows (hash, ID and 3-gram Jaccard audited against Lot 1) across the dataset family.
- ⚖️ **New Regulatory CoT Domains — Planned:** additional Chain-of-Thought reasoning branches expanding jurisdictional and compliance-domain coverage.
- 🔔 **Never miss a release:** click **Follow** on [springofwindslabs](https://huggingface.co/springofwindslabs) here on Hugging Face, and see the [project documentation](https://springofwindslabs.github.io/springofwinds-datasets/?utm_source=huggingface&utm_medium=readme&utm_campaign=mcp-agent-trajectory-benchmark) to receive release alerts the moment new lots go live.

Existing Lot 1 license holders can expand coverage incrementally — every new lot is guaranteed non-overlapping with prior purchases, so no budget is ever spent twice on the same row.

---

## 🏢 Enterprise Institutional Procurement & Tier Transparency

Our production assets are curated exclusively for institutional LLM alignment pipelines and commercial system integration. To align with quarterly technology budgets, we offer tiered procurement caps based on transaction row density (**Standard 1,000-row volumes** vs. **2,300+ row non-overlapping lot packages** — mutually exclusive by hash, ID and 3-gram Jaccard audit). Commercial invoicing, corporate wire clearance, and SLA terms are fully detailed upon gateway entry.

Enterprise teams evaluating MCP / tool-use alignment can advance directly to production deployment here:

🚀 **Advance straight to production-grade LLM alignment today:**
➔ Commercial licensing and package details: **[Commercial licensing and package details](https://springofwindslabs.github.io/springofwinds-datasets/?utm_source=huggingface&utm_medium=readme&utm_campaign=mcp-agent-trajectory-benchmark)**

## 📖 Citation

If this dataset supports your research or product evaluation, please cite:

```bibtex
@misc{springofwindslabs2026mcp,
  title  = {MCP Agent Trajectory Benchmark: Schema-Validated Multi-Turn Tool-Use Trajectories with Error Recovery},
  author = {springofwindslabs},
  year   = {2026},
  url    = {https://huggingface.co/datasets/springofwindslabs/mcp-agent-trajectory-benchmark}
}
```

---

### Enterprise Procurement
For licensing, corporate invoicing, procurement review, or custom commercial agreements:
✉️ springofwindslabs@gmail.com

<!-- repo-doctor-bridge -->
## 🩺 Building with AI coding agents? (free tool from this lab)

Datasets like this one train agents to handle tool calls and recovery — but the
**repository you point an agent at** matters just as much. Missing AGENTS.md,
undiscoverable build/test commands, or absent constraints make even strong
models fail.

We built **repo-doctor** — a zero-dependency CLI that scores a repository's
**AI readiness** (plus docs, secrets exposure, tests/CI, dependencies, hygiene,
git history) in one command, fully offline:

```bash
repo-doctor .
```

Free & MIT-licensed → **[github.com/springofwindslabs/repo-doctor](https://github.com/springofwindslabs/repo-doctor)**
