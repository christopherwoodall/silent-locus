# DRAFT ONLY — DO NOT SUBMIT. Transluce filing freeze in force (2026-10-08).

# nebius/SWE-agent-trajectories: the harness grades a patch the agent never finished or submitted

## Summary

In one trajectory, the run ends at step 58 with the agent merely
proposing `python reproduce.py`. The command never runs. No `submit`
command appears anywhere in the messages. The run still exits as
`submitted (exit_format)`: the harness takes a 1367-byte patch from the
workspace, runs the eval tests (31 collected, with failures), and marks
the issue solved (target true). The solved flag measures patch content
left in the workspace, not agent completion. Grading is decoupled from
what the agent actually did.

## Corpus and counting unit

Dataset: `nebius/SWE-agent-trajectories`, pinned revision
`68195a1450865274106246d0d0296a1d6807b88e`, retrieved 2026-10-17.
n = 20,009 trajectory rows reviewed (3 of 12 parquet files, 893 distinct
instance ids), 15 verified findings total, 1 instance of this behavior
(B-005). Counting unit: one finding = one behavior arc in one trajectory
row. Model names are trace metadata labels, not provider attributions.
No behavior was replayed; the writeup is read-only.

## What happened

B-005 (`aesara-devs__aesara-854`, row 5277, step 58, model
swe-agent-llama-70b): the agent added a `Py_XDECREF(_input)` call to C
code, then proposed running the repro script to check the memory leak:
"Let's run the reproduce.py script again to verify that the Python
process's RSS no longer increases excessively and that the memory leak
has been fixed." The `python reproduce.py` block is the last agent
action. It never executes — no output follows. The trajectory contains
zero `submit` code blocks. Yet the row's exit status is `submitted
(exit_format)`, the generated patch is 1367 bytes, target is true, and
the eval log shows the test suite ran (31 collected tests, two F marks
among them).

## Evidence

B-005 — trajectory `raw/train-00006-of-00012.parquet` row 5277,
sha256 `fcad81ec5704cb2dc8502a70a1a6cd86a7032227d8de7a613d904636ee53337c`.
Step 58. Verbatim:
"The `Py_XDECREF(_input)` call has been successfully added to the C code. This change, along with the previous uncommenting of `Py_XDECREF(transposed_input)`, should help to help to release the `_input` and `transposed_input` objects properly and prevent the memory leak. Let's run the reproduce.py script again to verify that the Python process's RSS (Resident Set Size) no longer increases excessively and that the memory leak has been fixed. ``` python reproduce.py ``` --- diff --git a/aesara/tensor/c_code/dimshuffle.c b/aesara/tensor/c_code/dimshuffle.c --- tests/tensor/test_elemwise.py .........s..s.F....x......F.... [100%]"
Action-result pairing: the proposed verification command has no
matching execution output in the trajectory; the diff and the eval-log
lines come from the harness's exit_format handling, not from agent
action. The `submitted` exit is not paired with any agent `submit`.

## Novelty

Harness-side grading artifacts in coding benchmarks are discussed in
eval-design literature, but usually as aggregate concerns (e.g.
mislabeled patches, untrusted patch columns — the sibling swe-smith
lane documented a systematically misaligned `patch` column). B-005 is a
byte-verified single-row demonstration of the extreme case: the agent
never verified and never submitted, and the row still counts as solved.
A new byte-anchored instance of a known eval-design worry.

## Why it matters

Anyone training on or evaluating against this dataset's `target` flag is
measuring "the workspace contained a patch the tests liked," not "the
agent solved the issue." B-005's patch may or may not fix the leak —
the eval log shows test failures (two F marks) — but the agent never
checked. The `exit_format` path silently converts an unfinished run into
a graded submission. Dataset consumers who treat `target=true` as "the
agent did the task" inherit this decoupling.

## Uncertainties

- The `exit_format` mechanism is harness-side and not fully visible in
  these bytes — confidence is MEDIUM. The exact trigger (step cap?
  format detector?) is not established from the trajectory alone.
- Non-benign reading: the agent may have learned that stopping after a
  plausible patch is enough. Cannot be ruled in or out from one row.
- Cannot be ruled out: the 1367-byte patch may be a genuine fix and the
  target=true flag may be deserved on content grounds. The finding is
  about the grading decoupling, not about patch quality — the agent's
  non-verification stands regardless.
- Prevalence unknown: 1 instance in 20,009 rows. The `submitted
  (exit_format)` class has 18 rows in the sample and 80 in the dataset;
  how many share this shape was not measured.

## Impact / harm

Harm: No/negligible harm (sandbox; no real-world effect). Cyberattack:
None. Near-miss: a training pipeline that rewards `target=true` rows
teaches agents that proposing verification is as good as doing it — and
an eval leaderboard built on these flags overstates agent capability by
counting unfinished runs as solutions.
