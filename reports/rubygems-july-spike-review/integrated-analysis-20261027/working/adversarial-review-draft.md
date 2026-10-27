# ADVERSARIAL REVIEW (draft) — integrated analysis, July 2026 RubyGems spike set

Reviewer role only. No push. No Factum write. No other worker file touched.
Read-only recomputation from the operator CSV and the census JSONs.
No payload executed. No credential-shaped value and no full canary token
is reproduced here; canaries and hosts are described by shape and count only.

Path note: the brief's `../REPORT.md` and
`../live-check-reconciled-20261027/RECONCILIATION.md` do not exist at those
paths. The files actually read were
`reports/rubygems-july-spike-review/REPORT.md` and
`reports/rubygems-july-spike-review/live-check-reconciled-20261027/RECONCILIATION.md`.
The integrator should fix the brief's paths so the next reviewer does not
treat the prior review as missing.

## VERDICT: NO-SHIP

The draft must not ship as an integrated report until the fix list below
is applied and re-verified. The blocks are not typos. One recommended gap
is false (fix 14), one verdict-level claim is overstated in both
directions (fixes 3–4), one headline count is a residual dressed as a
positive count while the number it corrects is still unreproduced
(fix 8), and the consolidated verdict states a disproof the evidence
does not support (fix 1). Everything else in the "survived" section
held under attack and may ship once the fixes land.

## What survived attack (say so plainly)

- Prior verdicts (a)–(e) in verdict-survivor.md STAND: dashboard export
  not our observation; July-7 NO CHANGE; GemStuffer/JFrog NO CHANGE
  (file silent); Andrey78 batch = shape only; agent activity UNPROVEN.
- Combinatorial grammar 310 (129 / 113 / 68), university template 309
  with 116 X values and one off-template row, placeholder summaries 86
  (54 / 19 / 9 / 4), epoch-suffixed names 34, `ssrf-*` prefix 23,
  strict `apex-black-test-NNN` 14 cross-author / 11 under `tester`.
  All recomputed from the CSV and confirmed.
- Cryptologist union 82 scan-set rows / 84 including the author field,
  with set sizes summing to 86 minus exactly the 4-row OAST∩XSS overlap.
  OAST 29 rows, webhook 19 rows, no overlap, combined out-of-band 48.
  OAST host correction stands: 6 distinct full hosts, 4 base domains,
  one host carrying 22 of 29 rows.
- Shell taxonomy itself: page 200 proves nothing; API is the authority
  for index membership; Diffend content (full / stub) is not live status;
  code recovery needs a gem file, tag/commit, or matching tree. The
  klondikemarlen repo-mirror analysis and the OAST-listener analysis
  are correctly fenced.
- Callback question correctly graded UNRESOLVED in open-questions (c)
  and shell §4: a live listener is not a receipt, and absence of a
  public receipt is not proof no callback arrived.
- jrjackson dominance note (10,508,353 of 11,138,862 total downloads,
  94.3%) and the blank-field caution (21 of 23 live rows are blank-field
  rows, out of 49 blank rows) both recompute exactly. Blank means
  neither safe nor gone.

## Fix list

Each fix: claim, flaw, required change.

### 1. Consolidated verdict states agent activity as disproven

- Claim: verdict-survivor §4, "what it is not is agent activity."
- Flaw: this contradicts the same lane's verdict (e), "agent activity
  UNPROVEN." No datum in the CSV or the census distinguishes a human
  publisher from an agent publisher. An agent could have published
  probe-shaped metadata; the file simply holds no model, harness,
  prompt, tool-call, or session artifact either way. Absence of actor
  evidence is not evidence of a non-agent actor.
- Required change: replace every "is not agent activity" sentence with
  "is not established as agent activity on this evidence." Apply the
  same downgrade to "July-7 probe/test cluster" as a bare fact: write
  "July-7 probe-shaped cluster" and grade probe intent as INFERENCE
  from self-description, not as an observed event.

### 2. "Abandoned listing residue" / "abandoned test residue" is an upgrade

- Claim: verdict-survivor §3, probe survivors are "abandoned listing
  residue, not ongoing activity"; test survivors are "abandoned test
  residue, most likely."
