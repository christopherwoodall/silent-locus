# Evidence index — LongRCA ingest 2026-10-16

## Inputs (producer)

- `data/lanes/longrca-trajectories/raw/MANIFEST.json` — manifest:
  dataset CLoud5-real/longrca-bench, revision
  9f45acb66948d5d20c663b4ce4ec8ea5ab0076dd, complete: true, 1,140
  files. Gitignored (local-only byte store).
- `data/lanes/longrca-trajectories/raw/<benchmark>/<qid>.json` —
  1,140 raw trajectory files + .PROVENANCE.txt sidecars per file.
  Gitignored (local-only).
- `data/lanes/longrca-trajectories/verified-findings.json` — 30
  verifier-confirmed findings (all bytes-confirmed), PRIMARY grade.
- `data/lanes/longrca-trajectories/kill-list.json` — 1 kill: F-A15.
- `data/lanes/longrca-trajectories/reviewer-a-findings.json`,
  `reviewer-b-findings.json` — per-reviewer finding sets (F-A* and
  LB-F* passes).

## Build products

- `data/lanes/longrca-trajectories/build_factum_bundle.py` — bundle
  builder. Emits bundle-longrca.json (3,483 records) + build-report.json.
- `data/lanes/longrca-trajectories/bundle-longrca.json` — the
  submitted bundle. Idempotency key longrca-ingest-2026-10-16-v1.
  Bundle sha256 8652206724c7914bdffb959e14e894225d9a1aae58d90e6377dfbad234cb9239.
- `data/lanes/longrca-trajectories/build-report.json` — build stats:
  1,140 trajectories, 30 findings, 238,242,050 bytes.
- `data/lanes/longrca-trajectories/dedup_check.py` — pre-ingest
  dedup: authoritative data/records/ scan for dataset id + lane name
  + all 1,140 question_IDs, plus fuzzy match probes. Result: 0
  overlaps.
- `data/lanes/longrca-trajectories/validate_batch.py` — batch
  validator run directly on the exported batch files (no DB locks):
  6,966 records, 0 errors, 0 warnings.

## Factum records

- Batch: `data/records/bbab7554189943ca94522cf5fb138faa/`
  (records.jsonl + manifest.json with receipt).
- Record counts by kind: source 1, run 1, observation 1,171
  (dataset.record 1,140 + dataset.snapshot 1 + intel.behavior 30),
  artifact 1,140, edge 4,653 (1,140 related_to run->trajectory + 30
  supports finding->trajectory + 3,483 auto in_lane). Total 6,966.
- Lane: `data/lanes/longrca-trajectories/` (lane.json; docs_path =
  data/lanes/longrca-trajectories/). Legacy lane dir
  data/lanes/2026-10-16-longrca-trajectories-956a3eca/ merged into it.
- Every record carries tags.lane="longrca-trajectories".

## Report

- `reports/trajectory-ingest/longrca/REPORT.md` — full ingest
  report (this run): Purpose, Sources, Method, Findings by class
  (30 PRIMARY), Killed (1), Overlap (0), Open questions (5).
