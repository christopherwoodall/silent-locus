# xss-ssti-census lane: readiness before ingest

Date: 2026-10-09. Author: readiness check. Status: PRE-INGEST.

## 1. What the source is

- File: `data/lanes/xss-ssti-census/events.jsonl` (122 events, 146,357 bytes).
- Integrity: SHA256SUMS passes. Hash `9bac6e9cb629cc5b1ca504f668cf38d43cf69af6b02ed70f00ca00c84dc0c619` matches.
- No duplicate `payload_id` values inside the file (122 unique).
- Composition: 113 XSS events, 9 SSTI events. `windowname-svg-onload` is the largest family (82 events, tier A).
- No records for this lane exist in `data/records/` yet. Ingest has not started.

## 2. Quality flags (not blockers)

- 117 of 122 events have no `first_seen` value. Use `timestamp_source` fallback `no_recoverable_date`.
- 40 of 122 payload texts carry the upstream shortener URL in redacted form. This is a pre-existing corpus-build redaction (accepted 2026-09-29). Provenance for those 40 is degraded. Keep them anyway.

## 3. Schema gap: needs a decision

The `infra.ioc` type (factum-infra pack 1.0.0) needs `term` and `category`. The events do not carry these fields directly.

Proposed mapping:

- `term` <- `labels.text`, or `labels.markers_present` when text is absent.
- `category` <- payload family from the URL pattern, or `labels.marker` when absent.
- `provenance` <- `labels.source_ref`.

The extractor cannot do a valid ingest until the coordinator confirms or overrides this rule.

## 4. Dedup check: 21 july7 overlaps are complementary, not dupes

- 21 of the 22 `july7-gem-wave` events in this lane match gem names already ingested by the `july7-wave` lane (checked against `evidence/remove-2026-07-07-july7-wave/raw/diffend_sweep_results_july7.jsonl`, 264 names).
- Same pattern as the `july7-gem-forensics` lane: these are payload-mechanism records, not package records. They complement the package records.
- Proposed treatment: ingest them as complementary records, edged to the july7-wave counterparts (same as the 7 gem-forensics records). Do not skip them wholesale.
- One genuinely new probe gem: `proxssrfetviqtfb` (proxy_name grammar). It has no counterpart.

## 5. Novelty: artifactory-board markers

These markers appear in the lane events but not in the current corpus:

- `packages.hub.ace-research.openai.org` — 100 hits in the new events, zero hits in `data/records/`.
- `zz-label:zzMODALFUNC42536108RUN42` — only in the new events.

This is the strongest new IOC content in the lane. Note: the `github-remote-cache/zz` Artifactory board path is the hunt's strongest known cross-corpus link.

## 6. Decisions needed from the coordinator

1. Confirm or override the `term` / `category` mapping in section 3.
2. Confirm the dedup treatment in section 4 (ingest 21 overlaps as complementary, edged to july7-wave).