- Flaw: observed bytes are only: single live version each for the 3
  probes, no live source repo, Diffend stub, downloads 515 / 550 /
  1,282, and no post-July version visible. None of that observes
  abandonment, an actor stopping, or a July testing event having
  occurred. A single-version gem with no new release is also consistent
  with a finished test fixture, a forgotten listing, or a project that
  simply has not released. The lane admits this ("residue stays
  INFERENCE") and then lands on it as the section conclusion anyway.
- Required change: demote both headings to "listing residue (INFERENCE,
  unproven against still-referenced fixture)." State the discriminator
  that would settle it (post-July version, download-by-date, dependents,
  callback receipt) and leave the call open until one arrives.

### 3. testgem-mini: wrong rank, and the landing points the wrong way

- Claim: verdict-survivor §2 note, "34,151 downloads is the second-
  highest test-class count"; §3, testgem-mini is test residue with an
  unexplained count.
- Flaw: two errors. First, rank: recomputed first-census downloads
  rank testgem-mini 4th of all 23 live gems (after jrjackson, eco-helpers,
  ecoportal-api-graphql) and HIGHEST of the 2 test gems, not second-
  highest in any grouping. Second, logic: a 5-version, Diffend-full gem
  with 34,151 downloads is the survivor that least fits "residue."
  The lane lists dependency, mirror, CI reuse, and shared-fixture
  explanations, then still lands on residue without checking any of
  them. The count is evidence AGAINST pure residue, or at minimum
  evidence that residue is not the best fit on current data.
- Required change: correct the rank. Reclassify testgem-mini as
  "test-named, use UNEXPLAINED" and require a dependents check plus
  download-by-version before any residue/legit call. Do not use the
  count to promote it to legit either; the point is the count blocks
  the residue landing, it does not decide the other side.

### 4. "Continued maintenance" for the 18 legit gems is false as a blanket

- Claim: verdict-survivor §3 heading, "continued availability, and for
  most, continued maintenance"; §4, legit survivors "survive because
  they are real projects with post-July versions."
- Flaw: no version publish date exists in any live JSON for any
  non-shirobai survivor (the lane admits this), so "maintenance" for
  14 of 18 rests on version-number increase alone. Recomputed against
  the first-census latest field: live latest exceeds CSV latest for
  13 legit gems, is BELOW CSV latest for 3 (edoxen, intranet-pictures,
  sportdb-parser), is EQUAL for 1 (minitest-hashdiff, single version
  0.1.1, unchanged), and is ambiguous for 1 (jrjackson: latest field
  0.3.8 below CSV 0.5.2, while its versions list reaches 0.5.5). Only
  the 4 shirobai gems carry dated version strings (2026.1027.0730,
  census day). A version number without a date does not prove a
  post-July release: the CSV latest is a July-window value, and
  version ordering across branches is not a calendar.
- Required change: split the class in the text. "Dated post-July
  activity: shirobai family only (4). Version-number increase, dates
  unobserved: 13. No post-July version visible or downward: 5
  (name them)." Fetch version publish dates for the 23 live gems
  (the RubyGems versions endpoint returns them; the censuses dropped
  them) before any maintenance sentence ships. Until then, the only
  earned blanket claim is "continued availability."

### 5. "CSV latest matches live latest on only 3 of 23" is wrong; it is 4

- Claim: verdict-survivor census section.
- Flaw: recomputed against the first-census `rubygems_latest` field,
  matches are 4: apex-black-test-011, apex-oidc-probe, minitest-hashdiff,
  AND test_gem_kangaroo (0.0.14 = 0.0.14). The lane missed the fourth.
  Worse, the reconciled JSON alone cannot support the claim at all:
  its `rubygems_latest_version` is null for minitest-hashdiff,
  pico_phone, query-stream, rosett-ai, rubocop-metz, shirobai family,
  sportdb-parser, and others. A claim sourced to "the three live JSONs"
  without naming which field came from which file is unverifiable.
- Required change: correct to 4 of 23, cite the first-census field by
  name, and state that the reconciled JSON's latest field is
  incomplete and was not used for this count.

### 6. Version-loss discussion names 2 cases; the census lists show more

- Claim: verdict-survivor census section, "two differ downward ...
  apex-blk-test-final ... edoxen."
