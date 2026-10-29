# HUNT LANE 16 — GitHub Gists
Date: 2026-09-27
Task: hunt GemStuffer campaign fingerprints in public gists (scratch-space / dead-drop lane).

## Method (read-only, no auth, paced)

- 11 `site:gist.github.com` web searches for the literal beacon/payload markers:
  `"builder alive"`, `"YARD RAN"`, `"yard exploit"`, `"HOOKED!!!!!!"`,
  `"malicious crawler"`, `"perhaps yard reads"`, `"go-import"`, `r.jina.ai`,
  `southwarkssrfhack`, `southfetchprobe`, `zzjina`.
- 6 unauthenticated GitHub REST API searches (`/search/repositories`, ~11 calls
  total, well under the 60/hr limit) for exact campaign names
  (`tryf3zz`, `southwarkssrfhack`, `zzjina`, `yardbreaker`) and date-boxed
  grammar sweeps (`oai in:name` and `probe in:name`, May–Jul 2026 window).

No forks, stars, comments, or logins. Nothing downloaded.

## Verdict: NEGATIVE — the beacons never leaked into gists.

| Marker | Result |
|---|---|
| `builder alive` | 0 hits |
| `YARD RAN` | 0 hits |
| `yard exploit` | 0 hits |
| `HOOKED!!!!!!` | hits, all tokenized noise (`hooked` vars, `HOOKED_texOff` shader code, "hooked it up" prose) |
| `malicious crawler` | 0 hits |
| `perhaps yard reads` | 0 hits |
| `<meta name="go-import">` | hits, all legitimate (Go vanity-import configs, nginx snippets, GitHub's own scraped page meta) |
| `r.jina.ai` | hits, all legitimate Jina Reader usage (bookmarklets, docs, API clients) |
| `southwarkssrfhack` | 0 hits |
| `southfetchprobe` | 1 hit — unrelated Fabric deploy script (token match on south/fetch/probe, ~10 years old) |
| `zzjina` | 0 hits |

GitHub repo search: exact campaign names (`tryf3zz`, `southwarkssrfhack`, `zzjina`,
`yardbreaker`) → **total 0** each. Date-boxed `oai in:name` (458 results) and
`probe in:name` (85 results) across the campaign window → all ordinary repos
(OIDC tooling, django deploy probes, personal projects), nothing campaign-shaped.

## Interpretation

Gists join the clean negatives: deps.dev, PyPI, npm, Docker Hub, urlscan, doc
pipelines, GitHub Actions. The campaign's observable footprint remains
RubyGems-only; its dead-drop channels (gem metadata board, webhook dead-drops)
never extended to gist-shaped scratch space.

## Honest gaps

- GitHub has no public gist search API; literal content search inside gist bodies
  relied on search-engine indexing of gist.github.com (same limitation as the
  PyPI lane). Unindexed or very recent gists would not surface.
- GitHub code search requires auth, so beacon search inside workflow files /
  repo contents wasn't possible unauthenticated (also noted in lane 14).
