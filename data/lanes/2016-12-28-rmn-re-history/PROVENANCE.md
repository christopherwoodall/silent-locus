# PROVENANCE — rmn-re-history

Reconstruction of the rmn.re YOURLS shortener's link-table evolution, built
2026-09-28 (dataset dated 2026-09-27).

## Inputs

1. `../rmn-re/link_table_2026-09-27.jsonl` (764 records) — read-only crawl of
   rmn.re's public paginated front-page index, 2026-09-27. Per-slug `created`
   timestamps are YOURLS-authoritative (the shortener records creation time
   itself), so the first-appearance timeline below needs no archive to be
   trustworthy.
2. `../wiki_shortener_detail.json` (499 records) — the preserved shortener log
   from the wiki corpus; crawl window 2026-05-26T18:01Z → 2026-06-21T20:22Z.
   Publisher-selected ("agent-related text"), not a full census.
3. archive.org Availability API (`archive.org/wayback/available`) — nearest-
   snapshot probes for 2026-06-17, 2026-07-15, 2026-09-01. Result: exactly one
   homepage snapshot exists (2025-06-22); none during or after the June 2026
   campaign burst.

## What did not work

- Wayback CDX listing (`web.archive.org/cdx/search/cdx?url=rmn.re`) returned
  upstream HTTP 500 with an empty body; not retried per access policy.
- Playback of the single 2025-06-22 snapshot also returned upstream HTTP 500
  from this network. Its content is therefore NOT included here — only its
  existence and timestamp are recorded (archive_lookup.json).

## Files

- `slug_evolution.jsonl` — one record per slug: slug, created (ISO-8601 UTC),
  in_june_log (bool), grammar (zz/epoch10/oai/other), target_host, clicks,
  creator_ip16 (/16-truncated).
- `growth_curve.json` — monthly new/cumulative link counts, 2016-12 → 2026-09.
- `grammar_first_appearance.json` — earliest slug per campaign grammar.
- `archive_lookup.json` — archive probe results and failure record.
- `manifest.json` — file list + SHA-256.

## Scope

Agents and infrastructure only. Creator IPs are /16-truncated; no operator
identity is pursued. Read-only throughout; nothing was created on rmn.re.

## Raw layer 2026-09-29

- `slug_evolution.jsonl` -> `raw/slug_evolution.jsonl` (script-consumed transform input; consumer: scripts/es_ingest_rmn_history.py). Upstream name preserved; raw layer exempt from event schema.

## Normalization 2026-09-29 (events.jsonl + rollup.jsonl)

- `events.jsonl`: 768 rows, all schema-conformant.
  - 764 `wiki_shortener` — one per row of `raw/slug_evolution.jsonl`
    (764 slugs; `created` is YOURLS-authoritative).
  - 3 `timeline_anchor` — one per grammar in
    `grammar_first_appearance.json` (zz/epoch10/oai first slugs).
  - 1 `archive_probe` — the `archive_lookup.json` availability/CDX/playback
    probes (single 2025-06-22 snapshot; CDX 500; playback 500).
  - `growth_curve.json` is a derived aggregate: it does NOT appear in
    events.jsonl (fully reconstructible from the per-slug events); it lives
    in `rollup.jsonl`. `manifest.json` is lane bookkeeping (not an event).
- `rollup.jsonl`: 47 rows, `link_growth_rollup` — the monthly
  new/cumulative link counts from `growth_curve.json` (2016-12 -> 2026-09;
  genuine aggregate layer).
- Fingerprint identity strings: `rmn.re/<slug>` (per-slug);
  `grammar_first:<name>` (grammar first-appearance);
  `archive_lookup:rmn.re` (archive probe); `growth_curve:<month>` (rollup).
- `labels.timestamp_source`: `labels:slug.created` (per-slug);
  `labels:grammar.created`; `labels:probe.attempted_at` (=2026-09-28T03:05Z);
  `labels:curve.month` (rollup).
- New record_kinds: `archive_probe`, `link_growth_rollup`.

## 2026-09-29: ingest script co-located (hunt convention)
- `es_ingest_rmn_history.py` moved from `scripts/` into this directory per
  Christopher's single-collection convention; transforms
  `raw/slug_evolution.jsonl` into shared-schema docs (YOURLS dates, June-log
  membership, grammar tags — real transform, not a pure loader).
- `REPO_ROOT` in the script adjusted (repo root is now three levels up).
  Offline verification: `python3 -m py_compile` clean.
- `scripts/local_es_manifest.json` via_script entry repointed here.
- SHA256SUMS regenerated (script file added to coverage).

## Historical loader relocation (2026-09-30)

Preserved `es_ingest_rmn_history.py` at `raw/scripts/legacy/es_ingest_rmn_history.py` as a historical, optional Elasticsearch loader; it is not an active collection event builder. Its local path resolution now targets the same collection and repository inputs from the archived location. No source evidence, `events.jsonl`, or `rollup.jsonl` was changed; no network or ES actions were run. The SHA256SUMS entry records the relocated script bytes.

## 2026-10-10 — Factum ingest (lane `2016-12-28-rmn-re-history`)

- Moved lane artifacts `evidence/2016-12-28-rmn-re-history/` ->
  `data/lanes/2016-12-28-rmn-re-history/`; tombstone at
  `evidence/remove-2016-12-28-rmn-re-history/` (README.md explains the move).
- Submitted 5 records, all tagged `{"lane": "2016-12-28-rmn-re-history"}`:
  1 source (this reconstruction) + 1 `infra.ioc` (first zz-grammar slug
  `zzzz`, 2020-03-12) + 3 `reachability.check` (archive.org availability,
  CDX listing, snapshot playback probes, 2026-09-28T03:05Z).
  Ingest actor: `agent:lane-ingest:2016-12-28-rmn-re-history`.
- Dedup (pre-ingest, per standing rule):
  - 764 `wiki_shortener` per-slug events: ALL already present in Factum as
    `infra.shortcut` (lane `2016-12-28-rmn-re` ingested 2026-10-10 plus
    earlier lanes). Skipped, not resubmitted. The per-slug grammar /
    in_june_log analysis stays in the lane documents (`events.jsonl`,
    `raw/slug_evolution.jsonl`).
  - `timeline_anchor` oai (`oaix5507`) and epoch10 (`mailtest1779882833`):
    already asserted by the event record in lane
    `2026-03-07-timeline-anchors` (source_lane rmn-re-history). Skipped.
  - 47 `link_growth_rollup` rows: no installed schema type covers monthly
    aggregates (schema gap, noted below); kept as lane documents, same as
    the sibling `2016-12-28-rmn-re` lane's rollup. Fully reconstructible
    from the per-slug events (rollup new-sum = 764, verified).
- Schema gaps noted: (1) no aggregate/timeseries observation type for the
  monthly growth curve; (2) `factum-web` type names are inconsistent --
  the reachability check is registered as `reachability.check` (no `web.`
  prefix) while `web.capture` keeps it; `add` rejects the prefixed form
  with "Unknown observation type". Verify exact type names with
  `schema assigned observation <type>` or corpus precedent before
  submitting.
- Validator `validate_ingest.py`: independent re-derivation from the lane
  evidence (kind-combo counts, verbatim spot-checks against raw/*.json,
  dedup-skip recomputation over all committed batches). PASS against the
  exported batch.
- SHA256SUMS regenerated from actual bytes in `data/lanes/`; `sha256sum
  -c` green.
