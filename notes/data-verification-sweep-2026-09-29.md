# Data verification sweep — 2026-09-29

64 dated collections under `data/`, one worker per collection, coordinator
reconciliation + central rerun. Branch `local`. All workers complete.

## Central rerun results (post-worker, 2026-09-29 ~05:00 UTC)

- `sha256sum -c SHA256SUMS` in all 64 collections: **all green, zero failures**
- `python3 scripts/validate_schema.py` (repo): **141,804 records in 84 event files,
  0 files with violations**
- Top-level `file` pointers: **1,726 total, 1,569 stale** (all understood drift,
  bytes verified elsewhere — see fix list)
- `python3 -m compileall` over `scripts/` + all collection `.py`: clean
- `push_to_local_es.py --all --dry-run`: **fails** on a stale manifest path
  (`scripts/es_ingest_jfrog.py` was moved into its collection by the parallel
  script-condense crew; its manifest entry hasn't been updated yet). Condense
  crew owns the manifest; flagged to them, not fixed here.
- Stale `2016-05-06-reverse-tunnels` refs remain in: the renamed collection's own
  `PROVENANCE.md`, `scripts/es_ingest_reverse_tunnels.py`,
  `scripts/local_es_manifest.json`, `schema/collections.json`, `temp/*`
  (temp files are scratch; historical `notes/*` hits are fine).

## Checksum regens committed (25 commits, explicit pathspecs, `local` only)

All drift understood from git history: manifests committed at inception with
hashes that never matched the committed bytes (wrong at birth), phantom
`raw/progress.log` entries for a file never committed anywhere, one CRLF-vs-LF
normalization case, and layout-normalization path-only updates without rehash.
Disk bytes == HEAD blobs in every case; no data was touched.

| Commit | Collection |
|---|---|
| 9e500af | 2026-08-25-commonlog-scan |
| afcef35 | 2026-03-07-timeline-anchors |
| d4324c7 | 2026-05-11-july6-staging |
| 622939f | 2026-05-17-iowacollab-pastes |
| b4ba88c | 2026-09-28-agents-relay-sweep |
| 99be392 | 2025-12-04-urlquery-marker-sweep |
| fe14d36 | 2026-02-01-agent-convo-venues |
| c5f5a3c | 2026-05-11-osv AND 2026-07-07-exfil-endpoint-pivot (shared-index race, one commit) |
| e778d65 | 2026-05-05-gomod-hunt |
| 0fbf2cb | 2026-05-12-webhook-deaddrops |
| 059253f | 2026-08-10-wayback-gem-capture |
| fc08f81 | 2026-07-21-transfer-test-family |
| de61e03 | 2026-09-28-open-data-api-venues |
| d4cd39f | 2026-09-28-pxweb-national-stats |
| 307bd25 | 2026-09-28-nsi-venue-sweep |
| d8d5384 | 2026-09-28-pastebin-pivot |
| 9aac826 | 2026-09-28-university-shorteners-batch3 |
| 22149f3 | 2026-09-28-university-shorteners |
| 2c697a7 | 2026-09-28-worldpoverty-task-family |
| e9ccc81 | 2026-09-29-forged-flag-hunt |
| a6959eb | 2026-09-28-yourls-resweep |
| 139bf73 | 2026-06-04-admin-deletions |
| c1b4d35 | 2026-09-28-pastebin-cluster-sweep |
| ddadf02 | 2026-05-17-collusion-wiki |
| 4b9f8fa | 2026-09-28-university-shorteners-batch2 |

The three initially FLAGGED manifests (pastebin-cluster-sweep, collusion-wiki,
university-shorteners-batch2) were regened by the coordinator after independent
disk-vs-HEAD-blob verification: bytes stable since creation, corroborated by
per-record sha256 fields / PROVENANCE evidence tables. Zero manifests remain
unresolved.

## Master table (condensed; full per-worker rows at coordinator's /tmp/verify-table.md)

Legend: checksums green/regen all verified post-regen; layout "ok" = canonical
root files + raw/; provenance gaps are doc-only unless noted.

| Collection | Checksums | Layout | Root .py | Stale `file` ptrs | Date | Schema | Provenance gaps |
|---|---|---|---|---|---|---|---|
| 2016-12-28-rmn-re-history | green | ok | none | 0 | ok | ok | ok |
| 2021-05-10-vanderbilt-shortener | green | ok | es_ingest_vanderbilt.py | 0 | ok (12 documented 1970 fallbacks) | ok | ok |
| 2021-10-30-demowiki | green | ok | none | 0 | ok | ok | missing: raw/sweep.json, 7 raw/history_*.html |
| 2022-03-01-jsonhero | green | ok | none | 0 | ok | ok | title stale (data/jsonhero/) |
| 2022-05-14-jqp-vercel | green | ok | none | 0 | ok | ok | ok |
| 2022-08-09-github-forensics | green | temp/build_rollup_w8.py (documented) | none | 0 | ok | ok | inventory omits 20 raw files (checksummed) |
| 2023-11-14-hfspace-proxies | green | raw/ missing (never existed) | none | 0 | ok | ok | inventories spaces.jsonl, on disk as events.jsonl |
| 2025-03-04-rubygems-goimport-campaign | green | ok | es_ingest_gems.py, es_ingest_jfrog.py | 0 | ok (2 epoch placeholders documented) | ok | ok |
| 2025-05-15-hf-tampering-check | green | ok | none | 0 | ok | ok | cites progress.log, never existed |
| 2025-12-04-urlquery-marker-sweep | regen | ok | none | 0 | ok | ok | artifacts section stale post-21312cf |
| 2026-02-01-agent-convo-venues | regen | ok | none | 0 | ok | ok | Files section stale (renames) |
| 2026-02-14-md-succ-ai | green | ok | none | 0 | ok | ok | ok |
| 2026-03-07-march7-rce-modality | green | ok | es_ingest_march7.py | 0 | ok | ok | raw/manifest.json covers 18/24 files, old path prefix |
| 2026-03-07-timeline-anchors | regen | ok | none | 0 | ok | ok | raw/manifest.sha256 names pre-normalize file |
| 2026-03-11-dse-wiki-verification | green | ok | none | 0 | ok | ok | ok |
| 2026-03-12-paste-archive-gap | green | ok | none | 0 | **MISMATCH** (prefix 2026-03-12, min event 2018-05-09; documented gap period) | ok | stale paths/counts, names missing progress.log |
| 2026-05-05-gomod-hunt | regen | ok | none | 0 | ok | ok | ok |
| 2026-05-11-july6-staging | regen | ok | none | 0 | ok | ok | Files section pre-normalization names |
| 2026-05-11-osv | regen | ok | none | 0 | ok (1238/1956 sentinel 1970 documented) | ok | 2 logs never committed; sweep jsonls intentionally merged |
| 2026-05-12-university-shorteners-events | green | raw/ missing (never existed) | none | **1522 (all records)** | ok | ok | inventories old paths + old filename |
| 2026-05-12-webhook-deaddrops | regen | raw/ missing | none | 0 | ok | ok | inventories stale working filename |
| 2026-05-17-collusion-wiki | regen | ok | none | 0 | ok | ok | .gz companions unlisted; 2 PROVENANCE hashes copied from stale manifest; false "passed" claim |
| 2026-05-17-iowacollab-pastes | regen | ok | none | 0 | ok | ok | 2 raw files unlisted; names dataset.jsonl (renamed) |
| 2026-05-26-paste-linuxiarz | green | root temp/ (documented) | es_ingest_paste.py | 0 | ok | ok | raw/sweep.json not in PROVENANCE |
| 2026-05-27-paste-archive | green | ok | es_ingest_paste_archive.py | 0 | ok | ok | omits 55 anna bodies + 4 manifests; narrative says bodies unavailable (stale) |
| 2026-06-04-admin-deletions | regen | ok | none | 0 | ok | ok | raw/STAGED-UNWIND-2026-09-28.md not in PROVENANCE |
| 2026-06-17-reverse-tunnels | green | ok | none | 0 | ok | ok | ok (see .pyc decision below) |
| 2026-06-20-powerbi-fronting | green | ok | none | 0 | ok | ok | ok |
| 2026-07-07-exfil-endpoint-pivot | regen | ok | none | 0 | ok | ok | names identifiers.jsonl (never existed); dataset value vs PROVENANCE |
| 2026-07-07-july7-gem-forensics | green | ok | none | 0 | ok (54 sentinel 1970 documented) | ok | 2 retired shards inventoried; events.jsonl not in table; title stale |
| 2026-07-07-july7-wave | green | root __pycache__/ (ignored) | es_ingest_july7.py | 0 | **MISMATCH-understood** (2 May-27 events, documented) | ok | stale gemstuffer CSV path; Method describes removed progress.log |
| 2026-07-07-xss-ssti-census | green | raw/ missing (documented, fully derived) | none | 0 | ok (sentinels documented) | ok | payloads.jsonl, progress.log inventoried-but-missing; title stale |
| 2026-07-21-transfer-test-family | regen | raw/ missing | none | 0 | ok (1 epoch placeholder) | ok | inventories old jsonl name |
| 2026-08-10-wayback-gem-capture | regen | ok | none | 0 | ok | ok | inventories deleted hits.jsonl/progress.log; header stale |
| 2026-08-19-tantive-space | green | ok | none | 0 | ok | ok | ok |
| 2026-08-21-public-board | green | root __pycache__/ (ignored) | es_ingest_public_board.py | 0 | ok | ok | ok |
| 2026-08-25-commonlog-scan | regen | ok | none | 0 | ok | ok | messages.jsonl→events.jsonl rename not reflected; 3 stale names |
| 2026-09-03-collusion-manifest | green | ok | none | 0 | ok | ok | ok |
| 2026-09-04-thecolony-ai | green | ok | none | 0 | ok | ok | 3 cascade_rubygems_*.json not in Files inventory |
| 2026-09-05-fieldnotes-gem | green | ok | none | 0 | ok | ok | ok |
| 2026-09-05-termina-digital | green | ok | none | 0 | ok | ok | RSS 10-vs-9 noted inline; wayback_manifest file values carry pre-rename prefix (labels-level) |
| 2026-09-12-jsonhero-docs-archive | green | ok | es_ingest_jsonhero_archive.py | 0 | ok | ok | __pycache__/ transient, uninventoried |
| 2026-09-27-rmn-re | green | root temp/build_rollup_w8.py (documented) | none | 0 | **MISMATCH** (prefix = crawl date 2026-09-27, min event 2016-12-28; documented) | ok | ok |
| 2026-09-27-rmn-re-linktable | green | raw/ missing (documented) | none | 0 | **MISMATCH** (prefix = materialization date, event 2026-06-19; documented) | ok | ok |
| 2026-09-28-agent-surfaces | green | root __pycache__/ (ignored) | es_ingest_agent_surfaces.py | 0 | ok | ok | progress.log prose-inventoried, never tracked; old paths cited |
| 2026-09-28-agents-relay-sweep | regen | raw/ missing | none | 0 | ok | ok (validated via jsonschema; worker reported validate_schema.py transiently missing — exists now) | no inventory table |
| 2026-09-28-counter-channel | green | ok | none | 0 | ok | ok | ok |
| 2026-09-28-dockerhub-trojan-images | green | root SHA256SUMS.txt (tracked duplicate) | none | 0 | ok | ok | fetch_stdout.log, progress.log named but never in git |
| 2026-09-28-jsonhero-docs | green | root temp/ (documented) | none | 0 | ok | ok | 2 stale relative paths; header stale |
| 2026-09-28-ludism-wikis | green | ok | es_ingest_ludism.py | 0 | ok | ok | __pycache__/ transient; 2 missing raw/ prefixes (doc only) |
| 2026-09-28-nsi-venue-sweep | regen | raw/ missing | none | 0 | ok | ok | names hits.jsonl (→events.jsonl) |
| 2026-09-28-open-data-api-venues | regen | raw/ missing | none | 0 | ok | ok | Sources use pre-normalization paths (content exists at renamed dirs) |
| 2026-09-28-pastebin-cluster-sweep | regen | raw/ missing | none | 0 | ok | ok | names sweep.jsonl/progress.log (renamed/never-existed) |
| 2026-09-28-pastebin-pivot | regen | ok | none | 0 | ok | ok | title + evidence paths pre-rename |
| 2026-09-28-pxweb-national-stats | regen | ok | none | 0 | ok (12/12 resolve) | ok | internal paths stale pre-normalization |
| 2026-09-28-university-shorteners | regen | ok | none | **12** | ok | ok | evidence paths stale; wayback lane + captures uninventoried |
| 2026-09-28-university-shorteners-batch2 | regen | ok | none | **1** | ok | ok | Contents section pre-normalization |
| 2026-09-28-university-shorteners-batch3 | regen | ok | none | **3** | ok | ok | Contents section pre-normalization; 6 html captures + events.jsonl unlisted |
| 2026-09-28-uoft-shorteners | green | ok | none | 0 | ok | ok | ok |
| 2026-09-28-worldpoverty-task-family | regen | ok | none | 0 | ok | ok | inventories old jsonl names |
| 2026-09-28-yourls-resweep | regen | ok | none | **31** | ok | ok | inventories pre-normalization paths |
| 2026-09-29-forged-flag-hunt | regen | ok | none | 0 | **MISMATCH-understood** (all 1970 sentinels; event.created 2026-09-29 matches) | ok | describes pre-normalization layout |
| 2026-09-29-gem-temporal-pivot | green | ok | none | 0 | ok (all 1970 sentinels documented; event.created matches) | ok | header + dataset value staleness (cosmetic) |
| 2026-09-29-separate-eval-test | green | ok | none | 0 | **MISMATCH-understood** (all 1970 sentinels, documented backfill) | ok | nested SHA256SUMS unlisted (cosmetic) |

## Proposed fix list (Christopher's decision — NOT executed)

### Stale `file` pointers — 1,569 records, 5 collections
- `2026-05-12-university-shorteners-events`: 1,522 pointers → pre-normalization
  `data/university-shorteners{,-batch2,-batch3}/` paths (deleted by 84edfb3).
  All bytes exist under `data/2026-09-28-university-shorteners{,-batch2,-batch3}/raw/`.
  13 distinct bad path values. Mechanical rewrite.
- `2026-09-28-university-shorteners`: 12 pointers missing `raw/` prefix.
- `2026-09-28-university-shorteners-batch3`: 3 pointers missing `raw/` prefix.
- `2026-09-28-university-shorteners-batch2`: 1 pointer missing `raw/` prefix.
- `2026-09-28-yourls-resweep`: 31 pointers → `data/yourls-resweep-2026-09-28/evidence/…`
  should be `data/2026-09-28-yourls-resweep/raw/evidence/…`.
- Also labels-level (not top-level, not counted): termina-digital
  `wayback_manifest.json` values, wayback-gem-capture `labels.saved_file`,
  exfil-endpoint-pivot `labels.local_saved_copy`.

### Date-prefix decisions
- `2026-03-12-paste-archive-gap`: prefix describes gap period; min real event
  2018-05-09. Rename candidate or documented exception.
- `2026-09-27-rmn-re`: prefix = crawl date; content spans 2016-12→2026-09.
- `2026-09-27-rmn-re-linktable`: prefix = materialization date; event 2026-06-19.
- `2026-07-07-july7-wave`: 2 May-27 events — documented, keep as-is.
- `2026-09-29-forged-flag-hunt`, `2026-09-29-separate-eval-test`: 1970 sentinels,
  documented — keep as-is.

### Provenance rewrites (doc-only, ~40 collections list stale paths/names)
Largest single pass. Mechanical: old dir names → dated names, `raw/` prefixes,
renamed jsonl names. Includes paste-archive's stale "bodies unavailable"
narrative and collusion-wiki's false "sha256sum -c passed" claim.

### Layout exceptions to ratify or fix
- `raw/` missing: hfspace-proxies, university-shorteners-events, xss-ssti-census
  (derived), webhook-deaddrops, transfer-test-family, open-data-api-venues,
  nsi-venue-sweep, pastebin-cluster-sweep, rmn-re-linktable — document as
  canonical exceptions or add real raw layers.
- `temp/` at collection root: rmn-re, jsonhero-docs, paste-linuxiarz, ludism-wikis.
- Root `__pycache__/`: transient, git-ignored; remove after script work settles.
- dockerhub `SHA256SUMS.txt`: tracked byte-identical duplicate of SHA256SUMS —
  delete.
- reverse-tunnels `.pyc`: ignored, present locally, in SHA256SUMS + PROVENANCE.
  Clean checkout → manifest entry for a missing file. Decide: force-add as
  curated artifact, or drop its provenance/checksum claim and discard.

## Systemic patterns

1. **Manifests were born stale.** The dominant defect class: SHA256SUMS hashes
   that never matched any committed bytes, carried through the 84edfb3 layout
   update and the 21312cf normalization (path-only manifest edits). Bytes were
   stable throughout — the defect is manifest-side only.
2. **Ghost `progress.log` entries.** ~20 manifests carried entries for a run log
   that was never committed in any collection. All dropped.
3. **PROVENANCE.md wasn't updated by the rename commits.** ~40 collections have
   stale paths/names; the bytes and manifests are now canonical, the docs lag.
4. **Pointers weren't rewritten on the raw/ move.** 21312cf moved files into
   `raw/` without updating `file` values — the source of all 1,569 stale pointers.
5. **Shared-index commit races.** Several parallel workers' commits swept
   siblings' staged files (fe14d36, c5f5a3c, 059253f, 139bf73). Content verified
   correct everywhere; attribution mixed. History left alone per the no-rewrite
   rule.
6. **Incident:** a worker's `git reset --soft` orphaned the condense crew's commit
   21e2372 ("condense: move es_ingest_termina.py…"). Content intact in the working
   tree / index (diff vs orphaned commit is empty); the condense crew is actively
   committing on the branch and must recommit that file. Not touched here.

## Retained exceptions (no action)

- Documented 1970 sentinels (rubygems 2, vanderbilt 12, osv 1238, xss-ssti-census,
  gem-forensics 54, gem-temporal-pivot all, forged-flag-hunt all,
  separate-eval-test all, transfer-test-family 1).
- Single-collection root build scripts: vanderbilt, rubygems (gems+jfrog),
  march7, paste-archive, paste-linuxiarz, july7, ludism, agent-surfaces,
  jsonhero-archive, counter-channel (via_script manifest entry).
- `temp/build_rollup_w8.py` in rmn-re and github-forensics: committed, documented.
- Genuine `rollup.jsonl` layers kept where aggregates exist (termina-digital,
  paste-linuxiarz, ludism-wikis, agent-surfaces, jsonhero-docs-archive,
  jsonhero-docs, admin-deletions, july7-wave).

## Validation note

Repo-wide validator reports 141,804 records / 84 event files / 0 violations
repeatedly. The count excludes collection-root staged rollup intermediates
(e.g. university-shorteners' `raw/staged_rollup/`) by design.
