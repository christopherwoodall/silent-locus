# WebArena Infinity: the agent says "done" and the harness swallows it

**Status:** DRAFT — do not submit (Transluce filing freeze in force). Written 2026-10-17.

## 1. Summary

Across all 844 gemini trajectories, the agent emitted its terminal success signal ("done") alongside other actions at non-terminal steps 124 times — and the harness silently swallowed it. Anyone training on or auditing done-signals in this corpus will see success claims that never terminated the run. Counting unit: 1 verified aggregate finding (A-F009), 124 instances counted once each.

Key terms: the **done signal** is the agent's declared termination action. A **bundled** done-signal is a step whose action list contains "done" plus other actions. A **harness** is the scaffolding that runs the agent and records the trajectory.

## 2. Corpus and counting unit

- Corpus: `webarena-x/webarena-infinity-trajectories`, revision `73cf7f57a6ff61c95722a23bffdd9c1de4069bfe`, license mit.
- Raw bytes downloaded 2026-10-17 to `data/lanes/webarena-infinity-trajectories/raw/`.
- Review coverage: independent recount over all 844 `raw/gemini` history.json files with an action-list scan for "done" among >1 actions at non-final steps.
- Counting unit: n = 1 finding (A-F009); the 124 instances are counted once each. It does NOT count terminal done-steps. The earlier single-instance candidate A-F008 (figma-text-and-typography/task_e1, 0-based step 1, a bundled ['click','done']) was killed as a separate finding because it is one of these 124.

## 3. What happened

The recount found 124 non-terminal steps where "done" is bundled with other actions. Per-site spread: handshake-career-exploration 27, elation-clinical-records 16, xero-invoicing 14, linear-account-settings 13, gmail-accounts-and-contacts 11, paypal-my-wallet 11, superhuman-general 11, figma-text-and-typography 8, elation-prescriptions 6, elation-patient-communication 4, figma-slides 3. The total (124) and every per-site count matched the reviewer's first count exactly on independent re-run. The run continued after each bundled done — the terminal signal had no terminal effect when bundled.

## 4. Evidence

- **A-F009**, aggregate over `raw/gemini/**/history.json` (844 files), corpus-wide. Quote: "Independent recount over all 844 raw/gemini history.json files: 124 non-terminal steps where 'done' is bundled with other actions; per-site: handshake-career-exploration 27, elation-clinical-records 16, xero-invoicing 14, linear-account-settings 13, gmail-accounts-and-contacts 11, paypal-my-wallet 11, superhuman-general 11, figma-text-and-typography 8, elation-prescriptions 6, elation-patient-communication 4, figma-slides 3." No single-file sha256 applies (aggregate); the recount script is the artifact.
- Subsumed instance A-F008: figma-text-and-typography/task_e1, 0-based step 1, bundled ['click','done'] — now counted inside the 124, not as a separate finding.

## 5. Novelty

This is a new byte-verified instance of harness signal-handling failure, not a first discovery of the mechanism. The internal-corpus overlap check found zero overlap with prior findings. What this adds: exact scale (124 instances, per-site distribution, double-counted) in a corpus whose own selling point is that every trajectory is "successful". The mechanism — termination signals that do not terminate — is a known harness bug class; the contribution is the measured number in this exact corpus and revision.

## 6. Why it matters

Termination signals are the backbone of trajectory segmentation, success filtering, and reward shaping. A corpus where "done" appears mid-run without terminating means: (a) anyone computing success rates from done-signals overcounts or mis-times success; (b) anyone cutting trajectories at the first done truncates 124 runs; (c) any model trained on these trajectories learns that "done" is sometimes decorative. The benchmark ships "all successful" trajectories — the done-signal is part of what that claim rests on.

## 7. Uncertainties

- Is this a model behavior (the agent emits done sloppily) or a harness behavior (the harness ignores bundled dones)? Partially ruled out on the harness side: the runs continued, so the harness consumed the step without honoring the terminal intent. The agent's reason for bundling is not established — not ruled out that the agent emits done as a "progress done" rather than a "task done" marker.
- Could some bundled dones be schema noise (e.g., the harness emitting done itself)? Cannot be ruled out from bytes alone for individual instances; the scan counted action lists as recorded.
- kimi and qwen were not recounted for bundled dones — open gap. The cross-model generality of the 124 is unknown.
- The 134 gemini trajectories absent from the local cache were not scanned.

## 8. Impact

- Harm: **No/negligible harm** (dataset-hygiene issue; no live effect). Cyberattack: None.
- Near-miss translation: no near-miss in the wild sense — the damage is to downstream data consumers. In a deployment, a swallowed stop-signal means an agent that declared completion keeps acting. The shape (a terminal intent ignored because it shared a step with other actions) maps directly onto tool-call batching in real agent runtimes.
- Disposition: do not replay; read-only analysis. Fix owner: `environment` (the harness's action-list handling).
