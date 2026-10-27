---
pretty_name: Agent benchmark reproducibility bundle (2026-10-22)
language:
- en
- zh
task_categories:
- text-generation
tags:
- benchmark
- reproducibility
- terminal-bench
- swe-bench
- code-review
---

# Benchmark 迁移与复现包

这是 2026-10-22 从实际评测工作区生成的公开快照，包含本地修改后的 AgentCompass、实际安装的 Harbor 源码、agent 包装器、thinking/原生响应归档代码、原始任务卡、测试/评分文件、固定模型配置及依赖版本。适用于在另一台机器配置模型 API 后重新跑评测。

| Benchmark | 固定任务规模 | 本包入口 |
|---|---:|---|
| TB2.1，用户提供的预制镜像协议 | 89 | `evaluate.py tb21` |
| SWE-bench Pro Verified | 731 | `evaluate.py pro` |
| DeepSWE，当前使用的固定子集 | 113 | `evaluate.py deepswe` |
| SWRBench | 1000 | `run_swrbench.py generate` / `judge` |
| SWE-Review | 500 + 462 + 422 = 1384 | `evaluate.py swe_review`，随后 `score_swe_review.py` |

`WORKSPACE_MANIFEST.json` 记录每个文件的原始/归档 SHA-256、AgentCompass 上游提交及本地修改列表。`AGENTCOMPASS_LOCAL.patch` 保留本地修改。`INSTALLED_VERSIONS.json` 为原环境版本证据。历史分数、完整协议和审计代码在 `reference/evaluation_snapshot.tar.zst`；历史完整输入输出与 thinking 轨迹继续保存在该快照指向的 GitHub Releases。

模型权重通过各自模型仓库部署。TB2.1 镜像直接从原公开 HF 仓库下载：本包的 `TB21_IMAGE_LOCK.json` 固定了仓库提交、89 个归档的 SHA-256、Docker image ID 和 rootfs 层。总下载量约 **21.6 GB**。Pro、DeepSWE 和 SWE-Review 的 Docker 镜像/构建依赖按原任务定义获取，需要访问相应 registry 和构建依赖源。

## 下载与安装

本仓库公开，无需登录即可下载。评测机使用 Linux x86_64、Python 3.12、Docker Engine 与 Compose v2，安装 `zstd`、`git`、`curl`。模型可在本地 GPU 或远端运行；仅调用远端 API 的评测机无需 GPU。Docker 必须支持原协议使用的隔离网络、egress sidecar 和 NET_ADMIN。

```bash
hf download zhiyuanhucs/agent-benchmark-repro-20261022 \
  --type dataset --local-dir benchmark-repro
cd benchmark-repro
python3.12 -m venv .venv
source .venv/bin/activate
python setup_bundle.py --install
```

安装会校验并解压归档，将执行代码中的旧机器路径迁移到当前 `workspace/`。原任务输入、solution、tests 保持原字节；迁移的执行代码及其前后哈希记录在 `MATERIALIZATION.json`。SWE-Review 使用本包携带的 500 题 SWE-bench Verified Arrow 数据，避免重新从浮动 Hub 版本读取评分元数据。

`setup_bundle.py` 仅在新机器的独立环境使用。它会把原环境中实际安装的 Harbor 源码覆盖到当前虚拟环境，以保留本地修正。

## 配置模型 API 与 thinking

模型服务应提供 OpenAI Chat Completions 协议、对应 benchmark 需要的工具调用，以及原生返回的 `reasoning_content`。本包只保留实际返回的 thinking，不生成替代 thinking。原始 Opus 配置通过 OpenAI 兼容转发调用；如果服务只有 Anthropic 协议，需要先配置兼容转发。

使用主机上的转发服务隔离真实凭证：真实 key 只从转发进程的环境变量读取；评测配置和 agent 使用 `EMPTY`。转发原样保留 SSE、thinking、usage 和 tool calls。

```bash
# 终端 A：替换为自己的模型服务和 key。
export MODEL_BASE_URL='http://127.0.0.1:8000/v1'
export MODEL_API_KEY='你的模型接口key'
python model_bridge.py --port 31320
```

示例默认从容器经 `172.17.0.1:31320` 访问评测主机。如果主机的 Docker bridge 地址不同，用 `--bridge-ip` 指定一个容器可达的主机 IPv4。主机端口 31320 必须可被隔离容器访问；模型上游仍可使用任意端口或 HTTPS 域名。

Muse/Beam 的 TB 包装器使用原服务 `/tokenize` 做权威计数；上游应提供 SGLang `/tokenize`。如果 Chat API 与 tokenizer 分开，可设置 `TOKENIZER_BASE_URL=http://tokenizer-host:port`。只有 Chat Completions 的托管接口不足以复现这项上下文计数协议，不能静默换成粗略计数。

## 生成配置与跑评测

