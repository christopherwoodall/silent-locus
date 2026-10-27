---
license: apache-2.0
task_categories:
- text-generation
language:
- en
- multilingual
tags:
- animal-liberation
- animal-advocacy
- open-paws
- ethics
- alignment
- tool_use
size_categories:
- 10K<n<100K
pretty_name: "Open Paws Tool Use Llama Format"
configs:
- config_name: default
  data_files:
  - split: train
    path: "*"
---

# Open Paws Tool Use Llama Format

This dataset is part of the Open Paws initiative to develop AI training data aligned with animal liberation and advocacy principles. Created to train AI systems that understand and promote animal welfare, rights, and liberation.

## Dataset Details

- **Dataset Type**: Tool Use Data
- **Format**: JSONL (JSON Lines)
- **Languages**: Multilingual (primarily English)
- **Focus**: Animal advocacy and ethical reasoning
- **Organization**: [Open Paws](https://huggingface.co/open-paws)
- **License**: Apache 2.0

## Dataset Structure

Parquet format with tool usage examples:
- `messages`: Conversation with tool usage in Llama format
- `average_rating`: Quality assessment score (0.0 to 1.0)

### Ethical Guidelines
- ✅ Content promoting animal welfare and rights
- ✅ Educational material about animal liberation
- ✅ Ethical reasoning and advocacy strategies
- ❌ Content promoting animal exploitation
- ❌ Harmful or misleading information about animals

## Usage

### Loading the Dataset

```python
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("open-paws/tool-use-llama-format")

# Access training split
train_data = dataset["train"]

# Iterate through samples
for sample in train_data:
    print(sample["messages"])
    if "average_rating" in sample:
        print(f"Rating: {sample['average_rating']}")
```

### Use Cases

- Training animal liberation-focused AI models
- Fine-tuning for animal advocacy applications
- Research on AI alignment with ethical values

## Community and Contributions

- **Organization**: [Open Paws](https://huggingface.co/open-paws) - Making AI an ally to animals
- **Website**: [openpaws.ai](https://www.openpaws.ai/)
- **Community**: Join our mission to use AI for animal liberation
- **Issues**: Report data quality issues via HuggingFace discussions

## Dataset Contact

For questions about this dataset, please reach out via:
- **HuggingFace Discussions**: [open-paws/tool-use-llama-format](https://huggingface.co/open-paws/tool-use-llama-format/discussions)
- **Organization Page**: [Open Paws](https://huggingface.co/open-paws)

---

*Built with 🐾 for animal liberation and AI alignment*
