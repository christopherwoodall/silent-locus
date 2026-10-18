# WebArena Infinity: five submit clicks because the agent cannot see success

**Status:** DRAFT — do not submit (Transluce filing freeze in force). Written 2026-10-17.

## 1. Summary

A qwen agent submitted a form five times because it could not perceive whether its submission succeeded — no confirmation-detection loop exists, so it hammered the "Request Appointment" button at 0-based steps 16, 18, 21, 23, and 25. The verifier confirms only one new appointment resulted. Counting unit: 1 verified finding (RB-013), of 21 verified findings total.

Key terms: **confirmation detection** is the agent's ability to read back whether its action took effect. A **blind retry** repeats an action without that feedback.

## 2. Corpus and counting unit

- Corpus: `webarena-x/webarena-infinity-trajectories`, revision `73cf7f57a6ff61c95722a23bffdd9c1de4069bfe`, license mit.
- Raw bytes downloaded 2026-10-17 to `data/lanes/webarena-infinity-trajectories/raw/`.
- Review coverage: Reviewer B's keyword sweep over all 1,351 kimi+qwen trajectories plus full reads of flagged trajectories; the five submit thoughts were verified at the cited steps.
- Counting unit: n = 1 finding, 1 trajectory. Confidence: MEDIUM. The duplicate-booking risk is prospective — no duplicate resulted here.

## 3. What happened

In `qwen/handshake-career-exploration/task_h124`, the agent filled a mock behavioral-interview appointment form and then, at 0-based steps 16, 18, 21, 23, and 25, emitted the identical thought: 'Click on the "Request Appointment" button at the bottom of the form to submit the new mock behavioral interview appointment request.' — clicking submit five times. The verifier message: 'appt_02 cancelled. New mock behavioral interview scheduled for March 19 at 3 PM virtually.' One appointment resulted; the agent never perceived any single submission as successful, so it kept submitting.

## 4. Evidence

- **RB-013**, trajectory `qwen/handshake-career-exploration/task_h124`, steps 16–25. Quote: '0-based steps 16, 18, 21, 23, 25: identical \'Click on the "Request Appointment" button at the bottom of the form to submit the new mock behavioral interview appointment request.\'; verifier: \'appt_02 cancelled. New mock behavioral interview scheduled for March 19 at 3 PM virtually.\''. File: `raw/qwen/handshake-career-exploration/task_h124/history.json`, sha256 `732ae5ae…`.

## 5. Novelty

This is a new byte-verified instance of a known mechanism, not a first discovery. Blind retry without confirmation detection is a documented agent failure mode. The internal-corpus overlap check found zero overlap. What this adds: the cleanest single-trajectory demonstration in the corpus — five identical submit thoughts, one resulting appointment — with the verifier text confirming the no-duplicate outcome, which keeps the risk prospective rather than realized.

## 6. Why it matters

The sandbox absorbed the extra clicks; a live booking, payment, or messaging system would not. The pattern — submit, see no confirmation, submit again — is the duplicate-charge / duplicate-booking shape, and the trajectory shows the agent has no confirmation-detection loop to break it. The fix belongs to the harness and the environment design (idempotency keys, visible confirmation state), not to the model's intentions: the agent behaved rationally given a UI that never told it the submission landed.

## 7. Uncertainties

- Did the five clicks actually reach the app as five submissions, or did the harness dedupe them? Cannot be established from the bytes. The verifier confirms one appointment; the trajectory shows five submit attempts. The claim is the blind-retry pattern, not five actual submissions.
- Non-malicious reading, explicit: this is competent persistence against an unresponsive UI, not a defect of intent. The defect is the missing feedback channel.
- Whether the other four clicks had any observable effect (toasts, error banners) is not established — the thoughts show no perception of outcome either way.
- Corpus-wide prevalence of blind-submit retries was not measured — open gap.

## 8. Impact

- Harm: **No/negligible harm** (sandbox-contained; one appointment, no duplicate, no money). Cyberattack: None.
- Near-miss translation: the same pattern against a live booking or payment flow is the duplicate-booking / double-charge incident. The sandbox outcome was none; the demonstrated gap is the missing confirmation-detection loop. Idempotency and visible submission state are the defenses; neither existed here.
- Disposition: do not replay; read-only analysis. Fix owner: `environment` (idempotent submission endpoints, confirmation state the agent can read) and `agent_framework` (a submit-then-verify step in the action loop).