- Flaw: incomplete. CSV latest is absent from the first-census versions
  list for at least 8 live gems: apex-blk-test-final (0.0.5),
  edoxen (2.1.3, no 2.x in the live list), intranet-pictures
  (3.0.0.rc2; only rc1 is live), sportdb-parser (0.9.0),
  testgem-mini (0.4.6), talk_to_your_app (0.1.0.pre.4; pre.7 and pre.3
  are live, pre.4 is not), eco-helpers (3.2.18; 3.2.23 and 3.2.14 are
  live), ecoportal-api-graphql (1.3.13), query-stream (1.3.0).
  Separately, jrjackson's two API fields contradict each other
  (latest field 0.3.8 vs versions-list maximum 0.5.5) and the lane
  never resolves which field is authoritative.
- Required change: publish the full absent-from-list table with the
  caveat that "absent from the census versions list" is observed while
  "yanked" is inference pending a list-completeness check (platform-
  duplicate rows, as in pico_phone's 55-entry list, show the lists are
  not plain distinct-version lists). Resolve the jrjackson field
  conflict explicitly instead of quoting either value bare.

### 7. The survivor "multi-factor rule" collapses to summary judgement

- Claim: verdict-survivor §2, classification by "name + CSV summary +
  live version count + live downloads + live source status."
- Flaw: the non-summary factors do not discriminate the close calls.
  minitest-hashdiff is legit despite the probe profile (1 version,
  Diffend stub, no source) — the same profile as all 3 probes.
  jrjackson is legit despite Diffend stub and no source. talk_to_your_app
  is legit despite a dead (404) repo. Conversely testgem-mini beats
  minitest-hashdiff on every non-summary factor (5 versions vs 1,
  Diffend full vs stub, 34,151 downloads vs 2,395) yet is classified
  the other way. The rule as stated therefore overstates its own
  robustness; in practice the classifier is name-and-summary wording.
- Required change: either state honestly that classification is
  single-criterion (name + summary self-description) with version /
  download / source data as context only, or mark minitest-hashdiff
  and testgem-mini as UNCERTAIN close calls. Do not present a
  five-factor rule whose factors point the wrong way on the close calls.

### 8. Linguist 117 is a residual, not a positive count; prior 105 is still unreproduced

- Claim: linguist §1/§4, family B descriptive summaries = 117, correcting
  the prior review's 105.
- Flaw: 117 is arithmetic, not observation: 203 (family B) minus 86
  (placeholders). Family B is itself defined as the remainder after
  removing the 310 combinatorial rows and the 20 manually-judged
  ordinary rows. So 117 inherits every judgement in the C = 20 call;
  it is not an independent count of rows whose summaries positively
  signal a probe. Meanwhile 105 is reproduced by NO rule tested — by
  this reviewer or by the linguist. Tested and rejected: scored
  descriptive in family B = 97; Haiku registry-category non-placeholder
  = 97; 117 minus markup-only summaries = 107; minus markup + SSTI =
  103; minus markup + SSTI + pipe row = 102. The prior review's own
  partition does not sum either: 309 university + 86 placeholder + 105
  probe-descriptive = 500, leaving 33 rows unaccounted (the 138-row
  remainder minus 105 = 33, i.e. the 20 ordinary + 1 off-template
  combinatorial + the 12-row gap).
- Required change: do not quote either 117 or 105 as "probe-descriptive
  summaries" in the integrated report. Quote the earned form:
  "203 family-B rows, of which 86 carry placeholder summaries and 117
  carry non-placeholder summaries (family B by remainder definition;
  probe-ness of the 117 rests on name + summary judgement, not on a
  positive-signal count)." If the integrator wants a positive-signal
  count, it must publish the signal list and the per-row rule that
  yields it, and must explain the prior review's 33-row hole or
  retract 105.

### 9. Linguist family method is underspecified for replication

- Claim: linguist §5, "Ordinary test: name not combinatorial AND summary
  is descriptive library prose with no test/probe/attack word from the
  section 2b signal list. Probe test: the remainder."
