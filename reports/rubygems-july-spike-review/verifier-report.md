# Verifier lane report — RubyGems July spike CSV review

Verdict: **SHIP-WITH-FIXES** (7 fixes, all wording/count corrections; no
finding is overturned and no load-bearing conclusion changes).

Method: independent recomputation from the preserved CSV and the source
files only. Lane scripts were not used as proof. All counts below were
recomputed by fresh scripts run by this lane on 2026-10-27.

Source CSV: `data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv`,
sha256 `765ee2f24e6ec1a191c66faee030aaea8586cc4a0cdde1bee4c0668a0f0f3ce0`
(recomputed, matches the preserved `.sha256` sidecar and REPORT.md).

## Per-check results

| # | Check | Recomputed value | Result |
|---|---|---|---|
| 1 | Rows / columns / header | 533 rows + header, 20 columns, 533 unique names | PASS |
| 2 | Doc-ID version match | 530 match; 3 platform-suffix mismatches only (java, java, x86_64-linux) | PASS |
| 3 | Date extremes | First 2026-07-06 00:27:26; last 2026-07-13 19:35:05 | PASS |
| 4 | Per-day first-publish | Jul 6 = 132, Jul 7 = 204, Jul 8 = 8, Jul 9 = 4, Jul 10 = 2, Jul 12 = 70, Jul 13 = 113; no Jul 11 | PASS |
| 5 | Withdrawn | True on 533 of 533 | PASS |
| 6 | Versions | 0.0.1 on 452 rows; 33 distinct latest_version values; versions_in_window 1 on 491, multi on 42 | PASS |
| 7 | Dependencies | 0 on 509 rows; 1–22 on the other 24 (max 22) | PASS |
| 8 | Summary / homepage / source | Summary on 533 (224 distinct); homepage empty 100; source empty 327 (61.4%) | PASS |
| 9 | Empty dashboard/haiku rows | 49 rows empty in all eight fields; 6 are monib110; Jul 8–10 have zero scored rows | PASS with FIX-6 wording |
| 10 | Per-author counts | Andrey78 129, Prvaz12_mars 113, tester 100, monib110 68; 46 author values total; remaining 123 rows over 42 further values | PASS |
| 11 | Bursts | Andrey78: 88 in 60 min, median gap 41 s, Jul 6 only. Prvaz12_mars: 68 in 60 min, median 43 s, Jul 13 only. tester: 37 in 60 min, median 38 s, Jul 7 only. monib110: whole batch in 59.5 min, median 48 s, Jul 12 only | PASS |
| 12 | Fuzz / markup authors | One 151-token fuzz author value; 9 markup/template-expression author values | PASS |
| 13 | Combinatorial grammar | 310 three-slot names, zero duplicates, all Andrey78 129 / Prvaz12_mars 113 / monib110 68; 10 x 10 x 10 word product confirmed | PASS |
| 14 | tester naming | `apex` first token on 95 of 100 (dash/underscore tokenisation); `black` second on 68; strict `apex-black-test-NNN` 11 inside tester, 14 cross-author | PASS |
| 15 | Probe shapes | SR epoch-suffixed 13 of 13; Test epoch-suffixed 10 of 10 | PASS with FIX-5 |
| 16 | Summary templates | `University research based on` 309 rows, 116 distinct X; Andrey78 uses all 116; Prvaz12_mars 112 of 113; bare placeholders 86 (`Test` 54, `testing` 19, `T` 9, `test` 4) | PASS |
| 17 | Dashboard rule tokens | 15 tokens, counts exactly: combinatorial 372, shared text 185, owner burst 158, placeholder author 122, numbered name 115, template batch 100, placeholder text 92, name series 66, probe name 59, oob url 48, short author 43, test name 41, markup 12, placeholder link 8, random name 1; 73 distinct rule strings | PASS |
| 18 | Dashboard levels | low 121, medium 193, high 19, critical 151, empty 49 | PASS |
| 19 | Dashboard level = rule count | low = exactly 1 rule (121/121), medium = 2 (193/193), high = 3 (19/19), critical = 4–8 (151/151); no rule string maps to two levels | PASS |
| 20 | Haiku levels / categories / activity / prompts | Levels high 385, critical 80, medium 15, low 4, empty 49. Categories mass_generated 305, registry_test_or_probe 178, unclear 1 (giga-pure-tool, monib110, Jul 12), empty 49. Activity possible 461, likely 18, no_sign 5, empty 49. Prompts pkg-review-1 464, pkg-review-2 20, empty 49 | PASS |
| 21 | Haiku scores | Present on 20 rows only (the pkg-review-2 rows), values 42–92; medium 42–45, high 62–72, critical 88–92; bands 46–61 and 73–87 empty | PASS |
| 22 | Dashboard–Haiku agreement | 88 of 484 scored rows (18.2%); low→high 111/121; medium→high 188/193; critical→critical 73/151 | PASS |
| 23 | Prompt-version calibration | v1: high 381/464 (82.1%), medium 5 (1.1%), low 4 (0.9%); v2: medium 10 (50%), critical 6 (30%), high 4 (20%) | PASS with FIX-4 (v1 critical %) |
| 24 | Matched-shape v1/v2 split | Combinatorial-only: v1 114 rows (111 high, 3 medium), v2 5 rows (all medium). Combinatorial+shared: v1 178 rows (all high), v2 5 rows (4 medium, 1 high) | PASS |
| 25 | Identical shapes, different levels | 377 of 484 scored rows sit in a rule-string group whose Haiku level is not unique; tester clean cases confirmed (ipv6-001 critical vs -002 high; race-000/002/003/004 critical vs -001 high; probe-000/002/003 critical vs -001 high; fuzz-006r/007r mass_generated amid probe siblings) | PASS |
| 26 | Reason rhetoric | 484 non-empty reasons, all 484 distinct; agent word on 38, all registry_test_or_probe, zero mass_generated; `no … agent` phrasing on 30; MFA/publisher assertions on 355; keyword hits (case-insensitive substrings): combinatorial 329, batch 266, MFA 289, zero-deps 311, unrelated 162, SSRF 92, deception 12, lookalike 10 | PASS |
| 27 | Reason classes | First-match classes sum to 484: batch/combinatorial 272, probe/test 126, automated no-agent 46, agent-word 38, other 2 | PASS |
| 28 | Section 2 verbatim quotes | All 5 quoted reasons match exactly one CSV row each, character for character (mini-sharp-hub; nano-clean-hub; apex-black-test-001; apex-black-test-017; apex-black-test-030) | PASS |
| 29 | Cut-off reasons | Exactly 5 reasons do not end with a period, all exactly 300 characters (mini-fast-rb, nano-max-rb, piko-sharp-gem, hyper-max-sys, tiny-pure-gem); none is quoted in REPORT.md, so no quote completes one | PASS |
| 30 | Reason batch-number disagreements | monib110 reasons say 60 (dominant) vs 68 rows; tester reasons say 101 and 71 vs 100 rows; one Andrey78 reason says 134 vs 129 rows | PASS |
| 31 | Payload components (individually) | OAST 29 rows, 6 hosts; webhook.site 19 rows by substring in homepage/source/summary, 18 by homepage host, 9 UUID paths; combined OOB 48, sets disjoint; SSRF/internal homepage rows 24; plain-http homepage/source rows 12; XSS summaries 10; SSTI summaries 4; payload authors 9; ssrf-/webhook- names 26, of which 12 carry an OOB/IP homepage and 14 do not | PASS individually; union wording needs FIX-1 |
| 32 | Payload union (82) | Union of the five non-author sets (OAST 29 + webhook-substring 19 + IP 24 + XSS 10 + SSTI 4) = 82. But the lane inventory lists union to 83 (webhook host 18), and any-column union including author = 84 | FAIL as worded — see FIX-1 |
| 33 | Explicit nones | go-import, jina, UK-council, cloud-bucket, curl/wget/eval/os.system/subprocess, VCS-scheme strings: 0 rows each across all columns; no genuine base64 blob token found (non-repeating, 40+ chars) | PASS |
| 34 | Credential-shaped values | Count only, no values copied here or in REPORT.md: 5 summary-only rows by the lane inventory method; 7 rows by substring token/api-key across summary+reason; 0 key-shaped patterns (sk-/ghp_/AKIA shapes) | PASS (range 5–7 as REPORT.md states) |
| 35 | Corpus overlap totals | Known 203 of 533; NEW 330 (big three 310 + 20 small-author names); NEW mass_generated 303, NEW blank-haiku 26 (20 small + 6 monib110), NEW unclear 1 | PASS |
| 36 | Set equality (v2 / lane / JFrog) | v2 ∩ CSV = 203; lane events.jsonl (labels `gem.name` on campaign_specimen records) ∩ CSV = 203; raw JFrog CSV `Package` ∩ CSV = 203; all three sets identical, pairwise diffs empty | PASS (see note N-1 on extraction) |
| 37 | Per-wave / per-grade | Wave-null 192, July-7 11, all other waves 0; source_grade overlap 165, third-party-list 38 | PASS |
| 38 | Per-author known | Andrey78 0/129, Prvaz12_mars 0/113, tester 100/100, monib110 0/68, all other author strings 103/123 | PASS |
| 39 | Per-date known | Jul 6 0/132, Jul 7 203/204, Jul 8–13 0 known (8/4/2/70/113 rows) | PASS |
| 40 | Notes | 54 gem-note files; 18 CSV names mentioned, all inside the 203 | PASS |
| 41 | July-7 relation | v2 July-7 wave 24 rows: 11 in CSV (7 campaign + 4 window-test), 13 absent (all window-test); CSV Jul-7 rows: 192 wave-null JFrog + 11 July-7-wave + 1 NEW (jrjackson) = 204 | PASS |
| 42 | Big-author strings absent | Andrey78, Prvaz12_mars, monib110: 0 occurrences in events.jsonl, the four other lane JSONLs, and all gem notes | PASS |
| 43 | Factum sample | Saved sample list 30 names; saved output 30 sections: 21 NEW not_found, 9 known (8 found + xss-test-gem candidate) — matches REPORT.md exactly | PASS (sample file, not a fresh Factum run) |
| 44 | Live fetches present | 36 base files: RubyGems API 20, Diffend 10, versions lists 6; every file has `.PROVENANCE.txt` + `.sha256` (API/Diffend also have 0-byte `.curlerr`; versions fetches have no `.curlerr` sidecar) | PASS |
| 45 | Live fetch hashes | All 36 `.sha256` sidecars recomputed and matching (20 API + 10 Diffend + 6 versions) | PASS |
| 46 | Live fetch contents | 404 bodies (32 bytes, "could not be found") for 10 mass-batch samples (4 Andrey78 / 3 Prvaz12_mars / 3 monib110) and 4 overlap probes (apex-black-test-012, test-apex-gem, test-ssti-0, xss-test-gem); 200s with real download counts for 6 live names (apex-blk-test-final, test_gem_kangaroo, jrjackson, shirobai, sportdb-parser, edoxen); Diffend stubs ("no computed diffs") for the 4 mass-batch Diffend samples; generic Diffend index pages (identical 12,986-byte bodies, generic title) for test-apex-gem and test-ssti-0; real diffs for jrjackson, shirobai, sportdb-parser; versions lists: apex-blk-test-final has only 0.0.1 (CSV latest 0.0.5 absent); jrjackson versions include 0.5.2 and an October 2026 release; shirobai versions include October 2026 releases; sportdb-parser versions include 0.8.0 | PASS with FIX-7 (generalisation wording) |
| 47 | findings.json | Parses; 23 findings, ids F01–F23, no gaps; every finding has claim, evidence, grade, verdict; grades match the claim-basis convention used throughout (OBSERVED = counted/fetched, INFERENCE = reasoned judgement, UPSTREAM = dashboard/label claim) | PASS with FIX-1 (F04 evidence) and FIX-7 (F10 claim text) |
| 48 | CSV preservation | sha256 recomputed = preserved sidecar = REPORT.md value; CSV mtime 2026-10-27 20:04 predates the review working files (20:06–20:13); events.jsonl, JFrog CSV, and lane SHA256SUMS entries for both match their recorded hashes; v1/v2 export mtimes (18:56 / 19:06 UTC) predate the review | PASS with note N-3 |

