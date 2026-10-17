# TELBench — Evidence Index

Lane: `telbench-trajectories`. All paths are repository-relative
to `~/workspace/silent-locus/`.

## Raw dataset

`data/lanes/telbench-trajectories/raw/`:

| File | Bytes | SHA-256 (short) | Note |
|---|---|---|---|
| `TELBench.jsonl.enc` | 20,230,368 | `f21caccb…4afa1dc1` | Encrypted source file |
| `TELBench.jsonl` | 20,230,340 | `9f10b1cb…a21082` | Decrypted, verified |
| `TELBench.jsonl.enc.sha256` | 85 | — | Upstream checksum |
| `TELBench.jsonl.sha256` | 81 | — | Upstream checksum |
| `TELBench.passphrase.txt` | 45 | — | Public passphrase |
| `*.PROVENANCE.txt` | — | — | One per file: source URL, retrieval time, method, SHA-256, dataset revision |

Dataset revision: `307d870d7424be265653bb7a566793cc217105be`.
License: Apache-2.0.

## Reviewer outputs

| File | Content |
|---|---|
| `data/lanes/telbench-trajectories/review-a-findings.json` | 6 findings, records 1–500 |
| `data/lanes/telbench-trajectories/review-b-findings.json` | 11 findings, records 501–1000 |
| `data/lanes/telbench-trajectories/verified-findings.json` | 17 verdicts with corrections; B-001 flagged for adjudication |

## Factum batch

- `data/records/271cd986f6c54195ae4ef28341fe6bbd/` — 115 records.
- Commit `0c2836a2` on branch `work`.

## Report

- `reports/trajectory-ingest/telbench/REPORT.md` — this lane's
  report.
- `reports/trajectory-ingest/telbench/EVIDENCE-INDEX.md` —
  this file.
