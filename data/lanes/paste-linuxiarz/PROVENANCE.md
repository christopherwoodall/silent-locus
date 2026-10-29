# PROVENANCE — paste.linuxiarz.pl agent-text dataset

Separate dataset. Not part of collusion-wiki.

## Source
- Texts preserved by the Nightingale Collective collusion.wiki investigation,
  `records.jsonl` in the 11-file export bundle
  (https://collusion.wiki/explorer/download, retrieved 2026-09-27, all SHA-256 verified).
- Investigators' `site-coverage.csv` lists `paste.linuxiarz.pl` with
  `selected_distinct_texts = 158`, `compilation_status = selected_agent_related_text_preserved`,
  `prior_status = prior_concrete_paste_bodies_reused`.
- This dataset holds the 131 distinct paste IDs URL-enumerated in `records.jsonl`
  (`https://paste.linuxiarz.pl/view/<id>`); the remaining ~27 of the investigators'
  158 were not URL-enumerated in the export and are not recoverable from it.

## Method
- Bodies extracted verbatim from `records.jsonl` `text` fields (the investigators'
  preserved copies; live site returns 404 for sampled IDs as of 2026-09-28).
- One file per paste: `<id>.txt` (raw body bytes, unmodified).
- `manifest.jsonl`: per-paste id, title, retrieval timestamp, source URLs,
  investigator SHA-256 vs local body SHA-256, origin kinds, corpus record IDs,
  source references, live-vs-archived status.
- Live check: single HEAD/GET per paste URL, ≥5s pacing, browser UA, read-only.

## Caveats
- Investigator-selected subset ("agent-related text"), not a site census.
- Authorship fields in source records read `not_independently_authenticated`.
- `source_date_literal` values are epoch-ish strings from the investigators,
  unverified against the live site.
- Live availability decays: sampled IDs 404 on the live site; bodies here are
  the archived copies.

## Keep-all policy
Nothing dropped; failures/empties recorded in the manifest, not silently omitted.

## Raw layer 2026-09-29

- `data/paste-linuxiarz/manifest.jsonl` -> `data/2026-05-26-paste-linuxiarz/raw/manifest.jsonl` (crawl manifest consumed by `es_ingest_paste.py`, now co-located at `data/2026-05-26-paste-linuxiarz/es_ingest_paste.py`)

## Schema normalization 2026-09-29 (worker W7)

- Built `events.jsonl`: 131 records, one per paste `.txt` in `raw/`
  (paste id = filename stem); `manifest.jsonl` folded into labels
  (builder: `temp/build_events_w7.py`, repo root passed as argv[1]).
- record_kind: `relay_paste` (existing registry kind; no new kinds introduced).
- Fingerprint identity string: `linuxiarz-paste:<paste_id>` (sha256 hex).
- `@timestamp`: epoch `source_date_literals[0]` -> ISO-8601 Z
  (`labels.timestamp_source = "labels:paste.source_date_literal"`); all 131 present
  and in range (2026-05-26 -> 2026-06-17). The standing caveat holds: these are
  investigator-supplied epoch strings, unverified against the live site.
- Body sha256 + byte size verified per file against `manifest.jsonl` at build time
  (all 131 match); carried as top-level `sha256` / `size_bytes`; the investigator's
  per-paste retrieval time as `retrieved_at`.
- `SHA256SUMS` regenerated (sha256sum-style): `events.jsonl` + all `raw/` contents,
  verified with `sha256sum -c`.

## Rollup 2026-09-29 (W8)

Built `rollup.jsonl`: 3 rows x `paste_day_burst` — per-day paste bursts over
2026-05-26 -> 2026-06-17: 11 / 119 / 1 (the 2026-06-16 wave is the
agent-comms burst, 119 pastes in 42 seconds, top title `IowaCollabReply` x55;
live-check mix recorded per day). `@timestamp` = first paste of the day,
`labels.timestamp_source="labels:paste.source_date_literal"` (the standing
caveat holds: investigator-supplied epoch strings, unverified against the
live site). Fingerprint identity string `linuxiarz-paste-day:<day>`.
Builder: `temp/build_rollup_w8.py` (repo root passed as argv[1]); per-day
counts independently recomputed (sum = 131). `scripts/validate_schema.py`:
0 violations. SHA256SUMS regenerated (135 entries, incl. rollup.jsonl);
`sha256sum -c` OK.

## Date-prefix audit 2026-09-29 (worker W5)

Dir renamed `2026-09-28-paste-linuxiarz` -> `2026-05-26-paste-linuxiarz`.
All 131 paste events carry @timestamp 2026-05-26 -> 2026-06-17 (paste creation
dates; the 2026-06-16 burst holds 119/131). The old 2026-09-28 prefix was the
lane/build date, not an event date. Per schema/collections.md (prefix = first
event), the correct prefix is 2026-05-26. `event.dataset` updated in
events.jsonl / rollup.jsonl (`...-rollup` suffix preserved); SHA256SUMS
regenerated.

## Ingest script co-location 2026-09-29

- `scripts/es_ingest_paste.py` moved to `data/2026-05-26-paste-linuxiarz/es_ingest_paste.py`
  per the single-collection-build-script convention (this script only reads
  this collection's `raw/` + per-paste `.txt` captures).
- `REPO_ROOT` fixed (one extra `dirname`, matching the new depth); body path
  fixed to `raw/{pid}.txt` (the 84edfb3 layout commit moved bodies under
  `raw/` and the script was never updated — it would have raised
  FileNotFoundError before this fix).
- Verified: `build_docs()` rebuilds exactly the 131 committed `events.jsonl` rows.
- `local_es_manifest.json` `via_script` entry for `2026-05-26-paste-linuxiarz`
  now points at the co-located path.

## 2026-09-29 — build scripts co-located per convention
Normalization-wave build scripts moved from `temp/` to the collection root
per the 2026-09-29 convention (single-collection build scripts live in the
collection dir; schema/collections.md). `temp/` removed. SHA256SUMS
regenerated; `sha256sum -c` green.

## Historical loader relocation (2026-09-30)

Preserved `es_ingest_paste.py` at `evidence/remove-2026-05-26-paste-linuxiarz/raw/scripts/legacy/es_ingest_paste.py` as a historical, optional Elasticsearch loader; it is not an active collection event builder. Its local path resolution now targets the same collection and repository inputs from the archived location. No source evidence, `events.jsonl`, or `rollup.jsonl` was changed; no network or ES actions were run. The SHA256SUMS entry records the relocated script bytes.

## Lane-1 extension 2026-10-05 (joshuadavid corpus reconciliation)

- Source: public export `agent-logs/paste-linuxiarz/` of
  JoshuaDavid/WikiAgentSwarmInvestigation (branch `main`, retrieved
  2026-10-05 via raw.githubusercontent.com; the paste hosts were never
  probed). Their export = 219 shellac-imported pastes + 162
  Wayback-recovered pastes (81 `swarm` / 81 `unclear` verdicts), 2022-07 →
  2026-09.
- Reconciliation: all 131 of our original pastes are a subset of their 219
  shellac imports (exact ID match, 131/131). **250 pastes are genuinely new
  vs this dataset**: 88 additional shellac imports (dated 2022-07-06 →
  2026-06-18) + 162 Wayback rows (no absolute timestamps; 35 full-body,
  127 view-page-only: title + posted-name + relative-age only).
- Extension method: `raw/<pid>.txt` added for the 123 new full-body
  pastes (all body SHA-256 match the investigators'); 250 manifest rows
  appended (jd verdict/inclusion/body-availability/wayback fields +
  external-overlap annotation); 250 `relay_paste` event rows appended
  (fingerprint `linuxiarz-paste:<pid>`; view-only rows carry
  `@timestamp = 1970-01-01T00:00:00Z` sentinel +
  `labels.timestamp_source = "fallback:no_recoverable_date"` and omit
  `sha256`, per schema; confidence `confirmed` for body-verified,
  `medium` for view-only). Builder: lane1 `build_lane1_ingest.py`
  (idempotent; skips already-present IDs).
- Totals after extension: 381 pastes in `evidence/remove-2026-05-26-paste-linuxiarz/raw/manifest.jsonl` / `events.jsonl`
  (254 with bodies on disk).
- `rollup.jsonl` left frozen at the original 131-row wave (2026-05-26 →
  2026-06-17 day bursts); the 250 new rows are not rolled up (heterogeneous
  timestamp grades — 162 have no absolute dates).
- `scripts/validate_schema.py`: 0 violations over the combined 381 rows.
  `SHA256SUMS` regenerated (whole tree); `sha256sum -c` green.
- Note on the 2026-09-27 "~27 unrecoverable": re-audit of the local
  collusion-wiki `records.jsonl` shows all 158 linuxiarz-origin records carry
  a paste URL and resolve to exactly our 131 distinct paste IDs — the "27"
  were duplicate/redundant records, not missing texts. There is no
  additional recoverable text in the joshuadavid export beyond the 250 new
  IDs enumerated here.
