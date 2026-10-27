---
license: cc-by-4.0
task_categories:
- text-generation
language:
- en
tags:
- computer-use
- gui
- deeplabcut-adjacent
- markov-ai
size_categories:
- 1K<n<10K
---

# computer-use-large-actions

9,000 instruction pairs derived from [`markov-ai/computer-use-large`](https://huggingface.co/datasets/markov-ai/computer-use-large) `descriptions.parquet` (not the raw 12,300 hours of video).

Each row is a 10-second segment whose LLM `description` is a real GUI action (`NO_TASK` dropped). Source license is CC-BY-4.0.

## Split by software

| category | examples |
|---|---|
| vscode | 2,500 |
| autocad | 2,500 |
| blender | 1,000 |
| excel | 1,000 |
| photoshop | 1,000 |
| salesforce | 1,000 |

VS Code and AutoCAD are oversampled for Emmanuel's agentic-coding and DigiCatWalk CAD work.

## Format

`messages` for TRL SFT: system + user (software / tutorial title / ASR transcript) → assistant (one-sentence GUI action).

## What this is not

This is not a click/xy action trace and not a video-VLM dataset. The videos stay on `markov-ai/computer-use-large`. Use those later to add frames at `t0`–`t1` for a vision pass.
