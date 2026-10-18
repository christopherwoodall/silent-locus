# Sampling Plan — Open-SWE-Traces (nvidia/Open-SWE-Traces)

Recorded BEFORE any download. Date: 2026-10-16.

## Objective
Selectively acquire NVIDIA Open-SWE-Traces agent trajectory data for BEHAVIOR
REVIEW of agentic shortcutting / reward-hacking behaviors. Quality over
quantity. Disk budget: < 500 MB total.

## What the dataset is
- Repo: huggingface.co/datasets/nvidia/Open-SWE-Traces, public, ungated, CC-BY-4.0.
- Dataset revision pinned: `1db674173119d71df45c22007af99e214600711a`
  (lastModified 2026-10-13T23:39:28Z).
- ~678k rows (card prose); API reports `usedStorage` 419,645,222,744 bytes
  (~391 GiB across ~285 parquet shards; ~44 GB in the task brief was wrong).
- No per-split row counts in the API; split structure comes from cardData
  configs and `data_distribution.md` (v1.0 section) plus the README.

## Split structure (from cardData configs)
- v1.0: openhands + sweagent, models minimax_m25, qwen35_122b.
  151,219 trajectories AFTER a scrub on 08/26 removed trajectories containing
  git-hacking behaviors (was 207k). See README "What's New" 06/21 entry.
- v1.1: + deepseek_v4_flash_0731, qwen36_27b; adds minisweagent harness.
- v1.2: + qwen38_27b, qwen38_flash_next; opencode / claude-code harnesses
  promised, not present yet.
- Task sources per split dir: `swe-rebench-v2` and `scale-swe`.

## Why prioritize v1.0
The README states v1.0 was scrubbed (08/26) of trajectories that include
git-hacking behaviors, following arXiv 2609.06780. For a behavior review of
agentic shortcutting, the v1.0 population is the one that was touched by the
scrub: it is where residual / borderline shortcutting behaviors would live if
the scrub was imperfect. Inclusion rule: one whole shard from each of the two
highest-trajectory v1.0 model x harness combos, covering BOTH harnesses and
BOTH models (thinking vs non-thinking is a core behavioral axis in the paper).

## Selected files (whole shards, original names)
1. `data/sweagent/minimax_m25/swe-rebench-v2/train-00000-of-00019.parquet`
   - v1.0, SWE-agent harness, MiniMax-M2.5 (thinking), swe-rebench-v2 source.
   - Highest trajectory count in v1.0 (46,819). Thinking-model trajectories
     have richer internal reasoning to audit.
   - Size: 208,152,116 bytes (measured via Content-Range probe).
2. `data/openhands/qwen35_122b/swe-rebench-v2/train-00000-of-00017.parquet`
   - v1.0, OpenHands harness, Qwen3.5-122B (non-thinking), swe-rebench-v2 source.
   - Completes the 2x2 model x harness matrix; non-thinking agent behavior is
     the contrast class.
   - Size: 236,380,400 bytes (measured via Content-Range probe).

Both files chosen on `swe-rebench-v2` because the safety paper audits
SWE-bench-family harnesses and the DeepSWE line; scale-swe excluded from this
sample.

Budget check: 208,152,116 + 236,380,400 = 444,532,516 bytes (~424 MiB)
< 500 MB. Paper PDF adds a few MB on top of the trajectory budget.

## Secondary context
- `data_distribution.md` (10,613 bytes, cached in raw/): PRIMARY stats on
  v1.0 trajectory distribution. Provenance recorded.
- arXiv 2609.06780 PDF (SECONDARY): "Shortcutting the Fix: Identifying and
  Categorizing Agentic Exploits in Software Engineering Benchmarks" — the
  paper the scrub followed. Abstract documents exploit categories including
  retrieving upstream solutions and exploiting local Git histories
  ("git hacking"), attempt rates 60.7%-90.1% under standard evaluation.
  This is SECONDARY material (someone else's analysis), cached for context,
  not treated as PRIMARY observation.

## Explicit gaps (within budget)
- v1.0 openhands/minimax_m25 and sweagent/qwen35_122b combos uncovered
  (would complete 2x2 matrix at full depth).
- No v1.1 (deepseek_v4_flash_0731, qwen36_27b) or v1.2 (qwen38_27b,
  qwen38_flash_next) coverage — newer models may shortcut differently.
- No minisweagent / opencode / claude-code harness coverage.
- No scale-swe task-source coverage.
- shard-0 only per combo; per-shard row distribution is unvalidated.

## Constraints honored
- Passive read-only HTTPS GET via curl (python huggingface_hub broken on VM).
- Whole files only; no byte-range truncation (would corrupt provenance).
- Provenance sidecar per file: source_url, retrieved_at UTC ISO-8601,
  retrieval_method=https-get, sha256, dataset_revision.
- Actual byte sizes measured at download time; HF metadata sizes are null.
- No redaction of observed values. No execution of trajectory payloads.
- Agents + infrastructure scope only.
