# NOTES — tau-bench

- Source URL: https://github.com/sierra-research/tau-bench (git clone --depth 1, commit 59a200c6d575d595120f1cb70fea53cef0632f6b, 2026-03-18)
- Homepage: https://github.com/sierra-research/tau-bench
- Eval org: Academic (Sierra Research)
- License: MIT
- Retrieved: 2026-10-05
- Raw: raw/tau-bench/ (full repo clone; questions extracted from tau_bench/envs/airline/tasks.py and tau_bench/envs/retail/tasks.py)
- Banked questions: 165 / expected 165 (50 airline + 115 retail, paper) — MATCH
- Included: yes — user instructions for tool-calling agents (booking/shopping); not web-search questions but agent-task prompts
- Normalization: `tasks` list exec'd from each tasks.py; question_id = tau-{airline|retail}-{i:03d}; topic = domain. No telecom env dir exists in this repo snapshot (telecom is a v2 addition elsewhere).
