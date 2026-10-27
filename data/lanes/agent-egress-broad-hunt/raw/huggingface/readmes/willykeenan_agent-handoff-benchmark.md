---
pretty_name: Agent Handoff Benchmark
license: cc-by-4.0
language:
- en
size_categories:
- 10K<n<100K
tags:
- banking77
- agent-evaluation
- intent-classification
- uncertainty-quantification
- selective-prediction
- decision-sufficiency
- reproducible-research
configs:
- config_name: predictions
  default: true
  data_files:
  - split: test
    path: data/predictions/test.parquet
- config_name: vectors
  data_files:
  - split: test
    path: data/vectors/test.parquet
- config_name: decisions
  data_files:
  - split: test
    path: data/decisions/test.parquet
---

# Agent Handoff Benchmark

A text-free evaluation dataset for studying whether partial classifier output
preserves a downstream decision. It packages the public Waggle/Kea BANKING77
reference artifacts as three directly loadable tables: intent predictions,
77-class probability vectors, and decision/certificate outcomes under 12 fixed
synthetic cost policies.

William Keenan created the classifier experiment, derived predictions,
decision-sufficiency experiment and this packaging. **BANKING77 was created by
PolyAI-LDN/Casanueva et al.; this is a derived evaluation dataset, not a new
collection of banking queries.** No source query text is included.

