# Lane: hf-trajectories-audit

## Purpose
Factum ingest of the 2026-10-07 HF trajectory flag-audit verdicts. The audit
scanned 10 HuggingFace agent-trajectory datasets for unreported anti-bot
(CAPTCHA / Turnstile / Cloudflare) defeats and for our marker grammar.
Result: 9 CLEAN, 1 DOCUMENTED, 0 NEW DEFEAT.

## Legacy documents
The former audit workspace at `evidence/hf-trajectories/` was removed in
commit `d3360745` (2026-10-11) after its behavioral content was verified
ingested into Factum. The successor ingest lanes are
`data/lanes/2026-10-11-hf-traj-{glm52,hermes,swenext,tbench}/`. This lane
holds the structured verdicts; the raw bytes now live in those lanes.

## Records in this lane
- 1 source record: `FINDINGS.md` in this lane (ranked rollup).
- 1 run record: the flag-audit run (10 datasets, complete coverage).
- 10 `dataset.snapshot` observations, one per audited dataset.
- 10 claim records, one audit verdict each (9 CLEAN, 1 DOCUMENTED), grade OBSERVED.
- 1 claim record: the audit headline (no NEW DEFEAT), grade OBSERVED.

## Factum lane tag
All records carry `{"lane": "hf-trajectories-audit"}`.
