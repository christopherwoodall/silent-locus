---
configs:
  - config_name: customer-support-triage
    data_files:
      - split: train
        path: data/customer-support-triage/train.parquet
  - config_name: code-review-pipeline
    data_files:
      - split: train
        path: data/code-review-pipeline/train.parquet
  - config_name: market-research
    data_files:
      - split: train
        path: data/market-research/train.parquet
  - config_name: legal-document-analysis
    data_files:
      - split: train
        path: data/legal-document-analysis/train.parquet
  - config_name: data-pipeline-debugging
    data_files:
      - split: train
        path: data/data-pipeline-debugging/train.parquet
  - config_name: content-generation
    data_files:
      - split: train
        path: data/content-generation/train.parquet
  - config_name: financial-analysis
    data_files:
      - split: train
        path: data/financial-analysis/train.parquet
  - config_name: incident-response
    data_files:
      - split: train
        path: data/incident-response/train.parquet
  - config_name: academic-paper-review
    data_files:
      - split: train
        path: data/academic-paper-review/train.parquet
  - config_name: ecommerce-product-enrichment
    data_files:
      - split: train
        path: data/ecommerce-product-enrichment/train.parquet
license: mit
language:
  - en
task_categories:
  - text-generation
  - text-classification
tags:
  - agent-traces
  - ocel
  - multi-agent
  - process-mining
  - synthetic
  - llm-agents
  - conformance-checking
  - ai-agents
  - workflow-traces
  - agent-observability
  - tool-use
  - chain-of-thought
  - anomaly-detection
pretty_name: Open Agent Traces
size_categories:
  - 10K<n<100K
---

# Open Agent Traces

**17,019 LLM-enriched agent trace events** across **500 workflow runs** in **10 enterprise domains** and **3 workflow patterns**.

