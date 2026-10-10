# Ingested into Factum — safe for later removal

Lane `deepsearchqa` (DeepSearchQA benchmark question set, `google/deepsearchqa`
pinned at `b2623f8653065c2672de6d941fc5434cd652376c`, 900 questions, collected
2026-10-01) has been ingested into Factum.

- Lane artifacts (provenance.md, join_keys.md, sibling_benchmarks.md,
  events.jsonl, questions.jsonl, build.sh, build_events.py, hf_raw/): moved to
  `data/lanes/deepsearchqa/`
- Factum records: 1 dataset.snapshot + 1 source + 1 artifact + 900
  dataset.record (one per question, ids dsqa_0..dsqa_899), all tagged
  `{"lane": "deepsearchqa"}`
- Ingest actor: `agent:lane-ingest-2026-10-01-deepsearchqa`

This directory is a tombstone only. The contents above were moved, not
copied. Do not re-ingest.
