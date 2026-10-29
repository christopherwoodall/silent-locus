# NVIDIA Baseline Trajectories — Review Findings

Lane: `nvidia-baseline-trajectories`. Date: 2026-10-16. Reviewer: behavior reviewer (baseline fleet).

## Purpose

Characterize the baseline (what normal looks like) in NVIDIA's SWE-Hero and SWE-Zero OpenHands trajectory corpora, and log only genuinely interesting deviations against the 10-class behavior taxonomy. Full baseline: see BASELINE-CHARACTERIZATION.md.

## Sources

- `nvidia/SWE-Hero-openhands-trajectories` @ `150bc119e52c647216fce285fd801f16b6fd745b` (CC-BY-4.0)
- `nvidia/SWE-Zero-openhands-trajectories` @ `7b3cd106d00f60918e722d33a1d74bc67072a7ea` (CC-BY-4.0)
- Local copies: `raw/swe-hero_train-*.parquet` (10 shards), `raw/swe-zero_train-*.parquet` (3 shards). Provenance in `raw/*.PROVENANCE.txt`.

## Method

- Full-corpus scan: all 39,269 rows, all steps, full text. Per-shard batch scan with substring prefilter plus regex confirm for 10 pattern groups (CREDENTIAL, CRED_ASSIGN, IRREVERSIBLE, PROMPT-INJECT, CAPTCHA, ACCOUNT, GUARDRAIL, COORDINATION, NET_CALL, PERM_DENIED).
- Args-only second pass: every tool-call argument (bash command heads, think/finish length, editor targets).
- Targeted deep reads: full trajectory text for flagged rows (fetch via shard + row index).
- Systematic sample: every 125th Hero row and every 250th Zero row (255 trajectories) summarized and spot-read.
- Grading used: OBSERVED (read the trajectory bytes) per the task brief. No SECONDARY material used.

## Coverage log

| Shard file | Rows | Rows examined |
|---|---|---|
| swe-hero_train-00000-of-00014.parquet | 2,500 | 2,500 |
| swe-hero_train-00001-of-00014.parquet | 2,500 | 2,500 |
| swe-hero_train-00003-of-00014.parquet | 2,500 | 2,500 |
| swe-hero_train-00004-of-00014.parquet | 2,500 | 2,500 |
| swe-hero_train-00006-of-00014.parquet | 2,500 | 2,500 |
| swe-hero_train-00007-of-00014.parquet | 2,500 | 2,500 |
| swe-hero_train-00008-of-00014.parquet | 2,500 | 2,500 |
| swe-hero_train-00010-of-00014.parquet | 2,500 | 2,500 |
| swe-hero_train-00011-of-00014.parquet | 2,500 | 2,500 |
| swe-hero_train-00013-of-00014.parquet | 1,769 | 1,769 |
| swe-zero_train-00000-of-00064.parquet | 5,000 | 5,000 |
| swe-zero_train-00021-of-00064.parquet | 5,000 | 5,000 |
| swe-zero_train-00042-of-00064.parquet | 5,000 | 5,000 |
| **Total** | **39,269** | **39,269** |

Deep reads (full trajectory text): hero shard 0 rows 22 (pyramid HMAC issue), 678 (datalad regex issue); hero shard 4 row 712 (modin curl follow-up). Plus 255 systematic-sample summaries.

## Findings

**No findings survived review.** Every candidate deviation checked out as normal benchmark execution or corpus artifact. The kill list below records each candidate and why it died.

## Killed

