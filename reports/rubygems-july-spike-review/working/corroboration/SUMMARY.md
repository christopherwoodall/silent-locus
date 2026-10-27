# Corroboration lane — summary (2026-10-27)

Source CSV: `data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv`
(sha256 verified 765ee2f24e6ec1a191c66faee030aaea8586cc4a0cdde1bee4c0668a0f0f3ce0; 533 rows + header; all `withdrawn=True`).
Recompute script: `corroborate.py` in this directory. Matrix: `corroboration-matrix.{json,csv}`.
NEW list: `new-names.{json,csv}` (330 rows).

## Overlap counts (of 533)

- In v2 export (`reports/ruby-sus-gems-export-v2.json`, 3,036 rows): **203**
  - v2 wave null (JFrog GemStuffer-list rows): 192
  - v2 wave july-7: 11
  - v2 waves may-11-rehearsal, may-12-burst, june-18, march-7, other-probe-family: **0 each**
  - v2 source_grade: overlap 165, third-party-list 38
  - v2 triage_verdict: campaign-associated-per-JFrog-list 192; campaign 7; july7-window-test-gem (not GemStuffer) 4
- In lane JSONLs (5 files): **203**, all in `events.jsonl` only; 0 in gem-graph-nodes, gem-iocs-2026-09-27,
  gem-june18-wayback, gem-ioc-hits. The v2 set, the events.jsonl set, and the raw JFrog CSV set are
  exactly the same 203 names (verified by set equality in the script).
- In notes (`docs/notes/gem-*.md`, 54 files scanned): **18**, all a subset of the 203.
- In pins files / bundle.json: 0.
- In ANY of v2/lane/notes: **203**. NEW (absent from all): **330**.

## Per author (CSV author field, exact)

- Andrey78: 129 rows, 0 known, 129 NEW
- Prvaz12_mars: 113 rows, 0 known, 113 NEW
- tester (lowercase): 100 rows, 100 known, 0 NEW
- monib110: 68 rows, 0 known, 68 NEW
- All other author strings combined: 123 rows, 103 known, 20 NEW
  (the 20 NEW are ordinary-looking gem names with blank dashboard/haiku fields; see NEW list)

## Per CSV first-published date

- 2026-07-06: 132 rows, 0 known (129 Andrey78 + 3 small NEW)
- 2026-07-07: 204 rows, 203 known, 1 NEW (jrjackson, author Guy Boertje)
- 2026-07-08: 8 rows, 0 known
- 2026-07-09: 4 rows, 0 known
- 2026-07-10: 2 rows, 0 known
- 2026-07-12: 70 rows, 0 known (68 monib110 + 2 small NEW)
- 2026-07-13: 113 rows, 0 known (all Prvaz12_mars)

## July-7 relation verdict: PARTIAL OVERLAP, disjoint authors except the probe batch

- v2 july-7 wave has 24 rows; 11 are in the CSV, 13 are not.
- The 11 shared names are the July-7 probe/test batch (Apex/Testing-animal/XSS/SSTI probe names).
- The other 192 CSV July-7 rows are v2 wave-null JFrog-list rows, not our july-7 wave rows.
- The CSV July-7 rows are dominated by author `tester` (100) plus t/SR/Test/T variants — author strings
  that v2 does not record (v2 package_author is null for 196 of the 203 overlapping rows).
- The 13 v2 july-7 rows absent from the CSV are ALL july7-window-test-gems (not GemStuffer):
  a--0zlink83721, attacker-homepage-xss, test-metadata-xss-1, test-metadata-xss-3,
  test-xss-name, test-xss-rhino, test-xss-xss-data, test-xss-xss-html, test-xss-xss-img,
  test-xss-xss-link, test-yaml-rce, test_gem_no_mfa, zlink83721.
  The 11 shared july-7 rows split 7 campaign + 4 window-test-gems.

## Andrey78 verdict: ENTIRELY NEW TO US

