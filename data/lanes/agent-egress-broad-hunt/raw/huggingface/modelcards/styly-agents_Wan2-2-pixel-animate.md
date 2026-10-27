---
license: apache-2.0
base_model:
  - Wan-AI/Wan2.2-I2V-14B-480P
tags:
  - lora
  - video-generation
  - image-to-video
  - pixel-art
  - sprite-animation
  - game-development
  - wan
  - comfyui
library_name: diffusers
pipeline_tag: image-to-video
---

# Wan2.2 Pixel Animate Adapter

A LoRA adapter for Wan 2.2 I2V (Image-to-Video) model, fine-tuned specifically for generating pixel art sprite animations from static images.

## Model Details

| Property | Value |
|----------|-------|
| Base Model | Wan2.2-I2V-A14B (14B parameters) |
| Adapter Type | LoRA |
| LoRA Rank | 256 |
| Precision | bfloat16 |
| File Size | ~2.3 GB |

## Training

- **Epochs**: 100
- **Optimizer**: AdamW (lr=2e-5, betas=[0.9, 0.99])
- **Gradient Accumulation**: 4 steps
- **Activation Checkpointing**: Unsloth

## Dataset

Trained on **226 pixel art sprite animation videos** covering:

- **Character Sprites**: Cowboys, zombies, skeletons, dark elves, fantasy characters, Santa, city characters, anime warriors
- **Magic Effects**: Projectiles, elemental spells, energy bursts
- **VFX**: Explosions, smoke effects, dust clouds
- **Actions**: Attack cycles (slashing, shooting, casting), idle animations, walking cycles

**Resolution**: 600x370 pixels
**Frame Buckets**: 8, 16, 24, 32 frames (up to 2 seconds at 16fps)

## Usage

This LoRA is designed for **Image-to-Video generation** - transforming static pixel art characters into animated sprite sequences.

### ComfyUI Workflow

Load using `LoraLoaderModelOnly` node with the Wan 2.2 I2V model:

1. Load base model: `wan2.2_i2v_high_noise_14B_fp16.safetensors` or `wan2.2_i2v_low_noise_14B_fp16.safetensors`
2. Apply this LoRA adapter with strength 1.0
3. Use with `PainterI2V` node for image-to-video conditioning
4. Recommended: Use with 4-step distillation LoRA for faster inference

See included `wan2-2-video.json` workflow file for a complete setup.

### Recommended Settings

- **Sampler**: DDIM
- **Steps**: 4 (with distillation LoRA) or higher without
- **ModelSamplingSD3 Shift**: 5.0
- **Frame Count**: 45 frames
- **CFG Scale**: 1.1

## Files

- `wan2.2_animate_adapter_model.safetensors` - The LoRA adapter weights
- `wan2-2-video.json` - ComfyUI workflow for using this model

## License

Please refer to the Wan 2.2 model license for usage terms.
