---
dataset_info:
  features:
  - name: trajectory_2d
    sequence:
      sequence: int64
  - name: goal_2d
    sequence: int64
  - name: trajectory_3d
    sequence:
      sequence: float64
  - name: shorter_trajectory_2d
    sequence:
      sequence: int64
  - name: shorter_trajectory_3d
    sequence:
      sequence: float64
  - name: subsampled_trajectory_2d
    sequence:
      sequence: int64
  - name: lang_goal
    dtype: string
  - name: text
    dtype: string
  - name: label
    dtype: string
  - name: label_list
    sequence:
      sequence: string
  - name: horizon
    dtype: int64
  - name: curvature
    dtype: float64
  - name: image
    dtype: image
  - name: camera_params
    dtype: string
  splits:
  - name: train
    num_bytes: 22198900728.25
    num_examples: 199998
  download_size: 22155327981
  dataset_size: 22198900728.25
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---
