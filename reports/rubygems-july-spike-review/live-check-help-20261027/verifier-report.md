# Verifier report — merged live-check census, July spike CSV (2026-10-27)

Independent verifier lane. The verifier did not run the census.
No input file was modified. Source URIs were NOT re-fetched in the
fresh re-check (scope was RubyGems API, gem page, and Diffend only).
This file is the verifier's only write.

## Overall verdict: SHIP-WITH-FIXES

All counts, the name set, the artifact rule, the text-file union, and
lane reconciliation pass exactly. The fresh re-check passes 20/20 on
API status, gem-page status, and Diffend content, and 19/20 on exact
Diffend HTTP status. The single failure is one post-census Diffend
status drift that changes no count, no content class, and no artifact
(see Check 5, Fix 1). Fixes 2 and 3 are optional normalizations, not
blockers. If the census is shipped strictly as a 2026-10-27 snapshot,
Fix 1 can instead be recorded as a drift note and the verdict is SHIP
as a snapshot.

## Check 1 — Name set: PASS

- `live-urls.json` parses as a JSON array.
- Objects: 533. Unique names: 533. Duplicates: 0.
- CSV rows: 533. Unique CSV names: 533. Duplicates: 0.
- Names in CSV but not in JSON: 0. Names in JSON but not in CSV: 0.
- Name sets are exactly equal.

## Check 2 — Counts recomputed from live-urls.json: PASS

All summary counts reproduce exactly.

| Field | Recomputed | Summary | Match |
| --- | --- | --- | --- |
| RubyGems API 200 | 23 | 23 | yes |
| RubyGems API 404 | 510 | 510 | yes |
| RubyGems page 200 | 533 | 533 | yes |
| Diffend full | 18 | 18 | yes |
| Diffend stub | 514 | 514 | yes |
| Diffend gone | 1 | 1 | yes |
| Source 200 | 10 | 10 | yes |
| Source 404 | 194 | 194 | yes |
| Source 301 | 1 | 1 | yes |

Source non-numeric accounting (the part that needs grouping):

- CSV rows with an empty `source_code_uri`: 327. This is the
  summary's "no URI in CSV x 327".
- Deliberately not fetched: 1 (`apex-black-test-001`, internal
  metadata URI, `source_status` = "unchecked").
- 327 + 1 = 328 non-numeric source rows. In JSON these appear as
  `source_status` = null x 260 and "unchecked" x 68 (67 no-URI rows
  from lane 4 plus the 1 deliberately-not-fetched row).
- 10 + 194 + 1 + 328 = 533. No mismatch; see Fix 3 for the encoding
  inconsistency (null vs "unchecked" for the same "no URI" meaning).

Diffend status detail (consistent with the content counts):
200 x 506 (488 stub + 18 full), 302 x 27 (26 stub + 1 gone).

## Check 3 — Artifact consistency: PASS

Uniform rule applied as stated, with one host clarification:

- Gem page URL iff RubyGems API status is 200.
- Diffend URL iff `diffend_content` is "full".
- Source URI iff `source_status` is 200.
- The Diffend host actually used throughout (all lane notes and
  partials) is `my.diffend.io`, i.e. Diffend URLs are
  `https://my.diffend.io/gems/<name>`. Under that host, mismatches
  are 0 out of 533. (A literal `diffend.io` host would mismatch all
  18 full-Diffend rows; that host is not what any lane used.)
- `artifact_urls` equals `artifact_urls_uniform` on all 533 rows
  (0 differences).
- Total artifact assignments: 51 (23 gem pages + 18 Diffend pages +
  10 source URIs).
- Distinct URLs in the union of all `artifact_urls`: 49.
- `live-urls.txt`: 49 lines, 49 unique, set-equal to that union
  (0 lines only in the file, 0 union URLs missing from the file).
- The 51-to-49 collapse is verified and is exactly two shared
  source repos, each used by two names:
  - `https://github.com/klondikemarlen/jira-api` — shared by
    `klondikemarlen-jira-api` and `marlens-jira-api`.
  - `https://github.com/fuentesjr/metz-scan` — shared by
    `metz-scan` and `rubocop-metz`.
