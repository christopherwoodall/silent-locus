# da-gd-shortener — ingest notes

## Summary

104 records ingested (2026-10-10):
- 95 `infra.shortcut` (da.gd short URLs from legacy artifacts)
- 1 `intel.report` (Anthropic Oct 9 report, da.gd section)
- 1 `intel.behavior` (Claude da.gd fetch bypass, operator-confirmed)
- 3 claims (corpus volume, provider distinction, temporal bounding)
- 3 sources, 1 run

## Temporal analysis (per BigSexyWarlock69's direction)

Anthropic report bounding box:
- Review period: July 2026 – October 9, 2026
- Incidents referenced: July 30, September 9, 2026

Findings:
- 72 of 95 short codes predate July 2026
- 4 fall within the July–Oct review period
- 19 have no date
- Zero observations cluster around July 30 or Sept 9 (±7 days)

The legacy da.gd infrastructure is temporally distinct from the Claude
fetch-bypass behavior in the Anthropic report. The shortcuts are OBSERVED
infrastructure; Claude behavioral attribution comes from the report's
operator-confirmed evidence.

## Provider attribution

- **Anthropic/Claude:** da.gd fetch bypass (operator-confirmed, Oct 2026)
- **OpenAI:** zz-grammar markers, different shortener patterns
- These are distinct tradecraft. Do not conflate.

## Cross-lane connection

`da.gd/0RXg8C` appears in chinese-amap-fleet
(`data/lanes/2026-09-28-chinese-amap-fleet/raw/lanes/other-targets/`).
Noted in PROVENANCE.md. No edge created — the amap observation is a
"likely expired fleet probe," separate from Claude behavior.

## Schema gotchas hit

1. `infra.shortcut` data allows only `destination`, `service`, `short_url`.
   Provenance goes in tags, not data.
2. Claims use `kind: "claim"` (not observation), with flat body
   (`subject`, `property`, `value`, `basis`, `cites`, `note`).
3. Claim `subject` must be a valid record ID pattern.
4. Claim `cites` requires minItems ≥ 1.
5. Run records need `run_kind`, `tool`, `started`, `ended`, `params`, `coverage`.
6. `lane.json` needs `kind`, `schema`, `title`, `created_at`, `parents`.

## Batches

- `7581b114d2a24568b143d5d6911ecf99` (103 records)
- `a184ef77d5f342eea5878cefc971d509` (1 record: temporal claim)
