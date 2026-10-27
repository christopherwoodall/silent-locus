---
pretty_name: Exgentic Agent LLM Traces v2
language:
  - en
size_categories:
  - 10K<n<100K
task_categories:
  - text-generation
  - question-answering
  - other
task_ids:
  - dialogue-modeling
tags:
  - agents
  - agentic
  - benchmarks
  - opentelemetry
  - gen-ai
  - evaluation
  - tool-use
  - appworld
  - swebench
  - browsecomp
  - tau2
configs:
  - config_name: default
    data_files:
      - split: train
        path: data/train/*.parquet
---

# Exgentic Agent LLM Traces v2 — Agent Chat Only

OpenTelemetry-shaped execution traces for **10,057 agent runs** across **6 benchmarks** (AppWorld, SWE-bench, BrowseCompPlus, τ²-bench Airline/Retail/Telecom), filtered to the **agent under test's chat-only LLM calls**. This is the dataset for **replay testing**, behavioral analysis, or any task where you care about what the benchmarked model actually did — not the eval scaffolding around it.

**This v2 release expands upon [`Exgentic/agent-llm-traces`](https://huggingface.co/datasets/Exgentic/agent-llm-traces) (v1)** with 5.6× more traces (10,057 vs 1,781 sessions), higher-quality data, and additional attributes.

Derived from the full corpus [`Exgentic/traces-v2`](https://huggingface.co/datasets/Exgentic/traces-v2) — re-running that single script on the full corpus reproduces this dataset bit-for-bit.




---

## v1 drop-in compatible

```python
from datasets import load_dataset
ds = load_dataset("Exgentic/agent-llm-traces-v2", split="train")
row = ds[0]
row["spans"][0]["attributes"]["gen_ai.usage.input_tokens"]   # native int
row["spans"][0]["attributes"]["gen_ai.response.finish_reasons"]  # native list[str]
row["spans"][0]["attributes"]["gen_ai.request.temperature"]      # native float
row["spans"][0]["attributes"]["gen_ai.input.messages"]           # JSON string (parse to access parts)
```

Matches the published [`Exgentic/agent-llm-traces`](https://huggingface.co/datasets/Exgentic/agent-llm-traces) v1 layout — anything that loaded v1 directly loads this directly.

---

## Schema — chat-only, minimal attribute set

Every span has `gen_ai.operation.name == "chat"` and a non-empty `gen_ai.input.messages`. The attribute struct carries the 10 keys v1 already specified plus 8 populated `gen_ai.*` extras that downstream replay needs (LLM request parameters not in v1's 10).

| Attribute key | Type | Notes |
|---|---|---|
| `gen_ai.operation.name` | string | Always `"chat"` (the filter guarantees this) |
| `gen_ai.request.model` | string | Canonical name (no routing prefix — see below) |
| `gen_ai.response.model` | string | |
| `gen_ai.usage.input_tokens` | int64 | |
| `gen_ai.usage.output_tokens` | int64 | |
| `gen_ai.response.id` | string | |
| `gen_ai.response.finish_reasons` | list&lt;string&gt; | |
| `gen_ai.input.messages` | string (JSON) | OTel multi-part message shape |
| `gen_ai.output.messages` | string (JSON) | |
| `gen_ai.tool.definitions` | string (JSON) | |
| `gen_ai.request.temperature` | float64 | Extra vs v1 — needed for replay |
| `gen_ai.request.max_tokens` | int64 | Extra vs v1 |
| `gen_ai.request.stop_sequences` | list&lt;string&gt; | Extra vs v1 |
| `gen_ai.system_instructions` | string | Extra vs v1 |
| `gen_ai.output.type` | string | Extra vs v1 |
| `gen_ai.provider.name` | string | Extra vs v1 |
| `gen_ai.conversation.id` | string | Extra vs v1 |
| `error.type` | string | Set on failed calls (rate-limit, bad-request, …) |

Per-row top-level columns include the usual identifiers (`session_id`, `run_id`, `harness`, `benchmark`, `benchmark_subset`) plus per-session aggregates (`score`, `success`, `status`, `steps`, `action_count`, `agent_cost`, `benchmark_cost`, `execution_time`, `total_tokens`, `max_tokens`).

### Model name canonicalization

Routing prefix segments are stripped. `Azure/gpt-5.2-2025-12-11`, `openai/Azure/gpt-5.2-2025-12-11`, and `gpt-5.2-2025-12-11` (all the same deployment) collapse to a single canonical name. Both `gen_ai.request.model` / `gen_ai.response.model` in spans and the per-row top-level `models` list use the canonical form. After this fix, the dataset contains 5 distinct canonical models with zero top-level/span mismatches across all 10,057 rows.

---

## Filtering applied (by `build_agent_llm_traces.py`)

In order, per session:

1. **Drop scaffolding chats** — `exgentic.actor.role == "user_simulator"` (τ²-bench customer role-play) and `"judge"` (BrowseCompPlus correctness judge).
2. **Collapse failed-retry groups** — a run of consecutive failed chat spans (`status.code == 2`) with identical `gen_ai.input.messages`, terminated by a successful chat with the same input. Failed spans are dropped; subsequent spans shift back by the wasted retry duration (matches v1's `filter_failed_retries_and_adjust_timestamps`).
3. **Keep only chat spans with non-empty `gen_ai.input.messages`** — drops `invoke_agent`, `execute_tool`, and the small residue of stragglers whose response content was lost at ingest.
4. **Drop sessions with no surviving spans**.
5. **Project `attributes` to the 18 keys above** — `exgentic.*` provenance is dropped.
6. **Recompute `models` / `total_tokens` / `max_tokens` from surviving spans**.

---

## Storage layout

| | |
|---|---|
| Sessions (rows) | **10,057** (filtered from 10,573 full) |
| Total chat spans | **241,674** (filtered from 626,278 full) |
| Compressed size | **236 MB** across 9 shards |
| Shards | `data/train/{0000..0008}.parquet` |
| Compression | zstd level 12, `row_group_size=10`, `data_page_size=4 MB` |
| Source framework | [Exgentic](https://github.com/Exgentic/exgentic) |
| Tracing spec | [OTel GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) |

---

## Dataset Statistics

#### By Benchmark

| Benchmark | Traces (Sessions) | Turns (med/mean/max) | Harnesses | Models | Workload Description |
| --- | --- | --- | --- | --- | --- |
| appworld | 1500 | 19 / 32.3 / 300 | claude_code, openai_solo, smolagents_code, tool_calling, tool_calling_with_shortlisting | DeepSeek-V3.2, Kimi-K2.5, claude-opus-4-5, gemini-3-pro-preview | Personal assistant |
| browsecompplus | 1948 | 13 / 19.7 / 167 | claude_code, openai_solo, smolagents_code, tool_calling | DeepSeek-V3.2, Kimi-K2.5, claude-opus-4-5, gemini-3-pro-preview, gpt-5.2-2025-12-11 | Deep research |
| swebench | 1959 | 38 / 46.8 / 259 | claude_code, openai_solo, smolagents_code, tool_calling | DeepSeek-V3.2, Kimi-K2.5, claude-opus-4-5, gemini-3-pro-preview, gpt-5.2-2025-12-11 | Software engineering |
| tau2_airline | 957 | 10 / 11.4 / 151 | claude_code, openai_solo, smolagents_code, tool_calling | DeepSeek-V3.2, Kimi-K2.5, claude-opus-4-5, gemini-3-pro-preview, gpt-5.2-2025-12-11 | Customer service |
| tau2_retail | 1848 | 11 / 11.9 / 151 | claude_code, openai_solo, smolagents_code, tool_calling | DeepSeek-V3.2, Kimi-K2.5, claude-opus-4-5, gemini-3-pro-preview, gpt-5.2-2025-12-11 | Customer service |
| tau2_telecom | 1844 | 13 / 16.3 / 198 | claude_code, openai_solo, smolagents_code, tool_calling | DeepSeek-V3.2, Kimi-K2.5, claude-opus-4-5, gemini-3-pro-preview, gpt-5.2-2025-12-11 | Technical support |

#### By Model

| Model | #Traces | Avg LLM Calls | Failed Spans (%) | Avg Input Messages | Avg Tool Use Calls | Avg Duration (s) |
| --- | --- | --- | --- | --- | --- | --- |
| DeepSeek-V3.2 | 2299 | 29.4 | 5.74 | 47.8 | 0.66 | 675.68 |
| Kimi-K2.5 | 2285 | 24.13 | 7.07 | 48.47 | 0.54 | 462.24 |
| claude-opus-4-5 | 1920 | 29.06 | 22.94 | 36.43 | 0.86 | 1241.14 |
| gemini-3-pro-preview | 1428 | 24.14 | 2.35 | 37.69 | 1.16 | 687.34 |
| gpt-5.2-2025-12-11 | 2124 | 13.41 | 0.0 | 18.86 | 0.63 | 357.13 |

#### By Harness

| Harness | #Traces | Avg LLM Calls | Failed Spans (%) | Avg Input Messages | Avg Tool Use Calls | Avg Duration (s) |
| --- | --- | --- | --- | --- | --- | --- |
| claude_code | 2071 | 32.95 | 29.28 | 38.95 | 1.13 | 1742.0 |
| openai_solo | 2608 | 18.29 | 2.6 | 39.72 | 0.97 | 150.82 |
| smolagents_code | 2434 | 21.33 | 0.05 | 43.71 | 0.0 | 653.14 |
| tool_calling | 2643 | 22.16 | 0.23 | 43.72 | 0.94 | 317.8 |
| tool_calling_with_shortlisting | 300 | 50.14 | 0.06 | 25.92 | 0.62 | 1006.52 |

### Token Usage

The following tables show token usage statistics calculated from successful LLM API calls only (failed spans are excluded).

Token metrics include:
- **Avg. Request Tokens/Span**: Average input tokens per successful API call
- **Avg. Response Tokens/Span**: Average output tokens per successful API call
- **Avg. Total Tokens/Span**: Average total tokens (input + output) per successful API call
- **Avg. Total Tokens/Trace**: Average total tokens consumed across all successful API calls in a trace

#### Token Usage by Benchmark

| Benchmark | Avg. Request Tokens/Span | Avg. Response Tokens/Span | Avg. Total Tokens/Span | Avg. Total Tokens/Trace |
| --- | --- | --- | --- | --- |
| appworld | 61529 | 424 | 61953 | 1686420 |
| browsecompplus | 57173 | 764 | 57937 | 1556931 |
| swebench | 45237 | 1231 | 46469 | 2111792 |
| tau2_airline | 12434 | 389 | 12823 | 257511 |
| tau2_retail | 12392 | 303 | 12695 | 202004 |
| tau2_telecom | 16257 | 400 | 16656 | 331882 |

#### Token Usage by Model

| Model | Avg. Request Tokens/Span | Avg. Response Tokens/Span | Avg. Total Tokens/Span | Avg. Total Tokens/Trace |
| --- | --- | --- | --- | --- |
| DeepSeek-V3.2 | 28848 | 177 | 29025 | 880158 |
| Kimi-K2.5 | 22802 | 313 | 23115 | 654512 |
| claude-opus-4-5 | 66336 | 436 | 66772 | 2425658 |
| gemini-3-pro-preview | 40042 | 1746 | 41787 | 1108585 |
| gpt-5.2-2025-12-11 | 25467 | 827 | 26295 | 551742 |

#### Token Usage by Harness

| Harness | Avg. Request Tokens/Span | Avg. Response Tokens/Span | Avg. Total Tokens/Span | Avg. Total Tokens/Trace |
| --- | --- | --- | --- | --- |
| claude_code | 33686 | 262 | 33948 | 914499 |
| openai_solo | 18864 | 126 | 18989 | 522539 |
| smolagents_code | 71895 | 1914 | 73809 | 2368095 |
| tool_calling | 22710 | 158 | 22868 | 644134 |
| tool_calling_with_shortlisting | 10287 | 871 | 11158 | 693897 |

---

## Reproducing

```bash
huggingface-cli download Exgentic/traces-v2 --repo-type dataset --local-dir traces-v2/
python scripts/build_agent_llm_traces.py traces-v2/data/train out/data/train
```

---

## Citation

```bibtex
@misc{exgentic-agent-llm-traces-v2,
  title  = {Exgentic Agent LLM Traces v2: Chat-Only Execution Traces for Agent Benchmarks},
  author = {Exgentic team},
  year   = {2026},
  url    = {https://huggingface.co/datasets/Exgentic/agent-llm-traces-v2}
}
```
