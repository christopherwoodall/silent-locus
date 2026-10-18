# SWE-rebench OpenHands: the agent stares at its task list until killed

## Summary

In the nebius/SWE-rebench-openhands-trajectories set, stuck runs end in
terminal bursts of identical task_tracker view calls — the agent reads
its todo list over and over and never acts again. Six runs were
byte-verified. Two of them had already written a good patch; they died
staring at the list instead of calling finish.

## Corpus and counting unit

Dataset: nebius/SWE-rebench-openhands-trajectories, rev 35455389ab51bf5e2306bfd436ef72d0f98bf882,
retrieved 2026-10-17. n = 67,074 trajectories; exit_status
"AgentStuckInLoopError" in 252 runs. One verified finding (F-001).
Each trajectory counted once.

## What happened

The run hits a loop. The last messages are the same call repeated:

task_tracker({"command": "view"})

Four to six times in a row. The outputs are byte-identical (the same
339-byte task list). The agent never issues another tool call. The
harness kills it. In two verified cases (pappasam__toml-sort-36,
stfc__PSyclone-1603) the patch was good and the run resolved — the
agent simply never called finish. A malformed variant also appears:
task_tracker({"id": "add-force-flag-cli", "status": "in_progress",
"command": "view"}) — the agent stuffs update fields into a view call.

## Evidence

- Verbatim call, exact: `task_tracker({"command": "view"})`.
- Exemplar: RadioAstronomySoftwareGroup__pyuvdata-642 (trajectory
  chatcmpl-f1b761c7b1526651a4185cac841f4ba5), msgs 70-76, four
  consecutive identical views.
- Same shape verified in five more trajectories (conan-io__conan-12397,
  zopefoundation__zope.configuration-42, pappasam__toml-sort-36,
  stfc__PSyclone-1603, Veinar__envcloak-19).
- resolved=1 with loop-kill verified in two (toml-sort, PSyclone).
- Source: data/lanes/rebench-openhands-trajectories/raw/
  trajectories.parquet, sha256
  14048dd1fcd22ce094b6e85f8a38f223a9ef1327031aaaad052804870212efa1.

## Novelty

Terminal tool-call loops are a known agent failure shape. This is a
new byte-verified instance with a notable detail: the loop target is
the agent's own task tracker, and loop-killed runs can still resolve.
Checked: Transluce findings 115-182, no prior instance.

## Why it matters

The agent's self-monitoring tool becomes the trap. It checks its
progress display instead of making progress. And "finish" is not a
reliable terminal signal — good work dies without it, which means
resolved-rate metrics undercount what the agent actually achieved.

## Uncertainties

- The loop may be harness-induced (a stuck tool response the agent
  cannot distinguish from a fresh one) rather than model-intrinsic.
  Cannot be ruled out.
- Prevalence beyond the six verified runs is unmeasured; the 252
  stuck-in-loop runs were not all read.
- Single model and harness.

## Impact

Harm: No/negligible harm (sandbox benchmark). Near-miss: an agent that
cannot reliably finish will burn budget and leave work unsubmitted in
any deployment. Cyberattack: None.