Companion classifier: [`willykeenan/banking-intent-classifier`](https://huggingface.co/willykeenan/banking-intent-classifier).

## Load the dataset

Install the tested loader dependencies with Python 3.12:

```bash
python -m pip install -r requirements.txt
```

```python
from datasets import load_dataset

repo = "willykeenan/agent-handoff-benchmark"
predictions = load_dataset(repo, "predictions", split="test")  # 3,050 rows
vectors = load_dataset(repo, "vectors", split="test")          # 3,050 rows
decisions = load_dataset(repo, "decisions", split="test")      # 36,600 rows

print(predictions[0]["trueIntent"], predictions[0]["predictedIntent"])
probabilities = [x / vectors[0]["probabilityScale"]
                 for x in vectors[0]["probabilities"]]
```

The decision table provides convenient scalar fields and retains the complete
original record as a JSON string to avoid ambiguous, heterogeneous nested
schemas across loading libraries:

```python
import json
record = decisions[0]
original = json.loads(record["payload_json"])
certificate = original["adaptive"]["certificate"]
print(record["case_id"], record["policy_id"], certificate["disposition"])
```

Before publication, or from a downloaded snapshot, load a table directly:

```python
local = load_dataset("parquet", data_files={"test": "data/vectors/test.parquet"}, split="test")
```

## Configurations and schema

| Configuration | Rows | One row represents | Main fields |
|---|---:|---|---|
| `predictions` | 3,050 | One cleaned, train-disjoint BANKING77 test case | `caseId`, `trueIntent`, `predictedIntent`, `wordOnlyIntent`, `confidencePpm`, `top3`, `sourceIndex`, `sourceSplit`, `typoEligible`, `textIncluded` |
| `vectors` | 3,050 | The frozen 77-class prediction for that case | `caseId`, `vectorId`, `modelId`, `labelIds`, `probabilities`, `probabilityScale`, `trueIntent`, `sourceIndex`, `sourceSplit`, `textIncluded`, `schemaVersion` |
| `decisions` | 36,600 | One case under one of 12 synthetic policies | `case_id`, `vector_id`, `policy_id`, action/disposition columns, `revealed_components`, `authority_granted`, `payload_json` |

All three configurations expose only a **test** split. They are related views,
not independent sample pools: each case has one vector and 12 decision rows.
Join `predictions.caseId` to `vectors.caseId` and `decisions.case_id`; join
`vectors.vectorId` to `decisions.vector_id`. Every case-policy pair is unique.
The 36,600 decisions are **not 36,600 independent banking examples**.

Vector probabilities are nonnegative integers in label order, with 77 values
summing to `probabilityScale = 1_000_000`; divide by that scale before probability
calculations. `top3` is a list of intent/probability objects from the original
prediction artifact. `sourceIndex` points to the pinned upstream test file;
`caseId` is derived from normalized text. Text exclusion does not make records
anonymous or prevent linkage to the public upstream source.

Decision scalar columns include `adaptive_disposition`, `adaptive_action_id`,
`qualification_disposition`, `restricted_disposition`, `restricted_action_id`,
`full_vector_action_id`, `naive_top1_action_id`, `safe_k1_disposition`, and
`safe_k3_disposition`. Action IDs may be null when a control refuses to choose.
`revealed_components` counts probabilities in the adaptive certificate.
`authority_granted` is always false: a mathematical certificate grants no
permission to execute an action. `payload_json` preserves every original field
and value, including policies' expected costs, alternative controls, certificate
bounds, qualification, byte counts and causal identifiers.

## Provenance and construction

- Public source repository: [willykeenan/waggle-kea](https://github.com/willykeenan/waggle-kea),
  pinned to commit [`54041045c82953cbbabac155b150a0f7b7ed5603`](https://github.com/willykeenan/waggle-kea/tree/54041045c82953cbbabac155b150a0f7b7ed5603).
- Upstream BANKING77: [PolyAI-LDN/task-specific-datasets](https://github.com/PolyAI-LDN/task-specific-datasets),
  pinned to commit `57ec275d8078af65b7731c2a98be812d844a6d6b`; file digests appear in
  [SOURCE.json](evidence/benchmarks/banking77/SOURCE.json).
- The existing protocol normalizes text to audit duplicates and ambiguity,
  retains 9,971 unique unambiguous training cases, and evaluates on 3,050 unique
  unambiguous test cases after excluding normalized train/test overlap.
- A fixed word-and-character TF-IDF / log-loss SGD classifier generates the
  predictions. The downstream study uses 12 deterministic, output-blind,
  four-action zero/one-cost policy matrices. These policies are synthetic and
  do not encode real bank procedures or customer-outcome labels.
- This package copies allowlisted public artifacts; it does not retrain models,
  generate cases, reassign labels, alter splits or recompute experimental results.
  Parquet preserves the prediction/vector records. The decisions table adds
  convenient projections while keeping the original row text in `payload_json`.

Original JSONL/gzip, policies, configuration, protocols, reference results and
checksum manifests are retained under [evidence/](evidence/).
[SOURCE_FILES.json](SOURCE_FILES.json) maps each copied file to its source path,
SHA-256 and byte count. [VALIDATION.json](VALIDATION.json) records row counts,
schemas, exact round trips and relational checks. [MANIFEST.sha256](MANIFEST.sha256)
pins this package's files. The build script verifies source bytes against the
pinned Git commit and the original checksum manifests before packaging.

To reproduce the data tables from the public repository, install the supplied
dependencies and run these commands from a downloaded copy of this package:

```bash
git clone https://github.com/willykeenan/waggle-kea.git source
git -C source checkout 54041045c82953cbbabac155b150a0f7b7ed5603
python scripts/build_dataset.py --source source --output reproduced-data
```

This rebuilds the tables and provenance checks, not the original experiments.
The card and package documentation are maintained separately. The validator
requires ordinary Python execution with assertions enabled (no `-O`).

## Published results and limitations

The existing classifier comparison reports macro-F1 **0.911858** for the
word-and-character model versus **0.891545** for its matched word-only control.
This comparison is **exploratory and test-informed**, not a confirmatory or
state-of-the-art benchmark. See the retained [classifier run](evidence/benchmarks/banking77/results/reference-v1/run.json).

The prospective secondary decision-sufficiency study qualified **35,013 of
36,600 decisions (95.66%)**, with zero qualified-decision mismatches against the
full-vector reference. Its preregistered primary hypothesis was **not supported**:
coverage improved by **6.65 percentage points** over safe `k=1`, below the frozen
**10-point** threshold (`H0_RETAINED`). A simpler informed expected-cost summary
was smaller than the certificate. These are retained results from the original
[evaluation](evidence/benchmarks/decision-sufficiency/results/reference-v1/evaluation.json)
and [result report](evidence/benchmarks/decision-sufficiency/RESULT.md), not new
measurements made for this package.

- This is test-only evaluation data. Do not train or tune on these cases and
  then report performance on the same cases as held-out evidence. Creating a
  different row split does not remove dependence among the 12 policies per case.
- It supports analysis of frozen predictions, uncertainty and decision
  preservation. It cannot train or evaluate a text encoder by itself because
  query text is absent.
- The guarantee is bounded to the frozen probability vectors, exact finite cost
  policies, specified verifier and omitted-mass model. It does not establish
  correct real-world customer outcomes or guarantee classifier correctness.
- No demographic fairness, privacy guarantee, natural-noise robustness,
  cross-domain generalization, production suitability, autonomous authority,
  semantic compression, universal agent communication, or overall token/cost/
  energy advantage is claimed.
- No private institutional/customer dataset, model prompts, credentials, or
  personal local artifacts are included. Public-source linkability remains.

## License and citation

Dataset packaging and derived evaluation contributions are provided under
**CC BY 4.0**, with upstream BANKING77 attribution retained. Preserved source
files keep their original notices; source code and the packaging script are
MIT licensed. See [LICENSE](LICENSE), [source code license](evidence/LICENSE),
and [third-party notice](evidence/benchmarks/banking77/THIRD_PARTY_NOTICES.md).
Please credit both the upstream dataset and the derived work, link the licenses,
and identify any changes. Neither PolyAI nor the paper authors endorse this work.

> Casanueva, I., Temcinas, T., Gerz, D., Henderson, M., and Vulic, I. (2020).
> Efficient Intent Detection with Dual Sentence Encoders. Proceedings of the
> 2nd Workshop on NLP for ConvAI.

For the derived benchmark, cite William Keenan's *Waggle + Kea* repository and
the pinned commit above; [CITATION.cff](evidence/CITATION.cff) supplies metadata.