Generated with [ocelgen](https://github.com/juliensimon/ocel-generator) (`pip install open-agent-traces`) and validated against the OCEL 2.0 standard, PM4Py, and 5 semantic validation layers.

```python
from datasets import load_dataset

ds = load_dataset("juliensimon/open-agent-traces", "incident-response")

for event in ds["train"]:
    if event["run_id"] == "run-0000":
        print(f"{event['event_type']:25s} | {event['agent_role']:12s} | {event['reasoning'][:60] if event['reasoning'] else ''}")
```

## What's inside each trace

Every event includes the same data you'd see in production agent observability tools:

- **Agent reasoning** — chain-of-thought for every agent step
- **LLM prompts and completions** — realistic request/response pairs with calibrated token counts
- **Tool calls with inputs and outputs** — structured JSON for each tool invocation
- **Inter-agent messages** — handoff content between workflow steps
- **Deviation labels** — ground-truth annotations marking conformant vs anomalous behavior
- **Realistic timestamps** — seconds-scale LLM latencies, not synthetic milliseconds
- **Cost estimates** — per-invocation and per-run cost tracking

```
run-0000: "My order arrived damaged, what are my options?"
├── run_started                                              08:00:00.007
├── agent_invoked          researcher    gpt-4o              08:00:00.052
│   ├── llm_request_sent   "Search for refund policy..."     08:00:00.067
│   ├── llm_response       "The refund policy states..."     08:00:00.749
│   ├── tool_called        web_search    → policy found      08:00:01.705
│   └── tool_called        file_reader   → order history     08:00:01.898
├── agent_invoked          analyst       gpt-4o              08:00:02.281
│   ├── llm_request_sent   "Analyze refund eligibility..."   08:00:02.334
│   ├── llm_response       "Customer is eligible for..."     08:00:06.747
│   └── tool_called        calculator    → refund amount     08:00:08.819
├── agent_invoked          summarizer    claude-3.5-sonnet   08:00:09.680
│   ├── llm_request_sent   "Draft resolution response..."    08:00:09.717
│   └── llm_response       "Dear customer, we apologize..."  08:00:10.363
└── run_completed                                            08:00:10.369
    cost: $0.038 | 3,950 input + 2,516 output tokens | 5 LLM calls | 3 tool calls
```

## Domains

| Config | Pattern | Runs | Noise | Events | Description |
|--------|---------|------|-------|--------|-------------|
| `customer-support-triage` | sequential | 50 | 20% | 1,483 | Classify ticket, research KB, draft response |
| `code-review-pipeline` | supervisor | 50 | 20% | 2,035 | Delegate to linter, security reviewer, style checker |
| `incident-response` | supervisor | 50 | 30% | 1,976 | Route to diagnostics, mitigation, communications |
| `data-pipeline-debugging` | supervisor | 50 | 25% | 2,033 | Log analyzer, schema checker, fix proposer |
| `market-research` | parallel | 50 | 20% | 1,671 | Competitor analyst, trend researcher, report writer |
| `content-generation` | parallel | 50 | 20% | 1,668 | Researcher, writer, editor working concurrently |
| `academic-paper-review` | parallel | 50 | 15% | 1,695 | Methodology, novelty, writing reviewers |
| `legal-document-analysis` | sequential | 50 | 15% | 1,498 | Extract clauses, check compliance, summarize risks |
| `financial-analysis` | sequential | 50 | 20% | 1,471 | Gather filings, compute ratios, write investment memo |
| `ecommerce-product-enrichment` | sequential | 50 | 20% | 1,489 | Scrape specs, normalize attributes, generate descriptions |

**Workflow patterns:**
- **Sequential** — linear chain (A → B → C)
- **Supervisor** — central agent delegates to specialist workers
- **Parallel** — fan-out to concurrent agents, then aggregate

## Schema

Each row is one event in the OCEL 2.0 trace:

| Column | Type | Description |
|--------|------|-------------|
| `event_id` | string | Unique event identifier |
| `event_type` | string | `run_started`, `agent_invoked`, `llm_request_sent`, `llm_response_received`, `tool_called`, `tool_returned`, `message_sent`, `routing_decided`, `agent_completed`, `run_completed`, `error_occurred`, `retry_started` |
| `timestamp` | string | ISO 8601 with realistic inter-event durations |
| `run_id` | string | Workflow run identifier |
| `sequence_number` | int | Monotonic order within the run |
| `is_deviation` | bool | Whether this event is part of an injected deviation |
| `deviation_type` | string | `skipped_activity`, `inserted_activity`, `wrong_resource`, `swapped_order`, `wrong_tool`, `repeated_activity`, `timeout`, `wrong_routing`, `missing_handoff`, `extra_llm_call` |
| `step_id` | string | Workflow step identifier |
| `agent_role` | string | Agent role (e.g. `researcher`, `supervisor`, `coder`) |
| `model_name` | string | LLM model (e.g. `gpt-4o`, `claude-3-5-sonnet`) |
| `prompt` | string | LLM prompt text |
| `completion` | string | LLM completion text |
| `tool_name` | string | Name of the tool called |
| `tool_input` | string | Tool input as JSON |
| `tool_output` | string | Tool output as JSON |
| `message_content` | string | Inter-agent handoff message |
| `reasoning` | string | Agent chain-of-thought reasoning |
| `input_tokens` | int | Input token count (calibrated to content) |
| `output_tokens` | int | Output token count (calibrated to content) |
| `latency_ms` | int | LLM or tool call latency in ms |
| `cost_usd` | float | Estimated invocation cost |
| `is_conformant` | bool | Whether the run follows the expected workflow |
| `pattern` | string | `sequential`, `supervisor`, or `parallel` |
| `domain` | string | Domain name (same as config name) |
| `user_query` | string | User request that initiated the run |

## Usage examples

```python
from datasets import load_dataset

# Load one domain
ds = load_dataset("juliensimon/open-agent-traces", "customer-support-triage")

# Get all LLM completions
completions = ds["train"].filter(lambda x: x["event_type"] == "llm_response_received")
for row in completions:
    print(f"Prompt: {row['prompt'][:100]}...")
    print(f"Completion: {row['completion'][:100]}...")

# Analyze deviations
deviant = ds["train"].filter(lambda x: x["is_deviation"])
print(f"Deviation types: {set(e for e in deviant['deviation_type'] if e)}")

# Cross-domain comparison
for domain in ["customer-support-triage", "incident-response", "code-review-pipeline"]:
    ds = load_dataset("juliensimon/open-agent-traces", domain)
    agents = set(row["agent_role"] for row in ds["train"] if row["agent_role"])
    print(f"{domain}: {agents}")
```

### Load with PM4Py

```python
from huggingface_hub import hf_hub_download
import pm4py

path = hf_hub_download(
    repo_id="juliensimon/open-agent-traces",
    filename="ocel/incident-response/output.jsonocel",
    repo_type="dataset",
)
ocel = pm4py.read.read_ocel2_json(path)

# Event types are in 'ocel:activity' (not 'ocel:type')
print(ocel.events["ocel:activity"].value_counts())
```

## Use cases

- **Agent observability and debugging** — build and test monitoring dashboards with the same data platforms like LangSmith, Arize, and Braintrust display
- **Conformance checking and anomaly detection** — train models to detect deviant agent behavior using labeled ground-truth deviations
- **Process mining** — apply OCEL 2.0 conformance checking algorithms to multi-agent systems
- **Agent evaluation and benchmarking** — compare agent reasoning across sequential, supervisor, and parallel architectures
- **Agent framework testing** — validate orchestration frameworks against realistic trace data across 10 enterprise domains

## Files per domain

| Path | Format | Description |
|------|--------|-------------|
| `data/{domain}/train.parquet` | Parquet | Flat tabular (one row per event) |
| `ocel/{domain}/output.jsonocel` | OCEL 2.0 JSON | Native object-centric event log |
| `ocel/{domain}/normative_model.json` | JSON | Expected workflow template |
| `ocel/{domain}/manifest.json` | JSON | Generation metadata + deviation ground truth |

## Generate your own

```bash
pip install open-agent-traces

# Generate structural traces (no API key needed)
ocelgen generate --pattern sequential --runs 50 --noise 0.2 --seed 42

# Enrich with any OpenAI-compatible LLM
ocelgen enrich output.jsonocel --domain customer-support-triage

# Or use a local model
ocelgen enrich output.jsonocel -d customer-support-triage \
  --model local-model --base-url http://localhost:8080/v1
```

See the [ocelgen documentation](https://github.com/juliensimon/ocel-generator) for custom domains, validation, and the full CLI reference.

## How it was built

Generated with **[ocelgen](https://github.com/juliensimon/ocel-generator)** — a two-pass architecture:

1. **Structural generation** — OCEL 2.0 traces with configurable workflow patterns, deviation injection (10 types), and deterministic seeding
2. **LLM enrichment** — each agent step enriched with domain-specific prompts; outputs chain across steps for coherence

Quality measures:
- 5 semantic validators (referential integrity, temporal ordering, type attributes, workflow conformance, JSON schema)
- Validated with PM4Py across all 10 domains
- Token counts calibrated to actual content length
- Realistic timestamps (seconds-scale LLM latencies)
- 50 unique queries per domain (LLM-expanded from seed set)
- Deviation-aware content (deviant steps reflect failures in their reasoning)

## Citation

```bibtex
@misc{open-agent-traces-2026,
  title={Open Agent Traces: Synthetic Multi-Agent Workflow Datasets},
  author={Julien Simon},
  year={2026},
  publisher={Hugging Face},
  url={https://huggingface.co/datasets/juliensimon/open-agent-traces}
}
```

## License

MIT — source code at [github.com/juliensimon/ocel-generator](https://github.com/juliensimon/ocel-generator)
