# Ingest notes — 2026-03-07-timeline-anchors

Ingest date: 2026-10-09. Worker: agent:lane-ingest-2026-03-07-timeline-anchors.
Factum batch: 02551a35ce7b44dbaef74fc99fea8237.

## What was ingested

48 timeline-anchor events from evidence/2026-03-07-timeline-anchors/events.jsonl
(now this directory). Submitted as:

- 1 `source` record (the legacy events.jsonl).
- 1 `dataset.snapshot` observation (48 rows, coverage complete, revision = sha256
  of events.jsonl from SHA256SUMS).
- 48 `event` records, one per anchor. Each cites the snapshot.

## Mapping rules

Use plain words. Short sentences.

- Event type is `incident.reported` for all 48. This is the closest registered
  event type. It is not perfect. Some anchors are report publication dates or
  dataset notes, not incidents. The true legacy kind `timeline_anchor` is kept
  in `tags.legacy_record_kind`. A dedicated anchor type would need a new schema
  pack. That is out of scope for this lane.
- `occurred`: `day` precision gives `on_date`. `timestamp` precision gives `start`.
  Estimated precisions (`day-estimated`, `month-estimated`) give `raw` text only,
  for example `2026-06-18 (day-estimated)`. Precision is never invented.
- `title` is a short label derived from the description (text before the first
  `;` or ` -- `, max 140 chars). It is a label, not evidence.
- The full description is kept byte-identical in `tags.description`.
- Grade: `UPSTREAM` when the anchor comes from press or a public report
  (source lane `press/*`, or source URL on rubyhack.ai / socket.dev). Else
  `OBSERVED` (the hunt team's own lane-note observations). 41 OBSERVED, 7 UPSTREAM.
- June-18 cluster members keep `tags.anchor_cluster=june-18` and the queryable
  tag `anchor:june-18=true`.
- No edges were created. Edge building is a separate pass.

## Checks done

- Dedup: 8 distinctive key terms (zzmasscounty, oaitest1778473828,
  atlas_qa_handoff_20260528230548, df40f1f1, GemStuffer, public-board.com note
  history, fieldnotes gem burst, VG_CEMETERY) returned not_found against the
  corpus. 48 legacy fingerprints and 48 legacy ids are all unique.
- Post-export check: all 48 events verified — descriptions byte-identical,
  occurred mapping consistent with date_precision, cites present, lane tag on
  every record, no reserved tag keys, no empty titles.
- `verify --blobs` passed.

## Builder

`build_factum_bundle.py` in this directory rebuilds the submitted bundle
deterministically from events.jsonl.
