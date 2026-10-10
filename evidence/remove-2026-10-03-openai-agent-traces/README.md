# remove-2026-10-03-openai-agent-traces (ingested)

This lane was aggregated into Factum as lane `openai-agent-traces` on
2026-10-10 (commit pending — see `data/lanes/openai-agent-traces/`).

- 589,972 traces too large for per-trace ingest; stored as census
  rollups: 1 corpus + 10 per-slug `dataset.snapshot` observations.
- 1 `source` record, 1 `run` record, 6 graded `claim` records.
- 19 records total in `hidden_files/factum-batches/openai-agent-traces/bundle.json`.

All artifacts (legacy-PROVENANCE.md, SHA256SUMS, events.jsonl, raw/)
moved to data/lanes/openai-agent-traces/. This directory is safe for
later removal.
