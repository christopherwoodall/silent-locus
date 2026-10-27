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
    num_bytes: 37566031
    num_examples: 5114
  download_size: 7950013
  dataset_size: 37566031
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
- reasoning
- agentic
- multistep
- bfcl
- sequential
size_categories:
- 1K<n<10K
---