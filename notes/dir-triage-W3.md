# Dir triage — worker W3 (2026-09-29)

Normalization sweep over 5 dirs. All 5 completed: events.jsonl built, SHA256SUMS
regenerated, PROVENANCE.md carries a dated build note with the fingerprint
identity strings. No dir BLOCKED. Nothing pushed (per instructions).

## Row counts

| dir | events | rollup | notes |
|---|---|---|---|
| 2022-12-30-dse-wiki-verification | 21 | — | 6 downloads + 15 indicator sweeps (4 hit / 11 negative) |
| 2025-01-13-jsonhero-docs-archive | 6 | 1 | 1 recovered + 5 CDX negatives; rollup = recovery census |
| 2025-02-04-thecolony-ai | 55 | — | 10 posts, 9 searches, 6 cascades, 6 downloads, 24 sweep patterns |
| 2025-03-04-rubygems-goimport-campaign | 10,421 | 5 | nodes 2830, ioc-log 1262, hits 2339 (2 dup lines dropped), iocs 334, wayback 16, pins 615, jfrog 3025; rollup = per-day graph aggregates |
| 2025-05-14-hf-tampering-check | 21 | 4 | 15 commits, 1 discussion, 5 snapshots; rollup = per-repo commit summaries (0 commits in 2026-07-10/13 breach window) |

Rollup decisions: built ONLY where a genuine aggregate layer exists
(jsonhero census, gems per-day waves, hf per-repo summaries). dse-wiki and
thecolony are pure event streams — no rollup.jsonl, documented in PROVENANCE.

## New record_kinds (do NOT edit schema/README.md per instructions)

- `recovery_census` — one-row archive-recovery census rollup (jsonhero).
- `campaign_day_rollup` — per-day IOC-graph aggregates (gems rollup).
- `repo_commit_rollup` — per-repo commit summary with breach-window flag (hf rollup).

All event kinds used are existing registry kinds: `download`,
`corpus_hit`, `corpus_grep_negative`, `artifact_observation`,
`venue_finding`, `extraction`, `tag_liveness`, `graph_node`,
`diffend_harvest`, `wiki_ioc_pivot`, `wayback_capture`, `campaign_specimen`.

## Removal / rename / fix candidates (with evidence)

1. **Stale MANIFEST.sha256** — `data/2025-05-14-hf-tampering-check/raw/MANIFEST.sha256`
   lists `progress.log` (hash `b699414c…`), but no `progress.log` exists in
   `raw/` or the dir. The manifest also predates the regenerated SHA256SUMS.
   Candidate: lane owner regenerates or removes it. (Left untouched — read-only guard.)
2. **Stale path in manifest** — `data/2025-01-13-jsonhero-docs-archive/raw/manifest.json`,
   entry `swJMw8b6VwDC`, field `"file": "data/jsonhero-docs-archive/swJMw8b6VwDC.json"`.
   That path predates the date-prefix rename; the file now lives at
   `data/2025-01-13-jsonhero-docs-archive/raw/swJMw8b6VwDC.json`. Candidate: fix the path.
3. **Pending relocation note** — `data/2025-03-04-rubygems-goimport-campaign/PROVENANCE.md`
   still says "pending-relocation … will relocate to the sibling repo
   `../rubygems-goimport-campaign/`". If the move is still planned, the new
   `events.jsonl`/`rollup.jsonl` move with it; if cancelled, the note should go.
4. **Dir-date question** — `data/2022-12-30-dse-wiki-verification/`: no event in the
   collection is dated 2022-12-30 (earliest record event is 2026-03-11; the lane ran
   2026-09-27). Per `schema/collections.md` the date prefix = first event, so the
   prefix looks inherited from elsewhere. Flagging, not renaming (out of scope).
5. **Cascade count drift** — thecolony PROVENANCE closure says "5 cascade records"
   but `raw/` holds 6 cascade files (2 empty txt, 1 `[]` owner json, 3 "could not
   be found" json). events.jsonl carries all 6 as `tag_liveness`. No action needed;
   noting the drift.
6. **Stale dir path in lane note** — `notes/gem-hunt-dse-wiki-verification-2026-09-27.md`
   references `data/dse-wiki-verification-2026-09-27/`; the dir is now
   `data/2022-12-30-dse-wiki-verification/`. Cosmetic.

## Verification performed per dir

- `scripts/validate_schema.py`: 0 violations on all 8 files (5 events + 3 rollups).
- `sha256sum -c SHA256SUMS`: OK in all 5 dirs.
- Fingerprint method proven: recomputed sha256("TheNacken/python-cors-proxy") =
  `14c645d9…efbe94` exactly, before writing any record.
- Spot-checked ≥2 rows per dir against raw sources (report dates, capture
  timestamps, post authors, node ids, pin names, commit SHAs) — all match.
- In/out counts logged in each builder's stdout (gems: 2341 hit lines -> 2339
  after dropping 2 byte-identical dup lines; pins: 1217 lines -> 615 unique).

## Builders (repo root passed as argv[1]; no hardcoded paths)

- `temp/build_events_w3_dse_wiki.py`
- `temp/build_events_w3_jsonhero_archive.py`
- `temp/build_events_w3_thecolony.py`
- `temp/build_events_w3_gems.py`
- `temp/build_events_w3_hf.py`
