# Live-status census — July spike CSV — 2026-10-27

Scope: all 533 names in the operator-supplied July spike CSV
(`data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv`).
This is a live-status census only. It does not re-do the review in
`reports/rubygems-july-spike-review/REPORT.md`.

## Answer in one line

23 of 533 packages are still live on RubyGems. 510 are gone from the index.
52 URLs carry real artifacts. The other 510 RubyGems pages still render, but
only as yanked / not-hosted notices — they are not live packages.

## Counts (all reconcile to 533 names)

- RubyGems API: 200 live = 23; 404 gone = 510; unchecked = 0.
- RubyGems gem page: 200 renders = 533 (all of them — see the tombstone note).
- Diffend: full content = 22; stub = 511; gone/unchecked = 0.
- Source URI (206 rows carry one; 327 rows have none):
  live repo = 9 rows; live callback endpoint = 2 rows; 404 = 194 rows;
  unreachable (status 0) = 1 row.
- Artifact URLs in `live-urls.txt`: 52 = 23 RubyGems gem pages + 22 Diffend
  pages + 7 unique live repo URLs (9 repo-200 rows share 2 repos).
- Yanked tombstone pages in `yanked-tombstone-pages.txt`: 510.

Cross-checks: 23 + 510 = 533 (API). 22 + 511 = 533 (Diffend).
9 + 2 + 194 + 1 = 206 (source URIs); 206 + 327 = 533.
`live-urls.txt` lines == union of `artifact_urls` in `live-urls.json` (verified).

## Method

- Tool: curl (this VM's egress proxy; python httpx is broken here).
  Read-only GET, plus HEAD for source URIs (GET fallback on 405/501).
  No login, no account, no POST, no sessions. No payloads executed.
- Rate: 5 concurrent workers, at least 200 ms between requests to the same
  host. Zero 429 responses on any host, so no host was stopped and nothing
  was left unchecked for rate reasons.
- RubyGems live = API 200. Versions come from the versions endpoint for
  API-live names only; downloads and latest version from the gem endpoint.
- Diffend content signal (status alone lies — Diffend returns 200 even for
  gone gems):
  - stub = page text contains "There are no computed diffs for this gem."
  - full = version-pair diff rows present (arrow between versions) or a
    single version row present. The detail field records which.
- Source artifact rule: status 200 AND the host is a code host
  (github.com, a GitLab host, bitbucket.org, codeberg/sourcehut family).
  Callback-collector endpoints answering 200 are NOT counted as artifacts
  (see below).

## The tombstone correction (read this before using the page statuses)

Every one of the 533 RubyGems gem pages returns HTTP 200, including all 510
API-404 names. Two sampled shapes explain it:

- Yanked tombstone: e.g. mini-sharp-hub — "Yanked by rubygems-security-team".
- Not-hosted notice: e.g. test-apex-gem — "This gem is not currently hosted
  on RubyGems.org. Yanked versions of this gem may already exist."

So page-200 alone proves nothing about a package being up. The API status
is the authority for index membership, and `live-urls.txt` uses it. The 510
tombstone/not-hosted page URLs are kept separately in
`yanked-tombstone-pages.txt` so they are viewable without being mistaken
for live packages. Page-content sampling covered 3 names in full plus the
5-name marker check; API status (not page text) drives the classification.

## Notable cases

- Live on both RubyGems and Diffend (22): rosett-ai, sportdb-parser,
  edoxen, apex-black-test-011, test_gem_kangaroo, apex-oidc-probe,
  apex-blk-test-final, testgem-mini, shirobai, shirobai-performance,
  shirobai-rspec, shirobai-rails, rubocop-metz, metz-scan,
  ecoportal-api-graphql, marlens-jira-api, eco-helpers, minitest-hashdiff,
  pico_phone, intranet-pictures, query-stream, talk_to_your_app.
- Live on RubyGems only (1): jrjackson — API live, latest 0.3.8,
  10,508,353 downloads, 50 versions, Diffend stub (no computed diffs).
  Live on Diffend only: 0.
- Legit gems still up: jrjackson, eco-helpers (438,219 downloads,
  277 versions), sportdb-parser, ecoportal-api-graphql, pico_phone.
  Probe gems still up: apex-black-test-011 (v9.9.9), apex-oidc-probe,
  apex-blk-test-final, test_gem_kangaroo.
- Still versioned today: the shirobai family (shirobai,
  shirobai-performance, shirobai-rspec, shirobai-rails) all show latest
  version 2026.1027.0730, i.e. dated 2026-10-27.
- Live source repos (7 unique URLs): gitlab.neatnerds.be/foss/rosett-ai,
  github.com/metanorma/edoxen, github.com/fuentesjr/metz-scan (shared by
  rubocop-metz and metz-scan), github.com/klondikemarlen/jira-api (shared
  by marlens-jira-api and klondikemarlen-jira-api), github.com/gjack/pico_phone,
  bitbucket.org/ebling-mis/intranet-pictures,
  github.com/Atelier-Mirai/query-stream.
- Live callback endpoints, NOT counted as artifacts (2): an oast.online URL
  for apex-black-test-013 and one for xss-test-gem both answer 200. That is
  the collector answering, not a repo. The gems themselves are API-404.
- Unreachable source URI (1): apex-black-test-001 points at
  http://metadata.aws.internal/latest/meta-data/ — a cloud-metadata SSRF
  probe URI, not a repo; status 0 from here.
- No credential-shaped values were copied into any output. (Presence check:
  none found in the generated files.)

## Verification

- Fresh re-check of a seeded random 20-name sample (API status, page status,
  Diffend content class): 0 mismatches out of 20.
- `live-urls.txt` vs `live-urls.json` artifact sets: identical.
- All counts above recomputed from `live-urls.json`.

## Files

- `live-urls.txt` — 52 artifact URLs, one per line, deduplicated, sorted.
- `live-urls.json` — one object per gem name (533): API/page statuses,
  page-content note, versions, latest, downloads, Diffend status/content/
  detail, source URI/kind/status, artifact URLs.
- `yanked-tombstone-pages.txt` — 510 RubyGems page URLs for API-404 names
  (viewable notices, not live packages).
- `live-check-summary.md` — this file.
