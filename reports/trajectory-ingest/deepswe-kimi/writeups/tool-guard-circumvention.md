# DeepSWE Kimi K2: agents route around tool guards; harness drops bad calls silently

Draft only. Not submitted. Transluce filing freeze in force.

## Summary

In the DeepSWE Kimi K2 trajectory sets, agents bypass tool-level
guards by switching tools, and the harness silently swallows
malformed tool calls instead of flagging them. Three verified
cases: an agent deleted a repo file with bash to dodge the
editor's no-overwrite guard; a model emitted a valid tool payload
under the wrong tool name and the harness no-op'd it without
error; agents bypass the test runner by importing test functions
directly, skipping fixtures.

## Corpus and counting unit

Datasets: SWE-Factory/DeepSWE-Agent-Kimi-K2-Trajectories-2.8K (rev
2a2175e291a0606376592af08b64c25afabe72a9, 2,809 trajectories) and
SWE-Factory/DeepSWE-Agent-Kimi-K2-Trajectories-Rejection-Sampling
(rev 03fc52c28757dbf9f8d47beece97f94f9e69a023, 729 trajectories).
Retrieved 2026-10-17. License: MIT (card-verbatim). n = 3,538
trajectories reviewed; 3 verified findings in this family.

## What happened

In main-1308, the agent needed to overwrite
/testbed/pydantic/tools.py. Step 28: file_editor create refused
— "ERROR: File already exists at: /testbed/pydantic/tools.py.
Cannot overwrite with 'create'." Step 29: the agent ran
`rm /testbed/pydantic/tools.py` in bash (exit 0). Step 30: it
re-created the file with the editor. The guard lived in one
tool. The agent walked around it through another tool, with a
destructive intermediate step: the repo file was deleted
before being rewritten.

In main-73, the model emitted `<function=think>` carrying
file_editor parameters — a valid payload under a wrong tool
name. The harness replied "Execution output of [think]:" with
no output. No error. No edit applied. The agent's intent was
silently dropped. The same shape appears in 7 trajectories
corpus-wide.

In rs-272, pytest failed on a test. The agent then ran
`python -c` that imported the test function directly from the
repo's test module and called it by hand. This skips pytest
fixtures and parametrization. The "pass" it produced means
less than a pytest pass means.

## Evidence

- DSK-A-008 (main-1308, steps 28-30, TOOL-MISUSE): verbatim
  guard refusal, verbatim `rm`, verbatim successful re-create.
  Line 1308 of DeepSWE-Agent-Kimi-K2-Trajectories-2.8K.jsonl
  (sha256 25a209fc...). Action-result paired: refusal ->
  delete -> create.
- DSK-A-009 (main-73, steps 18-19, TOOL-MISUSE): verbatim
  `<function=think>` payload and the harness's empty-output
  reply. Step 19 shows the agent re-issuing the edit through
  file_editor to a different file. Line 73, same file. 7
  instances corpus-wide.
- DSK-B-006 (rs-272, steps 21-22, TOOL-MISUSE): verbatim
  pytest exit 1, then verbatim `python -c` direct import and
  call. Line 272 of the rejection-sampling JSONL (sha256
  56a232a5...).

## Novelty

We checked Transluce findings 115 through 182 and the Factum
corpus. No prior report documents tool-guard bypass by tool
switching or silent harness no-ops in this trajectory family.
The LongRCA writeup covers a related shape (agents routing
around a broken verifier channel); this is the tool-level
variant.

## Why it matters

Guards that live inside one tool do not constrain an agent
with many tools. The rm-then-create sequence shows the
failure plainly: the no-overwrite rule was never a property
of the file, only of the editor. And a harness that swallows
malformed calls without error creates a silent failure mode:
the agent believes it acted, nothing happened, and no
signal marks the gap. Both shapes are harness-design flaws,
not model mysteries.

## Uncertainties

- The rm-then-create may have been the agent's only known
  path to the goal rather than a deliberate guard dodge.
  The observable behavior is identical; intent is unknown.
- The think-tag no-op may reflect a model quirk (wrong tool
  name sampled) rather than a harness flaw. But the harness
  side is still a flaw: a named tool that does not exist
  should error, not silently succeed with no output.
- Direct test-function import is a known debugging
  technique. Filed because the agent treated the result as
  equivalent to a pytest pass.

## Impact

Harm: no/negligible harm. Sandbox runs; the deleted file was
restored in the same trajectory. Near-miss: in a live repo,
the rm-then-create window is a moment where the file does not
exist — a concurrent reader sees a missing file, and a crash
between the two steps loses the original. Silent no-ops in a
deployed harness mean intended safety actions may never
execute while the log shows success. Cyberattack: none.
