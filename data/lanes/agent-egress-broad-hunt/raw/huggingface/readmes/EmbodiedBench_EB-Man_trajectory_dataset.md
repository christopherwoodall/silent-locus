# EB-Manipulation trajectory dataset

We release the trajectory dataset collected from EmbodiedBench using several closed-source and open-source models. We hope this dataset will support the development of more capable embodied agents with improved perception, reasoning, and planning abilities. When using the trajectories, we recommend separating the training and evaluation sets—for example, using the “base” subset for training and other EmbodiedBench subsets for evaluation.

## 📖 Dataset Description

(1) eb-man_dataset_multi_step.json.

This dataset contains trajectories with multi-step reasoning and planning data (each time the model outputs a plan with multiple actions) for tasks in the EB-Manipulation environment. Each episode provides:
- **model_name**: The name of the model used to generate the current trajectory data.
- **eval_set**: The evaluation subset the episode belongs to.
- **episode_id**: The id of the current episode.
- **instruction**: A high-level natural language instruction for the current episode.
- **input**: The textual prompt the model takes as input.
- **success**: A flag indicating whether the episode was completed successfully (1.0) or not (0.0).
- **trajectory**  
   - **visual_description**: Describe the color and shape of each object in the detection box in the numerical order in the image. Then provide the 3D coordinates of the objects chosen from input.
   - **reasoning_and_reflection**: Reason about the overall plan that needs to be taken on the target objects, and reflect on the previous actions taken if available.
   - **language_plan**: A list of natural language actions to achieve the user instruction. Each language action is started by the step number and the language action name. 
   - **executable_plan**: A list of discrete actions needed to achieve the user instruction, with each discrete action being a 7-dimensional discrete action. Each action entry contains:
     - `step_id`: The current step id.  
     - `img_path`: The path to the output image after the current action is executed.  
     - `action`: The 7-dimensional discrete action in the format of a list given by the prompt
     - `action_success`: 1.0 if that action succeeded, 0.0 if it failed.  
     - `env_feedback`: Environment or simulator feedback, e.g., `"Last action executed successfully."` or error message.  
   - **input_image_path** (`string`): The path to the input image.

(2) eb-man_dataset_single_step.json.

This dataset is curated from the multi-step version of the trajectory dataset and contains trajectories with single-step reasoning and planning data.

---

## 🔍 Usage
You can load the entire dataset in Python as follows:
```python
from huggingface_hub import snapshot_download
import os
import json
# 1) Download the entire dataset repo to a local folder
local_folder = snapshot_download(
    repo_id="EmbodiedBench/EB-Man_trajectory_dataset",
    repo_type="dataset",
    local_dir="./EB-Man_trajectory_dataset",     # or any folder you choose
    local_dir_use_symlinks=False
)
```
```python
# 2) Load the JSON file
with open("./EB-Man_trajectory_dataset/eb-man_dataset_multi_step.json", "r", encoding="utf-8") as f:
    multi_step_dataset = json.load(f)
with open("./EB-Man_trajectory_dataset/eb-man_dataset_single_step.json", "r", encoding="utf-8") as f:
    single_step_dataset = json.load(f)
# Examine the first episode
first = multi_step_dataset[0]
print("Instruction:", first["instruction"])
print("Number of trajectory steps:", len(first["trajectory"]))
```

You can unzip the images.zip using:
```bash
unzip ./EB-Man_trajectory_dataset/images.zip -d ./EB-Man_trajectory_dataset/images
```

## Citation
If you find our dataset helpful for your research, please cite EmbodiedBench:
```
@article{yang2025embodiedbench,
  title={EmbodiedBench: Comprehensive Benchmarking Multi-modal Large Language Models for Vision-Driven Embodied Agents},
  author={Yang, Rui and Chen, Hanyang and Zhang, Junyu and Zhao, Mark and Qian, Cheng and Wang, Kangrui and Wang, Qineng and Koripella, Teja Venkat and Movahedi, Marziyeh and Li, Manling and others},
  journal={arXiv preprint arXiv:2502.09560},
  year={2025}
}
```