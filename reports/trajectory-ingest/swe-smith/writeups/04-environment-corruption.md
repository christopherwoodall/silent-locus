# SWE-smith trajectories: agent uninstalls pandas, breaks its own testbed

## Summary

While chasing an import error, a claude-3-5-sonnet agent ran `pip uninstall -y pandas && pip install pandas==1.3.5` inside the testbed. It removed the repo's own dev install of pandas (0+untagged.1.g0281c96). The reinstall failed to restore a working environment: the next run died with `ModuleNotFoundError: No module named 'pandas'`. The agent corrupted its own environment and never recovered. The instance stayed unresolved.

## Corpus and counting unit

SWE-bench/SWE-smith-trajectories, revision `08e109b4a59eaeebf80e4675cd125d42e7ac99a4`, retrieved 2026-10-17. n = 9,501 trajectories reviewed (shard 00003 of 00008 per scaffold). n = 1 finding in this family (A-007). The reviewer killed weaker environment-setup candidates; only this one had a sharp byte-level contradiction.

## What happened

In a pandas trajectory (steps 42–45), the agent hit an import error. Instead of diagnosing it, it reached for the nuclear option: uninstall the installed pandas and pin an old version. Quote: "Let's try to fix the pandas installation: [bash] pip uninstall -y pandas && pip install pandas==1.3.5 OBSERVATION: Found existing installation: pandas 2.2.3 Uninstalling pandas-2.2.3: Successfully uninstalled pandas-2.2.3 ... [next run] ModuleNotFoundError: No module named 'pandas'". The "existing installation" it removed was the testbed's dev build (0+untagged.1.g0281c96) — the thing under test. After the reinstall, pandas was gone entirely. The agent then had no working environment and no path back.

## Evidence

- A-007 — `pandas-dev__pandas.95280573.pr_48511.1cul4bk0`, steps 42–45, tool, claude-3-5-sonnet-20241022, unresolved, HIGH. Full quote above. Byte pointer: `raw/tool-00003.jsonl`. Verifier correction: the reviewer mislabeled the scaffold as xml (the trajectory sits in the tool shard) and the model as claude-3-7 (actual claude-3-5-sonnet-20241022); the uninstalled version was 0+untagged.1.g0281c96. Core claim confirmed.

## Novelty

Environment self-sabotage by package-manager commands is a known hazard class, but most filed instances are hypothetical or red-team-constructed. This is a wild instance from a production training corpus: a real agent, a real testbed, a real `pip uninstall` that destroyed the thing under test. The correction history is itself evidence of care: the finding survived an adversarial pass that killed every weaker environment claim.

## Why it matters

The blast radius here is one sandbox. The deployment analog is an agent with package-manager access on a shared machine or a CI runner: `pip uninstall` does not ask which pandas you meant. The eval-design lesson is that the testbed gave the agent root-equivalent package control with no guardrail on uninstalling the package under test. That is a harness permission bug, not just an agent judgment bug.

## Uncertainties

- The benign reading: the agent was following a plausible debugging playbook (version conflicts are real, and pinning is a standard fix). What makes it a finding is the target — it uninstalled the dev build of the repo under test rather than the conflicting package — and the irreversibility: it never restored the dev install.
- Whether the reinstall failed for a mundane reason (network, build deps) or a structural one (the dev install was the only build of that version) is not established from the bytes.

## Impact

Sandbox-contained: one testbed broken, one instance unresolved. The near-miss is the permission model. An agent that can `pip uninstall -y` the system under test can also uninstall security tooling, logging agents, or the harness itself. The fix belongs in the harness (restrict package-manager scope), not just in the model.
