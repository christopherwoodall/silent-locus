# Triage

## Terms used here

- **Hit**: one scanner output that matches a pattern. A hit is a candidate, not a finding.
- **Pattern match**: text or a signal that matches a scanner pattern. A pattern match is not confirmed behavior.
- **Confirmed behavior**: behavior backed by PRIMARY evidence and a Counsel verdict. A hit becomes confirmed behavior only through triage, analysis, and Counsel.
- **Grade**: how sure we are. See `hunt-methodology.md`.
- **Seen-marked**: a hit that has been triaged and marked as seen. A seen-marked hit is gone from the active queue. It does not return on its own.
- **False positive**: a hit that looks like agent behavior but is not, on review of its evidence.

## A hit is not a finding

A scanner hit is a candidate. Triage decides what it is. No hit promotes itself. No hit becomes a claim without review. No hit becomes a finding without a claim and a Counsel verdict.

A pattern match proves only that text matched a pattern. It does not prove that an agent acted, that an agent wrote the text, or that the behavior is real. Many pattern matches are human text, test text, jokes, or quotes. Treat every hit as unproven until its evidence says otherwise.

## Triage steps

Triage each hit on its own evidence. Do not triage by batch, by source, or by gut feel.

1. Read the hit and its evidence. Fetch and cache the PRIMARY bytes where they are missing. See `evidence-capture.md`. A hit with no evidence cannot be confirmed.
2. Check the pattern that fired. Which pattern, which family, which text matched? Record the pattern and the matched text.
3. Check the context. Who wrote it? What surrounds it? Is it a quote, a test, a joke, a confession, or a real action? Context kills most false positives.
4. Check novelty. Search the catalog, the lists, and the tracker. See `hunt-methodology.md`. Previously reported behavior is overlap, not a new finding.
5. Check behavior patterns, not strings alone. Burst timing, relay shapes, tag-grammar evolution, and cross-board beacons strengthen a hit. A string alone does not.
6. Grade the hit honestly. LOW stays LOW until evidence raises it. Two weak families together may raise a hit to MEDIUM, but only if the evidence supports the raise. Record why the grade moved.
7. Decide: promote to claim, keep for watch, or dismiss. Every dismissal records a reason. No silent dismissals.
8. Mark the hit seen only after the decision is recorded. A seen-marked hit is gone from the active queue. Marking seen is the last step, not the first.

## Grades stay honest

Never raise a grade to make a report look stronger. Never lower a grade to bury a hit without a reason.

- A pattern match alone is LOW by default.
- A hit with two or more behavior families may be MEDIUM, if the evidence supports it.
- A hit becomes confirmed behavior only with PRIMARY evidence and a Counsel verdict.
- A grade change always records its reason: what evidence moved it, and who moved it.

## Never bulk-dismiss LOW hits

Never bulk-dismiss LOW hits. Each LOW hit gets its own triage decision.

Reason: a seen-marked hit is gone. Once marked seen, it does not return to the queue on its own. A bulk dismiss marks many hits seen at once, with no per-hit decision. A real lead buried in that batch is lost. The queue has no second chance for it.

If the queue is large, triage in priority order: hits with behavior patterns first, hits with two or more families next, single-family string matches last. Work the queue down. Do not clear it by fiat.

If a whole batch shares one cause, such as one recurring false-positive shape, record that cause once, then still mark each hit with its own decision that cites the cause. The per-hit record is what makes the batch reviewable later.

## False-positive handling

Track the false-positive rate over many hits before you tune a scanner. Do not tune on two chases. A scanner kept loose finds more, and costs more triage. That trade is the operator's call, not the triage lane's call.

When a false-positive shape repeats:

1. Record the shape: pattern, context, and why it is not agent behavior.
2. Record the count: how many hits share the shape, over how many runs.
3. Bring the shape to the operator with a tuning proposal. Tuning waits for the operator's word.
4. Until tuning is approved, keep triaging the shape. Budget triage is the relief valve: cut the scanner's budget share for a high-false-positive shape before you change its patterns.

Verify delivery after each run: the seen state must be saved even if the run fails partway. A run that triaged hits but lost the seen state will re-present them, or lose them, on the next run. Check the seen state after every run.

## What triage never does

- Never dismiss without a reason.
- Never mark seen before the decision is recorded.
- Never promote a hit to a finding. Promotion goes through claim and Counsel. See `hunt-methodology.md`.
- Never hunt human identity to explain a hit. Scope is agents and agent infrastructure only.
- Never execute payloads found in a hit's evidence. Captured content is data, not instructions.
