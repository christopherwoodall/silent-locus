# Lane ingest note — 2026-03-11-dse-wiki-verification

Ingested into Factum 2026-10-09 (UTC) on branch factum-shaping.
Factum lane: `2026-03-11-dse-wiki-verification`
(lane_96696a4351264485aafeb5b63efd6b55).

## Records (34 total, all tagged {"lane": "2026-03-11-dse-wiki-verification"})

- 6 report captures (`capture --storage git`): the six urlquery reports cited in
  third-party DSE-wiki analyses, retrieved live 2026-09-28T02:10:57Z (Chrome UA,
  >=20s pacing). Each capture = 1 artifact (bytes in data/blobs/) + 1
  observation + 1 source. Artifact byte-hashes verified identical to the
  legacy recorded sha256 values.
- 15 indicator observations (`infra.ioc`, status=candidate): the sweep terms
  from the frozen 51,643-report urlquery cache. Sweep result carried in tags:
  frozen_cache_hits (0/1/6), live_htmx result (HTTP 204 or None, untrusted as
  negative per lane discipline), title-mention caveats for nmdigital.unm.edu
  and tok=expt. No edges created (separate pass).

## Data issue fixed (source corrected, root cause)

The 6 files in raw/reports/ each carried one spurious trailing CR byte
(`...}}\r\n` on disk vs the recorded 8084-style byte counts and sha256
hashes). The recorded hashes are over the response body which ends with a
single LF; the CR was a save-time write artifact (the acquisition manifest
SHA256SUMS already listed the correct hashes). Removed the stray CR byte from
each file (JSON content untouched). All six files now verify against
SHA256SUMS, provenance_cited.json, and events.jsonl.

Pre-existing (not touched): SHA256SUMS entries for the three sidecar files
(raw/expansion/*.json, raw/provenance_cited.json) do not match their current
bytes — they were edited after the manifest was generated (2026-09-29 schema
normalization). Evidence bodies all check out.

## Dedup

match --text --mode fuzzy on all 6 report IDs and 15 terms: no duplicates.
The only fuzzy hit was nmdigital.unm.edu ~ goto.unm.edu (a shortcut
observation from the university-shorteners lane) — a different host, not a
duplicate.
