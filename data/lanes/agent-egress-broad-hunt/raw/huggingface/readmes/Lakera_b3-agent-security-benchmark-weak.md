---
license: other
task_categories:
- text-classification
- text-generation
language:
- en
tags:
- security
- safety
- agent
- prompt
- injection
- jailbreak
- tools
pretty_name: 'B3: AI Agent Security Benchmark'
size_categories:
- n<1K
configs:
- config_name: default
  data_files:
  - split: test
    path: "selected_attacks_low-quality.csv"
  
---
[[paper]](https://arxiv.org/pdf/2510.22620) [[blogpost]](https://www.lakera.ai/blog/the-backbone-breaker-benchmark) [[game]](https://play.lakera.ai/agent-breaker)

# b3 AI Security Benchmark: **B**reaking Agent **B**ack**b**ones
Highly contextalized prompt injections crowd-sourced during the [Agent Breaker Challenge](https://play.lakera.ai/agent-breaker). 
This is a *low-quality* version of the data behind [Breaking Agent Backbones: Evaluating the Security
 of Backbone LLMs in AI Agents](https://arxiv.org/pdf/2510.22620).
The high quality dataset was used to evaluate the security of more than 30 LLMs.

<img src="https://cdn-uploads.huggingface.co/production/uploads/650993961b3694179ddfa381/_Ic8YzJKjgjs5Dm0a5vFm.png" alt="drawing" width="400"/>


## Dataset Summary
**Purpose:** This dataset contains crowdsourced adversarial attacks against AI‑agent backbones (Large Language Models, LLMs) as collected via the Agent Breaker Challenge. It is designed for benchmarking the security of backbone LLMs embedded in agentic systems, by providing realistic contextual attack instances mapped to “threat snapshots” that isolate specific states of an agent execution flow.  
**Size:** *210 attacks* selected from *194,331 unique crowdsourced attacks* (from ~2,400 sessions) collected in the challenge. There are 630 entries, because each attack is assigned to 3 different security levels.
**Sample details:** Each sample contains an attack and the app slug identifying the threat snapshot it was collected from.

**Authors:** 
- Julia Bazińska (Lakera AI),
- Max Mathys (Lakera AI),
- Francesco Casucci (Lakera AI, ETH Zurich),
- Mateo Rojas-Carulla (Lakera AI),
- Xander Davies (UK AI Security Institute, OATML, University of Oxford),
- Alexandra Souly (UK AI Security Institute),
- Niklas Pfister (Lakera AI).

**Keywords:** LLM security, prompt injection, tool invocation, agentic systems, adversarial attacks, threat snapshots, AI agent security.

## Running the benchmark

The code to execute and grade the benchmark will soon be available as part of [Inspect Evals](https://github.com/UKGovernmentBEIS/inspect_evals).

## Dataset Structure
**Data format:** The dataset comprises records of attacks, each mapped to a specific “threat snapshot” (one of 10 agent applications × 3 defence levels L1/L2/L3) and annotated with metadata identifying the threat snapshot. See the threat_snapshot directory for specification of the threat snapshots.

**Defense levels:** The dataset contains 3 defense levels for each threat snapshot. The defense levels are:
- L1: System prompts without defense.
- L2: Stronger system prompts.
- L3: L1 with a self judge.

**Splits:** Benchmark dataset; no standard train/validation/test split.

**Repo Structure:**
- `threat_snapshots/`: Specifications of the threat snapshots.
- `tool_specs/`: Specifications of the tools used in the threat snapshots.
- `selected_attacks_low-quality.csv`: Actual attack data.

## Dataset Creation 
**Collection process:** Crowdsourced via [Agent Breaker Challenge](https://play.lakera.ai/agent-breaker).  
Steps:
1. Participants attack randomly assigned backbone LLMs within a specific snapshot/level.
2. Attacks are scored (0–100).
3. High‑scoring (≥75) attacks (~10.9k) are re‑evaluated across 7 different LLMs.
4. We exclude the top scoring attacks and include 7 unique attacks per snapshot × level (210 total).

## Dataset Maintenance & Licensing
**License:** MIT  
**Contact:** Niklas Pfister — niklas.pfister@lakera.ai  
**Citation:**
> Bazinska, J., Mathys, M., Casucci, F., Rojas‑Carulla, M., Davies, X., Souly, A., & Pfister, N. (2025). *Breaking Agent Backbones: Evaluating the Security of Backbone LLMs in AI Agents.* arXiv : 2510.22620.

