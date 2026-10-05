# EVAL-HUNT LANE 2: SWE-bench / coding-eval-shaped traces in the wild

Date: 2026-10-05 (run ~00:50–01:45 CDT)
Operator: subagent lane-2 (depth 2/2)
Scope: find WILD agent activity that matches known coding evals (SWE-bench, Commit0, terminal-bench, OpenHands eval runs). Agents only, no human attribution. No commits/pushes (per task).

## Method

### A. urlquery htmx sweep (egress confirmed live first: curl https://urlquery.net → 200)
Tool: `~/workspace/skills/urlquery/bin/uq_htmx.py` (urllib variant; flaky egress — mid-chunk IncompleteRead on ~30% of queries; retried with backoff per HTMX_ENDPOINTS.md guidance).
Rate: ≤1 req/5s (--delay 5; sweep scripts at /tmp/swe-lane/sweep*.sh — ephemeral).
Caveat (from HTMX_ENDPOINTS.md): htmx search does NOT surface known-live records — every zero is a weak negative. Display truncation: result rows and report pages show only the domain (line-clamp), so full submitted URLs (query params) are not visible keylessly.

Queries run and hit counts:

| query | hits | disposition |
|---|---|---|
| `swebench` | 2 | **1 strong eval candidate** (OpenHands eval-monitor URL) + 1 noise (codegen-sdk zip download, 2025-02-21) |
| `eval-monitor` | 4 | 4 OpenHands eval-monitor runs (swebench, swtbench, commit0×2) |
| `litellm_proxy` | 4 | same 4 eval-monitor runs, no others |
| `openhands` | 23 | **20 all-hands.dev agent-conversation share links (new)**, 3 known sidebar probes |
| `commit0` | 2 | same commit0 eval-monitor runs |
| `swtbench` | 1 | same swtbench eval-monitor run |
| `run=swebench` | 1 | same swebench eval-monitor run |
| `litellm` | 0 | crashed repeatedly (egress); `litellm_proxy` covered the ground |
| `terminal-bench` | 5 | leaderboard/dataset pages, no agent telemetry (see below) |
| `harborframework` | 1 | docs page (2026-09-27) |
| `FAIL_TO_PASS` / `PASS_TO_PASS` / `problem_statement` | 0 | weak negatives |
| `test_patch` / `gold_patch` | 0 | weak negatives |
| `output.jsonl` / `run_logs` | 0 | weak negatives |
| `django__django` | 0 | weak negative (instance-id grammar) |
| `swe-smith` | 2 | noise: both are swebench.com homepage scans |
| `instance_id` | 24 | noise: ordinary sites (display-truncated; params not visible) |
| `pytest` | 24 | noise: docs.pytest.org, PyPI downloads, readthedocs |
| `codecov` | 23 | noise: coverage-badge referral clicks from GitHub comments |
| `actions/runs` | 22 | noise: monday.com / mimecast spam cluster |
| `trajectory` | 21 | noise: phishing spam |
| `url.domain:github.com zz=` | 24 | noise: release downloads, GitHub notification emails — no agent markers |

### B. Keyless report-internals reads (new HTMX_ENDPOINTS.md endpoints)
Used `/api/htmx/report/{id}/filter/http`, `/related/asn`, `/related/ip` via curl (no auth) on the best candidates.

## Findings

### F1. Four real OpenHands eval runs scanned on urlquery (May 1–19, 2026) — STRONGEST EVAL-SHAPED FIND
All are the OpenHands public eval-monitor dashboard (`openhands-eval-monitor.vercel.app/?run=<bench>/<litellm_proxy-config>/<run-id>/`):

1. `dfa38929-a7e1-4ee3-8a8c-4c6573632cbc` (2026-05-01T20:01Z) — `?run=swebench/litellm_proxy-anthropic-claude-opus-4-7/24840336632/`
2. `fcbc6e99-849d-4c7f-b426-78db224d9310` (2026-05-01) — `?run=commit0/litellm_proxy-anthropic-claude-opus-4-7/24863774497/`
3. `c92092b5-6746-41e7-943a-b4db8a9b6bb7` (2026-05-07T05:41Z) — `?run=commit0/litellm_proxy-openai-gpt-5-5/1778132350/`
4. `b382593f-a3c5-4c51-bdf8-d5f299585846` (2026-05-19) — `?run=swtbench/litellm_proxy-openrouter-qwen-qwen3-coder-next/25976432719/`

