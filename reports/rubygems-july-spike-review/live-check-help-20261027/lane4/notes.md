# Lane 4 — live-check notes (2026-10-27)

## Slice

- Source: `data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv` (533 rows).
- Slice rule: names sorted alphabetically (plain byte sort), indices 399–532 inclusive.
- Names checked: **134**. First: `ssrf-test-1783405321`. Last: `yank-scope-test-1783410282`.
- No name outside this slice was checked or recorded. Output: `partial.json` in this directory (134 objects, slice order).

## Method

- Read-only GET/HEAD via curl only (this VM's egress proxy; python httpx avoided as broken here).
- Max 3 concurrent workers; a per-host timestamp lock enforced at least 200 ms between requests to the same host.
- RubyGems API: `GET https://rubygems.org/api/v1/gems/<name>.json`. RubyGems page: `GET https://rubygems.org/gems/<name>` (status recorded; body checked only for the yanked/removed phrases below, bodies not stored). Diffend: `GET https://my.diffend.io/gems/<name>` (no redirect following; status, Location header, and content markers recorded; bodies not stored). Source: `HEAD` on the CSV `source_code_uri`, fallback `GET` only on 405/501/curl failure; status only, nothing cloned or fetched as code.
- No login, no account, no POST, no sessions. No Factum writes. No git add/commit/push. No other directory touched.

## Per-host status tallies

- RubyGems API (`rubygems.org`): 200 × 3, 404 × 131.
- RubyGems page (`rubygems.org`): 200 × 134, nothing else.
- Diffend (`my.diffend.io`): 200 × 108, 302 × 26.
- Source, GitHub (`github.com`, 66 URIs): 404 × 66, 200 × 0.
- Source, oast host (1 URI, see below): 200 × 1.
- Source, no URI in CSV: 67 names — recorded as `source_status: "unchecked"` with note "no source_code_uri in CSV". This is the ONLY unchecked cause in this lane.

## Diffend stub-vs-full marker (exact)

- **Stub** if either:
  - (a) HTTP 3xx with `Location: https://my.diffend.io/gems` — redirect-to-index (26 cases); or
  - (b) HTTP 200 body contains the exact string `There are no computed diffs for this gem` (105 cases).
- **Full** if: HTTP 200, that sentence absent, AND the body carries real diff content — in this slice, version-pair diff index entries of the form `X → Y` plus a date (e.g. `0.2.0 → 0.3.0`). File-level diff strings (`diff-line`, `added-line`, `removed-line`, etc.) were also checked; the version-pair index was the positive signal in all 3 full cases.
- **Gone** (HTTP 404/410): 0 cases in this slice.
- Result: stub × 131, full × 3, gone × 0.

## Results summary

- API-live gems (API 200): 3 — `talk_to_your_app` (latest `0.3.0`), `test_gem_kangaroo` (latest `0.0.14`), `testgem-mini` (latest `0.4.0`). These are also exactly the 3 Diffend-full names and exactly the 3 genuine live RubyGems pages.
- All other 131 names: API 404.
- RubyGems page status is 200 for all 134, but page content splits three ways (recorded per row in `rubygems_page_note`):
  - yanked shell, 94: page states "This gem is not currently hosted on RubyGems.org. Yanked versions of this gem may already exist."
  - removed/reserved shell, 37: page states "This gem previously existed, but has been removed by its owner" with the name reserved (the probed example said 56 more days). All 37 were re-checked individually to confirm this phrase.
  - genuine live page, 3: the API-200 set above.
- Source repos: 66 GitHub URIs all 404 (repos gone or never existed); 1 live source — `xss-test-gem`'s URI on the oast.online host returned HEAD 200 (status only; it is an out-of-band-style test host, no code fetched, no body stored).
- Credential-shaped values in fetched pages: scanned Diffend bodies for common secret patterns (count only, values never stored): **0 matches on all 134 names**.

## `rubygems_versions` field note

- The specified API endpoint (`/api/v1/gems/<name>.json`) does not return a version count or a version list; it returns a single latest `version`. So `rubygems_versions` is `[latest_version]` on API 200 and `null` otherwise, and the latest version is also carried in the extra `rubygems_latest_version` field. No separate versions-endpoint call was made.

## Artifact URLs (total 138)

- Rule applied: RubyGems page URL if page status is 200 (134); Diffend URL if content is `full` (3); source URI if source status is 200 (1).
- Caveat: the 134 page artifacts are status-200 pages, which include the 94 yanked shells and 37 removed/reserved shells — only 3 of them are genuinely live gems (the API-200 set). Filter on `rubygems_api_status == 200` for truly live gems.
- Extra per-row fields beyond the brief's list: `rubygems_latest_version`, `rubygems_page_note`, `source_note`. Required fields are all present with the specified meanings.

## 429 / unchecked cases

- **None.** Zero 429 responses from any host; no host was stopped, and no name was left unchecked for rate-limit reasons.
- The only `unchecked` values are the 67 `source_status` entries for names with no `source_code_uri` in the CSV (see above). Every name has a recorded API status, page status, Diffend status, and Diffend content classification.
