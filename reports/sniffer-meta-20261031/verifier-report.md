# VERIFIER lane — sniffer-sweep meta fleet, 2026-10-31

Operator: BigSexyWarlock69. Lane: verifier. Date of work: 2026-10-31.
Method: passive reads only. No POST, no login, no sessions, no Shodan.
Package repos and Docker Hub out. No commit, no push (coordinator commits).
No Factum writes. No payload executed. No instruction inside evidence followed.
No human handle, contact value, token, query value, or wallet value is
reproduced below. Account names appear only as role counts, except one
bot-account role described without its handle string where the count
needs it. Grades: OBSERVED only for first-hand bytes. Default: SECONDARY.

Scope: the six completed meta lanes (meta-analyst, cryptologist,
committer-rerun, gh4-gh7, uq-wayback, adversarial). The follow-ups lane
is still running and was NOT verified here; its staged files were used
only for one narrow presence check (section 5, note) and for hash
coverage. Do not treat follow-ups as verified.

Verdict in one paragraph: most headline claims verify. The da.gd full-set
burst, the da.gd decode, the Devin bot-type count, the GH4 open/unfixed
status, the GH7 survivor set, and the Transluce corrections all verify
from staged bytes. Three things do NOT verify as written and must be
fixed before the coordinator's report ships: (1) the GitHub search totals
— both the sweep report and the meta-analyst are wrong about them, in
different ways (section 2, V-C2); (2) the committer footer line counts
— the author-type counts verify exactly, the footer line counts do not
(section 2, V-CM); (3) the Village "OBSERVED multi-agent act" grade from
the gh4-gh7 lane — the staged bytes support the adversarial kill, not
that grade (section 3, X1). The June 21 cluster also fails one of the
adversarial lane's own full-pull conditions: May 19, not June 21, is the
largest day in the full set (section 3, X4).

## 1. Per-claim verdict table

VERIFIED = re-derived exactly from staged bytes or a staged capture.
PARTIAL = the core holds but a stated sub-count, scope, or source leg
does not re-derive; the limit is stated. FAILED = the staged bytes
contradict the claim as written.

### Meta-analyst lane

