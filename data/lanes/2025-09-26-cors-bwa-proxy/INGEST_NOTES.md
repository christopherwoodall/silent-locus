# Ingest notes — 2025-09-26-cors-bwa-proxy (standard)

## Record mapping (legacy record_kind -> Factum type)

| legacy kind (count) | Factum type (count) | note |
|---|---|---|
| proxied_target (113) | infra.proxy_chain (47) | 66 skipped: same proxied URL already in corpus as infra.proxy_chain (lane 2026-10-01-intermediary-relays) |
| proxy_ladder (29) | infra.proxy_chain (29) | aggregate edges; target_url is the destination host |
| proxy_family (6) | infra.proxy_instance (5) | r.jina-ai.workers.dev skipped: already in corpus |
| venue_summary (6) | 6 claims on run | venue coverage counts |

Total submitted: 86 records (81 observations, 1 source, 1 run, 3 claims).
Skipped: 67 (drop_log.json).

## Field conventions

- `target_url` = the proxied URL exactly as observed (verbatim
  `matched_string`, schemeless as captured, e.g.
  `cors.bwa.workers.dev/da.gd/sndagentma`). The decoded destination is in
  `tags.decoded_target`.
- `chain` = legacy `chain_layers` (e.g. `["cors.bwa.workers.dev", "da.gd"]`).
- `observed_at` = legacy `incident_ts`, `time_basis` = `source_metadata`.
  Ladder/family rows: `observed_at` = 2026-09-28 (analysis date),
  `time_basis` = `legacy_documented`.
- proxy_instance `invocation_shape` generalized from
  `raw/other_workers_dev_hostnames.json` `sample_raw` (passive sweep; no
  live probing, so `access` = `unknown` and `live` omitted).

## Dedup (pre-ingest, against exported batches)

URL-variant match (triple percent-decode, scheme strip, wrapper-host strip,
inner-URL strip) over all corpus `infra.proxy_chain` target_urls; exact host
match for `infra.proxy_instance`. 66 proxied_target rows collide with
2026-10-01-intermediary-relays chains (same urlquery-scan evidence, wrapped
URL form); 1 proxy_family host collides with an existing proxy_instance.
Skipped per the pre-ingest dedup rule; every skip is in drop_log.json with
its legacy fingerprint.

## Overlap

Sibling lane 2026-10-01-intermediary-relays already covers 66 of the 113
proxied URLs (ingested 2026-10-10 from sweep samples over the same corpora).
The 47 submitted here are genuinely new targets. The 29 ladder aggregates
and 5 family instances are new aggregate evidence.

## Edges

No edges submitted during ingest.

## Batches

One bundle, idempotency key `2025-09-26-cors-bwa-proxy-v1` (86 records).

## Validator

`validate_bundle.py` — independent re-derivation from events.jsonl
(kind counts, own dup-set recompute matched by legacy fingerprint: 47/66
exact), bundle structure, schema-required fields, verbatim spot-checks.
PASS.
