---
language:
- en
license: apache-2.0
task_categories:
- text-generation
tags:
- mcp
- tool-use
- agent
- trajectory
- benchmark
- function-calling
- atif
size_categories:
- n<1K
configs:
- config_name: default
  data_files:
  - split: train
    path: train.jsonl
---

# MCP Agent Trajectory Benchmark

A benchmark dataset of **49 MCP (Model Context Protocol) agent trajectories** (38 single-pass + 11 multi-conv) with complete tool-use traces in the **ATIF v1.2** (Agent Trajectory Interchange Format) format. Each agent operates in a distinct business domain with custom tools, realistic user conversations, and full execution traces.

Designed for training and evaluating **tool-use / function-calling** capabilities of LLMs.

## Overview

| Item | Details |
|------|---------|
| Total Trajectories | 49 (38 single-pass + 11 multi-conv) |
| Format | ATIF v1.2 (Agent Trajectory Interchange Format) |
| Model | kimi-k2.5 |
| Single-Pass Files | 380 |
| Multi-Conv Files | 30 |
| Domains | Finance, Health & Fitness, HR, Logistics, Marketing, Customer Service |

## Agent Roster by Domain

### 💰 Finance & Trading (16)
accountant, backtest-expert, budget-planner, crypto-portfolio-tracker, crypto-tracker, expense-tracker, expense-tracker-pro, financial-advisor, intelligent-budget-tracker, invoice-manager, loan-calculator, personal-finance, portfolio-monitor, stock-analyzer, stock-watcher, tax-calculator, trading-backtester, us-stock-analysis

### 🏋️ Health & Fitness (8)
calorie-counter, diet-tracker, endurance-coach, fasting-tracker, fitbit, garmin-health, health-summary, hevy, oura-analytics

### 📦 Operations & Logistics (3)
inventory-supply-chain, logistics-optimizer, production-scheduling

### 📣 Marketing & Sales (3)
campaign-orchestrator, crm-manager, email-marketing

### 👥 HR & Management (3)
employee-onboarding, project-manager, recruiter

### 🛎️ Service (2)
customer-support, recipe-finder

## Multi-Conv Trajectories (NEW)

11 multi-turn conversation agent trajectories captured from real OpenClaw agent sessions. Unlike the single-pass ATIF v1.2 trajectories above, these capture **extended multi-session interactions** with varying formats reflecting organic agent usage.

| Item | Details |
|------|---------|
| Trajectories | 11 |
| Format | Session-based (varies per agent) |
| Source | Real OpenClaw agent sessions |
| Location | `multi_conv/` directory |

### Agent Scenarios

| Scenario | Description |
|----------|-------------|
| Airline_plan | Flight planning and itinerary management |
| Airline_plan_2nd_trial | Airline planning iteration with refined approach |
| Bilibili_Marketing_Session_20260319 | Bilibili platform marketing analysis (iPhone Air case) |
| expense_tracker | Personal expense tracking and categorization |
| finclaw_export | Financial data extraction and export |
| hevy | Workout tracking and fitness data analysis |
| project_manager | Project task management and coordination |
| Skill_collect | Agent skill discovery and collection |
| Storage_Chip_Industry_Analysis | Storage chip industry research report |
| Weather_tool | Weather data retrieval and forecasting |
| Webpage_info | Web page content extraction and analysis |

### Format Differences

| Aspect | Single-Pass (38) | Multi-Conv (11) |
|--------|-------------------|-----------------|
| Schema | ATIF v1.2 (standardized) | Session-based (organic) |
| Structure | `steps[]` with `tool_calls` + `observation` | Varies: session lists, conversation arrays, agent traces |
| Source | Synthetic (kimi-k2.5) | Real agent sessions (OpenClaw) |
| Files per agent | ~10 (trajectory + conversation + mcp_server + workspace) | 1-5 (trajectory.json + optional artifacts) |

## Data Structure (Single-Pass)

Each agent directory contains:

```
├── conversation.jsonl         # User messages (multi-turn conversation)
├── trajectory.json            # Full ATIF v1.2 trajectory with tool calls
├── mcp_server.py              # MCP server implementation (tool definitions)
└── workspace/
    ├── SOUL.md                # Agent persona & behavior guidelines
    ├── AGENTS.md              # Agent configuration
    ├── TOOLS.md               # Tool usage notes
    ├── USER.md                # User profile
    ├── IDENTITY.md            # Agent identity
    ├── BOOTSTRAP.md           # Bootstrap instructions
    └── HEARTBEAT.md           # Heartbeat config
```

### trajectory.json (ATIF v1.2)

```json
{
  "schema_version": "ATIF-v1.2",
  "session_id": "mt-fin2-accountant__4TAccTyw",
  "agent": {
    "name": "mcp",
    "version": "unknown",
    "model_name": "openai/kimi-k2.5"
  },
  "steps": [
    {
      "step_id": 1,
      "source": "user",
      "message": "How did we do this quarter?"
    },
    {
      "step_id": 2,
      "source": "agent",
      "message": "Analysis: ... Plan: ...",
      "tool_calls": [
        {
          "tool_call_id": "get_financial_statements-2-0",
          "function_name": "get_financial_statements",
          "arguments": { "type": "income" }
        }
      ],
      "observation": {
        "results": [
          {
            "source_call_id": "get_financial_statements-2-0",
            "content": "{ ... financial data ... }"
          }
        ]
      }
    }
  ]
}
```

