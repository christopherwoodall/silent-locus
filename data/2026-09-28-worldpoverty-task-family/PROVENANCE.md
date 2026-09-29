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
