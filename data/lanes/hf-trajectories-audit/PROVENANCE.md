# Provenance — hf-trajectories-audit

Cite Factum records here.

## Source documents
- `evidence/hf-trajectories/RANKED-HITS.md` — ranked hit list, written 2026-10-07.
- `evidence/hf-trajectories/<slug>/AUDIT.md` — 10 per-dataset audit docs, 2026-10-07.

## Audit method
Row-group streaming scan (`scripts/rg_scan.py`) of all text columns in parquet
shards, plus per-file text scans of jsonl/json. Sharp-pattern plus
challenge-solved plus marker-grammar regexes. Every distinct hit was
byte-verified with full step context. A flag set by template default is not a
defeat: the audit required actual challenge-solving steps and successful
fetches. Grades: CLEAN / DOCUMENTED (defeat or technique already reported
elsewhere, with citation) / NEW DEFEAT (unreported, byte-verified).

## Datasets audited
| dataset | coverage in audit |
|---|---|
| yoonholee/terminalbench-trajectories | complete (2 parquet shards, ~52K rows) |
| Hcompany/trajectories | partial (P2 sample: 50 of 7,368 files) |
| 0xSero/glm-5.2-nf3-hybrid-terminal-bench-2.1-traces | complete (863 files) |
| TIGER-Lab/BrowserAgent-Data | complete (16,804 rows) |
| DJLougen/hermes-agent-traces-filtered | complete (3,679 traces) |
| TIGER-Lab/SWE-Next-SFT-Trajectories | complete (2,473 rows) |
| Crownelius/GPT-5.6-Sol-Luna-Terra-Traces | complete (15,353 rows) |
| TIGER-Lab/SWE-QA-Pro-SFT-Trajectories | complete (1,000 rows) |
| TIGER-Lab/BrowserAgent-SeedData | complete (10 parquets, ~242K rows) |
| aisa-group/ResearchArena-Trajectories | partial (P2 sample, 13 files of ~6.2 GB repo) |

## Raw data
Cached under `evidence/hf-trajectories/raw/<slug>/` with per-dataset
PROVENANCE.md. Total ~943 MB parquet. Not moved into Factum blobs: the
verdict records reference the legacy path.

## Time basis
All observation times use the documented audit date 2026-10-07
(`time_basis: legacy_documented`). No finer time is in the source.
