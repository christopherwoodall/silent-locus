---
dataset_info:
  features:
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
  - name: dataset_source
    dtype: string
  - name: id
    dtype: string
  splits:
  - name: train
    num_bytes: 2544063832
    num_examples: 227579
  download_size: 789047125
  dataset_size: 2544063832
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---

Our new tool-use data for Olmo 3 Instruct models.
For the full dataset, documentation, etc. see the [main dataset card](https://huggingface.co/datasets/allenai/Dolci-Instruct-SFT).

This dataset is licensed under ODC-BY. It is intended for research and educational use in accordance with Ai2's [Responsible Use Guidelines](https://allenai.org/responsible-use).

## Citation

```
@misc{olmo2025olmo3,
title={Olmo 3},
author={Team Olmo and Allyson Ettinger and Amanda Bertsch and Bailey Kuehl and David Graham and David Heineman and Dirk Groeneveld and Faeze Brahman and Finbarr Timbers and Hamish Ivison and Jacob Morrison and Jake Poznanski and Kyle Lo and Luca Soldaini and Matt Jordan and Mayee Chen and Michael Noukhovitch and Nathan Lambert and Pete Walsh and Pradeep Dasigi and Robert Berry and Saumya Malik and Saurabh Shah and Scott Geng and Shane Arora and Shashank Gupta and Taira Anderson and Teng Xiao and Tyler Murray and Tyler Romero and Victoria Graf and Akari Asai and Akshita Bhagia and Alexander Wettig and Alisa Liu and Aman Rangapur and Chloe Anastasiades and Costa Huang and Dustin Schwenk and Harsh Trivedi and Ian Magnusson and Jaron Lochner and Jiacheng Liu and Lester James V. Miranda and Maarten Sap and Malia Morgan and Michael Schmitz and Michal Guerquin and Michael Wilson and Regan Huff and Ronan Le Bras and Rui Xin and Rulin Shao and Sam Skjonsberg and Shannon Zejiang Shen and Shuyue Stella Li and Tucker Wilde and Valentina Pyatkin and Will Merrill and Yapei Chang and Yuling Gu and Zhiyuan Zeng and Ashish Sabharwal and Luke Zettlemoyer and Pang Wei Koh and Ali Farhadi and Noah A. Smith and Hannaneh Hajishirzi},
year={2025},
eprint={2512.13961},
archivePrefix={arXiv},
primaryClass={cs.CL},
url={https://arxiv.org/abs/2512.13961},
}
```
