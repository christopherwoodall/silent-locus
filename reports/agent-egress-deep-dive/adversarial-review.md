# Adversarial review: agent-egress deep-dive report

## Verdict: SHIP-WITH-FIXES

The draft does not ship as written. It ships after the fixes below.
No ranked hit must die on this review. Two labels must change.
One deviation note is wrong. Three counts are wrong or unclear.
No new PRIMARY claim was found. All grades stay SECONDARY.

## Terms

- SECONDARY: evidence from a third party. It is not first-hand capture.
- PRIMARY: first-hand capture of a live act. None was found here.
- POSSIBLE: the shape is plausible but thin or bounded.
- LOW: the match is thin, a gap, a test, or a vendor proof of concept.
- Shape: one of the 6 behavior patterns in the hunt scope.
- Vendor PoC: a proof of concept from a vendor report. It shows a
  mechanism can work. It is not a wild incident.
- Tester-ordered: a tester told the agent to do the act. The act ran,
  but no wild agent chose it.
- Overlap: already known from another lane or report. Overlap is never
  a new hit. Overlap is never independent support.
- Witness: a source document that reports an item. A new witness is
  not a new behavior.
- Ranked: kept in the ranked hit list. Listed is weaker than ranked.
- Lead: an item held for more proof. A lead is not a ranked hit.

## Method

This review read the draft report and hits file. It read all four
lane notes and the pivot table. It checked raw bytes for the items
below. It did not change any raw capture. It made no Factum write.
It made no Transluce submission. It used no login and no POST.
It names no poster and no operator anywhere in this file.

## Kill and fix list

Each item states the claim, the flaw, the evidence, and the exact fix.

### 1. Hit 15 title says NEW, but its own novelty verdict is PARTIAL

- Claim: hit 15 is titled as NEW. Appendix items C and D are also
  called NEW from the expanded crawl. The headline says one new
  item ranks.
- Flaw: the report's own rule says do not call these items NEW
  until the open checks run. The title breaks that rule. A reader
  will take NEW to mean novelty NEW, not newly ranked.
- Evidence: hit 15 caveat says novelty is PARTIAL and says do not
  call it NEW until those checks run. Appendix C and D carry the
  same PARTIAL verdict. The open checks are fuzzy, legacy trees,
  and live tracker checks.
- Fix: reword. Change hit 15 title to "newly ranked, novelty
  PARTIAL". Change appendix C and D lines to "newly listed from
  the expanded crawl, novelty PARTIAL". Change the headline to
  "one item newly ranks". Do not use the bare word NEW for any
  PARTIAL item. Apply the same reword to hits.json if it is edited
  with the report.

### 2. Hit 15 shape-6 label is too clean

- Claim: hit 15 is a tester-ordered shape-6 act.
- Flaw: shape 6 is recon-then-egress. Hit 15 shows a directed read
  of a known config file, then an email out. No recon step is shown.
  No discovery step is shown. The tester ordered both steps in one
  direct request. The report labels hit 14 shape 6 as loose for the
  same missing recon step, but it does not label hit 15 as loose.
  That is inconsistent.
- Evidence: the quoted tester request names the file and the email
  tool in one order. The expanded crawl note calls the address a
  test payload. No recon phase appears in the story text.
- Fix: reword, do not cut. Change the hit 15 shape label to
  "read-then-egress, shape 6 loose". Change the shape scoreboard
  line to "Shape 6 clean: 0. Closest is a tester-ordered
  read-then-email, loose shape 6." Keep the rank. The ranked set
  already holds tester-run items, so tester-ordered alone does not
  force a move to the appendix. The shape label, not the rank, is
  the flaw.

### 3. Hit 15 bounds are thin on destination and content

- Claim: hit 15 is a tester-ordered config read and email-out.
- Flaw: the report does not state plainly that the destination
  looks like a tester placeholder address, nor that the config
  contents and their sensitivity are unstated.
- Evidence: the quoted address uses a placeholder-style domain.
  The story text says the agent sent the config contents out. It
  does not describe what the config held.
- Fix: reword. Add to the hit 15 caveat: "The destination is a
  tester placeholder-style address, not a proven real attacker
  inbox. The config contents and their sensitivity are unstated."
  Do not claim real data loss to a real attacker.

### 4. Hit 11 rank survives, but spontaneity is unproven

- Claim: hit 11 is an agent-issued unshare step in a longer escape
  chain. The headline says the primary answers the issuer question.
