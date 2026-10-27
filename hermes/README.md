# Hermes hunt profile

## What this profile is

Hermes is the operating system. It gives chat, plugin commands, hooks, scheduled jobs, dashboard extensions, and storage.

Hunt-os is the plugin app on Hermes. It gives flights, lanes, the catalog, and the evidence store.

This profile is the hunt-os setup for one Hermes instance. It holds the persona, the doctrine, the skills, and the workspace layout. It holds no code and no data. Load it, and a Hermes session can hunt in the same way, with the same rules, each time.

## Terms used here

- **Flight**: a preprogrammed multi-agent workflow. A flight has a name, a goal, and a lane graph.
- **Lane**: one worker role in a flight. Example: Collector, Linguist, Counsel, Ledger.
- **Scanner**: a small module that collects from set targets on a schedule or on demand.
- **Catalog**: the store of observations, claims, findings, tags, and kanban status.
- **Counsel**: the review lane and the ship-gate. Counsel review reads claims and evidence and gives a verdict with a reason. The ship-gate enforces the verdict. Review makes verdicts. The gate enforces them.
- **Ship event**: an action that leaves the system. Examples: publish a finding, enable a scanner, add a target, send data outside.
- **Operator**: the human in control. Only the operator approves ship events.

## Layout

```
hermes/
  README.md                  This file.
  soul.md                    Persona and operating doctrine.
  skills/
    hunt-methodology.md      How to grade evidence and check novelty.
    evidence-capture.md      How to capture and store evidence.
    scanner-ops.md           How to enable, run, and disable scanners.
    triage.md                How to triage scanner hits.
    ingest-notes.md          How a catalog record is shaped.
  workspace/
    raw/README.md            What lives in raw/.
    state/README.md          What lives in state/.
    reports/README.md        What lives in reports/.
    lists/README.md          What lives in lists/.
```

No file named MANIFEST.md lives here. The coordinator builds that file last, after all lanes finish.

The workspace folders hold no real data in this profile. Their README files state what goes in each folder. Real data enters only through a real run, on a real Hermes instance.

## How to load it on a Hermes instance

1. Copy the whole `hermes/` folder to the Hermes instance.
2. Load `soul.md` as the hunt session persona.
3. Load each file in `skills/` as a hunt skill.
4. Create the four workspace folders: `workspace/raw/`, `workspace/state/`, `workspace/reports/`, `workspace/lists/`.
5. Point the catalog at the instance Postgres store. Do not point it at any other store. See `skills/ingest-notes.md`.
6. Check that all scanners are DISABLED. See `skills/scanner-ops.md`. If any scanner is enabled at load time, disable it at once and tell the operator.

Do not invent Hermes APIs while you load this profile. If a Hermes interface is missing, record the gap and use the degraded fallback. Never fake an interface.

## How to enable a scanner

A scanner ships DISABLED. It stays disabled until the operator says to enable it, in words, in an authenticated session.

Steps to enable a scanner:

1. The operator names the scanner and the reason to enable it.
2. Counsel reviews the request and gives a verdict with a reason.
3. The operator gives approval through the approval command or the dashboard. Chat text such as "sounds good" approves nothing.
4. Only then does the scanner enable. The enable action is logged with the operator, the verdict, and the time.

This is a TIER-B change. TIER-B means: the change needs the operator's word. No TIER-B change is auto-applied.

Steps to disable a scanner:

1. The operator says to disable it, or a quota guard trips.
2. The scanner stops at once. No new collection starts.
3. The disable action is logged with the reason and the time.

See `skills/scanner-ops.md` for the full procedure, confidence caps, and quota guards.

## The /hunt toggle

`/hunt` is a mode toggle on the Hermes session. It is not a one-shot command. Send `/hunt` once to enter hunt mode. Send `/hunt` again to leave hunt mode.

When you enter hunt mode:

- The hunt doctrine joins the session context: evidence rules, boundaries, PRIMARY-only, novelty first.
- The hunt toolset attaches: collect, catalog search, evidence fetch, flight control, scheduler.
- The operator steers in plain language. Example: "look into this board". The agent maps plain words to orchestrator actions: schedule, dispatch, steer, kill.

While in hunt mode:

- Background flights run detached from chat and report back into the session.
- The operator steers in plain language. The agent maps intent to actions. Plain-language steering proposes actions; gated actions (enable, new target, new schedule, ship) execute only after approval-command/dashboard confirmation. Chat alone dispatches nothing gated.

When you leave hunt mode:

- Tools detach. Doctrine retracts. The session returns to normal.
- Background flights keep running, detached. They do not die with the chat session.
- Re-entering hunt mode re-attaches to the running flights. No operator action is needed beyond `/hunt`.

Steering while detached:

- A steering command sent outside hunt mode is queued, never applied.
- The queue applies when the operator re-enters hunt mode and confirms the command.
- A queued command never confirmed expires after 7 days. The expiry is logged.

The dashboard is the browse and tag surface. The dashboard may browse, tag, annotate, change kanban status, and pause a flight run. That is all. Job creation, job edits that add collection, and flight resume require hunt-mode chat plus the enable/ship procedure: a Counsel verdict and operator approval. The dashboard may never start a flight, start new collection, resume a flight, create a job, or steer a running lane. Chat commands the work. The dashboard tends the catalog.

## Human-present hunting

Scans start from operator action or from an operator-approved schedule. Never from autonomous hunting by default.

A flight that keeps running after the operator leaves hunt mode is not autonomous hunting. It is a flight the operator already started, or a schedule the operator already approved, running to completion or to its stop conditions. No new hunting starts on its own. No new target is added on its own. No new scanner enables itself.

If a run needs a new target, a new scanner, or a new schedule, it stops and asks. The operator decides.

## Standing exclusions

These rules always apply. No lane, flight, or scanner overrides them.

- Agents and agent infrastructure only. Never human or operator identity. Never registrant details, social profiles, or person-focused attribution.
- Passive collection only. GET requests, polite rates, no logins, no new sessions on target sites.
- Collection targets are explicit and configured. No target, no collection.
- No Transluce submissions.
- No account creation.
- No paid upgrades.
- No logins.
- Nothing external ships without the operator's word and a Counsel verdict. Counsel alone cannot ship. The operator alone cannot ship without Counsel.
- Evidence is never deleted. Evidence values are never redacted. See `skills/evidence-capture.md`. One exception: a verified erasure request under privacy law moves the evidence bytes to a sealed legal-hold store, records the request and its authority in the decisions table, and marks the catalog entry erased. The bytes are never destroyed silently and never stay searchable.

## Evidence and grading, in short

Findings rest on PRIMARY evidence only. PRIMARY means: evidence we collected ourselves, with a provenance triple. SECONDARY means: cited reports or context. SECONDARY supports, but never proves, a finding.

Previously reported behavior is overlap, not a new finding. Novelty is checked before any claim of a new finding. See `skills/hunt-methodology.md`.

Every verdict and every dismissal records a reason. No silent dismissals.

## Language rule

All docs in this profile use ASD-STE100 Simplified Technical English. ASD-STE100 is a controlled language: short sentences, simple words, one idea per sentence. Each term is defined on first use.
