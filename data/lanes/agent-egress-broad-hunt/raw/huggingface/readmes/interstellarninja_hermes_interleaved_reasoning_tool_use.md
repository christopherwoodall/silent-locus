---
dataset_info:
  features:
  - name: conversations
    list:
    - name: from
      dtype: string
    - name: value
      dtype: string
  - name: task
    dtype: string
  - name: category
    dtype: string
  - name: source
    dtype: string
  splits:
  - name: train
    num_bytes: 9347997
    num_examples: 1706
  download_size: 1156705
  dataset_size: 9347997
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---
