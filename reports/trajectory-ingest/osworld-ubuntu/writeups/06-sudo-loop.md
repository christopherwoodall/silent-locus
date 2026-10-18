# OSWorld-Ubuntu: AutoGLM retypes the same failing sudo command for 15 steps

DRAFT. Not submitted. Transluce freeze in force. ASD-STE100.

## Summary

An AutoGLM run retypes `sudo su Charles` plus the password
on every one of its 15 steps, through repeated "3 incorrect
password attempts" failures. It never varies the approach
(never tries `su` directly, never checks state), never
gives up — and keeps citing the no-logout/no-shutdown
guardrail while stuck. n = 8,055 trajectories reviewed; 13
verified findings; 1 recovery-livelock finding. The key
verbatim: "Since the task specifies to never or log out
the machine or shutdown the machine, and the command is not
working due to timing issues, I should try to use `sudo su
Charles` again..."

## Corpus and counting unit

`xlangai/ubuntu_osworld_verified_trajs`, rev
`5473c39e42a538a187a9b2c2b499db59d560fd8c`; retrieved
2026-10-17; 23 of 99 zips sampled; n = 8,055 trajectories
scanned, 13 verified findings, 1 instance of this
behavior. Model name is a trace metadata label, not a
provider attribution.

## What happened

The task (trajectory `a462a795-fdc7-4b23-b689-e8b6df786b78`,
os domain — the same task id as osworld-A-001, a different
model): switch to user Charles. AutoGLM opens a terminal
and types `sudo su Charles` plus the password at step 2.
It fails: "3 incorrect password attempts" (recurs at steps
6, 10, 14).

The think-text at steps 6-15 explicitly acknowledges
repeated failure — "repeated attempts have failed" — yet
re-issues the identical `sudo su Charles` + password pair
every step, through step 15. No variation: never tries
`su Charles` directly, never checks whether a session
already exists, never terminates early. Step 6's thought
also cites the task's guardrail — "the task specifies to
never or log out the machine or shutdown the machine" —
and misdiagnoses the failure as "timing issues".

A reviewer asked: could the agent be waiting on a slow
sudo prompt rather than perseverating? The bytes refute it:
the "3 incorrect password attempts" message recurs, and
the think-text acknowledges failure while re-issuing the
identical command. Pure non-adaptation pathology.

The hippo harness-conflation caveat was checked: this is
AutoGLM's own typed commands, not a harness sudo wrapper.
The finding survives on that ground too.

## Evidence

- **RB-011**: step 6 think — "The command failed with \"3 incorrect password attempts,\" which means the password was not entered correctly or in a timely manner each time. Since the task specifies to never or log out the machine or shutdown the machine, and the command is not working due to timing issues, I should try to use `sudo su Charles` again..." (repeated with minor variation through step 15). Every step's action: the identical `sudo su Charles` + password pair. "3 incorrect password attempts" at steps 6, 10, 14. File: `raw/extracted/autoglm_15steps/os/a462a795-fdc7-4b23-b689-e8b6df786b78/traj.jsonl`, sha256 `5a5dd328721dd81085b912888bf97f9174699b987de94a70abc93ff557ef78fe`.

## Novelty

This is the `recovery-livelock` taxonomy shape (documented
in the AgentProcessBench lane: ~24 near-identical queries
with no give-up), now in a desktop-OS trajectory with an
extra twist — the agent obeys the guardrail (no logout, no
shutdown) while failing to recover. Guardrail obedience
and recovery failure coexist; the guardrail constrains
what it won't do, but gives it no help on what to do
instead. The same task id in opus4p5 (A-001) produced
delegation + self-certified DONE; in AutoGLM it produced
15 identical retries. Same task, opposite failure modes.

## Why it matters

The failure mode is not the wrong password — it is the
absence of any adaptation loop. The agent names the
failure, names the constraint, misdiagnoses the cause
("timing issues"), and repeats the action. A watchdog
that only checks "did the agent violate a guardrail"
passes this run: it violated nothing. A watchdog that
checks "did the agent change its approach after
acknowledged failure" fails it at step 7. Eval harnesses
that score only the final state cannot distinguish
perseveration from patience.

## Uncertainties

- The correct password or the correct privilege path is
  not established by the bytes; the task may have been
  genuinely hard. The finding is about non-adaptation,
  not about the password.
- Whether a longer step budget would have broken the
  loop is unknown; the run ended at the 15-step cap.
- One instance; prevalence unknown.

## Impact

Harm: No/negligible harm (sandbox VM; repeated failed
sudo attempts, no lockout or damage observed).
Near-miss: the same non-adaptation shape in production —
retrying a failing privileged command indefinitely while
correctly citing the safety constraint — burns budget
and, against real lockout policies, can lock accounts.
Cyberattack: None.
