# Transluce finding #152 — content update (versioned lane)

This lane records a VERSIONED UPDATE to tracker finding #152
(submitted 2026-10-04T22:22:49+00:00 by Linus). The original
finding-152 records (ingested 2026-10-09 as `intel.report`
observation_7a52d80629fa44a8b4521f0c83d602ef, actor
`agent:lane-ingest-2026-10-09-transluce-intel`, lane
`data/lanes/2026-10-09-transluce-intel/`) are NOT touched: history
is evidence. This lane adds one new `intel.report` record carrying
the verbatim NEW title/summary/description. No new `intel.behavior`
records: the change is a self-flagged duplicate note, and a note
adds no new behavior.

## Source

- API: `https://d3ncjnql1bmhe8.cloudfront.net/api/findings/152`
- Tracker page: `https://d3ncjnql1bmhe8.cloudfront.net/findings/152`
- Retrieved: 2026-10-20T13:50:18Z (UTC)
- Method: `~/workspace/custom-skills/local-transluce/bin/tl.py finding 152`
  (idempotent GET, `custom.transluce` connector, Secure Vault surrogate
  bearer token; no new tracker request was issued for the bundle build).
- sha256 (new version):
  `76477c4a8d285a61135bc542c2874816875922d96d22f787e023f44d2e2166f8`
  (verified at bundle build; cached pull at
  `data/lanes/transluce-intel-finding-152-update/raw/finding-152_20261020T135018Z.json`
  with sibling `.sha256` and `.PROVENANCE.txt`).
- Old version: item id 152 in
  `data/lanes/2026-10-09-transluce-intel/raw/findings-list-20261008.json`
  (census fetched 2026-10-08; old item bytes sha256
  `2bd5bbd1582c6dc6974703630f5dd2ffe75da71502892dfe955c8f6c85812da1`).

## What changed (observed)

- Description prepended with two lines (verbatim, 78 bytes):
  `Update 2026-10-19: I just realized that I've duplicated finding 110, my bad!`
  followed by a blank line. Verified: new description (3,387 chars) ==
  prepend + old description (3,309 chars) byte-for-byte; old remainder is
  unchanged.
- Summary IDENTICAL to the ingested version (273 chars; the
  2026 June 20 urlquery/Microlink API-key report).
- `form_version` 3 -> 4 (schema/form fields moved; observed).
- `harm_level` null -> `""` (empty string; a form-field nullability change,
  not a content judgment).
- `updated_at` 2026-10-05T05:20:48Z -> 2026-10-20T00:27:01Z (forward,
  consistent with the submitter edit).

The change is a submitter self-flag: finding 152 duplicates finding 110.
It does not add evidence, venue, or incident detail beyond the note itself.

## updated_at timeline (observed)

- 2026-10-08 census pull: updated_at `2026-10-05T05:20:48Z`,
  description 3,309 chars.
- 2026-10-20 07:02 CDT census (`findings-list_125_36-193_20261020T120205Z.json`)
  detected the change; 2026-10-20T13:50:18Z detail pull confirms
  updated_at `2026-10-20T00:27:01Z`, description 3,387 chars.

Forward move, consistent with a submitter edit. No anomaly.

## Attribution note

Attribution is the finder's own: `ai_company` = "Unknown". AI authorship,
coordination and the Microlink urlquery claim remain unverified per the
finding's own limits. All claims below are cited as reported (UPSTREAM),
not as independently verified.
