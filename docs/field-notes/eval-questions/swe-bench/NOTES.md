# NOTES — swe-bench — WRONG SHAPE (raw only)

- Source URL: https://huggingface.co/datasets/princeton-nlp/SWE-bench
- Homepage: https://www.swebench.com/
- Eval org: Academic (Princeton)
- License: MIT
- Retrieved: 2026-10-05
- Raw files: raw/dev-00000-of-00001.parquet, raw/test-00000-of-00001.parquet, raw/train-00000-of-00001.parquet (byte-identical)
- Banked questions: n/a — excluded from questions.jsonl by design
- Why excluded: wrong shape — SWE-bench tasks are code-generation GitHub-issue instances (problem_statement + repo + fix patch), not web-search/agent-trace questions. Banked raw for completeness only.
