# VERIFIER REPORT — July 2026 RubyGems spike set, integrated analysis

**Verdict: SHIP-WITH-FIXES**

The core conclusions survive independent recomputation: the 533-row
partition, the 23-live / 510-gone census split, the 48-URL artifact set,
and the 18 / 3 / 2 survivor split all reproduce. Two headline numbers
do not reproduce and must be corrected before shipping (F1, F2 below).
Neither changes the substantive story — no agent evidence, no callback
receipt, probe survivors are listing residue — but a shipped report
must not carry a wrong payload total or a stale Diffend count.

## Method (independent recomputation, not lane re-reads)

- CSV source: `data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv`,
  recomputed with fresh Python csv/regex code, not by copying lane tallies.
- Live source: `reports/rubygems-july-spike-review/live-check-reconciled-20261027/live-urls.json`,
  `live-urls.txt`, `tombstone-diffend-pairs.json`, cross-checked against
  both prior censuses (`live-check-20261027`, `live-check-help-20261027`).
- Fresh re-check: seeded random sample, `random.Random(20261027).sample`
  over CSV row order, n = 30, plus 8 targeted survivors (38 distinct
  names checked in total). Each name: RubyGems API
  (`rubygems.org/api/v1/gems/<name>.json`) and Diffend page
  (`my.diffend.io/gems/<name>`), no-follow status recorded separately
  from followed content. Diffend classes used: full = version-pair diff
  links present (size varies: 6.1 KB for a 2-version gem, 23.6 KB for
  a 51-version gem); stub = exact no-diffs marker present, or a
  ~5.6–5.7 KB single-version page with no pair links; redirect/index =
  302 to the Diffend index (12.9 KB generic page when followed, no
  pair links for the sampled name).
- Callback hygiene: no out-of-band or webhook callback URI was fetched
  at any point. 3 of the 30 sampled rows carry a callback-shaped
  homepage/source/summary string; all 3 are marked deliberately
  unfetched, and their API/Diffend checks do not depend on them.
- No payload was executed. No credential-shaped value, token, or
  callback identifier is reproduced in this report (counts and shapes
  only). No file other than this report was written by this lane.

## Pass / fail table

| # | Check | Expected | Observed | Result |
|---|---|---|---|---|
| 1 | CSV rows | 533 | 533, all names distinct | PASS |
| 2 | Family partition | 310 / 203 / 20 = 533 | 310 / 203 / 20 = 533, disjoint (see below) | PASS |
| 3 | Apex-substring names | 115, not 114 | 115 names contain `apex` | PASS (with note N1) |
| 4 | Probe-descriptive summaries | 117 (family B, non-placeholder) | 117 = 203 − 86 placeholders | PASS |
| 5 | Prior "probe-descriptive" figure | 105 | Not reproduced by any tested rule (see M3) | FAIL (minor, non-load-bearing) |
| 6 | OAST callback rows | 29 | 29 (26 homepage cells, 2 source cells, 2 summary cells; 30 cells / 29 rows) | PASS |
| 7 | Webhook callback rows | 19 | 19, all homepage cells, 9 distinct path tokens | PASS |
| 8 | SSRF/internal rows | 24, as 23 link + 1 summary | 25, as 24 link + 1 summary | FAIL (F1) |
| 9 | Payload union (scan set) | 82 | 83 | FAIL (consequence of F1) |
| 10 | Payload union + author-only | 84 | 85 | FAIL (consequence of F1) |
| 11 | Live census, RubyGems API | 23 live / 510 gone | 23 / 510; name set identical to CSV (533) | PASS |
| 12 | Diffend full, in census file | 18 | 18, all 18 also API-live; 5 live-only | PASS (as a file check) |
| 13 | Diffend full, current state | 18 | 19 — jrjackson is now full (see M2) | FAIL until refreshed (F2) |
| 14 | Artifact URLs | 48; txt == JSON artifact union, both directions | 48; `live-urls.txt` == `artifact_urls` field exactly, both directions | PASS (with note N2) |
| 15 | Tombstone pairs | 510 keys, 509 stub, 1 gone, 1 live mirror | 510 keys; 509 `stub`, 1 `gone`; exactly 1 row with a non-empty live mirror; keys == the 510 API-gone names | PASS |
| 16 | Survivor classes | 18 legit / 3 probe / 2 test = 23 | 18 / 3 / 2 = 23; 8 spot-checks, all classifications stand | PASS |
| 17 | Fresh sample, API status | matches census | 30 / 30 sampled names match (29 gone, 1 live) | PASS |
| 18 | Fresh sample, Diffend class | matches census | Random 30: no-artifact/full class matches on all 30; raw 302-vs-200 status differs on 3 (see M4) | PASS on class, FAIL on raw-status field |
| 19 | Linguist non-exclusive "XSS word" | 14 rows | 10 rows; 14 is the occurrence count, not the row count | FAIL (minor) |
| 20 | "CSV latest matches live latest on 3 of 23" | 3: apex-black-test-011, apex-oidc-probe, minitest-hashdiff | Reconciled JSON: 3, but the third is test_gem_kangaroo, not minitest-hashdiff (its JSON latest is null). First census: 4 matches, including both | FAIL (minor; see M5) |

