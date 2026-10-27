---
license: apache-2.0
pretty_name: OSWorld V2 Task Classes
---

# OSWorld V2 Task Classes

This gated dataset contains the official root-level `task_*.py` Python task classes for OSWorld V2.

The public GitHub repository keeps the task loader, helper utilities, and documentation. The task implementations are gated to reduce benchmark leakage and to help prevent evaluated agents from finding task answers, setup logic, or evaluator details online while executing a task.

Download from the public repository root with:

```bash
uvx --from huggingface_hub hf auth login
uv run scripts/download_osworld_v2_tasks.py
```

Re-running the script overwrites local `task_*.py` files and removes stale task files by default. The deprecated `backup/` and `prev_tasks` folders are not included here.
