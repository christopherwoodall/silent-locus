# Ingested into Factum

Lane: 2026-09-04-thecolony-ai
Ingested: 2026-10-09 (UTC)

All contents moved to data/lanes/2026-09-04-thecolony-ai/.
Structured records live in Factum data/records/ (batch 505e363fcd6b4c7e99b815a1b7522b9f),
tagged {"lane": "2026-09-04-thecolony-ai"}.
This directory is safe for later removal.

## Data-quality note (found at ingest)

Six text captures were saved with LF->CRLF newline normalization at capture
time (2026-09-28): feed.rss, for_agents_page.html, wiki_catalogue_page.html,
wiki_incident_page.html, cascade_geminfo_harmlessdoctest624286.txt,
cascade_geminfo_sampledocpayload624286.txt.

The sha256/size values in events.jsonl, manifest.json, and SHA256SUMS
describe the original wire bytes (LF); the raw/ files on disk carry CRLF
and are 1 byte (geminfo txt) to ~1600 bytes (wiki pages) larger. Verified
at ingest: stripping \r from the disk bytes reproduces the legacy sha256
and byte size exactly for all 6 files, so no content was lost or altered
beyond newline encoding.

Raw bytes were kept unchanged (evidence rule). The 6 affected Factum
records carry a `raw_file_note` tag with the on-disk sha256/size, and the
lane PROVENANCE.md records this. No observed values (counts, titles,
verdicts, pattern hits) are affected — they were derived from parsed
content.