- Flaw: "descriptive library prose" is a judgement, not a rule, and the
  section 2b list as printed does not by itself separate the 40
  blank-field descriptive non-combinatorial rows into the 20 ordinary
  and the 20 probe-shaped rows without the reviewer's manual call
  (e.g. deciding that a Rails-agent-stack summary is ordinary prose
  while a cross-tenant-test summary is not). A replicator following
  only the printed method cannot reproduce 310 / 203 / 20 exactly.
- Required change: publish the ordinary set's membership rule in full
  (exact signal list, including whether generic words like "test"
  count, and how multi-sentence prose was judged) or downgrade the
  family sizes from OBSERVED to OBSERVED-shape-plus-judgement. The
  date corroboration helps (family C spread July 6–12 with exactly 1
  July-7 row, jrjackson; family B entirely July 7) but does not replace
  the rule.

### 10. Apex correction stands; the prior 114 matches no rule

- Claim: prior review, "114 apex names"; linguist, 115.
- Flaw (in the prior review, confirmed): recomputed substring `apex`
  in name = 115, all inside family B, none in families A or C.
  Prefix rules also fail to give 114: dash-only prefix = 80,
  dash-or-underscore prefix = 112, `tester`-only apex-prefix = 95
  (68 dash-form `apex-black-*` + 27 underscore-form). The linguist's
  recommendation to quote "95 apex-prefixed (68 `apex-black-*`)"
  for `tester` is the earned form.
- Required change: correct 114 to 115 in any integrated text and never
  quote 114 again. This fix is already correctly made in the linguist
  lane; it must survive integration, not be reverted to the prior
  figure.

### 11. YAML and tar counts collide across lanes and must not be quoted bare

- Claim: linguist §2b, YAML signal 4, tar wording 3; cryptologist §1,
  YAML anchor/alias/tag 0, tar traversal 0.
- Flaw: both lanes are right under different definitions, which is
  exactly the trap. The linguist's YAML 4 counts name-word `yaml`
  plus summary shapes, including 2 rows whose summaries are only a
  placeholder or a template string (name alone carries the signal).
  The cryptologist's 0 counts document markers (`!!`, anchors, aliases)
  in metadata fields that are not YAML documents. Same for tar: wording
  ("tar traversal" in a name/summary) vs traversal strings (`../`,
  encoded, backslash), which are 0. An integrated sentence like "4 YAML
  payloads, 3 tar payloads" would be false under the cryptologist's
  (payload-string) definition and misleading under either.
- Required change: ban bare "YAML 4" and "tar 3" from integrated text.
  Write "YAML-word signal in name/summary: 4 rows; YAML document shape:
  0 rows" and "tar wording: 3 rows; tar-traversal string: 0 rows,"
  wherever either number appears.

### 12. Prior review's SSRF field attribution and webhook count are wrong

- Claim: REPORT §3, "SSRF / internal targets: 24 homepage rows" and
  "Webhook.site: 19 rows by substring (18 by homepage host)."
- Flaw: recomputed link-field cells: SSRF/internal homepage cell hits
  = 23, source cell hits = 1 on a row already counted via its homepage,
  so link-field rows = 23, not 24. The 24th row is a summary-text URL
  row (a localhost URL carried in summary text, not in a link field).
  The cryptologist's correction on this point stands. Webhook: homepage
  cells = 19, source cells = 0, so "18 by homepage host" is off by one;
  the cryptologist's 19 homepage cells is correct.
