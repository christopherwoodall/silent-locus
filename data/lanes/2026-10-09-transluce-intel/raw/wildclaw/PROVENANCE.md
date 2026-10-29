# Provenance — ClawBench / WildClawBench trajectory evidence

Collected 2026-10-07 (CDT) by subagent lane `wildclaw` for the Transluce-findings integration
(findings #138, #141, #142, #143, #144, #149).

## Method
- HF metadata/listings: `curl` against `https://huggingface.co/api/datasets/<id>` (and
  `?blobs=true`, `/tree/main[/<path>]`). No python `huggingface_hub` (broken on this VM per TOOLS.md).
- File pulls: `curl -sL https://huggingface.co/datasets/<id>/resolve/<rev>/<path>`.
- All values below are observed (sha256 of bytes on disk). No redactions applied.

## Dataset repos
| Dataset | Pinned rev used | LFS size (API, 2026-10-07) | File mix |
|---|---|---|---|
| internlm/WildClawBench-Trajectories | d2816016a7a7b41fa6b7ba368b28ddafcb54fd93 | 8.675 GB (615 files) | 600 jsonl sessions, 10 tar.gz (per-provider archives, 102MB–1.3GB), 2 zip (qwen), 1 train.parquet 25.4MB |
| NAIL-Group/ClawBenchV1Trace | f1570c092187ba9dcacf14d8abfdd36fbb783f4c | 30.244 GB (19,819 files) | 6,169 jsonl, 4,641 json, 2,114 mp4, 4,833 png, 2,048 .sync_complete |
| TIGER-Lab/ClawBenchV2Trace | bb88da2b8a94044df7888d79c1ad4c7e88949043 | 18.852 GB (36,899 files) | 2,823 jsonl, 2,342 json, 2,028 log, 935 mp4, 28,769 png |

## Files cached here (see SHA256SUMS.txt for full list)
- wcb_glm52_paper_affiliation.jsonl — #141 evidence. sha256 5adeda9c6ace417405795368451031d4933745e581c91d80c1a22aeab1d0f3ae == published in finding. OBSERVED match.
- wcb_grok45_constraint_search.jsonl — #138 evidence (Grok run).
- wcb_glm52_constraint_search.jsonl — #138 evidence (GLM run).
- cbv1_zillow_glm5.jsonl — #143 evidence. sha256 ca3c0e052daff61b28e852c00b06d63478469e46fb3ff49406b605205e628bae == published. OBSERVED match.
- cbv1_instacart_glm5.jsonl — #144 evidence. sha256 1a26f364d43dcf74a8edcb7d86f208c0c378a816467504e2e54cccecbeea5f69 == published. OBSERVED match.
- cbv2_changeorg_deepseek.jsonl — #149 evidence. sha256 520edea2bc8d03e5e1a9d92d1374a9ab928f9b11f054a78a5fa133904acf1797 == published. OBSERVED match.
- wildclaw_train.parquet — full WildClawBench evaluation corpus, 720 rows (12 models x 60 tasks), columns task_id/trajectory/model_name/task_category. Pulled at rev d2816016… (same pin as findings).
- sample04/ — 16 extra sessions: task_3 + task_8 for 8 other provider dirs (5.3 MB).
- tree_*.json, cbv2_batch_summary.json — directory listings / batch summary via API.

## Notes / limits
- #142 (Parks Canada, task-625 runs) traces were NOT individually pulled: the HF `/tree/main`
  endpoint caps at 1000 entries (V1 listing stops at task 533); dirs for task 625+ need a deeper
  enumeration (recursive per-prefix tree calls). Finding #142 already pins byte-level line refs.
- Nothing over ~500MB was pulled. Full corpora left on HF (sizes above).
- Parquet parsed with pyarrow (installed via pip for this analysis only); no python HF libs used.
