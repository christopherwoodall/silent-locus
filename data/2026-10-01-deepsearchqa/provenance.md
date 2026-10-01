# Provenance — 2026-10-01-deepsearchqa

| field | value |
|---|---|
| Source | HuggingFace dataset `google/deepsearchqa` |
| Pinned revision (commit sha) | `b2623f8653065c2672de6d941fc5434cd652376c` |
| Repo last_modified (HF metadata) | 2025-12-17T21:41:32+00:00 |
| License | Apache-2.0 |
| Pull date | 2026-10-01 |
| Question count | **900** (single `eval` split, `DSQA-full.csv`) |
| Raw artifacts in dir | `hf_raw/DSQA-full.csv`, `hf_raw/README.md`, `hf_raw/.gitattributes` |
| Derived | `questions.jsonl` (one JSON object per question; `id` = `dsqa_<0-based row index>`) |
| Build script | `build.sh` (single-collection script in event dir, per 2026-09-29 convention) |

## ID convention (verified, not invented)

DeepSearchQA's public material refers to tasks as `dsqa_NNN`. Cross-checking against
Transluce's explicit quote of **dsqa_250** (the civilrightsdata.ed.gov
counselor-ratio question) confirms the ID is the **0-based row index** of the
question in `DSQA-full.csv`: row 250's text matches Transluce's quoted text
verbatim (punctuation aside). All `dsqa_NNN` IDs in this event are assigned by
that rule.

## Question set shape

- 900 questions, 17 categories (Politics & Government 148, Finance & Economics 132,
  Geography 95, Education 94, Health 92, Science 90, Other 65, History 44,
  Travel 36, Media & Entertainment 29, Arts 26, Technology 22, Sports 20,
  Current Events 3, Biology 2, Linguistics 1, Arts & Entertainment 1).
- answer_type: 584 Set Answer / 316 Single Answer. (Dataset card: answer_type must
  NOT be shown to the agent at inference time.)
- Card states tasks are hand-crafted causal-chain multi-step info-seeking tasks;
  paper/leaderboard linked in README.

## Temporal metadata available (steering 2026-10-01)

- No per-question added/relevant dates exist in the dataset or its card. Timing
  evidence is limited to: repo last_modified 2025-12-17, pinned commit sha above,
  and per-question reference windows embedded in question text (e.g. 2017–2018,
  1990–2020). There is no dataset version history to align against incident
  burst timing beyond "dataset predates incidents".
