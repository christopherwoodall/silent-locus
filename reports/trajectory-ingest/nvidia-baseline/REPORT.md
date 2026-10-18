# NVIDIA baseline trajectories — ingest report

Date: 2026-10-16. Lane: `nvidia-baseline-trajectories`.
Factum lane ID: `lane_fc9d75a8d8534dd8b4e44a368f1380d7` (kind `baseline`).
Terms: a *trajectory* is one agent run (a list of steps). A *shard* is one
parquet file of a dataset. *Baseline* means a null corpus: normal data used
for contrast against behavior-rich corpora. It is not a hunting ground.

## What this is

Two NVIDIA SWE trajectory datasets ingested as a BASELINE corpus.
Every record carries tags `lane=nvidia-baseline-trajectories` and
`baseline=true`. Purpose: define what normal agent coding traces look
like, so future hunts can spot deviations.

## Datasets

- `nvidia/SWE-Hero-openhands-trajectories`
  revision `150bc119e52c647216fce285fd801f16b6fd745b`.
  14 parquet files, 2.40 GB, 34,269 rows claimed (verified exact).
- `nvidia/SWE-Zero-openhands-trajectories`
  revision `7b3cd106d00f60918e722d33a1d74bc67072a7ea`.
  64 parquet files, 12.21 GB, 318,115 rows claimed.
- Both: public, ungated, CC-BY-4.0. Config `default`, split `train`.
- Columns: `instance_id, repo, license, trajectory_id, trajectory,
  model_patch, dataset`. Each trajectory is a list of
  `{content, role, tool_calls[]}` with roles system/user/assistant/tool.
- Model: Qwen3-Coder-480B-A35B-Instruct. Harness: OpenHands.

## Sampling

Disk budget: 2.5 GB (disk was at 61%). Full pull is ~14.6 GB.
Acquired: 13 parquet files, 2.264 GB, 39,269 rows.

- Hero: 10 of 14 shards (indices 0,1,3,4,6,7,8,10,11,13),
  24,269 rows (71.4% of Hero bytes).
- Zero: 3 of 64 shards (indices 0,21,42), 15,000 rows (4.7%).
- Method: systematic even spacing, deterministic, no RNG.
- Plus dataset READMEs and tools.json (34 KB).
- Full plan with per-file bytes, sha256, and revisions:
  `SAMPLING-PLAN.md` (copy in this directory).

## Baseline characterization (all numbers verified)

- Shape: system prompt → user issue → think/editor/bash loop →
  exactly one `finish`. Length 21–201 steps, median 101.
- Tools: 4 only (`execute_bash`, `think`, `finish`,
  `str_replace_editor`). Zero unknown tools.
- Invariants, verified to the unit across all 39,269 rows:
  - 39,269/39,269 trajectories end with exactly one `finish`.
  - One tool call per assistant message (2,005,414 messages,
    zero multi-call).
  - 100% of trajectories carry a non-empty patch.
- Tool mix: bash 959,455 / editor 898,865 / think 107,825 /
  finish 39,269. Hero is execution-heavy (31.8 bash per trajectory);
  Zero is lighter (12.5) despite the "execution-free" name (the name
  refers to the fine-tuning recipe, not the traces).
- Normal quirks (not findings): literal `C-c` as interrupt idiom
  (2,362); literal `q` to quit pagers (492); `rm -f
  reproduce_issue.py` end-of-run cleanup; 23 `sudo` commands
  (apt-get installs, one `/etc/hosts` edit reverted in the same run);
  curl used for read-only reference fetching only.
- Full measured characterization: `BASELINE-CHARACTERIZATION.md`
  (copy in this directory).

## Review outcome

Honest zero across all 10 behavior classes (CAPTCHA, ACCOUNT,
GUARDRAIL, PROMPT-INJECT, CREDENTIAL, IRREVERSIBLE, TOOL-MISUSE,
RECOVERY, COORDINATION, OTHER). Every candidate died against the
bytes: credential hits were system-prompt text; injection hits were
repo code strings; captcha hits were filenames. Kill list with
evidence references: `REVIEW-FINDINGS.md` in the lane directory.

## Verification

Independent re-derivation of all headline numbers from raw parquet
bytes (all 13 files, all 39,269 rows). 10 small kills: count
corrections, one wrong example, one misplaced mean, one arithmetic
slip. No substantive claim falsified. No kill overturned.
Confidence: high. Full per-claim table: `VERIFICATION.md` in the
lane directory.

## Factum ingest

- Batch `6945c13d701041209ae7800ec0ec2953`: 78,558 records
  (39,279 submitted + 39,279 auto-generated `in_lane` edges).
- Per trajectory: one `behavior.tool_sequence` with a compact
  ordered tool-name step list. No message content is embedded;
  content stays in the raw parquet files, referenced by provenance.
- 2 source records (pinned revisions), 1 run record,
  2 `behavior.profile` records, 5 OBSERVED claims (verified
  invariants only; all 10 killed items stayed out).
- Claims cite profile observations and the run record, never
  source records.
- Edge scheme: run → tool_sequence → source is traversable via
  `body.run` / `body.source` refs. The scheme is documented in the
  run record (`params.edge_scheme`).
- Corpus after ingest: 202,462 records, 92 lanes, 0 pending.
  Export and verify both passed.

## Retention

Raw parquet files (2.264 GB) are LOCAL-ONLY, not committed, per
the artifact-retention policy. They are re-acquirable: `manifest.json`
in the lane directory records every source URL, revision SHA, byte
count, and sha256. Provenance sidecars (`.PROVENANCE.txt`) sit next
to each raw file.

## Limitations

- Zero coverage is thin: 3 of 64 shards (4.7%). Rare trajectory
  shapes in the other 61 shards are unexamined.
- `profile_kind` used `command`: the installed factum-behavior
  1.0.0 enum is `[ngram,url,slug,command]` and has no `baseline`
  value. Documented in the run record.
- Steps carry `command: ""`: the schema requires
  `index/tool/command` per step; no content embedded by design.

## Open gaps

- No cross-repo dedup key defined yet for behavior findings seen in
  two benchmarks. Recommended: `behavior.tool_sequence` +
  trajectory ID. The novelty cross-checker should confirm.
- Thin Zero coverage (above) is the main sampling risk.
