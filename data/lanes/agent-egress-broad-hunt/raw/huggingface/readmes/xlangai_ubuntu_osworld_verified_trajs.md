---
license: mit
tags:
- code
pretty_name: OSWorld-Verified Trajectories
size_categories:
- 100K<n<1M
---
# OSWorld-Verified Model Trajectories

This repository contains trajectory results from various AI models evaluated on the OSWorld benchmark - a comprehensive evaluation environment for multimodal agents in real computer environments.

## Dataset Overview

This dataset includes evaluation trajectories and results from multiple state-of-the-art models tested on OSWorld tasks.


## File Structure

Each zip file contains complete evaluation trajectories including:
- Screenshots and action sequences
- Model reasoning traces
- Task completion results
- Performance metrics

## Evaluation Settings

Models were evaluated across different step limits:
- **15 steps** - Quick evaluation
- **50 steps** - Standard evaluation  
- **100 steps** - Extended evaluation

And multiple runs.

## Task Domains

The evaluation covers diverse computer tasks including:
- **Office Applications** (LibreOffice Calc/Writer/Impress)
- **Daily Applications** (Chrome, VLC, Thunderbird)
- **Professional Tools** (GIMP, VS Code)
- **Multi-app Workflows**
- **Operating System Tasks**

## Usage

These trajectories can be used for:
- Model performance analysis
- Trajectory visualization and debugging
- Training data for computer use agents (not recommended)
- Benchmark comparison studies
- Research on multimodal agent behaviors

## Maintenance

This dataset is actively maintained and will be continuously updated.

## Citation

If you use this dataset in your research, please cite the OSWorld paper:

```bibtex
@article{osworld_verified,
  title = {Introducing OSWorld-Verified},
  author = {Tianbao Xie and Mengqi Yuan and Danyang Zhang and Xinzhuang Xiong and Zhennan Shen and Zilong Zhou and Xinyuan Wang and Yanxu Chen and Jiaqi Deng and Junda Chen and Bowen Wang and Haoyuan Wu and Jixuan Chen and Junli Wang and Dunjie Lu and Hao Hu and Tao Yu},
  journal = {xlang.ai},
  year = {2025},
  month = {July},
  url = "https://xlang.ai/blog/osworld-verified"
}
```

## Contact

For questions or contributions, please open an issue or contact the OSWorld team.

---

**Last Updated**: August 2025  
**Total Models**: 15+ model variants  
**Total Trajectories**: 1000+ evaluation episodes