- 0 of 129 in v2, lane files, or notes; author string `Andrey78` appears nowhere in the 5 lane
  files or any gem note. Same for `Prvaz12_mars` and `monib110` (author strings absent everywhere).
- Factum sample (below) confirms not_found for all 4 sampled Andrey78 names.

## Factum sample (READ-ONLY exact match; 30 names; full output `factum-sample-output.txt`)

- Sampling: 21 NEW (Andrey78 x4, Prvaz12_mars x4, monib110 x3, small-NEW x10) + 9 known
  (july-7 wave x5, null-wave tester batch x4). One command per name, `--mode exact`,
  corpus commit 19a11da46960cd6510e0d43889dba2271df0a1b0.
- Result: all 21 NEW = `not_found`; 8 of 9 known = `found`; 1 known (xss-test-gem) = `candidate`
  (near-match status; the name is still confirmed known via v2 + lane + notes).
- Factum was NOT run exhaustively (533 exact matches would be ~30+ min at observed pace);
  the sample is stratified as stated, and the exhaustive local sources (v2/lane/notes) already
  cover all 533 names, so Factum adds no new classification — it only cross-checks the sample.

## Live spot-checks (2026-10-27 ~20:07–20:12 UTC; READ-ONLY GET; full bytes saved)

RubyGems API (20 names) + Diffend (10 names) under
`data/lanes/rubygems-july-spike-review/raw/corroboration/`, each with `.PROVENANCE.txt` + `.sha256`.
Extra: versions-list fetches for the 6 live names (`rubygems-versions-*.json`).

- Mass-generated batches GONE from registry: all 10 sampled Andrey78/Prvaz12_mars/monib110 names
  return RubyGems API 404 ("This rubygem could not be found.") — consistent with CSV withdrawn=True.
  Their Diffend pages return 200 but contain only the "no computed diffs" shell (no version data).
- Overlap probe batch MIXED: test-apex-gem, xss-test-gem, test-ssti-0, apex-black-test-012 = 404
  (gone); apex-blk-test-final and test_gem_kangaroo = still live on the API (200), authors
  Apex Black / Testing Kangaroo, latest versions 0.0.1 / 0.0.14. Diffend for test-apex-gem and
  test-ssti-0 returned a generic Diffend index/listing page (not a gem page) — recorded as
  inconclusive, not as absence.
- Small NEW names ALIVE: jrjackson, shirobai, sportdb-parser, edoxen all return API 200 with
  current versions and real download counts; Diffend shows real version diffs, including
  Oct 2026 releases for jrjackson and shirobai. Their CSV window versions are still listed
  by the versions API (jrjackson 0.5.2, sportdb-parser 0.8.0 present) — so for these names
  CSV `withdrawn=True` does NOT mean the gem is gone; it appears to be a per-version/window
  flag, and these 20 small NEW names look like ordinary live gems caught in a withdrawal
  window, not mass-generated batches. (apex-blk-test-final is the same shape: CSV latest 0.0.5
  is NOT in the live versions list, but 0.0.1 survives — i.e. one version yanked, gem alive.)
- No credential-shaped values were observed in any output handled here (count: 0).
- No live fetch failed for egress/timeout reasons; every non-200 is a genuine registry 404
  with the standard "could not be found" body, except the two Diffend generic-page cases noted.

## Caveats

- "NEW" means absent from v2 + the 5 lane JSONLs + 54 gem notes + (sample) Factum. It does NOT
  mean campaign membership: the 3 big batches (310 names) carry mass_generated haiku labels,
  but the 20 small NEW names carry blank dashboard/haiku fields and live-registry evidence
  pointing to ordinary gems.
- Overlap names are JFrog-list-derived in v2 (wave null, third-party-list/overlap grades);
  only the 11 july-7 rows have our own wave attribution. Overlap therefore corroborates the
  JFrog list, not independent lane observation, except where notes/events add detail.
- CSV author strings for probe-batch rows include XSS/SSTI payload text used as the author
  field; those strings are described here, not reproduced, except where a name itself is one.
