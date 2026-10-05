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

Preserved `es_ingest_paste.py` at `raw/scripts/legacy/es_ingest_paste.py` as a historical, optional Elasticsearch loader; it is not an active collection event builder. Its local path resolution now targets the same collection and repository inputs from the archived location. No source evidence, `events.jsonl`, or `rollup.jsonl` was changed; no network or ES actions were run. The SHA256SUMS entry records the relocated script bytes.
