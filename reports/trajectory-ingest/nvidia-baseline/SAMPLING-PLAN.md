# Sampling plan — nvidia-baseline-trajectories lane

## Objective
Acquire a disk-bounded (≤ 2.5 GB) sample of the two NVIDIA SWE trajectory
datasets for baseline ingest. Full pull is ~14.6 GB; budget allows ~17%.

## Datasets (both public, ungated, CC-BY-4.0)

| Dataset | Revision (sha) | Files | Bytes avail | Rows claimed | Issues claimed |
|---|---|---|---|---|---|
| `nvidia/SWE-Hero-openhands-trajectories` | `150bc119e52c647216fce285fd801f16b6fd745b` | 14 parquet (`data/train-00000..00013-of-00014.parquet`) | 2,402,012,417 (2.40 GB) | 34,269 | 11,766 |
| `nvidia/SWE-Zero-openhands-trajectories` | `7b3cd106d00f60918e722d33a1d74bc67072a7ea` | 64 parquet (`data/train-00000..00063-of-00064.parquet`) | 12,207,153,721 (12.21 GB) | 318,115 | 118,092 |

Both: config `default`, split `train`, pattern `data/*.parquet`.
Features: `instance_id, repo, license, trajectory_id, trajectory, model_patch, dataset`.
`trajectory` = list of `{content, role, tool_calls[]}`; roles: system/user/assistant/tool.
Row counts above are README-claimed; the HF API exposes no per-file row counts.
Measured post-download: Hero shards hold 2,500 rows each except the last (1,769);
13×2,500+1,769 = 34,269 — matches the claim exactly. Zero shards hold 5,000 rows
each (3 sampled); 64×5,000 = 320,000 vs 318,115 claimed (last shards presumably short).

## Budget check that forced sampling both
Initial idea (full Hero ~2.0 GB est. + 0.5 GB Zero sample) did not fit:
measured Hero total is 2,402,012,417 bytes (2.40 GB), not ~2.0 GB. Full Hero
alone would leave < 100 MB — no room for any Zero shard (smallest 137.8 MB).
Decision: sample both datasets, weighting the smaller, execution-based Hero
set more heavily.

## Method — systematic even spacing (no seed; deterministic)
Shard filenames are zero-padded ordinals, so index order == shard order.
Even spacing across the shard list maximises coverage of whatever ordering the
shards carry (e.g. by source repo), with no RNG involved.

- Hero: 10 of 14 → indices `round(i × 14/10)` for i in 0..9
  = [0, 1, 3, 4, 6, 7, 8, 10, 11, 13]
- Zero: 3 of 64 → indices [0, 21, 42] (step ≈ 21.3)

Plus full metadata per dataset (`README.md`, `tools.json`) — tiny, not sampled.

## Acquired (all verified: HTTP 200, byte-exact vs `X-Linked-Size`, sha256)

Hero parquets (10): 1,684,815,584 bytes, 24,269 rows (71.4% of Hero bytes)
Zero parquets (3): 579,169,092 bytes, 15,000 rows (4.7% of Zero bytes)
Metadata (4 files): 34,420 bytes
**Total: 2,264,018,096 bytes (2.264 GB) + 17 provenance sidecars — under the 2.5 GB budget with ~236 MB margin.**

Per-file bytes/rows/sha256: see `manifest.json`. Every raw file has a matching
`<filename>.PROVENANCE.txt` (source_url, retrieved_at UTC, retrieval_method=https-get,
sha256, dataset_revision).

## Retrieval notes
- `huggingface_hub` python lib is broken on this VM; used `curl` only.
- Per-file sizes came from the `X-Linked-Size` response header on the
  (unfollowed) `…/resolve/<sha>/<rfilename>` 302 redirect — the parquet blobs
  live on HF's Xet bridge CDN. Plain HEAD `Content-Length` reflects the 302
  body, not the blob; a ranged GET through the redirect chain returns 200
  without `Content-Range`.
- Cross-check: datasets-server `/parquet` endpoint sizes match the
  `X-Linked-Size` values byte-for-byte (e.g. Zero shard 0: 180,588,173 both).
- Egress is flaky: ~1.3 MB/s with mid-transfer truncations (always within a few
  MB of the end). Two Hero shards needed a second pass (fresh retry, not resume)
  after 4 truncated attempts each; all 13 parquets ultimately byte-verified.
- 1–2 s pacing between files; retries with backoff on non-200/size mismatch.

## Limitations of the sample
1. Zero coverage is thin: 3/64 shards (4.7% of bytes, ~15k of 318k rows).
   Rare repos/trajectory shapes in Zero are likely missed.
2. Hero coverage is good but not complete: 10/14 shards (71.4%).
3. Systematic spacing assumes shard order carries the stratification of
   interest; if shards are randomly ordered the sample is effectively random,
   if ordered by something unrepresentative (e.g. all of one source repo per
   shard) spacing helps but cannot guarantee balance — the `dataset` and `repo`
   fields per row allow a post-hoc representativeness check.
4. Row counts per shard were measured only for acquired shards (pyarrow);
   unacquired shards' row counts are unknown (API exposes none).
5. Sample reflects dataset revisions pinned above; upstream re-uploads would
   change bytes/hashes — provenance records the revision per file.
