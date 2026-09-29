# Dir triage — worker W4 (2026-09-29)

Dirs: `2026-01-25-agent-surfaces`, `2026-02-01-march7-rce-modality`,
`2026-02-14-md-succ-ai`, `2026-03-12-paste-archive-gap`,
`2026-09-03-collusion-manifest`.
Builder: `temp/build_w4.py` (repo root as argv; no network, read-only on raw/).

## New record_kinds (do NOT edit schema/README.md per sweep rules)

- `coverage_gap` — one per row of `coverage-gaps.csv` plus one per category in
  rollup (110 + 7 rows in `2026-09-03-collusion-manifest`). Semantics: a known
  coverage-gap assessment for a site/category (prior_status, compilation_status,
  gap_remains, saved-response counts). Did not reuse `corpus_grep_negative` /
  `sweep_negative` — those imply a search that found nothing; these rows are
  gap assessments, not empty searches.
- Side observation (not mine to fix): `schema/README.md`'s registry is already
  behind other merged dirs — `board_note`, `board_post`, `forum_message`,
  `repo_snapshot`, `repo_commit`, `gist_scan_page`, `null_read`, `comparator`,
  `related_readme`, `wiki_page_snapshot` are all live in events.jsonl files but
  absent from the registry.

## Rollup decisions

- `2026-01-25-agent-surfaces`: rollup YES — 11 per-surface `venue_finding` rows
  (pages_ok/total, first/last probe, content types), identity
  `agent-surfaces-rollup|<slug>`, dataset `…-rollup`.
- `2026-02-01-march7-rce-modality`: rollup NO — 5 atomic records
  (4 `campaign_specimen` + 1 `artifact_observation`), no genuine aggregate layer.
- `2026-02-14-md-succ-ai`: rollup NO — 2 `artifact_observation` records, pure
  event stream.
- `2026-03-12-paste-archive-gap`: rollup YES — 2 per-batch `extraction` rows
  (`lane-m` 16 pastes / `lane-1-retry` 51 pastes; counts, bytes, first/last
  created, confirmed deletions), identity `anna.fyi-rollup:<source>`. The
  investigator-repo snapshot is a provenance artifact, excluded from the rollup.
- `2026-09-03-collusion-manifest`: rollup YES — 7 per-category `coverage_gap`
  rows (site/host counts, gaps-remaining, saved-response totals), identity
  `coverage-gap-rollup:<category>`.

## data/md-succ-ai (untracked) vs data/2026-02-14-md-succ-ai — NOT a duplicate

`diff -rq data/md-succ-ai/repo data/2026-02-14-md-succ-ai/raw/repo`: the
untracked `data/md-succ-ai/repo/` holds only 2 files (`Makefile`,
`scripts/browser-server.mjs`, both dated 2026-09-28 20:29) versus 79 files in
`2026-02-14-md-succ-ai/raw/repo/`. The two are disjoint in content — this looks
like a leftover stub from the 2026-09-28 `repo/` → `raw/repo/` move (or a
partial re-clone), not a copy. Left untouched; flag for the lane owner to
decide. NOT deleted/moved per guard.

## Removal/rename candidates

None. Everything in the 5 dirs is referenced and checksummed. Non-actionable
observations (kept as-is, raw is read-only history):

- `2026-01-25-agent-surfaces/raw/_capture_summary.json` is stale/partial: it
  lists only nervesocket + bitily although 11 surfaces were captured. The
  per-surface `pages.json` files are authoritative and drive events.jsonl.
- `2026-02-01-march7-rce-modality/raw/manifest.json` keys use the pre-rename
  path prefix `./data/march7-rce-modality/raw/…` (dir is now
  `2026-02-01-march7-rce-modality`). Keys only; harmless.
- `2026-03-12-paste-archive-gap/PROVENANCE.md` cites pre-rename paths
  (`data/paste-archive-gap/…`, `data/agent-surfaces/…`). Doc-only.

## BLOCKED dirs

None — all 5 dirs built, validated (scripts/validate_schema.py: 0 violations),
`sha256sum -c` green, fingerprints spot-recomputed.

## Verification log (per dir: raw-in → events-out)

| dir | raw in | events | rollup | checks |
|---|---|---|---|---|
| agent-surfaces | 76 files (87 pages.json entries, 11 surfaces) | 87 venue_probe | 11 venue_finding | ts/sha/bytes vs pages.json; fp recompute |
| march7 | 24 files (results.json 4 gems; sweep.json; post JSON) | 4 campaign_specimen + 1 artifact_observation | none | fp=sha256(gem:name); per-gem dates; post.created_at |
| md-succ-ai | 81 files (repo 79 + openapi pair) | 2 artifact_observation | none | openapi sha256/size vs .sha256 sidecar |
| paste-archive-gap | 72 files (66 bodies + manifest 67 + crossref + cemetery + investigator-repo + 2 coverage docs) | 67 pastebin_probe + 1 artifact_observation | 2 extraction | manifest created_utc/sha; d266bdde sentinel; decoded generated_at |
| collusion-manifest | 2 files (110-row CSV + manifest.json) | 110 coverage_gap + 1 artifact_observation | 7 coverage_gap | CSV row ↔ labels; manifest counts; fp recompute |
