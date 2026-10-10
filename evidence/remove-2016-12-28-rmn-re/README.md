# Ingested into Factum — safe for later removal

Lane `2016-12-28-rmn-re` (passive crawl of the open rmn.re YOURLS shortener,
2026-09-27: 764-link table with short slug, target URL, creation date,
creator IP, click count) has been ingested into Factum.

- Lane artifacts (PROVENANCE.md, SHA256SUMS, build_rollup_w8.py,
  events.jsonl, rollup.jsonl, raw/): moved to
  `data/lanes/2016-12-28-rmn-re/`
- Factum records: 730 (1 source + 729 infra.shortcut observations), all
  tagged `{"lane": "2016-12-28-rmn-re"}`. 35 of the 764 links already
  existed in Factum from earlier lane ingests (open-data-api-venues,
  pxweb-national-stats, worldpoverty-task-family); those were skipped as
  duplicates, not resubmitted.
- Ingest actor: `agent:lane-ingest:2016-12-28-rmn-re`
- SHA256SUMS fix: the manifest's raw/ entries were stale after the
  2026-10-09 locus reconstruction (commit bcb00e6f); regenerated from
  actual bytes in data/lanes/, `sha256sum -c` green.

This directory is a tombstone only. The contents above were moved, not
copied. Do not re-ingest.
