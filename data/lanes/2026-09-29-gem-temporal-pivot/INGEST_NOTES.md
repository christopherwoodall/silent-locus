# Ingest notes — 2026-09-29-gem-temporal-pivot

## Record type

`infra.package` (urn:factum:infra:package:1), one observation per
events.jsonl row (3,027). `name` is the verbatim gem name (the IOC),
`ecosystem` = rubygems, `versions` = plain version strings in source order.
Full version/date objects are preserved losslessly in
`tags.versions_detail` (canonical JSON). Probe outcome lives in tags:
`in_diffend`, `http_status` (raw value), `redirect_target`,
`probe_ok`/`probe_error`, `file_origin`.

## Timestamps

Rows carry no recoverable probe time (`timestamp_source =
fallback:no_recoverable_date`). `observed_at` is the documented sweep-leg
date (2026-09-28 for the targeted-check and phase-1 sweep; 2026-09-29T12:03Z
for the resume-leg completion per the run log), `time_basis =
legacy_documented`. The precision limit is recorded per row in
`tags.observed_at_note`.

## Two-pass names

`attacker-xss-admin-1` and `xssname-1783397821` were probed twice
(2026-09-28 targeted-check: connection failure; 2026-09-29 resume leg:
success with version dates). Kept as two distinct observations per the
keep-all policy, annotated with `duplicate_phase_note`. Nothing is dropped:
both passes are queryable. This satisfies the 2026-10-10 multi-row lesson
(no pass may be silently dropped).

## Overlap

14 gem names also appear in other lanes (webhook-deaddrops,
2026-03-07-march7-rce-modality, 2026-08-10-wayback-gem-capture). Those are
distinct sightings in different sweeps, so all rows are kept; the overlap
is annotated in `tags.also_observed_in_lane`.

## Edges

No edges submitted during ingest. No `in_lane` edges exist.

## Batches

7 bundles, idempotency keys `gem-temporal-pivot-ingest-p1..p7-of-7-v1`.
Batch dirs (data/records/):
22f24a1a36064ad18acdb1afe52729c7, c6ca57b5febf4b0597a3487f784ce814,
ebd9378bd8194000890136bfcb7eeb83, 054547a1ff5c4886b6f3781906c45c84,
3b049bbd929742a98d5ccf0d7c96e269, 86ff992a65d94c11a5b99108a976b769,
ab903879734243b99fc115084e17fcf3.
Each bundle carries one source record; all 7 got the lane tag via
`factum update` after submit (the bundle builder did not tag sources).

## Validator

/tmp/gem-temporal-pivot-bundles/validate_ingest.py re-derives expectations
from events.jsonl independently: 1:1 row-to-observation mapping, verbatim
names, versions/version-detail fidelity, census (2251/774/2 in_diffend
split, 3 out-of-window, 14 overlaps, 2 probe failures), zero edges.
Result: PASS, 0 failures.
