---
license: mit
tags:
- swe-bench
- harbor
- swe-bench-verified
---

# swebench-verified-mini-swe-agent-gpt41mini-test

Harbor evaluation on swebench-verified@1.0: 0/1 resolved (0.0%), 0 errors

## Dataset Info

- **Rows**: 1
- **Columns**: 25

## Columns

| Column | Type | Description |
|--------|------|-------------|
| instance_id | Value('string') | Task identifier (e.g. astropy__astropy-12907) |
| reward | Value('float64') | Verifier reward (e.g. 0.0 or 1.0) |
| resolved | Value('bool') | Whether the task was resolved (reward > 0) |
| agent | Value('string') | Agent name used for this trial |
| model | Value('string') | Model identifier used by the agent |
| started_at | Value('string') | Trial start timestamp (ISO 8601) |
| finished_at | Value('string') | Trial end timestamp (ISO 8601) |
| duration_seconds | Value('float64') | Wall clock duration of the trial |
| error | Value('null') | Exception message if the trial failed, null otherwise |
| trajectory | Value('string') | ATIF (Agent Trajectory Interchange Format) JSON trace of the agent's actions |
| trajectory_raw | Value('string') | Native agent trajectory JSON (agent-specific format) |
| agent_output | Value('string') | Raw text output from the agent |
| agent_command | Value('string') | Shell command executed by the agent |
| agent_stdout | Value('string') | Stdout from the agent's command execution |
| agent_return_code | Value('int64') | Return code from the agent's command execution |
| setup_stdout | Value('string') | Stdout from the agent environment setup |
| setup_stderr | Value('string') | Stderr from the agent environment setup |
| setup_return_code | Value('int64') | Return code from the agent environment setup |
| verifier_stdout | Value('string') | Stdout from the verifier test execution |
| verifier_report | Value('string') | Verifier report JSON with FAIL_TO_PASS and PASS_TO_PASS results |
| trial_config | Value('string') | Trial-level configuration JSON |
| trial_result | Value('string') | Trial-level result JSON (full Harbor trial output) |
| trial_log | Value('string') | Trial-level log text |
| job_config | Value('string') | Job-level configuration JSON |
| job_log | Value('string') | Job-level log text |


## Generation Parameters

```json
{
  "script_name": "harbor_toolkit",
  "model": "mini-swe-agent (gpt-4.1-mini)",
  "description": "Harbor evaluation on swebench-verified@1.0: 0/1 resolved (0.0%), 0 errors",
  "hyperparameters": {
    "job_name": "2026-02-20__15-53-32",
    "jobs_dir": "jobs",
    "n_attempts": 1,
    "timeout_multiplier": 5.0,
    "debug": false,
    "orchestrator": {
      "type": "local",
      "n_concurrent_trials": 1,
      "quiet": false,
      "retry": {
        "max_retries": 0,
        "include_exceptions": null,
        "exclude_exceptions": [
          "VerifierTimeoutError",
          "AgentTimeoutError",
          "RewardFileNotFoundError",
          "VerifierOutputParseError",
          "RewardFileEmptyError"
        ],
        "wait_multiplier": 1.0,
        "min_wait_sec": 1.0,
        "max_wait_sec": 60.0
      },
      "kwargs": {}
    },
    "environment": {
      "type": "daytona",
      "import_path": null,
      "force_build": false,
      "delete": true,
      "override_cpus": null,
      "override_memory_mb": null,
      "override_storage_mb": null,
      "override_gpus": null,
      "suppress_override_warnings": false,
      "kwargs": {}
    },
    "verifier": {
      "override_timeout_sec": null,
      "max_timeout_sec": null,
      "disable": false
    },
    "metrics": [],
    "agents": [
      {
        "name": "mini-swe-agent",
        "import_path": null,
        "model_name": "openai/gpt-4.1-mini",
        "override_timeout_sec": null,
        "override_setup_timeout_sec": null,
        "max_timeout_sec": null,
        "kwargs": {}
      }
    ],
    "datasets": [
      {
        "task_names": [
          "matplotlib__matplotlib-13989"
        ],
        "exclude_task_names": null,
        "n_tasks": null,
        "registry": {
          "name": null,
          "url": "https://raw.githubusercontent.com/laude-institute/harbor/main/registry.json"
        },
        "name": "swebench-verified",
        "version": "1.0",
        "overwrite": false,
        "download_dir": null
      }
    ],
    "tasks": []
  },
  "input_datasets": [
    "swebench-verified@1.0"
  ]
}
```

## Usage

```python
from datasets import load_dataset

dataset = load_dataset("reasoning-degeneration-dev/swebench-verified-mini-swe-agent-gpt41mini-test", split="train")
print(f"Loaded {len(dataset)} rows")
```

---

*This dataset is tracked in [reasoning-degeneration-dev/PROJECT-MANIFEST](https://huggingface.co/datasets/reasoning-degeneration-dev/PROJECT-MANIFEST)*
