---
license: cc-by-4.0
language:
- en
size_categories:
- n<1K
tags:
- agent-traces
- coding-agent
- hf-agent-trace-viewer
- claude-code
- pi-coding-agent
- ml-intern
- jim-crow-laws
- biglam
pretty_name: Agent Race Traces — same task, multiple harnesses & models
---

# Agent Race Traces

Coding-agent session traces from running the **same task and the same one-line prompt** through multiple harnesses and driver models. Useful for comparing how different agent harnesses + models approach an identical real-world ML task.

**Blog post**: [danielvanstrien.xyz/posts/2026/agent-race](https://danielvanstrien.xyz/posts/2026/agent-race/)

## The task

Fine-tune a model on [`biglam/on_the_books`](https://huggingface.co/datasets/biglam/on_the_books) to identify Jim Crow laws, train via HF Jobs, push the trained model to the Hub.

The exact one-line prompt was given verbatim to every run (only the push-target namespace varies per run).

## Runs

| File | Harness | Driver model | Trained model pushed to |
|---|---|---|---|
| `claude-code.jsonl` | Claude Code | Claude Opus 4.7 | [`davanstrien/jim-crow-laws-claude-code`](https://huggingface.co/davanstrien/jim-crow-laws-claude-code) |
| `pi-kimi.jsonl` | [Pi coding agent](https://github.com/badlogicgames/pi) | [`moonshotai/Kimi-K2.6`](https://huggingface.co/moonshotai/Kimi-K2.6) | [`davanstrien/jim-crow-laws-pi-kimi`](https://huggingface.co/davanstrien/jim-crow-laws-pi-kimi) |
| `ml-intern-claude-opus.jsonl` | [ml-intern](https://github.com/huggingface/ml-intern) | `bedrock/us.anthropic.claude-opus-4-6-v1` | [`davanstrien/jim-crow-laws-ml-agent`](https://huggingface.co/davanstrien/jim-crow-laws-ml-agent) |
| `ml-intern-kimi.jsonl` | [ml-intern](https://github.com/huggingface/ml-intern) | `moonshotai/Kimi-K2.6` | `davanstrien/jim-crow-laws-ml-agent-kimi` |

Three harnesses (Claude Code, Pi, ml-intern), two driver models (Claude Opus, Kimi K2.6), four runs total — lets you disentangle *harness effect* from *model effect* on the same task.

## Format

Each `.jsonl` file is a single agent session converted to a Claude-Code-style event stream — one JSON event per line. Compatible with the Hugging Face [agent-trace viewer](https://huggingface.co/datasets/davanstrien/agent-race-traces) on the Hub (browse the dataset above to see traces rendered).

## Reuse

These traces are useful for:
- Comparing tool-use patterns across harnesses
- Studying how different driver models approach the same real-world ML problem
- Building agent-behaviour datasets and evals
- Reproducing the agent race with a different prompt or model

## Citation

If you use these traces, please cite the blog post:

```
@misc{vanstrien2026agentrace,
  author = {van Strien, Daniel},
  title  = {The Agent Race: Pi+Kimi vs Claude Code on biglam/on_the_books},
  year   = {2026},
  url    = {https://danielvanstrien.xyz/posts/2026/agent-race/}
}
```
