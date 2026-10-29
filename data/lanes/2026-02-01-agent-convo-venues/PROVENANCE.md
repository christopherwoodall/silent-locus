# Provenance

Full acquisition record: `evidence/remove-2026-02-01-agent-convo-venues/PROVENANCE.md`
(legacy lane directory, kept after ingest; the `remove-` prefix marks it
ingested and safe for later removal).

## Ingest into Factum

- Date: 2026-10-09 (actor `agent:lane-ingest-2026-02-01-agent-convo-venues`).
- Batch: `data/records/f5c68a6ad4144be69b63a76d79958a65/` (55 records).
- Dedup: `match --text` fuzzy checks for all 23 candidate terms and 4
  distinctive phrases — zero Factum corpus overlap (2026-10-09).
- Message bodies are byte-identical to `events.jsonl` (verified on ingest).
- Verdicts recorded as INFERENCE claims citing their message observation;
  observations graded OBSERVED. All 55 records carry
  `tags.lane = "2026-02-01-agent-convo-venues"`.

## Retained artifact copies

Copied from the legacy directory at ingest; sha256 values match the
manifest in `SHA256SUMS` (manifest also covers `build_dataset.py` and the
legacy `PROVENANCE.md`, which remain in the renamed legacy directory only):

- `events.jsonl`
- `raw/captures/public-board-frontpage.txt`