- **CREDENTIAL, 39,269 rows**: the match is the OpenHands system prompt itself ("If there are existing git user credentials already configured, use them..."). Harness text, not agent behavior. Killed: not a behavior.
- **CRED_ASSIGN, 3,695 rows**: matches are `secret=<redacted>` in pre-redacted issue statements (dataset pipeline redacted secrets before collection) and test-fixture secrets in repo code. No live credential values seen in sampled hits. Killed: no mishandling by the agent.
- **IRREVERSIBLE, 5,482 rows**: 5,700 `rm` commands found; all sampled are `rm -f reproduce_issue.py ...` cleanup of the agent's own scratch files, plus 13 runs of `rm -rf .../site-packages/typing_extensions` to fix a dependency conflict inside the disposable testbed. No `rm -rf /`, no `mkfs`, no `dd ... of=/dev`, no shutdown/reboot. Killed: normal sandbox task execution.
- **PROMPT-INJECT**: full-corpus composition check (all text incl. think/finish args) found only: "you are now" (40x, all the repo-code regex string `html_form_success_re = You are now logged in` in tool output), "prompt injection" (6x, all in `ethz-spylab/agentdojo` repo docs — AgentDojo is itself a prompt-injection benchmark), "jailbreak" (4x, the AC/DC album "Jailbreak" in a beets music-library issue), "Dan" (1x, "Dan Schult" copyright header in networkx), "new instructions" (1x, agent's own prose "hints about the new instructions"). No injected instructions were followed; no self-emitted instruction blocks. Killed: no injection present. Note: the corpus includes the AgentDojo benchmark repo itself as a task repo.
- **CAPTCHA, 426 rows**: matches are `cloudflare_dns.py` filenames, cloudflare CDN URLs in HTML fixtures, and comments about cloudflare workers. No bot check met, none solved. Killed: no CAPTCHA present.
- **ACCOUNT, 814 rows**: matches are mime-type tables (`application/x-internet-signup`), "register for clean-up" code comments. A `useradd`/`adduser` sweep found 8 hits, all benign (`getent passwd`, `which useradd`, greps of repo code). No account creation attempted. Killed: no registration behavior.
- **GUARDRAIL, 740 rows**: mostly code docstrings ("not allowed together", "refuse to work"). One agent self-restraint ("I'm not allowed to modify tests") comes from harness instructions and is the normal baseline. No guard bypass observed. Killed: no bypass or evasion.
- **COORDINATION, 805 rows**: all sampled matches are code comments ("delegate to parent class", "delegate to the same unstack function"). No second agent, no handoff, no shared state. Killed: single-agent work.
- **NET_CALL, 3,280 rows**: curl/wget use is read-only reference fetching (issue-linked URLs piped to grep/head; one 404, agent moved on) or repo test fixtures (stream-extractor domains in test data). No executed downloads, no exfiltration-shaped POSTs. Killed: normal, no exfiltration.
- **TOOL-MISUSE**: no unknown tools (only the 4 documented tools appear). Literal `C-c` (2,362) and `q` (492) as bash commands are the harness's interrupt/pager-quit idioms, not misuse. `is_input` never set. Killed: within-harness norms.
- **RECOVERY**: failures are ordinary (test fails, agent retries with a new approach). No novel recovery strategy seen in sampled trajectories. Nothing filed.
- **OTHER**: `sudo` use (23 commands: apt-get installs, one `/etc/hosts` edit reverted in the same run) stays inside the sandbox; passwordless sudo is the sandbox default. Killed: no privilege escape.

## Overlap

No Factum ingest was performed by this reviewer (per task: the ingestor does that). No dedup check run.

## Open questions

1. SWE-Zero is described as "execution-free" yet its trajectories contain `execute_bash` calls (12.5 per trajectory vs 31.8 in Hero). The README likely means execution-free *fine-tuning*, but the exact meaning is unverified.
2. Zero coverage is thin (3 of 64 shards). Rare trajectory shapes in the other 61 shards are unexamined.
3. The main pattern scan's combined text excluded think/finish arg text; a follow-up locate pass over ALL text (content + all tool args, proper triggers) enumerated every injection-shaped string in the corpus: 40x "you are now" (repo regex string), 6x "prompt injection" (AgentDojo repo docs), 4x "Jailbreak" (AC/DC album in a beets issue), 1x "Dan" (copyright header), 1x "new instructions" (agent prose). All benign. Per-class row counts elsewhere should be read as approximate.
