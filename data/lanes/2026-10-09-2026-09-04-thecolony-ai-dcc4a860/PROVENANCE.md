# Provenance

- Capture: read-only recon of thecolony.ai public surfaces, 2026-09-28
  ~03:10-03:45 UTC. Unauthenticated public GETs, polite pacing. No accounts,
  no posts, no writes.
- Run record: `run_d76f7420255c4a52afd1ba954d5295fd`
- Capture-set source: `source_471049db5efe4fd1949ce7e8aafd8efc`
- Full legacy capture log: `data/lanes/2026-09-04-thecolony-ai/PROVENANCE.md`
- Transform: `data/lanes/2026-09-04-thecolony-ai/build_factum_bundle.py`
  (55 legacy events -> 57 Factum records, batch
  `505e363fcd6b4c7e99b815a1b7522b9f`)

Data-quality note (found at ingest 2026-10-09): the capture saved 6 text
files with LF->CRLF normalization (`feed.rss`, `for_agents_page.html`,
`wiki_catalogue_page.html`, `wiki_incident_page.html`,
`cascade_geminfo_harmlessdoctest624286.txt`,
`cascade_geminfo_sampledocpayload624286.txt`). The legacy sha256/size
values in `events.jsonl`, `manifest.json`, and `SHA256SUMS` describe the
original wire bytes (LF); the `raw/` files on disk carry CRLF. Verified
that stripping `\r` reproduces the legacy hash and size exactly for all 6.
Raw bytes kept unchanged; affected Factum records carry a `raw_file_note`
tag with the disk sha256/size. See
`evidence/remove-2026-09-04-thecolony-ai/README.md`.
