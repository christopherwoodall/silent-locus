# Findings

Claims are graded OBSERVED, UPSTREAM, or INFERENCE. Evidence sits in the
per-target `dataset.snapshot` observations and the original
`evidence/remove-2026-10-01-arquivo-pt/PROVENANCE.md`.

## Corroboration of the Transluce claims

- OBSERVED: Kansas (`kansasmemory.gov`) — 36,496 captures reproduce Transluce's
  claimed peak minute exactly (1,093/min). 32,349 of 36,496 captures are
  HTTP 504. Source: observation_795daf9d15aa456fb8bcfd93cefc1a59.
- OBSERVED: Maryland (`msde.maryland.gov`) — 293,898 captures vs 295,912
  claimed (99.3%); peak 5,555/min vs claimed 5,594/min. Source:
  observation_761464b811504da098fa4b0de115716e.
- OBSERVED: BEA (`apps.bea.gov`) — 2,988 vs 3,005 claimed (99.4%); 6 burst
  minutes. Source: observation_c91aca7b432d4e7997d31d48665e20ee.
- OBSERVED: Illinois (`iquery.illinois.gov`) — 117 of 171 captures are
  HTTP 503. Source: observation_70476f7b28ab48be8eea174766ad25b5.
- OBSERVED: DoE (`civilrightsdata.ed.gov`) — the exact probe
  `State_Id=1 OR 1=1` was captured once; `zz=fillNNNN` cache-buster on 27.7%
  of captures; 19-digit `nonce=`/`prepnonce=` values. Source:
  observation_09165100f03d449bafb9930279bffa1c.

## Agent-relay signal

- OBSERVED: SavePageNow share is ~100% on every non-zero target (collection
  `SAWP5`, `save-merged-*` WARCs). These are user-triggered captures, not
  background crawl. All snapshot records carry `savepagenow_share`.
- INFERENCE: the near-total SAWP5 share corroborates agent-relay use of
  ArchivePageNow's capture feature rather than archival crawl.

## Out-of-window leads (not in Transluce's windows)

- OBSERVED: DoE — 31,600 captures on 2026-06-16 (day before the incident) +
  109 on Jun 15 + 127 on Jun 18, same API endpoints, ramping 19:00–23:00 UTC.
  Source: observation_09165100f03d449bafb9930279bffa1c.
- OBSERVED: NYSED (`data.nysed.gov`) — 12 on May 16, 185 on May 18, 3 on
  May 19–20. Source: observation_c3732dccd8dc4946ab0a6aa8224307f2.
- OBSERVED: Navy (`history.navy.mil`) — 2 captures on Apr 22. Source:
  observation_d7c570fdd60c432ca1cd9ed915cfdb4b.

## Honest negatives

- OBSERVED: zero Arquivo.pt captures for doj-ojjdp, sec, cdc-wonder,
  texas-dshs. Sources: observation_834cc7f7c32b4168ad8f2be31c093c37,
  observation_5c314dfec1bc4b8b8b41912e1a9e8d55,
  observation_c9a85e12174140358ae0c7c6c15796d5,
  observation_2dad0db0a07247b79f591fbdef69cec8.
