# Provenance — 2026-05-11 OSV sweep

## Collection (2026-09-27/28)

Carried over from `evidence/2026-05-11-osv/PROVENANCE.md` (legacy,
kept verbatim in the renamed directory).

Hunt lanes 19 and 20. Read-only, paced (~1 req/s), no auth.

- **Lane 19 (OSV.dev / GitHub advisories)** — `notes/gem-hunt-osv-2026-09-27.md`:
  OSV API `POST /v1/query` for 42 campaign package names (7 GemStuffer
  `MAL-*` hits, all published 2026-07-07); `GET /v1/vulns/GHSA-9j48-x3c3-mrp2`
  (Fastly advisory — 404, not in OSV); GitHub Advisory API
  `GET /advisories?ecosystem=rubygems&type=malware` — 3,000 advisories pulled
  across 30 pages with incremental saves and retry/backoff, classified into
  1,687 GemStuffer-shaped vs 1,310 other-campaign names.
- **Lane 20 (Diffend sweep)** — `notes/gem-hunt-diffend-sweep-2026-09-27.md`:
  `scripts/diffend_sweep.py` over the 1,284 advisory-named campaign gems
  absent from the local corpus. 394 found in Diffend (all May-segment,
  first-publish 2026-05-11 19:40 → 2026-05-12 07:47 UTC), 218 confirmed
  absent, 672 unconfirmed due to connection failures. Retry pass
  `osv-diffend-sweep-results-retry.jsonl` re-checked a subset of names.

## Schema backfill (2026-09-29)

Transform `temp/backfill_w2.py` brought pre-schema flat records onto the
shared schema. `name` → `labels.gem.name`; `first_publish` →
`labels.first_publish_raw` (original non-ISO string preserved verbatim).
`@timestamp` = parsed `first_publish` ("%b %d, %Y %H:%M", assumed UTC);
records with no first_publish got sentinel `1970-01-01T00:00:00Z`.
`record_kind`: `diffend_harvest` when `in_diffend` true, else
`sweep_negative`. Fingerprint identity: `sha256(gem.name + "|" + pass)`.
Legacy `events.jsonl` concatenated from the two sweep shards; 9
notes-farm records appended (7 `osv_advisory`, 1 `sweep_negative`,
1 `finding`).

## Factum ingest (2026-10-10)

Bundle `lane-ingest-2026-05-11-osv-b1`, actor
`agent:lane-ingest:2026-05-11-osv`. 1,965 legacy events → 1,303 Factum
records (1,290 `infra.package` observations merged per gem across both
sweep passes; 7 UPSTREAM advisory claims; 1 OBSERVED negative-sweep
claim + run; 1 `intel.report`; 2 sources; 1 Diffend run).

Dedup: one gem (`slvhg151`) already existed as `infra.package` from the
webhook-deaddrops lane with richer provenance (Diffend page + webhook
deaddrop) — its legacy rows were skipped, not re-ingested. Exact-name
lookup plus full-corpus substring check found no other overlaps.

`observed_at` grounding: Diffend-present gems use the parsed
`first_publish` (`time_basis: source_metadata`); absent gems use the
documented 2026-09-27/28 lane-run window end (`time_basis:
legacy_documented`), noted in each record's provenance. No `in_lane`
edges submitted during ingest.