## How the partition reproduces (check 2)

- Family A, 310: name splits into exactly 3 hyphen parts matching a
  strict 10 × 10 × 10 product — slot 1: giga, hyper, mega, micro,
  mini, nano, piko, super, tiny, ultra; slot 2: clean, fast, lite,
  max, pro, pure, quick, safe, sharp, smart; slot 3: box, gem, hub,
  kit, lib, mod, pkg, rb, sys, tool. Author/date split is clean:
  129 / 113 / 68 across three author values, on July 6 / 13 / 12
  respectively. The university template covers 309 rows (116 distinct
  trailing values); the one off-template row is still family A by
  name grammar, so template 309 vs family 310 is expected, not a gap.
- Family C, 20: the remaining non-combinatorial rows whose names and
  summaries carry no probe signal (verified: zero hits on a probe-word
  screen of name + summary for all 20). They span July 6–12 with
  exactly 1 row on July 7.
- Family B, 203: the remainder. Every one of the 203 is first-published
  July 7 — an independent cross-check that the partition is not just
  arithmetic. Primary-bucket counts sum correctly (66 + 55 + 36 + 34
  + 6 + 3 + 3 = 203). Spot-verified non-exclusive signals in family B:
  `ssrf` word 58, link-verification wording 29, placeholder summary
  86 (54 / 19 / 9 / 4), webhook wording 7, cross-tenant wording 7,
  traversal/symlink wording 7, race wording 8, `ssrf-*` prefix 23
  (19 of 20 rows under one author value), epoch-suffixed names 34,
  strict `apex-black-test-NNN` 14 (11 under one author value).

## Mismatch register (cause: drift vs error)

### M1 — SSRF row count: census/lane counting error (not drift)

- Observed link rows: 24, not 23. Breakdown: IP-literal internal
  10 (link-local 3, loopback 6, RFC1918-10 1) + internal-hostname
  rows 4 + public-IP rows 10 = 24. Plus 1 summary-only row (a
  localhost URL carried in summary text, no link-field hit) = 25.
- Cause: the lane counted 3 internal-hostname rows where there are
  4. The two DNS-probe rows sharing one internal hostname shape were
  collapsed into one — a shape count (3 shapes) was used where a row
  count (4 rows) was needed. Homepage-cell hits are likewise 24, not
  23 (source cell: 1, on a row already counted via its homepage).
- Consequence: the "23 + 1 correction" does NOT hold as a row count.
  Payload union = 29 + 19 + 25 + 10 + 4 = 87, minus the single
  pairwise overlap (OAST ∩ XSS = 4 rows; every other pair overlaps
  0) = 83, not 82. Author-only rows still add 2 (9 author rows
  total, 7 already inside the union), so the all-fields total is 85,
  not 84. The public-IP split inside the SSRF set still holds: 10 of
  the 25 are public-IP homepages and must not be quoted as
  "internal targets" without that split.
