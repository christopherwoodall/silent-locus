# Lane 1 — live-check notes (2026-10-27)

Slice: CSV rows sorted by name (plain byte sort), indices 0–132 inclusive.
First name: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Last name: ecoportal-api-graphql
Names checked: 133 of 133. No name outside the slice was checked.

Method: read-only curl GET/HEAD only, max 3 concurrent, >=300 ms between
requests to the same host. No login, no POST, no sessions, no clones.
Page bodies were examined in memory for markers only and never saved.

## Per-host status tallies

RubyGems API (`GET https://rubygems.org/api/v1/gems/<name>.json`):
- 200: 5
- 404: 128
- 429/unchecked: 0

RubyGems gem page (`GET https://rubygems.org/gems/<name>`):
- 200: 133
- other: 0

Note: the API-404 + page-200 combination is the yanked-gem shape.
Spot-checked one such page (apex-black-fuzz-021): the page title carries
the gem name and the page text contains "yanked". API-200 gems (5):
apex-black-test-011 (latest 9.9.9, 1 version),
apex-blk-test-final (latest 0.0.1, 1 version),
apex-oidc-probe (latest 0.1.1, 1 version),
eco-helpers (latest 3.4.0, 277 versions),
ecoportal-api-graphql (latest 3.0.0, 49 versions).
Version counts come from the versions-list endpoint
(`GET https://rubygems.org/api/v1/versions/<name>.json`), fetched only
when the gem API returned 200; the single-gem API JSON carries no count
field, so `rubygems_versions` holds that list (null on API 404) and
`rubygems_version_count` / `rubygems_latest_version` are extra fields
alongside the specified ones.

Diffend (`GET https://my.diffend.io/gems/<name>`):
- status 200: 133
- content "stub": 131
- content "full": 2 (eco-helpers, ecoportal-api-graphql)
- content "gone": 0
- unchecked: 0

Source URI (CSV `source_code_uri`, HEAD with GET fallback, status only):
- no URI in CSV (source_status null): 130
- 200: 1 (apex-black-test-013, oast.online callback-style host)
- 404: 1 (apex-oidc-probe, github.com/attacker/repo)
- unchecked: 1 (see below)

Artifact URLs: 136 total across all records
(133 RubyGems page URLs + 2 Diffend full-content URLs + 1 live source URI).
Rule applied: page URL included iff page status is 200; Diffend URL
included iff content is "full"; source URI included iff its status is
2xx/3xx. Verified programmatically against the statuses in partial.json.

## Stub-vs-full marker (Diffend)

- "stub": the fetched page body contains the exact string
  `There are no computed diffs for this gem.`
  (Stub pages return HTTP 200, ~5.6 KB, and redirect nowhere.)
- "full": the body does NOT contain that string AND contains version-pair
  diff entries matching `\d+\.\d+(\.\d+)? → \d+\.\d+(\.\d+)?`
  (arrow-separated version pairs, e.g. a 2.x → 3.x pair on
  ecoportal-api-graphql). No "full" page contained the no-diffs string.
- "gone" was reserved for HTTP 404; no Diffend fetch returned 404.
  A redirect to the Diffend gems index would also have counted as stub;
  none occurred.

## Unchecked items / exceptions

- apex-black-test-001 — source_status "unchecked": its CSV source URI is
  an internal cloud-metadata address (metadata.aws.internal). It was
  deliberately NOT fetched, to avoid touching instance-metadata
  infrastructure. All other checks for this name completed normally
  (API 404, page 200, Diffend stub).
- No 429 responses were seen from any host, so no host was disabled and
  no name is unchecked for rate-limit reasons.
- No other fetch failures: no timeouts, no "unchecked" API/page/Diffend
  statuses.

## Credential-shaped values

Presence/count only, no values copied anywhere in the outputs:
- Diffend pages: all 133 successful (HTTP 200) page fetches carried a
  csrf-token meta field (count 133). Values were never stored; only the
  boolean presence flag (`csrf_present`) is recorded per record.
- RubyGems API JSON contains per-version hash fields; hashes were not
  copied into any output (only version numbers and counts were kept).
- No other credential-shaped values were observed in fetched responses.
  Fetched bodies were discarded after marker extraction.

## Output

- `partial.json`: JSON array, 133 objects, in slice order, names exactly
  equal to the slice (verified: no extras, no gaps; artifact URLs
  re-checked for consistency with the recorded statuses).
- Fields per object: name, rubygems_api_status, rubygems_page_status,
  rubygems_versions, diffend_status, diffend_content, source_uri,
  source_status, artifact_urls, plus extras rubygems_latest_version,
  rubygems_version_count, diffend_note, source_note, csrf_present.