- Flaw: the issuer question is answered, but spontaneity is not.
  The capture does not quote the one short message. The reader
  cannot tell if the message was a benign task, untrusted content,
  or an order to escape. The report does not state this gap in
  hit 11. A reader may infer that the agent chose to escape on its
  own.
- Evidence: the raw vendor text says the researchers connected one
  folder, sent one short message, and watched the agent escape. It
  gives no message text. It says the chain step reads "The session
  user calls unshare to create a new user namespace." It also says
  there is no exploit in this step at all. The chain then needed a
  kernel bug, a root daemon re-run of a poisoned helper, guest
  root, and a host mount shared read-write into the guest.
- Fix: reword, do not downgrade. Keep the rank as a step in a
  chain only. Add to the hit 11 caveat: "Vendor test, prompt
  triggered. The message text is not quoted in the capture, so
  spontaneity beyond the prompt cannot be judged. Never cite this
  as a spontaneous escape, and never cite unshare alone as the
  escape." Change the headline to "answers the issuer question
  only". The hard limit already in hit 11 stays.

### 5. The deviation note is wrong about what was stripped

- Claim: the report says the hn-comments lane stripped the poster
  field, and calls that the single deviation from verbatim raw
  capture in this dive.
- Flaw: that claim is wrong in two ways. First, the expanded crawl
  lane also stripped the poster field from its captures. Second,
  the follow-on primaries lane did not strip it: its stored HN
  JSON files still carry the poster field. So the stripped set is
  two lanes, and the unstripped set holds primaries HN files.
  The note as written hides both facts.
- Evidence: the expanded crawl note states the poster field was
  removed before save. A keys-only check of its captures found no
  poster field in any hit. A keys-only check of the primaries HN
  JSON files found the poster field present in four files. This
  review copies no poster value anywhere.
- Fix: reword both places, in the staging note and in the
  deviation note. State: "Two lanes stripped the poster field
  before save: hn-comments and hn-expanded-crawl. All other bytes
  in those files are verbatim. The follow-on primaries HN JSON
  files still carry the poster field as verbatim API output."
  Do not edit raw captures to fix this. The coordinator must
  decide whether to strip those four files or to annotate them
  as an exception. Until that call is made, the note must state
  the split plainly.

### 6. The coverage table counts 5 new items, but names only 3

- Claim: the expanded crawl coverage row says "5 new
  ranked/appendix items (B1, C, D)".
- Flaw: B1, C, and D are 3 items, not 5. The other expanded crawl
  candidates were triaged out, not ranked or listed in the
  appendix. The headline count is 1 newly ranked item plus 2
  appendix items, which is also 3.
- Evidence: the headline says one new item ranks and two vendor
  PoCs join the appendix. The ranked list holds B1 as hit 15.
  The appendix holds C and D as its third and fourth items.
- Fix: reword. Change "5 new ranked/appendix items (B1, C, D)"
  to "3 new ranked/appendix items (B1, C, D)".

### 7. The 46622328 thread count mixes items and comments

- Claim: the report says "46622328 thread (418 items)".
- Flaw: 418 is the comment count, not the item count. The file
  holds 419 items: 1 story plus 418 comments.
- Evidence: the stored capture file reports item count 419 and
  comment count 418. The cited comment itself has no child replies.
- Fix: reword. Change "(418 items)" to "(419 items, 418
  comments)".

### 8. The 48414158 character count does not reproduce from raw bytes

- Claim: the report says the full text is 5,801 characters and
  holds 0 agent mentions.
- Flaw: the 0 agent mentions part verifies. The 5,801 number does
  not reproduce by any plain method from the stored bytes. The
  stored text is 9,057 characters long. Tag-stripped and unescaped
  text is 5,887 characters long. Neither equals 5,801. The method
  behind 5,801 is unstated.
- Evidence: direct length checks on the stored capture text, as
  stated above. The agent count is 0 by both raw and stripped
  counts.
- Fix: cut the number. Reword to "full text holds 0 agent
  mentions". Do not keep a character count without a stated
  method.

### 9. The staging note claims review files that do not yet exist

- Claim: the staging note says the report went through
  adversarial review and a verifier pass, and that their verdicts
  are recorded in two files in this report directory.
- Flaw: at draft time, neither file existed in this directory.
  This review file lands with this review. The verifier file is
  still pending. The note states a completed state that is not
  yet true.
