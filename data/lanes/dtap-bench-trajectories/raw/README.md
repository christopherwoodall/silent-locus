---
license: apache-2.0
task_categories:
  - text-generation
  - reinforcement-learning
language:
  - en
tags:
  - ai-safety
  - red-teaming
  - llm-agents
  - prompt-injection
  - benchmark
  - mcp
  - agent-evaluation
pretty_name: DecodingTrust-Agent Platform (DTAP-BENCH)
size_categories:
  - 1K<n<10K
configs:
  - config_name: default
    data_files:
      - split: tasks
        path: "*/benign/**/config.yaml"
---

# DecodingTrust-Agent Platform

**A Controllable and Interactive Red-Teaming Platform for AI Agents.**

This is the full collection of the agent trajectories produced from evaluating the DTap-Bench from [DecodingTrust-Agent Platform (DTAP)](https://github.com/AI-secure/DecodingTrust-Agent),
spanning **14 real-world domains** and **50+ simulation environments** that replicate widely-used
systems such as Google Workspace, PayPal, Slack, Salesforce, Snowflake, and Databricks. Each task
ships the configuration the evaluator needs to spin up the sandbox, run an agent, and verify the
outcome — `config.yaml` (task spec + MCP server bindings), `setup.sh` (per-task environment
seeding), and `judge.py` (verifiable outcome check).

- 🌐 Website: <https://decodingtrust-agent.com>
- 📦 SDK / runner: <https://github.com/AI-secure/DecodingTrust-Agent>
- 📄 Paper: *DecodingTrust-Agent Platform (DTAP): A Controllable and Interactive Red-Teaming Platform for AI Agents.* Zhaorun Chen et al., 2026.

## What's in this dataset

| Domain | Benign tasks | Malicious tasks |
|---|---:|---:|
| browser | 34 | 167 |
| code | 330 | 286 |
| crm | 165 | 240 |
| customer-service | 160 | 201 |
| finance | 200 | 400 |
| legal | 200 | 400 |
| macos | 30 | 103 |
| medical | 642 | 451 |
| os-filesystem | 200 | 400 |
| research | 160 | 244 |
| telecom | 120 | 327 |
| travel | 130 | 225 |
| windows | 100 | 247 |
| workflow | 335 | 185 |
| **Total** | **2,806** | **3,876** |

Malicious tasks are further partitioned by **threat model** (`direct` vs. `indirect`) and
**risk category** (`data-exfiltration`, `dangerous-actions`, `invalid-consent`,
`misinformation-hallucination`, `fraud-impersonation`, `general-ai-restrictions`,
`deny-user-requests`, `manipulative-use`, ...).

## Folder layout

```
dataset/
└── <domain>/                          # one of the 14 domains above
    ├── benign/
    │   └── <task_id>/
    │       ├── config.yaml            # task spec + MCP server bindings
    │       ├── setup.sh               # seed the sandbox before the agent runs
    │       └── judge.py               # verifiable judge (task_success)
    └── malicious/
        └── <threat_model>/            # "direct" or "indirect"
            └── <risk_category>/       # e.g. "data-exfiltration"
                └── <task_id>/
                    ├── config.yaml
                    ├── setup.sh
                    └── judge.py       # verifies attack_success against the security policy
```

These paths are exactly what the `dtap eval` runner resolves task records to. For benign:
`dataset/<domain>/benign/<task_id>/`. For malicious:
`dataset/<domain>/malicious/<threat_model>/<risk_category>/<task_id>/`.

## How to use this dataset

### Option 1 — via the `dtap` CLI (recommended)

```bash
pip install decodingtrust-agent-sdk

# Download the dataset alongside your working directory
hf download AI-Secure/DecodingTrust-Agent-Platform \
  --repo-type dataset \
  --local-dir dataset

export OPENAI_API_KEY=sk-...

# Run a single benign CRM task
dtap eval \
  --task-list benchmark/crm/benign.jsonl \
  --agent-type openaisdk \
  --model gpt-4o \
  --max-parallel 4
```

The task lists under `benchmark/` (shipped with the SDK package) reference into this dataset by
`{domain, type, task_id, ...}` records. Docker sandboxes are pulled on demand by the first task
that needs them.

### Option 2 — via the Python API

```python
from huggingface_hub import snapshot_download

snapshot_download(
    "AI-Secure/DecodingTrust-Agent-Platform",
    repo_type="dataset",
    local_dir="dataset",
)
```

### Option 3 — programmatic task records

Each line in a `benchmark/<domain>/{benign,direct,indirect}.jsonl` file is a record like:

```jsonl
{"domain": "crm", "type": "benign", "task_id": "1"}
{"domain": "crm", "type": "malicious", "threat_model": "direct",   "risk_category": "dangerous-actions",  "task_id": "1"}
{"domain": "crm", "type": "malicious", "threat_model": "indirect", "risk_category": "data-exfiltration", "task_id": "1"}
```

— which resolves to the directory layout above.

## Supported domains

`browser` · `code` · `crm` · `customer-service` · `finance` · `legal` · `macos` · `medical` ·
`os-filesystem` · `research` · `telecom` · `travel` · `windows` · `workflow`

Each domain mounts one or more MCP-backed environments (Salesforce, Gmail, PayPal, Slack,
Atlassian, BigQuery, Snowflake, Databricks, GitHub, Google Docs, Booking, hospital, telecom,
terminal, Windows / macOS shells, ...). The full mapping lives in
[`dt_arena/config/mcp.yaml`](https://github.com/AI-secure/DecodingTrust-Agent/blob/main/dt_arena/config/mcp.yaml).

## License

Apache-2.0. See [`LICENSE`](https://github.com/AI-secure/DecodingTrust-Agent/blob/main/LICENSE)
on the upstream repo.

## Citation

If you find DTAP useful for your research, please cite:

```bibtex
@article{chen2026decodingtrust,
  title={DecodingTrust-Agent Platform (DTap): A Controllable and Interactive Red-Teaming Platform for AI Agents},
  author={Chen, Zhaorun and Liu, Xun and Tong, Haibo and Guo, Chengquan and Nie, Yuzhou and Zhang, Jiawei and Kang, Mintong and Xu, Chejian and Liu, Qichang and Liu, Xiaogeng and others},
  journal={arXiv preprint arXiv:2605.04808},
  year={2026}
}
```
