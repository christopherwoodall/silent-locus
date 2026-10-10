# DeepSearchQA benchmark question set (google/deepsearchqa)

## What this lane is

DeepSearchQA is a benchmark of 900 hand-made questions. Each question needs
many search steps to answer. The set is used to test deep-research agents.

This lane stores the full question set as Factum records. It also stores the
task-family JOIN KEY map (see `join_keys.md`). A JOIN KEY is a distinctive
string in a question (a domain, a query parameter) that links the question to
a real incident.

## Why this lane matters for the hunt

DeepSearchQA is the best fingerprint source in the sibling benchmarks.
The 900 questions are plain text. They contain rare entities. Example:
`civilrightsdata.ed.gov` in dsqa_250 links to the confirmed Department of
Education incident (Transluce us-canada-gov). See `join_keys.md` and
`FINDINGS.md`.

## Factum records

- 1 `dataset.snapshot` — the pinned HF revision, full coverage, 900 rows.
  ID: `observation_5b356f1ea59f409a830244b102a00991`.
- 1 `source` — `https://huggingface.co/datasets/google/deepsearchqa`.
- 1 `artifact` — `data/lanes/deepsearchqa/events.jsonl` (git-kept).
- 900 `dataset.record` — one per question, IDs `dsqa_0` .. `dsqa_899`.
  Each record points at its row in the artifact. Each record carries the full
  question text verbatim in `tags["question.text"]`, plus category and answer
  type.
- All records carry `{"lane": "deepsearchqa"}`. Lane edges (`in_lane`) link
  each record to this lane.

## Files in this directory

- `events.jsonl` — 900 `benchmark_question` legacy events (verbatim source
  for the Factum records).
- `questions.jsonl` — 900 questions (`id`, `problem`, `category`, `answer`,
  `answer_type`).
- `hf_raw/` — raw pull of `google/deepsearchqa` at the pinned revision
  (`DSQA-full.csv`, dataset README, `.gitattributes`).
- `provenance.md` — acquisition provenance (legacy doc).
- `PROVENANCE.md` — Factum ingest provenance.
- `join_keys.md` — question ID to incident JOIN KEY map (the hunt payload).
- `sibling_benchmarks.md` — sibling benchmark leads (not deep-pulled).
- `build.sh`, `build_events.py` — reproducible build scripts.
- `lane.json` — Factum lane record.