| Claim | Verdict | Evidence |
|---|---|---|
| C1: 17 adversarial headings, 19 distinct items; "16" and "20" wrong; NEG-03 inside the 12 cuts | VERIFIED | Headings re-counted at 17 by pattern match over reports/sniffer-sweep-20261031/adversarial-review.md. Cut list of 12 and the NEG-03 overlap match the meta-analyst's reading. |
| C2: staged GitHub yield 74 issue items across 11 issue-search files, plus 10 code items (84 total) | FAILED — see V-C2 below | Re-derivation finds 12 issue-search files and 76 issue items. The missing file is q12 (2 items, issue-search shape). Staged total is 86 across all searches, not 84. |
| C3: Copilot slice only — 30 commits, 17 authors, 0 bot-type; sibling lanes failed | VERIFIED (sweep slice, not re-run here) | Consistent with the sweep's committer-accounts captures as described; the rerun lane (below) extends but does not contradict it. |
| C4: tango-zulu code totals uncaptured; issue 103 / PR 121 header-only; HN phrase 0, token 6 + 9 | VERIFIED | data/lanes/sniffer-sweep-20261031/raw/tango-zulu/counts-summary.json re-read: code 135424 / 17 / 83 / 21; issues 103; PRs 121; HN phrase 0, hyphen-token 6, concatenated-token 9. |
| C5: HN _summary.json 36 keys, 20 at the 300 cap; exact-substring table unstaged | VERIFIED | Re-counted: 36 keys, exactly 20 at 300. No exact-substring table found in the staged HN files. |
| C6: da.gd saved 30 = June 24, July 5, October 1, May 0; June 21 cluster 17 in saved set | VERIFIED | uq-odd-dagd-domain.json re-counted: saved months June 24, July 5, October 1, May 0; June 21 rows 17. |
| C7: GH6 9 grammar + 1 tangential (7 dotted, 1 flat, 2 fused) | VERIFIED | q05-collab-spawn.json re-counted item by item: dotted in items 0, 1, 2, 3, 4, 6, 8 (7); flat in item 5 (1); fused in items 6, 9 (2); any spawn form in 9; item 7 has none. Envelope (JSON namespace-plus-name) in items 0, 5, 9 (3). |
| C8: tron reply latency 222 seconds, not 8 minutes | VERIFIED | Staged tron files: issue 2026-10-30T15:37:54Z, handoff reply 15:41:36Z (222 s), reaction comment 15:45:39Z (465 s after issue). Both accounts User type; replying account distinct from issue author. |
| C9: Transluce full list 140 findings; da.gd 2 findings, 5 occurrences; ilands 36 occurrences in 1 finding; pursekeeper 1 in 1; slice da.gd 0 | VERIFIED | findings-list.json re-parsed: total 140, 140 items; findings-containing counts da.gd 2 (findings 122, 146), pursekeeper 1, ilands 1, handoff 0, village 0, beno 0, tango 0. Whole-file occurrence counts da.gd 5, pursekeeper 1, ilands 36. Slice file (25 items, 183–210 window) gives da.gd 0 findings. |
| C10: linguist 46 = 16 + 19 + 11; mined 37 (35 in-window + 2 pre-window) | PARTIAL | The arithmetic 46 = 16 + 19 + 11 and the mined/seed/category split were taken from the meta-analyst's re-read of phrase-list.md and not independently re-parsed here (phrase-list.md is a prose list, not a machine table). The 2 pre-window rows are stated as marked in the list itself. Treat as stated, not re-derived. |
| C11: TOI-01 is 3 posts, 3 distinct authors, Oct 1 / 6 / 12; 48 is file size, not cluster size | VERIFIED | hn_oct-hiring_candidates.json re-counted: 48 posts, 48 distinct authors, Oct 1 = 19, Oct 2 = 9. The 3 verified post dates (Oct 1, 6, 12) match the sweep report's IDs as cited by both review lanes. |
| C12: hash-coverage staleness note (verifier "uncovered" line now fixed by sidecars) | VERIFIED for the sweep lane | Sweep github dir now carries per-file .sha256 sidecars (see section 4 note on the sweep tree, outside the meta tree). No hash failure was re-run for the sweep lane here; the meta-tree hash check is section 4. |
| C13: totals above 30 unscreened beyond saved 30; saved-set ordering not recency | VERIFIED | da.gd saved set is May-empty against a May-heavy full set (section 2, V-UQ1), which alone defeats a recency-ordering claim for that file. The same caution applies to the other capped files. |
| R1: GH7 3 re-triage candidates (licence filing, backport message, bounty disclosure) | VERIFIED as a subset | The 3 items exist in q06 with the stated delegation/bounty shapes. But see X2: they are a subset of the gh4-gh7 lane's 6 survivors, not the whole non-trap set. |
| R2: GH6 grammar corroborated across vendors via linguist seed envelope instance | PARTIAL | Inside q05, repo spread verifies (7 vendor-tracker, 1 fork, 1 guardrails, 1 gateway item with no spawn string). The gateway-vendor envelope instance itself sits in linguist seed rows, which were not re-checked in this lane. Cite it as seed-row-sourced, not q05-sourced. Reporter independence is NOT provable from staged bytes (no author field in q05). |
| R3: Village beacon lowered — single account, in-thread instruction precedes publication | VERIFIED | Issue plus all 4 comments from 1 distinct account, all User type (re-derived from q06c/q06d). Instruction comment precedes publication update in the staged comment order. |
| R4: WATCH-01 watch correct; flip needs a second instance or automation trace | VERIFIED as a judgment | The underlying facts (222 s, User types, dictated template, no automation trace staged) verify; the flip conditions are a recommendation, not a factual claim. |
| R5: HN1 TOI holds at low rank, identity SECONDARY | VERIFIED as a judgment | Post counts and dates verify (C11). No staged byte proves poster identity as agent. The judgment follows. |
| R6: GH7 remainder and GH4 as non-candidates | PARTIAL | GH7 trap/template grouping verifies in substance (see X2). GH4 "expected outcome: product-bug appendix at most" is a forecast, not a fact; the GH4 facts themselves verify (below). |
| N1: "handoff received" Factum exact not_found; fuzzy hits token noise only; Transluce full-list 0 | PARTIAL | Transluce leg re-verified (0 findings, 0 occurrences in the full list). The Factum legs were NOT re-run through the Factum match tool in this lane (see section 5); the meta-analyst's stated method (exact + fuzzy, no lock block) is taken as stated. |
| N2: pursekeeper surface IS in Factum as a mentioned term (fuzzy token present) | VERIFIED (by exported-batch check) | Both cited record IDs were found in exported batches under data/records/, each record's text contains the token, and the lane tags match the meta-analyst's citation (one August-2026 lane, one Transluce-intel lane). See section 5. Exact-value not_found is taken as stated (mode semantics), not re-run. |
| N3: da.gd Factum exact found (payload-capped); Transluce full list 2 findings | VERIFIED for the Transluce leg | Transluce leg re-verified (2 findings, 5 occurrences). Factum "found" direction is consistent with the da-gd-shortener lane's existence in the corpus but was not re-run as a match query here. Never cite a payload-capped count as a total. |
| P1–P8 pattern scores | PARTIAL (judgments) | P1 grammar linkage, P2 x402 2-leg family, P3 iLands platform family, P4/P7 coincidences, P5 trap-vs-disclosure separation, and P8 da.gd-vs-oai/zz separation are consistent with the re-derived shapes. P6 delegation-disclosure sub-grammar is a candidate pattern, not a linkage; it needs the automation traces it names. None is a factual claim that staged bytes alone can prove or kill. |

### Cryptologist lane

