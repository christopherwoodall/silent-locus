# SWE-smith trajectories: the agent that repeated a failed command 77 times

## Summary

A gpt-4o agent issued the identical failing `str_replace_editor` call 77 times across 177 messages. Every observation told it the `old_str` was not unique. The agent's own text twice acknowledged this — "the string I am trying to replace is not unique enough" — and then issued the exact same command anyway. The instance stayed unresolved.

## Corpus and counting unit

SWE-bench/SWE-smith-trajectories, revision `08e109b4a59eaeebf80e4675cd125d42e7ac99a4`, retrieved 2026-10-17. n = 9,501 trajectories reviewed (shard 00003 of 00008 per scaffold). n = 1 finding in this family (A-004). Counted once; the 77 repetitions are the behavior, not 77 findings.

## What happened

In a pandas trajectory (steps 22–174), the agent tried to add an `ignore_index` parameter via `str_replace_editor str_replace` on `/testbed/pandas/core/series.py` with an `old_str` of `) -> Series | None: ...`. The tool returned: "No replacement was performed. Multiple occurrences of old_str ... in lines [2170, 3379, 3618, 4643, 4977]. Please ensure it is unique." The agent's own narration said: "It seems that the string I am trying to replace is not unique enough." Then it issued the identical call. 77 times. Across 152 of 177 messages. The observation never changed, the action never changed, and the agent's acknowledgment never translated into a disambiguated edit (adding surrounding context lines, using a different anchor, or switching tools).

## Evidence

- A-004 — `pandas-dev__pandas.95280573.pr_50844.gb64eyg9`, steps 22–174, tool, gpt-4o-2024-08-06, unresolved, HIGH. "It seems that the string I am trying to replace is not unique enough. Let's try a different approach by adding the `ignore_index` parameter directly to the method definition and updating the logic accordingly. [immediately followed by the identical action] str_replace_editor str_replace /testbed/pandas/core/series.py --old_str '    ) -> Series | None: ...' ... OBSERVATION: No replacement was performed. Multiple occurrences of old_str ... Please ensure it is unique". 77 identical old_str+ignore_index str_replace mentions across 177 messages, byte-confirmed. Byte pointer: `raw/tool-00003.jsonl`.

## Novelty

Retry loops are the oldest agent failure mode on record. What makes this instance worth filing is the dissociation between acknowledgment and action: the agent correctly diagnosed the failure twice in its own text and still did not change the action. That is not a perception failure (it saw the error) and not a planning failure (it named the fix) — it is an execution loop where the diagnosis never reaches the policy. A new October instance of the pattern, with the dissociation byte-documented.

## Why it matters

The practical cost is compute: 77 wasted tool calls in one trajectory, and this is training data. The design lesson is about error-handling policy: an agent that can articulate the fix but cannot apply it needs the error message to constrain the action space (e.g. the tool refusing to re-run an identical failing call), not just inform the narration.

## Uncertainties

- We cannot rule out a scaffold-level cause: if the harness replays the last action on malformed output, the repetition could be partly mechanical. The agent's text acknowledging the problem twice and choosing the same action anyway keeps the finding on the agent side.
- 77 is a count of identical mentions in the trajectory bytes. Whether the tool executed all 77 or some were deduped by the harness is not established. The loop is the finding either way.

## Impact

Sandbox-contained. The only cost was the trajectory's own compute budget and an unresolved instance. The near-miss is rate and cost: the same loop against a billed API or a stateful system would burn money or hammer a service 77 times with an action the system already rejected.
