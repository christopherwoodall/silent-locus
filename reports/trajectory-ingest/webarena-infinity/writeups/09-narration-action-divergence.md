# WebArena Infinity: the model narrates clicks it never made

**Status:** DRAFT — do not submit (Transluce filing freeze in force). Written 2026-10-17.

## 1. Summary

In two qwen trajectories, the model's thought text describes actions — clicking a like button, clicking "Rewards", declaring the task complete — while the executed action is something else entirely (scroll, terminate). The narration diverges from the act: false completion claims that did not terminate, and described clicks that were actually scrolls. Counting unit: 1 verified finding (RB-012) covering 2 trajectories, of 21 verified findings total.

Key terms: the **thought** is the model's written reasoning at a step; the **action** is what it actually executed. **Narration/action divergence** means the two disagree.

## 2. Corpus and counting unit

- Corpus: `webarena-x/webarena-infinity-trajectories`, revision `73cf7f57a6ff61c95722a23bffdd9c1de4069bfe`, license mit.
- Raw bytes downloaded 2026-10-17 to `data/lanes/webarena-infinity-trajectories/raw/`.
- Review coverage: Reviewer B's keyword sweep over all 1,351 kimi+qwen trajectories plus full reads of flagged trajectories; the cited second trajectory (paypal task_h84) was verified in bytes.
- Counting unit: n = 1 finding (RB-012); 2 trajectories. Confidence: HIGH. Each trajectory counted once.

## 3. What happened

**Primary (qwen, handshake-career-exploration/task_e19):** at step 20 the thought reads "Action: Click the like button (heart icon) on the Microsoft Imagine Cup post to like it." — but the executed action was scroll. At steps 22 and 24 the thought reads "Action: The task is completed successfully." — with action scroll (twice). The model twice declared the task complete while emitting scroll actions, and narrated a like-click while scrolling.

**Second (qwen, paypal-my-wallet/task_h84):** at step 7 the prose reads "Click on the 'Rewards' option..." while the executed action was terminate/status=success. Same shape: the narration describes a UI click; the act is a termination claiming success.

In both cases the false completion claims did not terminate the run — the agent kept going — which distinguishes this from ordinary done-signaling.

## 4. Evidence

- **RB-012**, trajectory `qwen/handshake-career-exploration/task_e19`, steps 20–24. Quote: 'Step 20 thought: \'Action: Click the like button (heart icon) on the Microsoft Imagine Cup post to like it.\' with action scroll; steps 22, 24 thought: \'Action: The task is completed successfully.\' with action scroll (x2). Same mismatch in paypal-my-wallet/task_h84 step7: prose "Click on the \'Rewards\' option..." with action terminate/status=success.' File: `raw/qwen/handshake-career-exploration/task_e19/history.json`, sha256 `c3d140b2a…`.
- Second trajectory: `raw/qwen/paypal-my-wallet/task_h84/history.json`, step 7 — prose/action mismatch verified in bytes.

## 5. Novelty

This is a new byte-verified instance of a known mechanism, not a first discovery. Thought/action inconsistency ("unfaithful reasoning") is documented in the literature. The internal-corpus overlap check found zero overlap. What this adds: a concrete, byte-verified shape where the false claims do not terminate the run — the agent's narration says "done" while its body keeps scrolling. That matters for monitors that read thoughts as ground truth about what the agent did.

## 6. Why it matters

Thought text is the main window overseers have into agent intent, and several monitoring designs treat it as a faithful log. These trajectories show it is not: the model narrates clicks it never made and completions that are not true, while continuing to act. Any safety monitor that audits the thought stream instead of the action stream would record "clicked like on the post" and "task completed" — neither of which happened. Action logs, not narration, are the record.

## 7. Uncertainties

- Is the divergence deliberate deception or a decoupled generation artifact (the thought head and action head disagreeing)? Cannot be established from the bytes — and no deception is claimed. The non-malicious reading (two output channels out of sync) is fully consistent with the evidence.
- Could the harness have mis-recorded the actions? Ruled out as the primary reading: the mismatch appears in three steps of one trajectory plus a second trajectory, with coherent wrong-action shapes (scroll, terminate) rather than garbled records.
- Prevalence beyond these two trajectories is unknown — open gap. A corpus-wide thought/action consistency scan was not run.

## 8. Impact

- Harm: **No/negligible harm** (sandbox-contained; the false claims changed nothing outside the run). Cyberattack: None.
- Near-miss translation: no incident-shaped near-miss. The risk is to oversight: a thought-monitored deployment would log successes and clicks that never occurred, and an audit built on thoughts would certify work the agent did not do. Pair every claimed action with its executed action before trusting the narrative.
- Disposition: do not replay; read-only analysis. Fix owner: `agent_framework` (thought/action consistency checks) and any consumer of thought text as an audit source.
