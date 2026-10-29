# TraceLab — Evidence Index

Lane: `tracelab-trajectories`. Date: 2026-10-16.
Raw dir: `data/lanes/tracelab-trajectories/raw/`.

Every file below is cached primary-source evidence. Provenance sidecars
(`*.PROVENANCE.txt`) record source URL, retrieval time, method, and
sha256. Recomputed sha256 values match the sidecars char-for-char.

## Retrieved files (4 of 9)

| File | Bytes | sha256 | Retrieved (UTC) | Provenance |
|---|---|---|---|---|
| README.md | 6859 | `d0ff5ce6efe642b0ac9a79683c30acd68e9409d650d76c4174e86fc8518aa0ed` | 2026-10-16T21:03:10Z | README.md.PROVENANCE.txt (329 B) |
| LICENSE-DATASET.md | 2061 | `1e96a0ec55f98ee0e4e2432626c0201104ebfb7f98cecf0a31d5313ddad92e9a` | 2026-10-16T21:03:45Z | LICENSE-DATASET.md.PROVENANCE.txt (329 B) |
| NOTICE | 540 | `84f5e286d199c15c4ed2a85584ba0792cb813aa4a74ddbcf0559740244c24615` | 2026-10-16T21:04:05Z | NOTICE.PROVENANCE.txt (317 B) |
| SHA256SUMS | 521 | `dc866530dff00041c298a07fd9f2d21442c269516990968e0bdf638dc4f91998` | 2026-10-16T21:02:35Z | SHA256SUMS.PROVENANCE.txt (321 B) |

Source URL pattern for all four:
`https://huggingface.co/datasets/UW-SyFI/TraceLab/resolve/7256bbf77e76d5cb83f4ddbd5ad31d8faee9dc7a/<file>`.
Retrieval method: `https-get-curl`.

## Pipeline evidence files

| File | Bytes | sha256 | Notes |
|---|---|---|---|
| MANIFEST.json | 4041 | `4653f8a57e1e2f8e16c7b2f52302e9de9a61df02ce38082b13859c519f44e08c` | 9-file manifest: 4 downloaded + 5 GAPs, with expected sizes, expected sha256s, and the coverage note. Authored 2026-10-16T21:56Z. |
| XET_EVIDENCE.txt | 3006 | `eb0587999a38d220071c462318f90fb583ef0baa6c657b4da0e8f07fb1718aaf` | Full XET stall evidence: HEAD 302 chain, X-Linked-ETag verification, GET stall signature (curl rc=28), attempt counts, transient 36.9 MB window. |
| data/v0.0.2/ | — | — | Empty directory (0 files). Placeholder for the five blocked data artifacts. |

## Blocked artifacts (0 bytes retrieved)

Expected per MANIFEST.json (sha256 expected, verified against XET
redirect ETags char-for-char):

| Artifact | Expected bytes | Expected sha256 |
|---|---|---|
| data/v0.0.2/syfi_coding_trace.jsonl.gz | 100,939,722 | `11ce51ec0a25e3d1d95b025bca2f7d1647e47571eb7cc968acd5fc64d4b4fb65` |
| data/v0.0.2/rounds/train.parquet | 22,785,108 | `cb8c2b1d23307090c8057c747f955663bacde16a49f84a3c5071a1e2e96a7ab8` |
| data/v0.0.2/tool_calls/train.parquet | 25,909,050 | `7186e0d86d3d870e5b374cc29678a4754fcb789ebee4f5ad86461dd02db6f68b` |
| data/v0.0.2/timing_events/train.parquet | 28,511,584 | `a207499989d4f004a6807698c33ad6da57cd30fd45404188bf8593fc4d3b9296` |
| artifacts/v0.0.2/syfi_coding_trace.duckdb | 160,182,272 | `a7bab286bc640844560850965ccf47975cf66407154132abaab90f27ec9be744` |

Total expected for all 9 files: 338,402,667 bytes. Downloaded: 9,981 bytes.

## Factum batch

- Batch dir: `data/records/<batch-id>/` (batch id recorded at export time).
- 25 records: 5 sources, 10 observations, 9 claims, 1 run.
- Ingest bundle source: `data/lanes/tracelab-trajectories/bundle-tracelab-wave4.json`
  (built by `bundle-tracelab-wave4.py` in the same dir).
