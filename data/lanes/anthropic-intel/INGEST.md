# INGEST.md — anthropic-intel

Ingested into Factum 2026-10-10 (UTC) on branch factum-shaping.
Factum lane: `anthropic-intel` (lane_709b7d2a944b461ead63394e35713ad4).
Batch: 53886de8135e4968896f5b3f075164c7.

## Records (10 total, all tagged {"lane": "anthropic-intel"})

- 1 `intel.report`: the Anthropic report "Investigating unintended model
  actions" (2026-10-09).
- 4 `intel.behavior`: software-flaw-exploitation, unauthorized-form-submission,
  restriction-circumvention, url-shortener-abuse.
- 4 `intel.ttp`: sql-injection-via-url, token-extraction-from-client-config,
  url-shortener-abuse, form-auto-submission.
- 1 `source`: the report URL.

No edges created during ingest (separate pass). Author auto-stamped by Factum.
No blobs: no bytes were captured in this lane (raw/ is empty).

## Dedup

`match --text --mode fuzzy` on all 7 candidate identifiers before submit.
Six had zero matches. `url-shortener-abuse` had 2 pre-existing records in
lane `2026-09-28-worldpoverty-task-family` — they describe page-slot reuse,
not fetch-tool bypass. Not duplicates. `seen_before` empty on submit.

## Cleaner — PASS

Checked live records after submit: lane tag on all 10, severity enum valid,
no duplicate key fields in batch, no edge records, no manually set
factum.* tags. One fix applied via `factum update` (metadata only): the
source record was missing the lane tag; added {"lane": "anthropic-intel",
"basis": "upstream"}.

## Adversarial validator — CONDITIONAL-PASS

- A1 category collision (url-shortener-abuse vs worldpoverty records): PASS.
- A2 title source: FLAG. The report title is derived from the URL slug, not
  a fetched page <title>. Kept as a documented inference; provenance cites
  the URL.
- A3 evidence scope: PASS. Behavior examples (Haiku 4.5, da.gd, Mythos)
  come from docs/taxonomy/behavior-categories.md, which cites the same
  report. No contradiction found.
- A4 severity basis: PASS. Severity is an analyst assessment (INFERENCE),
  tagged basis=upstream.
- A5 dedup coverage: PASS.
- A6 no edges at ingest: PASS.
- A7 timestamps: PASS. No invented event times.

## Provenance chain

- Legacy: evidence/remove-2026-10-09-anthropic-intel/ (events.jsonl,
  build_events.py, legacy-PROVENANCE.md — original files unchanged).
- Source: https://www.anthropic.com/research/investigating-unintended-model-actions
