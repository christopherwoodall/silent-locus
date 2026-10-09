# Provenance — osv

## Source and method (from notes/)

Hunt lanes 19 and 20, 2026-09-27/28. Read-only, paced (~1 req/s), no auth.

- **Lane 19 (OSV.dev / GitHub advisories)** — `notes/gem-hunt-osv-2026-09-27.md`:
  OSV API `POST /v1/query` for 42 campaign package names (7 GemStuffer `MAL-*`
  hits, all published 2026-07-07); `GET /v1/vulns/GHSA-9j48-x3c3-mrp2` (Fastly
  advisory — 404, not in OSV); GitHub Advisory API
  `GET /advisories?ecosystem=rubygems&type=malware` — 3,000 advisories pulled
  across 30 pages with incremental saves and retry/backoff, classified into
  1,687 GemStuffer-shaped vs 1,310 other-campaign names. Products:
  `ghsa_rubygems_malware.json`, `ghsa_gemstuffer_batch_names.txt`,
  `ghsa_gemstuffer_classified.json` (incl. the 1,284-name `gs_not_in_corpus`
  sweep list), `osv_pkg_results3.json`.
- **Lane 20 (Diffend sweep)** — `notes/gem-hunt-diffend-sweep-2026-09-27.md`:
  `scripts/diffend_sweep.py` over the 1,284 advisory-named campaign gems
  absent from the local corpus. 394 found in Diffend (all May-segment,
  first-publish 2026-05-11 19:40 → 2026-05-12 07:47 UTC), 218 confirmed
  absent, 672 unconfirmed due to connection failures. Products:
  `diffend_sweep_results.jsonl` (1,284 rows), the retry pass
  `diffend_sweep_results_retry.jsonl`, and run logs `diffend_retry.log` /
  `sweep-stdout-relaunch.log`.

OSV/diffend sweep results over rubygems package names: for each candidate
name, whether it appears in diffend (`in_diffend`), HTTP status, version
list with publish timestamps (`versions`), first publish timestamp
(`first_publish`), mechanism notes, and name-grammar classifications.
`diffend_sweep_results_retry.jsonl` is a retry pass (`retry_pass: true`,
`fetch_client`) over a subset of the same names. See `diffend_retry.log`
and `sweep-stdout-relaunch.log` for run logs.

## Schema backfill 2026-09-29
- Transform: `temp/backfill_w2.py`. Pre-schema flat records brought onto the
  shared schema. `name` -> `labels.gem.name`; `first_publish` ->
  `labels.first_publish_raw` (original non-ISO string preserved verbatim);
  all other fields -> `labels` unchanged. `versions` (array of
  `{version, ts}` objects) flattened losslessly into two parallel scalar
  arrays `labels.versions.version` / `labels.versions.ts` per the ECS labels
  rule (no nested arrays).
- `@timestamp` = parsed `first_publish` ("%b %d, %Y %H:%M", assumed UTC ->
  Z); `labels.timestamp_source = "labels:first_publish_raw"`. Records with
  no first_publish (in_diffend=false): sentinel `1970-01-01T00:00:00Z` +
  `labels.timestamp_source = "fallback:no_recoverable_date"`.
- record_kind: `diffend_harvest` when `in_diffend` is true, else
  `sweep_negative` (both pre-existing registry kinds).
- fingerprint identity string: `sha256(gem.name + "|" + pass)` where pass is
  `initial` for diffend_sweep_results.jsonl and `retry` for
  diffend_sweep_results_retry.jsonl (gem names repeat across the two files;
  the pass disambiguates).
- event.dataset = `osv`; event.created = backfill run time.

## Canonical layout migration (2026-09-29)

Concatenated 2 event shards (osv-diffend-sweep-results-retry.jsonl, osv-diffend-sweep-results.jsonl) into `events.jsonl` in sorted-filename order (1956 records; count verified against inputs). Each record gained `labels.file_origin` = original shard basename; no other fields changed. Source shards removed after verification. file_origin preserves the initial/retry pass identity that the fingerprint identity string encodes.

## Notes-farm addition (2026-09-29, notes-farm worker)

9 new records appended to `events.jsonl` from
`notes/gem-hunt-osv-2026-09-27.md`:

- 7 `osv_advisory`: MAL/GHSA advisory IDs for campaign gems
  (zzjinavcsgit MAL-2026-9952, zzjinavcsbzr MAL-2026-9950, probejiqptzco
  MAL-2026-8427, uxjinalamb2 MAL-2026-9062, wandsworthprobe1778551714
  MAL-2026-9296, prx1b49033905 MAL-2026-8456, trya1zz MAL-2026-9003).
- 1 `sweep_negative`: July-7 XSS/SSTI wave has zero advisories anywhere.
- 1 `finding`: GHSA-9j48-x3c3-mrp2 (RubyGems CDN cache API-key leak).

No pre-existing advisory-ID records in this collection. Validation: 0
violations. SHA256SUMS regenerated.