- Names with at least one artifact: 26, matching the summary.
- `lane_artifact_urls` differs from the uniform `artifact_urls` on
  338 rows, by design (lanes used different page-artifact rules;
  the merged file preserves the lane list for audit). This is not
  a failure per the task brief.

## Check 4 — Lane reconciliation: PASS

| Lane | Rows | First name | Last name |
| --- | --- | --- | --- |
| lane1 | 133 | (100-char 'a' name) | ecoportal-api-graphql |
| lane2 | 133 | edoxen | mini-max-mod |
| lane3 | 133 | mini-max-pkg | ssrf-self-852d86f8 |
| lane4 | 134 | ssrf-test-1783405321 | yank-scope-test-1783410282 |

- Lane union: 533 unique names. Overlaps between lanes: 0.
- Lane union vs merged name set: equal, 0 gaps, 0 extras.
- Status comparison, merged vs each lane row, on all five fields
  (`rubygems_api_status`, `rubygems_page_status`, `diffend_status`,
  `diffend_content`, `source_status`): 0 divergences in every lane
  (533 rows compared).
- Not compared, per the brief and the summary: `rubygems_versions`
  (verbatim list in lane 3, [latest] in lane 4, count/latest extras
  in lane 1) and `lane_artifact_urls` (differs by design, above).

## Check 5 — Fresh re-check (20 names): 19/20 exact, 20/20 on content

Method: `random.Random(20261027).sample(sorted(CSV names), 20)`.
Sequential curl GET (at most 3 concurrent by construction), no
redirect following for Diffend, read-only, no login, no POST.
Diffend content rule: 200 + the exact sentence
"There are no computed diffs for this gem." = stub; 200 without
that sentence and with version-pair diff entries = full; 302 to the
Diffend gems index = redirect-to-index (merged maps lane-4 302s to
stub and the single lane-2 302 to gone — see Fix 2).
Source URIs were not fetched.

Merged = M, re-check = R. "Diffend" columns are HTTP status /
content. All 20 rows match on API status and gem-page status (page
200 in every row, both sides).

| Name | M API / page | R API / page | M Diffend | R Diffend | Verdict |
| --- | --- | --- | --- | --- | --- |
| giga-safe-gem | 404 / 200 | 404 / 200 | 200 / stub | 200 / stub | PASS |
| apex-black-race-002 | 404 / 200 | 404 / 200 | 200 / stub | 200 / stub | PASS |
| ecoportal-api-graphql | 200 / 200 | 200 / 200 | 200 / full | 200 / full | PASS |
| mega-clean-box | 404 / 200 | 404 / 200 | 200 / stub | 200 / stub | PASS |
| klondikemarlen-jira-api | 404 / 200 | 404 / 200 | 302 / gone | 302 / redirect-to-index (= gone in merged mapping) | PASS |
| super-quick-hub | 404 / 200 | 404 / 200 | 200 / stub | 200 / stub | PASS |
| apex_registry_test | 404 / 200 | 404 / 200 | 200 / stub | 200 / stub | PASS |
| micro-fast-rb | 404 / 200 | 404 / 200 | 200 / stub | 200 / stub | PASS |
| apex-black-fuzz-051 | 404 / 200 | 404 / 200 | 200 / stub | 200 / stub | PASS |
| apex-black-fuzz-053 | 404 / 200 | 404 / 200 | 200 / stub | 200 / stub | PASS |
| ultra-pure-gem | 404 / 200 | 404 / 200 | 200 / stub | 200 / stub | PASS |
| super-smart-tool | 404 / 200 | 404 / 200 | 200 / stub | 200 / stub | PASS |
| super-smart-sys | 404 / 200 | 404 / 200 | 200 / stub | 200 / stub | PASS |
| apex-black-long-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx | 404 / 200 | 404 / 200 | 200 / stub | 200 / stub | PASS |
| apex-test-write-001 | 404 / 200 | 404 / 200 | 200 / stub | 302 / redirect-to-index (= stub in lane-4 mapping) | PARTIAL — status drift only |
| test-ssti-4 | 404 / 200 | 404 / 200 | 302 / stub | 302 / redirect-to-index (= stub) | PASS |
| micro-lite-rb | 404 / 200 | 404 / 200 | 200 / stub | 200 / stub | PASS |
| ultra-pure-kit | 404 / 200 | 404 / 200 | 200 / stub | 200 / stub | PASS |
| mega-quick-hub | 404 / 200 | 404 / 200 | 200 / stub | 200 / stub | PASS |
| mini-fast-sys | 404 / 200 | 404 / 200 | 200 / stub | 200 / stub | PASS |

