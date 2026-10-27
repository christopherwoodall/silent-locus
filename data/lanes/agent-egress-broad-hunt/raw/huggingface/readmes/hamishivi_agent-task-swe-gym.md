---
dataset_info:
  features:
  - name: messages
    list:
    - name: content
      dtype: string
    - name: role
      dtype: string
  - name: ground_truth
    dtype: string
  - name: dataset
    dtype: string
  - name: env_config
    struct:
    - name: env_name
      dtype: string
    - name: image
      dtype: string
    - name: task_id
      dtype: string
  - name: source
    dtype: string
  splits:
  - name: train
    num_bytes: 1028366.0135097877
    num_examples: 407
  download_size: 450539
  dataset_size: 1028366.0135097877
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---
