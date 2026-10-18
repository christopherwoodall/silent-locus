# Transluce finding #185 — provenance

Tracker finding #185, submitted 2026-10-16T19:04:55+00:00 by Ayush Bhardwaj.

## Source

- API: `https://d3ncjnql1bmhe8.cloudfront.net/api/findings/185`
- Tracker page: `https://d3ncjnql1bmhe8.cloudfront.net/findings/185`
- Retrieved: 2026-10-17T11:58:37Z (UTC)
- Method: `tl.py finding 185` via the `custom.transluce` connector
  (Secure Vault bearer token), run by the `lab-intel-transluce-scan` hook
  (07:00 CDT); verified verbatim against this run's census pull.
- sha256: `9eee9deefcd65987bc30845cf8c04cd2e08fd202d3041b843ed3520e975336d2`
- Cached: `data/lanes/2026-10-09-transluce-intel/raw/finding-185_20261017T115837Z.json`
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

Summary: "Sep 20, 2026: a self-described “Green AI Bot” posted a UseMod sandbox pulse, reverted 39 minutes later. Related public posts share its name and wording; AI authorship, cross-site identity and autonomous coordination remain unverified."

Behaviors extracted (graded UPSTREAM — third-party claims via the tracker):

1. `unapproved-edits` — UseMod SandBox revision 334 (20 Sep 2026, 00:49, editor hostname exit-04.tor.r0cket.net) posts a message from a self-described "Green AI Bot": "Green AI Bot pulse check, 20 Sep 2026. *burp* Sandbox noted; this will get r...

Finding evidence links:

- `https://www.usemod.org/cgi-bin/wiki.pl?action=browse&id=SandBox&revision=334`
- `https://www.usemod.org/cgi-bin/wiki.pl?action=history&id=SandBox`
- `https://openagentchat.net/p/green-ai-bot-not-a-swarm-remnant-03a210e4`
- `https://openagentchat.net/p/200-ok-is-not-a-conversation-f3268591`

## Attribution note

Attribution is the finder's own: `ai_company` = "Unknown".
All behavior claims below are cited as reported (UPSTREAM), not as
independently verified.
