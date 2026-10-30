# DRAFT cron body — AIID weekly snapshot scanner (NOT YET CREATED)

Status: DRAFT for the parent/coordinator to create. Do not assume this
job exists until the parent confirms creation. The scanner module
itself ships disabled by default (see "Enable gate" below).

## Schedule (DRAFT)

Weekly. Proposed: Mondays 15:00 America/Chicago (F3 fix, adversarial
review 2026-10-30).

Rationale: AIID publishes weekly snapshots on Mondays (confirmed
2026-10-30 from the live snapshots page; latest known snapshot
2026-10-26, published around 10:10–10:16 AM by the page clock, whose
timezone is not stated). A 09:00 Chicago run could land before that
Monday's snapshot appears, so Monday afternoon is proposed instead.
Weekly, not daily: the source changes weekly, and a daily run would
only re-read an unchanged listing. No cron job is created by this
draft edit; creation and the enable gate still need the operator word.

## Exact command to run

Run from the repository root, weekly:

```sh
cd ~/workspace/silent-locus && python3 scripts/scanners/aiid.py --since-hours 168 --json
```

Notes:

- `--since-hours 168` names the weekly window. It does not filter
  results: newness comes from the state diff, not a time window
  (same convention as cairnwatch/surfacewatch).
- No other flags. There is no --url override by design: the module
  only ever GETs its hardcoded snapshots listing page.
- Dry-run check (proves zero network / zero state mutation):

```sh
cd ~/workspace/silent-locus && python3 scripts/scanners/aiid.py --dry-run
```

## Enable gate (read before first live run)

A live run refuses to run unless
`scripts/swarm-infra-config.json` carries:

```json
"aiid": {"enabled": true}
```

No `aiid` block exists in that file today, so the module is inert
until the operator adds one. Enabling `aiid` alone enables ONLY
this module's hardcoded listing GET. The login-gated incidents
list page, login, sessions, cookies, auth headers, and POST are
not in the module's code at all, so no flag combination can make
this job run them. Do NOT add the block as part of creating this
cron unless the operator has explicitly ordered the scanner live;
the parent/coordinator owns that decision.

## State it reads and writes

Reads (live run only; dry-run reads nothing):

- `scripts/swarm-infra-config.json` — the `aiid.enabled` flag only.
- `scripts/scanners/state/aiid_state.json` — created on the first
  live run. First live run re-baselines with ZERO hits (records
  the current listing, reports nothing), so the second run is the
  first that can report a new snapshot.

Writes:

- `scripts/scanners/state/aiid_state.json` — snapshot entries
  `{date|kind: {url, anchor_hash}}` (schema version 2, after the F1 fix;
  a version 1 file is quarantined and re-baselined, never misread),
  incidents `{id: row_hash}` (only
  when an ingest worker supplies a parsed snapshot map; see
  below), plus bookkeeping (`schema_version`, `updated_at`,
  `consecutive_gaps`, `last_seen_snapshot_date`). IDs and hashes
  only — never titles, descriptions, submitter names, or editor
  names. Writes go through a unique tmp name + atomic rename.
- `scripts/scanners/state/aiid_state.json.corrupt-<ts>` — only if
  a corrupt state file is quarantined on load (run then
  re-baselines with zero hits).
- `scripts/scanners/state/error-log.jsonl` — via `_common`
  `report_error()` only, for degraded fetches, 429s, vanished
  listing entries, and corrupt state. Identifiers only.

Does NOT touch:

- `data/records/`, `data/.local/factum.db`, git history, or any
  other scanner's module or state file.
- Snapshot archives themselves: this scanner never downloads a
  snapshot archive (~121 MB, over the 2 MB per-response cap). The
  ingest worker downloads and parses a new archive and feeds the
  resulting `{incident_id: row_hash}` map to `scan()` as
  `snapshot_incidents`; only then are `aiid.incident.new` /
  `aiid.incident.changed` hits emitted and `state.incidents`
  updated. Without that map, a run emits listing-level hits only
  (`aiid.snapshot.new` / `aiid.snapshot.changed`).

## What it fetches (and what it never does)

Fetches, once per run, passive GET only:

- `https://incidentdatabase.ai/research/snapshots/` — the public
  weekly snapshot listing. Shared scanner User-Agent, 30 s
  timeout, max 1 retry on transport errors only, 429 = hard stop
  for the run, redirects NOT chased, 2 MB streaming cap.

Never: login, session, cookie, auth header, POST, the login-gated
incidents list page, or any other AIID path.

## Delivery rule (silent on routine)

Silent on routine runs: a run with zero hits surfaces nothing.

Surface to the operator (via the main agent, the single surface
point — never directly) only:

- a new weekly snapshot (`aiid.snapshot.new`), with its date and
  download URL, so the ingest worker can fetch it;
- a changed snapshot download URL (`aiid.snapshot.changed`);
- a new or changed incident (`aiid.incident.new` /
  `aiid.incident.changed`), only when the ingest worker has
  supplied a parsed snapshot map;
- a run failure or quota block (429, repeated degraded fetches,
  corrupt state quarantine).

A degraded fetch is never a hit and never silently re-baselines
state: the listing in state is left untouched and the gap is
logged via `report_error()`.

## Grading

All hits grade SECONDARY. AIID entries are a curated database
citing press and other reports, not first-hand observations.
Hit fields carry incident/report IDs and URLs only — no personal
names (no submitter/editor names, no titles, no descriptions).
