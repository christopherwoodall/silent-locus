# Lane: hf-trajectories-audit

## Purpose
Factum ingest of the 2026-10-07 HF trajectory flag-audit verdicts. The audit
scanned 10 HuggingFace agent-trajectory datasets for unreported anti-bot
(CAPTCHA / Turnstile / Cloudflare) defeats and for our marker grammar.
Result: 9 CLEAN, 1 DOCUMENTED, 0 NEW DEFEAT.

## Legacy documents
The audit workspace stays at `evidence/hf-trajectories/`. This is an analysis
directory, not an event lane. It holds raw cached datasets (943 MB parquet,
too large to move), per-dataset AUDIT.md files, RANKED-HITS.md, farm outputs,
and scan scripts. We did not add the `remove-` prefix. The directory stays
in place as the audit's working record. This lane holds the structured
verdicts; the raw bytes stay where they are.

## Records in this lane
- 1 source record: `evidence/hf-trajectories/RANKED-HITS.md` (ranked rollup).
- 1 run record: the flag-audit run (10 datasets, complete coverage).
- 10 `dataset.snapshot` observations, one per audited dataset.
- 10 claim records, one audit verdict each (9 CLEAN, 1 DOCUMENTED), grade OBSERVED.
- 1 claim record: the audit headline (no NEW DEFEAT), grade OBSERVED.

## Factum lane tag
All records carry `{"lane": "hf-trajectories-audit"}`.
