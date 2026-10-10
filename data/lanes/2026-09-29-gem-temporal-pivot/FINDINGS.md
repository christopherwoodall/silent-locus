# Findings — 2026-09-29-gem-temporal-pivot

## Verdict: clean negative (OBSERVED)

3,025 RubyGems names swept for version dates on Diffend, 2026-09-28/29.
2,251 present with version dates; 756 absent (302 to gems index); 18 fetch
failures recorded honestly, not refetched. The hunt's verdict stands: no
temporal-pivot signal beyond the documented notes.

## Out-of-window versions (OBSERVED)

3 gems have versions dated outside 2026-05-05–2026-07-07:

- `lambethcalcqzewgt` — 0.0.4, 99.0.0 @ 2026-09-12T01:42:00
- `test_gem_kangaroo` — 0.0.5, 0.0.9 @ 2026-07-13T07:32:00
- `wanproxyq` — 0.0.2, 0.0.5 @ 2026-09-08T09:37:00

See `tags.out_of_window_detail` on their observations.

## Cross-lane names (OBSERVED)

14 swept names also appear in other lanes (webhook-deaddrops,
2026-03-07-march7-rce-modality, 2026-08-10-wayback-gem-capture); annotated
via `tags.also_observed_in_lane`. Same battery names recur across sweeps;
not evidence of a new campaign.
