# FALSE-POSITIVES — Lane 12: cairnwatch (Cairn panel watch)

Scope: 4 hardcoded Cairn panel hosts (counsel-cleared MALICIOUS,
2026-10-19), polled by passive GET /projects. Every indicator below
is a directly observed event, but "observed" is not "hostile": each
rule has benign triggers. Confidence is set per rule (documented
here per the counsel ship gate) and the mitigations column is what
the module already does, not what a triager must remember.

Confidence summary:
- cairn.project.created — HIGH (a new project id really appeared;
  the benign case is operator-side, not measurement error).
- cairn.project.status_changed — MEDIUM (transitions are observed,
  but operators move projects through statuses routinely).
- cairn.worker.first_observed — MEDIUM (piggybacks on a new project;
  the worker label is the panel's own claim, not verified).
- cairn.worker.heartbeat_resumed — MEDIUM (requires a real timestamp
  advance after a stale gap; clock skew can fake it).
- cairn.worker.heartbeat_stale — MEDIUM (a quiet worker is not a
  dead worker; the threshold is deliberately wide).
- cairn.host.dark — LOW (see "Dark means dark, not dead" below).

## Deleted-then-recreated projects (fake "new")

Benign trigger: an operator deletes a project and recreates it (same
target, new id, e.g. after a failed run). The module sees a brand-new
project id and fires cairn.project.created at HIGH. The id is
genuinely new to the panel; the "new activity" reading may be wrong.

Mitigation: none available at list level -- the panel exposes no
stable target fingerprint, and titles are never stored (counsel
constraint: projections + hashes only). Triage note: a "created"
hit whose worker set and counts mirror a recently vanished project
is probably a recreate, not fresh tasking. Do not treat one created
hit as proof of new operations without that comparison.

## Timestamps advance without agent action

Benign trigger: the panel's worker loop writes last_heartbeat_at on
its own schedule (keepalive ticks, retries, the dispatcher touching
a project). An advancing timestamp proves the panel process is
alive, not that an agent did work.

Mitigation: the module NEVER alerts on advancing timestamps. Only
transitions fire: heartbeat seen on a new project id, resume after a
stale gap, stale-while-active. Mere "timestamp got newer" produces
zero hits by design.

## Clock skew (heartbeat rules)

Benign trigger: the panel host's clock drifts, or our VM's clock
drifts. A skewed clock makes a live worker look stale (false
cairn.worker.heartbeat_stale) or a stale worker look resumed (false
cairn.worker.heartbeat_resumed).

Mitigation: the staleness threshold is deliberately wide --
STALE_THRESHOLD_HOURS = 2x poll interval + clock-skew margin =
2x24h + 2h = 50h. Normal NTP drift is minutes, not days; a 50h
threshold means skew alone cannot cross it. Unparseable timestamps
produce no assessment at all (no hit, no stale flag). The 2h margin
is documented in the module docstring next to the 24h poll-interval
assumption (daily orchestrator cadence); if the cadence changes, the
threshold must be recomputed.

## Status transitions are operator routine

Benign trigger: active -> completed is the normal end of a task.
Any status move can also be an operator cleaning up, re-running, or
relabeling.

Mitigation: confidence capped at MEDIUM. The hit always carries
from->to values so the triager sees which transition fired; a
completed -> active move (re-arm) is more interesting than
active -> completed (normal finish).

## Dark means dark, not dead

Benign trigger (the big one): one dark run cannot distinguish a
panel takedown from a network timeout, an egress blip, the operator
rebooting the box, or a firewall change. Panels on bulletproof-ish
hosts flap routinely.

Mitigation: no alert until DARK_ALERT_N = 3 consecutive dark runs,
and even then confidence LOW. Rationale for N=3: with a daily
cadence, 3 consecutive dark runs span ~3 days, which filters single
network blips and short maintenance windows while still surfacing a
real takedown within a work week. The counter resets on any
successful poll, so intermittent flapping never accumulates into a
false alert. A 429 (rate limit) is NOT counted as dark -- it is a
server-side signal, tracked separately, and stops requests to that
host for the run. Redirects, wrong content-type, and bad JSON shape
are "degraded", not dark: the host answered, so the dark counter
does not move.

## Heartbeat staleness threshold rationale

Stale-while-active fires when status=active at list level but the
last-known last_heartbeat_at is older than 50h (2x24h poll interval
+ 2h skew margin). Rationale: one missed daily poll is normal (a
single dark run already suppresses nothing, but a single stale read
could just be a quiet worker between ticks); two full poll intervals
of silence from a project the panel still calls "active" means the
worker's keepalive loop has plausibly died while the status enum
was never updated -- a real state worth a MEDIUM note, not proof of
anything. Fires once per stale episode (stale_alerted flag); a
fresh timestamp clears it and a subsequent resume fires
cairn.worker.heartbeat_resumed.

Limitation (documented, not worked around): /projects/{id} is
fetched only for unseen ids, so heartbeat data goes stale by design
for long-lived projects. A project that is quiet for months will
eventually fire heartbeat_stale from its frozen first-sight
timestamp -- that is the rule working as specified, and the
one-shot-per-episode + MEDIUM cap keep it a note, not an alarm.

## First-run and re-baseline silence

A fresh state file (first run) or a quarantined corrupt state
records all observed projects with ZERO hits. Otherwise the first
run after deployment would emit ~70 spurious "created" hits. This
is baseline establishment, not a clean negative -- the module logs
the (re)baseline to stderr.

## Credential-looking values in panel data

Project titles, worker strings, and detail payloads can contain
credential-looking substrings (test fixtures, leaked keys in task
descriptions). The credential sweep records counts per pattern
class only -- never the matched values, never decoded variants
(normalize() is detection-only). redact_secrets() applies to all
scanner-emitted paths (hits, error-log context, summaries/dedup
keys, state). Raw evidence captures are unaffected (separate path,
never redacted per the 2026-10-19 carve-out).
