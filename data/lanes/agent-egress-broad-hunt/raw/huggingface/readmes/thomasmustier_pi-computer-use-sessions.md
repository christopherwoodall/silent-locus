---
pretty_name: coding agent session traces
task_categories:
- text-generation
tags:
- agent-traces
- coding-agent
- pi-share-hf
language:
- en
- code
license: mit
---

# Coding agent session traces for thomasmustier/pi-computer-use-sessions

This dataset contains redacted coding agent session traces collected while working on https://github.com/tmustier/pi-computer-use. The traces were exported with [pi-share-hf](https://github.com/badlogic/pi-share-hf) from local [pi](https://pi.dev) workspaces and filtered to keep only sessions that passed deterministic redaction, secret scanning, visual review where applicable, and LLM review.

Source git repo: https://github.com/tmustier/pi-computer-use

## Data description

Each `*.jsonl` file is a redacted pi session. Sessions are stored as JSON Lines files where each line is a structured session entry. Entries can include session headers, user and assistant messages, tool calls/results, model changes, thinking level changes, branch summaries, compaction summaries, and custom extension data.

Pi session files are tree-structured via `id` and `parentId`. See the current session format documentation:

- https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/session-format.md

## Redaction and review

The data was processed with deterministic redaction plus TruffleHog secret scanning and LLM review. Deterministic redaction targets exact known secrets, PII, private routing markers, and curated credential patterns. The LLM review decides whether a session is about the OSS project, whether it is fit to share publicly, and whether sensitive content appears to have been missed.

Embedded images may be preserved where they passed manual/LLM review.

## Limitations

This dataset is best-effort redacted. Coding agent transcripts can still contain sensitive or off-topic content, especially if a session mixed OSS work with unrelated private tasks. Use with appropriate caution.

Initial upload in this dataset: 6 session(s).
