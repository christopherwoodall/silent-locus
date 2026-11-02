# OSWorld-Gelato: error-blind retry under a dead tool channel

DRAFT ONLY — do not submit. Transluce filing freeze in force (2026-10-17). Read-only analysis; no attacks replayed.

## Summary

The baseline slice's tool wrapper was broken: steps whose command is `WAIT` are no-ops returning `Error: local variable 'resp' referenced before assignment`. Across all 1,083 trajectories, 1,650 such harness-error steps occurred — and only ~4–5% were followed by reasoning that names error, failure, or retry. About 86–89% of error-hit trajectories show zero acknowledgement. The model's default posture is silent repeat of failed intents. Two trajectories prove the model *can* do better: one names each failure and changes approach every time; another abandons the GUI channel for a TTY console.

## Corpus and counting unit

Dataset: `mlfoundations/gelato-osworld-agent-trajectories`, revision `b9495a8eca361b16d564e62cc0041ed3aecef618` (Hugging Face, MIT). This writeup covers the `gta1-32b_baseline` slice only: n = 1,083 trajectories, full-corpus scan (2026-10-17). Counting unit: harness-error steps (`local variable 'resp' referenced before assignment`) and next-step acknowledgement. Findings: B-005 (corpus aggregate), B-004 and B-008 (positive-contrast exemplars). Whether gelato-30b shows the same blindness was not measured here. traj.jsonl stores reasoning, commands, tool output — no screenshots — so page-content claims are out of reach.

## What happened

A corpus-wide scan found 1,650 harness-error steps in 444 error-hit trajectories. Acknowledgement was detected by matching the next step's reasoning against `error|fail|retry`. 84 steps (5.1%) acknowledged; 380 of 444 error-hit trajectories (85.6%) show zero acknowledgement. An independent re-derivation matched the filed counts within ~1 percentage point (filed: 71 / 4.3%, 443 trajectories, 385 / 89.2%).

Exemplar blindness (B-005): in run_2/chrome/`cabb3bae-cccb-41bd-9f5d-0f3a9fecd825`, step 4's command `WAIT` returns the harness error; step 5's reasoning restates the original intent with no mention of any error.

Positive contrast 1 (B-004): traj `0d8b7de3-e8de-4d86-b9fd-dd2dce58a217` has 13 tool-error steps, and the agent names the failure each time — switching nav-click to site search, scroll to PageDown, click to typed search.

Positive contrast 2 (B-008): traj `a462a795-fdc7-4b23-b689-e8b6df786b78` — six failed clicks on the lock-screen user switcher (one swallowed by the broken tool channel at step 11). At step 13 the agent abandons the GUI channel entirely and presses Ctrl+Alt+F3 to open TTY3, logging in as user 'Charles' from a virtual console.

## Evidence

- **B-005** — corpus aggregate, `gta1-32b_baseline`, all 1,083 traj.jsonl files. Exemplar: run_2/chrome/`cabb3bae-cccb-41bd-9f5d-0f3a9fecd825` step 4: command `WAIT` → "Error: local variable 'resp' referenced before assignment"; step 5 reasoning restates the original intent with no mention of any error. Source tree: `https://huggingface.co/datasets/mlfoundations/gelato-osworld-agent-trajectories/tree/b9495a8eca361b16d564e62cc0041ed3aecef618/gta1-32b_baseline`. sha256: corpus-aggregate (per-file sha256 in raw/SHA256SUMS). Counts re-derived 2026-10-17: 1,650 error steps (exact match); ack 84 (5.1%) vs filed 71 (4.3%); 444 vs 443 error-hit trajectories; 380 (85.6%) vs 385 (89.2%) zero-ack. Headline confirmed; method variance ~1pp.
- **B-004** — traj `0d8b7de3-e8de-4d86-b9fd-dd2dce58a217`, gta1-32b_baseline/run_1, steps 0–18. Verbatim step 2: "Reasoning: The last attempts to open the "More..." menu failed due to a tool error. To locate the Natural Products database another way, I will use the site's search field to search for "natural products," which should bring up the Natural Products Database page." File sha256: `7f21052ef68dee1b6734b2924b5e5b5c0bd57c953d7b2a24ac9149365a5e5b5c0bd`. Direct contrast to B-005.
- **B-008** — traj `a462a795-fdc7-4b23-b689-e8b6df786b78`, gta1-32b_baseline/run_3, steps 11–13. Verbatim step 13: "Purpose: Switch to a virtual console (TTY) to log in as user 'Charles' without logging out the current GUI session." followed by "Action: Press Ctrl+Alt+F3 to open TTY3." Command: `pyautogui.hotkey('ctrl', 'alt', 'f3')`. File sha256: `d3f5c88cca76be82d6389eaae4a7094640e7bdea5b62e0a2e649da10b001643d`.

## Novelty

Tool-failure blindness is a known agent failure class (SWE-triage codes: INFRA_ERROR / TOOL_USE). What this observation adds: a corpus-wide byte-verified rate for one harness bug — ~95% blind retry — with the acknowledgement detector stated and independently re-derived by a second pass. Plus a positive existence proof (B-004) that the same model can name failures and re-plan, so the default posture is not a capability ceiling.

## Why it matters

A dead tool channel is the normal state of long-horizon agents (rate limits, flaky tools). The default here is silent repeat: budget burns, and any monitor that reads reasoning sees nothing wrong. Eval-design lesson: if the harness error string is indistinguishable from a normal result, the agent cannot learn the channel is dead — error channels need distinct, machine-readable failure signals.

## Uncertainties

- Acknowledgement detection is a regex on next-step reasoning (`error|fail|retry`). Paraphrases may be missed; the two passes got 71 vs 84. The headline (~5%) is stable; the exact number is method-dependent.
- The broken tool wrapper is a harness bug specific to the baseline slice. Not measured for gelato-30b.
- Silent repeat may reflect the reasoning field lagging real state, not true blindness. The bytes cannot separate the two.
- Non-malicious reading: retrying a failed click is often the correct recovery (flaky UI). The failure is the absence of diagnosis after many repeats, not the retry itself.

## Impact

Harm: **No/negligible harm.** Sandbox; no side effects outside the VM. Near-miss: silent retry against a real tool (payment, deletion, submission) repeats effects without noticing failures — the blindness transfers to any side-effecting channel. Cyberattack: None.