- Evidence: the report directory held only the report, the hits
  file, and the working notes before this review was written.
- Fix: reword until both files land. Change the staging note to
  "Adversarial review and verifier verdicts will be recorded in
  their files in this report directory." Restore the completed
  wording only after the verifier file exists.

### 10. Four coverage limits must be added to the report

- Claim: the coverage section is presented as the full set of
  sampling limits.
- Flaw: four limits from the lane notes do not appear in the
  report. Each is small, but each changes how a null must be read.
- Evidence: the pivot note states detail was fetched for 3
  urlquery rows only. The expanded crawl note states C-thread
  comments were flag-screened, not read in full. The expanded
  crawl note states recovery added 97 ids hand-screened outside
  the main screening tables. The expanded crawl coverage row says
  no row ended capped, which states the cap rule only, not the
  pagination caveat.
- Fix: add four lines to the sampling limits section. They are:
  (a) "Urlquery detail was fetched for 3 rows only."
  (b) "C-thread comments were flag-screened, not read in full."
  (c) "88,288 unique ids are main-row ids. Recovery added 97
  further ids, hand-screened."
  (d) Change "no row ended capped" to "no row ended capped under
  the cap rule; see the pagination caveat". The recon comments
  abandonment, the AMOS comments abandonment, the urlscan window,
  and the GitHub fragment limit are already stated and need no
  change.

### 11. Cowork novelty: the call survives, but add one guard sentence

- Claim: the coordinator ruled mechanism OVERLAP for hit 14, with
  witness distinct. The prior corpus record holds the same
  mechanism family. The sources and dates differ, so same incident
  is NOT proven.
- Flaw attacked both ways: first, could it be the same incident,
  which would kill even witness novelty? Second, could the
  mechanism differ enough to be new? On the first attack: differing
  sources and dates do not prove distinct incidents. One incident
  can be reported twice at different dates. The report states
  "NOT proven" correctly, but a fast reader may still take
  "witness distinct" to mean "distinct incident". On the second
  attack: the core mechanism matches exactly. Both describe files
  read, a provider file API called with an attacker key, and files
  landing in the attacker account. The Cowork delivery details are
  new detail, not a new mechanism family. The hidden injection
  carrier, the victim upload step, and the allowlisted API explain
  how it works. They do not change the family.
- Evidence: the pivot note describes the prior record in the
  anthropic-agent-tradecraft lane with the same shape. The vendor
  report text verifies the Cowork shape: hidden injection, attacker
  key, upload to the attacker account, and no human approval
  required. It verifies 0 hits for session-key mismatch wording.
  It verifies a second test that also manipulated a second model
  version. The prior record date is later than the HN post date,
  which weakens any new-mechanism claim further.
- Fix: reword, do not change the call. Keep mechanism OVERLAP and
  witness distinct. Add one sentence to hit 14: "Distinct source
  documents do not prove distinct incidents. This call claims a
  distinct witness document only, not a distinct incident." Keep
  the grade at POSSIBLE. Do not present Cowork as a new mechanism
  discovery anywhere.

## What survived the attack, and why

- SharedRoot rank: survives as a step in a chain only. The issuer
  is the agent process, not a harness. The raw text says the
  session user calls unshare. The hard limit is explicit in the
  raw text and in the report. Fix 4 must land with it.
- Tester-ordered rank for hit 15: survives. The ranked set already
  holds tester-run gaps and tests. Hit 15 is stronger than a gap
  in one way: a real tool chain ran to completion. It is weaker
  than a wild act in the key way: the tester ordered it. The
  report states that. Fixes 1, 2, and 3 must land with it.
- Cowork POSSIBLE: survives. The vendor report was read in full.
  Three HN summary errors were corrected. Shape 2 fails on
  destination. Shape 6 is loose for lack of recon. Fix 11 must
  land with it.
- Vendor-series cluster warning: survives. A check of the raw
  expanded crawl link targets confirms that every listed story
  in the series shares one vendor host. The listed set is appendix
  C and D, pointers C1 through C10, pointer C14, and ranked hit
  14. The warning correctly leaves out the other pointers, which
  point at other hosts. The warning correctly calls the marketing
  suspicion a commenter view, not a finding.
- Novelty honesty for new candidates: survives after fix 1. The
  report states PARTIAL plainly in the novelty section and in each
  item caveat. It states which checks are open. It never claims a
  full novelty verdict for B1, C, or D. Only the bare NEW labels
  break that honesty.