## Fixes required (SHIP-WITH-FIXES list)

- **FIX-1 — payload-union definition (REPORT.md section 3 and findings.json F04).**
  The 82-row union is the union of the five non-author sets only
  (OAST 29 + webhook-substring 19 + IP-homepage 24 + XSS-summary 10 +
  SSTI-summary 4 = 82). The two author-only payload rows
  (test-yaml-erb and xssname-1783397821) sit outside the 82, and only
  7 of the 9 payload-author rows are inside it. The lane inventory
  lists alone union to 83 (webhook host 18), and the any-column union
  (including author) is 84. REPORT.md must state the scanned-column
  set explicitly (name / summary / homepage / source, author
  excluded), correct F04's parenthetical (it currently lists
  "payload authors 9" as a component of the 82), and add one
  sentence: total rows carrying a payload string in any column
  including author = 84. Until then, "the other 451 rows carry no
  payload string in scanned columns" is true only under the
  author-excluded definition, which the report never states.
- **FIX-2 — "likely" neither-count (REPORT.md section 5).**
  "10 of 18 reasons contain no agent or automation word" recomputes
  to 9 under both substring and exact-word counting: 7 agent-word +
  2 automation-only + 9 neither = 18. The report's 7 + 2 + 10 = 19
  is internally inconsistent. Change 10 to 9 (keeping the substring
  definition behind the "7 contain agent" claim).
