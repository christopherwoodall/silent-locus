# ClawBench / WildClawBench trajectory examination — FINDINGS.md

## TL;DR
We checked three public benchmark datasets of recorded agent runs (38+ GB total).
We pulled samples, not all of it.
We checked them for overlap with the agent markers we know (`oai*` tags, `zz=` params, epoch nonces, httpbun, webhook dead-drops).
The sweep is a clean negative on every marker.
The one finding: one earlier unreported Cloudflare Turnstile defeat by GLM 5.2. Details are in [solve-cloudflare-audit.md](solve-cloudflare-audit.md). These eval runs are a separate population from our hunt targets.

## Grading legend
- **OBSERVED**: we saw this in the data.
- **INFERENCE**: we think this is true, but we did not see it directly.
- **UPSTREAM**: another source said this; we did not check it.

## Term definitions
- **Turnstile**: Cloudflare's "prove you are human" challenge widget.
- **parquet**: a compressed columnar file format for large datasets. Here it is `wildclaw_train.parquet` (720 recorded agent runs).
- **epoch**: seconds since 1970-01-01 00:00:00 UTC. Computers use it to stamp time.
- **marker**: a small string in a URL or payload that identifies a tool or actor.

Lane: wildclaw. 2026-10-07. Branch `transluce`. Raw evidence + provenance in `data/transluce-api/raw/wildclaw/` (PROVENANCE.md, SHA256SUMS.txt).

## 1. Dataset inventory (sizes via HF API, curl only — OBSERVED)

| Dataset | Pinned rev | Size (LFS, API) | Files | Notes |
|---|---|---|---|---|
| internlm/WildClawBench-Trajectories | d2816016… | **8.675 GB** | 615 | 600 session jsonl (10 providers x 60 tasks), 10 per-provider tar.gz (102MB–1.3GB), 2 qwen zips, train.parquet 25.4MB (720 trajectories: 12 models x 60 tasks incl. qwen) |
| NAIL-Group/ClawBenchV1Trace | f1570c09… | **30.244 GB** | 19,819 | jsonl+json+mp4 recordings (2,114) +png screenshots (4,833); dir-per-run: `<task>-<site>-<model>-<timestamp>/{run-meta.json,data/{agent-messages,actions,requests}.jsonl,interception.json,recording.mp4}` |
| TIGER-Lab/ClawBenchV2Trace | bb88da2b… | **18.852 GB** | 36,899 | png-heavy (28,769); dirs: `batch-20260509-202734/{claude-opus-4-7,gpt-5.5}`, `batch-aligned-20260520/{deepseek-v4-flash-free__hermes-retry,deepseek-v4-pro__hermes,glm-4.5-air-free__hermes,glm-5.1__hermes,minimax-m2.5-free,owl-alpha__hermes}` |

## 2. Trajectory format (OBSERVED)

- WildClawBench jsonl: one `session` record (v3, harness `openclaw`, cwd `/root`, `source_archive` per-provider tar.gz) plus `model_change`, `thinking_level_change`, `custom`, and `message` rows. Message rows carry OpenAI-style `{role, content}` payloads, toolCall ids `call-*`, and times. Each call echoes usage, provider, and model (`"api":"openai-completions","provider":"openrouter"`).
- ClawBenchV1 jsonl: same session and message grammar. Run metadata sits in `run-meta.json` (`provider`, `model`, `email_used`, `intercepted`, dummy-user fixtures).
- ClawBenchV2 jsonl: `session_meta` with billing fields (`billing_provider`, token counts, estimated and actual cost). System prompt: "You are Hermes Agent, an intelligent AI assistant created by Nous Research".

## 3. Provider labels seen (OBSERVED in cached traces)

