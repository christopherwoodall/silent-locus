---
language:
- en
tags:
- chatml
- browser
- agent
- sft
- rft
task_categories:
- text-generation
pretty_name: BrowserAgent ChatML Dataset
configs:
- config_name: sft
  data_files: sft.jsonl
- config_name: rft
  data_files: rft.jsonl
---

# BrowserAgent ChatML Dataset (SFT/RFT)

This dataset contains ChatML-style multi-turn dialogues for a browser agent task. The data is prepared as JSON Lines so it can be previewed directly with the Hugging Face Hub Data Visualizer and loaded with the `datasets` library.

## Links

[Paper](https://arxiv.org/abs/2510.10666)
[Github](https://github.com/TIGER-AI-Lab/BrowserAgent?tab=readme-ov-file)

## Files
- sft.jsonl — SFT split (one JSON object per line)
- rft.jsonl — RFT split (one JSON object per line)

## Schema
Each record is a JSON object containing:
- messages: list[object]
  - role: string ∈ {system, user, assistant}
  - content: string
- subset: string (the source filename without extension)
- stage: string ∈ {sft, rft}

## Load with datasets
```python
from datasets import load_dataset

ds = load_dataset(
    "json",
    data_files={
        "sft": "sft.jsonl",
        "rft": "rft.jsonl",
    },
)
print(ds)
print(ds["sft"][0]["messages"][0])
print(ds["sft"][0]["subset"])  # for filtering/grouping
print(ds["sft"][0]["stage"])   # sft or rft
```

## Notes
- Files are standard JSON Lines (.jsonl); the Hub Data Visualizer will display nested `messages` as JSON cells.
- The `subset` field helps trace each example back to its original source file.


## Citation
```
@misc{yu2025browseragentbuildingwebagents,
      title={BrowserAgent: Building Web Agents with Human-Inspired Web Browsing Actions}, 
      author={Tao Yu and Zhengbo Zhang and Zhiheng Lyu and Junhao Gong and Hongzhu Yi and Xinming Wang and Yuxuan Zhou and Jiabing Yang and Ping Nie and Yan Huang and Wenhu Chen},
      year={2025},
      eprint={2510.10666},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2510.10666}, 
}
```