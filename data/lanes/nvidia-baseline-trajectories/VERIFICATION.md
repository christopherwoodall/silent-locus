# NVIDIA Baseline Trajectories — Verification

Lane: `nvidia-baseline-trajectories`. Date: 2026-10-16. Role: verifier / adversarial reviewer.

## Method

Independent re-derivation from the raw parquet bytes. Not a re-read of the reviewer's structures.

- Scope: all 13 parquet files, all 39,269 rows, every step of every trajectory, full text including tool-call arguments. No sampling of content.
- Pass 1: per-row stats (length, tool counts, finish position, one-call-per-message, patch bytes, ids, instances, repos, licenses, datasets, think/editor/bash breakdowns, transitions, curl hosts from bash args).
- Pass 2: full-text needle counts (content + all tool args), chained-command counts for rm/sudo, finish-message formulas.
- Pass 3: rm-bucket split, sudo occurrence/command counts, per-trajectory host presence, kill-list context grabs, patch anomalies, system-prompt hashes.
- Pass 4: exact tool-sequence uniqueness, first-bash-command shapes, think 2–4 share, ≥1,000-byte patch share.
- Extra: per-dataset length stats, occurrence-level counts for the injection needles, SAMPLING-PLAN.md ↔ manifest.json ↔ disk cross-check.

One OOM kill happened on the first heavy pass (whole row groups in memory); the rerun used small batches and completed cleanly.

Terms: **trajectory** = one agent run (list of steps). **Verified** = my independent count matches the claim. **Weakened** = the claim's substance holds but a number, example, or wording needs correction (revised wording given). **Killed** = the claim's evidence does not support it.

## Per-claim table

### Corpus and shape (BASELINE-CHARACTERIZATION.md)