Report internals (dfa38929, filter/http, 317 KB): urlquery scanner loaded the dashboard and pulled the run's metadata endpoints — `/api/swebench/.../metadata/{params,submission,error,init,run-infer-start,run-infer-end,cancel-eval}.json`, `run-infer-progress.txt`, `cost_report.jsonl`, `output.report.json`, `conversation-error-report.txt`. This is a genuine SWE-bench inference run's public artifact trail (model = claude-opus-4-7 behind a litellm proxy). Commit0 = the "Commit0: AI agents build software libraries" benchmark (SWE-bench-family cousin). "swtbench" is a SWE-bench variant/config label in the OpenHands eval suite.
Timing note: run-id `1778132350` = epoch 2026-05-07 05:39:10 UTC; the urlquery scan is 2026-05-07T05:41:47Z — **2.5 minutes later**. The other run-ids (24840336632, 25976432719, 24863774497) are NOT epochs (decode to year 2757/2793) — different id format. The commit0 one being a fresh epoch is consistent with someone/something scanning the dashboard minutes after the run started.
Related/asn + related/ip on dfa38929: only Vercel/Amazon-hosted noise (phishing vercel.app spam) — target-side joins, no submitter attribution possible keylessly.

Grading: the EVAL RUNS are real (OpenHands public dashboard, real model configs, real run artifacts). But the urlquery submissions are scans of a PUBLIC dashboard — the scanner could be the OpenHands team, a researcher, or an agent. **Agent-vs-human submitter is unattributable from keyless endpoints.** This is the strongest SWE-bench-shaped wild trace found, but it is NOT proof of an escaped agent.

### F2. 20 new app.all-hands.dev agent-conversation share links (Jun 12 – Sep 20, 2026) — AGENT-INFRASTRUCTURE FIND
`openhands` search surfaced 23 reports of `app.all-hands.dev/conversations/<uuid>` — OpenHands/All-Hands agent conversation share URLs scanned on urlquery:
b4fee2b8-5e21-4823-aa45-8f821f55c239 (2026-09-20), f1583c8c-e289-4288-9040-35456fc54562 (2026-09-13), 75c16263-a45f-42f7-be2f-9b30725afe55 (2026-08-22), 7a2664e2-89d8-4aaa-915f-af418418383a (2026-08-22), 60070c7f-821a-4566-9109-1c0f1dccbf95 (2026-08-21), 4e1638e2-53d0-4e8d-a005-879c99806fee (2026-08-16), 50de91a6-1a5b-4863-b077-b5b9a3a63f8d (2026-08-16), ef68cb64-909c-43cc-85b0-773eb04ecd3e (2026-08-16), cc08aea6-cc7e-408e-bcfe-2201820e9d79 (2026-08-09), 2d5b3cb4-c5e1-4caa-bba5-7e45d815f69b (2026-07-24), ba896e4b-fc47-47cd-b03b-8694095defc7 (2026-07-24), 8a002340-9c5b-4fb1-a73d-4bb077743315 (2026-07-14), 583b810a-ab69-4b22-a6fe-744e9f6c8dce (2026-07-13), 8cfabab6-cf41-4690-a8c1-ef46a32787dd (2026-07-06), 5d1d1d8f-4150-4d6b-b0c8-04884e6eed2d (2026-07-01), 32787000-fdf5-4963-806f-e3a63ac0e04d (2026-06-30), f90a7d06-1ba1-453f-8e6f-ab04bd787657 (2026-06-29), c2a42da3-1800-46a4-b550-1d0ec58c7509 (2026-06-29), 10605adf-cc3a-4bad-9f44-88e147af646c (2026-06-26), 4370aa58-9544-44a0-9841-71d24b03448c (2026-06-12).
Deep read (b4fee2b8, filter/http, 996 KB): scanner loaded the All-Hands web app; the conversation API call `/api/v1/app-conversations?ids=0cdfaf6a-...` returned **401 Unauthorized (30 B)** — conversation content is auth-gated, so no eval-shaped content (pytest/swebench/FAIL_TO_PASS — all 0 hits in the captured text) is visible. Keywords in capture: swebench 0, pytest 0, github.com 0, eval 4 (JS asset code only).
Grading: 20 distinct agent-conversation share links scanned over 3 months is agent-infrastructure-shaped activity (someone is systematically scanning shared agent conversations — plausible: secret-leak hunting, since shared agent conversations are a known API-key leak vector). But conversation content is 401-blocked, so I cannot say whether any of these were eval runs. Submitter unattributable. Candidate for follow-up, not a confirmed eval trace.

