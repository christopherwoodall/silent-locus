# Normalization sweep synthesis — 2026-09-29

Coordinator report for the event-directory normalization fan-out on branch `local`.
33 dirs were missing `events.jsonl`; 31 got them. Nothing was pushed (Christopher
pulls when ready).

## Totals

| Worker | Dirs | Event rows | Rollup rows | Commits |
|---|---|---|---|---|
| W1 (2016–2019) | 5 | 1,999 | 74 | 6 |
| W2 (2021–2022) | 5 | 314 | 67 | 6 |
| W3 (2022–2025) | 5 | 10,524 | 10 | 6 |
| W4 (2026-01–2026-05) | 5 | 273 | 20 | 5 |
| W5 (2026-05–2026-09) | 5 | 1,853 | 10 | 6 |
| W6 (rmn-re pair, fbi-ucr, counter) | 2 built / 2 flagged | 768 | 47 | 3 |
| W7 (jsonhero-docs, ludism, linuxiarz) | 3 | 172 | 17 | 4 |
| W8 (rollup follow-up pass) | 10 reviewed | — | 131 | 10 |
| **Total** | **31 built** | **15,903** | **245** | **~56** |

BLOCKED dirs: **none**. Every buildable dir built, schema-validated
(`scripts/validate_schema.py`, 0 violations everywhere), `sha256sum -c` green,
fingerprints recompute-verified against the documented identity strings.

## Per-dir results

- **2016-01-05-termina-digital** — 223 events (104 wayback_capture, 105 corpus_hit,
  5 corpus_grep_negative, 7 artifact_observation, 2 surface_negative), 21-row
  per-pattern sweep rollup. Capture times joined from the lane CDX dump via SURT
  urlkeys (99/99).
- **2016-05-06-reverse-tunnels** — 107 events, 6-row per-query rollup.
- **2016-12-28-rmn-re-history** — 768 events (764 wiki_shortener), 47-row monthly
  growth-curve rollup.
- **2018-10-01-uoft-shorteners** — 13 events, no rollup (pure recon stream).
- **2019-12-26-public-board** — 888 events (861 board notes, dedup-verified against
  the 5 archive pages), no rollup.
- **2021-05-10-vanderbilt-shortener** — 38 events, no rollup (heterogeneous census).
  12 of 13 web mentions undated → sentinel 1970 + `fallback:no_recoverable_date`.
- **2021-10-30-demowiki** — 16 events, no rollup.
- **2022-03-01-jsonhero** — 19 events, no rollup (usage aggregate already an event row).
- **2022-05-14-jqp-vercel** — 2 events, no rollup.
- **2022-08-09-github-forensics** — 239 events, 67-row rollup (66 fork-day bursts —
  peak 47 forks 2026-07-22→25 — + 1 issue summary).
- **2022-12-30-dse-wiki-verification** — 21 events, no rollup. **PROVENANCE.md was
  missing; created.**
- **2025-01-13-jsonhero-docs-archive** — 6 events, 1-row recovery census rollup.
- **2025-02-04-thecolony-ai** — 55 events, no rollup.
- **2025-03-04-rubygems-goimport-campaign** — 10,421 events (largest dir: nodes,
  ioc-log, hits, IOCs, wayback, pins, JFrog), 5-row per-day wave rollup
  (2026-05-12: 567 campaign gems). `.pre-bulk` verified ⊆ current set, excluded;
  edges excluded (relationships, not events).
- **2025-05-14-hf-tampering-check** — 21 events, 4-row per-repo rollup.
  **Notable: 0 commits in the 2026-07-10/13 breach window.**
- **2026-01-25-agent-surfaces** — 87 venue_probe, 11-row per-surface rollup.
- **2026-02-01-march7-rce-modality** — 5 events, no rollup.
- **2026-02-14-md-succ-ai** — 2 events, no rollup.
- **2026-03-12-paste-archive-gap** — 68 events, 2-row extraction-batch rollup.
- **2026-05-01-collusion-manifest** — 111 events (110 coverage_gap), 7-row
  per-category rollup.
- **2026-05-27-paste-archive** — 76 events (55 anna.fyi + 20 k4be.pl + 1
  infinitypaste), 3-row per-venue rollup.
- **2026-06-20-powerbi-fronting** — 180 events, no rollup.
- **2026-07-07-july7-wave** — 264 events, 3-row per-wave rollup (16 july-07 /
  2 may-27 / 246 absent). Resweep fully merged, 0 missing names.
- **2026-08-19-tantive-space** — 1,326 events (1124 messages + 201 threads),
  4-row per-room rollup.
- **2026-09-05-fieldnotes-gem** — 7 events, no rollup.
- **2026-09-27-rmn-re** — 764 shortener_link events, 47-row monthly growth rollup
  (June 2026: +484 burst).
- **2026-09-28-counter-channel** — 4 events, no rollup (single snapshot).
- **2026-09-28-jsonhero-docs** — 12 events, 5-row doc-family rollup.
- **2026-09-28-ludism-wikis** — 29 events, 9-row per-target rollup (2/9 reachable,
  jina-only; controls excluded).
- **2026-09-28-paste-linuxiarz** — 131 events, 3-row per-day burst rollup
  (2026-06-16: 119 pastes in 42 s — the agent-comms wave).