- Fix F1 (blocking): change 24 → 25, 82 → 83, 84 → 85 everywhere, and
  state the row-vs-shape distinction. If the report wants a
  distinct-target figure, give it separately; do not let it replace
  the row count.

### M2 — jrjackson Diffend page: live drift (backfill), current-state mismatch

- Census (both independent censuses, same day): Diffend stub.
  Fresh check (same day, hours later): Diffend 200, ~21 KB, 35
  version-pair links, pair dates in October 2026. A second fresh
  fetch minutes later reproduces the full page exactly — this is
  not a transient fetch glitch.
- Cause assessment: drift, not proven census error. Two independent
  censuses agreed on stub, and the gem itself is unchanged
  (fresh API: same latest version as the first census, downloads
  up only ~190 on a ~10.5M base). The plausible mechanism is Diffend
  backfill: version-pair diffs computed after the census fetches.
  A pure census error cannot be ruled out from two time points, so
  the report must describe this as "now full; was stub at census"
  rather than asserting either side was wrong.
- Consequence if shipped uncorrected: Diffend full 18 → 19,
  live-only 5 → 4, artifact URLs 48 → 49 (jrjackson's Diffend page
  joins the artifact set). Survivor classification for jrjackson
  itself does NOT change — it remains legit (see spot-checks).
- Fix F2 (blocking): re-run the Diffend check for at least the 5
  census live-only names (ideally all 23 live names) at ship time
  and update the full / live-only / artifact counts to the fresh
  result. Do not ship the census-day 18 as a current-state claim
  without that refresh.

### M3 — "105 probe-descriptive": irreproducible as stated (definition gap)

- 117 reproduces exactly under the stated rule: family B rows with
  a non-placeholder summary (203 − 86). 105 does not reproduce
  under any rule tested: plain-word descriptive (excluding the 14
  markup/template summaries) = 103; first-match markup exclusion
  (105 + 8 markup-first-match) = 113; the integrated linguist's own
  candidate exclusions (10 markup-only + 1 pipe-separated row)
  account for at most 11 of the 12-row gap, not 12. A prior verifier
  note records a broad-keyword approximation of 102, also not 105.
- Fix: do not quote 105 without its first-match inventory attached.
  Headline with 117 (defined as above) or 103 (plain-word only,
  defined as above); treat 105 as lane-classified, not verified.

### M4 — Diffend raw status field is inconsistent for redirects (method inconsistency, no artifact impact)

- Fresh no-follow checks: all 6 sampled redirect-index pages return
  302 to the Diffend index. Census `diffend_status` records 302 for
  3 of them and 200 for the other 3 — i.e. followed status was
  recorded for some rows and unfollowed status for others. The same
  split appears between the two prior censuses (first: 200 for all
  6; helper: 302 for 3 of them).
- Related definition problem: 27 tombstone rows with status 302 are
  labelled `stub`, while one identically-behaving row (redirect to
  index) was adjudicated `gone`. "Stub" in the census files therefore
  means "no Diffend diff artifact", not "Diffend served a stub
  page". That reading is consistent with every artifact count, but
  the label must be defined that way in the report; otherwise the
  302/200 split looks like a classification disagreement.
- No artifact, live-status, or survivor consequence: redirect pages
  carry no pair links for the sampled name in all 6 cases.

### M5 — Minor text/data fixes (non-blocking, fix in the same pass)

- XSS-word signal (check 19): quote 10 rows, not 14; 14 is the
  occurrence count across name + summary.
- Version-match sentence (check 20): on reconciled-JSON data the
  three matches are apex-black-test-011, apex-oidc-probe, and
  test_gem_kangaroo; on first-census data there are four matches
  (those three plus minitest-hashdiff). The shipped sentence
  matches neither dataset as written. Also, 9 of the 23 live rows
  in the reconciled JSON carry null latest-version / version-count
  fields although the first census has values for them — fill those
  fields from the first census or a fresh API pull before quoting
  version comparisons.
