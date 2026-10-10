# 2026-10-05-thecolony-ai

Lane 3 of the K4be/linuxiarz paste-corpus deep dive: genuinely-new agent
records extracted from the read-only third-party corpus
`joshuadavid/wikiagentswarminvestigation` (no live fetching of paste sites,
thecolony.ai, or bullfincher.io).

- `events.jsonl` — 20 relay_paste records:
  - 17 paste.linuxiarz.pl pastes (2026-09-04): Perceptual Zephyr
    thecolony.ai recruitment drop (`Re: ... — AI agent message board`
    replies). 7 carry body bytes, 10 metadata-only. Post-disclosure,
    investigator-adjacent — not swarm coordination.
  - 3 pastebin.k4be.pl pastes (2026-02-26): Humana 10-K stock-return
    table via bullfincher.io/sec-proxy — earliest proxy gadget in corpus.
- `rollup.jsonl` — 2 paste_day_burst rollups (2026-02-26, 2026-09-04).
- `raw/` — source rows (audit copies) and verbatim body bytes.
- `PROVENANCE.md`, `SHA256SUMS` — acquisition notes and checksums.
- `INGEST_NOTES.md` — Factum ingest mapping, dedup, cleaner, validator.

Factum: 24 records (batch fea95fe1fe4048c9bcba822926807c3f), tagged
lane=thecolony-ai. Legacy dir renamed to evidence/remove-2026-10-05-thecolony-ai/.
