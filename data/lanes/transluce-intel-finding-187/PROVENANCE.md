# Transluce finding #187 — provenance

Tracker finding #187, submitted 2026-10-16T19:05:58+00:00 by Ayush Bhardwaj.

## Source

- API: `https://d3ncjnql1bmhe8.cloudfront.net/api/findings/187`
- Tracker page: `https://d3ncjnql1bmhe8.cloudfront.net/findings/187`
- Retrieved: 2026-10-17T11:58:37Z (UTC)
- Method: `tl.py finding 187` via the `custom.transluce` connector
  (Secure Vault bearer token), run by the `lab-intel-transluce-scan` hook
  (07:00 CDT); verified verbatim against this run's census pull.
- sha256: `1d25483dd4a67126b522a559f51aade4cbe737badb391f3619494641fb059ef7`
- Cached: `data/lanes/2026-10-09-transluce-intel/raw/finding-187_20261017T115837Z.json`
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

Summary: "A May 2024 rmn.re shortlink maps to a USAA-branded path on updateaccount-mobileapp.ru, with 176 recorded clicks. This is a suspicious historical URL lead; destination behavior, credential theft and AI involvement are unverified."

Behaviors extracted (graded UPSTREAM — third-party claims via the tracker):

(none — the finding documents a suspicious historical URL lead only; no agent behavior is demonstrated, so no intel.behavior records were extracted)

Finding evidence links:

- `http://rmn.re/iu`

## Attribution note

Attribution is the finder's own: `ai_company` = "Unknown".
All behavior claims below are cited as reported (UPSTREAM), not as
independently verified.