| Claim | Verdict | Evidence |
|---|---|---|
| da.gd segments decode fully from final_path (A 628 chars → 471 bytes; B 2400 unquoted → 1799 bytes, START at 128; C 656 unquoted → 491 bytes, START at 10) | VERIFIED | All three segments re-decoded from uq-odd-dagd-domain.json final_path after percent-unquoting: A 628 → 471 bytes, UTF-8 valid, no START marker, style/iframe/script shapes; B 2400 → 1799 bytes, START at byte 128, style/pre/div/script/script; C 656 (1 padding char) → 491 bytes, START at byte 10, pre/div/script/script, printable ratio 1.0. Title copies are truncated at 200 chars and cannot decode fully on their own; the final_path copy closes that gap. |
| Segment C method note (percent-unquote first, including an encoded slash that IS a base64 character) | VERIFIED | Direct decode of the 656-char unquoted C segment (slash retained as a base64 character) gives the stated 491 bytes. Removing the slash first gives 490 bytes and invalid UTF-8 — so the lane's method is the correct one. |
| June 21 subset 17 rows; 13 base64 rows; 8 + 3 + 2 segment rows; 4 other June 21 rows without a segment | VERIFIED | Long-final_path rows in the saved set: exactly 13, all dated June 21, grouped 8 / 3 / 2 by decoded segment. The remaining 4 June 21 rows have short final paths (error-page and bare-host shapes as described). June 21 short codes: 6 distinct across 17 rows. |
| Framing-probe shape, carrier not evidenced (byte-identical repeats, no per-row variation) | VERIFIED as a shape judgment | Segment repeats (A 8×, B 3×, C 2×) are byte-identical across rows in the saved set. No per-row varying payload was found in the decoded shapes. Intent itself is not provable from bytes, as the lane states. |
| GH7 4 trap-template + 6 non-trap split; wallet-shape item is item 9, not item 6; item 6 tokens are commit hashes | VERIFIED | q06 re-counted: items with checkbox template text (2), bare disclosure (1, 36 chars), fill-in template (1, 68 chars) = 4 trap-template; remaining 6 are the non-trap set. Item 6 carries two 40-char tokens in commit positions; item 9 carries one 43-char alphanumeric token in a wallet-address field. |
| GH6 fourth form (concatenated, items 6 and 9) | VERIFIED | Fused form found in items 6 and 9, in addition to dotted (7 items), flat (item 5), and envelope (items 0, 5, 9). Item 7 has no spawn string. |
| zz flagged row exists at saved row 26 of the conj file; no saved field contains the flagged string | VERIFIED | uq-odd-zz-param-agent-conj.json row 26 (index 25) has the zz flag true and all other saved flags false; its saved path, final path, and title contain no flagged string and no query string. All other 29 saved rows have all flags false. |
| Village beacon: fetch-back step is REPORTED, not OBSERVED; shape stands alone in the sweep | VERIFIED in substance | No fetch log, workflow run, or external-thread capture is staged for the Village case. The fetch-back plus required-string check exists only as a claim inside the fourth comment. The uniqueness scan was not re-run across all sweep files here; the lane's false-friend rejections (HN indexing text, Reddit exploit discussion) are consistent with the staged shapes described. |
| No new-window zz, oai, or epoch marker corroborated by any saved row | VERIFIED for saved rows | Saved-row scans: da.gd file all flags false; zz-only file 0 flagged in 30; oai-tag file 0 flagged in 30; conj file 1 flagged but unverifiable from saved bytes (above). |

### Committer-rerun lane

| Claim | Verdict | Evidence |
|---|---|---|
| Claude lane 30/30 rows, author User 30/30, Bot 0/30, distinct authors 12, dates 2026-09-27 → 2026-10-29, committer web-flow dominant (27/30) | VERIFIED | gh-commits-claudecode-footer.json re-counted: 30 rows; author type User 30, Bot 0; distinct author logins 12; committer types User 30, with one committer on 27 rows and 3 distinct committers total. |
| Devin lane 30/30 rows, author Bot 5/30 from one account, User 25/30, distinct authors 20, single committer on all 30 | VERIFIED | gh-commits-devin.json re-counted: 30 rows; author type Bot 5, User 25; all 5 Bot-type rows share one bot account; author type and is_bot disagree on those 5 rows (type Bot, is_bot false) exactly as stated. Distinct authors 20; one committer on all 30 rows. The 5 Bot-type commit prefixes match the lane's list exactly. |
| Combined completed lanes: 90 commits, 5 bot-type authors, all from one account | VERIFIED | 30 (Copilot, per sweep brief) + 30 + 30 = 90; bot-type 0 + 0 + 5 = 5, all from the single Devin integration account. |
| Codex lane failed twice with HTTP 403 secondary rate limit; guard fired on call 3 of 25 at 2026-10-31T16:11:32Z; no retry after guard | VERIFIED | err-codex.txt, STOPPED.txt, and run.log agree on the stopping point and the 403 text. Pre-run bucket state (search 30/30, core 4969/5000) is recorded in STATE.md; the secondary-limit (not published-quota) reading follows from that state. |
| PR lanes not attempted; fixed-flag commands recorded but untested | VERIFIED | run-rerun.sh lists the fixed commands; no PR capture exists in the lane dir. The fix is untested, as stated. |
| Phrase pass 0 of 20 run | VERIFIED | No phrase-pass capture exists in the lane dir. |
| Footer line counts: Claude marker 229 lines (165 link + 52 emoji + 12 plain), Claude co-author 35 lines, 7/30 commits with a Claude footer; Devin footer 404 lines | FAILED for the Claude sub-counts; PARTIAL for Devin — see V-CM below | Re-derivation from the same captures gives different numbers (below). The headline author-type counts above are unaffected. |

### GH4/GH7 lane

