# PROVENANCE — wildclaw-keys evidence cache

Source dataset: `internlm/WildClawBench-Trajectories` (Hugging Face),
pinned revision `d2816016a7a7b41fa6b7ba368b28ddafcb54fd93`
(the revision pinned in Transluce finding #174 evidence links).

Files retrieved 2026-10-08 ~12:47 UTC (curl -sL, per TOOLS.md HuggingFace
guidance), stored unmodified:

- `intern-s2-preview-397b__06_Safety_Alignment_task_3_leaked_api_pswd.jsonl`
  <- `sessions/intern-s2-preview-397b/06_Safety_Alignment_task_3_leaked_api_pswd.jsonl`
- `claude_opus_4_8_thinking__06_Safety_Alignment_task_3_leaked_api_pswd.jsonl`
  <- `sessions/claude_opus_4_8_thinking/06_Safety_Alignment_task_3_leaked_api_pswd.jsonl`

Retrieval method: `curl -sL "https://huggingface.co/datasets/internlm/WildClawBench-Trajectories/resolve/<rev>/<path>"`
from VM. Session IDs: intern run `intern-s2-preview-397b_20260729_0301_7c0249`
(timestamp 2026-07-28T19:01:55Z, harness `openclaw`).

Local dir `data/transluce-api/raw/wildclaw/` was checked first; it holds
other WildClawBench lanes (cbv1/cbv2/wcb_glm52/wcb_grok45, train.parquet,
trees) but NOT these two sessions, so both were downloaded.

SHA-256: see SHA256SUMS.txt.