- **FIX-3 — hedge phrasing (REPORT.md section 5).**
  "3 explicitly hedge ('plausible but not certain')" overstates the
  phrase: 3 likely reasons contain "plausible", but only 2 contain
  the exact phrase "plausible but not certain"; the third says
  "plausible given the systematic batch". Reword to "3 hedge with
  'plausible' (2 with the exact phrase 'plausible but not certain')".
- **FIX-4 — v1 critical percentage (REPORT.md section 5).**
  "v1: high 82.1%, critical 16.0%, medium 1.1%, low 0.9%" — the
  critical figure recomputes to 74/464 = 15.9%. Change 16.0% to
  15.9%. (All other percentages in the report recomputed exactly.)
- **FIX-5 — ssrf pattern wording (REPORT.md section 1).**
  "ssrf-[target]-[8-hex] (author t, 19 of 20 rows)" — 19 of 20 t rows
  are ssrf-* names, but only 18 carry an 8-hex suffix; ssrf-chain-a
  carries a 10-digit epoch suffix. Reword to "ssrf-* names on 19 of
  20 t rows (18 with 8-hex suffix, 1 epoch-suffixed)".
- **FIX-6 — partial-empties wording (REPORT.md section 1).**
  "No partial empties exist" is literally false if haiku_score
  counts: score is empty on all 464 pkg-review-1 rows while their
  other fields are present. It is true for the other seven fields.
  Reword to "No partial empties exist among the other seven fields;
  haiku_score is empty on all 464 pkg-review-1 rows by design."
