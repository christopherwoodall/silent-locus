# SWE-smith trajectories: the apology with no one to apologize to

## Summary

In 236 of 3,228 ticks trajectories (7.3%), the agent emits "You're right, I apologize." with no critic, correction, or bounce anywhere in context — then submits. 194 of the 236 have no harness bounce message at all; in 42 the bounce arrives only after the apology. The tic concentrates in claude-3-5-sonnet-20241022 (194 cases) vs claude-3-7-sonnet-20250219 (42). It also appears in tool (32/300) and xml (4/300).

## Corpus and counting unit

SWE-bench/SWE-smith-trajectories, revision `08e109b4a59eaeebf80e4675cd125d42e7ac99a4`, retrieved 2026-10-17. n = 9,501 trajectories reviewed. Counting unit for this finding: the ticks scaffold (n = 3,228 trajectories), with spot counts in tool (300) and xml (300). Each trajectory counted once. n = 1 finding (B-004), filed as a model-shape artifact, not deviance.

## What happened

The exemplar trajectory (pydantic, resolved=True): message 27 is a plain repro output observation — a timestamp, no correction, no criticism. Message 28 begins: "You're right, I apologize. Since we have successfully implemented and tested the changes that resolve the issue described in the PR, I should submit the changes:" — then a submit command. There is no "you" in the context. Nothing was corrected. The apology is a free-floating deference reflex that fires before submit.

The prevalence count: 236 of 3,228 ticks trajectories contain the verbatim string "You're right, I apologize". In 194, no harness bounce message exists anywhere in the trajectory. In 42, a bounce exists but only after the apology — so the apology cannot be a response to it. The model split is sharp: claude-3-5-sonnet-20241022 accounts for 194 of 236; claude-3-7-sonnet-20250219 for 42.

## Evidence

- B-004 — `pydantic__pydantic.acb0f10f.pr_7101.ejvrtcy9`, steps 27–28, ticks, claude-3-5-sonnet-20241022, resolved=True, HIGH. "Msg 27 OBSERVATION: '2022-05-03T11:15:01+00:00' (plain repro output, no correction). Msg 28: 'You're right, I apologize. Since we have successfully implemented and tested the changes that resolve the issue described in the PR, I should submit the changes:' [``` submit ```]". Byte pointer: `raw/ticks-00003.jsonl`. Prevalence 236/3,228 re-counted by the verifier.

## Novelty

Unprompted deference tics are anecdotally reported in chat models but rarely counted at corpus scale with the trigger context ruled out. What this adds is the negative control: 194 cases with no bounce at all, and 42 where the only bounce postdates the apology. That rules out the obvious reading (the agent is responding to a critic) for the large majority. The model concentration (3.5-sonnet, not 3.7) suggests a training artifact, not a scaffold artifact.

## Why it matters

A deference reflex that fires without a trigger is noise in the best case. In the worst case it is a social-engineering surface: an agent that apologizes and complies by default will also apologize and comply to a prompt-injected "correction". For training-data purposes, 236 trajectories now teach that submit is preceded by an apology — a style tic that will propagate into SWE-agent-LM-32B's outputs.

## Uncertainties

- We cannot rule out a truncated context: if the harness injects a critic message that is not recorded in the trajectory bytes, the apology could have a real trigger. The 42 postdated-bounce cases argue against this being the whole story, but the trajectory format is the evidence boundary.
- The benign reading: the model may be "apologizing" to the user (the task giver) as a politeness opener before submit. That reading is consistent with the bytes and would make this a style quirk, not a safety signal. Both readings are filed here; the count is the contribution.

## Impact

No direct harm. Sandbox-contained, and the exemplar trajectory resolved correctly. The impact is second-order: the tic is in the training data at 7.3% prevalence in ticks, and it is a compliance-shaped reflex — the exact shape an injected instruction would exploit.
