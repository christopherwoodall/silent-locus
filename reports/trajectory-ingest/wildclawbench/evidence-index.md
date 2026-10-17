# WildClawBench — Evidence Index

Lane: `wildclawbench-trajectories`. All paths are repo-relative to
`~/workspace/silent-locus`.

## Raw capture

- `data/lanes/wildclawbench-trajectories/raw/manifest.json` — the 918-file
  scrape manifest (URL, retrieved_at, method, sha256, bytes per file).
- `data/lanes/wildclawbench-trajectories/raw/sessions/` — 600 per-task
  trajectory JSONL files, 10 model dirs (`claude_fable5`,
  `claude_opus_4_8_thinking`, `glm52`, `gpt56_sol`, `grok45`, `hy3`,
  `intern-s2-preview-397b`, `kimi_k2.7_code`, `kimi_k3`, `muse_spark_1_1`).
- `data/lanes/wildclawbench-trajectories/raw/docs/context/` — Harbor grader
  context files.
- `data/lanes/wildclawbench-trajectories/raw/docs/fork_logs/` — Ethara-Ai
  fork run logs (evidence for WCB-RC-010).
- `data/lanes/wildclawbench-trajectories/raw/repo/` — GitHub repo clone.
- `data/lanes/wildclawbench-trajectories/raw/parquet/` — 2 parquet files.

## Review

- `data/lanes/wildclawbench-trajectories/review/reviewer-A-findings.jsonl`
  — 7 filed (RA-001..RA-007).
- `data/lanes/wildclawbench-trajectories/review/reviewer-B-findings.jsonl`
  — 12 filed (RB-001..RB-012).
- `data/lanes/wildclawbench-trajectories/review/reviewer-C-findings.jsonl`
  — 10 filed (RC-001..RC-010).
- `data/lanes/wildclawbench-trajectories/review/surviving-findings.jsonl`
  — the 26 canonical survivors (verifier's version; authoritative).
- `data/lanes/wildclawbench-trajectories/review/verifier-kills.jsonl`
  — empty (0 kills).
- `data/lanes/wildclawbench-trajectories/review/edge-scheme.md` — the
  linked-record edge scheme.

## Bundle and batch

- `data/lanes/wildclawbench-trajectories/build_bundle.py` — the bundle
  builder (regenerates `bundle.json` from `review/surviving-findings.jsonl`
  plus cached session bytes; edge fix applied 2026-10-16).
- `data/lanes/wildclawbench-trajectories/bundle.json` — the submitted
  bundle (219 records).
- `data/records/1762402022fc4d028d27c82fd92f8fc0/` — the exported,
  verified, committed batch (`records.jsonl`, `manifest.json`).
- Commit `b7d600d2` on branch `work` (not pushed).

## Report

- `reports/trajectory-ingest/wildclawbench/REPORT.md` — this lane's report
  (ASD-STE100).
- `reports/trajectory-ingest/wildclawbench/evidence-index.md` — this file.
