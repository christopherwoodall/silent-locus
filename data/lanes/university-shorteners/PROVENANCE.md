# university-shorteners-events — PROVENANCE

Explicit-events re-explosion of the university-shorteners family
(Christopher's explicit-events rule: no consolidation in primary indexes;
every observable event is its own doc).

Built: 2026-09-28T18:22:27Z (UTC), generator scripts/build_shortener_events.py (read-only,
offline re-parse of existing evidence captures; no live fetching;
hosted-Elastic writes paused — staged on disk for the local-push script).

## Sources (untouched)

- evidence/2026-09-28-university-shorteners/raw/goto-unm-edu/{7t6-o,discvr,reso,urphy21}_referrer_urls_daily_2026-09-28.json
- evidence/2026-09-28-university-shorteners/raw/u-ethz-ch/nB1nv_referrer_urls_daily_2026-09-28.json
- evidence/2026-09-28-university-shorteners-batch2/raw/goto-unm-edu/vbudg_stats_2026-09-28.txt (control)
- evidence/2026-09-28-university-shorteners-batch3/raw/go-uvm-edu/{-4s0q,tgmtq,xc26}_stats_2026-09-28.txt (UVM controls)
- evidence/2026-09-28-university-shorteners/raw/url-popcat-xyz/{5vtSk2RG2f,IRZTIxDlZ}_info_2026-09-28.txt

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

- `evidence/2026-09-28-university-shorteners/raw/goto-unm-edu/{7t6-o,discvr,reso,urphy21}_referrer_urls_daily_2026-09-28.json` — 1,407 rows
- `evidence/2026-09-28-university-shorteners/raw/u-ethz-ch/nB1nv_referrer_urls_daily_2026-09-28.json` — 90 rows
- `evidence/2026-09-28-university-shorteners/raw/url-popcat-xyz/{5vtSk2RG2f,IRZTIxDlZ}_info_2026-09-28.txt` — 2 rows
- `evidence/2026-09-28-university-shorteners/raw/wayback/IRZTIxDlZ/IRZTIxDlZ_referrer_urls_daily_wayback_{20260512030438,20260908215028}.json` — 2 rows
- `evidence/2026-09-28-university-shorteners-batch2/raw/goto-unm-edu/vbudg_stats_2026-09-28.txt` — 5 rows
- `evidence/2026-09-28-university-shorteners-batch3/raw/go-uvm-edu/{-4s0q,tgmtq,xc26}_stats_2026-09-28.txt` — 16 rows

Only the top-level `file` value changed; every other field byte-identical
(line-level round-trip checked). SHA256SUMS regenerated.

## raw/-missing exception 2026-09-29

2026-09-29: no raw/ layer — derived explicit-events re-explosion: all 1,522
events were parsed offline from existing captures held in sibling raw/ layers
(evidence/2026-09-28-university-shorteners/raw/, -batch2/raw/, -batch3/raw/);
this collection holds no own captures. Verified: no raw/ files ever committed
in git history; no stray evidence files on disk; SHA256SUMS green. Ratified as
a canonical-layout exception.

## Common Crawl stats-page capture 2026-09-29

Lane-12 shortener-cc sweep (`hidden_files/lane12/shortener_cc_sweep.py`,
queued 2026-09-28 by the July-5-6 UNM retry lane): exact-URL CC index queries
over the crawls intersecting 2026-06-01..2026-08-15 (CC-MAIN-2026-25, -30,
-34) for the 5 goto.unm.edu `+` stats pages, http/https variants — 30 queries
total, polite 2s pacing, read-only.

