---
license: apache-2.0
task_categories:
- question-answering
language:
- en
pretty_name: BrowserAgent-SeedData
size_categories:
- 100K<n<1M
configs:
- config_name: 2wiki
  data_files:
  - split: train
    path: 2wiki/train-*
  - split: validation
    path: 2wiki/validation-*
- config_name: bamboogle
  data_files:
  - split: test
    path: bamboogle/test-*
- config_name: hotpot
  data_files:
  - split: train
    path: hotpot/train-*
  - split: validation
    path: hotpot/validation-*
- config_name: musique
  data_files:
  - split: train
    path: musique/train-*
  - split: validation
    path: musique/validation-*
- config_name: nq
  data_files:
  - split: train
    path: nq/train-*
  - split: test
    path: nq/test-*
- config_name: popqa
  data_files:
  - split: test
    path: popqa/test-*
dataset_info:
- config_name: 2wiki
  features:
  - name: data_source
    dtype: string
  - name: prompt
    list:
    - name: content
      dtype: string
    - name: role
      dtype: string
  - name: ability
    dtype: string
  - name: reward_model
    struct:
    - name: ground_truth
      list: string
    - name: style
      dtype: string
  - name: extra_info
    struct:
    - name: golden_answers
      list: string
    - name: id
      dtype: int64
    - name: index
      dtype: int64
    - name: question
      dtype: string
    - name: selected_answer
      dtype: string
    - name: split
      dtype: string
    - name: url
      dtype: string
  splits:
  - name: train
    num_bytes: 30017634
    num_examples: 10000
  - name: validation
    num_bytes: 77487838
    num_examples: 25152
  download_size: 5337430
  dataset_size: 107505472
- config_name: bamboogle
  features:
  - name: data_source
    dtype: string
  - name: prompt
    list:
    - name: content
      dtype: string
    - name: role
      dtype: string
  - name: ability
    dtype: string
  - name: reward_model
    struct:
    - name: ground_truth
      list: string
    - name: style
      dtype: string
  - name: extra_info
    struct:
    - name: golden_answers
      list: string
    - name: id
      dtype: int64
    - name: index
      dtype: int64
    - name: question
      dtype: string
    - name: selected_answer
      dtype: string
    - name: split
      dtype: string
    - name: url
      dtype: string
  splits:
  - name: test
    num_bytes: 375279
    num_examples: 125
  download_size: 31940
  dataset_size: 375279
- config_name: hotpot
  features:
  - name: data_source
    dtype: string
  - name: prompt
    list:
    - name: content
      dtype: string
    - name: role
      dtype: string
  - name: ability
    dtype: string
  - name: reward_model
    struct:
    - name: ground_truth
      list: string
    - name: style
      dtype: string
  - name: extra_info
    struct:
    - name: golden_answers
      list: string
    - name: id
      dtype: int64
    - name: index
      dtype: int64
    - name: question
      dtype: string
    - name: selected_answer
      dtype: string
    - name: split
      dtype: string
    - name: url
      dtype: string
  splits:
  - name: train
    num_bytes: 275677806
    num_examples: 90447
  - name: validation
    num_bytes: 44988550
    num_examples: 14810
  download_size: 26887684
  dataset_size: 320666356
- config_name: musique
  features:
  - name: data_source
    dtype: string
  - name: prompt
    list:
    - name: content
      dtype: string
    - name: role
      dtype: string
  - name: ability
    dtype: string
  - name: reward_model
    struct:
    - name: ground_truth
      list: string
    - name: style
      dtype: string
  - name: extra_info
    struct:
    - name: golden_answers
      list: string
    - name: id
      dtype: int64
    - name: index
      dtype: int64
    - name: question
      dtype: string
    - name: selected_answer
      dtype: string
    - name: split
      dtype: string
    - name: url
      dtype: string
  splits:
  - name: train
    num_bytes: 30330307
    num_examples: 10000
  - name: validation
    num_bytes: 14816106
    num_examples: 4834
  download_size: 1903274
  dataset_size: 45146413
- config_name: nq
  features:
  - name: data_source
    dtype: string
  - name: prompt
    list:
    - name: content
      dtype: string
    - name: role
      dtype: string
  - name: ability
    dtype: string
  - name: reward_model
    struct:
    - name: style
      dtype: string
  - name: extra_info
    struct:
    - name: golden_answers
      list: string
    - name: index
      dtype: int64
    - name: question
      dtype: string
    - name: seed
      dtype: int64
    - name: selected_answer
      dtype: string
    - name: split
      dtype: string
  splits:
  - name: train
    num_bytes: 211902069
    num_examples: 79168
  - name: test
    num_bytes: 9704046
    num_examples: 3610
  download_size: 38473805
  dataset_size: 221606115
- config_name: popqa
  features:
  - name: data_source
    dtype: string
  - name: prompt
    list:
    - name: content
      dtype: string
    - name: role
      dtype: string
  - name: ability
    dtype: string
  - name: reward_model
    struct:
    - name: ground_truth
      list: string
    - name: style
      dtype: string
  - name: extra_info
    struct:
    - name: golden_answers
      list: string
    - name: id
      dtype: int64
    - name: index
      dtype: int64
    - name: question
      dtype: string
    - name: selected_answer
      dtype: string
    - name: split
      dtype: string
    - name: url
      dtype: string
  splits:
  - name: test
    num_bytes: 43789979
    num_examples: 14267
  download_size: 1301046
  dataset_size: 43789979
---

# BrowserAgent-Data

Dataset used in https://github.com/TIGER-AI-Lab/BrowserAgent.

## Summary

- Total rows: 230,015
- Total size: ~29.47 MB
- Subsets: 2wiki, bamboogle, hotpot, musique, nq, popqa

## Splits and Sizes

- 2wiki: 22,576 rows (~2.73 MB)
- bamboogle: 125 rows (~0.03 MB)
- hotpot: 97,852 rows (~14.20 MB)
- musique: 12,417 rows (~0.92 MB)
- nq: 82,778 rows (~10.14 MB)
- popqa: 14,267 rows (~1.45 MB)

Files are stored as Parquet under each subset directory with dev/train/test splits where applicable.