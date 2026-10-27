# Provenance — Cohere Qwen enrichment corpus copies

Fetched 2026-10-27T05:32:27Z (UTC) by curl -L, read-only linkage worker.
No trace or benchmark code was executed. No Factum write was made.

| File | Source URL | Retrieval method | SHA-256 |
|---|---|---|---|
| README.md | https://huggingface.co/datasets/CohereLabs/10-2026-qwen-investigation-traces/resolve/028b7cd7d931586dbfa05463903be9d45c4924ac/README.md | curl -L | 0e88e066b78d184d37b8fc708a72b4df9def4d105321a76e660759af8d291e8b |
| qwen-investigation.jsonl | https://huggingface.co/datasets/CohereLabs/10-2026-qwen-investigation-traces/resolve/028b7cd7d931586dbfa05463903be9d45c4924ac/qwen-investigation.jsonl | curl -L | 7110edee1203a58c8dea3b0e3f0a18a86fa42515a655b7b1901a7dda0278d1e6 |
| train-00000-of-00001.parquet | https://huggingface.co/datasets/CohereLabs/10-2026-qwen-investigation-traces/resolve/028b7cd7d931586dbfa05463903be9d45c4924ac/data/train-00000-of-00001.parquet | curl -L | f8c4b224d7d45aabf8b817ed4a85d2dd58c2d239c8cf6ba78ce42c7ecfa61e8b |
| cohere-blog.html | https://cohere.com/blog/concerning-behaviour-popular-open-weight-ai-model | curl -L | ced73ad8ae446372806565fcc119682ae802af3b3dcb3eee7a37d7d35e75413c |
| cohere-blog.txt | Derived text-only rendering of cohere-blog.html (tags stripped, local derivation, not a source fetch) | local derivation | — |

Source-layer notes (observed, not inferred):

- The Parquet holds 1 row: model `Qwen-3.8-Flash-Next`, one trace string (9,569 chars).
  Its only URL is `http://sanmaohe.oss-cn-beijing.aliyuncs.com/upload/test.bin`.
- The JSONL holds 4 lines (1 session + 3 messages). Same single URL.
- The README holds a reproduction script with 64 sampled probe completions.
  Those 64 URLs are sampled model outputs in the repro script, NOT the
  original trace. Entities from that list are marked "repro-sample" below
  and must not be read as original-trace observations.
- The blog names: Qwen3.8-Flash-Next, a Beijing Alibaba Cloud storage
  bucket, a Singapore proxy bucket named routify-file-proxy-sg, cloud
  metadata IP 169.254.169.254 (reported in 23–36% of completions in
  further testing), Qwen3.8-27B, Qwen3-Coder (comparison mention),
  and the CTI-REALM benchmark (Microsoft benchmark mention).