Result: 29/30 queries returned zero captures. The single hit was
`http://goto.unm.edu/discvr+` in CC-MAIN-2026-34, capture 2026-08-17T05:11:48Z
— 65,448 bytes of genuine YOURLS stats HTML ("Statistics for
https://goto.unm.edu/discvr"), parsed to 68 referrer-URL rows across 24 hosts.
No mid-July 2026 capture of any target exists in Common Crawl
(CC-MAIN-2026-30, the July 10–23 crawl, returned zero for all 10 URLs), so the
July 5–6 per-referrer rows remain unrecoverable from this backend — recorded
as a clean negative, not retried.

Merge: 69 exploded docs (68 `yourls_referrer_url` + 1 `yourls_stats_page`
page-observation for the 2026-08-17 capture), deduped on `labels.event_id`
against the 1,522 existing rows — 45 new, 24 skipped as duplicates. The 44
new referrer rows are URLs present in the August referrer table but washed
out of the 2026-09-28 all-time table (api.census.gov API-key queries,
allorigins-laundered sec.gov fetch, 2dd.pl, heyzine, TESTREF/TESTRR canaries).

Evidence staged at
`evidence/2026-09-28-university-shorteners/raw/wayback-cc/discvr/`
(`CC-MAIN-2026-34_20260817051148.html` raw WARC payload +
`discvr_referrer_urls_daily_cc_CC-MAIN-2026-34_20260817051148.json` evidence
JSON, SHA256SUMS + manifest.json regenerated after relocation). The script's
docstring staging path (`data/university-shorteners/wayback-cc/`) was
relocated to the normalized raw/ layer (sibling of `evidence/2026-09-28-university-shorteners/raw/wayback/`); its
events-JSONL append step targets the pre-normalization collection path and
was superseded by this merge — no parallel collection created, no
duplicates committed.

Worker note: the sweep could not run unmodified — Python's `http.client` is
systematically cut off by the egress proxy on index.commoncrawl.org
(IncompleteRead at ~16KB / RemoteDisconnected on every attempt, all header
combos; curl succeeds reliably), so `fetch()` now shells to curl. Same
signature, retry/backoff kept, output conventions unchanged.

## Wayback stats-page slice 2026-09-29 (one-shot; polling loop killed)

Christopher's decision 2026-09-29: kill the standing 15-min CDX polling loop
(`hidden_files/shortener-cdx/shortener_cdx_retry.sh`, already dead — left
dead), but run its queued work ONE final time now that the CDX backend
recovered. One-shot script: `/tmp/wayback_oneshot_2026-09-29.py` (ephemeral;
logic copied from `hidden_files/shortener-cdx/pull_and_explode.py` with
paths corrected for the normalized tree).

Method: CDX `url=<stats_url> output=json fl=timestamp,original,statuscode,digest
filter=statuscode:200 collapse=digest` for all 12 stats URLs (5 goto.unm.edu,
u.ethz.ch, 2 url.popcat.xyz, 3 go.uvm.edu, vanderbi.lt), 2s polite pacing,
urllib primary with curl fallback, read-only. Raw HTML kept per capture
(capture-first) at `evidence/remove-2026-05-12-university-shorteners-events/raw/wayback/<slug>/`
plus per-capture evidence JSONs (`<slug>_referrer_urls_daily_wayback_<ts>.json`),
`manifest.json` + `SHA256SUMS` regenerated in `evidence/remove-2026-05-12-university-shorteners-events/raw/wayback/`. Parsed with the
same table-row extractor; exploded via `scripts/build_shortener_events.py`
(`vanderbi.lt` monkeypatched locally as Vanderbilt University / university —
the canonical script lacks that instance entry).

Result: 12 targets, 19 captures seen, 17 downloaded (2 IRZTIxDlZ captures
already held in `evidence/2026-09-28-university-shorteners/raw/wayback/` — not
duplicated). 57 docs exploded from 17 evidence files — **24 new rows
appended** (1,567 → 1,591), 32 skipped as duplicates on `labels.event_id`,
1 within-batch dup skipped. New rows: 16 `yourls_stats_page`
page-observations + 8 `yourls_referrer_url` rows (all 8 from the 2026-09-06
u.ethz.ch/nB1nv capture; 26 of its 34 parsed rows already existed).

Notable: `goto.unm.edu/discvr+` has deep Wayback history (2019-09-17 through
2026-01-14, 9 captures) — all page-observations are new, none carried
referrer rows the dataset lacked. `go.uvm.edu/-4s0q+` CDX query timed out
twice (urllib + curl); a third attempt returned a genuine 0 captures.

**July 5–6 2026 UNM rows: still not surfaced.** Wayback holds NO May–Jul 2026
captures of any goto.unm.edu stats URL (urphy21: 0 captures ever; vbudg: 0;
discvr/reso/7t6-o: nothing in the window). Combined with the 2026-09-29
Common Crawl clean negative, both backends are exhausted for this window —
recorded as a clean negative, not retried further.

Note on the raw/-missing exception above: this collection now holds its own
`evidence/remove-2026-05-12-university-shorteners-events/raw/wayback/` slice; the exception stands for live-capture evidence only.

## Fingerprint completion

The 69 rows appended after the original 1,522 (Common Crawl and Wayback
slices) lacked the required top-level `fingerprint`. Added only that field to
rows 1,523–1,591, as lowercase SHA-256 hex of the UTF-8 `labels.event_id`.
Verified that the first 1,522 fingerprints already equalled this same digest,
all 1,591 event IDs are unique, and all other row fields and row order remain
unchanged. The collection contains 1,591 events.

## Empty `best_day` normalization

The 17 appended rows 1,567–1,579 and 1,588–1,591 carried empty objects
in `labels.best_day`. Per the existing `temp/backfill_w4.py` rule for empty
nested labels, each empty object is represented by the JSON string `"{}"`.
Only this label value changed in those 17 rows; all other fields and row
order were preserved. This makes the empty-object meaning lossless while
conforming to the flat-label schema.

`scripts/build_shortener_events.py` is now an **offline partial reconstruction
only**: it reads the original September 28 captures from the sibling
collections' `raw/` directories and emits 1,520 fingerprinted,
schema-valid rows in an offline check, but cannot reproduce 71 Common Crawl
and Wayback rows (including two Wayback rows in the original 1,522). It
requires `--output` pointing to a new, distinct path and refuses to overwrite
an existing output or this canonical `events.jsonl`; it does not rewrite this
provenance or SHA256SUMS.

## Historical HTML hash reconciliation 2026-09-30

The Wayback HTML capture at
`evidence/remove-2026-05-12-university-shorteners-events/raw/wayback/5vtSk2RG2f/20260512030653.html` did not match its historical
nested-manifest SHA-256
`1ae6a9108fa2ab2563bcc370baf2eea69f31544564b4160f6faffed0c9b82422`,
even after CRLF-to-LF normalization. Its current raw-byte SHA-256 is
`4d54469380dcdf8df98f660078d81fe10a35ef559db7770c75eb47dbbfc9f58b`.
The operator accepted the current bytes as canonical and authorized updating
the nested manifest. The file itself was not changed. The old hash remains
here for audit; this does not explain the difference or claim a matching
historical copy.

## Builder relocation (2026-09-30)

Historical builder `scripts/build_shortener_events.py` was moved via staging into `data/2026-05-12-university-shorteners-events/build_events.py`. This is a preservation move, not a rebuild: existing events/rollups and raw captures were not regenerated or modified. The relocated script is historical and may overwrite collection outputs, provenance, checksums, or raw evidence if executed; do not run it against this collection. Only its offline path resolution was adjusted where applicable. The canonical shortener-events builder alone explicitly rejects the canonical events file and existing output paths. Older script paths elsewhere in this document refer to their historical locations.

The event file was LF-only at the start of the script reorganization
(1,591 rows, SHA-256 `e1a07aa5336979b1021d674f91f99eff5682333da18fbcba70603f62e2a32703`).
Its previous manifest hash
`8bcf0358cafa900d7e7c19ca79738e43a4cfc53a31a2da8e5e2a3ccd0b5b9ce0`
matches the exact same content with CRLF line endings. No event content
changed during the reorganization; the checksum now pins the LF checkout.
