---
pretty_name: WebChain
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
---

# WebChain

WebChain is a large-scale, human-annotated dataset of real-world web interaction trajectories for training and evaluating GUI agents and web agents. WebChain contains **31,725 trajectories**, **317,993 steps**, and **428 unique domains**. Its core contribution is a **Triple Alignment** of visual context, structural context, and action grounding, enabling supervision for both **spatial grounding** and **long-horizon planning**. 

Paper: https://arxiv.org/abs/2603.05295

## Open access and license

WebChain is released under the [Creative Commons Attribution 4.0 International License](LICENSE). See the license and its [official legal code](https://creativecommons.org/licenses/by/4.0/legalcode) for the applicable permissions and attribution requirements. This repository is public and ungated.

## What is included

This repository contains the WebChain dataset in both raw and processed forms. Some raw modalities in the public release are partially available, especially full-page screenshots.

```text
WebChain/
├── README.md
├── LICENSE
├── .gitattributes
├── raw/
│   ├── json/
│   ├── img/
│   └── full_screenshots/
└── processed/
    ├── high_parquet/
    └── low_parquet/
```


### Directory overview

- `raw/json/`: raw trajectory and step-level structured records.
- `raw/img/`: viewport-level images or cropped visual observations used for step grounding.
- `raw/full_screenshots/`: partial full-page screenshots aligned with step context where available. This folder is not exhaustive and does not provide full coverage for all trajectories or steps.
- `processed/high_parquet/`: processed Parquet files for high-level task formulation. Samples typically contain the user instruction, prior action history, and the current page screenshot, targeting planning and long-horizon decision-making.
- `processed/low_parquet/`: processed Parquet files for low-level step formulation. Samples typically contain the current-step instruction together with the current observation, targeting grounding and action localization.

## Dataset summary

- **31,725** human-verified trajectories
- **317,993** total interaction steps
- **428** unique domains
- Average trajectory length: **10.02** steps
- Average task duration: **1.07 minutes**

Each step may include the following modalities, depending on the release split and format:

- **Visual context**: viewport screenshots and, where available, full-page screenshots
- **Structural context**: HTML snapshots and Accessibility (AX) tree snapshots
- **Precise grounding**: element bounding boxes, CSS selectors, and pixel coordinates
- **Behavioral annotations**: action type, input text when applicable, timestamps
- **Reasoning traces**: Chain-of-Thought style rationales where included in the release

## Data construction

The paper describes a three-stage construction pipeline:

1. **Constraint-Based Task Synthesis**
   - Structured functionality extraction from target websites
   - Schema-constrained task generation to avoid unsupported or hallucinated tasks
2. **Human-in-the-Loop Trajectory Collection**
   - Human annotators execute tasks on real websites
   - Each step records state, action, and rich alignment signals
3. **Post-processing Contextual Enrichment**
   - Visual grounding densification
   - Synthetic rationale generation for planning supervision

## Intended use

WebChain is intended for research and education in:

- Web agents
- GUI grounding
- Vision-Language-Action (VLA) models
- Long-horizon planning
- Agentic reasoning on websites
- Dataset and benchmark research for multimodal agents

Potential use cases include:

- Supervised fine-tuning (SFT)
- Reward modeling or post-training
- Long-horizon planning experiments
- Benchmarking on held-out web interaction tasks

## Format note

This repository is not intended to be parsed as a single standardized Hugging Face dataset repository with one unified schema across all files. The recommended programmatic entry point is the processed Parquet release under `processed/high_parquet/` and `processed/low_parquet/`.

The raw folders are released as downloadable research artifacts and may require custom parsing scripts depending on the specific subdirectory and file type.

## Quick start

### Option A: load processed Parquet files directly

```python
from datasets import load_dataset

# Example: read all parquet shards in the higher-fidelity release
hf_repo = "webagentlab/webchain-legacy"

dataset = load_dataset(
    "parquet",
    data_files={
        "train": f"hf://datasets/{hf_repo}/processed/high_parquet/*.parquet"
    }
)

print(dataset)
print(dataset["train"][0])
```

### Option B: iterate over downloaded local shards

```python
import glob
import pandas as pd

files = sorted(glob.glob("processed/high_parquet/*.parquet"))
print(f"Found {len(files)} parquet shards")

sample = pd.read_parquet(files[0])
print(sample.head())
print(sample.columns.tolist())
```

### Option C: access raw files

You can clone or download the repository and work directly with:

- `raw/json/` for raw structured records
- `raw/img/` for viewport images
- `raw/full_screenshots/` for partial page-level images

## Example available fields

A step in WebChain may align the following information:

- task / instruction
- trajectory id
- step id
- action type
- action arguments
- click coordinates
- target bounding box
- input text
- CSS selector
- XPath or DOM reference
- AX tree snapshot
- screenshot path
- full screenshot path
- timestamp
- optional rationale / CoT

## Responsible use

You agree not to:

- attempt to re-identify individuals from the dataset;
- use the dataset in ways that violate privacy, platform rules, or applicable law;
- use or redistribute the dataset contrary to the LICENSE.

Please report any privacy, redaction, or policy issue to the maintainers.

## Citation

If you use WebChain in your work, please cite:

```bibtex
@article{fan2026webchain,
  title   = {WebChain: A Large-Scale Human-Annotated Dataset of Real-World Web Interaction Traces},
  author  = {Sicheng Fan and Rui Wan and Yifei Leng and Gaoning Liang and Li Ling and Yanyi Shang and Dehan Kong},
  journal = {arXiv preprint arXiv:2603.05295},
  year    = {2026}
}
```

## Contact

For questions, please contact:

- **Fan Sicheng**
- **sicheng_fan@foxmail.com**

## Acknowledgements

We thank the annotators, collaborators, and institutions who supported the creation and release of WebChain.