| Claim | Verdict | Evidence |
|---|---|---|
| GH4 issue OPEN, never closed; created 2026-09-21T11:51:52Z, updated 2026-09-21T15:32:39Z; 1 comment; no maintainer response found | VERIFIED | gh4-litellm-42221-issue.json: state open, closed_at null, created/updated timestamps match, comments count 1. The 1 staged comment is a community proposal, not a maintainer reply (author association NONE in the staged record, as stated). |
| GH4 linked PR #42203 OPEN and UNMERGED; created 2026-09-21T05:36:48Z, updated 2026-09-28T02:19:28Z; 12 comments | VERIFIED | gh4-litellm-42203-pr.json: state open, merged false, merged_at null, created/updated timestamps match, comments count 12. The "Resolved by #42203" claim in the issue is therefore not borne out at pull time. |
| GH4 reproduction REPORTED, not OBSERVED; no version range established | VERIFIED as grading | No reproduction run is staged. No version list appears in the issue or PR body fields of the staged captures. |
| GH4 PR review associations CONTRIBUTOR and NONE only; checklist boxes unchecked | PARTIAL | The PR record file stages no review objects and no review-comment bodies (only counts: comments 12, review_comments field present as a count in the record). The review-association claim cannot be re-derived from the staged captures; it may rest on a live read that was not captured as a file. Do not cite it as staged-byte evidence until a reviews capture is staged. The unchecked-checklist claim was not independently re-checked here (PR body text was not re-parsed for checkbox states). |
| GH7: all 10 issues OPEN at pull time; comment counts 0 except NGINX entry (1) and Village entry (4) | VERIFIED | All 10 gh7-*-issue.json captures: state open. Comment counts: 0 for 8 entries, 1 for the NGINX entry, 4 for the Village entry. |
| GH7: 9 of 10 full bodies match staged bodies exactly; registration body differs only by the wallet withholding | VERIFIED | Body-length and equality check staged q06 vs gh4-gh7 captures: 9 of 10 byte-identical. The registration capture body is shorter than the staged body, with the first difference at the wallet-field position and a withholding marker present; no long token remains in the sanitized capture body. |
| GH7: 6 survivors (list proposal, licence question, backport request, Village launch, bounty-work filing, registration filing) | VERIFIED as a set; grade disputed for one member (see X1/X2) | The 6 items exist with the stated shapes and open status. The Village member's grade is disputed (X1). The list-proposal member's act-grade is disputed by the meta-analyst's product-description label (X2). |
| GH7 novelty spot-check: lists/urls zero for survivor terms; reports/ zero except Village in parent sweep docs; Factum fuzzy no true-substring hits | PARTIAL | The lists/ and reports/ greps were not re-run in this lane (they are stated-method checks from the gh4-gh7 lane). The Factum fuzzy caveat (heuristic, not exhaustive) is correctly stated and must travel with the claim. The Village-in-parent-docs exception is consistent with the sweep's own q06b/q06c/q06d captures. |

### UQ-Wayback lane

| Claim | Verdict | Evidence |
|---|---|---|
| Full da.gd pull: 98 rows, 98 unique IDs, saved-30 is a strict subset | VERIFIED | uq-dagd-domain-FULL.json: total_hits 98, saved 98, 98 unique report IDs. All 30 saved-30 IDs from the sweep file appear in the full set. |
| Month distribution: May 53, June 31, May+June 84/98 (85.7%) | VERIFIED | Full-set month counts re-derived: 2025-11: 2, 2025-12: 1, 2026-02: 2, 2026-03: 2, 2026-04: 1, 2026-05: 53, 2026-06: 31, 2026-07: 5, 2026-10: 1. May + June = 84 of 98. |
| June 21 cluster 17 in the full set, same as saved-30; composition 6 distinct codes | VERIFIED | Full-set June 21 rows = 17, all already inside the saved 30. Code counts in the full set match the lane's composition (most frequent code 9 rows, then 3, then 2, then three 1-row codes). |
| May 19 is the largest single day: 19 rows, 19:08–21:48 UTC, 16 distinct codes | VERIFIED | Full-set day ranking: May 19 = 19 (19:08:15Z–21:48:34Z, 16 distinct short codes), June 21 = 17, May 21 = 8. May 19 final domains and title-host shapes match the lane's description (unctad-shaped destinations dominant). |
| Short-code reuse: 70 distinct path tails, 15 repeat, 43 rows covered | VERIFIED | Full-set path tails re-counted: 70 distinct (including the bare root path, 2 rows), 15 repeating tails covering 43 rows, with the stated top counts (9, 4, 4, 3, 3, then 2s). |
| Full-set zz 0/98, oai 0/98; 63/98 rows carry a query string (presence only) | VERIFIED | Full-set flag counts re-derived: has_zz_param 0, has_oai_token 0, query-present 63. |
| zz flagged row resolved: flag comes from the final redirect landing URL's query, not the submitted URL | VERIFIED in mechanism; PARTIAL in provenance | The mechanism is consistent with the cryptologist's saved-byte finding (no flagged string in any saved field) and explains it: the flag data lives in the full final URL, which the saved row does not preserve. The targeted re-fetch itself was transient (nothing raw saved), so this lane cannot re-verify it from a staged capture — it rests on the uq-wayback lane's live read. The fresh re-run total drift (68265 → 68260, 0 flagged in the new top 30) is consistent with a rotated-out snapshot row and is taken as stated. |
| T/Z bounded probe: HN 4/1/7 hits, 0 literal; urlquery agent 20996, harness 20070; untestable, stopped | VERIFIED | tz-bounded-probe.json re-read: HN entries 4, 1, 7 with 0 literal matches each; urlquery totals 20996 and 20070 as stated. No standalone T/Z search was run, as stated. |
| CDX retry: domain query 200 with 50 rows (47×302, 2×404, 1×200), zz/oai 0; zz-filter query 504, no further retry | VERIFIED | cdx-dagd-domain-RETRY.json re-counted: 50 rows, status 302: 47, 404: 2, 200: 1; flag counts 0/0. Month slice matches the lane's (2026-10: 20, 2026-04: 17, remainder small). cdx-dagd-zz-filter-RETRY.json records the 504 with 0 rows. The slice is urlkey-ordered and capped at 50 and must not be cited as a burst distribution, as the lane states. |

