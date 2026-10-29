# openai-intel — provenance

OpenAI system card lab intel ingest (2026-10-10).

## Sources

Two system cards fetched via curl on 2026-10-10T14:42:34Z. Raw HTML cached in
`raw/` with sha256 recorded.

1. "GPT-6 Sol and GPT-6 Luna: October 2026 update" (published 2026-10-07)
   - URL: https://deploymentsafety.openai.com/gpt-6-october
   - Cached: raw/gpt-6-october.html
   - sha256: 31ba1b900cceac03e677770cc1b8aef90ecebe60a0b3fdf1e0d05c1c12d4b033

2. "Addendum to GPT-6 Astra System Card: GPT-6.1 Sol" (published 2026-09-29)
   - URL: https://deploymentsafety.openai.com/gpt-6-1-sol
   - Cached: raw/gpt-6-1-sol.html
   - sha256: 683f73b7efdc4fe5e6a034239f0edc2cf5b569b202986f6ffb0afa7697304ab7

Also cached for reference (not ingested): the GPT-6 Astra card
(raw/gpt-6-astra.html, sha256 86caeff0...) and the hub index
(raw/index.html, sha256 95bfa23a...).

## Extraction

Text extracted from HTML by stripping script/style tags and HTML markup.
Section content pulled from `data-section-slug` anchors. Behavior
descriptions preserve source wording where practical. All evaluative
statements graded OBSERVED (direct quotes) from the reports themselves.

## Records

22 records, all tagged {"lane": "openai-intel"}:
- 1 source (OpenAI Deployment Safety Hub)
- 2 intel.report (one per card)
- 9 intel.behavior (4 from October card, 5 from 6.1 Sol addendum)
- 9 graded claims (OBSERVED, citing report observations)
- 1 run record
