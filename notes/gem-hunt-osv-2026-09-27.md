# HUNT LANE 19 — OSV.dev
Date: 2026-09-27
Task: query OSV.dev for GemStuffer advisories, the Fastly cache advisory, and any
RubyGems advisories mentioning go-import/yardopts/r.jina.ai.

## Method (read-only, paced, no logins)

1. OSV API `POST /v1/query` for 42 campaign package names (RubyGems ecosystem).
2. `GET /v1/vulns/GHSA-9j48-x3c3-mrp2` for the Fastly advisory.
3. GitHub Advisory API `GET /advisories?ecosystem=rubygems&type=malware` (public,
   unauthenticated) — 3,000 advisories pulled across 30 pages with incremental
   saves and retry/backoff; results sorted newest-first.

## Finding 1: OSV carries 7 GemStuffer MAL advisories

Package queries hit on 7 of 42 names (all OSV `MAL-*` malicious-package records,
all published 2026-07-07, all modified 2026-09-24):

| Package | OSV ID | GHSA ref | Affected |
|---|---|---|---|
| zzjinavcsgit | MAL-2026-9952 | GHSA-f527-jgx8-pfqp | = 0.0.1 |
| zzjinavcsbzr | MAL-2026-9950 | GHSA-j6gr-82ww-c4qg | (record) |
| probejiqptzco | MAL-2026-8427 | GHSA-rw2q-5849-m886 | = 0.0.1–0.0.4 |
| uxjinalamb2 | MAL-2026-9062 | GHSA-q97g-2vc7-54mg | (record) |
| wandsworthprobe1778551714 | MAL-2026-9296 | GHSA-324m-86gr-542m | (record) |
| prx1b49033905 | MAL-2026-8456 | GHSA-wc5w-6c9w-3xpm | (record) |
| trya1zz | MAL-2026-9003 | GHSA-8rjv-chpm-63m6 | (record) |

Details fetched for two: both CWE-506 (embedded malicious code), severity
critical, GitHub-published 2026-07-18. `probejiqptzco` lists 0.0.1–0.0.4
(our corpus recorded 6 versions in 33 min — advisory covers the first four).
Snyk also carries the family (e.g. SNYK-RUBY-ZZTXTWTMP11-18017593, CVSS 9.3,
disclosed 18 Jul 2026).

Zero OSV hits on: tryf3zz, southwarkssrfhack, southfetchprobe42, londonyardtestabc,
slnleaker4/5, southpxdatapp6pi, yardxabc889, f2fe-s1, q--00cfmapjson726, all
June-18 names, and **all seven July-7 wave names** (xss-test-gem,
attacker-xss-admin-1, xssname-1783397821, test-apex-gem, test-ssti-0/1/4).

## Finding 2: Fastly advisory is NOT in OSV

`GET /v1/vulns/GHSA-9j48-x3c3-mrp2` → 404 "Vulnerability not found". The advisory
covers the rubygems.org service itself (not a gem package), so it has no
OSV package record. Canonical source remains the RubyGems blog post:
https://github.com/rubygems/blog/blob/HEAD/_posts/2026-07-22-security-advisory-legacy-api-key-leak.md

## Finding 3 (the big one): GitHub's 2026-07-18 bulk advisory batch

GitHub published **2,997 rubygems malware advisories on 2026-07-18** — a bulk
import covering the campaign. Classified by our campaign name grammars
(zz*/oai*/try*zz/epoch-suffixes/probe/proxy/fetch/yard/jina/south/wand/lamb/sln/prx/sa*/pd*/rx*/ux*/root/pwn/rfetch + epoch regex):

- **1,687 GemStuffer-shaped** (206 oai-prefixed, 73 zz-prefixed, 132 epoch-suffixed)
- 1,310 other-campaign (includes the Socket-reported May-1 `knot-*` typosquat
  family — a separate campaign in the same bulk import)

### Cross-inventory reconciliation

| Comparison | Result |
|---|---|
| GS-shaped advisory names ∩ JFrog CSV (3,025) | **1,686 / 1,687** — JFrog's inventory is essentially complete for the advisory-covered set (only `sarif` missing, likely a classifier edge) |
| JFrog names with NO advisory | 768 — campaign packages GitHub never published advisories for |
| GS-shaped advisory names ∩ our Diffend corpus (565) | 403 |
| GS-shaped advisory names NOT in our corpus | **1,284** — the concrete Diffend-sweep target list |

## Data saved

- `data/osv/ghsa_rubygems_malware.json` — 3,000 advisories (ghsa_id, summary, published_at, severity, url)
- `data/osv/ghsa_gemstuffer_batch_names.txt` — 1,897-name sample (regenerate from the classified JSON for the full 2,997)
- `data/osv/ghsa_gemstuffer_classified.json` — gemstuffer_shaped_ghsa (1,687), other_campaign_ghsa (1,310), gs_not_in_jfrog, gs_not_in_corpus (1,284)
- `data/osv/osv_pkg_results3.json` — raw OSV package-query results (batch 3)

## Bottom line

1. OSV has a thin but real GemStuffer layer (7 MAL records); the advisory
   infrastructure lives primarily in GitHub's bulk 2026-07-18 batch.
2. The 1,687-name advisory set independently validates JFrog's 3,022-package
   inventory (99.94% agreement).
3. **1,284 advisory-named campaign packages are absent from our corpus** —
   that is the bounded, high-value Diffend sweep list (vs the open-ended
   2,463 JFrog-only gap).
4. The July-7 XSS/SSTI wave has zero advisories anywhere — it is the least
   catalogued part of the campaign.
5. The Fastly GHSA is not in OSV; nothing new there.

## Suggested follow-ups

- Diffend sweep for the 1,284 `gs_not_in_corpus` names (bounded list, in
  `data/osv/ghsa_gemstuffer_classified.json`).
- The 1,310 `other_campaign_ghsa` names deserve their own lane — the `knot-*`
  typosquat family (BufferZoneCorp, May 1) is a different operator worth
  characterizing separately.
- July-7 wave names have no advisories and no corpus bytes: Diffend sweep for
  xss-test-gem, attacker-xss-admin-1, xssname-1783397821, test-apex-gem,
  test-ssti-0/1/4.
