# Verifier report — integrated analysis, July 2026 RubyGems spike set

## Verdict: SHIP-WITH-FIXES (fixes applied)

The verifier lane recomputed every count from source files
(CSV, reconciled live JSON and text files, tombstone pairs)
plus a fresh live re-check, without re-reading lane claims.
Its full draft is preserved at
`working/verifier-report-draft.md`. Its verdict was
SHIP-WITH-FIXES. Both blocking fixes are applied in
REPORT.md. The coordinator's ship-time refresh is recorded
at the end.

## Pass / fail table (verifier's, verbatim in substance)

| Check | Expected | Observed | Result |
|---|---|---|---|
| CSV rows | 533 | 533, distinct names | PASS |
| Partition | 310 / 203 / 20 | 310 / 203 / 20, disjoint; combinatorial via strict 10x10x10 product (129 / 113 / 68 by author, July 6 / 13 / 12); all 203 family-B rows first-published July 7 | PASS |
| Apex-substring | 115, not 114 | 115 | PASS |
| Probe-descriptive | 117 (family-B non-placeholder) | 117 = 203 − 86 | PASS as residual definition |
| Prior "105" probe-descriptive | 105 | Irreproducible: plain-word rule 103, first-match 113, broad keyword ~102 | FAIL (minor) |
| OAST / webhook | 29 / 19 | 29 / 19 | PASS |
| SSRF / internal | 24 (23 link + 1 summary) | 25 (24 link + 1 summary) | FAIL — corrected, see F1 |
| Payload union / +author-only | 82 / 84 | 83 / 85 | FAIL (consequence of F1) |
| Live API | 23 live / 510 gone | 23 / 510; JSON name set = CSV set | PASS |
| Diffend full in census file | 18 | 18, all API-live | PASS as file check |
| Diffend full, current state | 18 | 19 (jrjackson now full) | FAIL until refreshed — refreshed, see below |
| Artifact URLs | 48, txt == JSON union both ways | 48; txt == `artifact_urls` exactly | PASS |
| Tombstone pairs | 510 keys, 509 stub, 1 gone, 1 live mirror | Exactly that; keys == the 510 API-gone names | PASS |
| Survivors | 18 legit / 3 probe / 2 test = 23 | 18 / 3 / 2; 8 spot-checks all stand | PASS |
| Fresh sample API (seed 20261027, n=30) | matches census | 30 / 30 (29 gone, 1 live) | PASS |
| Fresh sample Diffend class | matches census | Class matches 30 / 30; raw 302-vs-200 status differs on 3 redirect pages | PASS on class, FAIL on raw-status field |

## Mismatches and causes

1. **SSRF 25, not 24 — counting error, not drift.**
   Link rows are IP-internal 10 + internal-hostname rows 4
   + public-IP rows 10 = 24, plus 1 summary-only row =
   25. The cryptologist lane counted 3 internal-hostname
   rows, collapsing two DNS-probe rows sharing one
   hostname shape into one (a shape count used where a
   row count was needed). Hence union 83, not 82, and
   total with author-only 85, not 84. The 10-public-IP
   split inside the set still holds.
2. **jrjackson Diffend now full — live drift (backfill),
   not proven census error.** Both independent censuses
   said stub. Fresh check (confirmed on refetch, 35
   version-pair links, ~21 KB) shows full, while the gem
   itself is unchanged (same latest version, downloads
   +190 on a ~10.5M base). Applied: Diffend full 18 → 19,
   live-only 5 → 4, artifact URLs 48 → 49. Legit
   classification unchanged.
3. **Redirect-status inconsistency — method inconsistency,
   no artifact impact.** All 6 sampled redirect-index
   pages are 302 no-follow, but census records 200 for 3
   of them; 27 tombstone rows labelled "stub" are also
   302s, while one identical redirect was adjudicated
   "gone". "Stub" must be defined as "no Diffend diff
   artifact," not "served a stub page." REPORT.md §6
   adopts that definition and the future gone =
   redirect-to-index rule.
4. **Minor text fixes (all applied):** linguist "XSS word
   14" is 10 rows (14 is the occurrence count); the "3
   version matches" sentence matches neither dataset
   (reconciled JSON: apex-black-test-011, apex-oidc-probe,
   test_gem_kangaroo; first census: 4 including
   minitest-hashdiff) — REPORT.md uses 4 with the
   first-census field cited; 9 live rows in reconciled
   JSON have null version fields despite first-census
   values; `artifact_urls_uniform` (49) is
   pre-reconciliation and must not be quoted (it still
   contains the 2 excluded callback endpoints); 114 is
   reproducible as names *starting with* `apex`, so the
   report says "115 substring, 114 prefixed."

## Blocking fixes before ship (both applied)

- **F1.** Correct 24 → 25, 82 → 83, 84 → 85 throughout.
- **F2.** Refresh Diffend for the live set at ship time
  and update full / live-only / artifact counts.

## Coordinator's ship-time refresh (this report)

- jrjackson Diffend re-fetched 2026-10-27: HTTP 200,
  ~21 KB, stub marker absent, 35 arrow version-pairs,
  title "Versions diffs," latest pair 0.5.5-java dated
  October 21, 2026. Class: full. This confirms the
  verifier's drift call independently.
- Refreshed artifact list written to
  live-urls-refreshed-20261027.txt: 49 lines, verified
  superset of the reconciled 48 plus the jrjackson
  Diffend URL, no other change.
- Version publish dates for all 23 live gems fetched from
  the RubyGems versions endpoint and preserved in
  live-version-dates-20261027.json (used for REPORT.md
  §3.2). testgem-mini reverse-dependencies page checked:
  zero dependents.
- No callback URL was fetched. No payload was executed.
  No credential-shaped value is reproduced here.
- Core conclusions (partition, live/gone split, artifact
  set, survivor split, no agent evidence) all survive.
  The one quality gate still open is the second
  adversarial pass noted in adversarial-review.md.
