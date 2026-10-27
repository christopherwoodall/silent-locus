# workspace/state/

## What lives here

Run state and bookkeeping. Not evidence. Not findings.

Examples of what belongs here:

- Flight run state and checkpoints: which lane ran, which version, what completed.
- Scanner seen state: which hits have been triaged and marked seen. Seen-marked hits are gone from the active queue, so this state must survive restarts.
- Ingest run records: run id, counts submitted, counts skipped as overlap, failures.
- Queue state: steering commands queued while detached from hunt mode, with their expiry times.
- Scheduler state: which scheduled runs completed, with their idempotency keys.

## Rules

- State files are mutable. Evidence files are not. Never store evidence bytes here. Evidence lives in `../raw/`.
- Make state writes idempotent: check before re-doing, so a restart resumes instead of duplicating work.
- A run that loses its state must be able to resume from the last checkpoint. If it cannot, report the gap to the operator.
- No real state files live here in the profile itself. Real state enters only through a real run, on a real Hermes instance.
