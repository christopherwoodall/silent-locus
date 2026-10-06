# NOTES — assistantbench

- Source URL: https://huggingface.co/datasets/AssistantBench/AssistantBench/resolve/main/assistant_bench_v1.0_test.jsonl
- Homepage: https://assistantbench.github.io/
- Eval org: Academic (Yoran et al.)
- License: apache-2.0
- Retrieved: 2026-10-05
- Raw file: raw/assistant_bench_v1.0_test.jsonl (byte-identical)
- Banked questions: 181 / expected 214 (paper) — MISMATCH (-15.4%, flagged)
- Discrepancy investigation: the public test file genuinely contains 181 records — verified independently via the HuggingFace datasets-server parquet conversion (resolve/refs%2Fconvert%2Fparquet/default/test/0000.parquet), whose footer reports num_rows=181. The paper's 214 = test (181) + dev/validation (33, verified via the validation parquet conversion). Only the test split was banked per brief; the dev file (assistant_bench_v1.0_dev.jsonl) is also public.
- Included: yes — realistic time-consuming web-agent tasks
- Normalization: one JSON object per line; question_id = source `id` (hex string); question = `task`; topic = `difficulty` (null in this release → '').