Each step captures: user input → agent reasoning → tool calls (function name + args) → tool results → agent response.

### conversation.jsonl

```jsonl
{"message": "How did we do this quarter?"}
{"message": "Are the books balanced?"}
{"message": "What are our key ratios?"}
```

### mcp_server.py

Complete Python implementation of the MCP tool server, defining all available tools for the agent (e.g., `get_financial_statements`, `calculate_ratios`, `check_balance` for the accountant agent).

## Use Cases

- **Tool-Use SFT**: Train models to select the right tool, construct correct arguments, and interpret results
- **Function-Calling Evaluation**: Benchmark accuracy of tool selection and parameter generation across 38 domains
- **Agent Architecture Research**: Study how agents chain multiple tool calls to answer complex queries
- **MCP Ecosystem**: Standard training data for MCP-compatible agent frameworks
- **Multi-Turn Tool Reasoning**: Train models on realistic multi-step tool-use conversations

## Key Features

- ✅ **Real tool implementations** — not mocked; each mcp_server.py is a working tool server
- ✅ **Multi-turn conversations** — 3-5 turns per agent with escalating complexity
- ✅ **Diverse domains** — 38 agents across 6 business verticals
- ✅ **Complete agent configs** — SOUL.md personas make each agent behave distinctly
- ✅ **Standardized format** — ATIF v1.2 for cross-framework compatibility

---

# MCP Agent 轨迹基准数据集

包含 **49 条 MCP（Model Context Protocol）Agent 轨迹**（38 条单轮 + 11 条多轮对话）的基准数据集，采用 **ATIF v1.2**（Agent Trajectory Interchange Format）格式。每个 Agent 在不同业务领域运行，配备专属工具、真实用户对话和完整执行追踪。

用于训练和评估 LLM 的 **工具调用（Tool-Use / Function-Calling）** 能力。

## 数据概览

| 项目 | 详情 |
|------|------|
| 轨迹总数 | 49 条（38 单轮 + 11 多轮） |
| 格式 | ATIF v1.2 |
| 模型 | kimi-k2.5 |
| 总文件数 | 380 |
| 领域覆盖 | 金融、健康健身、HR、物流、营销、客服 |

## 领域分布

| 领域 | 数量 | Agent 示例 |
|------|------|-----------|
| 💰 金融与交易 | 16 | accountant, stock-analyzer, crypto-tracker, tax-calculator |
| 🏋️ 健康与健身 | 8 | calorie-counter, fitbit, garmin-health, endurance-coach |
| 📦 运营与物流 | 3 | inventory-supply-chain, logistics-optimizer |
| 📣 营销与销售 | 3 | campaign-orchestrator, crm-manager, email-marketing |
| 👥 HR 与管理 | 3 | employee-onboarding, recruiter, project-manager |
| 🛎️ 服务 | 2 | customer-support, recipe-finder |

## 用途

- **Tool-Use SFT**: 训练模型选择正确工具、构造参数、解读结果
- **Function-Calling 评估**: 跨 38 个领域 benchmark 工具选择和参数生成准确率
- **Agent 架构研究**: 研究 Agent 如何链式调用多个工具回答复杂问题
- **MCP 生态**: 为 MCP 兼容框架提供标准训练数据
- **多轮工具推理**: 训练模型处理真实的多步骤工具调用对话


## 多轮对话轨迹（新增）

11 个多轮对话 Agent 轨迹，来自真实 OpenClaw Agent 会话。与上述单轮 ATIF v1.2 轨迹不同，这些数据捕获了**多会话交互**，格式反映了真实的 Agent 使用场景。

### 场景清单

| 场景 | 描述 |
|------|------|
| Airline_plan | 航班规划与行程管理 |
| Airline_plan_2nd_trial | 航班规划迭代优化 |
| Bilibili_Marketing_Session_20260319 | B站营销分析（iPhone Air 案例） |
| expense_tracker | 个人消费追踪与分类 |
| finclaw_export | 金融数据提取与导出 |
| hevy | 健身训练追踪与数据分析 |
| project_manager | 项目任务管理与协调 |
| Skill_collect | Agent 技能发现与收集 |
| Storage_Chip_Industry_Analysis | 存储芯片行业研究报告 |
| Weather_tool | 天气数据查询与预测 |
| Webpage_info | 网页内容提取与分析 |

### 格式对比

| 维度 | Single-Pass（38条） | Multi-Conv（11条） |
|------|---------------------|-------------------|
| Schema | ATIF v1.2（标准化） | Session 格式（原生） |
| 来源 | 合成数据（kimi-k2.5） | 真实 Agent 会话（OpenClaw） |
| 每条文件数 | ~10 | 1-5 |

## Organization

Published by [OBay Data](https://huggingface.co/obaydata) — specializing in AI training data production.
