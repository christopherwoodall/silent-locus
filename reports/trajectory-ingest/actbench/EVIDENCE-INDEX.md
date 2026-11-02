# ActBench — evidence index

## Dataset

- HF: ZJUICSR/ActBench, revision f6bf788ea6b182300950e318c0caa0d52de2750f, MIT.
- Local: `data/lanes/actbench-trajectories/raw/` (1.23 GB, local-only).
  - `raw/task_pairs/test-00000-of-00001.parquet` — 300 rows / 600 cases, 15 behavior types.
  - `raw/trajectories/<backend>__<model>.parquet` — 20 files x 1,200 rows = 24,000 trajectories.
  - Each file has `.PROVENANCE.txt` (URL, retrieval time/method, SHA-256).
- Manifest: `data/lanes/actbench-trajectories/MANIFEST.json`.

## Reviews

- `data/lanes/actbench-trajectories/review/reviewer-A-benign-findings.md` — benign split (6,000 rows), 4 findings.
- `data/lanes/actbench-trajectories/review/reviewer-B-attack1-findings.md` — attack files 1-10 (9,000 rows), 21 candidates.
- `data/lanes/actbench-trajectories/review/reviewer-C-attack2-findings.md` — attack files 11-20 (9,000 rows), 18 findings.
- `data/lanes/actbench-trajectories/review/reviewer-D-taxonomy-matrix.md` — taxonomy + coverage matrix, 21 findings + aggregate.
- `data/lanes/actbench-trajectories/review/VERIFIED-findings.md` — adversarial verification: 50 survive, 8 killed, 6 merged.

## Build

- `data/lanes/actbench-trajectories/working/assemble.cjs` — bundle assembler (Node port).
- `data/lanes/actbench-trajectories/working/findings.py` — verified findings table (source of truth).
- `data/lanes/actbench-trajectories/working/parse_findings.cjs` — findings.py parser.
- `data/lanes/actbench-trajectories/working/BUILD-NOTES.md` — build documentation.
- `data/lanes/actbench-trajectories/working/chunks/` — 20 extraction JSONL (138 MB, local-only).
- `data/lanes/actbench-trajectories/working/bundle-actbench.json` — factum bundle (~150 MB, local-only).

## Report

- `reports/trajectory-ingest/actbench/REPORT.md` — findings, killed, coverage, edge schema.