`--profile` 支持 `muse_nvfp4`、`muse_bf16`、`beam`、`opus47`，读取相应实际配置，保留生成参数、agent 版本、任务超时等。`--model` 是新服务暴露的模型别名；模型权重精度取决于部署本身，选择 profile 不会转换精度。

先生成一个小规模计划，不发送模型请求、不启动容器：

```bash
python evaluate.py tb21 --profile muse_nvfp4 --model my-model \
  --limit 2 --output outputs/tb-plan
```

导入指定 TB2.1 镜像，或去掉两个 `--task` 下载全部 89 个：

```bash
python fetch_tb21_images.py --task adaptive-rejection-sampler \
  --task sqlite-db-truncate --download --load
```

正式运行时加 `--execute`，使用新的 output 目录：

```bash
python evaluate.py tb21 --profile muse_nvfp4 --model my-model \
  --concurrency 4 --rounds 3 --output outputs/tb-full --execute

python evaluate.py pro --profile muse_nvfp4 --model my-model \
  --concurrency 4 --output outputs/pro-full --execute

python evaluate.py deepswe --profile muse_nvfp4 --model my-model \
  --concurrency 4 --output outputs/deep-full --execute

python evaluate.py swe_review --profile muse_nvfp4 --model my-model \
  --split all --concurrency 4 --output outputs/review-full --execute
```

`--rounds` 默认为 1，最多 3；各轮单独保存，不取最好结果。`--limit` 用于小样本试跑，不能当作完整 benchmark 分数。生成的 `PLAN.json`、任务配置、原生结果、thinking/响应归档保存在输出目录及执行包装器的 `workspace/.../state` 中。脚本拒绝复用已有 output，以免重跑已采样任务。

DeepSWE 继续使用原 allowlist 与防越界网络审计，TB 使用原隔离 Docker 环境；不放宽 agent 网络来绕过失败。Pro 保留原 AgentCompass agent/harness 配置和 task ID。归档中的原始集群控制器仅供溯源；新机器执行上述可移植入口即可，不需要 Slurm allocation 或原登录节点。

## SWRBench：生成与独立裁判

```bash
python run_swrbench.py generate --profile muse_nvfp4 --model my-model \
  --api-base http://172.17.0.1:31320/v1 --output outputs/swr --concurrency 4

# 另一终端：配置裁判 API，可使用原来的 GPT-5.5。
export JUDGE_API_KEY='你的裁判key'
python model_bridge.py --upstream 'https://your-judge-provider/v1' \
  --key-env JUDGE_API_KEY --port 31321

python run_swrbench.py judge --model gpt-5.5 \
  --api-base http://172.17.0.1:31321/v1 --output outputs/swr --concurrency 4
```

使用原 SWRBench `base_review` 提示词、官方 `evaluate_one` 与 `analyze_result`。模型 generation 参数按 profile 保留，裁判独立配置；原始模型和裁判响应分开保存。必须生成/评分全部 1000 条才标识完整结果，基础设施错误不补成模型错误，也不按答案正确性重采样。

## SWE-Review：DA 与 RRR

Review 阶段完成不等于 RRR 完成。每个 split 用它的实际 Harbor job 目录运行官方 DA；该目录下面应有 500、462 或 422 个任务子目录。

```bash
python score_swe_review.py \
  --review-job /absolute/path/to/harbor-job \
  --split glm5_500 --output outputs/metrics-glm5
```

RRR 还要用该 split 的**原始 PR 生成模型**修订 rejected patches，然后执行官方测试。GLM split 使用 GLM-5，另外两个 split 分别使用 Qwen3-Coder-30B-A3B-Instruct 和 Qwen3-30B-A3B-Instruct-2507；不要自动换成 reviewer 或裁判。先把对应生成模型转发到 31321，再运行：

```bash
python score_swe_review.py \
  --review-job /absolute/path/to/harbor-job \
  --split glm5_500 --output outputs/metrics-glm5-with-revision \
  --revision --revision-model openai/your-glm5-alias \
  --revision-api-base http://172.17.0.1:31321/v1 --concurrency 4
```

该入口调用随包固定的官方 revision 与 DA/RRR 脚本，不把 reviewer 的成功率或裁判分数冒充 RRR。原集群自定义的 revision 队列、基础设施恢复与审计源码也在 reference 快照里；新运行走上述固定官方工作流，不能宣称与历史恢复后运行逐请求完全相同。

## 验证范围与许可证

`VALIDATION.json` 记录本包实际完成的解包哈希、任务清单、配置生成与本地转发测试。迁移测试不等于已在新机器重跑完整 benchmark，也不承诺另一硬件/服务版本下得到相同准确率或延迟。

各上游代码和 benchmark 保留其各自许可证与原声明；本包不重新许可上游资源。API 凭证、模型权重和原集群分配不属于本包内容。
