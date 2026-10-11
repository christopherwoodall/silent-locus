# NOTES — xbench-deepsearch — SKIPPED (encrypted)

- Source URL: https://huggingface.co/datasets/xbench/DeepSearch/resolve/main/DeepSearch.csv and https://github.com/xbench-ai/xbench-evals (data/DeepSearch-2505.csv, data/DeepSearch-2510.csv)
- Homepage: https://xbench.org
- Eval org: xbench (xbench.org, Alibaba-linked)
- License: mit
- Retrieved: 2026-10-05
- Raw files banked (ENCRYPTED): raw/DeepSearch-2510.csv (100 rows), raw/DeepSearch-2505.csv (100 rows) — byte-identical downloads of the ciphertext
- Banked questions: 0 — plaintext NOT banked, deliberately
- Why skipped: benchmark data is encrypted by design (anti-contamination). Decryption is technically trivial — xbench_evals.py ships a `xor_decrypt` (XOR of base64-decoded prompt/answer with the row's `canary` string as key), stdlib-only, no installs. BUT the repo README states: "you can use the decrypt code in xbench_evals.py to get the plain text data. Please don't upload the plain text online." This collection lives in a repo that pushes to GitHub, so banking decrypted plaintext here would violate the author's explicit request. Encrypted raw is banked for provenance; W3/parent can revisit if the project decides to keep a local-only decrypted copy out of the repo.
- Stretch outcome: attempted, not forced — per brief.
