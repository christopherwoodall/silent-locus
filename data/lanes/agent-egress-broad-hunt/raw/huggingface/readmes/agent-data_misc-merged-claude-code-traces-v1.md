---
dataset_info:
  features:
  - name: id
    dtype: string
  - name: source_table
    dtype: string
  - name: source_repo
    dtype: string
  - name: messages_json
    dtype: string
  - name: system_prompt
    dtype: string
  - name: user_prompt
    dtype: string
  - name: assistant_response
    dtype: string
  - name: model
    dtype: string
  - name: timestamp
    dtype: string
  - name: request_id
    dtype: string
  - name: tools_json
    dtype: string
  - name: gitdiff
    dtype: string
  - name: claude_log
    dtype: string
  - name: chatml
    dtype: string
  - name: has_empty_response
    dtype: bool
  - name: content_hash
    dtype: string
  splits:
  - name: train
    num_bytes: 5494041444
    num_examples: 32133
  download_size: 1157999310
  dataset_size: 5494041444
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---

# MISC Unification of Public Claude Code Traces

A unified dataset of **32,133 deduplicated Claude API conversation traces** focused on software engineering and code generation tasks. This dataset merges and normalizes traces from 10 different source datasets into a single, consistent format.

## Dataset Description

This dataset contains real Claude API interaction traces capturing software engineering workflows including:
- Code generation and modification
- Bug fixing and debugging
- Repository exploration
- Git operations
- Tool use (Bash, file operations, etc.)

### Sources

The dataset was created by merging and deduplicating the following Hugging Face datasets:

| Source | Original Rows | Description |
|--------|---------------|-------------|
| `archit11/complete-conversations-dataset` | 59,990 | Claude Code conversation traces |
| `archit11/claude_traces_hs` | 784 | Hyperswitch repository traces with git diffs |
| `archit11/claude_traces_hs2` | 784 | Hyperswitch traces with Claude logs |
| `archit11/claude-code-traces` | 25 | Claude Code API traces |
| `archit11/out_dataset` | 59 | Claude agent outputs |
| `robin0307/claude-code-mend` | 100 | Claude Code mending traces |

Additional normalized views from prior merge efforts were also included. After deduplication (by content hash of user prompt + assistant response), **32,133 unique conversations** remain.

## Dataset Schema

| Column | Type | Description |
|--------|------|-------------|
| `id` | string | Unique identifier (UUID) |
| `source_table` | string | Original source table name |
| `source_repo` | string | Original HuggingFace repo |
| `messages_json` | string | Full conversation as JSON array of `{role, content}` |
| `system_prompt` | string | System prompt if available |
| `user_prompt` | string | Extracted user message content |
| `assistant_response` | string | Extracted assistant response content |
| `model` | string | Claude model used (e.g., `claude-sonnet-4-5-20250929`) |
| `timestamp` | string | ISO timestamp of the interaction |
| `request_id` | string | API request ID if available |
| `tools_json` | string | Tool definitions as JSON if available |
| `gitdiff` | string | Git diff context if available |
| `claude_log` | string | Claude execution logs if available |
| `chatml` | string | Original ChatML format if applicable |
| `has_empty_response` | bool | True if assistant response is empty/missing |
| `content_hash` | string | MD5 hash of (user_prompt + assistant_response) for deduplication |

## Model Distribution

| Model | Count |
|-------|-------|
| claude-sonnet-4-5-20250929 | 20,414 |
| claude-haiku-4-5-20251001 | 10,900 |
| claude-3-5-haiku-20241022 | 23 |
| (not recorded) | 796 |

## Usage

```python
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("nlile/claude-code-traces-unified")

# Filter to only rows with responses
with_responses = dataset.filter(lambda x: not x["has_empty_response"])

# Access a conversation
example = dataset["train"][0]
print(f"User: {example['user_prompt'][:200]}...")
print(f"Assistant: {example['assistant_response'][:200]}...")
```

### Working with messages_json

```python
import json

example = dataset["train"][0]
if example["messages_json"]:
    messages = json.loads(example["messages_json"])
    for msg in messages:
        print(f"{msg['role']}: {msg['content'][:100]}...")
```

## Data Quality Notes

- **6,685 rows** (~20%) have empty assistant responses - these are incomplete conversations where only the user turn was recorded
- All rows have been deduplicated by content hash
- Original raw data is preserved in source columns for traceability
- Some conversations contain tool use (Bash commands, file operations) embedded in the assistant responses
