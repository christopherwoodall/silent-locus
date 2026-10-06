# Analyst notes — index

162 analyst writeups across the hunt, one file per investigation thread.
Companion to `data/` (evidence) — this is the narrative/interpretation layer.

## Naming

- `analyst-note-<topic>-<YYYY-MM-DD>.md` — single writeups
- `<topic-slug>/` — threads with multiple files (e.g. `chinese-agent-fleet/`, `exploitgym/`, `dockerhub-trojan-images/`)

## What a note covers

Each note summarizes one investigation: what was checked, observed evidence
(with full unredacted values per the standing never-redact rule), verdict,
and open leads. Notes are dated to the investigation, not the event.

## Using them

- To trace a lane: grep by topic slug, then follow the `data/<date>-<slug>/`
  links inside the note for the raw evidence.
- Keystone notes: `analyst-note-chinese-agent-fleet-2026-10-05.md` (fleet
  synthesis), `dir-triage-W1.md` … `dir-triage-W7.md` (weekly triage),
  `completeness-audit-A…D-2026-09-29.md` (corpus completeness audits).
- Housekeeping: `ELASTIC_WRITE_PAUSE` marks the Elastic write freeze.
