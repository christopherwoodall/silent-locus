# DONE.md — Wikipedia top-500 infra scan (2026-10-06)

**Status: COMPLETE.** Branch `wikipedia-top500-infra-scan-2026-10-06` pushed to origin. Main untouched.

## What was done

1. **Top-500 list**: September 2026 pageviews API → 489 main-namespace articles (+11 non-articles excluded; rank 433 duplicated). Cached in `raw/`.
2. **Range files**: AWS, Azure (live ServiceTags 2026-10-05), GCP, OpenAI/Anthropic/Perplexity bot ranges → **73,818 validated CIDR→provider records** in `raw/cidr-provider-map.jsonl`, each with provenance.
3. **Revision pull**: 489 per-article JSONL files, **677,635 revisions**, 2020-01-01 → 2026-10-07, curl-only, ≤1 req/5s, across 12 chunk pullers + 3 repull workers (74 files lost to VM storage flakiness, recovered).
4. **Completeness audit**: 100% API-ground-truth verified by 4 audit workers — every file's oldest timestamp matches the live API's oldest in-window revision. 3 defects caught and repaired.
5. **Matcher**: IP editors extracted (61,179 = 9.03%; temp 21,922 = 3.24%; named 594,534 = 87.74%), joined against the CIDR map via bisect lookup → 90 initial hits (aws 62, azure 28).
6. **Metrics-analyst**: per-provider tables, current-vs-reverted sample (4/8/3 of 15), content characterization.
7. **Reviewers** (kill-or-fix authority):
   - **Reviewer-1 (attribution): KILLED all 90.** Range currency — every hit's CIDR entered the provider feed 1–6 years after the edit; 0/67 IPs in any edit-contemporaneous provider range. Cached 19 historical Wayback range snapshots (`raw/history/`) as evidence. Corrected match count: **0**.
   - **Reviewer-2 (methodology): KILLED the AI-agent headline claim.** IP visibility is 0% in 2026; the method is blind to the agent era by construction.

## Final verdict

**Zero verified datacenter-infra edits attributable to any provider — and zero attributable to any AI lab — in the visible history of the top-500 articles.** Clean, reviewed negative.

- Zero matches on any AI-lab-published range across 677,635 revisions.
- Zero provider-range matches among the 22,190 agent-era (2024–2025) IP-visible revisions.
- The 90 pre-kill candidates were ordinary human IP editing (mobile tags, vandalism, reverts) with no automation-shaped metadata — and their attributions were false positives from matching 2020–2023 edits against 2026 range maps.
- Honest limits documented in SCAN-SUMMARY.md: temporal blindness, the colocation blocklist purging the target population, range-currency false positives, thin lab-egress coverage, selection bias, data-quality notes.

## Deliverables (all in the event dir, committed + pushed)

- `SCAN-SUMMARY.md` — verdict, per-provider table, limits, clean negatives, killed-by-review appendix
- `workers/IOCS.md` — no surviving IOCs; killed-by-review appendix; candidate leads for future work
- `raw/` — article lists, CIDR map + source files, 489 revision JSONLs, ip-matches.jsonl (90 pre-kill evidence), article-aggregates.tsv, history/ (19 Wayback snapshots + provenance)
- `workers/` — per-worker FINDINGS.md (list-builder, range-curator, 12 pullers, 3 repull, 4 audit, matcher, metrics-analyst, reviewer-1, reviewer-2)
- `PROVENANCE.md` — event provenance

## Operational lessons (for the manual)

1. **Ghost workers**: "errored" runtime reports can mean "still running detached" — build resume logic with content verification, not existence checks.
2. **Storage flakiness**: this VM silently loses file writes in bursts; write temp+fsync+atomic-rename and verify on-disk content, never trust in-memory counts.
3. **Range currency**: matching historical events against current infra feeds is a guaranteed false-positive machine — always bracket with edit-contemporaneous sources.
4. **Worker hygiene**: some workers pushed to the branch despite instructions; verify branch state before pushing.

## Open threads (not this scan's job)

- Temp-account clustering for the agent era (the wikipedia-edit-hunt lane's current direction) — this scan's method can't reach it.
- The rank-222 redirect ("european election 2014" → "2014 European Parliament election"): re-pull with `redirects=1` if the target article should be covered.