### Adversarial lane

| Claim | Verdict | Evidence |
|---|---|---|
| TOI-01 KEEP, low TOI, borderline, with stated kill condition | VERIFIED as a judgment | Underlying counts verify (C11). The kill condition (one failed platform-contact check, or shared authorship behind two of the three) is testable and correctly stated. Disclosure unevenness (explicit form in 2 of 3) matches the adversarial lane's re-derivation and must travel with every TOI-01 citation. |
| GH2 kill STANDS; beacon demoted to DISCUSSED signature | VERIFIED | Single-account fact re-derived (section 3, X1). The demotion follows: a step described only inside a comment by the same account cannot be OBSERVED. |
| GH6 CUT STANDS for TOI; grammar survives as search signature only | VERIFIED as a judgment | Grammar counts verify (C7); all 10 items are tracker text about a feature, not wild acts. Repo spread verifies (7 vendor-tracker, 1 fork, 1 guardrails, 1 gateway with no spawn string). |
| WATCH-01 KEEP AS WATCH; two-account distinction added | VERIFIED | Two distinct User-type accounts re-derived (issue author vs replying account). Promotion condition (automation evidence for the replying side) is correctly stated as unmet. |
| WATCH-02 KEEP AS WATCH; chain check adds zero agency weight | VERIFIED as a judgment | The chain check corroborates the listed project, not the filing act; no staged byte ties authorship verification to the maintainer's check. |
| WATCH-03 KEEP AS WATCH; saved set cannot speak for the full set | VERIFIED, and now strengthened by the full pull | The zero-May saved set is verified. The full pull (uq-wayback lane) now answers the sampling question but raises the day-shape question in X4. |
| G1 headline arithmetic FAIL (20 vs 16); G3 hash denominator; G4 committer qualifier; G10 unscoped superlatives; G11 volume-shape merge | VERIFIED | G1: 17 headings / 19 items re-counted (C1). G3/G4/G10/G11 are report-wording failures that the meta-analyst's corrections (C2-adjacent, C3, C6, C13) independently support. G2, G5–G9, G12–G14 are wording fixes; their underlying facts (cap counts, tango totals, HN summary) verify where re-checked above. |
| "SHIP-WITH-FIXES, narrower than NO-SHIP" | PARTIAL (recommendation, not fact) | The recommendation depends on fixes G1, G3, G4, G10, G11 being applied. This lane adds three more blocking fixes: V-C2 (GitHub totals), V-CM (footer counts), and X1 (Village grade). Ship only after all of them are applied. |

## 2. New verifier findings (not in any lane's FINDINGS file)

### V-C2. GitHub search totals — both the sweep report and the meta-analyst are wrong

Re-derivation from data/lanes/sniffer-sweep-20261031/raw/github/:

- Issue-search files (list shape, search-query naming): q01, q02, q03,
  q04, q05, q06, q07, q08, q09, q12, q13, q14 = 12 files.
- Issue items: 0 + 0 + 4 + 0 + 10 + 10 + 10 + 10 + 10 + 2 + 10 + 10 = 76.
- Code-search files: q10, q11 = 2 files, 5 + 5 = 10 items.
- Staged total across all searches: 86 items.

So: the sweep report's "12 issue searches" count is correct, but its
"86 issue hits" is wrong — 86 is the all-search total (76 issue + 10
code), not the issue-only total. The meta-analyst's C2 ("74 across 11")
is wrong in the other direction: it omits q12 (2 items, issue-search
shape with body/createdAt/number/repository/title/url fields, same
shape as the other search files). Corrected statement to ship: "12
issue searches, 76 issue items; 2 code searches, 10 code items; 86
items staged in total." The "+2 gap" the meta-analyst left open is q12.
No 13th search file and no other gap remains in staged bytes.

### V-CM. Committer footer line counts do not re-derive

Re-derivation from the committer-rerun captures (commit message text):

- Claude lane: exact phrase "Generated with Claude Code" appears 65
  times (65 lines), not 229. Total "Claude Code" mentions are 231
  lines — close to 229 but a different quantity (all mentions, not
  the Generated marker). Co-author footer lines total 32, all naming
  the same assistant family, across 6 commits with any co-author
  footer — not 35 lines across 7 commits. Six is a hard cap: only 6
  commits in the capture contain any co-author footer at all, so a
  7-commit Claude-footer count cannot hold for this capture.
- Devin lane: co-author footer lines total 385 (374 naming the
  vendor assistant, 9 naming a vendor APK variant, 2 naming another
  assistant family), not 404. Commits carrying at least one Devin
  footer: 30/30 — that headline verifies. Lines mentioning the
  vendor assistant outside co-author lines: 73 (context lines, not
  footers).

Fix: ship the author-type counts (which verify exactly) and either
correct the footer line counts to 65 / 32 / 6 (Claude) and 385 / 30
(Devin), or drop the line counts and cite only the per-commit footer
presence (Claude 6/30, Devin 30/30). Do not ship 229 / 35 / 7 / 404.
Possible cause (inference, not established): the lane may have
counted footer lines from a different message field or an earlier
capture version. The coordinator should ask the lane which field it
counted before re-citing any footer line total.

