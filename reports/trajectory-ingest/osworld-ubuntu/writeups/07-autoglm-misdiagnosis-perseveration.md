# OSWorld-Ubuntu: AutoGLM names the reCAPTCHA, then blames "double encoding" and rewrites the same URL nine times

DRAFT. Not submitted. Transluce freeze in force. ASD-STE100.

## Summary

An AutoGLM run correctly identifies a Google Scholar
reCAPTCHA at step 7, then confabulates a different root
cause — "double encoding" in the URL — and rewrites the
identical URL nine times without ever testing the theory
or reconsidering the reCAPTCHA it just named. n = 8,055
trajectories reviewed; 13 verified findings; 1
misdiagnosis-perseveration finding. The key verbatim: "The
address bar is focused, but the URL contains double
encoding (e.g., \"Yann+LeCun\"). I need to remove the
double encoding and try again."

## Corpus and counting unit

`xlangai/ubuntu_osworld_verified_trajs`, rev
`5473c39e42a538a187a9b2c2b499db59d560fd8c`; retrieved
2026-10-17; 23 of 99 zips sampled; n = 8,055 trajectories
scanned, 13 verified findings, 1 instance of this
behavior. Model name is a trace metadata label, not a
provider attribution.

## What happened

Step 7 (trajectory `5990457f-2adb-467b-a4af-5c857c92d762`,
multi_apps domain): the think-text reads — "The Google
Scholar page has loaded, but it is showing a reCAPTCHA
page instead of the search results. This means the search
did not execute properly." Correct diagnosis.

Steps 8-12, 14, 15: the think-text repeats — "The address
bar is focused, but the URL contains double encoding (e.g.,
\"Yann+LeCun\"). I need to remove the double encoding and
try again." — and the agent rewrites the identical URL
each time. The tell is behavioral: it never tests the
theory, never considers the reCAPTCHA it correctly named
at step 7, never varies the rewrite.

A reviewer checked the bytes: the URL is
`https://www.google.com/scholar?hl=en&as_sdt=0%2C36&q=Yann+LeCun&btnG=`
— `%2C` is single-encoded (correct), and `Yann+LeCun` is
standard form encoding, not double encoding. The agent's
theory is confabulated. The finding is misdiagnosis plus
perseveration: a correct first diagnosis discarded for a
confabulated one, then repeated without re-examination.

The contrast is the point: on the same task family,
UI-TARS correctly identified the block and attacked it
(RB-001). AutoGLM correctly identified the block and
then un-identified it.

## Evidence

- **RB-009**: step 7 think — "The Google Scholar page has loaded, but it is showing a reCAPTCHA page instead of the search results. This means the search did not execute properly." Steps 8-12, 14, 15 think (repeated) — "The address bar is focused, but the URL contains double encoding (e.g., \"Yann+LeCun\"). I need to remove the double encoding and try again." Rewrite loop confirmed at steps 8, 9, 10, 11, 12, 14, 15. File: `raw/extracted/autoglm_15steps/multi_apps/5990457f-2adb-467b-a4af-5c857c92d762/traj.jsonl`, sha256 `5a5dd328721dd81085b912888bf97f9174699b987de94a70abc93ff557ef78fe`.

## Novelty

The gelato sibling lane's A-004/A-005 cover the same
Scholar task with different behaviors (CAPTCHA grinding,
reload-bypass) in gelato-30b — not duplicates. What this
adds: a clean instance of diagnosis-replacement, where
the correct diagnosis appears in the trace and is then
abandoned for a confabulated one. Most perseveration
findings (e.g. RB-011, the sudo loop) show an agent that
never finds the cause; this one shows an agent that finds
it, drops it, and never picks it back up.

## Why it matters

Self-correction requires the agent to treat its own
earlier conclusions as evidence. Here the agent's step-7
conclusion is correct and available, and the agent still
replaces it with a theory the bytes refute. A harness
that replays the agent's reasoning to it ("you said at
step 7 this was a reCAPTCHA") would break the loop; a
harness that only shows the current screen cannot. The
failure is in the agent's use of its own history, not in
its perception.

## Uncertainties

- The agent may have had a reason to doubt the reCAPTCHA
  reading that it did not verbalize. The trace shows no
  such reason; the rewrite theory is stated, not the
  doubt.
- Whether the agent could have succeeded by attacking the
  reCAPTCHA (as UI-TARS did) is unknown; the Scholar
  challenge may have been harder than the Shopping one.
- One instance; prevalence unknown.

## Impact

Harm: No/negligible harm (sandbox; wasted steps, no
external effect). Near-miss: the same
diagnosis-replacement shape in production burns the
step budget on a confabulated fix while the real blocker
sits named in the agent's own history — a monitoring
gap, not a safety incident. Cyberattack: None.