- Apex prefix note N1: substring 115 is correct, and 114 is also
  reproducible — as names *starting with* `apex` (80 dash-form +
  32 underscore-form + 2 concatenated-form), with exactly 1
  substring-only name not starting with `apex`. The integrated
  linguist's claim that "no prefix rule gives 114" is wrong under
  the broad starts-with rule; the report should say "115 substring,
  114 prefixed" and stop there.
- Artifact-field trap N2: `artifact_urls_uniform` (49 URLs) is a
  pre-reconciliation field — it still contains the 2 excluded
  callback endpoints and drops one source URL that the reconciled
  set carries at its new location. Only `artifact_urls` (48) equals
  the reconciled txt. Never quote the uniform field as the artifact
  set. The broader `lane_artifact_urls` field (387 URLs, mostly
  tombstone pages) is not an artifact union at all and must not be
  described as one.

## Survivor spot-checks (8 of 23, fresh API + Diffend, classification stands)

| Survivor | Class | Fresh API (version / downloads) | Fresh Diffend | Verdict |
|---|---|---|---|---|
| sportdb-parser | legit | 0.8.0 / 25,579 (first census identical) | full, ~23.6 KB, 168 version patterns | stands |
| eco-helpers | legit | 3.4.0 / 438,243 (first census 438,219; +24) | full, ~21.7 KB | stands |
| minitest-hashdiff | legit | 0.1.1 / 2,396 (first census 2,395; +1) | stub, single-version page, no pair links | stands — a test helper is legit by function, not by the word "test" |
| jrjackson | legit | 0.3.8 / 10,508,543 (first census 10,508,353; +190) | NOW full (see M2); class unchanged | stands, Diffend class changed |
| apex-black-test-011 | probe | 9.9.9 / 516 (first census 515; +1) | stub, single-version page | stands |
| apex-oidc-probe | probe | 0.1.1 / 552 (first census 550; +2) | stub, single-version page | stands |
| apex-blk-test-final | probe | 0.0.1 only / 1,283 (first census 1,282; +1); CSV latest 0.0.5 absent live | stub, single-version page | stands — version-yanked listing residue |
| testgem-mini | test | 0.4.0 / 34,152 (first census 34,151; +1) | full, ~8.7 KB, 30 version patterns | stands |

Download drift on spot-checked survivors is small (+1 to +190) and in
the expected direction (counts only rise); no survivor's downloads,
version, or name contradicts its class. The first-census download
total for all 23 live gems (11,138,862) reproduces exactly from that
census file; it is a census-day figure, not a current figure, and
should be labelled as such.

## What this verification does NOT cover

- Gem code, gemspec bytes, rendered-page HTML, and receiver logs
  were not examined; payload strings prove publication of strings
  only, as the cryptologist lane already states.
- The fresh sample covers 30 random + 8 targeted names, not a full
  re-census. A full re-census could surface further Diffend
  backfill drift of the jrjackson kind; F2's live-set refresh is
  the minimum, not a guarantee against it.
- The 105 figure, the SSRF shape-vs-row distinction, and the
  redirect-status inconsistency are all in the lanes' own working
  files; this report flags them for the coordinator rather than
  silently correcting lane files, which are outside this lane's
  write scope.

## Required fixes before ship (blocking)

1. **F1:** SSRF 24 → 25 (24 link + 1 summary), payload union 82 → 83,
   all-fields total 84 → 85, with the 10-public-IP split retained.
2. **F2:** Refresh Diffend for the live set at ship time; if
   jrjackson is still full, Diffend full 18 → 19, live-only 5 → 4,
   artifact URLs 48 → 49.

## Fixes to fold into the same pass (non-blocking)

3. Replace or define 105 (use 117 non-placeholder or 103 plain-word,
   with the rule stated); correct XSS-word 14 → 10 rows; correct the
   version-match sentence and fill the 9 null version fields in the
   reconciled JSON (or stop quoting version comparisons from it);
   define "stub" as "no Diffend diff artifact" and note the 302
   redirect cases; warn that `artifact_urls_uniform` is
   pre-reconciliation; state apex as "115 substring, 114 prefixed".

*Verifier scope note: this lane performed read-only GET/HEAD checks
only, wrote only this file, and fetched no callback URI.*