## 3. Contradiction check and resolutions

### X1. Village: gh4-gh7 "OBSERVED multi-agent act" vs adversarial "KILL STANDS"

Staged bytes support the adversarial reading. Re-derived from q06c
(issue) and q06d (4 comments): issue plus all 4 comments come from 1
distinct account, all User type. The second "agent" check-in, the
instruction to post externally, and the publication-plus-fetch-back
update are all comments by that same account. No external-thread
capture, workflow run, or fetch log is staged. Resolution: the filing
of a launch note is OBSERVED (a post exists). A multi-agent act is
REPORTED (claimed inside comments by the same account that staged
both sides). The gh4-gh7 grade must be downgraded to "OBSERVED filing
act; multi-agent coordination REPORTED, single-account, killed as a
multi-agent claim." The cryptologist's "beacon shape" survives only
in the adversarial lane's demoted form: a DISCUSSED protocol
description usable as a hunt signature, not a finding about this
instance. The gh4-gh7 lane's "6 survivors" count is unaffected as a
set count, but its Village row grade must change before ship.

### X2. GH7 counts: meta-analyst (3 candidates) vs cryptologist / gh4-gh7 (6 non-trap / 6 survivors)

Not a count contradiction once grouping is unpacked — it is a grading
disagreement about two members. All three lanes partition the same 10
items: 4 cut (2 honeypot trap + 2 unticked-template false positives)
and 6 non-trap. The meta-analyst's "3 candidates" are the strongest
subset of the 6 (licence filing, backport message, bounty disclosure).
The remaining 3 non-trap members are graded differently: the
directory-listing addition proposal (gh4-gh7: OBSERVED filing act;
meta-analyst: product-description item), the Village launch note
(gh4-gh7: survivor; meta-analyst/adversarial: duplicate of GH2, never
double-count), and the registration filing (all lanes: filing act,
substance unconfirmed). Resolution: ship the 4-cut / 6-non-trap
partition with per-member grades, and never cite "3" and "6"
interchangeably. For the listing proposal: the act-grade follows
gh4-gh7 (a filing was made — the body is a filed addition request
with a proposed row, not a bare product blurb), while the
substance-grade follows the meta-analyst (the app claims inside it
are REPORTED and unconfirmed). For the Village note: cite it only
under GH2, never as a second GH7 instance.

### X3. zz flagged row: cryptologist (flag real, unverifiable from saved bytes) vs uq-wayback (redirect artifact)

Compatible, and the uq-wayback lane resolves the cryptologist's open
question. The cryptologist proved the flag cannot be verified from
saved fields (no flagged string in any saved field). The uq-wayback
lane's transient re-fetch explains why: the flagged parameter lives
in the final redirect landing URL's query, which the saved row does
not preserve, while the submitted URL has no query string. Resolution:
file-level count 1 stands as a sweep-time snapshot; it is a
redirect-landing tracking-parameter artifact, not a submitted zz
marker and not agent evidence. Neither lane's claim needs correction;
the coordinator's report should carry the combined sentence, not
either half alone.

### X4. June 21 vs May 19: adversarial full-pull condition vs uq-wayback full pull

The adversarial lane's section 6 required, among other conditions,
that June 21 remain a standout day in the full set. The full pull
fails that condition on day-count: May 19 (19 rows) exceeds June 21
(17 rows). It also fails the shape-carry-over condition as a single
pattern: May's rows are dominated by a different destination shape
(unctad-shaped destinations) than June 21's echo-host shapes, and
May holds several other multi-row days (May 21: 8, May 26: 6,
May 27: 5, May 12: 5). Resolution: the volume claim ("May–June 84 of
98") verifies, but the single-pattern claim ("one May–June burst")
does not. Ship WATCH-03 as two distinct day spikes inside a May–June
volume elevation — a June 21 echo-test cluster (17 rows, 6 codes,
decoded framing-probe shapes) and a May 19 spike (19 rows, 16 codes,
different destination shape) — with agency unproved for both and
single-source status unchanged (CDX adds no burst distribution).
The adversarial lane's remaining full-pull conditions (code-reuse
rate in the full set: verified at 15 repeating tails / 43 rows;
full payloads: decoded by the cryptologist lane; marker zero: 0/98
for zz and oai) are now met, so the watch item's sampling caveat can
be retired while its pattern caveat must be restated as above.

### X5. Meta-analyst C2 vs sweep report vs staged bytes

Resolved in V-C2 above. Neither prior statement ships. The staged
bytes support: 12 issue searches, 76 issue items, 2 code searches,
10 code items, 86 total.

### X6. Committer scope: meta-analyst C3 (Copilot slice, no lane-wide claim) vs rerun combined 5/90

No contradiction. The rerun extends the completed-lane picture from
30 to 90 commits and from 0 to 5 bot-type authors, all from one
account. The "no lane-wide negative" qualifier still holds: Codex
and both PR lanes remain unmeasured (0 rows, not 0 bot-type), and
the 20-phrase pass remains unrun. Any combined "5/90" citation must
carry "completed lanes only (Copilot + Claude-footer + Devin);
Codex, PR, and phrase lanes unmeasured."

## 4. Hash-check table (meta tree only)

