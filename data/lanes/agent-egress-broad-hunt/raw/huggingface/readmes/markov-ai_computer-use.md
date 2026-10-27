---
license: apache-2.0
task_categories:
  - robotics
  - image-to-text
tags:
  - computer-use
  - gui-agent
  - osworld
  - trajectories
  - reinforcement-learning
size_categories:
  - n<1K
configs:
  - config_name: default
    data_files:
      - split: train
        path: data/train-*.parquet
---

# Computer Use Trajectories

Successful computer-use agent trajectories collected on [OSWorld](https://os-world.github.io/) tasks.

## Dataset Details

- **Rows**: 160 (one per task trajectory)
- **Steps**: 1,378 total across all trajectories (avg ~8.6 steps/task)
- **Agent**: Gemini 3 Flash Preview with linearized accessibility-tree grounding
- **Score filter**: Only trajectories with score = 1.0 (fully successful)

### Domains

| Domain | Tasks | Description |
|--------|-------|-------------|
| chrome | 21 | Web browsing tasks in Google Chrome |
| gimp | 15 | Image editing in GIMP |
| libreoffice_calc | 17 | Spreadsheet tasks in LibreOffice Calc |
| libreoffice_impress | 20 | Presentation tasks in LibreOffice Impress |
| libreoffice_writer | 11 | Document editing in LibreOffice Writer |
| multi_apps | 21 | Cross-application workflows |
| os | 15 | Operating system / desktop tasks |
| thunderbird | 10 | Email tasks in Thunderbird |
| vlc | 8 | Media player tasks in VLC |
| vs_code | 22 | Code editing in VS Code |

## Schema

Each row is a complete task trajectory. Per-step data is stored as parallel lists (index `i` across all list columns gives step `i`).

| Column | Type | Description |
|--------|------|-------------|
| `task_id` | string | UUID of the task |
| `domain` | string | Application domain (e.g. "chrome", "gimp") |
| `instruction` | string | Natural-language task instruction |
| `score` | float | Final task score (all 1.0 since filtered to successful) |
| `num_steps` | int | Number of steps in this trajectory |
| `actions` | list[string] | Executed pyautogui actions (Python code or JSON) |
| `responses` | list[string] | Full LLM responses including `<think>` reasoning |
| `screenshots` | list[Image] | PNG screenshots of the desktop at each step |
| `accessibility_trees` | list[string] | Linearized accessibility tree at each step |
| `exe_statuses` | list[string] | Execution status per step ("success" / "error") |
| `exe_outputs` | list[string] | Stdout from each action execution |
| `exe_errors` | list[string] | Stderr from each action execution |
| `rewards` | list[float] | Per-step reward (0 for intermediate steps) |
| `dones` | list[bool] | Whether the episode ended at each step |
| `recording_path` | string | Relative path to MP4 screen recording |

## Usage

```python
from datasets import load_dataset

ds = load_dataset("markov-ai/computer-use")

# Each row is a full trajectory
traj = ds["train"][0]
print(traj["instruction"])
print(f"{traj['num_steps']} steps")

# Iterate through steps
for i in range(traj["num_steps"]):
    screenshot = traj["screenshots"][i]
    action = traj["actions"][i]
    print(f"Step {i+1}: {action[:80]}...")

# Filter by domain
chrome_tasks = ds["train"].filter(lambda x: x["domain"] == "chrome")
```

## Recordings

MP4 screen recordings are stored in `recordings/{domain}/{task_id}.mp4`.
These are full-episode videos capturing the agent's desktop interaction.

## Source

Collected using the [ComputerRL](https://github.com/anthropics/ComputerRL) evaluation framework on OSWorld virtual machines.
