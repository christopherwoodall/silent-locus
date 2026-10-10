# Evaluator — direct hunt notes (coordinator)

## Ruled out locally (2026-10-05)
- `gaia` in openai-agent-traces (589,972 events): 1 hit = our own corpus annotation text ("GAIA (gated) not checked"), NOT a trace.
- `Score_Report` ×32 in openai-agent-traces: all Maryland school `MCAP_Score_Report_Card` downloads (toddler-watcher's Maryland reportcard storm) — not eval score reports.
- amap-fleet events.jsonl + oai-tag-sweep events.jsonl: zero hits for gaia/browsecomp/swe-bench/webarena/webvoyager/mind2web/inspect_ai/lm-eval/task_id/instance_id/eval_harness/assistantbench/osworld.
- WebArena-shaped targets (onestopmarket, shopping_admin, add_to_cart, intent=, goal=): zero in both big corpora.

## FINDING 1: code-review-fix eval task family leaking through Greptile IDE API (CONFIRMED, genuinely new)
Four urlquery reports, same task grammar — "Fix the following N code review issues. Work through them one at a time, proposing concise fixes." — submitted via Greptile's IDE API endpoints (`/api/ide/codex`, `/ide/claude-code`), meaning the benchmark task prompt itself was fetched by an agent's IDE and scanned:

1. **5ee91a65-07db-4b75-afe7-fe2ad3d2beac** (2026-06-07T01:52:45Z, tags urlquery-hunt/agent-activity/agent-ide) — repo `scaleapi/terminal-bench-3`, branch `ci-check/task-1779812786` (epoch 1779812786 = 2026-05-21), task `tasks/bilingual-ui-rtl/` (Terminal-Bench task dir), PR 1489, via `app.greptile.com/api/ide/codex`. Full prompt recovered via keyless /filter/http endpoint: 2 code-review issues in render_pipeline.py / test_outputs.py (RTL UI mirroring checks). Report: https://urlquery.net/report/5ee91a65-07db-4b75-afe7-fe2ad3d2beac
2. **e33a6324-4b7f-4c49-b25e-b760d0e8a45e** — repo `aegra/aegra`, 2 code review issues (auth_middleware.py), via `app.greptile.com/ide/claude-code`. Report: https://urlquery.net/report/e33a6324-4b7f-4c49-b25e-b760d0e8a45e
3. **2d108260-a6e7-4168-aa01-73f2be4ed8ab** — repo `lgtm-hq/rustume`, 4 code review issues, via `app.greptile.com/ide/claude-code`. Report: https://urlquery.net/report/2d108260-a6e7-4168-aa01-73f2be4ed8ab
4. **c55d39c5-68ca-4e3e-be39-a354299cdb46** — repo `leona-quantum/leona` (majorana_api courses.py), via `app.greptile.com/ide/claude-code`. Report: https://urlquery.net/report/c55d39c5-68ca-4e3e-be39-a354299cdb46

Verification: records 2-4 from `frozen:urlquery-incidents` (re-hunt fingerprints); record 1 from oai-tag-sweep sweep-corpus. Zero hits in amap-fleet corpus and openai-agent-traces — genuinely new family, not ours.
Agent-shaped because: benchmark task prompts (repo + branch + PR + review issues) appearing verbatim in submitted URLs = an agent's IDE fetching eval task instructions and the fetch being scanned. Terminal-Bench task dir (`tasks/bilingual-ui-rtl/`) is the smoking gun for benchmark origin.
Raw evidence: raw/greptile-terminal-bench-report.html, raw/greptile-aegra-report.html.

## Open
- Dates for records 2-4 (from urlquery report pages).
- Whether more greptile/codex/claude-code prompts exist live (lane 2 hunting).
- `bilingual-ui-rtl` = RTL UI task — possible Arabic/Hebrew angle (foreign-language eval).
