# Ingest notes — 2026-09-28-gem83-reconciliation (standard)

## Record mapping

83 `gem_reconciliation` rows -> 83 `infra.package` observations (1:1).
No rows skipped.

## Field conventions

- `name` = legacy `gem.package` (verbatim, e.g. `a----00proxy38998`);
  `ecosystem` = `rubygems`; `versions` = [`gem.versions`];
  `xray_id` = legacy `gem.xray_id`;
  `provenance` = `2026-09-28-gem83-reconciliation
  (nightingale-collective gem83-reconciliation-ingest)`.
- `observed_at` = 2026-06-18 (june-18 wave date, inferred from name grammar
  + JFrog/thecolony.ai reports per legacy `timestamp_source`);
  `time_basis` = `legacy_documented`.
- Reconciliation evidence (wave, name_family, identification_source,
  wayback recovery status, wiki gem-bridge) in tags.

## Dedup / overlap (the notable decision)

All 83 gem names already exist in Factum as `infra.package` in lane
2026-09-29-gem-temporal-pivot. They were NOT skipped: the existing records
carry the Diffend temporal-sweep pass (in_diffend=false, versions empty),
while these rows carry the reconciliation pass (JFrog Xray IDs, versions
0.0.1, june-18 wave, wayback recovery status, wiki gem-bridge info).
Per the multi-pass rule every pass's evidence is kept; the overlap is
annotated in `tags.also_observed_in_lane`, and the corpus_overlap claim
documents the distinction. No duplicate evidence is created -- the two
record sets describe different analysis passes over the same gems.

## Edges

No edges submitted during ingest.

## Batches

One bundle, idempotency key `2026-09-28-gem83-reconciliation-v1`
(87 records: 83 observations, 1 source, 1 run, 2 claims).

## Validator

`validate_bundle.py` — 83 rows / 83 unique names, name-set equality
against legacy, xray_id/version passthrough spot-checks, required fields.
PASS.