Method: sha256 recomputation over every .sha256 sidecar under
data/lanes/sniffer-meta-20261031/raw/. No SHA256SUMS file exists
anywhere in the meta tree (0 found). Sidecar target resolution uses
the sidecar's stated target basename in the same lane dir.

| Lane dir | Sidecars | Pass | Fail | Uncovered files (no sidecar) |
|---|---|---|---|---|
| meta-analyst | 0 | 0 | 0 | FINDINGS.md, STATE.md — NO sidecar coverage |
| cryptologist | 0 | 0 | 0 | FINDINGS.md, STATE.md — NO sidecar coverage |
| adversarial | 0 | 0 | 0 | ADVERSARIAL.md, STATE.md — NO sidecar coverage |
| committer-rerun | 5 | 5 | 0 | run-rerun.sh, run.log, STOPPED.txt, STATE.md, FINDINGS.md, gh-commits-codex.json (0-byte failed capture, no sidecar), plus 3 .PROVENANCE.txt notes (provenance notes are not hashed by design) |
| gh4-gh7 | 25 | 25 | 0 | FINDINGS.md.PROVENANCE.txt, STATE.md.PROVENANCE.txt, dir-level .PROVENANCE.txt, and 22 capture .PROVENANCE.txt notes (provenance notes are not hashed by design). Every data capture and both report files carry a passing sidecar. |
| uq-wayback | 7 | 7 | 0 | Dir-level .PROVENANCE.txt only. Every data file, script, and both report files carry a passing sidecar. |
| followups (still running — coverage snapshot only, not verified) | 26 | 26 | 0 | 26 .PROVENANCE.txt notes (not hashed by design); no FINDINGS.md/STATE.md staged yet at check time. |
| TOTAL (six completed lanes) | 37 | 37 | 0 | — |
| TOTAL (including follow-ups snapshot) | 63 | 63 | 0 | — |

Result: 0 hash failures in the meta tree. The three lanes with NO
sidecar coverage (meta-analyst, cryptologist, adversarial) are the
three lanes that staged no fetched captures — their STATE files say
so explicitly, and their outputs are prose re-derivations from the
sweep's own hashed captures. That is a coherent reason, not a gap in
capture integrity, but the coordinator's report must not describe
the meta tree as "fully hash-covered": prose-only lanes are
uncovered by construction. The one true coverage gap in a capture
lane is the committer-rerun 0-byte Codex capture, which has a
provenance note but no .sha256 sidecar (its error files do carry
sidecars).

## 5. Factum / Transluce re-checks (read-only)

- Transluce: re-parsed from the staged snapshot files (not a live
  Transluce call). Full list (140 findings): da.gd 2 findings / 5
  occurrences; pursekeeper 1 / 1; ilands 36 occurrences in 1 finding;
  handoff 0; village 0; beno 0; tango 0. Slice (25 items): da.gd 0.
  These match the meta-analyst's C9/N-table exactly.
- Factum pursekeeper token presence: VERIFIED without a live match
  query, by grepping exported batches under data/records/ (read-only,
  no lock encountered on that path). Both record IDs cited by the
  meta-analyst resolve to exported records whose text contains the
  token, with lane tags matching the citation (one August-2026 lane,
  one Transluce-intel lane). A Factum status call run after the
  main verification completed and confirmed the meta-analyst's
  stated DB state exactly: initialized, state commit matching the
  cited commit, 1 pending batch, no lock block observed. The
  exact-mode not_found legs and the da.gd "found" direction were
  not re-run as match queries in this lane and remain taken as
  stated from the meta-analyst's read-only checks.
- No Factum writes were made. No Transluce submissions were made.

## 6. Value-leak scan (meta tree only, shapes only, no values reproduced)

Method: pattern scan over the six completed lanes' files plus the
follow-ups snapshot, counting shapes only. Generic 32–44-char
alphanumeric shapes are noisy (report IDs, base64 fragments, commit
hashes) and are NOT treated as wallet evidence on their own.

| Shape | Where found | Assessment |
|---|---|---|
| 0x + 40 hex (wallet-address shape) | Nowhere in the meta tree (0 matches in all six lanes) | Clean. |
| 40–45-char alphanumeric token | Meta-analyst prose: 1 match, which is a public repo commit hash cited as Factum state, not a secret. Committer captures: commit SHA strings (expected GitHub API data). GH7 captures: two 40-char commit hashes in the backport body (expected) and zero long tokens in the sanitized registration capture. | No credential-like value. The registration sanitization verifies: no long token remains in that capture body. |
| Email-shaped string | Committer FINDINGS prose: 2 matches, both bot-account noreply footer forms (self-declared assistant addresses, not human contact values). Committer captures: author-email strings inside GitHub API commit records (expected API data, including human-authored commit emails — these live in raw captures only, not in prose). GH7 captures: 2 email-shaped strings in API records. | Prose is clean of human contact values. Raw captures contain API-returned emails by construction; the coordinator should keep captures out of any outward-facing artifact, as with all raw API captures. |
| Key/token/secret assignment (key: value shape) | Meta-analyst prose: 1 match, a false positive — ordinary prose ("token:" introducing a sentence about the token itself), not an assignment of a value. | Clean. |
| Query-string value (zz= + value) | UQ-wayback FINDINGS prose: 6 matches, all query-term mentions (the search term itself and a CDX filter pattern), never a captured query value. UQ data files carry flags and paths with queries dropped, per that lane's sanitization. | Clean. No query value is reproduced in any meta FINDINGS file. |
| Phone-number shape | 0 matches in all six lanes. | Clean. |
| Human handle (github.com/user path or @mention in prose) | 0 in meta-analyst, cryptologist, gh4-gh7, uq-wayback, adversarial prose. Committer FINDINGS prose: 2 @-forms, both bot-account noreply address forms (see email row), not human handles. | Clean of human handles in prose. Raw API captures necessarily contain account login strings; those are capture data, not prose attribution, and are not reproduced here. |
| Wallet value in prose | 0 in all six FINDINGS files. The gh4-gh7 lane's withholding marker is present in the registration capture; no wallet-shaped value appears in any meta FINDINGS file. | Clean. |

