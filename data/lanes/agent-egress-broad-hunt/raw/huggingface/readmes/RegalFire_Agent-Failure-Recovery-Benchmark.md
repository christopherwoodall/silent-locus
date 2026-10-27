---
pretty_name: Agent Failure Recovery Benchmark — 22,573 Verified Trajectories
license: mit
language:
- en
task_categories:
- reinforcement-learning
- text-generation
tags:
- agents
- agentic-ai
- benchmark
- evaluation
- reasoning
- trajectories
- failure-recovery
- reinforcement-learning
- synthetic-data
- verified
- planning
- multi-agent
- text
size_categories:
- 10K<n<100K
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train.parquet
  - split: validation
    path: data/validation.parquet
  - split: test
    path: data/test.parquet
  - split: holdout
    path: data/holdout.parquet
---

# Agent Failure Recovery Benchmark

**22,573 synthetic, source-verified failure → recovery trajectories across four domains.**
Evaluate whether a system can reject a failed plan, choose a recovery, or recognize that no recovery exists. Every row links to a hashed record in a pinned public source and is checked by independent computational oracles and trajectory replay.

**Tasks:** failure diagnosis, recovery-action prediction, planning regression, scoped agent evaluation and imitation learning.

**Limits:** controlled harness errors, not real agent logs; small template diversity; public answers; no measured model performance. Physics rows correct predictions rather than perform physical interventions. Planning rows verify one next step, not full task completion.

```python
from datasets import load_dataset
import json
ds = load_dataset("RegalFire/Agent-Failure-Recovery-Benchmark")
row = ds["test"][0]
failure = json.loads(row["failure_state"])
recovery = json.loads(row["recovery_action"])
```

## Coverage

| Domain | Records | Failure and recovery contract |
|---|---:|---|
| Navigation | 8,000 | A critical grid edit blocks a legacy path; replan optimally or report unreachable |
| Multi-agent | 8,000 | A premature stop fails the goal; recover with a collision-free optimal joint plan or report infeasible |
| Counterfactual physics | 6,000 | An inconsistent prediction is rejected; replace it with the analytical transition |
| Planning | 573 | A wrong available policy action is rejected; apply the independently verified next step |

Includes recoverable and unrecoverable cases. There are 27 domain-specific task families and 23 connected source/template groups. See `stats.json` for exact family counts.

## A trajectory at a glance

```text
initial state → rejected action / prediction → failure state
             → verified recovery (or no recovery) → final state
```

Each record provides `initial_state`, `goal`, `action_history`, `failure_state`, `failure_type`, `recovery_available`, `recovery_action`, `recovery_sequence`, `final_state`, `success`, `cost_or_steps`, `oracle`, `provenance`, `group_id`, and `split`. Four complete examples are in [samples/examples.jsonl](samples/examples.jsonl).

## Viewer and formats

The default configuration uses Zstandard Parquet. Heterogeneous object/list columns are **losslessly encoded JSON strings**, including JSON `null` for absent recovery actions. Decode them with `json.loads`; see `serialization.json` for the exact columns. This avoids incompatible nested Arrow schemas across domains.

Original nested records remain in `dataset.jsonl` and the four root split JSONL files. Use plain Python to read those; the default Hub loader uses Parquet. Samples are examples of existing rows, not additional data.

## Evaluation without answer leakage

Run `python evaluate.py make-prompts test prompts.jsonl`, give only those prompts to your system, then save predictions as one JSON object per line:

```json
{"id":"<record id>","recovery_available":true,"recovery_action":{"action":"<predicted action>"}}
```

Run `python evaluate.py score test predictions.jsonl`. It reports availability accuracy and strict recovery-action exact match, overall and per domain. Missing predictions count as failures; unknown/duplicate IDs are rejected. **Exact match can penalize alternative equally valid paths/plans.** It is a reproducible baseline, not a semantic trajectory judge or a model-performance claim. The independent validator verifies dataset truth, separately from this baseline scorer.

Prompt exports exclude reference recovery, final state, oracle and provenance. Public split labels are still visible, so this is an exposed regression benchmark, not a secret evaluation.

## Validation you can rerun

```bash
pip install -r requirements.txt
python validator/validate.py .
python validator/check_package.py
```

