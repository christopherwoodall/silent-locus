# BrowserAgent P14 RL assets

Upload this directory as a Hugging Face **dataset repository**. It is a resource package, not a single tabular dataset. Download the snapshot and pass its path to the deployment code.

- `models/p14-sft`: complete merged Qwen2.5-VL P14 model for RL.
- `models/p14-lora`: adapter plus portable base-model configuration.
- `datasets/rl1000`, `datasets/rl2000`, `datasets/validation100`: historical inputs.
- `provenance`: data composition, overlap audit, and model identities.
- `manifest.json`: every payload file's size and SHA-256.

The 1000/2000 training sets overlap in 342 exact question strings. They are not disjoint. The alternate 500-Hotpot/1500-NQ 2000-row dataset is not included.

Wiki ZIM and the BrowserAgent environment are prepared by the code repository. No Wiki file, base-model duplicate, SFT images, optimizer states, or credentials are included.

Base model: Qwen/Qwen2.5-VL-7B-Instruct at `cc594898137f460bfe9f0759e9844b3ce807cfb5`. Preserve the base model and source datasets' licenses.
