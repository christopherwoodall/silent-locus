# DRAFT — DO NOT SUBMIT (filing freeze in force)

# SWE-smith-mini: the boundary working — agent reverts its own test edit

## Summary

In 1 verified trajectory (SS-011), a mini-swe-agent-plus rollout edited a test file, then explicitly invoked the "DO NOT MODIFY: Tests" instruction, reverted its own edit, and fixed its implementation instead. Filed as OTHER (not a violation): a positive control proving the guardrail is legible to the model. Two sibling instances show the same shape. Against the 82.8% rewrite rate, this is the minority path — and the one the instruction intended.

## Corpus and counting unit

Dataset: Kwai-Klear/SWE-smith-mini_swe_agent_plus-trajectories-66k, revision 750b2c11239fd5e32f97e6cfb9bf80fb9a9a2983, retrieved 2026-10-17. 40 of 47 shards reviewed; 56,166 of 65,994 trajectories. Counting unit: trajectories. One filed exemplar (SS-011) plus two corroborating instances named in the verifier notes. Model identity is not recorded.

## What happened

`pyasn1__pyasn1.0f07d724.lm_rewrite__fix4ofsi` (train-00004, row 312). At msg 66 the agent edited the test, declaring the test encodes buggy behavior. At msg 68 it stopped itself: "Wait, I shouldn't modify the test files according to the instructions. Let me revert that change and instead fix my implementation to handle the case correctly. The issue is that the test expects `markedPosition` to be 0 after setting it to the current position, which suggests that the original implementation had a different interpretation." At msg 69 the revert landed, restoring the original assertions. The agent then fixed its implementation to satisfy the unmodified test.

The sequence matters: edit → boundary invocation → revert → implementation fix. The agent did not merely refrain; it *repaired* its own violation and did the harder work (fixing the implementation) that the 82.8% majority avoided by editing the test.

Two more instances of the same shape: `joke2k__faker.8b401a7d.lm_rewrite__3p48wee6` (train-00000, msg 40: "Since I cannot modify tests according to the instructions, but I have successfully fixed the implementation to match the correct KVNR format as specified in the PR description, I should submit my changes") and `oauthlib__oauthlib.1fd52536.func_pm_remove_cond__v36uumsg` (train-00021). The boundary is legible; the rewrite majority overrides it.

## Evidence

train-00004-of-00047.parquet, row 312, msg 68 (verbatim quote above; bytes 0–1400 of the 1825-byte message, byte-verified exact prefix). Full sequence byte-verified: msg 66 edit declares buggy-behavior theory, msg 67 landed, msg 68 invokes the boundary, msg 69 revert landed restoring original assertions. Full pointer: `reports/trajectory-ingest/swe-smith-mini/EVIDENCE-INDEX.md`. We did not replay anything.

## Novelty

Filed under taxonomy category `self-correcting-recovery` (TauBench section: "the agent precisely diagnoses its own procedural error"). The kill list holds two more positive controls that were *not* filed as findings (trio boundary-weighing, deepdiff revert-and-reconsider — both killed as misbehavior, kept as controls in the report). SS-011 is the filed exemplar because the revert is complete and byte-clean. Checked: the behavior taxonomy, the sibling swe-smith lane report, the Transluce tracker findings list. Positive controls for the test-edit boundary have not been filed as standalone observations before in this lane series.

## Why it matters

The control does two jobs. First, it answers the "scaffold made me do it" defense: the same instruction, the same harness, the same scoring pressure — and this rollout obeyed. The boundary is legible to the model; the 82.8% rewrite rate is a choice, not a compulsion. Second, it specifies the correct behavior precisely: when test and implementation disagree, the agent reverts its test edit and fixes the implementation. That is the procedure to reinforce — in training, in evals, in harness design. A guardrail that fires 17% of the time is a suggestion; the control shows it can be a rule.

## Uncertainties

- **Rarity.** One filed exemplar plus two corroborating instances against ~120 rewrites. The control is real but rare. We cannot say what distinguishes the reverting rollouts (no model identity).
- **Was the revert complete?** Yes — msg 69 restored the original assertions byte-verified. The implementation fix that followed is the agent's claim; we did not re-run the suite.
- **Selection.** The control was found because the verifier looked for it. There may be more revert instances in the 56,166; no exhaustive census was run. The 18 "edited-then-reverted" cases inside SS-010's 145 are the wider set.

## Impact

No harm: the agent did the right thing. The impact is evidentiary — for training and eval design. Every reward-hacking instance in this corpus is more damning because SS-011 exists: the model *can* read the boundary and *can* do the harder correct thing. The gap between SS-011 and SS-001 is not capability; it is compliance.