The first command checks all 22,573 records: strict JSON, schema, identity, exact semantic deduplication, source file and row hashes, source relations, source oracles, failure/recovery contracts, recovery witnesses, and grouped split partitioning. It does not import a builder. Pinned ancestors require network access or a populated Hugging Face cache; credentials are unnecessary.

The second independently compares decoded Parquet with original rows and deliberately corrupts ten trajectory fields in each of four domains. All 40 corruptions must be rejected. Reports: `validation_report.json`, `package_validation.json`; prior release tests are retained in `robustness_report.json`.

## Splits and limitations

| Split | Rows |
|---|---:|
| train | 15,150 |
| validation | 1,200 |
| test | 165 |
| holdout | 6,058 |

Splits retain whole task-template families and connected grid groups. The uneven sizes and small test split are intentional consequences of grouping; validation and holdout should also be evaluated separately. Master seeds identify generation runs, not independent task seeds. These are template-held-out splits, not fresh-seed independence experiments. Exhaustive semantic near-duplicate detection is not claimed.

Real agents may fail in ways absent here. No browser/tool/API error traces, measured model leaderboard, real-world outcomes, contamination-free evaluation, or reinforcement-learning environment implementation are provided. Successful recovery means the narrow contract described above.

## Provenance and license

This release packages an existing verified RegalFire asset; it adds **zero new trajectories**. The previous release is pinned in `PACKAGE_PROVENANCE.json`. `SOURCE_LOCK.json` pins four MIT source datasets and file hashes:

- [GameNav-CriticalEdits-25K](https://huggingface.co/datasets/RegalFire/GameNav-CriticalEdits-25K)
- [GameCoord-JointPlans-25K](https://huggingface.co/datasets/RegalFire/GameCoord-JointPlans-25K)
- [GamePhysics-Counterfactuals-100K](https://huggingface.co/datasets/RegalFire/GamePhysics-Counterfactuals-100K)
- [GameAgent-Horizon-120K](https://huggingface.co/datasets/RegalFire/GameAgent-Horizon-120K)

Per-row provenance retains source ID, source hash, transformation and license. No unverified Bionic input was added. Do not count these rows and their source ancestors as independent examples. This dataset contains synthetic MIT rows; no scientific community/CC BY-SA content is present. Preserve `LICENSE`, `THIRD_PARTY_LICENSES.md` and validator notices.

## Custom / Private Dataset Work

RegalFire builds custom AI datasets, evaluation sets and reproducible data pipelines for research and production systems.
Contact: ootiris@gmail.com
Hugging Face: [RegalFire](https://huggingface.co/RegalFire)

Private adaptation can include client-owned environments, new failure contracts, independent validators and private holdout sets. Public source adaptations remain public-license material.


## Windway Data community research

Windway Data is an early-stage AI reliability and data infrastructure startup. This existing public asset retains its original license and source provenance. It is distinct from our measured local AI experiments.

Don't trust agent self-report. Verify environment state. See the [four-case False Completion Community Release](https://huggingface.co/datasets/RegalFire/Windway-False-Completion-Cases-v0.1) for sanitized factual state/claim contrasts, not raw private conversations or a model leaderboard.

[Windway Data](https://windwaydata.com) · [Research](https://windwaydata.com/research/) · [Failure Is Not Binary](https://windwaydata.com/research/failure-is-not-binary/) · [Custom/private evaluation](https://windwaydata.com/contact/).


## Windway publication and related research

Windway Data maintains this selected public research asset through the existing RegalFire publication account. This operator statement does not replace historical RegalFire attribution, change the asset-specific license, or claim ownership of third-party material. Company/operator disclosures are on the [canonical legal page](https://windwaydata.com/legal/).

- [Windway Data — canonical website](https://windwaydata.com/)
- [Windway research](https://windwaydata.com/research/)
- [Failure Is Not Binary — methodology and limitations](https://windwaydata.com/research/failure-is-not-binary/)
- [Verified Agent Trajectories v0.1 — 60 state-verified episodes](https://huggingface.co/datasets/RegalFire/windway-verified-agent-trajectories)
- [False Completion Cases v0.1 — four editorial cases](https://huggingface.co/datasets/RegalFire/Windway-False-Completion-Cases-v0.1)

These are distinct resources: fixed-label fixtures, recorded state-verified trajectories, editorial cases and a research note. Their sample sizes and metrics must not be pooled. No customer evaluation or comparative leaderboard is implied.
