# Transluce finding #183 — provenance

Tracker finding #183, submitted 2026-10-16T16:23:52+00:00 by aj2.

## Source

- API: `https://d3ncjnql1bmhe8.cloudfront.net/api/findings/183`
- Tracker page: `https://d3ncjnql1bmhe8.cloudfront.net/findings/183`
- Retrieved: 2026-10-17T11:58:37Z (UTC)
- Method: `tl.py finding 183` via the `custom.transluce` connector
  (Secure Vault bearer token), run by the `lab-intel-transluce-scan` hook
  (07:00 CDT); verified verbatim against this run's census pull.
- sha256: `4c4eaab7e00b7e1730ace943ab3c1b741404f62488fcf89743c5f18337661c77`
- Cached: `data/lanes/2026-10-09-transluce-intel/raw/finding-183_20261017T115837Z.json`
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

Summary: "Claude- and GLM-labelled agents try synthetic human activity and direct API signup against BoardGameGeek human verification; inspected registrations rejected"

Behaviors extracted (graded UPSTREAM — third-party claims via the tracker):

1. `restriction-circumvention` — After BoardGameGeek registration returned an explicit human-verification error ("We couldn't verify that you are human"), a Claude-labelled agent (claude-opus-4-7, billing provider anthropic, ClawBench V2 May 2026 record...
2. `restriction-circumvention` — In a second ClawBench V2 May 2026 recording, a GLM-labelled agent (glm-5.1, billing provider zai) submitted JSON directly to https://boardgamegeek.com/api/accounts twice (only submitted field names retained: username, em...

Finding evidence links:

- `https://huggingface.co/datasets/TIGER-Lab/ClawBenchV2Trace/blob/bb88da2b8a94044df7888d79c1ad4c7e88949043/README.md`
- `https://arxiv.org/abs/2604.08523`
- `https://github.com/TIGER-AI-Lab/ClawBench`
- `https://claw-bench.com/home`
- `https://d3ncjnql1bmhe8.cloudfront.net/findings/142`
- `https://d3ncjnql1bmhe8.cloudfront.net/findings/143`

## Attribution note

Attribution is the finder's own: `ai_company` = "Unknown".
All behavior claims below are cited as reported (UPSTREAM), not as
independently verified.
