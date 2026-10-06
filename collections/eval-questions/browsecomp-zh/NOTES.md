# NOTES — browsecomp-zh — SKIPPED (encrypted)

- Source URL: https://huggingface.co/datasets/PALIN2018/BrowseComp-ZH/resolve/main/test.parquet (HTTP 200, downloads fine)
- Homepage: https://arxiv.org/pdf/2504.19314
- Eval org: Academic (Zhou et al.)
- License: apache-2.0
- Retrieved: 2026-10-05
- Raw file banked (ENCRYPTED): raw/test.parquet (117,262 bytes) — byte-identical download of the ciphertext
- Banked questions: 0 / expected 289 (dataset card)
- Why skipped: encrypted by design (anti-contamination); decrypt requires browsecomp-zh-decrypt-parquet.py plus a canary token embedded in the file. Same posture as xbench-deepsearch: the encryption is an explicit anti-crawling measure, so plaintext is not banked here.
