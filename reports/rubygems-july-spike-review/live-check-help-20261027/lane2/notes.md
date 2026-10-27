# Lane 2 — live-check notes (2026-10-27)

## Slice and count

- Names checked: 133.
- Slice: all 533 CSV names sorted by plain byte sort, indices 133–265 inclusive.
- First name: `edoxen`. Last name: `mini-max-mod`.
- No name outside this slice was checked. Output: `partial.json` (133 objects, order = slice order).
- Method: read-only curl GET/HEAD only, no login, no POST, no sessions, no clones,
  no fetched payload executed. Max 3 concurrent; at least 250 ms between requests
  to the same host. RubyGems versions list came from
  `https://rubygems.org/api/v1/versions/<name>.json` (used for `rubygems_versions`
  and `rubygems_version_count`); the gem JSON supplied the latest version.
  Source check was HEAD with a GET fallback, status only.

## Per-host status tallies

- RubyGems API (`rubygems.org/api/v1/gems/<name>.json`): 200 = 5, 404 = 128.
  Live (API 200): `edoxen` (latest 0.8.4, 10 versions), `intranet-pictures`
  (2.2.0, 12), `jrjackson` (0.3.8, 50), `marlens-jira-api` (0.7.0, 5),
  `metz-scan` (0.6.0, 2).
- RubyGems gem page (`rubygems.org/gems/<name>`): HTTP 200 = 133.
  NOTE: RubyGems returns HTTP 200 even for removed gems, so status alone does
  not mean live. A second body check classified pages: live = 5 (exactly the
  API-200 names), removed-notice = 128. The removed pages carry one of two
  body phrases: "This gem is not currently hosted on RubyGems.org." or
  "This gem previously existed, but has been removed by its owner."
  `artifact_urls` includes a gem-page URL only when the page is body-live
  (`rubygems_page_live` = true in `partial.json`); the raw 200 status is
  still recorded in `rubygems_page_status`.
- Diffend (`my.diffend.io/gems/<name>`, curl without `-L` so redirects are visible):
  HTTP 200 = 132, HTTP 302 = 1.
  Content: full = 4 (`edoxen`, `intranet-pictures`, `marlens-jira-api`,
  `metz-scan`), stub = 128, gone = 1 (`klondikemarlen-jira-api`, 302 to the
  `/gems` index).
- Source repo (CSV `source_code_uri`, HEAD / fallback GET, status only):
  200 = 4, 301 = 1 (`edoxen`, `https://github.com/metanorma/edoxen`),
  404 = 66, null = 62 (62 rows have an empty `source_code_uri` in the CSV;
  null means "no URI supplied", not "unchecked").
  Source-200: `intranet-pictures` (bitbucket.org/ebling-mis/intranet-pictures),
  `klondikemarlen-jira-api` and `marlens-jira-api` (both point to
  github.com/klondikemarlen/jira-api), `metz-scan` (github.com/fuentesjr/metz-scan).

## Diffend stub-vs-full marker (exact)

- "full": HTTP 200 AND the page body contains a version-pair arrow matching
  `N.N.N → N.N.N` (e.g. `0.8.3 → 0.8.4`), with the stub phrase absent.
- "stub": HTTP 200 AND the body contains the exact phrase
  "There are no computed diffs for this gem."
  (One fallback rule was also applied: an HTTP 200 page with neither the stub
  phrase nor a version-pair arrow would be classed stub as empty of diff
  content; this fallback did not trigger — all 128 stubs carried the phrase.)
- "gone": HTTP 302 redirecting to `https://my.diffend.io/gems` (the index),
  or HTTP 404.

## Artifact URLs

- Total artifact URLs: 13.
- Breakdown: 5 live gem pages + 4 Diffend full pages + 4 live source URIs.
- Names with at least one artifact URL: `edoxen`, `intranet-pictures`,
  `jrjackson`, `klondikemarlen-jira-api` (source only), `marlens-jira-api`,
  `metz-scan`.

## 429 / unchecked cases

- None. Zero HTTP 429 responses from any host, so no host was blocked and no
  name is marked unchecked for any host. Every record has a concrete status
  for API, page, Diffend, and source (source null only where the CSV URI is empty).

## Credential-shaped values

- A pattern scan of fetched API/Diffend bodies for explicit key/secret/password
  assignments found 0 hits (Diffend's per-page csrf-token was excluded from
  this scan as a session token, and no values were copied anywhere). No
  credential-shaped values are present in the outputs.
