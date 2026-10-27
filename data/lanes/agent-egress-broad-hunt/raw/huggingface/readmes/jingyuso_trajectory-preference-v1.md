---
dataset_info:
  features:
  - name: id
    dtype: string
  - name: token
    dtype: string
  - name: preference_sample_token
    dtype: string
  - name: category
    dtype: string
  - name: split
    dtype: string
  - name: prompt
    dtype: string
  - name: chosen
    dtype: string
  - name: rejected
    dtype: string
  - name: annotator_name
    dtype: string
  - name: confidence
    dtype: float64
  - name: notes
    dtype: string
  - name: original_preference
    dtype: string
  - name: uncertain
    dtype: bool
  - name: created_at
    dtype: string
  - name: trajectory_A_scores
    dtype: string
  - name: trajectory_B_scores
    dtype: string
  - name: image_stitched_camera
    dtype: image
  - name: image_bev_trajectory_A
    dtype: image
  - name: image_bev_trajectory_B
    dtype: image
  splits:
  - name: train
    num_bytes: 56761476382.697
    num_examples: 9803
  - name: val
    num_bytes: 14293127698.672
    num_examples: 2458
  download_size: 71053971717
  dataset_size: 71054604081.369
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
  - split: val
    path: data/val-*
---
