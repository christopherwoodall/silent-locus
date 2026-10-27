---
license: cc-by-nc-4.0
task_categories:
  - text-generation
language:
  - en
  - zh
tags:
  - agent
  - skills
  - benchmark
  - evaluation
  - claude
  - multi-domain
pretty_name: "Claude Agent Skills Benchmark"
size_categories:
  - n<1K
---

# Claude Agent Skills Benchmark

**Claude Agent Skills 评测数据集**

## Dataset Description

- **Homepage:** [obaydata.com](https://obaydata.com)
- **Organization:** New Oriental Bay Limited (obaydata)
- **Contact:** simon.su@obaydata.com

## Description

A benchmark dataset for evaluating whether LLMs can accurately trigger and execute domain-specific Skills on the Claude Code platform. Skills are designed by vertical domain experts with varying complexity levels (based on attachments: scripts, references, assets, and reference markdown files).

**Evaluation Scenarios Cover:**
Office automation, coding, investment promotion, financial services, industrial manufacturing, technology innovation, legal applications, clinical consultation, and 13+ scenario categories.

**Scoring System:**
- Coarse/fine-grained hybrid scoring
- Domain-specific quality metrics and scoring rules
- Global scoring indicators across all scenarios

**LLM Evaluation Toolkit:**
Automated extraction of interaction processes and generated content, comparison against scoring rubrics, automatic score aggregation with normalization.

**Data Production:**
Domain experts design generalizable vertical Skills steps; production tools generate professional Skills verified by experts for executability.

**Test Case Design:**
Precisely targeted test cases including single-Skill, serial, and parallel execution scenarios.

### 中文描述

给定由垂类专家设计好的Skills，在Claude Code平台上判断模型是否能够根据query准确触发与执行相应的Skills。针对不同Skills附件（scripts、references、assets）以及参考类md文件数量评估不同Skills的执行复杂度，设计复杂度不同的Skills阶梯式评测模型能力。

评测场景覆盖：办公、代码、招商、金融服务、工业制造、科技创新、法律应用、临床问诊等13类场景大类。

评分体系：粗/细粒度混合的评分方式，各个具体场景都设定专属质量指标与专属评分规则，同时也有不区分场景的全局评分指标与全局评分细则。

## Repository Structure

```
├── data/
│   └── supplementary/
│       ├── board_game_samples.pdf      # Board game evaluation samples
│       └── path_planning_samples.pdf   # Path planning evaluation samples
└── skills/
    ├── DEEPTUTOR评分数据/              # DeepTutor scoring data
    │   ├── deeptutor-skill-master/     # DeepTutor skill code (SKILL.md + scripts)
    │   ├── 数据一/                     # Test case 1: Probability & Statistics textbook (172MB PDF)
    │   │   ├── attachmeny-概率论与数理统计教程.pdf
    │   │   ├── query.txt
    │   │   └── rubric.json
    │   └── 数据二/                     # Test case 2: English 7th grade textbook (12MB PDF)
    │       ├── attachment-义务教育教科书・英语七年级上册.pdf
    │       ├── query.txt
    │       └── rubric.json
    ├── 医疗/clinical-trial-screening/  # Medical: Clinical Trial Screening
    │   ├── skill/                      # Complete skill implementation
    │   │   ├── SKILL.md               # Skill definition
    │   │   ├── config/                # YAML configs (data cleaning, risk assessment, etc.)
    │   │   ├── docs/                  # Implementation docs
    │   │   ├── knowledge/             # GCP knowledge base
    │   │   ├── scripts/               # Python pipeline scripts (6 steps)
    │   │   ├── templates/             # CSV templates
    │   │   ├── tests/                 # Unit + integration tests
    │   │   └── work/                  # Session logs from evaluation runs
    │   ├── 评分表.xlsx                 # Scoring rubric
    │   ├── 备注.txt                    # Notes
    │   ├── 输入案例-潜在受试者信息.xlsx  # Input: patient candidate info
    │   ├── 输入案例-研究项目受试标准.xlsx  # Input: trial criteria
    │   ├── 以输入案例为例启动skill的输出.md  # Output with skill enabled
    │   └── 以输入案例为例不启动skill的输出.md  # Output without skill (baseline)
    └── 法律/commercial-contract-validity/  # Legal: Commercial Contract Validity
        ├── skill/                      # Complete skill implementation
        │   ├── SKILL.md               # Skill definition
        │   ├── references/            # API reference, fonts, scripts docs
        │   ├── resources/             # Report skeleton, styles
        │   ├── scripts/               # Python pipeline (6 steps + utilities)
        │   └── 最终交付说明.md         # Final delivery notes
        ├── 评分表.xlsx                 # Scoring rubric
        ├── 备注.txt                    # Notes
        ├── 输入案例-商事合同效力争议.docx  # Input: contract dispute case
        ├── 以输入案例为例启动skill的输出.md  # Output with skill enabled
        └── 以输入案例为例不启动skill的输出.md  # Output without skill (baseline)
```

## Skills Overview

### 1. DeepTutor (教育辅导)
An intelligent tutoring skill that processes textbook PDFs and generates structured educational content. Includes graph-based knowledge retrieval and scoring rubrics for evaluation.

### 2. Clinical Trial Screening (临床试验筛选)
A medical domain skill for screening potential clinical trial participants. Implements a 3-step pipeline: data standardization → matching & risk assessment → PDF report generation. Includes GCP (Good Clinical Practice) compliance checking.

### 3. Commercial Contract Validity (商事合同效力审查)
A legal domain skill for analyzing commercial contract validity disputes. Implements a 6-step pipeline: extraction → review → law matching → validity analysis → risk planning → report export.

## Dataset Details

| Property | Value |
|----------|-------|
| **Scale** | Weekly production capacity: 20 entries |
| **Format** | JSON / Markdown Skills files / Python scripts |
| **License** | CC-BY-NC-4.0 |
| **Copyright** | Full copyright provided |
| **Domains** | Education, Medical, Legal (3 domains with complete skills) |
| **Use Case** | Evaluating LLM agent skill triggering and execution accuracy across vertical domains |

## Citation

If you use this dataset, please cite:

```bibtex
@dataset{obaydata2026,
  author = {OBayData Team},
  title = {Claude Agent Skills Benchmark},
  year = {2026},
  publisher = {HuggingFace},
  url = {https://huggingface.co/datasets/obaydata/claude-agent-skills-benchmark}
}
```
