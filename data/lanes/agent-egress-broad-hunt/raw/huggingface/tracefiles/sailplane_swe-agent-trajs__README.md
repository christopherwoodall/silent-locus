---
dataset_info:
  features:
  - name: exit_status
    dtype: string
  - name: submission
    dtype: string
  - name: model_stats
    struct:
    - name: api_calls
      dtype: int64
    - name: instance_cost
      dtype: float64
    - name: tokens_received
      dtype: int64
    - name: tokens_sent
      dtype: int64
    - name: total_cost
      dtype: float64
  - name: total_cost
    dtype: float64
  - name: instance_cost
    dtype: float64
  - name: tokens_sent
    dtype: int64
  - name: tokens_received
    dtype: int64
  - name: api_calls
    dtype: int64
  - name: trajectory
    dtype: string
  - name: filename
    dtype: string
  - name: resolved
    dtype: bool
  - name: steps
    dtype: int64
  - name: 20240620_sweagent_claude3.5sonnet
    dtype: bool
  - name: 20240402_sweagent_gpt4
    dtype: bool
  - name: 20240721_amazon-q-developer-agent-20240719-dev
    dtype: bool
  - name: 20240628_autocoderover-v20240620
    dtype: bool
  splits:
  - name: train
    num_bytes: 370108525
    num_examples: 2294
  download_size: 92251627
  dataset_size: 370108525
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---
