---
dataset_info:
  features:
  - name: available_tools
    dtype: string
  - name: message_history
    dtype: string
  - name: score
    dtype: string
  - name: failure_reason
    dtype: string
  splits:
  - name: test
    num_bytes: 62214490
    num_examples: 9813
  download_size: 20381332
  dataset_size: 124428980
configs:
- config_name: default
  data_files:
  - split: test
    path: data/test-*
license: mit
---


# Dataset Summary

The MCP Tool Call Evaluation Test Dataset is a synthetic dataset designed for evaluating and benchmarking language models' ability to correctly execute function calls in the context of Model Context Protocol (MCP) tools. This dataset contains 9,813 test examples that assess a model's proficiency in:

1. **Tool Selection**: Choosing the correct function from available tools
2. **Parameter Structure**: Providing all required parameters with correct names
3. **Parameter Values**: Supplying appropriate values that match expected data types and user intent

## Data Fields

- **available_tools**: List of available MCP tools with their schemas
- **message_history**: Conversation context leading up to the tool call, containing:
  - **user_request**: The original user query that triggered the tool call
  - **tool_call**: The actual tool call made by the model (may be correct or incorrect)
- **score**: Ground truth classification of the tool call quality
- **failure_reason**: Detailed explanation of what went wrong (if applicable)

## Dataset Structure

Each instance contains:

```json
{
  "available_tools": [
    {
      "name": "function_name",
      "description": "Function description",
      "input_schema": {
        "type": "object",
        "properties": {...},
        "required": [...]
      }
    }
  ],
  "message_history": [
    {
      "role": "user|assistant",
      "content": "Message content"
    }
  ],
  "score": "correct|incorrect_tool|incorrect_parameter_names|incorrect_parameter_values",
  "failure_reason": "Description of failure (if any)",
}
```


## Dataset Creation

### Curation Rationale

This dataset was created to address the need for standardized evaluation of language models' tool-calling capabilities in the context of MCP (Model Context Protocol). The synthetic nature allows for controlled testing scenarios and comprehensive coverage of various failure modes.

### Source Data

#### Initial Data Collection and Normalization

The dataset was synthetically generated using a combination of:
- Real MCP server definitions from the Smithery registry
- Automated tool call generation with intentional errors
- Manual validation and quality control

### Scores

Each example was automatically labeled based on predefined criteria:
- **correct**: Tool call matches available tools and parameters exactly and achieves user request
- **incorrect_tool**: Function name doesn't exist in available tools or incorrect function was chosen
- **incorrect_parameter_names**: Correct function was chosen but parameter names are wrong
- **incorrect_parameter_values**: Function and parameters are correct but values are inappropriate


```bibtex
@dataset{mcp_tool_call_eval_test,
  title={MCP Tool Call Evaluation Test Dataset},
  author={QuotientAI},
  year={2025},
  url={https://huggingface.co/datasets/quotientai/limbic-eval-tool-use-mcp}
}
```