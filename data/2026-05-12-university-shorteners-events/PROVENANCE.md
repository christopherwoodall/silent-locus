# university-shorteners-events — PROVENANCE

Explicit-events re-explosion of the university-shorteners family
(Christopher's explicit-events rule: no consolidation in primary indexes;
every observable event is its own doc).

Built: 2026-09-28T18:22:27Z (UTC), generator scripts/build_shortener_events.py (read-only,
offline re-parse of existing evidence captures; no live fetching;
hosted-Elastic writes paused — staged on disk for the local-push script).

## Sources (untouched)

- data/2026-09-28-university-shorteners/raw/goto-unm-edu/{7t6-o,discvr,reso,urphy21}_referrer_urls_daily_2026-09-28.json
- data/2026-09-28-university-shorteners/raw/u-ethz-ch/nB1nv_referrer_urls_daily_2026-09-28.json
- data/2026-09-28-university-shorteners-batch2/raw/goto-unm-edu/vbudg_stats_2026-09-28.txt (control)
- data/2026-09-28-university-shorteners-batch3/raw/go-uvm-edu/{-4s0q,tgmtq,xc26}_stats_2026-09-28.txt (UVM controls)
- data/2026-09-28-university-shorteners/raw/url-popcat-xyz/{5vtSk2RG2f,IRZTIxDlZ}_info_2026-09-28.txt

## Supersedes

The 16 consolidated docs currently in the `university-shorteners` hosted
index (record_kind yourls_stats_page / yourls_stats_detail /
shortener_info_page, one doc per stats page) are earmarked for the support
index `university-shorteners-rollup`. The per-event docs in
university-shorteners-events.jsonl are their replacement in the primary
index. labels.event_id is deterministic for idempotent loads.

## Caveats

- YOURLS all-time daily series is decimated (~6-week sampling, includes
  zero-hit days); last-30-days series is full resolution.
- Per-day tables for 2026-07-05/06 are structurally unpullable from the
  YOURLS public UI (no per-day drill-down) — recorded, not retried.
- UVM referrers are owner-only (NetID login); only traffic + location rows
  exist for go.uvm.edu.
- retrieved_at for txt-parsed sources is normalized from the capture-time
  note in the file header (CDT = UTC-5); the raw string is not retained.

## Schema backfill 2026-09-29

`university-shorteners-events.jsonl` (1,522 records) brought to full
conformance via `temp/backfill_w4.py`. Existing `@timestamp`, `event`
(dataset `university-shorteners` — this file feeds the
`university-shorteners` index, distinct from the rollup files), and
`record_kind` kept verbatim — additive only.

- **record_kind**: unchanged (`yourls_referrer_url` 1,188,
  `yourls_daily_hits` 308, `yourls_stats_page` 13, `yourls_country_hits` 13).
- **fingerprint**: added (was missing). Identity string:
  `labels.event_id` (e.g. `yourls:goto.unm.edu:7t6-o:refurl:48efafc811ab`),
  verified present and unique on all 1,522 rows.
- **labels**: `best_day` nested object flattened to `best_day.<field>`
  dotted keys (3 records). No other nesting; no invalid label keys.

## File-pointer rewrite 2026-09-29

All 1,522 rows carried a stale top-level `file` pointer under the
pre-migration `data/university-shorteners[-batchN]/...` tree (sources were
moved into `raw/` by the 21312cf migration without rewriting pointers).
Rewritten 1,522 / dropped 0.

Each pointer was relocated by basename search across the repo and verified
byte-for-byte against the row's own `sha256` + `size_bytes` before the
rewrite — no ambiguities, no unverifiable pointers:

- `data/2026-09-28-university-shorteners/raw/goto-unm-edu/{7t6-o,discvr,reso,urphy21}_referrer_urls_daily_2026-09-28.json` — 1,407 rows
- `data/2026-09-28-university-shorteners/raw/u-ethz-ch/nB1nv_referrer_urls_daily_2026-09-28.json` — 90 rows
- `data/2026-09-28-university-shorteners/raw/url-popcat-xyz/{5vtSk2RG2f,IRZTIxDlZ}_info_2026-09-28.txt` — 2 rows
- `data/2026-09-28-university-shorteners/raw/wayback/IRZTIxDlZ/IRZTIxDlZ_referrer_urls_daily_wayback_{20260512030438,20260908215028}.json` — 2 rows
- `data/2026-09-28-university-shorteners-batch2/raw/goto-unm-edu/vbudg_stats_2026-09-28.txt` — 5 rows
- `data/2026-09-28-university-shorteners-batch3/raw/go-uvm-edu/{-4s0q,tgmtq,xc26}_stats_2026-09-28.txt` — 16 rows

Only the top-level `file` value changed; every other field byte-identical
(line-level round-trip checked). SHA256SUMS regenerated.

## raw/-missing exception 2026-09-29

2026-09-29: no raw/ layer — derived explicit-events re-explosion: all 1,522
events were parsed offline from existing captures held in sibling raw/ layers
(data/2026-09-28-university-shorteners/raw/, -batch2/raw/, -batch3/raw/);
this collection holds no own captures. Verified: no raw/ files ever committed
in git history; no stray evidence files on disk; SHA256SUMS green. Ratified as
a canonical-layout exception.
