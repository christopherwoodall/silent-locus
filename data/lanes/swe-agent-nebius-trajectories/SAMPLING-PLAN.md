# SAMPLING PLAN — nebius/SWE-agent-trajectories

Status: plan only. No trajectory bytes were downloaded for this plan.
Method: metadata only (HF datasets API, datasets-server statistics,
README text, parquet footers via HTTP range requests). Full provenance
in PROVENANCE.txt.

Revision (pinned): `68195a1450865274106246d0d0296a1d6807b88e`
License (verbatim from API card): `cc-by-4.0`
Ungated: yes (`gated: false`). Mirror used: none (ElenaFu mirror out of scope).

## 1. Dataset facts

- Source: `nebius/SWE-agent-trajectories` on Hugging Face.
- Content: 80,036 agent trajectories. Each row is one attempt by the
  SWE-agent framework to solve one GitHub issue (from
  `nebius/SWE-bench-extra` plus the SWE-bench dev split).
- Layout: single split `train`, 12 parquet files under `data/`.
- Compressed download size: 1,114,367,701 bytes (~1.11 GB).
- Uncompressed dataset size: 5,627,973,531 bytes (~5.63 GB).
- Mean row size: ~70,316 bytes uncompressed.
- Columns: `instance_id` (string), `model_name` (string),
  `target` (bool — true means the model solved the issue),
  `trajectory` (list of message structs: role, text, system_prompt,
  mask, cutoff_date), `exit_status` (string), `generated_patch`
  (string), `eval_logs` (string).

Table 1 — files (sizes from the HF tree API at the pinned revision;
rows from parquet footers):

| file | compressed bytes | rows | LFS oid (sha256, first 12) |
|---|---|---|---|
| data/train-00000-of-00012.parquet | 89,182,938 | 6,670 | 5a395e8c7bb8 |
| data/train-00001-of-00012.parquet | 94,796,688 | 6,670 | fca106cce0f0 |
| data/train-00002-of-00012.parquet | 91,137,587 | 6,670 | fc28c2ab014c |
| data/train-00003-of-00012.parquet | 96,591,990 | 6,670 | b6a4e13118de |
| data/train-00004-of-00012.parquet | 92,560,283 | 6,670 | d1a8d8d3bafb |
| data/train-00005-of-00012.parquet | 99,091,960 | 6,670 | c507212cd721 |
| data/train-00006-of-00012.parquet | 85,410,328 | 6,670 | fcad81ec5704 |
| data/train-00007-of-00012.parquet | 94,992,382 | 6,670 | 65547ce464ae |
| data/train-00008-of-00012.parquet | 93,467,561 | 6,669 | bfbd9a58fc94 |
| data/train-00009-of-00012.parquet | 93,395,224 | 6,669 | 8b4c45d8811f |
| data/train-00010-of-00012.parquet | 88,668,958 | 6,669 | 419e02daa099 |
| data/train-00011-of-00012.parquet | 95,071,802 | 6,669 | 7c3ccb843bab |
| total | 1,114,367,701 | 80,036 | — |

## 2. Stratification dimensions

There is ONE scaffold in this dataset: the SWE-agent framework.
No scaffold column exists. The model variants are the config axis.

Table 2 — model_name (from datasets-server statistics):

| model_name | rows | share |
|---|---|---|
| swe-agent-llama-70b | 74,792 | 93.4% |
| swe-agent-llama-8b | 4,053 | 5.1% |
| swe-agent-llama-405b | 1,191 | 1.5% |

Table 3 — target (true = issue solved):

| target | rows | share |
|---|---|---|
| False (not solved) | 66,647 | 83.3% |
| True (solved) | 13,389 | 16.7% |

Table 4 — exit_status (9 classes):

| exit_status | rows | share |
|---|---|---|
| submitted | 51,087 | 63.8% |
| submitted (exit_context) | 21,026 | 26.3% |
| exit_context | 3,568 | 4.5% |
| early_exit | 3,176 | 4.0% |
| submitted_no_patch | 1,066 | 1.3% |
| submitted (exit_format) | 80 | 0.10% |
| exit_format | 20 | 0.025% |
| submitted (exit_cost) | 10 | 0.012% |
| exit_cost | 3 | 0.004% |

Primary strata for this lane: model_name x target (6 cells).
Secondary coverage check: all 9 exit_status classes.

## 3. Sample design

