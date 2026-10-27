---
dataset_info:
  features:
  - name: prompt
    dtype: string
  - name: mcp_config
    dtype: string
  - name: id
    dtype: string
  - name: metadata
    dtype: string
  - name: setup_tool
    dtype: string
  - name: evaluate_tool
    dtype: string
  - name: system_prompt
    dtype: string
  - name: agent_config
    dtype: string
  splits:
  - name: train
    num_bytes: 1660819
    num_examples: 369
  download_size: 250168
  dataset_size: 1660819
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---
