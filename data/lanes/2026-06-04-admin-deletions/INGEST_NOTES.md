# INGEST_NOTES — 2026-06-04-admin-deletions

Batch `d71a22ef05e2418c99e84697aa2aac31`: **5,248 records**, zero
retractions, zero `in_lane` edges (edge building is a later pass).

| records | kind / type |
|---|---|
| 1 | `source` — collusion-wiki corpus upstream |
| 2 | `artifact` — `events.jsonl`, `rollup.jsonl` as git references with `reported_sha256` |
| 2 | `dataset.snapshot` observations — delete-event dataset (5,217 rows), per-day rollup dataset (26 rows) |
| 5,217 | `dataset.record` observations — one per delete event, grade OBSERVED |
| 26 | `dataset.record` observations — one per per-day rollup doc (`record_subset: per-day-rollup`), grade INFERENCE |

Tag `{"lane":"2026-06-04-admin-deletions"}` on every record. `factum.author`
auto-stamped (never set manually).

## Legacy row mapping

Per delete event: `body.data.external_record_id` = legacy `event_id`
(for example `delete:dse:rclog:131972`); `locator` = `{artifact:
@events_artifact, row: {index: i}}`; `snapshot` = `@events_snapshot`;
`observed_at` = legacy `labels.time`, `time_basis` = `legacy_documented`.
The real IOC value (the deleted page name) is `delete.page` in tags;
`external_record_id` is the legacy row's natural key, same as the
deepsearchqa `dsqa_N` pattern.

Tags carry every non-null legacy label field verbatim (`delete.*`
namespace), plus `legacy_fingerprint`, `legacy_record_kind`
(`delete_event`), `legacy_dataset`. Six fields are null on all 5,217 rows
(`write_date`, `rcs_date`, `recent_changes_time`, `revision_ref`,
`related_event_id`, `relation_type`) and are omitted from tags; full
verbatim rows remain in the `events.jsonl` artifact. 29 events carry
`round_id`; 1 carries `clock_note`; both are tagged only when non-null.

Per rollup doc: `external_record_id` = `doc_id`
(`admin-deletions:2026-06-23` …), locator into the rollup artifact,
`observed_at` = the doc's `@timestamp`. The `description` is preserved
**verbatim, no truncation**; the doc's `tags` list, `confidence`,
`observer` block, and `source_url` are tagged (`rollup.*`). Grade is
INFERENCE because these are derived analytic summaries, not direct
observations.

## Validation

- Pre-ingest dedup: `match --text` (fuzzy) for `TestFoobaAgent`,
  `admin-deletions`, `collusion-wiki`; `match --value` (exact) for
  `TestFoobaAgent` and `delete:dse:rclog:131972`. The fuzzy hits were
  unrelated records (pastebin-k4be `infra.message`, transluce-intel
  report, powerbi-fronting messages) — different shapes, no overlap.
  `match --value` returned `not_found`. Batch-internal dedup by
  `event_id`/`doc_id`: all unique (asserted in the builder).
- Adversarial validator (`/tmp/adversarial_admin_deletions.py`, ephemeral):
  every one of the 5,248 records traced to lane bytes — locator row
  indexes, `observed_at`, fingerprints, verbatim descriptions, tag values
  (including the 29 `round_id`s and the single `clock_note`), artifact
  sha256 vs SHA256SUMS, ref integrity, lane tag on all records, no edge
  records, no placeholder text. **PASSED.**

## Discrepancies found

- None in the legacy data. One modeling note: the rollup `description`
  for 2026-06-23 writes "Seite geloescht." (ASCII) while the events carry
  "Seite gelöscht." (ö) — both preserved verbatim in their own records;
  not normalized.

## Root-cause notes for the next worker

- `python3 skills/factum/scripts/factum.py` works directly; `uv` is at
  `~/.local/bin/uv`, not on PATH.
- `template --bare` scaffolds are incomplete: observations REQUIRE
  `observed_at` + `time_basis` in `body`, and bundle `add --input`
  requires top-level `actor` + `idempotency_key`.
- Artifact schema is `oneOf`: use `reference` (with `reported_sha256`)
  OR `sha256`+`size`, never both.
- `lane new` writes `data/lanes/<date>-<slug>-<id>/`; `mv` to the plain
  slug and set `docs_path`/`legacy_path` tags at creation time.
- Snapshot `observed_at`: use the lane file's `event.created` timestamp
  with `time_basis: legacy_documented`.
