# Lane 3 live-check notes — 2026-10-27

## Slice

- Input: `data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv` (533 rows).
- Slice: all names sorted alphabetically (plain byte/codepoint sort, identical for these ASCII names), indices 266–398 inclusive = 133 names.
- First: `mini-max-pkg`. Last: `ssrf-self-852d86f8`.
- Names checked: 133. No name outside the slice was checked.

## Method (read-only)

- Tool: `curl` GET/HEAD only. No login, no account, no POST, no sessions. No fetched payload was executed. No code was cloned.
- Concurrency: 3 workers. Request starts to the same host were spaced at least 300 ms apart (task floor: 200 ms).
- RubyGems API: `GET https://rubygems.org/api/v1/gems/<name>.json`. On 200, the version list in `partial.json` (`rubygems_versions`) is the verbatim list from `GET https://rubygems.org/api/v1/versions/<name>.json`, in that endpoint's order, including per-platform duplicate entries (for example `pico_phone` returns 55 entries). On 404, `rubygems_versions` is null.
- RubyGems page: `GET https://rubygems.org/gems/<name>`, status recorded; the body was read only to test the owner-removed marker below and was not retained.
- Diffend: `GET https://my.diffend.io/gems/<name>`, status and content signal recorded.
- Source repo: the CSV's `source_code_uri` for that row, `HEAD` with a `GET` fallback (on 405/403/400 or no response), status only. Empty `source_code_uri` (68 rows) gives `source_status` null.

## Stub-vs-full marker (Diffend) — exact strings used

- **stub**: the page body contains the literal sentence `There are no computed diffs for this gem.`
- **full**: that sentence is absent AND the body contains a version-pair diff link of the form `/gems/<name>/<v1>/<v2>` (for example, the rails calibration page carries links such as `/gems/rails/8.1.3/8.1.4`).
- **gone**: Diffend HTTP 404/410. None observed — every Diffend request returned 200, even for gems gone from RubyGems.
- Redirect-to-index would have counted as stub. None observed.

## Per-host status tallies (133 names each, unless noted)

- RubyGems API (`rubygems.org/api/v1/gems/`): 200 × 10, 404 × 123.
- RubyGems page (`rubygems.org/gems/`): 200 × 133. Note: a page HTTP 200 does NOT mean the gem is installable — 123 of these names are API-404, and their pages render yanked/removed notices at 200. API status is the gem-liveness signal.
- Diffend (`my.diffend.io/gems/`): 200 × 133. Content: stub × 124, full × 9, gone × 0.
- Source repos (65 non-empty URIs; 68 rows have no `source_code_uri`):
  - `github.com`: 200 × 3, 404 × 61.
  - `gitlab.neatnerds.be`: 200 × 1.
  - Overall source: 200 × 4, 404 × 61, null (no URI) × 68.

## Live gems in this slice (API 200, 10)

Latest version is from the gems API JSON; count is the length of the verbatim versions-endpoint list.

| name | latest | versions listed |
| --- | --- | --- |
| minitest-hashdiff | 0.1.1 | 1 |
| pico_phone | 0.8.2 | 55 |
| query-stream | 1.4.0 | 2 |
| rosett-ai | 1.8.1 | 7 |
| rubocop-metz | 0.6.0 | 2 |
| shirobai | 2026.1027.0730 | 22 |
| shirobai-performance | 2026.1027.0730 | 9 |
| shirobai-rails | 2026.1027.0730 | 9 |
| shirobai-rspec | 2026.1027.0730 | 9 |
| sportdb-parser | 0.8.0 | 51 |

All other 123 names are API-404 (gone from the RubyGems API).

## Diffend full pages (9)

`pico_phone`, `query-stream`, `rosett-ai`, `rubocop-metz`, `shirobai`, `shirobai-performance`, `shirobai-rails`, `shirobai-rspec`, `sportdb-parser` — exactly the API-200 names except `minitest-hashdiff`, whose single version has no version pair to diff, so its Diffend page is a stub. All 124 stub pages carry the no-computed-diffs sentence.

## Artifact URLs (102 total, 89 names with at least one)

Rule, applied mechanically and verified against the statuses:

- RubyGems page URL included iff page HTTP 200 AND the body does NOT contain `has been removed by its owner` (the owner-removed reservation notice). 44 pages carry that notice and were excluded despite HTTP 200, leaving 89 page artifacts. Pages showing yanked versions without that notice count as live pages.
- Diffend URL included iff content is `full` (9).
- Source URI included iff source status is 200–399 (4).
- Total: 89 + 9 + 4 = 102. The 9 full-Diffend and 4 live-source names are all inside the 89 page-live names, so 89 distinct names carry artifacts.

## 429 / unchecked cases

- None. Zero HTTP 429 responses were seen from any host, so no host was stopped and no name is marked `unchecked` in `partial.json`.
- Two transient failures, both resolved by recheck (not left unchecked): `nano-clean-sys` and `nano-max-box` first returned a curl failure (no HTTP status) for the RubyGems page. Three retries each then returned HTTP 200 with no owner-removed marker, so both are recorded as page 200 with their page URLs in `artifact_urls`. Their API status is 404 and their source repos are 404 in both the main run and the record.

## Credential-shaped values

- Presence only, no values copied: probed Diffend pages carry a per-page anti-CSRF meta token, and probed yanked RubyGems pages carry a gem SHA-256 checksum field. These are page furniture, not leaked credentials. No page-body values appear in `partial.json` or in these notes, and page bodies were not retained.

## Verification performed

- `partial.json` parses, holds exactly 133 objects, and its name list exactly equals the slice (first `mini-max-pkg`, last `ssrf-self-852d86f8`, no extras, no gaps).
- `artifact_urls` were re-derived from the statuses (page-live rule, Diffend full, source 200–399) and match the file.
- No other directory was touched; no git add, commit, or push was run; no Factum writes were made.
