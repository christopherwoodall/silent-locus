# Provenance: World Poverty task-family structural dataset (Lane U, 2026-09-28)

## Question
How does the api.worldpoverty.io agent task family run — slug set, query templates,
wiki venue sheets, cross-family citation, timing shape.

## Inputs (read-only, on disk)
- `data/rmn-re/link_table_decoded_2026-09-27.json` — 15 decoded rmn.re slugs
  (slug, decoded_target, clicks, created (renders +4h vs UTC), creator_ip16, chain_wrappers)
- `data/collusion-wiki/shortener-logs.json` — rmn.re YOURLS log (site rmn.re):
  authoritative ISO-UTC creation times + click counts per keyword; 11 of 15 worldpoverty
  keywords at links 479-493, remaining 4 at 494/495/496/498
- `data/collusion-wiki/revisions.jsonl` — wiki page bodies + write_date + ip16 + label
  (3 Poverty Links pages byte-identical; WorldPovertyClockSequenceJun19 @1;
  IHMEFamilyPlanningDec13Cohort @4-@8; TmpJul20FPScoutTest @2)
- `data/collusion-wiki/events.jsonl` — save/delete events (burst + June-30 admin hygiene)

## Method
- Enumerated all 15 slugs matching api.worldpoverty.io in the decoded table; joined with
  the YOURLS log by keyword for authoritative UTC timestamps.
- Extracted the GraphQL query template per slug (year variants, country sets, field shapes);
  canonicalized into 12 templates in query_templates.json.
- Compared the 3 Poverty Links page bodies byte-wise (SHA-256) — identical.
- Ordered all dated events into timeline.json.

## Caveats
- rmn.re click counts differ slightly between the YOURLS log and the decoded table
  (both values recorded per slug; log is the earlier snapshot).
- No per-click timestamps exist in any corpus: click clustering cannot be tested.
- Author fields are ip16 + handle-grammar labels only; no operator attribution attempted.

## Outputs
- `hits.jsonl` — shared-schema docs, event.dataset="worldpoverty-task-family"
- `query_templates.json` — 12 canonical templates with example slugs
- `timeline.json` — 8 dated events, staging -> burst -> hygiene

## Closure 2026-09-28 (workstream C)

Closed: full structural census of the api.worldpoverty.io task family — 15
slugs enumerated from the decoded rmn.re link table (all matching slugs),
joined with the YOURLS log for authoritative timestamps, 12 canonical query
templates, 8-event timeline. No more worldpoverty slugs exist in the link
table; the family is bounded by construction. ES `worldpoverty-task-family`
_count=22 verified, schema-drift clean.

## Repair 2026-09-29 (build-script rebuild + payload embedding)

The collection's build inputs were lost in the 2026-09-28/29 normalization:
the original `hits.jsonl` was folded into the staged `events.jsonl` and
deleted, and the ingest script carried stale pre-rename paths plus a dead
Elastic-load path. Repaired per the 2026-09-29 directive (do not delete;
rebuild from the directory's data):

- `es_ingest_worldpoverty_task_family.py` (co-located in this dir per
  schema/collections.md) now rebuilds all 22 event docs from the surviving
  PRIMARY sources: `data/2026-09-27-rmn-re/raw/link_table_decoded_2026-09-27.json`
  (15/15 slugs verified present), `data/2026-05-17-collusion-wiki/raw/shortener-logs.json`
  (15/15 keywords verified present), `data/2026-05-17-collusion-wiki/raw/revisions.jsonl`
  (3 Poverty Links bodies + sequence page verified; original hits.jsonl also
  recoverable from git history at 4487b53 `data/worldpoverty-task-family/hits.jsonl`).
- Rebuild verified against the pre-repair staged events.jsonl: identical
  fingerprints (22/22) and identical notes/matched_string/tags. Only intended
  deltas: fixed `labels.source_file` paths (were `data/rmn-re/...` and
  `data/collusion-wiki/...`, which never existed post-rename), one fixed
  `source_url` on a run_shape doc (`data/worldpoverty-task-family/timeline.json`
  -> `data/2026-09-28-worldpoverty-task-family/raw/timeline.json`), and the new
  payloads below. Structural asserts kept: 15 slugs, 3 byte-identical Poverty
  Links bodies, sequence page present, 22 docs.
- Per-item payloads embedded in the new OPTIONAL top-level `payloads` array
  (schema/record.schema.json 2026-09-29; item shape
  {kind, content_type, content, encoding, truncated, byte_size, sha256}):
  15x kind=decoded_shortlink_target (full decoded GraphQL target URL per slug,
  26-464 B each, 3,408 B total) and 4x kind=wiki_page_body (full page bodies,
  460-615 B each; matched_string carries only the first 400 chars). All
  carried in full (truncated=false) -- no truncation cap exercised.
  NOT embedded: cross_family_citation citing revision bodies (~21.6 KB across
  10 revisions of another family's pages -- out of collection scope; the note
  quotes the citing lines and the bodies remain addressable in the
  2026-05-17-collusion-wiki collection). run_shape docs carry no per-item
  payload (collection-level artifacts already in raw/).
- Fingerprints use the legacy seed "worldpoverty-task-family" (pre-rename
  index name) so they stay stable with already-indexed docs. Known quirk
  (pre-existing, preserved): the 3 wiki_poverty_links_page docs share one
  fingerprint (byte-identical bodies -> identical matched_string).
  push_to_local_es.py derives the ES _id from the sha256 of the whole
  canonical doc, so the added payloads mean new _ids on the next load --
  recreate the 2026-09-28-worldpoverty-task-family index (or accept new _ids)
  when the hosted write freeze lifts.
- Pure builder: no network, no Elastic writes; deterministic (fixed
  event.created/@timestamp), re-runs byte-identical. Loading is generic via
  scripts/push_to_local_es.py auto-discovery. `python3 -m py_compile` clean;
  scripts/validate_schema.py reports 0 violations on the rebuilt events.jsonl.
