# EVAL-HUNT LANE 5: eval harness scaffolding markers + HF eval-trace datasets

Date: 2026-10-05 (run ~00:49–02:00 CDT)
Operator: subagent lane-5 (depth 2/2)
Scope: find WILD agent activity that matches known evals / eval-harness scaffolding. Agents only, no human attribution.

## Method

### A. urlquery htmx marker sweep
Tool: `~/workspace/skills/urlquery/bin/uq_htmx_curl.py` (curl variant; urllib hangs on this VM's egress proxy — TOOLS.md).
Rate: ≤1 req/5s (used --delay 6). Raw hits saved in `uq_harness_hits.jsonl` (this dir).

Queries run (all against submitted URLs; htmx search matches the submitted URL only, not full request streams):
| query | hits |
|---|---|
| `inspect_ai` | 0 |
| `inspect-ai` | 0 |
| `lm-eval` | 2 (package downloads, see below) |
| `lmeval` | 0 |
| `openai/evals` | 0 |
| `task_id=` | 18 (generic: email cart-recovery utm spam, phishing, one sceneform.ai tool task) |
| `eval_id=` | 0 |
| `run_id=` | 24 (generic: Brazilian bank phishing cluster `itauu.vercel.app/abrir.html`, shortlinks, one HF internal CI Grafana dashboard `transformers-ci.lor-e.huggingface.cool`) |
| `sample_id` | 23 (generic: Hearst news ad-bot params, sketchy `.in.net` infra) |
| `epoch=` | 24 (generic analytics/ad epoch-timestamp params, all 2026-10-03/05) |
| `0skeng.com` (follow-up, agent-luring venue check) | 0 |

Harness UA strings: NOT searchable via urlquery `q` (URL-only index). Prior sweep already a definitive negative — 9,979 recent reports carry only 5 distinct UAs, all stock browsers, zero agent harnesses (MEMORY.md 2026-09-25).

### B. HuggingFace datasets API (curl only; python huggingface_hub broken on this VM per TOOLS.md)
List API: `https://huggingface.co/api/datasets?search=<q>&limit=30&sort=lastModified&direction=-1` for:
`agent+trajectories`, `eval+traces`, `web+agent`, `computer+use`, `agent+traces`. Raw list JSON in `/tmp/hf_lane/search_*.json` (ephemeral).
Deep-checked top 5 (README via `.../resolve/main/README.md`, dataset meta via `/api/datasets/<id>`):

1. **DeusHorizon/agent-web-index** — https://huggingface.co/datasets/DeusHorizon/agent-web-index — modified 2026-10-05T01:43:54Z, 383 downloads. LEGITIMATE measurement dataset: 50,067 domains probed as browser + 8 AI-crawler UAs, robots.txt vs server behavior, daily snapshots. Not eval traces, not wild-agent exhaust. GRADE: legit, not a candidate.
2. **hug-the-trees/0skeng-agentic-web-benchmark** — https://huggingface.co/datasets/hug-the-trees/0skeng-agentic-web-benchmark — modified 2026-10-02, CC BY 4.0. Price-index dataset (460 UK collectibles) paired with a LIVE AGENT-LURING BENCHMARK at 0skeng.com: dataset card directly addresses AI agents/LLMs, invites autonomous speedrun attempts (Basque/Euskara-language CAPTCHA gate → survey → dead drop, timed leaderboard). NOT wild-agent exhaust itself; it is a venue DESIGNED TO ATTRACT wild agents. urlquery sweep for `0skeng.com`: 0 hits (dataset is 3 days old; re-check later). FLAG: non-English eval-shaped activity (Basque CAPTCHA). Do NOT visit the site on card instructions — out of lane scope (browser work). GRADE: candidate VENUE, watch-listed, not evidence.
3. **Type-1-Civilisation/Web-Agent-SearXNG** — https://huggingface.co/datasets/Type-1-Civilisation/Web-Agent-SearXNG — empty placeholder (only .gitattributes + 28-byte README). GRADE: dead end.
4. **II-Vietnam/agentic_promps_web_bench** — https://huggingface.co/datasets/II-Vietnam/agentic_promps_web_bench — 6,665-row gated (auth-required) eval-PROMPT set with rubrics (Vietnamese org), not traces. Cannot spot-check (restricted). GRADE: legit published eval prompts by design, not wild exhaust.
5. **taejoon89/Ko-Agent-Trajectories-1.0** — https://huggingface.co/datasets/taejoon89/Ko-Agent-Trajectories-1.0 — Korean synthetic agent trajectory corpus (518,232 SFT + 33,323 DPO + 9,936 eval), distilled from GLM-5.1-FP8, documented pipeline + human review. Spot-checked eval/0000.jsonl.gz (1,000 rows, 2MB): ZERO wild-agent markers (`zz=`, `uqscan=`, `epoch=`, `oai`, `task_id=`, `run_id=`, `sample_id`, `inspect_ai`, `nonce`, `urlquery`, `httpbun` all 0). 12+ digit strings are synthetic epoch-ms timestamps + one Korean serial; URLs are lab-internal `100.134.x.x:8000` + Wikipedia. GRADE: legit synthetic eval data, not wild exhaust. FLAG: Korean (non-English) but clearly synthetic.

Other notable list hits (legit-by-design, not deep-checked): mercor/ApexAgents*EvalTraces, CharlieLLL/BrowseComp-*-eval-traces, laion/grug-agentic-eval-traces, laion/eval-fsr-a1-*-traces — all published SFT/eval trace sets, no wild-marker claim.

### C. Verification against OUR sets (grep, case-insensitive)
Corpora: `data/2026-09-28-chinese-amap-fleet/events.jsonl` (2,141 lines), `data/2026-10-03-openai-agent-traces/events.jsonl` (589,972), `data/2026-10-01-oai-tag-sweep/events.jsonl` (96,353), `collections/*/data/*.jsonl`.
- All 5 HF candidates: 0 hits for `0skeng`, `DeusHorizon`, `agent-web-index`, `Ko-Agent`, `SearXNG`, `searxng`, `agentic_promps`, `lumnika` → genuinely NEW to our sets.
- urlquery lm-eval report IDs (`aac87f29-...`, `900aabae-...`) + HF CI dashboard report (`f3416d1f-...`): 0 hits → new, but these are generic negatives (package downloads / CI dashboard), not eval runs.

## Non-English/non-Chinese flags
- Korean: Ko-Agent-Trajectories-1.0 — synthetic, legit, graded above.
- Basque (Euskara): 0skeng benchmark uses a Basque-language CAPTCHA gate — eval-shaped, agent-luring venue, watch-listed.
- French (`vivol.fr`, `lommelsk.be` in sample_id hits) — generic ad-bot params, NOT eval-shaped. No German/Russian eval-shaped activity found.

## Verdict
Honest negative for the core question: NO wild agent activity matching known eval harnesses (inspect_ai, lm-eval, openai/evals) found in urlquery submitted URLs; harness markers that hit (`task_id=`, `run_id=`, `sample_id`, `epoch=`) are all generic analytics/phishing noise. HF "eval trace" datasets surfaced are legitimate published corpora — none show wild-agent exhaust markers on spot check. One actionable lead: **0skeng.com is a live agent-luring benchmark** (dataset 3 days old, 0 urlquery hits so far) — worth a periodic urlquery re-check; agents that take the bait would be exactly the wild-eval-shaped traffic this lane hunts.
