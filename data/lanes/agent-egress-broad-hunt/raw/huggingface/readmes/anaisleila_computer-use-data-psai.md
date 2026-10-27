---
license: mit
task_categories:
- reinforcement-learning
- robotics
- video-classification
- image-to-text
- visual-question-answering
- other
tags:
- computer-use
- gui-agents
- multimodal
- human-computer-interaction
- screen-recording
- vision-language-action
- imitation-learning
- agent-training
- pretraining
- fine-tuning
- sft
- supervised-fine-tuning
- vision-language-model
- action-prediction
pretty_name: Computer Use Dataset - Paradigm Shift AI
size_categories:
- 1K<n<10K
language:
- en
---

# Computer Use Dataset - PSAI

A large-scale, multimodal dataset of human-computer interactions for training and evaluating AI agents.

[![Dataset on HuggingFace](https://img.shields.io/badge/🤗%20Dataset-HuggingFace-yellow)](https://huggingface.co/datasets/anaisleila/computer-use-data-psai)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**🔗 Access Dataset:** https://huggingface.co/datasets/anaisleila/computer-use-data-psai

---

## 📊 Dataset Overview

This dataset contains **3,167 completed tasks** of human-computer interactions captured with video, screenshots, DOM snapshots, and detailed interaction events. Created by Paradigm Shift AI for advancing computer use AI agent research.

### Key Statistics

**Scale:**
- **3,167 tasks** with multimodal data
- **7.87 GB** dataset parquet (includes embedded screenshots)
- **49.2 GB** total (7.87 GB parquet + 16.9 GB videos + 24.4 GB DOM snapshots)
- **100% video coverage** (all 3,167 tasks)

**Task Distribution:**
- **Browser Tasks:** 2,220 (70.1%)
- **Computer Tasks:** 947 (29.9%)
- **Difficulty:** Easy (79.4%) | Medium (16.7%) | Hard (3.9%)
- **Platforms:** Cross-platform (95.1%) | Windows (4.5%) | macOS (0.4%)

### Data Coverage by Modality

**Videos:** 100% coverage (3,167/3,167 tasks) - 16.9 GB  
All tasks have screen recordings in MP4 format.

**Screenshots:** 42.6% coverage (1,349/3,167 tasks)  
14,740 images embedded directly in the parquet files (included in the 7.87 GB dataset size).

**DOM Snapshots:** 55.8% coverage (1,766/3,167 tasks) - 24.4 GB  
HTML structure captures for web-based tasks.
- Browser tasks: 77.5% have DOM snapshots
- Computer tasks: 4.8% have DOM snapshots

### Content Diversity

- **294 unique websites** (browser tasks) - Amazon, Google, ArXiv, Apple, Booking, and more
- **173 unique applications** (computer tasks) - MS Office Suite, File Explorer, Email clients, and more
- **31 subcategories** spanning:
  - Search & Research (928 | 29.3%)
  - Shopping & E-commerce (490 | 15.5%)
  - Social Media & Communication (210 | 6.6%)
  - News & Media (149 | 4.7%)
  - Document Editing (127 | 4.0%)
  - Education & Learning (101 | 3.2%)
  - Navigation & Maps (93 | 2.9%)
  - Email Ops (71 | 2.2%)
  - And 23 more categories...

---

## 🚀 Quick Start

### Option 1: Load Dataset Only (7.87 GB)
Fast access to metadata and embedded screenshots:

```python
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("anaisleila/computer-use-data-psai")

# Access a task
task = dataset['train'][0]
print(f"Task: {task['task_name']}")
print(f"Category: {task['category']}")
print(f"Screenshots: {len(task['screenshots'])} images")
```

### Option 2: Download Videos & DOMs On-Demand
Download specific files as needed:

```python
from huggingface_hub import hf_hub_download

# Download a specific video
video_path = hf_hub_download(
    repo_id="anaisleila/computer-use-data-psai",
    filename=task['video_file'],  # e.g., "videos/{task_id}.mp4"
    repo_type="dataset"
)

# Download DOM snapshot
dom_path = hf_hub_download(
    repo_id="anaisleila/computer-use-data-psai",
    filename=task['dom_snaps_file'],  # e.g., "dom_snaps/{task_id}.zip"
    repo_type="dataset"
)
```

### Option 3: Clone Full Dataset (49.2 GB)
Clone everything including videos and DOM files:

```bash
git lfs install
git clone https://huggingface.co/datasets/anaisleila/computer-use-data-psai
```

---

## 📚 What's in Each Task

Each task includes:

### Metadata Fields
- **unique_data_id** (string): Unique identifier for each recording
- **taskId** (string): Task template ID (non-unique - same task done by different vendors)
- **task_name** (string): Human-readable task description
- **category** (string): `BROWSER_TASK` or `COMPUTER_TASK`
- **subCategory** (list[string]): Specific categories (e.g., "Search & Research")
- **application_website** (string): Application or website used
- **tags** (list[string]): Descriptive tags
- **benchmark** (string): Benchmark identifier
- **appType** (string): `SINGLE_APP` or `MULTI_APP`
- **difficulty** (string): `EASY`, `MEDIUM`, or `HARD`
- **os** (string): `CROSS_PLATFORM`, `WINDOWS`, `macOS`, or `LINUX`
- **requires_login** (string): Whether task requires authentication
- **completedAt** (string): Timestamp (ISO 8601 format)

### Multimodal Data
- **screenshots** (list[images]): Screenshots at key moments - **embedded and viewable**
- **video_file** (string): Path to screen recording (MP4) - download on demand
- **dom_snaps_file** (string): Path to HTML DOM snapshot (ZIP) - download on demand
- **events** (string): Keyboard/mouse interactions with timestamps (JSON)
- **reasoning_steps** (list[string]): Step-by-step task completion reasoning
- **metadata** (string): System info (OS, screen resolution, hardware) (JSON)

**Note:** Screenshots are embedded for instant browsing. Videos and DOM snapshots are stored separately to keep the dataset size manageable.

---

## 💡 Usage Examples

### 1. Browse and Explore Tasks
```python
from datasets import load_dataset
import json

dataset = load_dataset("anaisleila/computer-use-data-psai")

# Browse tasks
for task in dataset['train'][:5]:
    print(f"Task: {task['task_name']}")
    print(f"  Category: {task['category']}")
    print(f"  Difficulty: {task['difficulty']}")
    
    # Parse metadata
    metadata = json.loads(task['metadata'])
    print(f"  System: {metadata.get('system')}")
    
    # Parse events
    if task['events']:
        events = json.loads(task['events'])
        print(f"  Events: {len(events)} interactions")
```

### 2. Filter by Criteria
```python
# Filter by difficulty
hard_tasks = dataset['train'].filter(lambda x: x['difficulty'] == 'HARD')
print(f"Hard tasks: {len(hard_tasks)}")

# Filter by category
browser_tasks = dataset['train'].filter(lambda x: x['category'] == 'BROWSER_TASK')

# Complex filter
windows_hard = dataset['train'].filter(
    lambda x: x['difficulty'] == 'HARD' and x['os'] == 'WINDOWS'
)
```

### 3. Download Files for Specific Tasks
```python
from huggingface_hub import hf_hub_download

# Find a task you're interested in
task = dataset['train'][0]

# Download video
video = hf_hub_download(
    repo_id="anaisleila/computer-use-data-psai",
    filename=task['video_file'],
    repo_type="dataset"
)

# Download DOM snapshot (if available)
if task['dom_snaps_file']:
    dom = hf_hub_download(
        repo_id="anaisleila/computer-use-data-psai",
        filename=task['dom_snaps_file'],
        repo_type="dataset"
    )
```

---

## 🎯 Use Cases

This dataset supports:
- **Training computer use AI agents** (vision-language-action models)
- **Reinforcement learning** for GUI interaction
- **Benchmark evaluation** of computer use capabilities
- **Research** in human-computer interaction patterns
- **Accessibility tools** development
- **Software testing** and quality assurance automation

---

## 📖 Dataset Details

### Data Collection

Data was collected using a custom-built computer interaction capture tool that records:
- Keyboard and mouse inputs with timestamps
- Full screen video recordings
- DOM snapshots for web-based tasks
- Accessibility tree information
- Detailed event streams

Human vendors performed tasks following specific instructions. All vendors signed disclosure agreements authorizing public release of the data.

### Privacy & Consent

- Data collected from consenting human vendors
- Vendors signed disclosure agreements for public release
- May contain some PII from vendor interactions
- Users should be aware tasks may show personal information

### Known Limitations

- Some tasks may reference applications or websites that have changed since data collection
- Not all tasks have screenshots or DOM snapshots (see coverage stats above for exact percentages)
- **Dataset contains 100 duplicate rows** (3,267 total rows, 3,167 unique tasks)
  - To deduplicate: `dataset.to_pandas().drop_duplicates(subset=['unique_data_id'], keep='first')`

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for full details.

```
Copyright (c) 2025 Paradigm Shift AI
Anais Howland, Ashwin Thinnappan, Jameel Shahid Mohammed
```

---

## 🙏 Citation

If you use this dataset in your research, please cite:

```bibtex
@dataset{psai_computer_use_2025,
  title={Computer Use Data - Paradigm Shift AI},
  author={Anais Howland and Ashwin Thinnappan and Jameel Shahid Mohammed},
  organization={Paradigm Shift AI},
  year={2025},
  publisher={HuggingFace},
  url={https://huggingface.co/datasets/anaisleila/computer-use-data-psai}
}
```

---

## 👥 Authors

**Anais Howland**, **Ashwin Thinnappan**, and **Jameel Shahid Mohammed**  
Paradigm Shift AI

This dataset was created by the team at Paradigm Shift AI, including:
- Data collection infrastructure and vendor coordination system
- Custom screen recording and interaction capture tool
- Dataset curation, validation, and quality assurance

---

## 📞 Contact & Contributions

This dataset is provided as-is for the research community. 

For questions or issues:
- Open a discussion on the [HuggingFace dataset page](https://huggingface.co/datasets/anaisleila/computer-use-data-psai)
- Contact: anaisaddad@gmail.com

---

## 📋 Changelog

- **v1.0 (2025):** Initial public release with 3,167 tasks