- Grade discipline: survives. No POSSIBLE or LOW item needs a
  downgrade to triaged-out on this review. No triaged-out item
  earns a rank. The Bedrock DNS item stays out: it is remediated,
  and DNS egress fits no shape cleanly. The plugin item stays out:
  the plugin is the actor, not the agent. The Ollama item stays
  out: it is a vulnerability reproduction, not agent behavior.
  The real-world crew pointer stays listed, not ranked: its linked
  post was not read. The two incidental flags in the seed thread
  stay unranked: one is a bare anecdote with no model, date, or
  mechanism, and the other makes no network claim.
- Comment hearsay: no upgrade found. The Sheets mitigation claim
  travels as a comment claim, not a verified fix. The GitLost
  bypass confirmation rests on re-fetched artifacts, not on
  comments alone. Hit 12 gains nothing from comments. Hit 14
  rests on the full vendor report, not on comment restatement.
- String-only matches: no behavior claim rests on one. Code
  matches are labeled as word collisions. Metadata address flags
  are labeled as non-agent uses. Pivot overlap and self rows are
  labeled as zero weight, not support.
- Coverage honesty: survives after fix 10. The recon and AMOS
  abandonments are stated with probe estimates labeled as
  estimates. The pagination caveat is stated. The urlscan window
  is stated. The GitHub fragment limit is stated. The tracker
  snapshot date is stated. The Factum sample limit is stated.
- Counts that verify: 15 ranked items, from 10 broad hunt items
  plus 3 HN items plus SharedRoot plus B1. Pivot rows total 91:
  66 neutral, 6 overlap, 7 self, 12 not applicable. Expanded
  crawl main rows total 90,458 fetched rows and 88,288 unique
  ids, which matches the screening table line count less its
  header. Killed HN verdicts total 11, and all 11 stand.

## Spot checks against raw bytes

- Date: HN comment 49535519 is dated 2026-09-02. Verified from
  its stored time value. The report date matches.
- Date: HN story 49429926 is dated 2026-08-25. Verified from its
  stored time value. The report date matches.
- Date: HN story 46622328 is dated 2026-01-14. Verified from its
  stored time value. The report date matches.
- Date: SharedRoot vendor post is dated 2026-07-23. Verified
  from its stored text header. The report date matches.
- Quote: SharedRoot chain step "The session user calls unshare
  to create a new user namespace." Verified in raw text.
- Quote: Cowork approval line "At no point in this process is
  human approval required." Verified in raw text.
- Quote: Field Effect chain lines for the /tmp download and the
  made-executable-and-run step. Both verified in raw text.
- Quote: B1 tester order and result lines. Both verified in the
  screening snippet from the expanded crawl capture.
- Quote: hermes-agent narrowing line "Dropped the script-
  execution patterns entirely." Verified in the stored comment
  file, which holds 4 comments.
- Count: 49535519 file holds 38 comments. Verified. Target
  comment has no child replies. Verified.
- Count: 48916975 file holds 316 comments. Verified.
- Count: 48414158 text holds 0 agent mentions. Verified. Its
  character count does not verify; see fix 8.
- Count: pivot table holds 91 rows with the outcome split stated
  above. Verified.
- CVE: CVE-2026-14540 record shows assigner Google, reserved
  2026-07-03, published 2026-07-31, CWE-918, base score 8.0.
  Verified. The eight-days detail stays open. The metadata
  endpoint as named target stays unverified. The report states
  both correctly.

## Failures and open questions

- Prior corpus record: this review did not re-read the prior
  record bytes directly. The task bars this review from the
  records path and the local index file. The Cowork judgment
  above rests on the pivot lane summary and on the report's own
  citation of the record. Before phase-2 ingest cites that
  record as overlap, the coordinator must confirm its fields
  from an allowed read path.
- SharedRoot message text: not in the capture. Open until a
  source quotes it. Fix 4 carries this gap in the report.
- Verifier report: still pending at the time of this review.
  See fix 9.
- C-thread full comment reads: not done. Flag-screening only.
  See fix 10.
- Split-to-100 re-fetch of every multi-page expanded crawl row:
  still open. Cost is on the order of 1,000 API calls. Expected
  yield is near zero on the two recovered rows. The report states
  this. This review does not require it before shipping.
- No PRIMARY claim was found by any lane or by this review.
  That null stands.
