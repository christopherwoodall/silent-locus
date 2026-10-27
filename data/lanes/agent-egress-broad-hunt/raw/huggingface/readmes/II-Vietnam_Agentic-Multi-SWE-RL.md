---
dataset_info:
  features:
  - name: org
    dtype: string
  - name: repo
    dtype: string
  - name: number
    dtype: string
  - name: state
    dtype: string
  - name: title
    dtype: string
  - name: body
    dtype: string
  - name: base
    dtype: string
  - name: resolved_issues
    dtype: string
  - name: fix_patch
    dtype: string
  - name: test_patch
    dtype: string
  - name: fixed_tests
    dtype: string
  - name: p2p_tests
    dtype: string
  - name: f2p_tests
    dtype: string
  - name: s2p_tests
    dtype: string
  - name: n2p_tests
    dtype: string
  - name: run_result
    dtype: string
  - name: test_patch_result
    dtype: string
  - name: fix_patch_result
    dtype: string
  - name: instance_id
    dtype: string
  - name: language
    dtype: string
  - name: docker
    dtype: string
  splits:
  - name: train
    num_bytes: 23849176039
    num_examples: 7526
  download_size: 5398000933
  dataset_size: 23849176039
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---