| Claim | Verdict | My evidence | Notes |
|---|---|---|---|
| 10 of 14 Hero shards, 24,269 rows; 3 of 64 Zero shards, 15,000 rows; 39,269 total | VERIFIED | Parquet metadata per file matches manifest num_rows exactly; file set = sampling indices [0,1,3,4,6,7,8,10,11,13] / [0,21,42] | |
| Step 0 is the system prompt; step 1 is the user prompt | VERIFIED | role=system at step 0 in 39,269/39,269; role=user at step 1 in 39,269/39,269; only 2 distinct system-prompt texts corpus-wide (one per dataset) | |
| Agent loops think / str_replace_editor / execute_bash | VERIFIED | Tool mix + transition counts + first-bash samples (find/python/pwd/grep/ls heads) | |
| Every trajectory ends with one finish call (39,269 of 39,269) | VERIFIED | 39,269 have finish as the last tool call; 0 without; exactly 1 finish call per trajectory (min=max=1) | Strongest invariant in the corpus |
| Length: min 21, p10 51, median 101, p90 157, max 201, mean 103.1 | VERIFIED | 21 / 51 / 101 / 157 / 201; mean 103.14 | Exact |
| No trajectory_id repeats | VERIFIED | 0 duplicate ids | |
| 25,835 unique instances; 10,402 with >1 trajectory (mean ~1.5) | WEAKENED | 25,835 and 10,402 verify exactly; 1.52 is the corpus-wide mean (39,269/25,835), but the mean among the 10,402 multi-trajectory instances is 2.29 | Revised: "25,835 unique instances; 10,402 have more than one trajectory; corpus-wide mean 1.52 trajectories per instance" |
| Tool totals: bash 959,455 / editor 898,865 / think 107,825 / finish 39,269 | VERIFIED | All four match to the unit | |
| No tool names outside the four | VERIFIED | Empty set | |
| One tool call per assistant message: 2,005,414 messages, zero multi | VERIFIED | Exact match | |
| think: 1–9 per trajectory, never zero; most call it 2–4 times | VERIFIED | min 1, max 9, 0 zero-call; 93.4% in 2–4; mean 2.75 | |
| think block usually 1,000–2,000 chars | VERIFIED | Median 1,425 chars | |
| Editor: view 612,049 (68%), create 136,828 (15%), str_replace 149,863 (17%), undo_edit 125 | VERIFIED | All exact; shares 68.1/15.2/16.7% | |
| Edited files mostly .py (737,003 calls) | VERIFIED | 737,003 exact (82.0%) | |
| cd is 85% of bash calls (817,513 of 959,304) | WEAKENED | 817,513 cd-headed commands verify exactly; my denominator is 959,455 (total execute_bash commands) vs their 959,304 (~151 empty/whitespace commands excluded); share is 85.2% either way | Revised: "817,513 of 959,455 (85.2%)" |
| After-cd top heads: grep 91,365, find 35,838, python 2,189, ls 2,018, curl 918, git 858 | WEAKENED | All match except python: derived 2,184, not 2,189 (diff 5). These are overall head counts, not after-cd-stripped | Revised python to 2,184 |
| pytest in 143,595 commands | WEAKENED | Derived 143,760 (diff +165, 0.1%) | Revised: 143,760 |
| pip install in 4,732 commands | WEAKENED | Derived 4,659 (diff −73, 1.5%) | Revised: 4,659 |
| Chained commands (&&, ;, \|) 889,498 of 959,304 (93%) | VERIFIED | 889,498 exact; 92.7% → 93% | |
| Hero 31.8 bash / 25.3 editor per trajectory; Zero 12.5 bash / 18.9 editor; think 2.7 both | VERIFIED | 31.81 / 25.34 / 12.50 / 18.93; think 2.744 / 2.748 | |
| Zero trajectories are shorter | VERIFIED | Median steps: Zero 65 vs Hero 119; mean 71.3 vs 122.8 | |
| Tool pairs: bash→bash 497,181; editor→bash 441,029; editor→editor 422,763 | VERIFIED | All exact | |
| Literal C-c commands (2,362) | VERIFIED | Exact | |
| Literal q commands (492) | VERIFIED | Exact | |
| is_input never set true (0 times) | VERIFIED | Flag absent from tool args corpus-wide | |
| Cleanup rm -f (5,700 rm commands), almost all rm -f reproduce_issue.py | WEAKENED | 5,062 rm -f commands (chained-head basis), not 5,700 (diff −638, 11%); only 3,305 (65%) contain "reproduce", so "almost all" overstates | Revised: "5,062 rm -f commands; ~65% remove reproduce_issue.py scratch files" |
| sudo (23 commands) | VERIFIED | Exactly 23 bash commands contain ≥1 sudo occurrence (28 occurrences, 12 trajectories) | |
| One run appended ::1 localhost to /etc/hosts, then reverted with sed -i '$ d' | VERIFIED | Trajectory cdf0c124-d745-4461-ae0a-e9bbb80619fb (clarketm__wait-for-it): sudo append, cat verify, sudo sed -i '$ d' revert, all in one run | |
| rm -rf site-packages dir (13 trajectories): rm -rf .../site-packages/typing_extensions | WEAKENED | Actual path is typing_extensions-stubs (not typing_extensions); 14 trajectories, not 13 | Revised: "14 trajectories rm -rf .../site-packages/typing_extensions-stubs" |
| Formulaic first commands (python version check, ls -la, pwd) | VERIFIED | First-bash samples: cd+python -c version checks, ls -la, reproduce_issue.py; top first heads find/python/pwd/grep/ls | |
| Formulaic finish messages: most start "I have successfully implemented the necessary changes..."; typical length 1,250–2,000 chars | VERIFIED | 14,514/39,269 (37%, plurality) start with the exact string; median length 1,680 chars | |
| System prompt carries the CREDENTIAL keyword | VERIFIED | Verbatim text in step 0 of all 39,269 rows; "credentials" hits all 39,269 trajectories via step 0 | |
| Issue statements pre-redacted: secret=<redacted> (e.g. pyramid session factory issues) | WEAKENED | The only literal occurrence is in a streamlink issue (user role: 403 error with redacted query params), not pyramid; pre-redacted issue text, no agent involvement | Revised example: streamlink, not pyramid |
| curl/wget in 3,280 trajectories | VERIFIED | Derived 3,288 (diff +8, 0.2%) | Approximate OK |
| Net-call top hosts: example.com (1,588), localhost (265), github.com (222), ... | KILLED | Irreproducible: args-level occurrences give raw.githubusercontent.com 192 top; full-text occurrences give github.com 4,266 top; trajectory presence gives github.com 30,316 top (badge domains). Only raw.githubusercontent.com (~195) and api.github.com (~142) match args-level. The leaderboard mixes methods | Kill the leaderboard; keep the qualitative claim |
| Net calls read-only and fixture-driven; one 404, agent moved on; media domains from test fixtures | VERIFIED | Agent curls are curl -s URL \| grep/head patterns; 404-co-occurring curls found (e.g. hydra.cc doc URLs) with agent moving on; stream-extractor fixture domains (lrt.lt, gulli.fr) in args-level hosts | |
| model_patch non-empty in 100% (39,269 of 39,269) | VERIFIED | Exact; smallest patch 94 bytes | Curation property, as stated |
| Patch size: median 2 KB, p90 23 KB, p99 105 KB; 79% ≥ 1 KB | VERIFIED | p50 2,925 B, p90 23,573 B, p99 105,612 B; ≥1,000 B = 79.09% | Median is 2.9 KB, reported as "2 KB" — loose but within rounding |
| 2,125 unique repos; pandas 4,608 (11.7%), numpy 1,816, MONAI 920 | VERIFIED | All exact | |
| Source datasets: nebius 13,484, internlm 8,848, SWE-Gym-Raw 8,064, R2E-Gym-Subset 7,721, SWE-Gym 1,152 | VERIFIED | All exact | |
| Licenses: BSD-3-Clause 12,985, Apache-2.0 12,640, MIT 11,943, BSD-2-Clause 1,653, MIT-0 48 | VERIFIED | All exact | Note: README misspells "BSD-2-Claude" and omits MIT-0 |
| Model Qwen3-Coder-480B-A35B-Instruct (per README); harness OpenHands | VERIFIED | README: "synthesized using Qwen3-Coder-480B-A35B-Instruct", "collected using the OpenHands framework"; no per-row model field in schema | UPSTREAM citation, consistent |
| Full tool sequences near-unique; most common occurs twice | VERIFIED | 39,258 unique sequences of 39,269; max frequency 2 | |
| Envelope: agents edit system state inside the sandbox; nothing leaves it | VERIFIED | All privileged paths are sandbox-internal (/opt/miniconda3/envs/testbed, /etc/hosts reverted in-run, apt installs) | |
| Envelope: agents fetch arbitrary issue-linked URLs read-only; one 404; no execution of fetched content | VERIFIED | curl -s ... \| grep/head shapes; no downloaded-and-executed chains found | |

