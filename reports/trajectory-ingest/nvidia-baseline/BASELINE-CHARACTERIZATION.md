# NVIDIA Baseline Trajectories — Baseline Characterization

Lane: `nvidia-baseline-trajectories`. Date: 2026-10-16. Reviewer: behavior reviewer (baseline fleet).

## Terms

- **Trajectory**: one agent run. It is a list of steps. Each step has a role: `system`, `user`, `assistant`, or `tool`.
- **Tool call**: a function call the agent makes. Four tools exist: `execute_bash`, `think`, `finish`, `str_replace_editor`.
- **Model patch**: the final code change the agent made, in diff format. An empty patch means the agent changed no code.
- **Shard**: one parquet file. SWE-Hero has 14 shards; SWE-Zero has 64 shards.

## Sources

- `nvidia/SWE-Hero-openhands-trajectories`, revision `150bc119e52c647216fce285fd801f16b6fd745b`. 10 of 14 shards read, all rows. 24,269 rows.
- `nvidia/SWE-Zero-openhands-trajectories`, revision `7b3cd106d00f60918e722d33a1d74bc67072a7ea`. 3 of 64 shards read, all rows. 15,000 rows.
- Total rows examined: 39,269. Full text scanned for all rows. No sampling of content.

Both sets are synthetic instruction-tuning traces. The model is Qwen3-Coder-480B-A35B-Instruct. The harness is OpenHands. Each task is a SWE-Bench-style GitHub issue. Provenance per file is in `raw/*.PROVENANCE.txt`.

## Baseline shape

A trajectory is one issue-fix run. The shape is fixed:

1. Step 0 is the system prompt (OpenHands agent instructions).
2. Step 1 is the user prompt: an uploaded repo path plus the issue text.
3. The agent then loops: `think` (plan), `str_replace_editor` (read or write code), `execute_bash` (run commands, mostly tests).
4. Every trajectory ends with one `finish` call. No trajectory lacks it (39,269 of 39,269).

Length (steps): min 21, 10th pct 51, median 101, 90th pct 157, max 201. Mean 103.1.

No trajectory_id repeats. 25,835 unique instances; 10,402 instances have more than one trajectory (mean ~1.5 trajectories per instance).

## Tool use

Counts per trajectory, whole corpus:

| Tool | Total calls | Per trajectory |
|---|---|---|
| `execute_bash` | 959,455 | 24.4 |
| `str_replace_editor` | 898,865 | 22.9 |
| `think` | 107,825 | 2.7 |
| `finish` | 39,269 | 1.0 |

No tool names outside these four appear. Strictly one tool call per assistant message: 2,005,414 assistant tool messages, zero with more than one call. This is a hard invariant of the corpus.

`think` use: every trajectory calls it 1 to 9 times (never zero). Most trajectories call it 2 to 4 times. A `think` block is usually 1,000 to 2,000 chars.

`str_replace_editor` commands: `view` 68% (612,049), `create` 15% (136,828), `str_replace` 17% (149,863), `undo_edit` 125. Edited files are mostly `.py` (737,003 calls).

`execute_bash` command heads: `cd` is 85% of all bash calls (817,513 of 959,304). The agent chains `cd <repo> && <command>` on almost every call. After `cd`, the top heads are `grep` (91,365), `find` (35,838), `python` (2,189), `ls` (2,018), `curl` (918), `git` (858). `pytest` appears in 143,595 commands (often inside chained commands). `pip install` appears in 4,732 commands. Chained commands (`&&`, `;`, `|`) are 889,498 of 959,304 (93%).

Hero vs Zero: Hero runs average 31.8 bash calls and 25.3 editor calls per trajectory. Zero runs average 12.5 bash calls and 18.9 editor calls. Zero trajectories are shorter and less execution-heavy. `think` use is the same (2.7 per trajectory).

Common tool pairs: `execute_bash -> execute_bash` (497,181), `str_replace_editor -> execute_bash` (441,029), `str_replace_editor -> str_replace_editor` (422,763). The loop is: look at code, run a command, look again.

## Baseline quirks

These are normal in this corpus. They are not findings.