Constraint: at most 1.5 GB uncompressed (ingested) bytes.
The manifest works at whole-file granularity (the scraper pulls
parquet files), so the sample is a cluster sample: 3 of 12 files.

Evidence for shard layout: parquet footers were read for all 12
files. Every file contains both target values and spans the full
model_name range (swe-agent-llama-405b to swe-agent-llama-8b) and the
full exit_status range (early_exit to submitted_no_patch) in its row
groups. The 12 files are interleaved shards of the full mix, not
model- or outcome-grouped. Any 3-file subset is therefore close to a
proportional stratified draw.

File choice: the 3 smallest files, to minimize transfer and leave
budget headroom:

| file | compressed bytes | rows | est. uncompressed bytes* |
|---|---|---|---|
| data/train-00006-of-00012.parquet | 85,410,328 | 6,670 | ~469,008,000 |
| data/train-00010-of-00012.parquet | 88,668,958 | 6,669 | ~468,937,000 |
| data/train-00000-of-00012.parquet | 89,182,938 | 6,670 | ~469,008,000 |
| total | 263,262,224 (~251 MB) | 20,009 | ~1,406,953,000 (~1.41 GB) |

\* estimated at the dataset mean row size of 70,316 bytes/row.
1.41 GB < 1.50 GB budget. Margin: ~93 MB (6%).

Expected per-stratum row counts (25.0% of dataset rows):

| stratum (model x target) | dataset rows | expected in sample |
|---|---|---|
| 70b x not solved | ~62,274 | ~15,569 |
| 70b x solved | ~12,518 | ~3,130 |
| 8b x not solved | ~3,375 | ~844 |
| 8b x solved | ~678 | ~170 |
| 405b x not solved | ~992 | ~248 |
| 405b x solved | ~199 | ~50 |

Expected exit_status coverage: the 5 common classes are certain;
submitted (exit_format) ~20 rows, exit_format ~5 rows,
submitted (exit_cost) ~2-3 rows, exit_cost ~0-1 rows (see gaps).

## 4. Rationale

- Proportional by construction: interleaved shards make a file-level
  pick behave like a stratified random sample across model, outcome,
  and exit class.
- All 3 model variants and both outcomes are certain to appear in
  large numbers (smallest expected cell: 405b x solved, ~50 rows).
- Rare exit classes: with ~25% of rows, every class with 80+ rows in
  the dataset is expected to appear at least ~20 times. Classes below
  that are flagged as gaps, not targets.
- 3 files (not 4): 4 files would be ~1.88 GB uncompressed, over the
  1.5 GB cap. 2 files would halve rare-class coverage for little gain.

## 5. Wire-up verification (scraper must do this)

1. Re-fetch the datasets API record. Abort if revision !=
   `68195a1450865274106246d0d0296a1d6807b88e` or license !=
   `cc-by-4.0`. Record the fetched values.
2. Download the 3 files from the manifest. Verify each file's sha256
   against the LFS oid in the manifest.
3. Read ONLY the label columns (model_name, target, exit_status) of
   the 3 files. Count per-file strata.
4. Accept the sample if: all 3 model variants present, both target
   values present, and the 5 common exit classes present in each
   file. If a file is an outlier (e.g. a whole exit class missing
   where the dataset rate predicts 50+ rows), swap it for the next
   smallest unused file and re-verify.
5. Report the true per-file stratum counts back to this lane before
   any TTP writeup uses the sample.

## 6. Coverage gaps

- exit_cost (3 rows) and submitted (exit_cost) (10 rows) in the full
  dataset are too rare for a 25% file-level sample to capture
  reliably. They are out of reach at this budget; note their absence,
  do not claim they were studied.
- exit_format (20 rows) and submitted (exit_format) (80 rows) are
  expected at ~5 and ~20 rows. Treat any writeup claims about them
  as anecdotal.
- Shard layout is inferred from footer bounds (min/max), not from
  per-file frequency tables. The wire-up check in section 5 is the
  guard against a mislabeled shard.
- instance_id spans SWE-bench-extra plus SWE-bench dev; repo-level
  stratification was not attempted (no repo column exists).
- Per-repository license terms (see raw/LICENSE.note) are not
  resolved per row in this lane.

## 7. Files in this lane

- SAMPLING-PLAN.md (this file)
- sample-manifest.json — exact rfilenames, download URLs, expected
  sizes, LFS sha256, stratum labels
- raw/LICENSE.note — license recorded verbatim
- PROVENANCE.txt — how every fact above was obtained
