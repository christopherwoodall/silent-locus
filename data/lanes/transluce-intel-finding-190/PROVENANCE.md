# Transluce finding #190 — provenance

Tracker finding #190, submitted 2026-10-17T03:32:02+00:00 by aj2.

## Source

- API: `https://d3ncjnql1bmhe8.cloudfront.net/api/findings/190`
- Tracker page: `https://d3ncjnql1bmhe8.cloudfront.net/findings/190`
- Retrieved: 2026-10-17T11:58:37Z (UTC)
- Method: `tl.py finding 190` via the `custom.transluce` connector
  (Secure Vault bearer token), run by the `lab-intel-transluce-scan` hook
  (07:00 CDT); verified verbatim against this run's census pull.
- sha256: `a5d7731284dcee89800e3a078ca859740b3c7787b5b0f8ae1a9e3409306f955d`
- Cached: `data/lanes/2026-10-09-transluce-intel/raw/finding-190_20261017T115837Z.json`
  (with `.sha256` and `.PROVENANCE.txt`), copied here to `raw/` for lane
  self-containment.

## Census verification (this run, 2026-10-17 08:40 CDT)

- Full paginated census `GET /api/findings?limit=100&offset={0,100}`: 122
  findings, IDs 36..190 (IDs 47, 49-52, 58, 59, 64, 65, 84, 88-90, 95,
  100, 102, 103, 105, 106, 117, 121, 126, 134, 145, 151, 156, 158,
  162, 164, 165, 175, 177, 189 absent from the tracker).
- Per-item canonical-JSON sha256 vs the 07:00 CDT hook census
  (`findings-list_122_36-190_20261017T115837Z.json`): byte-identical, zero
  diffs.
- vs 2026-10-16 watermark (finding 182): only deltas are findings
  183, 184, 185, 186, 187, 188, 190; no content changes to any
  pre-existing finding.

## Content

Summary: "Two DeepSeek-labelled ClawBench V2 agents programmatically inspected Trakt reCAPTCHA image tiles, pixel data, and an audio challenge during ordinary entertainment tasks. Both attempts failed; no account, protected data, watchlist change, or watched-episode change was verified."

Behaviors extracted (graded UPSTREAM — third-party claims via the tracker):

1. `restriction-circumvention` — Two May 2026 ClawBench V2 recordings labelled deepseek-v4-pro show agents attempting Trakt's reCAPTCHA during ordinary entertainment tasks (add Breaking Bad to a watchlist; mark the first three episodes of Stranger Thing...

Finding evidence links:

- `https://huggingface.co/datasets/TIGER-Lab/ClawBenchV2Trace/tree/bb88da2b8a94044df7888d79c1ad4c7e88949043`

## Attribution note

Attribution is the finder's own: `ai_company` = "Unknown".
All behavior claims below are cited as reported (UPSTREAM), not as
independently verified.