- **Literal `C-c` commands (2,362).** The agent sends the string `C-c` as a bash command to stop a hung process. It is the OpenHands interrupt idiom. The `is_input` flag is never set true (0 times).
- **Literal `q` commands (492).** The agent types `q` to quit a pager (`less`, `man`).
- **Cleanup `rm -f` (5,700 rm commands).** Almost all are `rm -f reproduce_issue.py ...`: the agent deletes its own scratch reproduction scripts before finishing. This is the standard end-of-run shape.
- **`sudo` (23 commands).** The sandbox allows passwordless sudo. Observed: `apt-get install -y ninja-build`, `apt-get install -y autoconf automake libtool`, and one run that appended `::1 localhost` to `/etc/hosts` to reproduce an issue, then reverted it with `sed -i '$ d'`. Agents can touch system config, but stay inside the sandbox and revert.
- **`rm -rf` of a site-packages dir (13 trajectories).** `rm -rf /opt/miniconda3/envs/testbed/lib/python3.9/site-packages/typing_extensions` — the agent removed a package dir to fix a dependency conflict. This is the most aggressive file operation seen. It stays inside the disposable testbed.
- **Formulaic first commands.** Runs open with `cd <repo> && python -c "import <pkg>; print(version)"`, `ls -la`, or `pwd`.
- **Formulaic finish messages.** Most start "I have successfully implemented the necessary changes...". Typical length 1,250 to 2,000 chars.
- **System prompt carries the CREDENTIAL keyword.** The OpenHands system prompt says "If there are existing git user credentials already configured, use them...". This matches every credential scan. It is harness text, not agent behavior.
- **Issue statements are pre-redacted.** Issue text contains `secret=<redacted>` (e.g. pyramid session factory issues). The dataset pipeline redacted secrets before the agent ever saw them.
- **Net calls are read-only and fixture-driven.** `curl`/`wget` appear in 3,280 trajectories. Top hosts: `example.com` (1,588), `localhost` (265), `github.com` (222), `example.org` (202), `raw.githubusercontent.com` (195), `api.github.com` (142), `test.com` (112). The media/TV domains (`tf1.fr`, `gulli.fr`, `lrt.lt`, `nos.nl`) come from repo test fixtures (stream extractors), not agent browsing. Agents do fetch issue-linked URLs (`curl -s <url> | grep ...`) for reference; observed fetches were read-only, one returned 404 and the agent moved on. No remote code was executed.

## Success and failure shapes

Success proxy: `model_patch` is non-empty. Result: 100% of trajectories (39,269 of 39,269) carry a non-empty patch. This is a curation property: the SFT set keeps only runs that produced a patch. There is no failed-run shape in this corpus.

Patch size: median 2 KB, 90th pct 23 KB, 99th pct 105 KB. 79% are at least 1 KB.

Repos: 2,125 unique. Heavy skew: `pandas-dev/pandas` 4,608 (11.7%), `numpy/numpy` 1,816, `Project-MONAI/MONAI` 920. Source datasets: `nebius/SWE-rebench` 13,484, `internlm/SWE-Fixer-Train-110K` 8,848, `SWE-Gym/SWE-Gym-Raw` 8,064, `R2E-Gym/R2E-Gym-Subset` 7,721, `SWE-Gym/SWE-Gym` 1,152. Licenses: BSD-3-Clause 12,985, Apache-2.0 12,640, MIT 11,943, BSD-2-Clause 1,653, MIT-0 48.

## Model and harness

- Model: Qwen3-Coder-480B-A35B-Instruct (per dataset README; no per-row model field in the data).
- Harness: OpenHands (system prompt names it; tools match the OpenHands tool set).
- Full tool sequences are near-unique: the most common exact sequence occurs twice. Behavior varies run to run, but the loop above holds.

## Deviations

No taxonomy-class deviation survived review. The kill list is in REVIEW-FINDINGS.md. Two envelope notes (not findings):

1. Agents edit system state inside the sandbox (`/etc/hosts`, `apt-get install`, site-packages removal). Nothing leaves the sandbox.
2. Agents fetch arbitrary URLs named in issues (read-only). One 404 observed; no execution of fetched content.
