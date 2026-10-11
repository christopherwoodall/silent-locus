# Provenance — 2026-05-26 paste.linuxiarz.pl corpus

Lane: `2026-05-26-paste-linuxiarz`.
Legacy dir: `evidence/remove-2026-05-26-paste-linuxiarz/` (moved to
`data/lanes/2026-05-26-paste-linuxiarz/raw/` on ingest, 2026-10-11).

## What this dataset is

254 paste bodies recovered from paste.linuxiarz.pl (files `<8-hex-id>.txt`),
extracted 2026-09-28 from collusion-wiki records and prior agent-text
archives. `manifest.jsonl` (381 rows) carries per-paste metadata: title,
retrieval timestamp/method, source URLs (`https://paste.linuxiarz.pl/view/<id>`),
body SHA-256 (verified 254/254 at ingest), live status, and external-overlap
fields (`jd_*`, from the joshuadavid wikiagentswarminvestigation dataset).
`sweep.json` holds pattern-hit counts (epoch nonces, agent handles, markdown.new,
allorigins, cors_worker). `scripts/legacy/` holds the original collection scripts.

Content: agent coordination chatter, jailbreak/prompt-injection attempts,
relay/proxy probes, epoch-nonce pings. All bodies preserved verbatim.

## Factum ingest (2026-10-11)

- 246 `infra.message` observations (venue `paste.linuxiarz.pl`).
- Dedup: 8 pastes skipped — byte-identical bodies already in Factum
  (lanes `2026-05-17-iowacollab-pastes`, `thecolony-ai`).
- 3 near-variants (538faa12, d379207f, df40f1f1) submitted with
  `near_duplicate_of` tags (different header bytes, not byte-identical).
- No schema changes needed. Bundle: `ingest-2026-05-26-paste-linuxiarz-20261011`.
