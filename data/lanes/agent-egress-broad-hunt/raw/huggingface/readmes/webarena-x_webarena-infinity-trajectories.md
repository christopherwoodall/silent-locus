---
license: mit
task_categories:
  - visual-question-answering
  - image-to-text
tags:
  - browser-agent
  - web-navigation
  - trajectories
  - gui-grounding
pretty_name: "WebArena-Infinity: Browser Agent Trajectories"
size_categories:
  - 1K<n<10K
---

# WebArena-Infinity: Browser Agent Trajectories

Successful browser-agent trajectories collected from the [WebArena-Infinity](https://github.com/web-arena-x/webarena-infinity) benchmark. WebArena-Infinity is a scalable approach for automatically generating realistic web environments paired with verifiable tasks, enabling robust training and evaluation of general-purpose browser agents. Each trajectory records a browser agent completing a real web-application task — including step-by-step screenshots, agent reasoning, and actions.

## Dataset Summary

| | Gemini 2.5 Flash | Kimi K2.5 | Qwen 2.5 VL Plus | Total |
|---|---|---|---|---|
| Trajectories | 978 | 643 | 708 | 2,329 |
| Environments | 13 | 13 | 13 | 13 |

**Difficulty breakdown:** 604 easy, 508 medium, 1,217 hard.

Trajectories span 13 auto-generated web-application environments sourced from real product documentation (Gmail, GitLab, PayPal, Xero, Elation EHR, Superhuman, Handshake, Linear, Figma).

## Data Layout

The dataset is stored as raw files (no parquet). Each trajectory is a directory:

```
data/
├── manifest.json              # Index of all 2,329 trajectories with metadata
├── gemini/
│   └── {environment}/
│       └── {task_id}/
│           ├── history.json       # Agent reasoning + actions per step
│           ├── result.json        # Task result (pass/fail, timing, final answer)
│           └── screenshots/
│               ├── step_1.png     # Screenshot after step 1
│               ├── step_2.png
│               └── ...
├── kimi/
│   └── ...
└── qwen/
    └── ...
```

### manifest.json

The manifest is the entry point. Each entry contains:

```json
{
  "model": "gemini",
  "environment": "gmail",
  "task_id": "task_e1",
  "difficulty": "easy",
  "instruction": "Star the email from Sarah Chen.",
  "elapsed": 32.3,
  "steps": 4,
  "verifier_message": "Email from Sarah Chen is now starred."
}
```

### result.json

Per-task result with verifier output:

```json
{
  "task_id": "task_e1",
  "difficulty": "easy",
  "instruction": "Switch the interface to dark mode.",
  "passed": true,
  "verifier_message": "Interface theme is set to Dark.",
  "elapsed": 41.7,
  "steps": 5,
  "is_done": true,
  "final_result": "I have successfully switched the interface to dark mode..."
}
```

## Agent Formats

The `history.json` file stores the original agent output. The format differs by model.

### Gemini 2.5 Flash (`browser_use`)

Gemini uses the [Browser Use](https://github.com/browser-use/browser-use) harness, interacting via DOM element indices (not pixel coordinates). It receives a text-based accessibility representation of the page.

```json
{
  "history": [
    {
      "model_output": {
        "evaluation_previous_goal": "Start",
        "memory": null,
        "next_goal": "Navigate to settings",
        "action": [{"click": {"index": 1177}}]
      },
      "result": [{"is_done": false, "extracted_content": "..."}],
      "state": {"url": "http://...", "title": "..."},
      "metadata": {"step_number": 0, "step_start_time": ..., "step_end_time": ...}
    }
  ]
}
```

**Action types:** `click`, `navigate`, `input_text`, `scroll_down`, `scroll_up`, `done` — all reference DOM elements by `index`.

### Kimi K2.5 / Qwen 2.5 VL Plus (`vision_agent`)

Vision-based agents that interact via pixel coordinates on screenshots.

```json
{
  "format": "vision_agent",
  "history": [
    {
      "thought": "Click on the star icon next to Sarah Chen's email.\n## Code:\n```python\npyautogui.click(x=0.018, y=0.175)\n```",
      "actions": [{"type": "click", "x": 35, "y": 189}]
    }
  ]
}
```

**Action types:** `click`, `type`, `scroll`, `terminate` — with absolute pixel coordinates `x`, `y`.

### Key differences

| | Gemini (`browser_use`) | Kimi/Qwen (`vision_agent`) |
|---|---|---|
| Input modality | Text (DOM tree) | Vision (screenshot) |
| Action targeting | DOM element index | Pixel coordinates (x, y) |
| Thought structure | Structured (eval + memory + goal) | Free-form text |
| Extra fields | `state`, `metadata`, `result` | — |

## How to Use

### Loading trajectories

```python
import json
from pathlib import Path
from huggingface_hub import snapshot_download

# Download dataset
local_dir = snapshot_download("webarena-x/webarena-infinity-trajectories", repo_type="dataset")
data_dir = Path(local_dir) / "data"

# Load manifest
manifest = json.loads((data_dir / "manifest.json").read_text())
print(f"{len(manifest)} trajectories")

# Iterate trajectories
for entry in manifest:
    task_dir = data_dir / entry["model"] / entry["environment"] / entry["task_id"]

    # Load agent history
    history = json.loads((task_dir / "history.json").read_text())

    # Load screenshots
    screenshots = sorted(
        (task_dir / "screenshots").glob("step_*.png"),
        key=lambda p: int(p.stem.split("_")[1]),
    )

    print(f"[{entry['model']}] {entry['instruction']}")
    print(f"  {entry['steps']} steps, {entry['elapsed']:.1f}s, {len(screenshots)} screenshots")
```

### Converting to a trajectory dataset (e.g., for training)

```python
import json
from pathlib import Path
from PIL import Image

def load_as_trajectory(data_dir: Path, entry: dict) -> dict:
    """Convert a raw trajectory into a training-ready format."""
    task_dir = data_dir / entry["model"] / entry["environment"] / entry["task_id"]
    raw = json.loads((task_dir / "history.json").read_text())
    is_vision = raw.get("format") == "vision_agent"

    screenshots = sorted(
        (task_dir / "screenshots").glob("step_*.png"),
        key=lambda p: int(p.stem.split("_")[1]),
    )

    steps = []
    for i, step in enumerate(raw.get("history", [])):
        if is_vision:
            # Kimi / Qwen: thought + pixel-coordinate actions
            thought = step.get("thought", "")
            actions = step.get("actions", [])
        else:
            # Gemini: structured model_output with DOM-index actions
            mo = step.get("model_output", {})
            thought = "\n".join(filter(None, [
                mo.get("evaluation_previous_goal"),
                mo.get("memory"),
                mo.get("next_goal"),
            ]))
            actions = mo.get("action", [])

        # Load corresponding screenshot if available
        screenshot = None
        if i < len(screenshots):
            screenshot = Image.open(screenshots[i])

        steps.append({
            "thought": thought,
            "actions": actions,
            "screenshot": screenshot,
        })

    return {
        "id": f"{entry['model']}_{entry['environment']}_{entry['task_id']}",
        "instruction": entry["instruction"],
        "difficulty": entry["difficulty"],
        "model": entry["model"],
        "environment": entry["environment"],
        "steps": steps,
    }
```

### Filtering

```python
# Only hard tasks
hard = [e for e in manifest if e["difficulty"] == "hard"]

# Only vision-agent trajectories (Kimi + Qwen)
vision = [e for e in manifest if e["model"] in ("kimi", "qwen")]

# Only a specific environment
gmail = [e for e in manifest if e["environment"] == "gmail"]
```

## Environments

| Environment | Domain | Source |
|---|---|---|
| `elation-clinical-records` | Healthcare | Elation EHR |
| `elation-patient-communication` | Healthcare | Elation EHR |
| `elation-prescriptions` | Healthcare | Elation EHR |
| `figma-slides` | Design | Figma |
| `figma-text-and-typography` | Design | Figma |
| `gitlab-plan-and-track` | DevOps | GitLab |
| `gmail` | Productivity | Gmail |
| `gmail-accounts-and-contacts` | Productivity | Gmail |
| `handshake-career-exploration` | Careers | Handshake |
| `linear-account-settings` | Project Mgmt | Linear |
| `paypal-my-wallet` | Finance | PayPal |
| `superhuman-general` | Productivity | Superhuman |
| `xero-invoicing` | Finance | Xero |

## Construction

This dataset was built from the [WebArena-Infinity](https://github.com/web-arena-x/webarena-infinity) pipeline. Each trajectory represents a successful task completion from a 3-repetition final evaluation run. Only passing trajectories (verified by programmatic verifiers that check application state) are included.

## Citation

```bibtex
@article{zhou2026wainf,
  title   = "WebArena-Infinity: Generating Browser Environments with Verifiable Tasks at Scale",
  author  = "Shuyan Zhou",
  journal = "shuyanzhou.com",
  year    = "2026",
  month   = "March",
  url     = "https://webarena.dev/webarena-infinity/"
}
```
