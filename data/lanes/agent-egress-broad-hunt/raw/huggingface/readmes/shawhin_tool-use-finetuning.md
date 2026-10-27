---
dataset_info:
  features:
  - name: query
    dtype: string
  - name: query_type
    dtype: string
  - name: trace
    list:
    - name: content
      dtype: string
    - name: role
      dtype: string
  - name: num_tools_available
    dtype: int64
  - name: tool_needed
    dtype: bool
  - name: tool_name
    dtype: string
  splits:
  - name: train
    num_bytes: 2897711
    num_examples: 477
  - name: validation
    num_bytes: 356429
    num_examples: 60
  - name: test
    num_bytes: 392928
    num_examples: 60
  download_size: 1000364
  dataset_size: 3647068
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
  - split: validation
    path: data/validation-*
  - split: test
    path: data/test-*
---

Dataset for fine-tuning gemma-3-1b-it for function calling. The code and other resources for this project are linked below.

Resources:
- [YouTube Video](https://youtu.be/fAFJYbtTsC0)
- [Blog Post](https://medium.com/@shawhin/fine-tuning-llms-for-tool-use-5f1db03d7c55)
- [GitHub Repo](https://github.com/ShawhinT/llm-tool-use-ft)
- [Fine-tuned Model](https://huggingface.co/shawhin/gemma-3-1b-tool-use) | [Original Model](https://huggingface.co/google/gemma-3-1b-it)

### Citation
If you find this dataset helpful, please cite:

```
@dataset{talebi2025,
  author    = {Shaw Talebi},
  title     = {tool-use-finetuning},
  year      = {2025},
  publisher = {Hugging Face},
  howpublished = {\url{https://huggingface.co/datasets/shawhin/tool-use-finetuning}},
}
```