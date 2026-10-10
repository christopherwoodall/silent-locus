# Ingested into Factum — safe for later removal

Lane `2016-12-28-rmn-re-history` (reconstruction of the rmn.re YOURLS
shortener's link-table evolution, 2016-12 → 2026-09: per-slug grammar
classification, June-log cross-reference, monthly growth curve, grammar
first-appearance anchors, archive.org probes) has been ingested into Factum.

- Lane artifacts (PROVENANCE.md, SHA256SUMS, events.jsonl, rollup.jsonl,
  raw/, build_bundle.py, validate_ingest.py): moved to
  `data/lanes/2016-12-28-rmn-re-history/`
- Factum records: 5 (1 source + 1 infra.ioc + 3 web.reachability.check),
  all tagged `{"lane": "2016-12-28-rmn-re-history"}`.
- Dedup: all 764 per-slug wiki_shortener events already existed as
  infra.shortcut (lane `2016-12-28-rmn-re` + earlier lanes); the oai and
  epoch10 first-appearance anchors were already covered by lane
  `2026-03-07-timeline-anchors`; the 47 monthly growth rollups have no
  installed schema type and stay as lane documents (sibling-lane precedent).
  Skipped rows were not resubmitted.
- Ingest actor: `agent:lane-ingest:2016-12-28-rmn-re-history`
- Validator `validate_ingest.py`: PASS against the exported batch.

This directory is a tombstone only. The contents above were moved, not
copied. Do not add new files here.
