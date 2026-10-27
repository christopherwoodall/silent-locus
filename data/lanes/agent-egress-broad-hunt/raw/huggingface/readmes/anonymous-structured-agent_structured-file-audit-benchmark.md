---
license:
  - cc-by-nc-4.0
  - cc-by-sa-4.0
  - other
task_categories:
  - table-question-answering
  - other
tags:
  - benchmark
  - data-quality
  - agents
  - spreadsheets
  - tabular
pretty_name: Structured-File Audit Benchmark
---

# Paper Data Release

This directory contains the benchmark dataset and evaluation scripts accompanying the ACL submission: the three data splits (SC-Flat, SC-Book, SC-Pro) and the code needed to score them.

## Contents

### `datasets/`

Benchmark data and per-task manifests for the three paper-facing splits.

- `datasets/sc_flat/data`
  SC-Flat is derived from DaBench, augmented with a replayable perturbation
  injected into each task's input artifact. Each task directory contains the
  perturbed file, the original file, and a `manifest.json` recording the
  injected defect.
- `datasets/sc_book/data`
  SC-Book is derived from SpreadsheetBench, augmented the same way. Includes
  task files, `manifest.json`, and split-level build summaries.
- `datasets/sc_pro/data`
  SC-Pro is derived from GDPval, augmented the same way, together with
  split-level selection and build summaries.
  Only benchmark tasks and manifests are included; run results are excluded.

### `eval_scripts/`

Evaluation scripts corresponding to the three data splits.

- `eval_scripts/sc_flat/`
  DA-Agent split evaluators (`eval_from_manifest.py`, `eval_rq1_pilot.py`)
- `eval_scripts/sc_book/`
  Spreadsheet split evaluators (`eval_spreadsheetbench_manifest.py`, `eval_spreadsheetbench_rq1.py`)
- `eval_scripts/sc_pro/`
  GDPval split evaluator (`eval_gdpval_sanity_results.py`)

## Not Included

This release is scoped to the benchmark dataset and its evaluation scripts,
not to experimental results.

## Licensing and Provenance

This release derives from three upstream sources. Each split carries the
license of its source dataset; redistribution of each split must comply with
that license.

- **`datasets/sc_flat/`** (from DaBench / InfiAgent,
  [InfiAgent/InfiAgent](https://github.com/InfiAgent/InfiAgent)):
  the upstream data is licensed **CC BY-NC 4.0**. This split is released
  under the same terms: attribution required, non-commercial use only.
- **`datasets/sc_book/`** (from SpreadsheetBench,
  [RUCKBReasoning/SpreadsheetBench](https://github.com/RUCKBReasoning/SpreadsheetBench)):
  the upstream data is licensed **CC BY-SA 4.0**. This split is released
  under the same license, as required by its share-alike terms: attribution
  required, derivatives must carry the same license.
- **`datasets/sc_pro/`** (from GDPval,
  [openai/gdpval](https://huggingface.co/datasets/openai/gdpval)):
  OpenAI describes the 220-task gold subset as open-sourced for research use,
  but the GDPval dataset card does not publish an explicit license field or
  redistribution terms for derivative datasets. This split is released in
  that open-sourced spirit, with provenance noted here; the licensing status
  of derivative redistribution is unconfirmed. If you are the GDPval dataset
  owner and have concerns about this release, please contact the authors.

The perturbation manifests and evaluators in this directory (`eval_scripts/`
and the manifest/patch files under `datasets/*/`) are original to this work.
