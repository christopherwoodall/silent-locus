# PROVENANCE.md — HF tampering check (LEAD 6 of 6)

Lane: Hugging Face metadata/history-only tampering check on `sunblaze-ucb/cybergym`
      and ExploitGym-named artifacts, against the July 10–13, 2026 breach window.
Date: 2026-09-28 (retrieval timestamps below, all UTC)
Method: public Hugging Face Hub API (JSON) + one dataset-discussion page; no login,
        no tokens, no corpus download (236GB untouched), no parquet/arrow shards,
        no image pulls, no file contents beyond API metadata.

## Endpoints fetched (in order)

1. `https://huggingface.co/api/datasets/sunblaze-ucb/cybergym`
   → `dataset-meta-20260928T233536Z.json` (full file listing: 7,538 siblings)
2. `https://huggingface.co/api/datasets/sunblaze-ucb/cybergym/commits/main?limit=100`
   → `commits-main.json`
3. `https://huggingface.co/api/datasets/sunblaze-ucb/cybergym/refs`
   → branch list (main only) + automated `refs/convert/parquet` ref
4. `https://huggingface.co/api/datasets/sunblaze-ucb/cybergym/commits/refs%2Fconvert%2Fparquet?limit=5`
   → `commits-parquet.json`
5. `https://huggingface.co/api/datasets?search=exploitgym&limit=20`
   `https://huggingface.co/api/models?search=exploitgym&limit=20`
   `https://huggingface.co/api/spaces?search=exploitgym&limit=20`
   → 3 user datasets found, 0 models, 0 spaces
6. Commit histories (`commits/main?limit=50`) for each of:
   - `shirman/exploitgym-results` → `commits-shirman_exploitgym-results.json`
   - `shirman/exploitgym-answers` → `commits-shirman_exploitgym-answers.json`
   - `SpeckledCerberus/exploitgym-answers` → `commits-SpeckledCerberus_exploitgym-answers.json`
   Metadata snapshots → `meta-shirman_exploitgym-results.json`,
   `meta-SpeckledCerberus_exploitgym-answers.json`
7. `https://huggingface.co/api/datasets?author=sunblaze-ucb&limit=50`
   → `author-repos.json` (8 org datasets; lastModified sweep)
8. `https://huggingface.co/api/datasets/sunblaze-ucb/cybergym/discussions?p=0`
   → `discussions-p0.json`; discussion #1 detail
   → `discussion-1.json`
9. Summary inventory → `file-listing-summary.json` (derived from #1)

## Analysis note

- `notes/analyst-note-hf-tampering-check-2026-09-28.md`

## Retrieval log

See `progress.log` for the ordered fetch log with per-file timestamps.

## Schema normalization 2026-09-29 (worker W3)

- Transform: `temp/build_events_w3_hf.py` (repo root passed as argv[1]).
- Grain (21 event records):
  - 15 commits -> `artifact_observation` (1 main + 1 refs/convert/parquet on
    sunblaze-ucb/cybergym; 4 shirman/exploitgym-answers; 4 shirman/exploitgym-results;
    5 SpeckledCerberus/exploitgym-answers), `@timestamp` = commit date
    (`labels.timestamp_source = "labels:commit.date"`)
  - 1 discussion thread (#1, "Distribution across Programming Languages") ->
    `artifact_observation`; `discussions-p1.json` is an empty page (no records)
  - 5 metadata snapshots -> `extraction` (dataset-meta, 2 repo metas,
    file-listing-summary, author-repos sweep of 8 org datasets),
    `@timestamp` = documented retrieval date 2026-09-28
  - `MANIFEST.sha256` excluded from records (lane file inventory; superseded by
    the regenerated SHA256SUMS below)
- Finding preserved in the rollup: ZERO commits fall in the July 10-13, 2026
  breach window on any of the 4 repos.
- Fingerprint identity strings:
  - commits: `sha256("hf-commit:<repo>:<sha>")`
  - discussions: `sha256("hf-discussion:<repo>#<num>")`
  - snapshots: `sha256("hf-meta-snapshot:<key>")`
  - rollup: `sha256("hf-repo-rollup:<repo>")`
  Reference method verified against data/2023-11-14-hfspace-proxies
  (sha256("TheNacken/python-cors-proxy") -> `14c645d9…efbe94`).
- Rollup: `rollup.jsonl` with 4 `repo_commit_rollup` rows (NEW kind, listed in
  notes/dir-triage-W3.md) — per-repo commit counts, first/last, and
  `rollup.in_breach_window_2026_07_10_13` (0 for all four). `event.dataset`
  suffixed `-rollup`.
- `event.dataset = "2025-05-15-hf-tampering-check"`; `event.created` = build time.

## Orphan run-log reconciliation (preservation-first)

The following original logs were relocated byte-for-byte from `data/2025-05-14-hf-tampering-check/` into this collection. They are historical run evidence, not additional positive findings or new collection events. Original source folders were removed only after their logs were copied and SHA-256 verified.

- `data/2025-05-14-hf-tampering-check/raw/progress.log` -> `raw/run-logs/2025-05-14-hf-tampering-check-progress.log`; SHA-256 `f59ef634cab2e04d2987f37fdba07e86a97e4f47ce01a67924dbb594a61e1d82`.

### Historical checksum conflicts (unresolved)

Bytewise verification of `SHA256SUMS` currently reports 4 mismatched historical entries in this collection; 4 match their recorded hashes only after CRLF-to-LF conversion. This is consistent with a line-ending change, but original evidence and recorded historical hashes were not rewritten. The newly recovered log entries were independently verified byte-for-byte against their source SHA-256 and match the new manifest lines. To enumerate all mismatches locally, run `sha256sum -c SHA256SUMS` from this collection directory. 
