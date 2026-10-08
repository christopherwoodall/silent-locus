---
license: mit
task_categories:
- other
tags:
- terminal-bench
- agent-traces
- llm-agents
- benchmark
- glm
pretty_name: GLM-5.2 NF3-Hybrid — Terminal-Bench 2.1 Traces
---

# GLM-5.2 (MXFP8-NVFP4-NF3-Hybrid) — Terminal-Bench 2.1 agent traces

Full agent traces from running **Terminal-Bench 2.1** (89 tasks) against a self-hosted
**GLM-5.2** in a `MXFP8-NVFP4-NF3-Hybrid` quantization, using the **Terminus-2** agent
via Harbor.

## Configuration

| | |
|---|---|
| Model | GLM-5.2 · MXFP8-NVFP4-NF3-Hybrid (753B MoE) |
| Agent | Terminus-2 |
| Reasoning effort | max |
| Context | 262,144 tokens |
| Concurrency | 2 |
| Attempts / task | 1 (`k=1`) |
| Serving | vLLM, tensor-parallel 4 + decode-context-parallel 4, MTP speculative decoding, FP8 KV |

## Results

| Metric | Value |
|---|---|
| Passed | 63 / 89 |
| Raw accuracy | **70.8%** |
| Genuine model accuracy | **77.8%** (63 / 81, excluding infrastructure/harness artifacts) |
| Genuine model failures | 18 |
| Invalid (infra/harness) | 8 |

`results_summary.json` holds the full per-task classification (`pass` / `fail` / `invalid`).

### On the "invalid" category

8 tasks scored 0 for reasons unrelated to model capability, verified by a per-task audit:
a headless Chromium that couldn't boot on the grader CPU, a flaky test whose SIGINT raced
interpreter startup, verifier timeouts, and 5 "wedge" tasks where `reasoning_effort:max`
turns (thousands of tokens each) overran a 30-minute watchdog under shared-GPU contention.
Timing forensics showed these are a throughput/timeout artifact, **not** a context-length
or reasoning limit — the model solves them given a dedicated stream and a longer timeout.

## Structure

```
traces/<task>__<id>/
  result.json              # outcome + timing + (any) exception info
  config.json              # per-trial agent/model config (endpoint redacted)
  agent/trajectory.json    # full ATIF trajectory: every message, reasoning, tool call, observation
  verifier/                # ctrf.json, test-stdout.txt, reward.txt
results_summary.json       # per-task pass/fail/invalid + scores
```

## Privacy

The serving endpoint hostname, tailnet addresses, and API key have been redacted
(`REDACTED-ENDPOINT`, `REDACTED-API-KEY`). No credentials or private infrastructure
identifiers are present.

## Acknowledgements

- Observations collected from **GLM-5.2 NF3-Hybrid** during REAP expert-pruning runs.
- [zai-org/GLM-5.2](https://huggingface.co/zai-org) for the upstream base model.
- [Cerebras Research](https://github.com/CerebrasResearch/reap) for the REAP method. Terminal-Bench 2.1 trace artifacts.