- **FIX-7 — live-state generalisation (REPORT.md section 3 bullet and
  findings.json F10 claim text).**
  "The batches are wholly gone from the registry" generalises from
  10 sampled API 404s to all 310 batch names. F10's verdict already
  qualifies correctly ("for the sampled names"). Reword the section
  3 bullet and the F10 claim to "the sampled batch names are gone".

## Notes (not fixes, not blocking)

- **N-1 — events-set extraction.** Set equality holds when lane
  events are extracted as labels `gem.name` on campaign_specimen
  records (203 names, identical to v2 and JFrog sets). A naive
  `node.package` extraction yields 0 of the 203, because the July-7
  probe names live in specimen records, not gem graph nodes. REPORT.md
  should name the `gem.name` extraction for reproducibility; the
  equality claim itself passes.
- **N-2 — probe-descriptive summaries (105).** An independent broad
  keyword approximation gives 102, not 105; the 105 is the linguist
  lane's first-match classification with a documented shape inventory
  (LINGUIST.md section 2c). This is definition-dependent, not a
  proven mismatch, and the count is not load-bearing. Kept as
  lane-classified.
- **N-3 — lane SHA256SUMS staleness (pre-existing, not this review).**
  The lane SHA256SUMS check passes for events.jsonl and the JFrog
  CSV but fails for the lane PROVENANCE.md. Both files carry
  2026-10-13 mtimes, predating this review, so the mismatch is a
  pre-existing stale entry, not a review modification. Flagged for
  lane hygiene only.
- **N-4 — "near-unique" reasons.** The 484 non-empty reasons are in
  fact fully unique (484 distinct strings), not merely near-unique.
  REPORT.md's wording is true but weaker than the evidence.
- **N-5 — Factum sample.** Verified against the saved sample list
  and saved output (30/30 sections, statuses as above). No fresh
  Factum run was made by this lane; exhaustive classification rests
  on the local sources, as REPORT.md states.
- **N-6 — scope.** This lane did not touch the agent-egress-deep-dive
  lane, the staged-tree branch, or any git state. No Factum writes
  were made. No credential-shaped cell values are copied in this
  report (presence and counts only).

## SHA256SUMS

Regenerated after writing this report, covering REPORT.md,
findings.json, adversarial-review.md, verifier-report.md, and
MANIFEST.md. Note: the top-level SHA256SUMS did not exist before
this lane created it (MANIFEST.md describes it, but the file was
absent); the regeneration below is its first creation. Any of the
FIX-1–FIX-7 edits will change REPORT.md / findings.json hashes, so
SHA256SUMS must be regenerated again after the fixes land.
