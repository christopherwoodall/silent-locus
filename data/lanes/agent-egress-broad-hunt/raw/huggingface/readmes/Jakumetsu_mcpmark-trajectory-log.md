---
license: mit
language:
- en
tags:
- agent
size_categories:
- 10K<n<100K
---

# MCPMark Trajectory Logs (mcpmark-v1-0905)

These logs are publicly available for research use. They capture end-to-end trajectories (prompts, tool calls, and outcomes) for MCPMark tasks across multiple MCP services and models.

## Contents
Each task run produces a trajectory folder containing three files:
- `meta.json`: Metadata (task id, model, timestamps, status, etc.)
- `messages.json`: Turn-by-turn exchanges including model thoughts/tool calls
- `execution.log`: Key execution-time logs

Typical structure:
```
mcpmark-v1-0905/
  <model>__<mcp_service>/
    run-1/
      <category>__<task>/
        meta.json
        messages.json
        execution.log
```

## Explore Logs in Your Browser
For fast browsing and inspection, use the MCPMark Trajectory Explorer. You can drag-and-drop either a single `messages.json` or a full trajectory folder (the three files above):
- Explorer: [https://mcpmark.ai/explorer](https://mcpmark.ai/explorer)