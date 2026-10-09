---
license: apache-2.0
language:
- en
pretty_name: BetterWright Agent Traces
size_categories:
- 1K<n<10K
task_categories:
- text-generation
tags:
- agent
- browser-agent
- web-agent
- tool-use
- function-calling
- reasoning
- betterwright
- trajectories
- synthetic
configs:
- config_name: accepted
  default: true
  data_files:
  - split: train
    path: data/accepted/train-*.parquet
---

# BetterWright Agent Traces

Full, untruncated agent trajectories recorded **inside the [BetterWright](https://github.com/BetterWright/betterwright) harness** (v2.8.7, `runAgentTask` — the same loop behind `betterwright exec`) while two open models drove a real BetterChromium browser against the **live web**. Every row is one complete run: the harness system prompt and tool schemas, every model turn with its **full reasoning**, every `browser` tool call (JavaScript/Playwright-style snippets executed by the harness), every tool result exactly as the harness returned it, the final `done` answer, per-turn token/latency telemetry, and an LLM-judge verdict.

It is meant for SFT / rejection-sampling / preference / RL work on models that should be *very good inside the BetterWright harness specifically* — the prompts, tools, observation format and failure modes are the harness's own, not a generic browser-agent abstraction.

## Summary

- **traces**: 4,647
- **accepted**: 3,840
- **unique tasks**: 1,672
- **turns**: 84,740
- **tool calls**: 84,615
- **completion tokens**: 57,613,050
- **reasoning tokens**: 29,195,602
- **max context tokens**: 188,262
- **length stops**: 2
- **built**: 2026-09-22T04:46:34Z

### By model and reasoning effort
| model / effort | traces | accepted | mean turns | mean max context (tok) |
|---|---:|---:|---:|---:|
| DeepSeek-V4.1-Flash / high | 804 | 689 | 16.4 | 34,488 |
| DeepSeek-V4.1-Flash / low | 804 | 681 | 17.7 | 30,242 |
| DeepSeek-V4.1-Flash / medium | 812 | 688 | 16.8 | 30,418 |
| DeepSeek-V4.1-Flash / none | 813 | 664 | 17.2 | 23,608 |
| Qwen3.8-Flash-Next / low | 352 | 266 | 17.4 | 22,976 |
| Qwen3.8-Flash-Next / medium | 353 | 279 | 19.5 | 32,828 |
| Qwen3.8-Flash-Next / none | 354 | 277 | 26.1 | 30,298 |
| Qwen3.8-Flash-Next / xhigh | 355 | 296 | 21.0 | 36,556 |

### By task horizon
| tier | traces | accepted | mean turns | mean max context (tok) |
|---|---:|---:|---:|---:|
| long | 1207 | 1000 | 21.6 | 35,990 |
| medium | 1580 | 1357 | 15.6 | 21,538 |
| short | 1308 | 1102 | 10.5 | 13,152 |
| very_long | 552 | 381 | 36.8 | 80,873 |

### By site mode
| site mode | traces | accepted | mean turns | mean max context (tok) |
|---|---:|---:|---:|---:|
| read | 3515 | 2926 | 19.3 | 33,496 |
| sandbox | 727 | 555 | 14.3 | 18,783 |
| tool | 405 | 359 | 16.1 | 19,555 |

## How it was made

- **Harness:** BetterWright 2.8.7 on Bun, BetterChromium 153 (headless), one fresh isolated browser profile per run, no credential vault, downloads denied. The agent loop, system prompt, tool definitions (`browser`, `done`, and `ask` when a simulated user is attached), transcript handling, retries and stop conditions are all the harness's own code. Only the OpenAI-compatible wire adapter was replaced by a logging twin of the harness's `openaiModel` that (a) records every request/response verbatim and (b) echoes `reasoning_content` back in history exactly like the harness's managed local-Qwen path (interleaved thinking).
- **Models, run concurrently:**
  - **Qwen3.8-Flash-Next** (RadixArk NVFP4) served locally with SGLang on one RTX PRO 6000 Blackwell, 262,144-token context, FP8 KV, up to 24 concurrent requests sharing one KV pool (no per-request context reduction), model-default sampling. Efforts: `none` (thinking off), `low`, `medium`, `xhigh` — every level the chat template supports.
  - **DeepSeek-V4.1-Flash** through Hugging Face Inference Providers (deepinfra primary; novita/baseten fallback, see `turns[].served_model`), 1M context. Efforts: `none` (thinking off), `low`, `medium`, `high`.
- **No context cutting:** `max_tokens` was 32,768 per turn, the harness transcript budget (640k chars) stops a run gracefully long before 262k tokens, and nothing in the pipeline prunes or summarizes history. `length_stops` counts turns that hit the output limit (such traces are never `accepted`), and `max_context_tokens` is the largest prompt actually sent.
- **Tasks:** synthesized by Qwen3.8-Flash-Next from a curated catalog of ~190 real websites, each prompt grounded on a live excerpt of the site's homepage. Four horizons — `short` (1–4 calls), `medium` (5–12), `long` (12–30) and `very_long` (30–100+ calls; wall-clock budgets 12 / 25 / 50 / 150 min). Three site modes: `read` (live public sites, strictly read-only: search, filter, sort, extract, compare, cross-site verification), `sandbox` (practice sites built for automation — real form filling, demo logins, carts and fake checkouts with obviously fake data) and `tool` (account-free web apps: editors, calculators, games). ~12% of generation prompts request a deliberately under-specified task answered through the harness `ask` tool by a simulated user (`ask_profile`, `ask_events`), and ~14% carry a **follow-up request** run in the same session through the harness `history` path (`followup_task`). The same task is often run by both models and at different efforts, which gives natural comparison pairs (`task_id`).
- **Judging:** every finished run is graded by Qwen3.8-Flash-Next (low effort) on the task, final answer and a clipped trajectory: success, 1–5 score, groundedness, fabrication, blocking, efficiency, failure mode, rationale. `accepted` = harness reported `done` without abort/length stop **and** judge success with score ≥ 4, grounded, not fabricated. The judge is an LLM and makes mistakes; treat it as a filter, not ground truth.
- **Safety rails:** purchases and account creation forbidden on live sites, no real personal data, no posting/messaging/contact forms on public sites; interactive flows only on dedicated practice sites. Text-only runs: when the harness attached a screenshot to a tool result the image was replaced with a one-line note (`images_omitted`).

## Columns

| column | meaning |
|---|---|
| `id`, `task_id` | run id; task id (shared across models/efforts for paired comparisons) |
| `task`, `followup_task`, `tier`, `site_mode`, `category`, `sites`, `task_kind`, `answer_format`, `expected_steps`, `ask_profile` | the task and its metadata |
| `model`, `model_id`, `provider`, `reasoning_effort`, `request_params` | who ran it and with which reasoning controls |
| `harness`, `guardrails`, `system_prompt`, `tools` | the exact harness context (tools is a JSON string of OpenAI tool schemas) |
| `messages` | the **complete OpenAI-format conversation** as last sent to the model plus its final reply: `role`, `content`, `reasoning_content`, `tool_calls[{id,name,arguments}]`, `tool_call_id` |
| `transcript` | the harness-native transcript (JSON string) returned by `runAgentTask` |
| `turns` | per model call: latency, finish reason, prompt/completion/reasoning/cached tokens, serving provider |
| `browser_steps`, `ask_events` | per executed browser snippet (ok, note, url, ms, error); simulated-user Q&A |
| `final_answer`, `success_reported`, `stop_reason`, `aborted`, `num_turns`, `num_tool_calls`, `num_browser_steps`, `wall_seconds`, `final_tabs` | outcome |
| `prompt_tokens_total`, `completion_tokens_total`, `reasoning_tokens_total`, `max_context_tokens`, `length_stops`, `images_omitted`, `model_errors_retried` | telemetry |
| `judge_*`, `accepted` | LLM-judge verdict and the strict acceptance flag |

This release contains the **`accepted`** subset only: runs where the harness reported completion without abort or output-length stop **and** the judge marked them successful (score ≥ 4), grounded and not fabricated. The summary tables above count every completed run (including the rejected ones) so the acceptance rates are visible; rejected runs were not published.

```python
from datasets import load_dataset
ds = load_dataset("ProCreations/betterwright-agent-traces", split="train")
ex = ds[0]
for m in ex["messages"]:
    print(m["role"], (m["reasoning_content"] or "")[:80], (m["content"] or "")[:80], [c["name"] for c in m["tool_calls"]])
```

## Caveats

- Live-web data: pages change, some sites block automation, and answers were true at collection time only (`finished_at`).
- Tasks and judgments are synthetic; a fraction of tasks are impossible as written (the honest "could not" traces are kept, scored ≤ 3).
- Generation was stopped after ~21 h of the planned 48 h window; Qwen3.8-Flash-Next lanes were retired ~3 h before DeepSeek.
- Traces contain public web page text as seen by the agent. No credentials other than the public demo logins of practice sites appear.
- `pipeline/` holds the exact generation code, the task pool and the SGLang arguments for reproducibility.