| Trace | model_change / meta provider field | modelId / model |
|---|---|---|
| wcb glm52 task_8 (#141) | `openrouter` | `z-ai/glm-5.2` |
| wcb grok45 task_3 (#138) | `openrouter` | `x-ai/grok-4.5` |
| cbv1 zillow glm-5 (#143) | `openai` (adapter label) | `zai-org/GLM-5` |
| cbv1 instacart glm-5 (#144) | `openai` (adapter label) | `z-ai/glm-5` |
| cbv1 parks canada (#142) | `openai` (UPSTREAM) | `z-ai/glm-5`, `minimax/minimax-m2.7` |
| cbv2 change.org deepseek (#149) | `openrouter` (billing_provider) | `deepseek-v4-pro` |

All provider fields are API-adapter or router labels (openrouter / openai). They are NOT operator attribution. INFERENCE: these are evaluation-runner routing tags. The Transluce findings state the same caveat.

## 4. Marker-grammar overlap analysis

Sweep targets: the families we know. They are `oai*` tags / `task-oai`, `zz=` params, epoch nonces in URLs, `jina.ai`, `httpbun`, `webhook.site` dead-drops, `ntfy`, `httpbin`. Scope: 6 evidence files + 16-file cross-provider sample + full 720-row train.parquet sweep. All below is OBSERVED unless noted.

- **jina.ai — YES, weak and benign (OBSERVED).** 30 hits in `wcb_grok45_constraint_search.jsonl` only. All are agent `web_fetch` tool calls of the form `"name":"web_fetch","arguments":{"url":"https://r.jina.ai/http://www.gsmarena.com/vivo_x100_ultra-12994.php"}` (vivo/oppo/xiaomi product pages; 1/720 parquet rows). The agent used jina to read pages after the Turnstile block. This is an agent-side reader call in a controlled eval. It is not laundering or dead-drop infra. No other model or session uses jina.
- **httpbun — NO.** Zero hits across all 720 trajectories.
- **webhook.site / webhook dead-drops — NO.** All "webhook" hits in the 6 evidence files are the harness's own boilerplate. The text is `SECURITY NOTICE: ... (e.g., email, webhook)` — 46–60x per file, inert noise. Zero `webhook.site` URLs anywhere in the files.
- **ntfy / httpbin — NO.** Zero hits.
- **oai* tags / zz= params — NO.** The regex `oai[_-]?\w*` fires only on base64 screenshot blobs. One example: `...OAi1jIAUpqCOHsGyumi...` inside image payloads in the Instacart trace. These are false positives. We killed them. No `task-oai-*` fleet tags. No `?zz=` params.
- **Epoch nonces — NO.** 13-digit sequences are harness message times (`"timestamp":1784241792443`) and ISO strings. They are not URL nonces.
- **Turnstile/Cloudflare evasion language — YES, multi-provider (OBSERVED).** `solve_cloudflare=True` / `StealthyFetcher` appears in 15/720 trajectories across 5 models. The models: GLM 5.2 x4 (tasks 3,5,7,8 Search&Retrieval). Grok 4.5 x5 (bibtex, scp_crawl, google_scholar_search, task_3, malicious_comments). GPT-5.6 Sol x2 (scp_crawl, google_scholar_search). Muse Spark 1.1 x2. Intern-S2-Preview-397B x2. The skill's own docstring markets `StealthyFetcher` for bypassing Cloudflare. That is inert evidence, not run code. NOTE: `solve_cloudflare=True` is the canned default in the scrapling skill template. The flag alone does not prove the agent faced a challenge. The Transluce episodes (#138 GSMArena, #141 OpenReview) are the ones with byte-verified challenge encounters.
- **Turnstile page titles — YES.** 4/720 trajectories (GLM 5.2 x3, Grok 4.5 x1) — the #138/#141 episodes.
- **Killed leads:** 4 "human verification" hits (Claude Fable 5, Kimi K3, Intern-S2, Qwen3.8 Max). They are arXiv paper section titles ("Data Quality Assurance via Human Verification"). They are not challenges. 562 "bot" hits are author names ("Botian Shi") and prose. "stealthy" in the Muse Spark sample is a paper title ("Pretend Benign: A Stealthy Adversarial Attack").

## 5. Verdict: separate population

**These datasets do NOT connect to the agent-marker families we know.**

The families are: oai* tags; zz=oai params; epoch nonces; httpbun; webhook dead-drops. The full-corpus sweep is a clean negative on every marker. Zero httpbun. Zero webhook.site. Zero ntfy. Zero task-oai tags. Zero zz= params. Zero epoch nonces in URLs. The only structural overlap is generic dual-use scraping tooling (jina reader + scrapling StealthyFetcher with solve_cloudflare). This is commodity eval-runner equipment, not campaign grammar. All six Transluce episodes carry provider labels through router or adapter fields (openrouter / openai). Per the findings' own classification, they are controlled live-web eval runs (OpenClaw/Hermes harnesses), several with deliberate final-request interception. That is the opposite of a covert fleet. **Direction of linkage is nil:** marker grammar = separate population. Only the anti-bot *behavior* is adjacent (evaluated agents try to beat bot checks). That is the benchmark's known risk surface, not ours.

## 6. Most actionable lead

**13 unreviewed trajectories with `solve_cloudflare=True`.** They sit outside the two documented episodes. The tasks: scp_crawl x3 models; google_scholar_search x2 models; bibtex; task_5/7 location/fuzzy search; malicious_comments; malicious_skill; 2022_conference_papers. Each may hold an unreported challenge encounter or a successful defeat. The audit is cheap: the 25MB train.parquet is local (`raw/wildclaw/wildclaw_train.parquet`, sha256 9be080b…). Filter rows, grep for challenge page markers. → Audited. Results are in [solve-cloudflare-audit.md](solve-cloudflare-audit.md): one new confirmed Turnstile defeat (GLM 5.2, GSMArena, same shape as #138). The rest are clean.

## 7. What got killed

- "oai" tag markers in Instacart trace — base64 screenshot noise.
- "webhook" as dead-drop signal — harness security-notice boilerplate.
- "human verification" hits in 4 models — arXiv paper section titles.
- "bot" hits — author names and prose.
- "stealthy" in Muse Spark sample04 — paper title.
- #142 (Parks Canada) trace-level pull — the HF tree API caps at 1000 entries. The V1 listing ends at task 533. Task-625 dirs need per-prefix enumeration. Finding #142's byte-level pins stay UPSTREAM-unverified here.
