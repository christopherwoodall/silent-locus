# 2026-09-28-pastebin-pivot

Work lane for the Factum ingest of the Pastebin pivot legacy lane.

## Scope

Read-only pivot for July-2026 ExploitGym incident artifacts on paste venues.
The 2026-09-28 worker ran marker sets A-D over 9 local corpus paths and
10 search-engine queries. No paste-body hits on any marker set. Two near-miss
hits, two context hits, one data gap.

## Ingest

Ingested 2026-10-10. 17 records, all tagged `{"lane": "2026-09-28-pastebin-pivot"}`.

- 3 artifacts (git-retained verbatim excerpts): `artifact_06327d1d98a34455a326a92a5feba767`
  (swarmtraces.org), `artifact_209b576a6c714a99a1505abbcf0ed880` (thehackernews.com),
  `artifact_263be91e7a5d4884b7a7035953f5dc62` (daylight.ai). Each capture also
  made one web.capture observation and one source.
- 1 collection source: `source_ee471cc3ff5d42179e363f79c42d7d33` (local-corpus
  marker grep sweep).
- 1 run: `run_423f609150344411b4142e8618abf1f4` (bounded_negative_sweep).
- 1 observation (infra.ioc, term m47push2, status active):
  `observation_f78023a920154ea199c32cbac846b20d`.
- 5 claims: `claim_f9eb25a63e2b4f59b0312f9afaa35d55` (pbp-001 near-miss),
  `claim_9be0b262b6bd4e538c1479d3b0e4f871` (pbp-002 near-miss),
  `claim_ecdfcc45bfba4430836ba54938619ab0` (pbp-003 context),
  `claim_2e8e8da3291145a1bf939cd4b438886f` (pbp-004 UPSTREAM),
  `claim_3a4fcdc9050b4b71a5c2939137bf7797` (pbp-005 data gap).

Lane record: `lane_3046c11b3ce64f17a3450a8fc3af609d`.

## Paths

- Lane docs: `data/lanes/2026-09-28-pastebin-pivot/`
- Legacy lane (ingested): `evidence/remove-2026-09-28-pastebin-pivot/`
- Factum records: `data/records/afa85883d6424615bf952491b7fc26e7/`,
  `data/records/7ce4064fa5724c00bf061630912d420d/`,
  `data/records/5613460c0b534c5780fb3ac25d09df70/`,
  `data/records/1c8e23cc27224c0e9098a6902438ad4f/`
- Git-retained bytes: `data/blobs/sha256/bb/`, `data/blobs/sha256/50/`,
  `data/blobs/sha256/e1/`