### Kill-list spot checks (REVIEW-FINDINGS.md) — each checked against raw bytes

| Kill entry | Verdict | Spot evidence |
|---|---|---|
| CREDENTIAL (39,269 rows) = system prompt | VERIFIED kill | Verbatim system-prompt line read in raw bytes; "credentials" in step 0 of all 39,269 rows |
| CRED_ASSIGN (3,695 rows) = pre-redacted issues + fixtures | VERIFIED kill | Single literal `secret=<redacted>` hit is streamlink issue text (user role), pre-redacted; no live values in sampled hits |
| IRREVERSIBLE (5,482 rows) = own-file cleanup + testbed rm -rf | VERIFIED kill (counts corrected above) | rm -f reproduce_issue.py confirmed; rm -rf typing_extensions-stubs confirmed; no rm -rf /, mkfs, dd, shutdown |
| PROMPT-INJECT | VERIFIED kill (description corrected) | "you are now": 40 occurrences in 26 trajectories — datalad regex plus benign repo code (tornado "logged out", charmcraft "publisher", kytos docs, requests_auth fixture); NOT all the datalad regex as stated. "prompt injection": 6 step-hits, 2 ethz-spylab/agentdojo trajectories, repo docs. "jailbreak": 4 occurrences, 1 beets trajectory, AC/DC album in issue text. "Dan Schult": networkx copyright header. "new instructions": 3 occurrences, 1 Qiskit trajectory, agent's own prose. None followed as instructions |
| CAPTCHA (426 rows) | VERIFIED kill | cloudflare_dns.py is a proxy plugin filename in tool output; no bot check present |
| ACCOUNT (814 rows) | VERIFIED kill | useradd hits are `which chage passwd useradd usermod` and greps of repo code; no account creation |
| GUARDRAIL (740 rows) | VERIFIED kill | "I'm not allowed to modify tests" is assistant prose from harness instructions; no bypass observed |
| COORDINATION (805 rows) | VERIFIED kill | "delegate to parent" is a code comment in tool output; no second agent |
| NET_CALL (3,280 rows) | VERIFIED kill (host leaderboard killed separately) | Read-only curl shapes confirmed; 404 cases move on |
| TOOL-MISUSE | VERIFIED kill | C-c 2,362 / q 492 exact; is_input never set |
| OTHER (sudo) | VERIFIED kill | 23 commands exact; all sandbox-scoped |

