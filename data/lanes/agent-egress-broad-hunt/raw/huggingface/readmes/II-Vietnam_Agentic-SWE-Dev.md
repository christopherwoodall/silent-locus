---
dataset_info:
  features:
  - name: task_id
    dtype: string
  - name: split
    dtype: string
  - name: level
    dtype: string
  - name: docker_image
    dtype: string
  - name: task
    dtype: string
  - name: workspace_dir
    dtype: string
  - name: test_command
    dtype: string
  - name: file_code
    dtype: string
  - name: original_file_code
    dtype: string
  splits:
  - name: train
    num_bytes: 1143350919
    num_examples: 13659
  - name: test
    num_bytes: 66712884
    num_examples: 836
  download_size: 325195901
  dataset_size: 1210063803
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
  - split: test
    path: data/test-*
---
