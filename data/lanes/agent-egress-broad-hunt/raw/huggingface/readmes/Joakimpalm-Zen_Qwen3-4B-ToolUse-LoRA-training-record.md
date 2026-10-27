---
license: apache-2.0
pretty_name: "Qwen3-4B tool-use LoRA: training data, evals and the three-precision study"
size_categories:
- n<1K
tags:
- lora
- tool-calling
- function-calling
- reproducible-training
- merge-erasure
- evidence
- xyntetik-runner
viewer: false
---

# Qwen3-4B tool-use LoRA: training record, held-out evals and the merge study

<!-- BEGIN xyntetik-dataset-summary -->
> **Research evidence dataset.** No model weights. Part of the collection
> *Xyntetik Research: LoRA Training on Quantized Weights* on this account, produced with
> [Xyntetik Runner](https://github.com/Joakimpalm-Zen/xyntetik-runner).

## Dataset summary

**Question tested.** Whether a LoRA trained directly through the quantized GGUF that serves it (no FP16 training copy) reaches exact tool-call agreement on a held-out set, whether the result is byte-reproducible, and what merging the adapter into a 4-bit file does to it.

**Models involved.**
- The adapter and merged weights: https://huggingface.co/Joakimpalm-Zen/Qwen3-4B-Runner-ToolUse-Q4_K_M
- Base: `Qwen/Qwen3-4B` at Q4_K_M (sha256 `fbe1d5ed...`), plus the Q8_0 and bf16 study arms

**Method.** Runner's `--train` (AdamW LoRA, rank 8, alpha 16, lr 1e-4, 316 steps, ctx 128, seed 0) on a deterministic generated dataset; a 29-prompt held-out eval scored on JSON parse, right tool, schema-shaped args and exact call; the same adapter trained through bf16, Q8_0 and Q4_K_M weights and compared in weight space and by logprob; the adapter merged to F16, Q8_0, Q4_K_M and re-evaluated; a served-vs-merged scale sweep.

**What each file contains.**
- `data/train.jsonl`, `data/eval.jsonl`: the deterministic training set and the held-out eval prompts (sha256 of the training set is in the train record)
- `Qwen3-4B-ToolUse-LoRA.gguf.train.json`: the machine-written training provenance record (schema `xyntetik.runner.train.v1`)
- `Qwen3-4B-ToolUse-LoRA.gguf.envelope.json`: the adapter's measured-envelope manifest
- `evals/eval-base-q4.json`, `evals/eval-adapted-q4.json`: the headline before/after eval; `evals/eval-cross-*.json`, `evals/eval-study-*.json`: cross-precision evals; `evals/merged-*.json`: evals after merging to F16, Q8_0, Q4_K_M; `evals/sweep-s*-{served,merged}.json`: the adapter-scale sweep; `evals/llamacpp-served-adapter.json`: the same adapter served by llama.cpp
- `evals/logprob-study/`: per-prompt logprob scores of the base and the three study adapters
- `study/*.train.json`: provenance records of the three study adapters; `study/divergence.jsonl`: their pairwise weight-space cosine and relative L2
- `merged/*.merge.json`: the merge receipts
- `assets/`: the two figures used on the model card

**Reproduction.** `python3 scripts/make-tooluse-data.py data/` then `runner --train` as on the model card; the record file is what the run writes, and re-running reproduces the adapter sha for sha.

**Result.** Base Q4_K_M scores 0.690 exact-call on the held-out set, the adapter 1.000; merging to F16 or Q8_0 keeps 1.00, merging to Q4_0 returns the base model's 0.69 (the adaptation is erased). The three precision arms learn measurably different adapters (12% relative divergence bf16 vs Q4_K_M).

**Links.**
- Model repository: https://huggingface.co/Joakimpalm-Zen/Qwen3-4B-Runner-ToolUse-Q4_K_M
- Runner: https://github.com/Joakimpalm-Zen/xyntetik-runner
- Runner docs: https://github.com/Joakimpalm-Zen/xyntetik-runner/blob/main/docs/train-lora-on-quantized-gguf.md
<!-- END xyntetik-dataset-summary -->

The adapter weights (`Qwen3-4B-ToolUse-LoRA.gguf`), the merged Q8_0 and the three study adapters stay in the model repository; this dataset holds the data, records and evaluations, unchanged from their copies there.

<!-- xyntetik-program -->
## About Xyntetik

This repository is published by [Xyntetik](https://xyntetik.com), the Zenova AB program for running capable language models on hardware you own and proving what they did. Its released engine is [Xyntetik Runner](https://github.com/Joakimpalm-Zen/xyntetik-runner): a free, single-binary GGUF engine in C for CPU, CUDA and Metal that serves, scores and trains through the quantized file it deploys and records every run as a receipt. The measurements behind the program's claims are collected at [xyntetik.com/evidence](https://xyntetik.com/evidence/). The program's organization on Hugging Face is [Xyntetik](https://huggingface.co/Xyntetik).
