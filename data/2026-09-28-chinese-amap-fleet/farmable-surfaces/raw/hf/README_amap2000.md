---
pretty_name: Amap 2,000 Deterministic Mock App Candidate Trajectories v1
language:
- zh
size_categories:
- 1K<n<10K
tags:
- synthetic
- gui-agent
- mock-app
- candidate-trajectories
---

# Amap 2,000 Deterministic Mock App Candidate Trajectories v1

## 数据集摘要

这是一个公开的、确定性生成的 MobileGym-Harmony 高德 Mock App 候选轨迹实验包。它包含 2,000 条候选轨迹，范围固定为 `candidate_experiment_only`，验收状态为 `pass_with_non_promotion_boundary`。

本包不是正式交付包，不是真实模型 rollout，不是真实高德采集，也没有证明这些数据适合训练或评测模型。

## 两条冻结链路

1. `chain_1_route_mode`：针对目标地点查看步行、骑行、驾车或公交路线；四种模式各 250 条，共 1,000 条。
2. `chain_2_nearest_compare`：在最近 N 个候选中，按最高评分或最低价格进行选择，再查看步行或骑行路线；四个交叉组合各 250 条，共 1,000 条。

显式投影与上下文投影各 1,000 条。所有轨迹均来自确定性的本地 Mock App 合成状态。

## 数据规模

- planned / produced / valid / current failed：`2000 / 2000 / 2000 / 0`
- 轨迹目录：2,000
- 动作记录：22,667
- 合成 Mock App JPEG 截图：22,836
- 截图视口：360 × 800
- 冻结任务家族：2
- 冻结叶子链路：8
- 独立 task ID、scenario ID、seed 和 scene hash：各 2,000

## 验证证据与边界

- 最高验证等级：V4。
- Amap app-link readiness：`not_ready`。
- 正式 Loop 2：`blocked_at_T0_not_ready`，未执行。
- 人工视觉复核：`not_performed_user_opt_out`。
- 严格 judge 负例测试：35 passed / 0 failed。
- reset/replay 抽样：15/15 projection equality，15/15 terminal equality；154/154 个 Mock App 业务区域截图步骤在既定容差内。
- 截图校验采用业务区域和有界像素容差；不要求 JPEG 全帧字节完全一致。

`2000 / 2000 / 2000 / 0` 只表示确定性合成器和校验器对冻结 Mock App 契约的通过情况。它不能解释为真实 Agent 成功率、真实模型成功率、真实高德成功率、自然语言泛化能力，或训练/评测有效性。

## 不包含的内容

本发布包不包含：

- 真实高德 App 采集或真实高德截图；
- 真实用户、账号、地点、订单、导航行为或个人信息；
- 本地受限视觉 oracle、A1/A2 采样文件或采样路径；
- Token、密码、API Key、私钥或本机绝对路径；
- 内部实施 brief、运行日志、恢复文件、进度分片或计划备份；
- 真实模型 rollout 或正式 Loop 2 产物。

轨迹中的地点名称、地址、距离、价格、评分、路线和 ETA 均为 Mock App 的合成内容，不代表真实地图实体或可执行导航结果。

## 文件结构

```text
README.md
RELEASE-MANIFEST.json
PUBLICATION-SAFETY.md
metadata/
  candidate-acceptance-report.json
  frozen-task-plan.json
  pool-manifest.json
  replay-summary.json
  scenario-pool.jsonl
  strict-judge-negative-report.json
  task-plan.jsonl
  validation-report.json
schema/
  mobile-action-space.json
  trajectory-schema.json
data/
  trajectories-000001-000250.tar.gz
  ...
  trajectories-001751-002000.tar.gz
checksums/
  CONTENT-SHA256SUMS
  SHA256SUMS
```

每个归档分片包含 250 个 `trajectories/amap_candidate_task_XXXXXX/` 目录。`CONTENT-SHA256SUMS` 校验解包后的轨迹成员，`SHA256SUMS` 校验发布包文件和归档本身。

## 适用范围

可以用于检查确定性 Mock App 候选轨迹的目录结构、动作 schema、合成 UI 状态和离线 judge 证据。任何训练、评测、真实导航、真实订单或产品成功率结论都需要独立的数据治理、真实运行时验证和人工审查；这些工作不在本发布包的证据范围内。

## 许可说明

本发布没有声明标准化 license 元数据。公开可访问性不应被解释为超出适用法律和权利范围的额外授权。
