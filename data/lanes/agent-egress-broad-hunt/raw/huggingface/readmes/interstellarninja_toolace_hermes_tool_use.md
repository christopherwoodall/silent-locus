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
    num_bytes: 54888037
    num_examples: 11300
  download_size: 17558528
  dataset_size: 54888037
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---