- Required change: adopt the cryptologist's split everywhere: "SSRF /
  internal-target rows 24 = 23 link-field rows + 1 summary-text row;
  of the 24, 10 are public-IP homepages, not internal targets"
  (see fix 13's companion split). Correct the webhook parenthetical
  to 19 homepage cells.

### 13. Public-IP rows must never be quoted as "internal targets"

- Claim (at risk in any summary of the cryptologist lane): 24-row
  SSRF/internal set.
- Flaw: 10 of the 24 are public-IP homepages swept in by the prior
  review's IP rule. A public IP-literal homepage proves only that
  someone put an IP-literal homepage on a gem; it is not an internal
  target, not a metadata address, and not evidence of a server-side
  fetch. The same applies to the plain-http count (12 rows): scheme
  alone proves nothing about target or payload.
- Required change: always quote the split — internal shapes (link-local
  metadata, loopback, RFC1918, provider-internal hostnames) vs
  public-IP homepages (10) vs summary-text row (1) — and never shorten
  the set to "24 internal targets."

### 14. Open-questions "66 unchecked tombstoned source URIs" is false — delete the gap

- Claim: open-questions §1 base numbers and §2 gap table, "among
  tombstoned gems, 66 rows have a source URI that the census did not
  check"; close condition "HEAD or GET per URI for the 65 checkable
  URIs"; ranked gap #2.
- Flaw: recomputed from the reconciled files, the 66 rows labelled
  `source_status = unchecked` in the tombstone-pairs file consist of
  65 rows with NO source URI in the CSV at all (their reconciled note
  reads "no source_code_uri in CSV") plus exactly 1 row with a URI
  deliberately not fetched (the internal metadata-address URI).
  The label means "nothing to check / excluded by design," not
  "URI present but unexamined." The first census in fact checked all
  196 tombstoned source URIs (192 × 404, 3 × 200, 1 × unreachable).
  The gap as written double-counts 65 source-absent rows already
  covered by the 327-no-source-URI gap, prescribes fetching 65
  non-existent URIs, and ranks a phantom gap #2, ahead of real gaps.
- Required change: delete gap #2 entirely. Replace it with the true
  statement: "tombstoned source URIs checked: 196 of 196 present
  (192 dead, 3 live: 1 repo mirror + 2 OAST listeners); 1 URI
  deliberately excluded (internal metadata address); 65 further rows
  in the 'unchecked' label set have no URI and belong to the
  source-absence gap, not to this gap." Re-rank the remaining gaps
  without it.

### 15. The "split" recommendation for the 330 new names is unsafe as written

- Claim: open-questions §1(a), admit the 310 combinatorial rows now as
  a shape-only lane; hold the 20 small-author names out as
  dashboard-only pointers.
- Flaw: three problems. (a) Laundering: the admitted 310 are 100%
  API-404 (129/129, 113/113, 68/68 gone), and all 191 of their present
  source URIs are exactly the mechanical `github.com/<author>/<name>`
  pattern — consistent with dashboard-generated links, not observed
  repos — while the first census found tombstoned GitHub sources dead.
  Ingesting those URIs as record fields would launder pattern-derived
  strings into corpus evidence. (b) Inversion: the held-out 20 contain
  18 of the 23 live gems — the only verifiable live projects in the
  set — while the admitted set contains zero live gems. A corpus rule
  that admits dead shapes and holds out live projects needs a better
  justification than "they do not share the shape." (c) Grade travel:
  nothing in the recommendation guarantees the shape-only grade
  survives downstream citation; a later reader citing "corpus lane:
  July mass generation, 310 rows" without the grade has already
  upgraded shape to campaign.
- Required change: admit names + grammar + timing + first-publish
  dates ONLY, with source_uri and homepage-profile fields either
  stripped or stored flagged as "pattern-derived, unverified, repo
  dead on census." Admit the 20 as ordinary-gem records on their own
  terms (or state explicitly that the corpus criterion is shape-only
  and the 20 are excluded for that reason, not because they are
  unverified — they are the most verified rows in the set). Every
  lane record must carry the grade string "shape-only, not agent
  activity, not severity" in the record itself, not in a covering note.

### 16. The pkg-review-2 re-run recommendation is not cost-justified as an unconditional

- Claim: open-questions §1(b), re-run all 464 pkg-review-1 rows under
  pkg-review-2 before any severity reuse.
- Flaw: (a) Version 2 is unproven, not a gold standard: n = 20, with
  empty score bands (46–61, 73–87) and matched-shape flips as large as
  version 1's (combinatorial-only: high on 111 v1 rows, medium on all
  5 v2 rows). Re-running 464 rows under v2 may replace one unstable
  distribution with another. (b) It fixes calibration only: the lane
  admits it does not fix the missing code or missing receipts, so
  post-re-run severity is still metadata severity. (c) No consumer is
  named: the integrated verdicts award NO severity verdict, and most
  rows are tombstoned, so the re-run gates no live decision.
  (d) Scope error: if the goal is fixing the severity denominator,
  the scope is 464 + 49 = 513, not 464 — the 49 unscored rows are
  omitted from the re-run recommendation while being cited as the
  denominator problem.
