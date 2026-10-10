# Provenance — deepsearchqa lane

## Upstream source

- HuggingFace dataset `google/deepsearchqa`, pinned revision
  `b2623f8653065c2672de6d941fc5434cd652376c`.
- License: Apache-2.0. Repo last_modified: 2025-12-17T21:41:32+00:00.
- Pulled 2026-10-01 via `build.sh` (HF CLI, pinned revision). Raw bytes:
  `hf_raw/DSQA-full.csv` (+ dataset README, `.gitattributes`).
- Full acquisition detail: `provenance.md` (legacy doc, moved with the lane).

## Factum ingest (2026-10-09)

- Actor: `agent:lane-ingest-2026-10-01-deepsearchqa`.
- Idempotency key: `deepsearchqa-ingest-2026-10-09`.
- 903 records in one bundle (batch `1af9855077ba4892a036ea30d0ba9c08`):
  1 source, 1 artifact, 1 `dataset.snapshot`
  (`observation_5b356f1ea59f409a830244b102a00991`), 900 `dataset.record`
  (`dsqa_0` .. `dsqa_899`), plus `in_lane` edges from the bundle-level lane.
- Verbatim chain verified pre-submit (cleaner): `hf_raw/DSQA-full.csv`
  `problem` == `questions.jsonl` `problem` == `events.jsonl` `description`
  for all 900 rows, byte-identical.
- Corpus dedup pre-submit: fuzzy `match` for `deepsearchqa`, `dsqa_250`,
  `civilrightsdata.ed.gov` — no existing question records found. Batch-internal
  dedup by question id (all 900 unique).
- Question text is preserved twice: verbatim in the git-kept artifact
  (`events.jsonl`, row-addressed) and verbatim in each record's
  `tags["question.text"]`.
- Time basis: `legacy_documented`. The dataset carries no per-question dates.
  `observed_at` is the documented pull date (2026-10-01). No timestamps were
  invented.
