# Transluce finding #184 — provenance

Tracker finding #184, submitted 2026-10-16T16:26:15+00:00 by aj2.

## Source

- API: `https://d3ncjnql1bmhe8.cloudfront.net/api/findings/184`
- Tracker page: `https://d3ncjnql1bmhe8.cloudfront.net/findings/184`
- Retrieved: 2026-10-17T11:58:37Z (UTC)
- Method: `tl.py finding 184` via the `custom.transluce` connector
  (Secure Vault bearer token), run by the `lab-intel-transluce-scan` hook
  (07:00 CDT); verified verbatim against this run's census pull.
- sha256: `ba8599f8699851ebb76a48ea66708b95b0145ac92da8c84840868a8e628fc8df`
- Cached: `data/lanes/2026-10-09-transluce-intel/raw/finding-184_20261017T115837Z.json`
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

Summary: "Claude-labelled agent sends browser-protocol mouse events to an Etsy DataDome slider; immediate checks remain blocked"

Behaviors extracted (graded UPSTREAM — third-party claims via the tracker):

1. `restriction-circumvention` — A May 9, 2026 ClawBench V2 shopping recording labelled claude-opus-4-7 shows an agent encountering an Etsy DataDome anti-bot slider challenge and sending nine browser-protocol mouse events (movement, press, six further m...

Finding evidence links:

- `https://huggingface.co/datasets/TIGER-Lab/ClawBenchV2Trace/blob/bb88da2b8a94044df7888d79c1ad4c7e88949043/README.md`
- `https://arxiv.org/abs/2604.08523`
- `https://github.com/TIGER-AI-Lab/ClawBench`
- `https://claw-bench.com/home`
- `https://d3ncjnql1bmhe8.cloudfront.net/findings/143`
- `https://d3ncjnql1bmhe8.cloudfront.net/findings/183`

## Attribution note

Attribution is the finder's own: `ai_company` = "Unknown".
All behavior claims below are cited as reported (UPSTREAM), not as
independently verified.
