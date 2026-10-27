---
dataset_info:
  features:
  - name: task_id
    dtype: string
  - name: Question
    dtype: string
  - name: Level
    dtype: int64
  - name: file_name
    dtype: string
  - name: Annotator Metadata
    struct:
    - name: How long did this take?
      dtype: string
    - name: Number of steps
      dtype: string
    - name: Number of tools
      dtype: string
    - name: Steps
      dtype: string
    - name: Tools
      dtype: string
  - name: trace
    dtype: string
  - name: prediction
    dtype: string
  - name: Final answer
    dtype: string
  - name: judge
    dtype: bool
  splits:
  - name: train
    num_bytes: 477031176
    num_examples: 165
  download_size: 472562057
  dataset_size: 477031176
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---
