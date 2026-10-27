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
  splits:
  - name: train
    num_bytes: 59393
    num_examples: 20
  download_size: 29434
  dataset_size: 59393
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---