Known-presence note: the sweep's raw tree (outside this scan's scope)
already carries its own presence note per the task brief; this scan
covers the META tree only and finds no new credential-like, wallet,
query-string, or human-contact value in any meta FINDINGS file. The
only values that need handling are the API-returned emails and login
strings inside raw captures, which are ordinary GitHub API capture
content and must stay out of outward-facing artifacts.

## 7. Failures, gaps, and open questions for the coordinator

1. BLOCKING — V-C2: ship "12 issue searches, 76 issue items, 2 code
   searches, 10 code items, 86 total." Neither "86 issue hits" nor
   "74 across 11" may ship.
2. BLOCKING — V-CM: correct or drop the committer footer line counts
   (Claude 65 / 32 / 6; Devin 385 / 30). Ask the committer lane which
   field it counted; do not re-cite 229 / 35 / 7 / 404.
3. BLOCKING — X1: downgrade the gh4-gh7 Village row grade to
   "OBSERVED filing act; multi-agent coordination REPORTED,
   single-account, killed as a multi-agent claim" and carry the
   DISCUSSED-signature wording for the fetch-back description.
4. BLOCKING — X4: restate WATCH-03 as two day spikes (June 21 echo
   cluster + May 19 spike) inside a May–June volume elevation, not
   one burst pattern. Retire the sampling caveat; keep the
   agency-unproved and single-source caveats.
5. BLOCKING — X2 wording: ship the GH7 partition as 4 cut / 6
   non-trap with per-member grades; never cite "3" and "6"
   interchangeably; cite the Village note only under GH2.
6. NON-BLOCKING — GH4 PR review associations (CONTRIBUTOR/NONE) are
   unstaged: either stage a reviews capture or soften to "no
   maintainer-identified review found in staged captures."
7. NON-BLOCKING — Committer 0-byte Codex capture has no .sha256
   sidecar. Add one (hash of the empty file) or note the gap in
   the manifest so the tree is not described as fully covered.
8. NON-BLOCKING — Factum match legs (exact not_found for handoff
   and pursekeeper; da.gd found direction) were taken as stated
   from the meta-analyst, not re-run through the match tool here.
   The pursekeeper token presence itself IS verified via exported
   batches (section 5).
9. OPEN — Follow-ups lane still running at check time: its claims
   (including any pursekeeper live-surface update) are NOT verified
   by this lane and must be verified separately before ship if the
   coordinator's report cites them.
10. OPEN — Codex commit lane, both PR lanes, and the 20-phrase pass
    remain unmeasured (rate guard). No zero may be cited for them.
11. OPEN — The GH6 gateway-envelope instance (linguist seed rows)
    and the linguist phrase-list splits (C10) were not re-parsed
    here; cite them as lane-stated, not verifier-confirmed.
12. OPEN — Live re-checks the lanes left open (GH4 PR #42203 merge
    status after 2026-10-31; GH7 survivor comment/closure status;
    Village external-thread capture; zz flagged-row full URL) were
    not run by this lane, per the passive-reads brief and the rate
    guard posture. Each needs its own later window if cited.

## Evidence paths

- This lane: data/lanes/sniffer-meta-20261031/raw/verifier/VERIFIER.md,
  STATE.md.
- Meta lanes verified: data/lanes/sniffer-meta-20261031/raw/
  meta-analyst/FINDINGS.md, cryptologist/FINDINGS.md,
  committer-rerun/FINDINGS.md (+ captures), gh4-gh7/FINDINGS.md
  (+ captures), uq-wayback/FINDINGS.md (+ captures),
  adversarial/ADVERSARIAL.md.
- Sweep staged bytes re-derived: data/lanes/sniffer-sweep-20261031/
  raw/github/q05-collab-spawn.json, q06-i-am-ai-agent.json,
  q06c-village-issue1-full.json, q06d-village-issue1-comments.json,
  q09e-tron-issue1-full.json, q09f-tron-issue1-comments.json,
  q12-every-step-tool-call.json, urlquery-wayback/
  uq-odd-dagd-domain.json, uq-odd-zz-param-agent-conj.json,
  hn-forum/_summary.json, hn_oct-hiring_candidates.json,
  tango-zulu/counts-summary.json.
- Transluce snapshots re-parsed: data/lanes/2026-10-09-transluce-intel/
  raw/findings-list.json (140 items),
  findings-list_25_183-210_20261031T115745Z.json (25 items).
- Factum exported batches checked (read-only grep, no writes):
  data/records/db0b983e1bb64c8daa74205ded247fca/ (August-2026 lane
  record) and data/records/14872dbd1f1444c1a92e4c77ef025a2e/
  (Transluce-intel lane record) — the two batches containing the
  cited pursekeeper records.
