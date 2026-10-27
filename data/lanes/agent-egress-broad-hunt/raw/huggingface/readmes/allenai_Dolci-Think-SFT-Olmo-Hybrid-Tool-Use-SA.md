---
dataset_info:
  features:
  - name: id
    dtype: string
  - name: source
    dtype: string
  - name: n_step
    dtype: string
  - name: n_turn
    dtype: string
  - name: is_refusal
    dtype: bool
  - name: exec_type
    dtype: string
  - name: messages
    list:
    - name: content
      dtype: string
    - name: function_calls
      dtype: string
    - name: functions
      dtype: string
    - name: role
      dtype: string
  splits:
  - name: train
    num_bytes: 39873516.35225376
    num_examples: 1595
  download_size: 3794071
  dataset_size: 39873516.35225376
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
license: cc-by-sa-4.0
---

### Licensing Information

Dolci Think SFT Olmo Hybrid Tool Use SA is licensed under the Open Data Commons Attribution License v1.0 (ODC-By). It is intended for research and educational use. For more information, please see our [Responsible Use Guidelines](https://allenai.org/responsible-use).
