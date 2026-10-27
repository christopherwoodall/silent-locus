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
    num_bytes: 138012926
    num_examples: 14579
  download_size: 26612632
  dataset_size: 138012926
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
license: apache-2.0
task_categories:
- question-answering
language:
- en
tags:
- tool-use
- multiturn
- agentic
- bfcl
- reasoning
size_categories:
- 10K<n<100K
---