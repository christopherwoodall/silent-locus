---
license: cdla-permissive-2.0
format: agent-traces
task_categories:
  - text-generation
language:
  - en
tags:
  - llm
  - traces
  - opentelemetry
  - benchmarks
  - agents
---
# Multi-Benchmark LLM Agent Traces

A comprehensive dataset of OpenTelemetry traces capturing LLM inference behavior across multiple agent frameworks, benchmarks, and model providers. This dataset enables research into LLM performance analysis, agent behavior patterns, and inference optimization.

**Collected by [Exgentic](https://www.exgentic.ai/)** - A platform for LLM observability and performance optimization.

## Dataset Overview

This dataset contains **1,781 execution traces** capturing detailed agent behavior from various LLM-powered systems across 6 different benchmarks.

### What Each Trace Captures

Each trace provides comprehensive observability data including:

- **Complete Conversation History**: Full message exchanges between users and agents, including system prompts
- **Token Usage**: Detailed input and output token counts for every LLM call
- **Timing Information**: Precise start and end timestamps for each operation
- **Tool Calls & Results**: Complete records of tool invocations, arguments, and execution results
- **Tool Definitions**: Available tools and their schemas (function signatures, parameters, descriptions)
- **Model Information**: Model used for each inference
- **Error States**: Status codes indicating success or failure of operations

### Key Statistics

- **Total Traces**: 1,781 execution traces
- **Benchmarks**: 6 (SWE-bench, AppWorld, BrowseCompPlus, TAU-Bench Airline, TAU-Bench Retail, TAU-Bench Telecom)
- **Agent Frameworks**: 5 (claude_code, openai_solo, tool_calling, tool_calling_with_shortlisting, smolagents_code)
- **Models**: 5 models including both closed-source (Claude Opus 4.5, GPT-5.2, Gemini 3 Pro Preview) and open-source (DeepSeek-V3.2, Kimi-K2.5)

#### By Benchmark

| Benchmark | Traces (Sessions) | Turns (med/mean/max) | Harnesses | Models | Workload Description |
|-----------|-------------------|----------------------|-----------|--------|---------------------|
| appworld | 406 | 14 / 21.4 / 126 | claude_code, openai_solo, smolagents_code, tool_calling, tool_calling_with_shortlisting | DeepSeek-V3.2, Kimi-K2.5, claude-opus-4-5, gemini-3-pro-preview | Personal assistant |
| browsecompplus | 133 | 19 / 24.6 / 88 | claude_code, openai_solo, tool_calling | Kimi-K2.5, claude-opus-4-5, gemini-3-pro-preview | Deep research |
| swebench | 391 | 35 / 43.6 / 158 | claude_code, openai_solo, smolagents_code, tool_calling | DeepSeek-V3.2, Kimi-K2.5, claude-opus-4-5, gemini-3-pro-preview, gpt-5.2 | Software engineering |
| tau2_airline | 196 | 7 / 8.0 / 19 | claude_code, openai_solo, smolagents_code, tool_calling | claude-opus-4-5, gemini-3-pro-preview, | Customer service |
| tau2_retail | 469 | 8 / 9.1 / 22 | claude_code, openai_solo, smolagents_code, tool_calling | claude-opus-4-5, gemini-3-pro-preview,  | Customer service |
| tau2_telecom | 186 | 15 / 17.3 / 54 | claude_code, openai_solo, smolagents_code, tool_calling | claude-opus-4-5, gemini-3-pro-preview,  | Technical support |

#### By Model

| Model | #Traces | Avg LLM Calls | Failed (%) | Avg Input Messages | Avg Tool Use Calls | Avg Duration (s) |
|-------|---------|---------------|------------|--------------------|--------------------|------------------|
| DeepSeek-V3.2 | 135 | 42.48 | 0.30 | 64.12 | 0.49 | 881.68 |
| Kimi-K2.5 | 160 | 42.29 | 8.32 | 64.73 | 0.59 | 508.25 |
| claude-opus-4-5 | 509 | 22.10 | 5.40 | 33.55 | 1.39 | 159.99 |
| gemini-3-pro-preview | 361 | 21.43 | 1.59 | 32.39 | 1.24 | 264.61 |
| gpt-5.2-2025-12-11 | 52 | 25.79 | 2.01 | 34.61 | 0.99 | 132.93 |

#### By Harness

| Harness | #Traces | Avg LLM Calls | Failed (%) | Avg Input Messages | Avg Tool Use Calls | Avg Duration (s) |
|---------|---------|---------------|------------|--------------------|--------------------|------------------|
| claude_code | 839 | 23.27 | 2.37 | 36.12 | 1.11 | 231.41 |
| openai_solo | 114 | 11.61 | 4.76 | 25.45 | 0.89 | 138.78 |
| smolagents_code | 315 | 25.44 | 1.92 | 66.40 | 0.10 | 324.84 |
| tool_calling | 431 | 16.27 | 8.61 | 39.38 | 1.36 | 221.94 |
| tool_calling_with_shortlisting | 82 | 26.57 | 2.52 | 12.59 | 0.77 | 401.41 |


#### Token Usage

The following tables show token usage statistics calculated from successful LLM API calls only (failed spans are excluded).
Token metrics include:
- **Avg. Request Tokens/Span**: Average input tokens per successful API call
- **Avg. Response Tokens/Span**: Average output tokens per successful API call
- **Avg. Total Tokens/Span**: Average total tokens (input + output) per successful API call
- **Avg. Total Tokens/Trace**: Average total tokens consumed across all successful API calls in a trace

###### Token Usage by Benchmark

| Benchmark | Avg. Request Tokens/Span | Avg. Response Tokens/Span | Avg. Total Tokens/Span | Avg. Total Tokens/Trace |
| --- | --: | --: | --: | --: |
| appworld | 63087 | 423 | 63511 | 1299476 |
| browsecompplus | 53435 | 534 | 53969 | 1671773 |
| swebench | 24732 | 202 | 24934 | 1183537 |
| tau2_airline | 9138 | 162 | 9300 | 105916 |
| tau2_retail | 9222 | 95 | 9317 | 119773 |
| tau2_telecom | 9856 | 92 | 9948 | 164962 |

###### Token Usage by Model

| Model | Avg. Request Tokens/Span | Avg. Response Tokens/Span | Avg. Total Tokens/Span | Avg. Total Tokens/Trace |
| --- | --: | --: | --: | --: |
| DeepSeek-V3.2 | 50247 | 216 | 50464 | 1624075 |
| Kimi-K2.5 | 32337 | 272 | 32609 | 1123526 |
| claude-opus-4-5 | 48984 | 249 | 49233 | 1182762 |
| gemini-3-pro-preview | 31977 | 529 | 32506 | 767914 |
| gpt-5.2-2025-12-11 | 20636 | 86 | 20722 | 580684 |

###### Token Usage by Harness

| Harness | Avg. Request Tokens/Span | Avg. Response Tokens/Span | Avg. Total Tokens/Span | Avg. Total Tokens/Trace |
| --- | --: | --: | --: | --: |
| claude_code | 35975 | 274 | 36249 | 974096 |
| openai_solo | 22927 | 130 | 23057 | 347897 |
| smolagents_code | 10353 | 104 | 10457 | 521204 |
| tool_calling | 31509 | 234 | 31743 | 645800 |
| tool_calling_with_shortlisting | 8553 | 456 | 9009 | 254463 |


## Trace Format

Each trace contains OpenTelemetry spans representing discrete operations in the LLM inference pipeline.

### Span Structure

```json
{
  "trace_id": "string",
  "span_id": "string",
  "parent_span_id": "string or null",
  "name": "string",
  "kind": "string",
  "start_time": "ISO 8601 timestamp",
  "end_time": "ISO 8601 timestamp",
  "attributes": {
    "gen_ai.operation.name": "chat",
    "gen_ai.request.model": "aws/claude-opus-4-5",
    "gen_ai.response.model": "aws/claude-opus-4-5",
    "gen_ai.usage.input_tokens": 18958,
    "gen_ai.usage.output_tokens": 92,
    "gen_ai.response.id": "chatcmpl-89052594-c0cd-49a4-a002-b3e75beca5f8",
    "gen_ai.response.finish_reasons": ["stop"],
    "gen_ai.input.messages": "[{\"role\": \"user\", \"parts\": [{\"type\": \"text\", \"content\": \"Complete this task...\"}]}]",
    "gen_ai.output.messages": "[{\"role\": \"assistant\", \"finish_reason\": \"stop\", \"parts\": [{\"type\": \"tool_call\", \"id\": \"tooluse_YQlkLGUuSk6Dp9WPwlmHzg\", \"name\": \"mcp__environment__bash\", \"arguments\": {...}}]}]",
    "gen_ai.tool.definitions": "[{\"type\": \"function\", \"name\": \"Task\", \"description\": \"...\", \"parameters\": {...}}]"
  },
  "resource_attributes": {
    "telemetry.sdk.language": "python",
    "telemetry.sdk.name": "opentelemetry",
    "telemetry.sdk.version": "1.40.0",
    "service.name": "litellm",
    "service.version": "1.0.0"
  },
  "status": {
    "code": 1,
    "message": ""
  }
}
```