- Required change: make the re-run CONDITIONAL: run it only when a
  concrete severity-reuse decision is pending, with scope 513,
  all three label sets preserved (dashboard, v1, v2 — never overwrite),
  and a matched-shape consistency check on v2 before any v2 label is
  quoted. Otherwise freeze v1 as UPSTREAM with the calibration warning
  attached and spend the effort on fix 4's date fetch instead.

### 17. "Further public searching will not close this" overclaims

- Claim: open-questions §1(c), cost of a public-data answer is low
  "and the answer is already known: no receipt is in public reach.
  Further public searching will not close this."
- Flaw: no exhaustive public search is evidenced in the lane; the
  correct statement is bounded to sources checked. The same lane
  correctly grades the question UNRESOLVED elsewhere — this sentence
  upgrades "not found in checked sources" toward "not findable,"
  which is evidence-of-absence language of exactly the kind fix 1
  targets.
- Required change: "No receipt was found in the public sources
  checked; receipts sit in private OAST/webhook inboxes held by
  others, and probing the endpoints would pollute the very logs
  that could settle it." Keep the do-not-probe restraint, which is
  correct and must survive.

### 18. Open-questions understates the census on the batch

- Claim: open-questions §1(a), "the census confirms the batch window
  is closed for sampled names: registry 404, Diffend stub only."
- Flaw: the census covered all 533 names, not a sample. The earned
  statement is stronger and already available: all 310 combinatorial
  rows are API-404 (129/129, 113/113, 68/68) and all 100 `tester` rows
  are API-404. "Sampled" understates the census and invites a reader
  to think the batch finding rests on sampling.
- Required change: replace "sampled names" with the full-census figures
  above wherever the batch's gone status is cited.

### 19. Artifact-count denominators must be named every time

- Claim (at risk across lanes): "48 artifacts."
- Flaw: 48 is the UNIQUE count (23 RubyGems pages + 18 Diffend pages
  + 7 unique live repo URLs). Per-gem entries on the reconciled
  `artifact_urls` field are 49 for live gems alone and 50 across all
  rows (the extra entry is the gone klondikemarlen gem sharing the
  marlens repo URL). The reconciled `artifact_urls_uniform` field
  gives yet another pair (51 entries / 49 unique, via the edoxen old
  URL). Verdict-survivor's single sentence mixes the live-only 49
  with the all-rows 50 without labelling which denominator applies
  where. Separately, the other "48" in the draft (48 out-of-band rows
  = 29 OAST + 19 webhook) is a different set that happens to share the
  number; open-questions correctly warns against conflating them, and
  that warning must travel with both numbers.
- Required change: every artifact sentence cites field + denominator,
  e.g. "48 unique artifact URLs (reconciled `artifact_urls` field:
  49 per-gem entries for live gems, 50 across all rows)." Never print
  "48" for artifacts and "48" for out-of-band rows in the same
  paragraph without the different-sets note.

### 20. First-census Diffend figures must not leak into the integrated report