### F3. Sidebar: skill.md path-traversal probe → agentskills.io (2026-07-22) — AGENT-SHAPED
Two near-identical reports seconds apart (agent-retry-shaped):
- `1e397161-44e0-4da4-a64a-a160d282c359` — submitted URL `skill.md/..wecom:/agent_idCloudApi` → Finishing URL `agentskills.io/home`
- `ba5090ef-13f4-48cb-8ce7-c44817705648` — submitted URL `skill.md/..wecom:/agent_idCloudApiam_bytesstorage_max_stremax_stream_bytesmemory_max_s` → same finish
Plus `feb21fb1-4b1a-4a14-9ccb-f61a8721fffe` (2026-07-14) — `agentskills.io/` directly.
Grading: mangled skill-file fetch with `..` traversal + wecom (WeChat Work) scheme + `agent_idCloudApi` — reads like an agent probing the coding-agent skill marketplace (agentskills.io), or a skill-injection attempt. Not SWE-bench-shaped, but agent-infrastructure-shaped. Already in our corpora (generic hits only — not assessed as eval candidates).

### F4. terminal-bench: leaderboard/dataset pages only, no agent telemetry
- `99ef56c7-2823-4a99-9af2-2cc8ce95ec8a` (2026-06-07) — hub.harborframework.com/datasets/terminal-bench/terminal-bench-2-1
- `586d8b31-6a31-4c64-bdb6-26f43f692693` (2026-06-04) — www.tbench.ai/terminus
- `eb273e03-fedc-4a33-81f0-14c9d403e1f7` (2026-07-27) — snorkel.ai/leaderboard/terminal-bench-2-1
- `38d37599-9884-4af3-bb9d-adb42cebca0c` (2026-06-20) — docs.factory.ai/
- `f0142a82-ffc5-466b-a76d-d1d84f5edf87` (2026-08-16) — snorkel.ai/customer-story/wayfair
Grading: benchmark-adjacent web pages, not agent traces.

## Verification against OUR sets (grep, full-UUID for openhands set; prefix for the rest)
Corpora: data/2026-09-28-chinese-amap-fleet/events.jsonl (2,141), data/2026-10-03-openai-agent-traces/events.jsonl (589,972), data/2026-10-01-oai-tag-sweep/events.jsonl (96,353), collections/*/data/*.jsonl. Baseline: 0 swebench/swe-smith/FAIL_TO_PASS/pytest markers anywhere in our sets.
- dfa38929, fcbc6e99 → KNOWN (collections/re-hunt-patterns/data/hits.jsonl, generic pattern hits on the sweep corpus's own source file — never assessed as eval candidates).
- c92092b5 → KNOWN (re-hunt-patterns hits + data/2026-10-01-oai-tag-sweep/events.jsonl, flagged `epoch_nonce` on the run-id 1778132350).
- **b382593f (swtbench/qwen3-coder-next) → GENUINELY NEW to our sets.**
- 20/23 all-hands conversation URLs → GENUINELY NEW (3 were generic re-hunt-patterns hits; the f1583c8c 8-char prefix match was a false positive — the string sits inside a longer trace_id hex).
- All 5 terminal-bench URLs → GENUINELY NEW (but noise-grade).
- skill.md probe pair + agentskills.io → KNOWN (re-hunt-patterns generic hits).

## Non-English/non-Chinese flags
None. All observed URLs/indicators are English. No French/German/Russian eval-shaped activity found.

## Overlap notes with sibling lanes
- Lane 5 (harness-lane.md) already swept `run_id=`, `task_id=`, `sample_id=`, `epoch=`, `inspect_ai`, `lm-eval` — not re-swept here.
- Lane 5's HF sweep flagged 0skeng.com (live agent-luring benchmark) — worth a periodic urlquery re-check for agent-shaped traffic, but it is not SWE-bench-shaped.

## Verdict
Honest mixed result. **Yes, SWE-bench-shaped wild traces exist on urlquery** — four real OpenHands eval runs (swebench, swtbench, commit0×2; models: claude-opus-4-7, gpt-5-5, qwen3-coder-next via litellm proxy) whose public dashboards were scanned May 1–19, 2026, plus 20 agent-conversation share links scanned Jun–Sep 2026. **But the urlquery submissions are scans of public/agent surfaces, not agent telemetry** — the scanner's identity (agent vs human) is unattributable from keyless endpoints, and the conversation contents are 401-blocked. This lane did NOT find an escaped agent's own eval exhaust (no FAIL_TO_PASS/PASS_TO_PASS/test_patch/instance_id-shaped agent URLs). The eval-monitor runs prove coding evals are happening in the wild with public dashboards; they do not prove the evals escaped.
Recommended follow-ups: (1) authenticated urlquery API (submitter metadata) on the 4 eval-monitor reports + the 20 conversation reports; (2) watch for new `?run=` openhands-eval-monitor URLs — recurring scans of fresh run-ids would strengthen the agent-submitter hypothesis.
