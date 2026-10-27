---
pretty_name: LongHorizon Full Data-Agent Benchmarks
task_categories:
  - question-answering
  - tabular-classification
  - tabular-regression
  - text-generation
tags:
  - agents
  - data-analysis
  - benchmark
---

# LongHorizon Full Data-Agent Benchmarks

Companion data artifacts for five complete evaluation tracks:

- DataSciBench full55 / 167 metric entries
- DABStep full450
- DABStep-Research full100
- DSBench Modeling full74
- LongDS full68 / 2,225 turns

The companion GitHub repository contains processed manifests, evaluation code,
historical API ReAct baseline code, download/preparation tools, and the frozen
source lock. `artifact_manifest.json` records every uploaded object's size,
SHA-256, installation path, and archive contents.

DataSciBench runtime trees and DSBench extracted directories are intentionally
not duplicated here. They are reconstructed from the compact source artifacts.
DABStep leaderboard submission history is excluded; all 450 task definitions
and all seven context files are included. LongDS is split by dataset family so
downloads can resume without a monolithic 19 GB archive.

The DABStep project metric uses six official public-dev references and 444
DataCOPE Genesis proxy references. It is not an official hidden-leaderboard
full-test score.

