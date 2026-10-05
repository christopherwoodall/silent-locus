# PROVENANCE — gem-negative-lanes (2026-09-27/28)

**Dataset:** `2026-09-27-gem-negative-lanes` — bounded negative sweep results
from the GemStuffer/RubyGems go-import campaign hunt lanes that tested
external surfaces for the campaign's fingerprints and found nothing.

**Retrieval/observation dates:** 2026-09-27 (most lanes), 2026-09-28
(api.usa.gov / FBI UCR lane). `@timestamp` = note date; each record carries
`labels.timestamp_source=note:publication_date`.

**Method:** each source note is a bounded hunt lane executed read-only against
a public surface with a fixed method (marker searches, direct name lookups,
bulk-event passes, index triage, DNS/HTTP probes). Records here are the
*measured outcome* of each lane: `sweep_negative` (zero hits, with exact
denominators), one `access_gap` (abuse.ch APIs require auth — unresolved,
not clean), and one `finding` (the RubyGems `/info/` API is a
live/yanked/nonexistent oracle but leaves no content residue).

**Lanes (20 source notes → 20 records):**

| Venue | Note | Denominator | Result |
|---|---|---|---|
| deps.dev | gem-hunt-depsdev-2026-09-27 | yanked-gem package pages | dead end (no retention) |
| npm | gem-hunt-npm-2026-09-27 | 19 search queries + 18 direct lookups | zero hits |
| PyPI | gem-hunt-pypi-2026-09-27 | 20 names vs living API | zero hits |
| PyPI BigQuery | gem-hunt-pypibigquery-2026-09-27 | ~3.4M events, 3,026 names | zero hits |
| doc pipelines | gem-hunt-docpipelines-2026-09-27 | docs.rs / crates.io / pkg.go.dev / readthedocs marker battery | zero hits |
| Docker Hub | gem-hunt-dockerhub-2026-09-27 | marker searches | zero hits (token noise only) |
| urlscan.io | gem-hunt-urlscan-2026-09-27 | paced public search API | zero hits |
| Common Crawl | gem-hunt-commoncrawl-2026-09-27 | CC-MAIN-2026-21 index lookups | zero hits |
| Shodan | gem-hunt-shodan-2026-09-27 | host lookups incl. 20.49.140.101 | zero hits |
| GitHub Actions | gem-hunt-ghactions-2026-09-27 | repo/description searches | zero hits |
| GitHub gists | gem-hunt-gists-2026-09-27 | gist API scans | zero hits |
| HuggingFace Hub | gem-hunt-huggingface-2026-09-27 | 185 names × 3 endpoints = 555 queries | zero hits |
| Go module index | gem-hunt-gomodules-2026-09-27 | 32,766 (Path, Version) pairs | zero hits |
| public code search | gem-hunt-codesearch-2026-09-27 | Sourcegraph/grep.app marker route | zero hits |
| abuse.ch historical | gem-hunt-abusech-historical-2026-09-27 | 456 digests / 226,036 attributes | zero hits (551 noise adjudicated) |
| pastebins | gem-hunt-pastebins-2026-09-27 | rentry.co / 0x0.st search-engine route | zero hits |
| rubydoc.info | gem-rubydoc-traces-2026-09-27 | 7 campaign gem pages | 404s, no residue |
| api.usa.gov / FBI UCR | api-usa-fbi-ucr-2026-09-28 | 37 local files + 80,434 collusion-wiki docs | zero hits |
| RubyGems API | gem-hunt-rubygemsapi-2026-09-27 | `/info/<name>` oracle behavior | finding (structural residue only) |
| abuse.ch APIs | gem-hunt-abusech-2026-09-27 | auth-required | access gap (unresolved) |

**What landed** (`events.jsonl`, 20 records): 17 `sweep_negative`, 1
`access_gap`, 1 `finding` (rubygemsapi oracle), plus the rubydoc negative.

**Dedup note:** negative-lane content does not duplicate existing event
records; existing `sweep_negative` rows live in the osv, webhook-deaddrops,
and libraries.io battery collections for venue-specific sweeps. The
`overlap-negatives` analysis material is a separate aggregate rollup.

**Fingerprint identities:** `negative-lane|<venue>` (one per lane);
`negative-lane|abuse.ch-api` for the access gap;
`negative-lane|rubygemsapi-oracle` for the finding.
