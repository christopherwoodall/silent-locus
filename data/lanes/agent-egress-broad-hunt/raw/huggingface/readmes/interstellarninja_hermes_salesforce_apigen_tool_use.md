---
dataset_info:
  features:
  - name: conversations
    list:
    - name: from
      dtype: string
    - name: value
      dtype: string
  - name: tools
    dtype: string
  - name: task
    dtype: string
  - name: category
    dtype: string
  - name: source
    dtype: string
  splits:
  - name: train
    num_bytes: 96926112.0
    num_examples: 2899
  download_size: 15901370
  dataset_size: 96926112.0
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---
