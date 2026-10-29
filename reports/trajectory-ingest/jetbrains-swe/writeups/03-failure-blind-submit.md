# JetBrains SWE-bench trajectories: submitting with three failing tests and no triage of the failures

**DRAFT — NOT FOR SUBMISSION (Transluce filing freeze in force, 2026-10-17).**

## 1. Summary

In `sympy__sympy-16334` the agent watched three pytest failures print, thought only about patch formatting, and submitted two messages later. It never asked whether its change caused the failures or whether they were pre-existing. This is distinguished, in bytes, from 60 "submitted while red" trajectories that the reviewers killed: those agents recorded a judgment that the failures were unrelated or pre-existing; here there is no judgment at all. Counting unit: 1,785 trajectories; 7 verified findings; n = 1 in this family (F-A-003).

## 2. Corpus and counting unit

- Corpus: `JetBrains-Research/agent-trajectories-swe-bench-test-minus-verified`, revision `dd79e2540cab4c0cc2c5bab6ea71ddd7ac6c1775`.
- Retrieval: 2026-10-17T02:53:07Z via curl -L.
- Raw file: `~/workspace/silent-locus/data/lanes/jetbrains-swe-trajectories/raw/data/train-00000-of-00001.parquet`, sha256 `5f0d6313bd297cf3d1e23d4a2a4bb27a2fec0bc8d21cf205aef4ff43d7d51b04`.
- n = 1,785 trajectories reviewed (rows 0–1784); 7 byte-verified findings; n = 1 in this family (F-A-003, trajectory row 157). The killed 60-case batch is named here only as the explicit negative comparison set; it is not counted.
- Factum lane: `jetbrains-swe-trajectories`; factum batch `ce81bb019a0340b2a3a45365d5d2834a` (+ 4 siblings from the same ingest: `435edfc4…`, `b1670cc9…`, `51368d31…`, `b6d86742…`), 3,595 records, 0 errors.

## 3. What happened

At user message 25 the agent received a pytest short summary showing three failures in `test_assumptions.py`:

> "...........................F.....................F........F........      [100%] | FAILED sympy/core/tests/test_assumptions.py::test_neg_symbol_falsenonnegative (+ test_issue_6275, test_issue_7993)"

The failures sit in the assumptions module covering the exact logic the agent changed (`Pow._eval_is_positive`). Between this red output (message 25) and the submit (message 28), no message investigates the failures. The intervening thought (message 26) is only about patch formatting; message 28 says:

> "The change is localized and looks correct in `Pow._eval_is_positive`. Next I'll prepare the final submission by staging all changes and showing the cached diff so it's clear exactly what was modified."

The agent then staged and submitted. It never compared the failures against a pre-change baseline, never ran the failing tests on the unmodified code, never wrote a single line addressing them.

## 4. Evidence

- Trajectory `sympy__sympy-16334` (row 157); step range: user message 25 (red output) → assistant messages 26 and 28 (submit). Quotes verified verbatim (message 28; curly apostrophes preserved); the failure lines corrected to verbatim bytes by the verifier (the reviewer's first-pass quote "E assert None is False" is not in the bytes — only the short-summary FAILED lines are). Source: raw parquet above, sha256 `5f0d6313bd297cf3d1e23d4a2a4bb27a2fec0bc8d21cf205aef4ff43d7d51b04`.
- The negative comparison set: 60 "submitted while last test run red" trajectories, sampled and killed (kill-list B: spot-checked tails showed agents judging remaining failures unrelated/pre-existing). The discriminator is byte-level and explicit: the killed cases contain an agent-written judgment of unrelatedness; F-A-003 contains none.
- Reading was read-only. Nothing was replayed or reproduced.

## 5. Novelty

No prior Transluce finding documents this behavior. Searched the local Transluce findings cache (`~/workspace/silent-locus/data/lanes/2026-10-09-transluce-intel/raw/findings-list*.json`, 115 unique findings) for submit-with-failures, while-red, and submission of failing tests: zero hits. This is new. What it adds: a clean byte-level line between normal SWE triage (an agent judges the red as unrelated and moves on — competent, killed as a finding) and the absence of triage (the agent simply never engages the red). The finding is about the missing judgment step, not about whether the failures were caused by the change. That distinction is the whole point of the 60-case kill comparison: submitters who skip triage are invisible to any review that only checks "did they see the red."

## 6. Why it matters

In real deployment, submitting over failing tests without triage is the mechanism behind broken-main incidents: the developer's own run showed red, and nobody asked why. The benchmark analog matters for eval validity too — if the submitted patch is what gets graded, an un-triaged submit is how regressions survive. The contrast with the killed 60-case batch is the operational lesson: a harness that only logs the last test-run color cannot distinguish careful triage from no triage. Distinguishing them requires the agent's reasoning trace — which this corpus preserves and which the submit step skipped.

## 7. Uncertainties

- Whether the three failures were pre-existing or caused by the change is an OPEN GAP. The finding is about the absence of triage, not causation; do not read it as "the agent broke three tests."
- Non-malicious reading: the agent may have judged the failures pre-existing silently — no internal reasoning on the point appears in bytes, but absence of recorded thought is not proof of absence of thought. The per-turn model mixing (writeup 05) means a turn from the other model may have held unrecorded context; nothing in bytes supports this, but it cannot be ruled out.
- Two of the three failures (`test_issue_6275`, `test_issue_7993`) are named only in the parenthetical; their bodies were not in the trajectory, so no statement is made about their content.
- Model attribution: trajectories mix `litellm_proxy/openai/gpt-5.2` and `litellm_proxy/openai/gpt-5-mini` per turn; model names are trace labels only.

## 8. Impact / harm

- Harm: No/negligible harm. Sandbox trajectory; the submitted patch affected only the benchmark harness.
- Near-miss translation: in a real repo, this exact submit shape — red run, no triage, staged diff, submit — lands a regression in main. The demonstrated gap is a missing verification step, not a malicious act.
- Cyberattack: None.
