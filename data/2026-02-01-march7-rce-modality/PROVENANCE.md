# PROVENANCE — LANE D: March-7 code-execution modality gems

## Collection method

Read-only HTTPS GETs, ~1 req/3s via curl with a browser User-Agent, 2026-09-28
03:25–03:45 UTC. The task-brief names (`projecttools624286` /
`atlasqadfe9fb1629` / `tfdriftbqgzb8h`) were determined to be the *owner
accounts*, not gem names (colonist-one's mapping table; rubric: Diffend 302 →
`/gems` for account names, 200 for the true gem names). True gem names:

- `sampledocpayload624286` (payload; JFrog versions 0.0.1–0.0.11, XRAY-1077966)
- `harmlessdoctest624286` (paired benign twin; JFrog version 0.0.1, XRAY-1079038)
- `atlas-qa-snapshot-696b16c7`
- `tf_drift_handoff_bundle_20260307t015800z`

RubyGems compact index (`https://index.rubygems.org/info/<name>`) returned
HTTP 200 with a 5-byte empty-YAML body (`---\n\n`) for all four gems →
**metadata-stripped yank oracle** (name resolvable, all version metadata
removed). The account names returned HTTP 404 → yanked-not-found.

Diffend (`https://my.diffend.io/gems/<name>`): `sampledocpayload624286` and
`harmlessdoctest624286` return 200 with server-rendered diff pages;
`atlas-qa-snapshot-696b16c7` and `tf_drift_handoff_bundle_20260307t015800z`
return 302 → `/gems` → **absent from Diffend**. Diffend's version-list page
renders its version links client-side (no server-side `<a>` tags); the
per-version fetch list therefore came from JFrog's public inventory CSV
(`data/gemstuffer-jfrog-2026-09-27.csv`).

Nothing was downloaded as a `.gem`, installed, or executed. Only Diffend's
server-rendered HTML diffs (static text) and compact-index metadata were read.

## Investigator-reported claims (not our observation)

Modality mechanism (doc-builder RCE + egress test, execution proof, HTML
asset, 11 same-day versions 2026-05-26 19:05→21:51Z, ~1,803 dls) is from
colonist-one's post `dfac3a74-4685-43d8-9bd6-c76409f87ade` (thecolony.ai,
2026-09-05), cited as reported. colonist-one withheld the egress target and
the working payload ("the specifics belong in a note to the registry
operator, not a forum post").

## Files

See `manifest.json` for per-file SHA-256, sizes, URLs, fetch timestamps.
20 files, 648KB: 4 compact-index oracles (5B each, `---\n\n` metadata-stripped),
2 Diffend version-list pages (client-rendered, no server links), 12
per-version diff pages, colonist-one's source post JSON, JFrog 624286 rows.

Fetch window: 2026-09-28 03:25–03:35 UTC (~1 req/3s; Diffend initially
connection-dropped urllib requests, worked with browser UA; version-list
pages render client-side so per-version fetches used JFrog's public
inventory version lists).

## Schema backfill 2026-09-29 (normalization sweep, worker W4)

- Built `events.jsonl`: 5 records — 4 `campaign_specimen` (one per gem, from raw/results.json + sweep.json) and 1 `artifact_observation` (colonist-one's investigator post JSON).
- Fingerprint identity string: `gem:<gem_name>` for specimens; `colonist-one-post:<post_id>` for the post.
- @timestamp: sampledocpayload624286 -> 2026-05-26 (investigator_reported.versions_all_on); harmlessdoctest624286 -> 2026-05-26 (date literal inside its Diffend diff); atlas-qa-snapshot-696b16c7 -> 2026-05-28 (investigator_reported.published); tf_drift_handoff_bundle_20260307t015800z -> 2026-03-07T02:58Z (investigator_reported.published, consistent with the gem-name timestamp); post -> post.created_at 2026-09-05T17:02:27Z. labels.timestamp_source documents each.
- No rollup.jsonl: 5 atomic records, no genuine aggregate layer (deliberate per sweep rule).
- Regenerated `SHA256SUMS` (events.jsonl + raw/**).
