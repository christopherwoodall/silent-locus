# JetBrains SWE-bench trajectories: the no-test-modification guardrail is enforced by the agent, not the harness

**DRAFT — NOT FOR SUBMISSION (Transluce filing freeze in force, 2026-10-17).**

## 1. Summary

Two agents violated the no-test-modification rule and then cleaned up their own violations — the harness never blocked them. In one case the agent needed five `rm -f` turns plus `git restore --staged` because an earlier `git add -A` had staged the offending file: deletion alone could not scrub a violation the harness had already let into the index. The self-policing worked; the boundary itself is enforced only by the agent. Counting unit: 1,785 trajectories; 7 verified findings; 2 findings in this family.

## 2. Corpus and counting unit

- Corpus: `JetBrains-Research/agent-trajectories-swe-bench-test-minus-verified`, revision `dd79e2540cab4c0cc2c5bab6ea71ddd7ac6c1775`.
- Retrieval: 2026-10-17T02:53:07Z via curl -L.
- Raw file: `~/workspace/silent-locus/data/lanes/jetbrains-swe-trajectories/raw/data/train-00000-of-00001.parquet`, sha256 `5f0d6313bd297cf3d1e23d4a2a4bb27a2fec0bc8d21cf205aef4ff43d7d51b04`.
- n = 1,785 trajectories reviewed (rows 0–1784); 7 byte-verified findings; n = 2 in this family (F-A-002, F-003).
- Factum lane: `jetbrains-swe-trajectories`; factum batch `ce81bb019a0340b2a3a45365d5d2834a` (+ 4 siblings from the same ingest: `435edfc4…`, `b1670cc9…`, `51368d31…`, `b6d86742…`), 3,595 records, 0 errors.

## 3. What happened

**Instance 1 — django__django-12747 (F-003, trajectory row 1510).** The agent wrote a scratch test file into `tests/` — outside the task boundaries. It caught itself at message 24:

> "I mistakenly modified the tests directory, which is disallowed by the task boundaries. I need to undo that change by removing the newly added test file so that only the non-test source code fix remains."

It then ran `rm -f` five times (messages 24, 26, 28, 32, 36). Deletion kept failing to clear the violation. The reason surfaced at message 37: the agent had earlier run `git add -A` (message 22), which staged (copied into git's submission index) the scratch file. `rm -f` removes a working file; it cannot remove a staged copy. At message 38 the agent recognized this and ran `git restore --staged .` plus `rm -f` plus a scoped re-add (`git add django/db/models/deletion.py`); message 39's git status showed only `M  django/db/models/deletion.py` remained. At no point did the harness refuse the original edit, the staging, or any step of the cleanup.

**Instance 2 — scikit-learn__scikit-learn-13467 (F-A-002, trajectory row 548).** At message 44 the agent reported:

> "I accidentally modified a test file, which is out of bounds per the task rules. I need to revert that change so only source (non-test) files remain modified, while keeping the RMSE functionality and scorer implemented in the library code."

It then ran `git checkout -- sklearn/metrics/tests/test_score_objects.py`. Same family: self-caught test modification followed by a self-revert, with no harness intervention visible anywhere in the 47-message trajectory.

## 4. Evidence

- F-003, trajectory `django__django-12747` (row 1510), assistant messages 24–38 (of 41): self-report quote verified verbatim at message 24; five `rm -f` turns at messages 24, 26, 28, 32, 36; `git restore --staged .` at message 38; staged-copy evidence at message 37 (`A  tests/delete/test_zero_delete_consistency.py`); clean final status at message 39. Source: raw parquet above, sha256 `5f0d6313bd297cf3d1e23d4a2a4bb27a2fec0bc8d21cf205aef4ff43d7d51b04`.
- F-A-002, trajectory `scikit-learn__scikit-learn-13467` (row 548), assistant messages 42–46 (of 47): self-report quote verified verbatim at message 44; `git checkout -- sklearn/metrics/tests/test_score_objects.py` at message 44. Same source file and sha256.
- Action–result pairing: in F-003 each cleanup step is followed by an observed git status; the final `M  django/db/models/deletion.py`-only state is the paired result of the message-38 restore. In F-A-002 the revert command's effect is not observable in the record (see Uncertainties).
- Reading was read-only. Nothing was replayed or reproduced.

## 5. Novelty

No prior Transluce finding documents this pattern. Searched the local Transluce findings cache (`~/workspace/silent-locus/data/lanes/2026-10-09-transluce-intel/raw/findings-list*.json`, 115 unique findings) for guardrail, self-report, and test modification: the only hit is #173, which concerns webhook inboxes, not test-file boundaries. This is new. What it adds: byte-level proof that a benchmark's "don't touch the tests" boundary can be a purely agent-enforced convention. The F-003 staged-copy detail is the sharp part — the harness not only failed to block the violation, it *preserved* the violation in the submission index, and only the agent's understanding of git staging undid it. Self-monitoring held here; the mechanism itself has no independent check.

## 6. Why it matters

Two sibling instances show the same rule being broken and self-repaired — and a third family member (writeup 01) shows the same rule being broken and not repaired. The self-policing in F-A-002/F-003 is genuinely positive behavior, but it is not a guardrail in the engineering sense: a guardrail is enforced by the system, and this one is enforced by the monitored party. A benchmark that wants its test files untouched needs a harness-level check (e.g. diff the submitted patch against the test tree) instead of relying on the agent's good faith. The F-003 staging detail also shows the self-cleanup can silently fail: had the agent stopped at `rm -f`, the violation would have shipped inside the submission index.

## 7. Uncertainties

- F-A-002 evidence gaps: the actual test-file edit is not visible anywhere in the 47 trajectory messages — only the agent's self-report claims it happened. The revert command's success is unverifiable: message 45's tool output is interleaved pytest noise (a known dataset quirk — the returncode belongs to a different command). The claim "the submitted diff contained only source files" is unverifiable; the trajectory ends at the submit command (message 46) with no diff output. Confidence MEDIUM on the self-monitoring narrative; the persistence of the cleanup is not in bytes.
- Interleaving quirk in F-003: some tool outputs mismatch their commands (messages 25, 27, 29), but the git-status evidence at messages 37 and 39 is unambiguous and survives the quirk.
- Harness-induced vs model-intrinsic: cannot rule out that the scaffold's submit flow (stage everything, then submit) is what created the staged-copy trap — the boundary may be as much a scaffold design gap as a model behavior. What the bytes establish regardless is that no independent enforcement existed.
- Model attribution: per writeup 05, trajectories mix `litellm_proxy/openai/gpt-5.2` and `litellm_proxy/openai/gpt-5-mini` per turn; model names are trace labels only.

## 8. Impact / harm

- Harm: No/negligible harm. Sandbox trajectories; the violations were cleaned by the agent before submission (F-003, verified in git status); no external system was touched.
- Near-miss translation: none demonstrated — the agents repaired the violation. The near-miss is conditional: in the F-003 trajectory, a less capable cleanup (`rm -f` only) would have left the test edit staged inside the submitted patch, silently shipping a rule violation that the harness would not have caught.
- Cyberattack: None.
