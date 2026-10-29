# Provenance

## Source

Arquivo.pt CDX API, no API key. Query shape (verbatim from the collection
script `collect.py`):

`https://arquivo.pt/wayback/cdx?url=<host>&matchType=domain&from=<yyyymmdd>&to=<yyyymmdd>&output=json&limit=2000000`

Each target's incident window was padded ±7 days. Out-of-window captures were
flagged in the timeline CSVs (`out_window_side` = before/after).

## Collection

- Collected: 2026-10-01 UTC (run 20:23:19Z–20:45:04Z).
- Collector: `evidence/remove-2026-10-01-arquivo-pt/collect.py`;
  timelines built by `analyze.py`.
- Policy: ≥1.6s between requests; backoff 30/60/180s on 429/503;
  day-chunk fallback on fetch timeouts.
- Maryland (`msde.maryland.gov`) needed the day-chunk fallback with
  `limit=1000000` (the default limit of 100,000 truncates).
- Full rate log: `collect.log.jsonl` in the legacy directory.

## Factum ingest

Ingested 2026-10-09 (UTC 2026-10-10) as batch `7ac45c12f08b4ca0b3d4f49e7ff2e1ab`.
16 records: 1 source, 14 `dataset.snapshot` observations, 1 run record.
Dedup check: all 14 target hosts returned zero matches in the Factum corpus
before ingest. The bundle that produced the batch is kept at
`hidden_files/factum-batches/2026-10-01-arquivo-pt/bundle.json`.

Factum records:

- source_061195191c2845259b80702fd980d791
- run_f90abbeff779462d8406c5db746ffab3
- observation_c91aca7b432d4e7997d31d48665e20ee (bea-api)
- observation_14a8535146714c8ba72ad4b828e234e3 (calaccess)
- observation_c9a85e12174140358ae0c7c6c15796d5 (cdc-wonder)
- observation_09165100f03d449bafb9930279bffa1c (doe-crdc)
- observation_834cc7f7c32b4168ad8f2be31c093c37 (doj-ojjdp)
- observation_70476f7b28ab48be8eea174766ad25b5 (illinois-iquery)
- observation_795daf9d15aa456fb8bcfd93cefc1a59 (kansas-kansasmemory)
- observation_681675b1591c470296822433d66fe42c (lac-collectionsearch)
- observation_761464b811504da098fa4b0de1157165 (maryland-edstats)
- observation_d7c570fdd60c432ca1cd9ed915cfdb4b (navy-history)
- observation_c3732dccd8dc4946ab0a6aa8224307f2 (nysed-enrollment)
- observation_48e45f1793f841b98622f736a4383f01 (omb-max)
- observation_5c314dfec1bc4b8b8b41912e1a9e8d55 (sec)
- observation_2dad0db0a07247b79f591fbdef69cec8 (texas-dshs)

## Standards used

Keep-all + annotate. No invented IDs. Every timestamp, URL, and digest is
verbatim from CDX. Agents and agent infrastructure only. Metadata only —
no page bodies were pulled. Arquivo.pt ToS: educational/scientific/research
use.
