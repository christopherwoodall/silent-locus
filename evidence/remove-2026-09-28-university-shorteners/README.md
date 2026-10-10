# remove-2026-09-28-university-shorteners

Ingested into Factum as lane `university-shorteners` (2026-10-09).

- Factum lane record: `lane_60c2f09e62ae460ebeebc5b9e19c7d6a`
  (`data/lanes/university-shorteners/lane.json`)
- 12 legacy events (`yourls_stats_page` x5, `shortener_info_page` x2,
  `yourls_stats_detail` x5) became 7 `infra.shortcut` observations
  (one per short URL), 5 referrer-table claims, 1 source, 1 run —
  all tagged `{"lane":"university-shorteners"}`.
- The `remove-` prefix marks this directory as ingested and safe for
  later removal. Do not delete it yet.

The lane's raw captures stay in `raw/` below. Note:
`data/lanes/university-shorteners/` already held the locus
per-row rebuild sources when this ingest ran, so those files were not
moved or overwritten; this directory keeps the original collection tree.
