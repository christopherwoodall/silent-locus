# 2026-10-01-arquivo-pt: Arquivo.pt capture-metadata collection for Transluce us-canada-gov incidents

## What this lane is

Arquivo.pt CDX capture metadata for 14 US/Canada government targets named in the
Transluce us-canada-gov report (https://transluce.org/us-canada-gov, published
2026-09-30). Each target's incident window was padded by 7 days. This lane
holds the Factum-structured view of the collection.

## What was ingested

- 14 `dataset.snapshot` observations — one per target slug. Metadata only.
  No page bodies were pulled.
- 1 `source` record — the Arquivo.pt CDX API endpoint.
- 1 `run` record — the `collect.py` run of 2026-10-01.

Full per-target stats (volumes, burst minutes, peak minutes, status/mime
distributions, SavePageNow share, nonce params) live in the record tags.

## Record IDs

- source_061195191c2845259b80702fd980d791 (Arquivo.pt CDX API)
- run_f90abbeff779462d8406c5db746ffab3 (collection run)
- observation_c91aca7b432d4e7997d31d48665e20ee (bea-api)
- observation_14a8535146714c8ba72ad4b828e234e3 (calaccess)
- observation_c9a85e12174140358ae0c7c6c15796d5 (cdc-wonder, honest negative)
- observation_09165100f03d449bafb9930279bffa1c (doe-crdc)
- observation_834cc7f7c32b4168ad8f2be31c093c37 (doj-ojjdp, honest negative)
- observation_70476f7b28ab48be8eea174766ad25b5 (illinois-iquery)
- observation_795daf9d15aa456fb8bcfd93cefc1a59 (kansas-kansasmemory)
- observation_681675b1591c470296822433d66fe42c (lac-collectionsearch)
- observation_761464b811504da098fa4b0de1157165 (maryland-edstats)
- observation_d7c570fdd60c432ca1cd9ed915cfdb4b (navy-history)
- observation_c3732dccd8dc4946ab0a6aa8224307f2 (nysed-enrollment)
- observation_48e45f1793f841b98622f736a4383f01 (omb-max)
- observation_5c314dfec1bc4b8b8b41912e1a9e8d55 (sec, honest negative)
- observation_2dad0db0a07247b79f591fbdef69cec8 (texas-dshs, honest negative)

## Original material

The legacy collection directory was renamed to
`evidence/remove-2026-10-01-arquivo-pt/`. It keeps `PROVENANCE.md`,
`events.jsonl`, `collect.log.jsonl`, `timeline/*.timeline.csv`,
`timeline/*.summary.json`, and the raw CDX dumps
(`raw/*.cdx.jsonl.gz`, 165 MB compressed).
