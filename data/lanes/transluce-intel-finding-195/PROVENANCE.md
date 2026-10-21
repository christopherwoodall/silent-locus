# Transluce finding #195 — provenance

Tracker finding #195, submitted 2026-10-21T06:03:21+00:00 by Ayush Bhardwaj.

## Source

- API: `https://d3ncjnql1bmhe8.cloudfront.net/api/findings/195`
- Tracker page: `https://d3ncjnql1bmhe8.cloudfront.net/findings/195`
- Retrieved: 2026-10-21T11:57:00Z (UTC)
- Method: authenticated GET /api/findings/195 via bin/tl.py (custom.transluce connector, Secure Vault bearer token, curl), cached 2026-10-21T11:57:00Z by the 07:02 CDT daily pull (transluce-api-pull-daily); verbatim bytes copied into this lane's raw/ for self-containment
- sha256: `198519f684a487e890d692889aab9cf06e2be011869fb0724a964f691fc31877`
- Cached: `data/lanes/transluce-intel-finding-195/raw/finding-195_20261021T115700Z.json` (with `.sha256`
  and `.PROVENANCE.txt`).

## Census verification (this run, 2026-10-21 08:40 CDT)

- Full paginated census `GET /api/findings?limit=100&offset={0,100}` at
  2026-10-21T14:30Z: 128 findings, IDs 36..196 (finding #196 created
  2026-10-21T13:25:10Z).
- vs 2026-10-20 watermark (finding 193): deltas are NEW findings 194, 195,
  196; no dropped IDs. The only pre-existing content change is finding
  152 (updated_at 2026-10-20T00:27:01Z), already ingested as
  `transluce-intel-finding-152-update/` on 2026-10-20.
- Pre-ingest dedup: grep over immutable exported batches `data/records/`
  for each new tracker URL (`findings/194`, `findings/195`,
  `findings/196`): zero hits; all three postdate prior ingests.

## Content

Summary: "Research lead: cityb repeats an 841-byte 'dead-drop.local-carrier' JSON on Ubuntu Paste; a matching trace appears in an MDShare probe. Consistent with carrier testing, but AI involvement, covert communication and harm are unconfirmed."

Category note (docs/taxonomy/behavior-categories.md checked, 2026-10-21): no existing category describes paste-bin carrier-probe repetition; no new category was invented (per the finding-193 precedent). The unsanctioned public-hosting writes fit the existing lab-derived category unsanctioned-communication (public file-hosting used for communication), and the unconfirmed-AI limits ride in the record description.

Behaviors extracted (graded UPSTREAM — third-party claims via the tracker):

1. `unsanctioned-communication` — Four preserved Ubuntu Paste bodies (4553112, 4553114, 4553119 and 4553122) contain the same 841-byte JSON after trimming whitespace (sha256 70a254cc7fe7d3d112950cf77a9dd6811750a8c3406551b507a44038e694...

## Attribution note

Attribution is the finder's own: ai_company = "Unknown"; untapped_source = "No"; harm_level = "No/negligible harm". The finding explicitly frames this as a low-confidence source/protocol lead: AI involvement, covert communication and harm are all unconfirmed. All behavior claims below are cited as reported (UPSTREAM), not as independently verified.
