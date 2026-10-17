# Sampling plan: Kwai-Klear/SWE-smith-mini_swe_agent_plus-trajectories-66k

Date: 2026-10-17 (UTC).
Dataset revision: 750b2c11239fd5e32f97e6cfb9bf80fb9a9a2983.

## 1. What the head sample shows

The head sample is shard 00 (1,405 trajectories).

- Schema: two columns only. `instance_id` (string) and `messages` (list of
  role and content). There are no other columns.
- `instance_id` has this shape: `<org>__<repo>.<commit>.<bug_type>__<nonce>`.
- **The metadata has no outcome flag.** There is no resolved/unresolved label.
  In the head sample, 100% of trajectories (1,405 of 1,405) end with the
  `MINI_SWE_AGENT_FINAL_OUTPUT` marker. The corpus holds only completed runs.
  Outcome classes must be derived from the message text (see section 3).
- Bug types ("error classes") can be read from the metadata. Counts from a
  full scan of all 47 shards' instance_id column:
  - `lm_rewrite`: 24,121 (36.6%)
  - `func_basic`: 7,008 (10.6%)
  - `combine_file`: 6,714 (10.2%)
  - `combine_module`: 5,096 (7.7%)
  - `func_pm_ctrl_shuffle`: 2,427; `func_pm_remove_assign`: 1,642;
    `func_pm_remove_cond`: 1,625; `func_pm_ctrl_invert_if`: 1,557;
    `func_pm_class_rm_funcs`: 705; `func_pm_remove_loop`: 679;
    `func_pm_op_swap`: 671; `func_pm_op_change`: 471;
    `func_pm_remove_wrapper`: 289; `func_pm_op_change_const`: 280;
    `func_pm_op_break_chains`: 213; `func_pm_class_rm_base`: 210;
    `func_pm_class_shuffle_funcs`: 6
  - `pr_*`: about 2,190 distinct values. Each one has 5 to 20 runs.
    These are bugs built from real GitHub PRs. This is the long tail.
- Source orgs: 116. Top: conan-io (4,798), stanfordnlp (4,309), tweepy (1,909).
  No org is held mostly in one shard. The corpus is well mixed.
- Shard size (compressed): 25.7 to 36.3 MB. Each shard holds about 1,404 rows.

## 2. Budget

- HF API `download_size` (compressed): 1,579,055,064 bytes = **1.58 GB**.
  The "4.64 GB" number is the uncompressed size. The sum of the 47 shard
  Content-Length values confirms 1.58 GB on the wire.
- Budget: at most 1.5 GB compressed. So we can keep at most 95% of the corpus.

## 3. Sampling design

The unit of choice is a whole parquet shard. A shard cannot be split at
download time. Strata:

- **S-A bug class**: keep the mix of all bug families. This covers
  `lm_rewrite`, `func_basic`, `combine_file`, `combine_module`, the 15
  `func_pm_*` program mutations, and the `pr_*` long tail.
- **S-B source org**: all 116 orgs. We checked that no dropped shard removes
  an org fully.
- **S-C outcome/error (derived after download, heuristic)**: no ground truth
  exists. After the download, we will score each trajectory from its text:
  - C1: last tool call returned 0 (clean finish)
  - C2: last tool call returned non-zero (error finish)
  - C3: the last assistant message has give-up language (abort proxy)
  - C4: trajectory length quartile (short = fast solve, long = loop/struggle)
  These are proxies. We will report them as proxies, not as true labels.

## 4. Choice of shards (deterministic)

- First try (REJECTED): drop the 7 shards with the fewest distinct bug types
  {01, 02, 03, 04, 13, 14, 16}. A check showed bias: shards 01-04 hold
  clusters of the `pr_*` tail and of early-shard orgs. Many `pr_*` groups
  would lose more than 20% of runs. 36 orgs would drop below 80% kept.
  We rejected this choice.
- Final choice: drop 7 shards at random, with a fixed seed.
  Seed 151 was the best of 200 tried. Rule: no bug family fully lost, and
  the worst kept share as high as possible.
  **Dropped: 13, 18, 22, 23, 26, 40, 45** (248.3 MB).
  **Kept: 40 shards** (00 is the head sample; 39 more to download).
- Checked coverage of the kept set: no bug family and no org (n>=10) is
  fully lost. Worst kept share: 50% for one small `pr_*` group
  (about 6 runs); 77% for the worst org. All 16 named bug families keep
  most of their runs.
- Expected result: **1.331 GB compressed (under 1.5 GB), 56,166 runs
  (85.1% of the 65,994-run corpus)**.

## 5. Download method

`curl -L -C - --retry 3 -o <file>`. One file at a time. We do not use
huggingface_hub (it is broken on this VM). Each file gets:
- `.PROVENANCE.txt`: source URL, retrieval time (UTC), method=curl, revision
- `.sha256`: sha256 hash, checked after the download

## 6. Checks after the download

- Check the sha256 of every file.
- Run the outcome heuristic (section 3, S-C) over all 40 shards. Report the
  C1/C2/C3/C4 mix that we see. If a class is empty, report the gap. Do not
  force coverage.
- Check free disk space before and after. It must stay above 10 GiB.