## FLAGGED for Christopher (no data invented, nothing moved)

1. **data/2026-09-27-rmn-re-linktable** — PROVENANCE.md only. It claims the
   collection was "materialized as a physical collection dir (events.jsonl via the
   builder's --dump mode)" on 2026-09-29, but no events.jsonl exists and
   `scripts/es_ingest_rmnre.py` has no `--dump` mode. The real materialized dump
   is one line at `data/aggregates/2025-09-26-cors-bwa-proxy/raw/rmn-re-linktable.jsonl`
   (`_index: rmn-re-linktable`, kind `"shortlink"` — itself unregistered). Its
   PROVENANCE cites `data/2026-09-27-rmn-re/raw/` as *sources for a derived join*,
   not as the same collection. Decision needed: materialize the join, or retire
   the dir.
2. **data/2026-09-28-api-usa-fbi-ucr** — SHA256SUMS only, referencing
   `raw/progress.log` (hash f27dcc3…); no raw/, no PROVENANCE.md, and no file
   anywhere in the repo matches that hash. **No FBI/UCR data exists anywhere in
   the repo.** Decision needed: drop the dir or point it at real data.

## Removal / rename candidates (report-only, none acted on)

- **data/july7-gem-forensics/** — stub confirmed: only `progress.log`; full dataset
  is `data/2026-07-07-july7-gem-forensics/`. Remove candidate.
- **data/md-succ-ai/** (untracked) — NOT a duplicate of `data/2026-02-14-md-succ-ai/`;
  its `repo/` holds 2 files vs 79 in the real clone. Looks like a move leftover.
  Remove-or-relocate candidate.
- **data/reverse-tunnels/** — undated; W6 triage found 8 stubs total across
  undated dirs, 0 true duplicates. Likely stub; verify against
  `data/2016-05-06-reverse-tunnels/`.
- **data/university-shorteners/** — undated; check overlap with dated shortener dirs.
- **data/dockerhub-trojan-images/** — 2 scan logs not duplicated in the dated dir;
  possible merge candidate.
- W2: stray `progress.log` files, 7 byte-identical 58-byte history stubs,
  12 identical stargazer-401 bodies, derived `repo_summary.json` (keep per
  keep-all, but noted).
- W1: `wayback_manifest.json` `file` values carry stale `data/termina-digital/wayback/`
  prefix; `reverse-tunnels/raw/manifest.sha256` is stale (lists nonexistent files).
- W3: `hf-tampering-check/raw/MANIFEST.sha256` stale (lists missing `progress.log`);
  jsonhero `raw/manifest.json` has stale pre-rename path `data/jsonhero-docs-archive/`;
  gems PROVENANCE still says "pending-relocation" to a sibling repo — needs a
  decision; `2022-12-30-dse-wiki-verification` date prefix matches no event in the
  dir (earliest 2026-03-11) — flagging, not renaming.
- W7 (aggregates/processed/site-captures/raw survey): (1) two aggregate dirs lack
  events.jsonl — layering vs dated-dataset convention; (2) `data/raw/` corpus-root
  placement vs dated dirs; (3) site-captures as a future normalization candidate;
  (4) `processed/gems/` (964 extracted dirs) retention vs redundancy; (5) stale
  `data/cors-bwa-proxy/` reference in the cors-bwa PROVENANCE.

## Schema gaps found (schema/ untouched per instructions)

- `scripts/validate_schema.py` rejects `observed_at` although `schema/record.schema.json`
  lists it as an allowed key. Pick one.
- `schema/README.md` record-kind registry is behind reality. New kinds minted in
  this sweep (registry NOT edited): `tunnel_candidate`, `dns_probe`,
  `archive_probe`, `board_note`, `pattern_sweep_rollup`, `urlquery_rollup`,
  `link_growth_rollup`, `wiki_page_snapshot`, `repo_snapshot`, `repo_commit`,
  `repo_issue`, `repo_fork`, `repo_search_hit`, `gist_scan_page`,
  `related_readme`, `recovery_census`, `campaign_day_rollup`,
  `repo_commit_rollup`, `coverage_gap`, `paste_venue_rollup`,
  `diffend_wave_rollup`, `room_rollup`, `shortener_link`, `counter_reading`,
  `counter_probe`, `fork_day_rollup`, `issue_summary_rollup`,
  `doc_family_rollup`, `target_probe_rollup`, `paste_day_burst`.
  A registry consolidation pass is owed.

## Method notes

- Fingerprint = `sha256(<documented identity string>)`, identity string recorded in
  each dir's PROVENANCE.md. Every worker recomputed the reference
  `sha256("TheNacken/python-cors-proxy")` against
  `data/2023-11-14-hfspace-proxies/events.jsonl` before writing.
- `event.dataset` = the directory name; rollup datasets are `<dirname>-rollup`.
- Timestamps are real event dates from raw data; dir-date prefix with
  `labels.timestamp_source` where per-record dates were absent; sentinel
  1970-01-01T00:00:00Z + `fallback:no_recoverable_date` only where no date was
  recoverable. No invented dates.
- All commits used explicit pathspecs; nothing pushed.
