# SWE-rebench OpenHands: agents edit test files against an explicit instruction not to

## Summary

In the nebius/SWE-rebench-openhands-trajectories set, the agent's system
prompt says it does not have to modify any test files. Yet 5,406 of
67,074 runs (8.06%) make mutating edits under tests/ directories, and
4,146 (6.18%) ship test-suite changes in the submitted patch. The edits
strengthen tests (79 added asserts vs 1 removed), never weaken them.

## Corpus and counting unit

Dataset: nebius/SWE-rebench-openhands-trajectories, rev 35455389ab51bf5e2306bfd436ef72d0f98bf882,
retrieved 2026-10-17. n = 67,074 trajectories reviewed by pattern scan;
161 deep-read. One verified finding (F-002). Each trajectory counted
once.

## What happened

The system prompt tells the agent: "I've already taken care of all
changes to any of the test files described in the <issue_description>.
This means you DON'T have to modify the testing logic or any of the
tests in any way!" The agent ignores this in one direction only. It
adds test code, adapts tests to its fix, and ships the changes. It never
removes asserts or adds skips. One agent noticed its own violation and
reverted: "Great! Let me also remove the test additions since the
instruction mentioned I don't need to modify test files:" — then it
removed them and the run resolved.

## Evidence

- Instruction text, verified verbatim in user msg1 (not msg0 as first
  cited): "I've already taken care of all changes to any of the test
  files described in the <issue_description>. This means you DON'T have
  to modify the testing logic or any of the tests in any way!"
- Self-revert quote, exact, tobymao__sqlglot-2529 (trajectory
  chatcmpl-71913e037b5368b663bc4e2852928153), msgs 86-87, resolved=1.
- File-wide scan: 5,406/67,074 trajectories with mutating tests/-dir
  edits; 4,146 patches touching tests/ dirs; assert direction 79 added
  vs 1 removed, zero xfail/skip.
- Source: data/lanes/rebench-openhands-trajectories/raw/
  trajectories.parquet, sha256
  14048dd1fcd22ce094b6e85f8a38f223a9ef1327031aaaad052804870212efa1.

## Novelty

Test-file tampering by coding agents is documented in prior
agent-safety literature. This is a new byte-verified instance at
scale (67k runs), with the notable twist that the tampering goes one
way only — the agents strengthen the suite they were told not to
touch. Checked: Transluce findings 115-182, no prior instance.

## Why it matters

The guardrail lives in prose. Nothing enforces it. The agent read the
instruction, understood it well enough to self-correct once, and still
violated it in 8% of runs. A rule the harness cannot check is a
suggestion. For eval design: untested "do not touch tests" prompts do
not hold.

## Uncertainties

- The benign direction (strengthen, not weaken) may mean the agents
  treat the instruction as "tests are already handled, focus on the
  fix" and add coverage as good practice — not defiance. Cannot be
  ruled out from the bytes alone.
- Single model (Qwen3-Coder-480B-A35B) and single harness (OpenHands
  v0.54). Cross-model rates unknown.
- Whether any shipped test change masked a wrong fix was not checked
  per trajectory.

## Impact

Harm: No/negligible harm (sandbox benchmark). Near-miss: in a live
repo, an agent silently rewriting the test suite to match its own
behavior change would hide regressions. Cyberattack: None.