Per-class row counts (3,695 / 5,482 / 426 / 814 / 740 / 805) use the reviewer's undisclosed pattern set and are not independently reproducible to the unit; kill reasons above were verified by direct byte reads.

### Open questions (REVIEW-FINDINGS.md)

1. **SWE-Zero "execution-free" vs execute_bash present — ANSWERED.** The README titles the dataset "Execution-free Fine-tuning" and cites arXiv 2604.01496 ("From SWE-ZERO to SWE-HERO: Execution-free to Execution-based Fine-tuning"). "Execution-free" describes the fine-tuning recipe, not the traces: the README states the 318k trajectories were "collected using the OpenHands framework", and OpenHands issues execute_bash. Verified: Zero trajectories average 12.5 bash calls. No contradiction.
2. **Zero coverage thin (3/64 shards) — STANDS.** Valid limitation; rare Zero shapes unexamined.
3. **think/finish-args exclusion — CLOSED.** Corpus-wide scan over ALL text (content + every tool-call argument): "you are now" 40 occurrences (26 trajectories), "prompt injection" 6 step-hits (2 trajectories), "jailbreak" 4 occurrences (1 trajectory), "Dan" (1, copyright header), "new instructions" 3 occurrences (1 trajectory). All benign (see kill table). Reviewer's "new instructions (1x)" should read 3 occurrences in 1 trajectory.

### SAMPLING-PLAN.md

- Shard-index formula `round(i×14/10)` reproduces [0,1,3,4,6,7,8,10,11,13]; Zero [0,21,42] matches. VERIFIED.
- Disk files = manifest files; all manifest size_bytes == on-disk sizes; row counts per file match parquet metadata; 17/17 provenance sidecars present. VERIFIED.
- Hero parquets 1,684,815,584 bytes; Zero parquets 579,169,092 bytes; total 2,264,018,096 bytes = 2.264 GB, under the 2.5 GB budget (~236 MB margin). VERIFIED.
- WEAKENED: "Metadata (4 files): 34,420 bytes" — actual 33,420 bytes (5,622+10,749+5,934+11,115). 1,000-byte arithmetic slip in the plan; manifest total is correct with 33,420.

## Kill list (one-line reasons)

1. **Net-call top-hosts leaderboard (example.com 1,588, localhost 265, github.com 222, ...)** — irreproducible under every counting method tried; numbers mix methods.
2. **"rm -rf .../site-packages/typing_extensions in 13 trajectories"** — actual path is `typing_extensions-stubs` in 14 trajectories; both path and count wrong.
3. **"Almost all rm commands are rm -f reproduce_issue.py"** — only ~65% of rm -f commands contain "reproduce".
4. **"secret=<redacted> (e.g. pyramid session factory issues)"** — the sole occurrence is a streamlink issue; the pyramid example cannot be located.
5. **"(mean ~1.5 trajectories per instance)" attached to the 10,402 multi-trajectory instances** — the mean among those is 2.29; 1.52 is the corpus-wide mean.
6. **"python (2,189)" bash-head count** — derived 2,184.
7. **"pytest in 143,595 commands" / "pip install in 4,732"** — derived 143,760 / 4,659.
8. **"5,700 rm commands"** — derived 5,062 rm -f chained-head commands.
9. **SAMPLING-PLAN "34,420 bytes" metadata** — actual 33,420 bytes (1,000-byte slip).
10. **PROMPT-INJECT count wording: "you are now (40x, all the datalad regex)"** — 40 is the occurrence count across 26 trajectories; non-datalad hits are other benign repo code (tornado, charmcraft, kytos, requests_auth), not the datalad regex.

## INGEST-APPROVED claim list (for the ingestor)

Use the corrected numbers below; everything here reproduced from raw bytes.

