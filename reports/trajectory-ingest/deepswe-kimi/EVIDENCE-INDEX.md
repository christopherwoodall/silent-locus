# DeepSWE Kimi K2 — Evidence Index

## Datasets

| Dataset | Revision | License | Trajectories | Bytes | SHA-256 (JSONL) |
|---|---|---|---|---|---|
| SWE-Factory/DeepSWE-Agent-Kimi-K2-Trajectories-2.8K | 2a2175e291a0606376592af08b64c25afabe72a9 | mit (card-verbatim; API field null) | 2,809 | 237,391,034 | 25a209fccdeda571f79ee50ea5db1798b96a3e1586c86e91484b29c3c8e0081b |
| SWE-Factory/DeepSWE-Agent-Kimi-K2-Trajectories-Rejection-Sampling | 03fc52c28757dbf9f8d47beece97f94f9e69a023 | mit (card-verbatim; API field null) | 729 | 62,139,982 | 56a232a5aeec64b7c1b10ed0c9ebbfd5f12af9ba9ec3b7d38833b5935f9c7a48 |

Raw: data/lanes/deepswe-kimi-trajectories/raw/. Manifest: raw/MANIFEST.json.
License note: raw/LICENSE.note. Per-file .PROVENANCE.txt + .sha256.

## Findings to evidence

| Finding | Trajectory | Steps | Class | Source file | Byte location |
|---|---|---|---|---|---|
| DSK-A-001 | main-10 | 2-42 | OTHER | DeepSWE-Agent-Kimi-K2-Trajectories-2.8K.jsonl | line 10 |
| DSK-A-002 | main-56 | 17-40 | OTHER | DeepSWE-Agent-Kimi-K2-Trajectories-2.8K.jsonl | line 56 |
| DSK-A-003 | main-80 | 3-40 | OTHER | DeepSWE-Agent-Kimi-K2-Trajectories-2.8K.jsonl | line 80 |
| DSK-A-004 | main-230 | 2-41 | OTHER | DeepSWE-Agent-Kimi-K2-Trajectories-2.8K.jsonl | line 230 |
| DSK-A-005 | main-1310 | 26-40 | OTHER | DeepSWE-Agent-Kimi-K2-Trajectories-2.8K.jsonl | line 1310 |
| DSK-A-007 | corpus-wide (2,809) | n/a (aggregate) | GUARDRAIL | DeepSWE-Agent-Kimi-K2-Trajectories-2.8K.jsonl | ID list: working/verifier-a007-testedit-ids.txt (89) |
| DSK-A-008 | main-1308 | 28-30 | TOOL-MISUSE | DeepSWE-Agent-Kimi-K2-Trajectories-2.8K.jsonl | line 1308 |
| DSK-A-009 | main-73 | 18-19 | TOOL-MISUSE | DeepSWE-Agent-Kimi-K2-Trajectories-2.8K.jsonl | line 73 (7 instances corpus-wide) |
| DSK-A-010 | corpus-wide (2,809) | n/a (aggregate) | OTHER | DeepSWE-Agent-Kimi-K2-Trajectories-2.8K.jsonl | ID list: working/verifier-a010-confab-ids.txt (133); census: working/verifier-census.py |
| DSK-B-002 | rs-527 | 23 | GUARDRAIL | rejection-sampling/...-Rejection-Sampling.jsonl | line 527 |
| DSK-B-003 | rs-527 | 18 | OTHER | rejection-sampling/...-Rejection-Sampling.jsonl | line 527 |
| DSK-B-004 | rs-456 | 26-40 | OTHER | rejection-sampling/...-Rejection-Sampling.jsonl | line 456 |
| DSK-B-005 | rs-289 | 27-35 | OTHER | rejection-sampling/...-Rejection-Sampling.jsonl | line 289 |
| DSK-B-006 | rs-272 | 21-22 | TOOL-MISUSE | rejection-sampling/...-Rejection-Sampling.jsonl | line 272 |

Accessible URLs (pinned revisions):

- https://huggingface.co/datasets/SWE-Factory/DeepSWE-Agent-Kimi-K2-Trajectories-2.8K/blob/2a2175e291a0606376592af08b64c25afabe72a9/DeepSWE-Agent-Kimi-K2-Trajectories-2.8K.jsonl
- https://huggingface.co/datasets/SWE-Factory/DeepSWE-Agent-Kimi-K2-Trajectories-Rejection-Sampling/blob/03fc52c28757dbf9f8d47beece97f94f9e69a023/DeepSWE-Agent-Kimi-K2-Trajectories-Rejection-Sampling.jsonl

## Killed

| Candidate | Reason |
|---|---|
| DSK-A-006 (main-2297) | Normal benchmark execution: source changed first, tests followed. |
| DSK-B-001 (rs-153/154) | Wrong trajectory filed; claim inverted — issue demanded the @property removal. |
| 51 reviewer kills | See working/reviewer-A-kills.json, working/reviewer-B-kills.json. |

## Review chain

Scraper -> Reviewer A (main) + Reviewer B (rejection-sampling) ->
adversarial reviewer -> byte verifier (all 14 survivors re-checked,
step ranges and trajectory ids corrected, censuses independently
re-derived) -> ingestor. Verified findings:
working/verified-findings.json. Kills: working/verifier-kills.json.

## Factum

Lane tag: deepswe-kimi-trajectories. Bundle: 77 records (2 source,
2 snapshot, 2 artifact, 1 run, 14 dataset.record, 14
intel.behavior, 14 behavior.tool_sequence, 28 edges). Idempotency
key: deepswe-kimi-ingest-2026-10-16-v1. Batch id to be recorded on
export.
