---
license: cc-by-4.0
task_categories:
  - video-classification
  - robotics
language:
  - en
tags:
  - screen-recording
  - computer-use
  - software-tutorials
  - gui
  - desktop
size_categories:
  - 10K<n<100K
configs:
  - config_name: autocad
    data_files:
      - split: train
        path:
          - data/autocad/*
          - data/autocad_2/*
  - config_name: blender
    data_files:
      - split: train
        path:
          - data/blender/*
          - data/blender_2/*
  - config_name: excel
    data_files:
      - split: train
        path: data/excel/*
  - config_name: photoshop
    data_files:
      - split: train
        path:
          - data/photoshop/*
          - data/photoshop_2/*
  - config_name: salesforce
    data_files:
      - split: train
        path: data/salesforce/*
  - config_name: vscode
    data_files:
      - split: train
        path: data/vscode/*
---

# Computer Use Large

A large-scale dataset of **48,478 screen recording videos** (~12,300 hours) of professional software being used, sourced from the internet. All videos have been trimmed to remove non-screen-recording content (intros, outros, talking heads, transitions) and audio has been stripped.

## Dataset Summary

| Category | Videos | Hours |
|---|---|---|
| AutoCAD | 10,059 | 2,149 |
| Blender | 11,493 | 3,624 |
| Excel | 8,111 | 2,002 |
| Photoshop | 10,704 | 2,060 |
| Salesforce | 7,807 | 2,336 |
| VS Code | 304 | 127 |
| **Total** | **48,478** | **~12,300** |

## Data Fields

Each folder contains a `metadata.jsonl` file with the following fields per video:

| Field | Type | Description |
|---|---|---|
| `file_name` | string | Filename of the video (e.g. `abc123.mp4`) |
| `category` | string | Software category |
| `trimmed_duration` | float | Duration of the video in seconds |
| `num_segments` | int | Number of contiguous screen recording segments |

## Data Organization

Videos are stored under `data/{category}/` with a `metadata.jsonl` per folder. Due to HuggingFace's 10,000 file per directory limit, some categories are split across two folders (e.g. `blender/` and `blender_2/`).

```
data/
  autocad/        (9,999 videos + metadata.jsonl)
  autocad_2/      (60 videos + metadata.jsonl)
  blender/        (9,999 videos + metadata.jsonl)
  blender_2/      (1,494 videos + metadata.jsonl)
  excel/          (8,111 videos + metadata.jsonl)
  photoshop/      (9,999 videos + metadata.jsonl)
  photoshop_2/    (705 videos + metadata.jsonl)
  salesforce/     (7,807 videos + metadata.jsonl)
  vscode/         (304 videos + metadata.jsonl)
```

## Usage

```python
from datasets import load_dataset

# Load a specific category
ds = load_dataset("markov-ai/computer-use-large", "blender")

# Load all categories
ds = load_dataset("markov-ai/computer-use-large")
```

## Intended Use

This dataset is designed for training and evaluating computer use agents — models that interact with desktop software through GUI actions (clicking, typing, scrolling). The screen recordings provide demonstrations of real software workflows across diverse applications.

## License

CC-BY-4.0
