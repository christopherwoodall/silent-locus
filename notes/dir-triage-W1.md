# Dir triage — worker W1 (2026-09-29)

Assigned dirs: `2026-09-05-termina-digital`, `2016-05-06-reverse-tunnels`,
`2016-12-28-rmn-re-history`, `2026-09-28-uoft-shorteners`,
`2026-08-21-public-board`. All DONE, none BLOCKED.

## Build summary

| dir | events in → out | rollup | kinds |
|---|---|---|---|
| 2026-09-05-termina-digital | 111 raw files → 223 events | 21 rows | wayback_capture 104, corpus_hit 105, corpus_grep_negative 5, artifact_observation 7, surface_negative 2 |
| 2016-05-06-reverse-tunnels | 22 raw files → 107 events | 6 rows | corpus_hit 85, tunnel_candidate 12, sweep_negative 7, dns_probe 2, corpus_grep_negative 1 |
| 2016-12-28-rmn-re-history | 5 raw files → 768 events | 47 rows | wiki_shortener 764, timeline_anchor 3, archive_probe 1 |
| 2026-09-28-uoft-shorteners | 13 raw files → 13 events | none (pure recon stream) | yourls_stats_page 10, shortener_info_page 2, artifact_observation 1 |
| 2026-08-21-public-board | 29 raw files → 888 events | none (pure event stream) | board_note 861, artifact_observation 26, sweep_negative 1 |

Rollup rule applied per Christopher's 2026-09-28 update: rollup.jsonl only
where a genuine aggregate layer exists in the raw (sweep pattern totals,
per-query urlquery totals, monthly growth curve). `event.dataset` on rollup
rows is `<slug>-rollup`, feeding the `<slug>-rollup` index.

Verification per dir: events.jsonl parses as JSON lines; every row has
`@timestamp`, `event.dataset`, `record_kind`, `fingerprint`;
`scripts/validate_schema.py` clean on all 5 dirs (2073 records, 0
violations); zero duplicate fingerprints within each file; 3 rows per dir
spot-checked against raw by hand; fingerprint method proven by recomputing
`sha256("TheNacken/python-cors-proxy")` == the reference fingerprint in
`data/2023-11-14-hfspace-proxies/events.jsonl` before building.

## New record_kinds introduced (for schema/README.md registry)

- `tunnel_candidate` — curated tunnel-hostname candidate (reverse-tunnels)
- `dns_probe` — DNS resolution/authoritative liveness check (reverse-tunnels)
- `archive_probe` — archive.org availability/CDX/playback probe (rmn-re-history)
- `board_note` — one agent note on public-board.com (public-board)
- `pattern_sweep_rollup` — per-pattern totals of the termina sweep battery
- `urlquery_rollup` — per-query hit totals (reverse-tunnels)
- `link_growth_rollup` — monthly new/cumulative link counts (rmn-re-history)

Already-in-use, not mine: `shortener_info_page` (used by sibling
university-shorteners datasets; used here for front pages).

## Removal / rename candidates (NOT acted on — read-only guard)

1. `data/2026-09-05-termina-digital/raw/wayback_manifest.json` — every
   `file` value carries the stale prefix `data/termina-digital/wayback/`
   (pre-dated-dir-move name). Evidence: `python3 -c` join against on-disk
   paths requires stripping that prefix. Candidate: rewrite prefix to
   `raw/wayback/`.
2. `data/2016-05-06-reverse-tunnels/raw/manifest.sha256` — stale lane
   manifest: lists `progress.log`, `htmx_search.py`, and a bare
   `PROVENANCE.md`, none of which exist in `raw/`. Candidate: regenerate
   against `raw/` or remove (dir-level SHA256SUMS now covers everything).
3. `data/2026-09-05-termina-digital/PROVENANCE.md` says the live RSS had
   "10 items"; the file on disk has 9 `<item>` elements. Minor doc drift;
   events.jsonl records the observed 9.
4. Out of scope (not my dirs, flagging only): non-dated directories directly
   under `data/` — `reverse-tunnels`, `dockerhub-trojan-images`,
   `forged-flag-hunt`, `gem-temporal-pivot`, `july7-gem-forensics`,
   `md-succ-ai` (untracked), `raw`, `processed`, `aggregates`,
   `separate-eval-test`, `site-captures`, `transfer-test-family`,
   `university-shorteners`, `xss-ssti-census`, `yourls-resweep-2026-09-28` —
   `schema/collections.md` says every collection dir is
   `YYYY-MM-DD-<slug>`; these look like pre-normalization leftovers.

## Deliberate non-events (documented in each PROVENANCE.md)

- Lane bookkeeping: `wayback_manifest.json` (termina),
  `raw/manifest.sha256` + `uq_report_summary.json` (tunnels),
  `manifest.json` (rmn-re-history, public-board).
- Derived aggregates kept out of events.jsonl: `growth_curve.json`
  (→ rmn-re-history `rollup.jsonl`); per-query totals (→ tunnels rollup);
  per-pattern totals (→ termina rollup).
- `notes.jsonl` is the single canonical per-note source for public-board:
  verified the 5 rotating archive pages union to exactly the same 861 ids
  and all 50 `changes.json` notes are within it — no double counting.

## Commits (branch `local`, NOT pushed)

- `b49ac7e` events: build events.jsonl for 2026-09-05-termina-digital
- `8b279d1` events: build events.jsonl for 2016-05-06-reverse-tunnels
- `f3434e3` events: build events.jsonl for 2016-12-28-rmn-re-history
- `08a729b` events: build events.jsonl for 2026-09-28-uoft-shorteners
- `aa11fca` events: build events.jsonl for 2026-08-21-public-board

Builder script kept at `/tmp/build_w1.py` (ephemeral; takes repo root as
argv[1], no hardcoded paths).
