# WebArena Infinity: verifiers certify runs the trajectory record contradicts

**Status:** DRAFT — do not submit (Transluce filing freeze in force). Written 2026-10-17.

## 1. Summary

Three qwen/gemini trajectories carry `passed=true` while their own records show the agent failed, thrashed, or could not confirm success. A separate class of six gemini trajectories carries `passed=true` while the final step judge says the run "insufficient" to confirm the result. The success labels in this dataset are not self-consistent. Counting unit: 3+6 findings in this family, of 21 verified findings total.

Key terms: a **trajectory** is one recorded agent run (a `history.json` plus a `result.json`). The **verifier** is the benchmark's programmatic pass/fail check. The **judge** is the LLM scorer that evaluates each step's result.

## 2. Corpus and counting unit

- Corpus: `webarena-x/webarena-infinity-trajectories`, revision `73cf7f57a6ff61c95722a23bffdd9c1de4069bfe`, license mit.
- Raw bytes downloaded 2026-10-17 to `data/lanes/webarena-infinity-trajectories/raw/` (2,195 history.json: gemini 844, kimi 643, qwen 708; the HF listing shows 2,329 — gemini is short 134 locally).
- Review coverage: Reviewer A read all 844 gemini trajectories via per-step digest; Reviewer B ran a keyword sweep over all 1,351 kimi+qwen trajectories plus full reads of flagged trajectories.
- Counting unit: n = 3 findings (RB-003, RB-004) of outcome contradiction plus 6 findings (A-F010) of judge/verifier disagreement; each counted once. n does NOT count the 124 bundled-done steps (a separate writeup).

## 3. What happened

**RB-003 (qwen, superhuman-general/task_m13):** the agent ran 50 steps, hit the step cap with `is_done=false`, and never recognized completion. Its thoughts looped: 18 times "Click on the circular button in the top-right corner of the interface..." and 8 times "Click on the 'K' icon located in the top-right corner...". The verifier passed it anyway: "Auto label Shipping Update is disabled." The label got disabled somewhere in the thrash; the agent never knew.

**RB-004 (qwen, figma-slides/task_e19):** at step 46 the agent terminated with failure status: "Terminate the task with failure status because the Thank You slide cannot be located in the presentation." The verifier passed it: "Slide numbers disabled on Thank You slide". Earlier, steps 9–44 include 7 repeated 'Show number' toggle attempts — off-target UI changes the success label also covers.

**A-F010 (gemini, 6 trajectories):** in gmail-accounts-and-contacts/task_e19, handshake-career-exploration/task_h6, paypal-my-wallet/task_e1, paypal-my-wallet/task_e15, xero-invoicing/task_e10, and xero-invoicing/task_h5, `result.json` says passed=true with a success-confirming verifier message, but the final step's `result[0].judgement` carries verdict=False with reasoning "insufficient to verify/confirm/complete". Example: in task_h6 the judge noted the agent clicked Follow 3 times but reported 2 — while the verifier passed it. (A seventh candidate, gmail-accounts-and-contacts/task_e4, was rejected: its final judgement is verdict=True; the word "insufficient" there refers only to element finding, not the outcome.)

## 4. Evidence

- **RB-003**, trajectory `qwen/superhuman-general/task_m13`, steps 0–49. Quote: "50 steps, is_done=false, steps=50, passed=true, verifier='Auto label Shipping Update is disabled.'" Thought-repeat counts verified in history.json. File: `raw/qwen/superhuman-general/task_m13/history.json`, sha256 `a9d3d822…`.
- **RB-004**, trajectory `qwen/figma-slides/task_e19`, steps 9–46. Quote: "Step 46 thought: 'Action: Terminate the task with failure status because the Thank You slide cannot be located in the presentation.' + terminate/status=fail action; result.json: passed=true, verifier='Slide numbers disabled on Thank You slide'". File: `raw/qwen/figma-slides/task_e19/history.json`, sha256 `d997c613…`.
- **A-F010**, 6 trajectories (listed above), final step of each. Quote: "6 trajectories where result.json passed=true and verifier_message confirms success, but the final step's result[0].judgement has verdict=False with 'insufficient to verify/confirm/complete' reasoning". Example bytes: task_h6 judge record notes 3 Follow clicks reported as 2, verifier passed. Files under `raw/gemini/<site>/<task_id>/history.json` + `result.json`; HF blob path pattern `data/gemini/<site>/<task_id>/`.

## 5. Novelty

This is a new byte-verified instance of an old problem, not a first discovery of the mechanism. Evaluator/eval-harness disagreement is a known benchmark-design failure class. The internal-corpus overlap check (verifier ran it; zero overlap with prior findings) confirms these instances are new to the hunt corpus. What this adds: three distinct disagreement shapes in one corpus — success-by-accident (RB-003), self-declared failure marked pass (RB-004), and step-judge vs programmatic-verifier contradiction (A-F010).

## 6. Why it matters

Anyone training on or benchmarking against the "successful" subset of this corpus will ingest runs where the agent was confused, thrashing, or explicitly failed. RB-003 shows a passed trajectory can hide total agent confusion; RB-004 shows success labels can mask off-target UI changes (7 stray toggle clicks) and an agent's own failure declaration. Success labels that do not survive a read of the trajectory are a data-quality hazard for reward modeling, SFT filtering, and capability claims alike.

## 7. Uncertainties

- Could RB-003's pass be correct-by-luck and the confusion harmless? Ruled out as a data-quality reading: regardless of the final state, the trajectory teaches the wrong behavior (thrashing until the cap).
- Could the A-F010 judge records be the faulty side (an over-strict judge) rather than the verifier? Cannot be ruled out from the bytes alone. The claim is disagreement, not which side is right.
- Single corpus, single dataset revision. Prevalence across other WebArena-derived corpora is unknown — open gap.
- The killed finding A-F008 (a single bundled done-step in figma-text-and-typography/task_e1) was subsumed by the bundled-done recount (A-F009) and is not double-counted here.

## 8. Impact

- Harm: **No/negligible harm** (sandbox-contained; no live systems touched, no money moved, no credentials). Cyberattack: None.
- Near-miss translation: a verifier that certifies thrashing and self-declared failures is a verifier that will also certify real harm it never looked at. In a deployment with the same verification shape, the "passed" label would give false assurance about runs that contain 50-step confusion loops and unacknowledged off-target UI changes.
- Disposition: do not replay; read-only analysis. Fix owner: `task_author`/`environment` (the verification design), not the model.
