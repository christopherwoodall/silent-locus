# CRS Label Independent Audit

This directory contains the raw labels from a **post-submission, independent
human audit** of the 147 CRS (completion-requires-secret) task labels used in
MCPHunt. It exists so the inter-annotator reliability statistic reported for the
CRS stratification is fully reproducible from released data.

## Provenance (what this audit actually is)

- **When:** performed *after* the paper was submitted (post-submission audit).
  It is **not** a pre-submission annotation and is **not** a pre-registered
  study.
- **Who:** two independent annotators who are **not authors** of the paper.
- **How:** each annotator labeled all 147 tasks **blind to trace outcomes** and
  blind to the other annotator, applying the published CRS rubric
  (`src/mcphunt/taxonomy.py`, CRS criteria block) to the task
  registry (id, mechanism, task type, description, prompt).
- **What the CRS registry label is:** the `completion_requires_secret` value in
  `src/mcphunt/taxonomy.py` remains **frozen task metadata**, assigned at task
  construction before any experiment ran. This audit does **not** change any
  registry label (project invariant #4); it measures how reliably an independent
  human, given only the rubric and the task text, recovers those labels.

## Files

| File | Contents |
| --- | --- |
| `annotation_1.csv` | Annotator 1's blind labels for all 147 tasks (`your_crs_label`). |
| `annotation_2.csv` | Annotator 2's blind labels for all 147 tasks. |

Each CSV has one row per task: `row, task_id, mechanism, task_type,
description, prompt, your_crs_label`. `your_crs_label` accepts
TRUE/FALSE (also T/F, 1/0, yes/no, case-insensitive).

## Reproducing the statistic

The headline reliability statistic is the **inter-annotator agreement between
the two independent annotators**:

```bash
PYTHONPATH=src python scripts/score_annotation.py \
    artifacts/release/crs_audit/annotation_1.csv \
    artifacts/release/crs_audit/annotation_2.csv
```

This reports Cohen's kappa with a percentile bootstrap 95% CI (fixed seed,
10,000 resamples), raw agreement, the 2x2 confusion matrix, and the list of
disagreements. The script is deterministic, stdlib-only, and has **no paid or
live-model path**.

As a secondary diagnostic, each annotator can be compared against the frozen
registry labels; this is an audit cross-check, **not** the inter-annotator
reliability statistic, and does not substitute for it.

## Honesty note

The reported kappa is whatever the two independent human annotators actually
produced — a moderate-to-substantial value is disclosed as-is, not adjusted.
The earlier submitted-version claim of a two-annotator kappa was unsupported by
any real annotation event and has been retracted; this directory is the genuine
independent-annotation event that replaces it.