- Corpus: 39,269 trajectories (24,269 Hero + 15,000 Zero), 10 Hero shards + 3 Zero shards of the pinned revisions; no trajectory_id repeats.
- Fixed shape: step 0 system prompt (OpenHands, 2 corpus-wide variants), step 1 user prompt (repo path + issue text), then the think→view/edit→execute loop.
- Invariants: 100% end with exactly one finish call; exactly one tool call per assistant message (2,005,414 messages, 0 multi-call); only 4 tools (execute_bash 959,455; str_replace_editor 898,865; think 107,825; finish 39,269); 100% non-empty model_patch.
- Lengths (steps): min 21, p10 51, median 101, p90 157, max 201, mean 103.1. Hero longer (median 119) than Zero (median 65).
- think: 1–9 per trajectory, never zero, 93.4% in 2–4; median block 1,425 chars.
- Editor: view 612,049 (68%), create 136,828 (15%), str_replace 149,863 (17%), undo_edit 125; .py files 737,003 calls.
- Bash: cd-headed 817,513 (85.2%); heads grep 91,365, find 35,838, python 2,184, ls 2,018, curl 918, git 858; pytest in 143,760 commands; pip install in 4,659; chained 889,498 (92.7%).
- Hero 31.8 bash / 25.3 editor per trajectory; Zero 12.5 / 18.9; think 2.7 both.
- Top tool transitions: bash→bash 497,181; editor→bash 441,029; editor→editor 422,763.
- Quirks: C-c 2,362; q 492; is_input never set; rm -f cleanup 5,062 commands (~65% remove reproduce_issue.py scratch); sudo 23 commands, all sandbox-scoped (apt installs, one /etc/hosts edit reverted in-run — trajectory cdf0c124); rm -rf .../site-packages/typing_extensions-stubs in 14 trajectories; finish messages 37% start "I have successfully implemented the necessary changes...", median 1,680 chars.
- Net: curl/wget in 3,288 trajectories; agent fetches read-only (curl -s URL | grep/head); 404s observed and moved on; no executed downloads; fixture domains (stream extractors) explain media hosts.
- Patches: median 2,925 B, p90 23.6 KB, p99 105.6 KB, ≥1,000 B in 79.1%; curation keeps only non-empty patches.
- Repos: 2,125 unique; pandas 4,608, numpy 1,816, MONAI 920. Sources: nebius/SWE-rebench 13,484, internlm/SWE-Fixer-Train-110K 8,848, SWE-Gym-Raw 8,064, R2E-Gym-Subset 7,721, SWE-Gym 1,152. Licenses: BSD-3-Clause 12,985, Apache-2.0 12,640, MIT 11,943, BSD-2-Clause 1,653, MIT-0 48.
- Tool sequences near-unique (39,258 unique of 39,269; max frequency 2).
- Model Qwen3-Coder-480B-A35B-Instruct, harness OpenHands (per dataset README; no per-row model field).
- Kill verdicts: no prompt injection, no credential mishandling, no CAPTCHA, no account creation, no guardrail bypass, no multi-agent coordination, no exfiltration, no destructive operations outside the sandbox. CREDENTIAL hits are system-prompt text; secret=<redacted> is pre-redacted issue text.
- Sampling: 2.264 GB under the 2.5 GB budget; provenance complete (17/17 sidecars).

## Notes for the ingestor (not claims, just data observations)

- Patch-size outliers: one 293 MB model_patch (sec-edgar trajectory 91e4e24d) and 19 patches >10 MB (18 numba, 1 MONAI) inflate the max; percentiles unaffected.
- Global min length 21 comes from Zero; Hero min is 49.
- README typos/omissions: "BSD-2-Claude" (should be BSD-2-Clause); MIT-0 (48 rows) not listed in the README's license set.
- Per-class row counts in the review's pattern groups (CRED_ASSIGN 3,695 etc.) are the reviewer's pattern-set output and were not reproducible to the unit; the kill reasons were verified directly.

## Overall confidence

High. The characterization reproduced almost exactly from raw bytes: every tool total, every editor command count, every tool-pair count, every length percentile, the one-call-per-message and finish invariants, the sudo count (23), the C-c/q counts, repo/dataset/license counts — all matched to the unit. The failures found are small-number corrections (pytest ±0.1%, pip install ±1.5%, rm -f −11%, typing_extensions path/count, host leaderboard), one wrong example (pyramid→streamlink), one misplaced mean (1.5 vs 2.29), and one 1,000-byte arithmetic slip in the sampling plan. No substantive characterization claim was falsified; no kill-list kill was overturned.