- Claim (at risk): any "22 Diffend full / 1 RubyGems-only" sentence.
- Flaw: the first census said Diffend full 22, RubyGems-only 1
  (jrjackson). Reconciliation cut 4 to stub (apex-black-test-011,
  apex-oidc-probe, apex-blk-test-final, minitest-hashdiff, each
  ~5.7 KB, no diff content). The reconciled figures — full 18,
  RubyGems-only 5, Diffend-only 0 — are the only ones that may ship.
  Verdict-survivor and shell-phenomenon correctly use the reconciled
  figures; the risk is an integrator copying a first-census sentence
  (including the first summary's "52 URLs carry real artifacts").
- Required change: grep the integrated draft for 22, 52, and
  "RubyGems only: 1" and replace with 18, 48, and 5, or delete.
  State the adjudication (4 full → stub) beside the first mention of
  the 18 so a reader comparing against the first summary is not
  confused.

## Shell gone/stub caveat — downstream impact assessed

The caveat is real and correctly stated in shell-phenomenon §2: among
the 510 tombstoned names, 28 Diffend URLs return HTTP 302, but only 1
carries the "gone" label (klondikemarlen-jira-api); the other 27 carry
the "stub" label with redirect-to-index notes. Recomputed from the
tombstone-pairs file: status 302 = 28, labelled gone = 1,
labelled stub = 509, functional no-diff content = 510 of 510.

No downstream count in the draft depends on the wrong reading, because
the counts that matter use CONTENT, not the gone label: Diffend full
18, RubyGems-only 5, artifact URLs 48, and "Diffend holds stubs" for the
batch all survive whether the 27 are called stub or gone. Two traps
remain, both fixed by wording, not by recounting: (a) never print
"Diffend gone = 1" without "no-diff = 510, redirect-status = 28"
beside it; (b) the all-533 line "plain stub 510" includes live
jrjackson and must not be read as "510 tombstoned stubs" (tombstoned
labelled stubs = 509). Recommended future rule, as the shell lane
says: redirect-to-index = gone (gone 28, 200-stub 482), applied
uniformly — but relabelling is a future-census decision, not a
blocker for this report once the wording fix lands.

## Count-consistency table (recomputed by this reviewer)

| Count | Draft value | Recomputed | Status |
|---|---|---|---|
| CSV rows | 533 | 533 | Confirmed |
| API live / gone | 23 / 510 | 23 / 510, both censuses | Confirmed |
| Diffend full / RubyGems-only / Diffend-only (reconciled) | 18 / 5 / 0 | 18 / 5 / 0 | Confirmed; first census 22 / 1 / 0 is superseded |
| Artifact URLs, unique | 48 (23 + 18 + 7) | 48 unique; 49 live per-gem entries; 50 all-rows per-gem entries (`artifact_urls`) | Confirmed with denominator fix (19) |
| Tombstoned Diffend labelled stub / gone | 509 / 1 | 509 / 1; redirect-status 28; no-diff 510 | Label confirmed; content is 510 no-diff |
| Combinatorial / probe-family / ordinary | 310 / 203 / 20 | 310 grammar-confirmed; 203 / 20 rest on manual ordinary judgement (fix 9) | Arithmetic confirmed; grade the judgement |
| Payload rows, scan set / incl. author | 82 / 84 | 82 / 84; 86 − 4 overlap | Confirmed |
| Out-of-band rows | 48 (29 + 19) | 48, no overlap | Confirmed; different set from 48 artifacts |
| Apex substring | 115 (linguist) vs 114 (prior) | 115; prefix rules give 80 / 112 / 95, never 114 | Linguist confirmed; prior wrong |
| Probe-descriptive summaries | 117 (linguist) vs 105 (prior) | 117 = residual only; 105 reproduced by no tested rule; prior partition leaves 33 rows unaccounted | NEITHER shippable as a positive count (fix 8) |
| Placeholder summaries | 86 (54 / 19 / 9 / 4) | 86, exact | Confirmed |
| Epoch-suffixed names | 34 | 34 | Confirmed |
| Scored rows | 464 v1 + 20 v2 + 49 unscored | 464 + 20 + 49 = 533 | Confirmed |
| Tombstoned source URIs unchecked | 66 (open-questions) | 1 genuinely excluded + 65 with no URI; 196 present URIs all checked in first census | FALSE — delete (fix 14) |
| Total live downloads | 11,138,862 | 11,138,862; jrjackson 94.3% | Confirmed |
| CSV-latest = live-latest | 3 of 23 (verdict lane) | 4 of 23 (first-census latest field) | Wrong — fix 5 |
| July-7 rows / July-7 live | 204 / 6 | 204 / 6 (jrjackson + 3 probes + 2 tests) | Confirmed |
| July-7 known / new | 203 / 1 (jrjackson) | Per prior review; consistent with July-7 live set | Confirmed as prior-review figure |

## What the integrator must do before re-review

1. Apply fixes 1–20 in the integrated draft, not in the working lanes
   alone, and re-run the count table above against the revised draft.
2. Fetch version publish dates for the 23 live gems before any
   maintenance sentence ships (fix 4), and run the testgem-mini
   dependents / download-by-version check before any residue sentence
   ships (fix 3).
3. Delete the 66-gap and re-rank the open-questions gaps (fix 14);
   make the pkg-review-2 re-run conditional with scope 513 (fix 16).
4. Do not re-poll the 2 live OAST endpoints; do not fetch the internal
   metadata-address URI. Both restraints are correct as written and
   are not part of this NO-SHIP.