Failure detail (the only re-check failure):

- `apex-test-write-001`: merged Diffend status 200, re-check 302
  with `Location: https://my.diffend.io/gems` (confirmed by a
  follow-up HEAD check; the same index redirect was confirmed for
  `klondikemarlen-jira-api` and `test-ssti-4`). Its lane-4 partial
  also records 200, so this is live drift since the census, not a
  merge error. Content class is unchanged (redirect-to-index =
  stub under the lane-4 rule), and it carries no Diffend artifact
  either way, so no count and no artifact changes.

Pass rates: API 20/20, gem page 20/20, Diffend content 20/20,
exact Diffend status 19/20, full-row exact 19/20.

## Check 6 — Credential scan: PASS (no credential values)

Scanned `live-urls.json`, `live-urls.txt`, and
`live-check-summary.md` for credential-shaped patterns. Presence
and counts only; no values are copied anywhere in this report.

- `api_key` / token / secret / password assignment patterns: 0.
- AWS key-ID pattern: 0. GitHub personal-token pattern: 0.
- CSRF token values: 0. Only the boolean field `csrf_present`
  appears (True on the 133 lane-1 rows, absent on other rows);
  no token value is stored.
- Hex strings of length 40+: 4 hits, all explained — they are the
  100-character 'a' gem name itself, in its `name` field and its
  `lane_artifact_urls` entry (2 records x 2 fields). Not secrets.
- OAST hostnames: present as hosts in source URIs, not as
  credential values. Occurrences: 8 in `live-urls.json` (2 records
  x 4 fields: `source_uri`, `artifact_urls`,
  `artifact_urls_uniform`, `lane_artifact_urls`), 2 in
  `live-urls.txt` (the 2 live source-artifact URLs), 0 in the
  summary. The two live OAST source URIs are the ones the summary
  already names as live HTTP endpoints only
  (`apex-black-test-013`, `xss-test-gem`); liveness is not proof
  any callback arrived. Their subdomain strings are deliberately
  not reproduced here.
- The internal metadata URI for `apex-black-test-001` appears only
  as a `source_uri` value that was deliberately not fetched; it is
  a URI, not a credential value.
- Conclusion: no credential VALUES are present in the merged
  outputs.

## Failures and fix list

1. (Required for a current-state merge; optional for a snapshot)
   `apex-test-write-001`: update `diffend_status` 200 to 302 in
   `live-urls.json` and in the lane-4 partial, or annotate the row
   as post-census drift. No summary count, content class, or
   artifact changes either way.
2. (Optional taxonomy note) Identical 302-to-index Diffend
   redirects are classed "stub" for 26 rows but "gone" for the one
   lane-2 row (`klondikemarlen-jira-api`). The summary already
   discloses this. Normalizing "gone" to "stub" would change the
   summary counts to stub x 515, gone x 0 and must be done together
   with the summary text; leaving it as disclosed is acceptable.
3. (Optional encoding note) "No source URI" is encoded as
   `source_status` null on 260 rows (lanes 1–3) and "unchecked" on
   67 rows (lane 4), and `source_note` is absent on 266 merged rows
   (lanes 2–3 do not carry that key). Counts are unaffected, but a
   future normalization should pick one encoding and carry it
   through the summary's source accounting.
4. No other failures. No lane-vs-merged divergence, no artifact
   rule violation, no text-file mismatch, no credential value.

## Verifier notes

- Diffend host clarification (Check 3) is a documentation point,
  not a data error: the task brief says "Diffend URL" without a
  host, and every lane used `my.diffend.io`.
- Re-check did not fetch source URIs, so source statuses were
  verified by recomputation against the CSV only (Check 2/3),
  not by live re-fetch.
- No git add, commit, or push was run. No directory other than
  this help directory was written to (this file only).
