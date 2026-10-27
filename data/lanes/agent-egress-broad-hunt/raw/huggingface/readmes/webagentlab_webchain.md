---
pretty_name: WebChain v2
license: cc-by-4.0
license_link: LICENSE
size_categories:
  - 10K<n<100K
tags:
  - web-agent
  - gui-agent
  - multimodal
  - trajectory
  - grounding
  - planning
  - accessibility-tree
  - screenshot
  - reinforcement-learning
  - supervised-fine-tuning
---

# WebChain v2

**A large-scale, human-annotated dataset of real-world web interaction trajectories for training and evaluating web agents.**

[[Paper](https://arxiv.org/abs/2603.05295)] [[Code](https://github.com/sicheng-fan/WebChain)] [[Dataset](https://huggingface.co/datasets/webagentlab/webchain)]

WebChain captures how people complete real tasks on live websites. It is designed for agents that must both identify the correct interface element and reason through a sequence of actions. Each trajectory aligns screenshots, web structure, grounded actions, and reasoning signals instead of treating web navigation as text-only imitation.

This repository is the cleaned, training-ready v2 release. You can use it directly for multimodal supervised fine-tuning, Seed/Demo-style GUI-agent training, data analysis, and offline evaluation without first reconstructing the original raw archives.

## Why WebChain?

Real-world web agents need two complementary capabilities:

1. **Spatial grounding** — locate the correct element on a visually dense page and produce the right coordinates or text argument.
2. **Long-horizon planning** — choose the next action from the task goal, current screenshot, and previous interaction history.

WebChain provides **Triple Alignment** across:

- **Visual context:** viewport and full-page screenshots;
- **Structural context:** HTML/DOM and Accessibility (AX) tree information;
- **Action grounding:** action types, pixel coordinates, bounding boxes, selectors, text arguments, and timestamps.

The accompanying paper also studies a **Dual Mid-Training** recipe that separates spatial grounding from planning. The experiments show that scaling human-verified trajectories improves long-horizon performance and that the proposed training recipe achieves state-of-the-art results on WebChainBench and public GUI benchmarks.

## Dataset at a glance

| Metric | Current v2 release |
|---|---:|
| Cleaned source trajectories | 31,675 |
| Raw interaction steps | 317,682 |
| Trace-level SFT rows | 31,675 |
| Seed/Demo sliding-window rows | 39,332 |
| SFT image/action turns | 263,995 |
| Data parts | 48 |
| SFT Parquet shards per format | 71 |
| Trace SFT indexed size | approximately 192.62 GB |
| Seed/Demo indexed size | approximately 193.39 GB |
| Evaluation subset | 150 traces |

The paper reports statistics for the full collected corpus before final release cleaning: 31,725 trajectories, 317,993 steps, 428 domains, an average trajectory length of 10.02 steps, and an average duration of 1.07 minutes. The downloadable v2 counts above are the authoritative counts for this repository.

## How the data was built

The paper describes a three-stage construction pipeline:

1. **Constraint-based task synthesis**
   - Extract a structured schema of each website's actual functionality.
   - Generate executable tasks within that schema rather than hallucinating unsupported website features.
   - Cover simple information retrieval, multi-constraint navigation, and conditional-dependency tasks.
2. **Human-in-the-loop trajectory collection**
   - Human annotators complete tasks on live websites.
   - The collection system records screenshots, DOM state, actions, coordinates, bounding boxes, selectors, and other step-level context.
3. **Post-processing contextual enrichment**
   - Densify visual grounding annotations across visible interactive elements.
   - Add trajectory-aware rationales for planning supervision.
   - Clean, convert, shard, index, and validate the final training release.

## Repository structure

```text
webchain/
├── README.md
├── LICENSE
└── data/
    ├── trace_sft/                    # Recommended general-purpose format
    │   ├── README.md
    │   ├── parts/part_00 ... part_47/
    │   │   ├── sft/*.parquet
    │   │   ├── metadata/*.parquet
    │   │   └── validation_summary.json
    │   ├── test_suite_150/
    │   ├── dataset_index.json
    │   ├── validation_summary.json
    │   └── MANIFEST.sha256
    └── seed_sft/                     # Seed/Demo tool-call format
        ├── README.md
        ├── parts/part_00 ... part_47/
        │   ├── sft/*.parquet
        │   ├── metadata/*.parquet
        │   └── validation_summary.json
        ├── metadata/
        ├── test_suite_150/
        ├── tools/
        ├── rl_reward_spec.md
        ├── dataset_index.json
        ├── validation_summary.json
        ├── verify_summary.json
        └── MANIFEST.sha256
```

## Which format should I use?

| Goal | Recommended path | Why |
|---|---|---|
| Train a general multimodal web agent | `data/trace_sft/` | One complete multi-turn SFT row per cleaned trajectory |
| Train a Seed/Demo-compatible GUI agent | `data/seed_sft/` | Seed XML tool calls, normalized points, and bounded sliding windows |
| Inspect trace/action statistics | `data/seed_sft/metadata/` | Consolidated trace-, action-, and window-level tables |
| Run a small evaluation or pipeline smoke test | `data/seed_sft/test_suite_150/` | Matching SFT rows and metadata for 150 stratified traces |
| Design RL or trajectory rewards | `data/seed_sft/rl_reward_spec.md` | Format, action, coordinate, text, sequence, and environment reward notes |

If you are unsure, start with **Trace SFT**. Use **Seed/Demo SFT** when your model or training framework expects Seed GUI function calls or when sliding-window samples are easier to fit into your context budget.

## SFT file format

All training shards are SNAPPY-compressed Parquet files with the same three top-level columns:

| Column | Parquet type | Description |
|---|---|---|
| `uid` | string | A trace UID, or `{trace_uid}::w{index}` for a Seed/Demo window |
| `images` | list&lt;binary&gt; | Ordered viewport PNG bytes used by the conversation |
| `inputs` | string | A JSON-encoded list of multi-turn conversation items |

After parsing `inputs` with `json.loads`, the conceptual structure is:

```json
[
  {"type": "special_token", "text": "[CLS]", "has_loss": 0},
  {"type": "special_token", "text": "user\n", "has_loss": 0},
  {"type": "text", "text": "<task or observation>", "has_loss": 0},
  {
    "type": "image",
    "image_index": 0,
    "width": 1280,
    "height": 720,
    "has_loss": 0
  },
  {"type": "special_token", "text": "[EOS]", "has_loss": 0},
  {"type": "special_token", "text": "[CLS]", "has_loss": 0},
  {"type": "special_token", "text": "assistant\n", "has_loss": 0},
  {"type": "text", "text": "<reasoning and action>", "has_loss": 1},
  {"type": "special_token", "text": "[EOS]", "has_loss": 1}
]
```

This example illustrates the schema rather than reproducing a particular dataset row. The `image_index` points into the row's `images` list.

### Loss-mask convention

- assistant payload text and assistant `[EOS]`: `has_loss=1`;
- assistant role tokens: `has_loss=0`;
- user/tool content, images, and other non-assistant items: `has_loss=0`.

### Trace SFT

Trace SFT preserves the trajectory as a complete multi-turn conversation. Each of the 31,675 cleaned trajectories produces one SFT row. It is appropriate for learning long-horizon state/action histories and trajectory-level planning.

Files:

```text
data/trace_sft/parts/part_*/sft/*.parquet
```

The part-level metadata includes:

- `traces.parquet`: one row per source trajectory;
- `actions.parquet`: one row per raw interaction step;
- `validation_rows.parquet`: per-trace validation counters;
- `action_counts.tsv` and `exclude_reasons.tsv`: action and filtering summaries.

See [`data/trace_sft/README.md`](data/trace_sft/README.md) for action distributions and package validation results.

### Seed/Demo SFT

Seed/Demo SFT converts the same source trajectories into 39,332 bounded sliding-window rows. Assistant turns use Seed GUI XML:

```xml
<gui_think>Reason about the current page and the next action.</gui_think>
<seed:tool_call>
  <function name="click">
    <parameter name="point" string="true">
      <point>512 384</point>
    </parameter>
  </function>
</seed:tool_call>
```

Point coordinates are integers normalized to the 0–1000 range:

```text
round(pixel_coordinate / image_dimension * 1000)
```

The release maps raw actions into the Seed action space, including `click`, `type`, `hotkey`, `left_double`, `right_single`, and `drag`. Exact mappings and counts are recorded in `data/seed_sft/metadata/action_mapping.tsv`.

See [`data/seed_sft/README.md`](data/seed_sft/README.md) for the complete format, metadata columns, and verification commands.

## Metadata

The consolidated Seed/Demo metadata is the easiest entry point for analysis:

| File | Granularity | Examples of included information |
|---|---|---|
| `metadata/traces.parquet` | one row per trace | query, intent type, host, web type, action/image counts, source IDs, DOM/AX URLs |
| `metadata/actions.parquet` | one row per action | raw action, Seed function, normalized coordinates, bbox, selector, href, provenance |
| `metadata/windows.parquet` | one row per SFT window | source turn span, image count, estimated image tokens, action types, output shard |
| `metadata/intent_taxonomy.tsv` | intent taxonomy | simple IR, multi-constraint, and conditional tasks |

CSV versions of the main trace, action, and window tables are also provided for quick inspection.

## Quick start

### 1. Install the dependencies

The dataset is public and ungated. No access request, Hugging Face account, or access token is required.

```bash
pip install -U datasets huggingface_hub pyarrow
```

### 2. Load Trace SFT

```python
from datasets import load_dataset

repo = "webagentlab/webchain"
trace_sft = load_dataset(
    "parquet",
    data_files={
        "train": (
            f"hf://datasets/{repo}/"
            "data/trace_sft/parts/part_*/sft/*.parquet"
        )
    },
    split="train",
)

print(trace_sft)
print(trace_sft.column_names)  # ['uid', 'images', 'inputs']
```

Loading every shard transfers roughly 193 GB. For a first test, load one part:

```python
sample = load_dataset(
    "parquet",
    data_files=(
        f"hf://datasets/{repo}/"
        "data/trace_sft/parts/part_00/sft/*.parquet"
    ),
    split="train",
)
```

### 3. Decode a row

```python
import io
import json
from PIL import Image

row = sample[0]
turns = json.loads(row["inputs"])
images = [Image.open(io.BytesIO(blob)) for blob in row["images"]]

print("uid:", row["uid"])
print("conversation items:", len(turns))
print("images:", len(images))
print("first item:", turns[0])
```

### 4. Load Seed/Demo SFT

```python
seed_sft = load_dataset(
    "parquet",
    data_files={
        "train": (
            f"hf://datasets/{repo}/"
            "data/seed_sft/parts/part_*/sft/*.parquet"
        )
    },
    split="train",
)
```

### 5. Load metadata only

```python
traces = load_dataset(
    "parquet",
    data_files=f"hf://datasets/{repo}/data/seed_sft/metadata/traces.parquet",
    split="train",
)

actions = load_dataset(
    "parquet",
    data_files=f"hf://datasets/{repo}/data/seed_sft/metadata/actions.parquet",
    split="train",
)
```

### 6. Start with the 150-trace subset

```python
test_suite = load_dataset(
    "parquet",
    data_files=(
        f"hf://datasets/{repo}/"
        "data/seed_sft/test_suite_150/sft/test_suite_150.parquet"
    ),
    split="train",
)
```

The subset contains 50 short, 50 medium, and 50 long trajectories, with controlled host and source-file diversity. It is useful for verifying a data loader or running a compact offline evaluation before downloading the full release.

## Verification and integrity

Each package includes SHA-256 manifests, file-size/row-count indexes, part-level validation summaries, and package-level verification results.

After cloning or downloading `data/seed_sft/`, run:

```bash
python data/seed_sft/tools/verify_seed_delivery.py \
  --root data/seed_sft \
  --workers 8 \
  --output data/seed_sft/verify_summary.json
```

Verify only the evaluation subset:

```bash
python data/seed_sft/tools/verify_seed_delivery.py \
  --root data/seed_sft \
  --test-suite-only \
  --output data/seed_sft/test_suite_150/verify_summary.json
```

The verifier checks the SFT schema, image metadata, loss masks, Seed XML, allowed function names, coordinate ranges, action-metadata agreement, and sliding-window image-token budgets.

## Intended use and responsible use

WebChain supports applications including:

- web and GUI agents;
- multimodal supervised fine-tuning;
- spatial grounding and action localization;
- long-horizon planning and agentic reasoning;
- reward modeling and reinforcement-learning warm starts;
- offline evaluation and dataset analysis.

Users are responsible for complying with website terms, privacy obligations, applicable law, and the dataset license. Do not attempt to recover personal information, credentials, or other sensitive data.

## Open access and license

WebChain is released under the [Creative Commons Attribution 4.0 International License](LICENSE). See the license and its [official legal code](https://creativecommons.org/licenses/by/4.0/legalcode) for the applicable permissions and attribution requirements. The dataset is public and ungated.

For privacy/redaction reports, attribution questions, or other policy questions, contact **Fan Sicheng** at **sicheng_fan@foxmail.com**.

## Citation

```bibtex
@article{fan2026webchain,
  title   = {WebChain: A Large-Scale Human-Annotated Dataset of Real-World Web Interaction Traces},
  author  = {Sicheng Fan and Rui Wan and Yifei Leng and Gaoning Liang and Li Ling and Yanyi Shang and Dehan Kong},
  journal = {arXiv preprint arXiv:2603.05295},
  year    = {2026}
}
```

## Acknowledgements

We thank the annotators, collaborators, and institutions who supported the creation and release of WebChain.

## v2 release notes and comparison with v1

The current repository is a cleaned, validated, training-ready release. Researchers who need the information-rich original artifacts—including raw JSON records, viewport images, partial full-page screenshots, and the earlier high-/low-level Parquet formulations—can access the **[original WebChain release (`webagentlab/webchain-legacy`)](https://huggingface.co/datasets/webagentlab/webchain-legacy)**.

Use v2 for new training pipelines and reproducible validation. Use the original release when your work requires the least-processed source artifacts or the original task formulations.

| Area | v1 | v2 |
|---|---|---|
| Trajectories | 31,725 | 31,675 cleaned trajectories |
| Raw steps | 317,993 | 317,682 cleaned steps |
| Main delivery | split raw archives plus high/low Parquet files | Trace SFT plus Seed/Demo sliding-window SFT |
| Training schema | multiple task-specific formulations | consistent `uid`, `images`, `inputs` schema |
| Images | separate split archives | ordered PNG bytes aligned inside each SFT row |
| Loss masks | not standardized in the release | explicit per-item `has_loss` values |
| Metadata | limited release-level structure | trace-, action-, window-, and validation-level tables |
| Evaluation | high/low test Parquet files | stratified 150-trace subset with matching SFT and metadata |
| Integrity | Git/LFS delivery | SHA-256 manifests, indexes, validation summaries, and verifier |
| Tooling | no packaged verifier | sampler, structure-URL checker, package verifier, and RL reward notes |
