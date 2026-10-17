# Evidence index — nvidia-baseline-trajectories

All paths are relative to `~/workspace/silent-locus/`.

## Lane working directory (committed, text only)

- `data/lanes/nvidia-baseline-trajectories/SAMPLING-PLAN.md`
  Sampling method, shard indices, byte/row totals, revisions,
  retrieval notes, limitations.
- `data/lanes/nvidia-baseline-trajectories/BASELINE-CHARACTERIZATION.md`
  Measured baseline: distributions, invariants, tool mix, quirks.
- `data/lanes/nvidia-baseline-trajectories/REVIEW-FINDINGS.md`
  Review coverage log and the kill list with evidence references.
- `data/lanes/nvidia-baseline-trajectories/VERIFICATION.md`
  Per-claim verification table, 10 kills with reasons, ingest-approved
  claim list.
- `data/lanes/nvidia-baseline-trajectories/manifest.json`
  Per-file source URL, size, sha256, revision, sampling metadata.
- `data/lanes/nvidia-baseline-trajectories/raw/` — LOCAL ONLY, not
  committed. 13 parquet files (2.264 GB) + 17 `.PROVENANCE.txt`
  sidecars (source_url, retrieved_at, retrieval_method, sha256,
  dataset_revision).

## Factum lane directory (committed)

- `data/lanes/2026-10-16-nvidia-baseline-trajectories-8f1380d7/`
  `lane.json`, `README.md`, `FINDINGS.md`, `PROVENANCE.md`.
  Lane ID `lane_fc9d75a8d8534dd8b4e44a368f1380d7`, kind `baseline`.
  `docs_path` tag points at `data/lanes/nvidia-baseline-trajectories/`.

## Factum batch (committed)

- `data/records/6945c13d701041209ae7800ec0ec2953/`
  `records.jsonl` (157.4 MB, 78,558 records), `manifest.json`.
  Export exit 0, verify exit 0.

## Report directory (this directory)

- `REPORT.md` — ingest report (ASD-STE100).
- `EVIDENCE-INDEX.md` — this file.
- `SAMPLING-PLAN.md` — copy of the lane sampling plan.
- `BASELINE-CHARACTERIZATION.md` — copy of the measured baseline.

## Pipeline

- `scripts/trajectory-pipeline-README.md` — pipeline doc, now with
  baseline-corpus notes.
- `scripts/trajectory-scout.py` — inventory tool (unchanged).
- `scripts/trajectory-review-prompts.md` — reviewer prompt pack
  (unchanged).
