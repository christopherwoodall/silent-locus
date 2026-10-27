# Live-check census (helper fleet) — July spike CSV, 2026-10-27

Independent parallel census of all 533 July spike CSV gem names, run by a
4-lane helper fleet while a first census worker ran separately. This dir is
the helper fleet's output only; the first worker's dir was never touched.

## Method

- RubyGems API (`/api/v1/gems/<name>.json`) + gem page, Diffend page, and the
  CSV's `source_code_uri`, all via curl, read-only GET/HEAD, max 3 concurrent
  per lane, >=200 ms same-host spacing. Zero 429s on any host; no host stopped.
- Diffend stub marker (all lanes converged): a 200 page containing exactly
  `There are no computed diffs for this gem.` is a stub; a 200 page without
  that sentence and with version-pair diff entries (`X → Y` / diff links) is
  full. A 302 redirect to the Diffend index counts as stub in lanes 1/3/4;
  lane 2 recorded its single such case as gone (see counts note).
- Artifact rule, normalized at merge (lanes differed — see below): a URL counts
  as an artifact iff the RubyGems API returns 200 (genuinely hosted), the
  Diffend page is full, or the source URI returns 200. A RubyGems page
  returning 200 alone does NOT count: yanked/removed shells also return 200.

## Counts (reconcile to 533)

- RubyGems API: 200 x 23, 404 x 510.
- RubyGems page status: 200 x 533 (all of them — status alone is meaningless
  here; only the 23 API-live pages are genuinely hosted).
- Diffend content: full x 18, stub x 514, gone x 1 (lane 2's 302-to-index
  case, klondikemarlen-jira-api; the other lanes' 302s sit inside stub).
- Source URI: 200 x 10, 404 x 194, 301 x 1 (edoxen, not counted as live),
  no URI in CSV x 327, deliberately not fetched x 1 (apex-black-test-001's
  URI is an internal cloud-metadata address; skipped for safety).
- Artifact assignments: 51 (23 gem pages + 18 Diffend pages + 10 source URIs)
  across 26 names, collapsing to 49 distinct URLs in live-urls.txt because
  two source repos are shared by two names each (klondikemarlen/jira-api,
  fuentesjr/metz-scan).

## Names with artifacts

- API-live (23): apex-black-test-011, apex-blk-test-final, apex-oidc-probe,
  eco-helpers, ecoportal-api-graphql, edoxen, intranet-pictures, jrjackson,
  marlens-jira-api, metz-scan, minitest-hashdiff, pico_phone, query-stream,
  rosett-ai, rubocop-metz, shirobai, shirobai-performance, shirobai-rails,
  shirobai-rspec, sportdb-parser, talk_to_your_app, test_gem_kangaroo,
  testgem-mini.
- Diffend-full (18): the API-live set minus apex-black-test-011,
  apex-blk-test-final, apex-oidc-probe, jrjackson, minitest-hashdiff.
- Source-live (10) includes two OAST callback URIs counted as live HTTP
  endpoints only (apex-black-test-013, xss-test-gem) — liveness of the URI,
  not proof any callback arrived.
- Names with an artifact but no live gem: klondikemarlen-jira-api (live
  source repo only), apex-black-test-013 (live OAST URI only),
  xss-test-gem (live OAST URI only).

## Lane-rule caveat (why the merge renormalized)

Lanes counted page artifacts differently: lane 1 counted all status-200
pages; lane 3 excluded owner-removed pages but kept yanked shells; lane 4
counted all status-200 pages with a caveat; lane 2 counted body-live pages
only. The merged live-urls.json recomputes artifact_urls under the uniform
rule above and preserves each lane's original list in lane_artifact_urls
for audit. Lane partials are untouched.

## Lanes

- Lane 1: sorted indices 0-132 (133 names). Lane 2: 133-265 (133).
  Lane 3: 266-398 (133). Lane 4: 399-532 (134). Union verified equal to
  the CSV name set, 533 unique, no overlaps, no gaps.
- Field variance (preserved as lanes recorded it): rubygems_versions is a
  verbatim versions list in lane 3, [latest] in lane 4, and version-count /
  latest extras in lane 1. Do not compare version counts across lanes.

## Verifier

See verifier-report.md (fresh 20-name re-check + count reconciliation).

## Verifier (2026-10-27, post-merge)

Verdict: SHIP-WITH-FIXES, fix applied. Fresh 20-name re-check: API 20/20,
gem page 20/20, Diffend content 20/20, exact Diffend status 19/20. One live
drift found and fixed in live-urls.json: apex-test-write-001 diffend_status
200 -> 302 (redirect to the Diffend index); content class stays stub, so no
count or artifact changes. Full detail: verifier-report.md.
