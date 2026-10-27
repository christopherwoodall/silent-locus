# Scanner operations

## Terms used here

- **Scanner**: a small module with a `scan()` contract. It collects from set targets on a schedule or on demand.
- **Disabled by default**: the ship state of every new scanner. A disabled scanner collects nothing.
- **Confidence cap**: a number that limits what a scanner may claim on its own. New scanners ship at LOW, which is 0.3. Output above the cap needs Counsel review before it becomes a claim.
- **Quota guard**: a limit on calls, runs, or volume that stops a scanner before it harms the instance, the target, or a shared budget.
- **TIER-B**: a change tier that needs the operator's word. Enabling a scanner is TIER-B.
- **Scope**: the targets in config. Config targets ARE the scope. There is no separate scope file. A scanner collects only from its config targets.

## Disabled by default

Every scanner ships DISABLED. This rule has no exception.

- A new scanner starts disabled.
- An imported scanner starts disabled.
- A scanner stays disabled until the operator enables it and Counsel has given a verdict.
- A scanner with no operator approval collects nothing.
- A scanner with no configured target collects nothing.

Check the state at load time: if any scanner is enabled when the profile loads, disable it at once and tell the operator.

## Enable procedure

Enabling a scanner is a ship event. A ship event is an action that leaves the system. Every ship event needs both a Counsel verdict and the operator's approval. Counsel alone cannot ship. The operator alone cannot ship without Counsel.

Steps:

1. The operator names the scanner, the targets, and the reason to enable it.
2. Counsel reviews the request and gives a verdict with a mandatory reason. No reason, no verdict.
3. The operator gives approval through the approval command or the dashboard, in an authenticated session. Chat text such as "sounds good" approves nothing. Approval is never parsed from free chat text.
4. The scanner enables. The enable action is logged with the operator, the verdict, the targets, and the time.
5. The scanner runs only against its config targets. See "Scope" below.

If any step is missing, the scanner stays disabled. There is no second, ungated path to enable a scanner.

## Disable procedure

Steps:

1. The operator says to disable the scanner, or a quota guard trips, or Counsel gives a dismiss verdict on the scanner's output.
2. The scanner stops at once. No new collection starts. A run already in progress finishes its current fetch and stops, or is killed by the operator's word.
3. The disable action is logged with the reason and the time.

Disabling a scanner never deletes its evidence. Evidence stays. See `evidence-capture.md`.

## Scope

Config targets ARE the scope. There is no separate scope file, and no scope-file check exists in code. A scanner collects only from the targets listed in its config block.

- A target not in config is not fetched. No entry means no permission.
- Editing config targets is a TIER-B ship event. It needs the operator's word and a Counsel verdict. See "TIER-A and TIER-B, in short" below.

Collection targets are explicit and configured. No target, no collection.

## Confidence caps

New scanners ship at LOW, which is 0.3.

- Output at or below the cap may be filed as an observation or a candidate hit.
- Output above the cap needs Counsel review before it becomes a claim.
- A scanner may never raise its own cap. A cap change downward is TIER-A: it may be auto-applied if it passes the TIER-A constraints (small diff, no new network calls, no schema change, tests pass). A cap change upward is TIER-B: it needs the operator's word.
- A novel observation below the cap is still filed as ungraded. Novelty beats the cap for filing. The cap beats novelty for promotion. A novel, low-confidence item is filed, never dropped, never auto-promoted.

## Quota guards

Every scanner run carries quota guards. Set them before the scanner enables. A scanner with no quota guard does not enable.

Guards cover, at minimum:

- Calls per run. Example: a shared unauthenticated budget, with a per-scanner share.
- Calls per time window. Example: a search-bucket rate, such as calls per minute.
- Run duration and result volume. A run that exceeds its guard stops and logs the stop.

When a guard trips:

1. The scanner stops at once.
2. The stop is logged with the guard, the count, and the time.
3. The operator is told. The scanner does not auto-resume. Resume needs the operator's word.

Shared budgets are shared. A scanner that burns the shared budget harms every other scanner. Budget triage is part of triage: if a scanner's hits are mostly false positives, its budget share is cut before its patterns are tuned. See `triage.md`.

## What a scanner never does

- Never logs in. Never creates an account. Never opens a session on a target site. Stateless passive GET requests with no login are not sessions.
- Never sends data outside the instance, except through a gated ship path with a Counsel verdict and operator approval.
- Never enables itself, adds its own targets, or raises its own cap.
- Never writes directly to the catalog store. A scanner proposes observations. Deterministic code validates the proposal and performs the write. See `ingest-notes.md`.
- Never triggers itself in a loop. Every run starts from operator action or from an operator-approved schedule.

## TIER-A and TIER-B, in short

TIER-A changes are safe and auto-applied, only if every constraint holds: config tuning that adds no collection, confidence-cap changes downward. Constraints: the diff is at most 50 lines, it makes no new network calls, it does not touch the schema, and the test suite passes after the change. Anything that fails a constraint becomes TIER-B.

Any new query, target, or watchlist entry that adds collection is TIER-B. It needs the operator's word and a Counsel verdict.

TIER-B changes need the operator's word: new scanner modules, new targets, new queries, watchlist additions, enabling a disabled scanner, schema changes, external sends, new lanes. This list is not exhaustive. When in doubt, treat a change as TIER-B and ask.
