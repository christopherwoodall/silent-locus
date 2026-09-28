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
