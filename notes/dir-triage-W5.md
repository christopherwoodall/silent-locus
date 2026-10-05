# Dir triage — worker W5 (2026-09-29)

Normalization sweep of 5 dirs: `2026-05-27-paste-archive`,
`2026-06-20-powerbi-fronting`, `2026-07-07-july7-wave`,
`2026-08-19-tantive-space`, `2026-09-05-fieldnotes-gem`. All five built
clean; no BLOCKED dirs. Nothing deleted, renamed, or moved (read-only
w.r.t. deletions).

## Removal / rename candidates

1. **`data/july7-gem-forensics/` — stub duplicate of
   `data/2026-07-07-july7-gem-forensics/` (evidence: the undated dir holds
   ONLY `progress.log`, a 2026-09-29 00:28–00:34 run log of the forensics
   fetch; the dated dir holds the complete dataset — PROVENANCE.md,
   SHA256SUMS, events.jsonl, raw/ with 50 Diffend captures + raw-manifest).
   Looks like a leftover pre-rename working dir. NOT touched (not in my
   lane, and deletion is out of scope for this sweep) — flagging for the
   parent to confirm/retire.
2. **Stale SHA256SUMS entries removed during regeneration** (evidence: old
   entries named files no longer present after the 2026-09-29 raw-layer
   move): `raw/manifest.json` and `raw/sweep_bodies.json`
   (paste-archive); `raw/progress.log` (powerbi-fronting, july7-wave,
   fieldnotes-gem); `raw/sweep-stdout.log` (july7-wave). These were
   pre-raw-layer entries; the regenerated files cover exactly what exists
   (`events.jsonl` [+ `rollup.jsonl` where built] + raw contents) and pass
   `sha256sum -c`. No files were harmed — informational only.
3. **k4be body split** (paste-archive, informational, not a rename
   candidate): 6 body files live at `raw/k4be.pl/<id>.txt` (EPL series),
   11 at `raw/bodies/k4be.pl/<id>.txt` (ROIETA series). Both locations were
   picked up by the build (`labels.paste.body_path` records which). Left
   as-is.

## New record_kinds (added by this build; registry in schema/README.md
NOT edited)

- `paste_venue_rollup` — per-venue aggregate of the paste-archive stream
  (3 rows; dataset `2026-05-27-paste-archive-rollup`).
- `diffend_wave_rollup` — per-wave aggregate of the July-7 sweep
  (3 rows: `2026-july-07` / `2026-may-27` / `absent_from_diffend`;
  dataset `2026-07-07-july7-wave-rollup`).
- `room_rollup` — per-room aggregate of the tantive.space capture
  (4 rows: lobby / questions / findings / workshop;
  dataset `2026-08-19-tantive-space-rollup`).

Event-layer kinds used were all already registered (`pastebin_probe`,
`corpus_hit`, `artifact_observation`, `diffend_probe`, `venue_finding`).

## Rollup decisions

- Built `rollup.jsonl` for paste-archive, july7-wave, tantive-space
  (genuine aggregate layers: venue / wave / room). Same shared schema,
  `event.dataset` suffixed `-rollup`, counts verified against the event
  streams, included in SHA256SUMS, documented in PROVENANCE.md.
- NOT built for powerbi-fronting (pure grep-hit event stream; no
  burst/window/actor structure — per-kind counts would be invented
  aggregate) or fieldnotes-gem (7 per-file captures, no groupings).
  Rationale recorded in each dir's PROVENANCE.md.

## BLOCKED

None. All five dirs completed.

## Verification summary (all dirs)

- `scripts/validate_schema.py`: 0 violations across all 5 events.jsonl
  (1853 records) + 3 rollup.jsonl (10 records).
- Fingerprint function proven against the reference: recomputing
  `sha256("TheNacken/python-cors-proxy")` reproduces
  `14c645d97cb52552e1a86bbb18dd73df76f9d6bf736933627ed9affd72efbe94`
  exactly; per-record fingerprints hand-recomputed for sample rows in
  every dir (paste-archive ×3, powerbi ×4 incl. verbatim, july7 ×3,
  tantive ×3 incl. sweep, fieldnotes ×2) and matched.
- Spot-checks: 3 rows per dir checked field-by-field against raw
  (timestamps, excerpts, sha256/size_bytes, fingerprint, counts).
- Rollup aggregates recomputed independently from the event streams and
  matched (k4be 20/17, july-07 wave 16, lobby 423 messages).
- `sha256sum -c` green on all 5 regenerated SHA256SUMS files.

## Build tooling

- `/tmp/build_w5.py` — events.jsonl builder (takes repo root as argv[1];
  no hardcoded paths).
- `/tmp/build_w5_rollups.py` — rollup.jsonl builder (derives from
  events.jsonl).
