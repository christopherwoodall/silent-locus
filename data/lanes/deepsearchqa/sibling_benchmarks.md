# Sibling deep-research benchmark leads (follow-up collection candidates)

Dataset repo IDs + question counts only. NOT deep-pulled (lane brief: leads only).
Verification status noted per row.

| Benchmark | HF dataset repo | Questions | Notes |
|---|---|---|---|
| BrowseComp (OpenAI) | — (not on HF; encrypted CSV via `openai/simple-evals`: `browse_comp_test_set.csv` on Azure blob) | 1,266 | Exact-match grading; live web; plaintext **intentionally withheld** — questions+answers ship encrypted, decrypted only at eval time. Canary present. Question-text fingerprinting is hard by design. |
| BrowseComp-Plus | `Tevatron/browsecomp-plus` | 830 | Subset of BrowseComp, frozen ~100K-doc local corpus; fields obfuscated except `query_id` (anti-leakage). |
| GAIA | `gaia-benchmark/GAIA` | 466 (165 validation / 301 test) | Verified live on HF 2026-10-01. Gated access. |
| WebWalkerQA | `callanwu/WebWalkerQA` | 680 (`main` split) | Verified live on HF 2026-10-01. |
| WideSearch | `ByteDance-Seed/WideSearch` | ~200 (ZH+EN, single `full` split per card) | Verified live on HF 2026-10-01. CC0-1.0 license file. |
| xbench/DeepSearch | `xbench/DeepSearch` | 100 (ZH) | Verified live on HF 2026-10-01. Encrypted test cases. |
| MM-BrowseComp | `mmbrowsecomp/MMBrowseComp` | 400 (expanded Jan 2026) | Encrypted by default; multimodal. |

**Hunt implication for sibling lanes:** DeepSearchQA is the best fingerprint
source — 900 plaintext hand-crafted questions with distinctive niche entities
(civilrightsdata.ed.gov, State_Id/Measure_Id-style params, obscure stat tables).
BrowseComp's plaintext is intentionally withheld, so it is a poor fingerprint
source by design. GAIA/WebWalkerQA/WideSearch/xbench are the natural next
enumerations.
