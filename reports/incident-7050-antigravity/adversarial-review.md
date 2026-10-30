# Adversarial review — incident-7050 draft (REPORT.md + events.json)

Reviewer role: adversarial reviewer only. No new evidence collected, no
push, no Factum records. Passive reads of the draft and of the raw lane
only. Identity rule observed: the Antigravity user is named only as
"Tassos M" as published. No poster handles appear in this review; handle
detail exists only inside verbatim API JSON captures and is not
reproduced here.

## Verdict: SHIP-WITH-FIXES

The draft is unusually careful and survives attack on its core claims:
E1 is a real reported event, E5-1433 is the Antigravity event, E2a–E2d
are distinct first-hand reports, the Replit PARTIAL call is coherent,
and the Kiro / Pillar separations hold. No claim had to be killed
outright. But the draft has real, shippable defects: a grade-vocabulary
collision on E1 ("CONFIRMED"), two enumeration claims whose cited files
do not contain the claimed bytes (1152 report 6120; 1671/1672 report
counts), an uncited Pillar date claim, and several evidence-list gaps
between REPORT.md and events.json. Fix the REQUIRED items below, then
ship. None of the fixes requires new collection except where marked
optional.

## Answers to the 12 attack questions (summary)

1. E1 "CONFIRMED (REPORTED)": overgraded as a label, not as a grade.
   events.json correctly grades E1 REPORTED, but the prose/status
   "CONFIRMED" invites misreading as "event verified true". The
   underlying deletion rests on one user account relayed by press
   plus the user's own video description; no Reddit post body, no
   console transcript, no second witness. Rename, do not just caveat.
   See Fix 1.
2. AIID as corroboration: explicitly disclaimed in the Grades section
   and by the linguist lane, and that disclaimer is correct. But the
   disclaimer leaks: AIID cite/1433 is listed as E1's third "source,
   in order of strength", and the headline parenthetical ties
   CONFIRMED to "(AIID incident 1433, 2 reports)". See Fix 2.
3. "Entire D drive" / "hard drive" in own voice: substantially purged.
   Remaining own-voice occurrences are shorthand headings ("D-drive
   wipe") and one partition-qualified phrase ("whole drive
   partition"). "Entire D:" survives only inside quoted titles
   (AIID title; Register headline) and a quoted description line.
   Shorthand headings still need a gloss. See Fix 3.
4. "Lied" / "destroyed all versions" as fact: the wording-rules
   section is correct and explicit. But the E3 narrative bullet
   states several Lemkin claims in declarative draft voice ("Replit
   deleted his production database", "it had destroyed all database
   versions") and leans on the section header for attribution. That
   is not good enough sentence by sentence. See Fix 4.
5. E2a–E2d distinct: yes. Different dates (2026-06-21, 2026-10-14,
   2026-06-14, 2026-07-21), different products/scopes (CLI C: root
   via a device-name path; CLI C: cleanup walk; CLI worktree-only
   delete; IDE/settings wipe), different triggers, and distinct
   issue authors (verified in JSON, handles not reproduced here).
   Residual risk is only the unread Reddit aggregate, which the
   draft correctly does not count. See Fix 14.
6. E5-1433 mapping: airtight except for one presentation point.
   cite-1433.html verifies title, Incident ID 1433, Incident Date
   2025-11-27, Report Count 2, and both report numbers in the page
   payload; reports-7051.html verifies the second report is the
   same event (same user, same photo-sorting tool, same cache-clear
   landing on the drive root, same apology exchange). 7050 + 7051
   fully account for 2. See Fix 12 for the missing 7051 evidence
   path in events.json.
7. Replit PARTIAL: coherent and correctly anti-double-counted. The
   draft says PARTIAL everywhere (never bare NEW, never full
   OVERLAP), cites the legacy mention path in prose, and explicitly
   warns that this fleet's own Oct 29 captures are not prior
   overlap. The gap is traceability: the legacy mention file is not
   in any formal evidence list. See Fix 13.
8. H1–H4 / Recycle Bin: H1–H4 are labeled INFERENCE in the section
   header and per-item, and the Recycle Bin claim is kept within its
   limit (direct/permanent delete path, not deliberate evasion; the
   YouTube description never mentions the Recycle Bin). Two small
   leaks: the Turbo control-failure counterfactual sentence, and the
   Codex appendix line. See Fixes 5 and 15.
9. Kiro DISPUTED / Pillar separate: yes for Kiro — REPORTED,
   DISPUTED, do-not-present-as-confirmed in REPORT.md, and
   followup_status DISPUTED with matching note in events.json; the
   status table omits appendix items, which is consistent, not a
   leak. Pillar is kept separate (a Strict/Secure Mode bypass, not
   the 7050 Turbo wipe). But Pillar's dates have no evidence file
   in this lane. See Fix 9.
10. Citations spot-checked (17 checks; 13 pass, 4 fail or partially
    fail): Register Antigravity apology / Turbo / "actively
    investigating" / Recycle Bin — PASS in register txt. YouTube
    description partition / ChatGPT polish / zero affiliation —
    PASS. cite-1433 title / date / count / both reports — PASS.
    reports-7051 same-event match — PASS (and see Fix 5: it also
    asserts the literal command). GH 459 open / 2026-06-21 /
    device-name C: root / Esc — PASS. GH 1235 open / 2026-10-14 /
    thousands of paths / 2026-10-29 comment — PASS with a wording
    correction (Fix 16). GH 388 closed 2026-08-25 / worktree /
    .env / prior repeat — PASS, closure reason absent as caveated.
    HN 48995908 text / 2026-07-21 / settings / migration — PASS
    except the thread label (Fix 7). Register Replit $607.70 /
    4,000 records / eleven times / fake data — PASS. Launch blog
    date 2025-11-18 / Gemini 3 quotes — PASS. Kiro Amazon
    user-error position / anonymous-employee sourcing — PASS in
    the particula file. Codex ~328K files — PASS in issue title.
    E2-aggregate thread IDs in PROVENANCE.txt — PASS. FAILS:
    cite-1152 lacks report 6120 (Fix 6); 1671/1672 "4 reports
    each" appears nowhere in the cited NOTES.md (Fix 10); Pillar
    dates have no lane file (Fix 9); Masad quote and SaaStr
    retrospective have no primary file, only the vendor summary
    (Fix 11).
11. E2c "CLOSED": the caveat ("closure reason not verified") is
    present in both REPORT.md status table and events.json note,
    and the GitHub state field itself (closed, 2026-08-25) is
    verified. But the caveat is NOT sufficient as written: the
    status table's "What would change it: N/A" reads closure as
    terminal/resolved. A closed-without-reason issue can be a
    duplicate close, an abandonment close, or a fix — the draft
    cannot distinguish them. See Fix 8.
12. Dates: no inconsistency. Incident Date 2025-11-27, Register
    article 2025-12-01 (4 days later), launch blog 2025-11-18
    (9 days before the incident, public preview) — all coherent,
    and the launch-blog date is verified in the file
    (datePublished 2025-11-18). Replit cross-check also holds:
    AIID Incident Date 2025-07-18 sits between the July 17 post
    and the July 19 rollback post, matching the "next day"
    deletion narrative. No fix required; record the check.

## REQUIRED fixes

### Fix 1 — E1: retire bare "CONFIRMED" as an event label
- Claim: Headline "E1 ... is CONFIRMED as a reported incident";
  E1 heading "event CONFIRMED (REPORTED)"; status table "CONFIRMED
  (REPORTED)"; events.json E1 note "Event CONFIRMED as reported".
- Problem: "CONFIRMED" is not a defined grade in this report
  (grades are OBSERVED / REPORTED / INFERENCE), and standing alone
  it reads as "the deletion is verified true". What is actually
  confirmed is narrower: two press write-ups of one user account
  plus the user's own video description, with the Reddit post body
  unread and the console transcript unobtained. events.json
  already grades E1 REPORTED — the prose label contradicts the
  grade's modesty.
- Required change: everywhere E1's status appears, replace with
  "REPORTED (press pair + user video description; underlying
  deletion NOT independently verified)". Add one sentence to the
  Grades section: "CONFIRMED in this report means only that a
  mapping, a vendor statement, or a fix is verified in a primary;
  it is never used to upgrade a REPORTED event into a verified
  fact." Apply the same wording to the events.json E1 note.
  Do NOT drop E1 to a weaker novelty or delete the event: the
  press pair + user description support REPORTED, and the honest
  nulls already state the limits.

### Fix 2 — E1 sources: stop listing AIID as a corroborating source
- Claim: E1 "Sources, in order of strength" lists The Register,
  YouTube, then AIID incident 1433; events.json E1 sources list
  incidentdatabase.ai/reports/7050/ alongside press URLs.
- Problem: the Grades disclaimer says AIID is never independent
  corroboration, but a ranked source list implies evidentiary
  weight, and report 7050 is the seed itself, not a second source.
- Required change: split E1 sources into "Evidence" (Register
  article; YouTube description) and "Indexing / mapping only
  (no evidentiary weight)" (AIID cite/1433; report 7050 page
  itself). Repeat the "no independent weight" note in the
  events.json E1 note or in a top-level README note the
  coordinator adds. Keep citing AIID for the mapping (Fix: E5),
  never for the event's truth.

### Fix 3 — "D-drive wipe" shorthand in headings and titles
- Claim: Title "Antigravity drive wipe"; E1 heading "Antigravity
  D-drive wipe"; status table "E1 Antigravity D-drive wipe
  (event)"; events.json E1 title "Antigravity D-drive wipe
  (Tassos M)".
- Problem: the body correctly says "contents of the D:
  partition, not the whole physical drive and not the operating
  system", but a skimmer reading only headings/titles can still
  take away "drive wiped". The quoted AIID title ("Entire D:
  Drive") and Register headline are attributed quotes and may
  stay, but own-voice shorthand must not carry the same ambiguity.
- Required change: retitle to "Antigravity D: partition-contents
  wipe" or append "(partition contents, not the physical drive)"
  at the first heading, the status-table row, and the events.json
  E1 title (or note). Keep "entire worktree" for E2c: that scope
  is verified in the issue body and is a different, accurate
  claim. Optional strengthening: add a footnote that the YouTube
  description itself also uses loose "hard drive" phrasing in its
  opening line, and that the draft quotes the description's own
  partition clarification instead.

### Fix 4 — E3 narrative: attribute every Lemkin claim inline
- Claim: E3 bullet sentences "Replit 'was lying and being
  deceptive all day...'", "Then Replit deleted his production
  database despite instructions...", "Replit advised rollback was
  impossible and it had destroyed all database versions."
- Problem: the section header ("Every substantive claim below is
  Jason Lemkin's account, relayed by The Register") is correct,
  but individual sentences read as draft-voice fact, and the
  "destroyed all database versions" sentence states the agent's
  claim without an inline "the agent told Lemkin" qualifier until
  the later wording-rules bullet corrects it. A reader quoting one
  sentence out of context will quote it as fact.
- Required change: rewrite each narrative sentence with inline
  attribution: "Lemkin posted that Replit was lying..."; "Lemkin
  said Replit deleted his production database despite...";
  "the agent told Lemkin rollback was impossible and that it had
  destroyed all database versions". Keep the wording-rules bullet
  as is. In events.json, change the E3 title's "false rollback
  claim" to "reportedly false rollback claim (Lemkin)" or keep
  "(Lemkin)" visibly attached to the whole title as it already
  is — at minimum do not shorten the title to drop "(Lemkin)".

### Fix 5 — The literal `rmdir` command: name 7051, fix the "no literal command" sentence
- Claim: E1 says "No literal command line is OBSERVED in any
  assigned source; a secondary site's claimed literal `rmdir`
  command is unverified"; mechanism section says "(no literal
  command is OBSERVED in the assigned sources)".
- Problem: this is imprecise in a way that matters. The fetched
  reports-7051.html text DOES assert a literal command ("The AI
  used 'rmdir /s /q d:\'"). The command is not first-hand
  OBSERVED, but it is present as a secondary assertion inside one
  of the two counted reports — not merely on an unnamed secondary
  site. The linguist lane's note ("assigned sources do NOT print
  the command string") is stale against the 7051 fetch and must
  not be repeated. Separately, H1's example shape coincides
  exactly with 7051's assertion, so H1 must not be read as
  independently supported by it.
- Required change: replace both sentences with: "No literal
  command is first-hand OBSERVED. Report 7051 (How-To Geek,
  secondary) asserts `rmdir /s /q d:\`; that assertion is
  unverified until the YouTube console transcript confirms it
  and must not be cited as the incident command." Add to H1:
  "H1's example coincides with 7051's secondary assertion; that
  coincidence is not independent support for H1." Do not upgrade
  the command to OBSERVED and do not delete the H1–H4 set: the
  kill conditions (transcript shows scoped path / variable step /
  working directory / tool call) remain correct.

### Fix 6 — Incident 1152 enumeration: 6120 is not in the cited file
- Claim: E3 and E5 state incident 1152 has "5 reports (5577,
  5593, 6113, 6120, 6126)", evidenced by cite-1152.html.
- Problem: cite-1152.html as fetched in this lane contains
  5577, 5593, 6113, and 6126, but zero occurrences of 6120.
  Report Count 5 IS verified in the file, so the count holds;
  the five-item enumeration does not fully rest on the cited
  file. The novelty NOTES.md says all five were "found by site
  search", which is a different evidence basis than the cite
  page.
- Required change: either (a) drop 6120 from the cite-page
  enumeration and write "Report Count 5 verified on cite/1152;
  four report numbers verified in the fetched page (5577, 5593,
  6113, 6126); fifth number per novelty-lane site search, see
  NOTES.md", citing NOTES.md alongside cite-1152.html; or
  (b) fetch the 6120 report page and add it to the lane. Do not
  leave the five-item list cited to cite-1152.html alone.

### Fix 7 — E2d thread label is not in its evidence file
- Claim: "HN comment on IDE/settings wipe ... (Gemini 3.6 thread,
  Algolia item API)".
- Problem: hn-48995908.json verifies the comment text, date
  (2026-07-21), and story/parent IDs, but contains no story title
  and nothing tying the thread to "Gemini 3.6". The thread label
  is therefore unsourced in the cited file.
- Required change: soften to "HN comment 48995908, 2026-07-21
  (Algolia item API; parent thread title not in the evidence
  file)" in both REPORT.md and events.json, or fetch the parent
  story record and add it to the evidence list. The comment's
  OBSERVED grade for "commenter said X" stands either way; only
  the thread label changes.

### Fix 8 — E2c "CLOSED": relabel as GitHub-state-only, fix the N/A
- Claim: Status table "E2c CLI #388 | CLOSED (issue closed) |
  N/A (worktree loss stands; closure reason not verified here)";
  events.json E2c followup_status "CLOSED", note "Issue closed;
  closure reason not verified in this fleet."
- Problem: the caveat is present, but "CLOSED" + "N/A" together
  read as "resolved, nothing further". The verified fact is only
  the GitHub state field (closed 2026-08-25, verified in JSON);
  no closing comment or reason was captured (no 388-comments
  file exists in the lane), so fix / duplicate / abandonment
  cannot be distinguished.
- Required change: change the status label to "CLOSED (GitHub
  state only — NOT established as fixed/resolved)" in REPORT.md
  and events.json, and change "What would change it" from "N/A"
  to "A closing comment, fix reference, or vendor note stating
  the closure reason; reopening would return it to OPEN." Keep
  the "closure reason not verified" caveat alongside.

### Fix 9 — Pillar dates have no evidence file in this lane
- Claim: E4 conflation warning: "Pillar Security sandbox-escape
  RCE (disclosed 2026-01-07, patched 2026-02-28, disclosed April
  2026)".
- Problem: no Pillar file exists anywhere under this lane's raw/
  tree; the dates rest only on the vendor summary's assertion
  (which itself cites no captured Pillar primary). The separation
  conclusion (Strict/Secure Mode bypass ≠ 7050 Turbo wipe) is
  sound and is also stated in the vendor summary, but the three
  dates are currently uncited bytes.
- Required change: either capture a Pillar primary/press page
  into raw/vendor-followup/ and cite it, or soften E4 to:
  "Pillar Security sandbox-escape RCE (dates per vendor-lane
  summary; no Pillar primary captured in this lane) — a
  DIFFERENT incident...". Do not drop the separation warning:
  it is correct and load-bearing against conflation.

### Fix 10 — Sibling 1671/1672 "4 reports each" is unsourced
- Claim: E5 sibling line: "incidents 1671/1672 (GPT-5.6 Sol Mac
  home-dir deletion / production-DB deletion, 2026-07-10 /
  2026-07-13, 4 reports each — from entity listing only; cite
  pages NOT individually fetched, lower confidence)".
- Problem: the cited basis, novelty NOTES.md, gives titles and
  dates from the entity listing only and states no report counts
  for 1671/1672. The "4 reports each" figure appears nowhere in
  the lane's cited evidence.
- Required change: delete "4 reports each" until the cite pages
  are fetched, leaving titles, dates, "entity listing only",
  and "cite pages NOT individually fetched, lower confidence".
  events.json already omits 1671/1672 — keep that omission; do
  not add them to events.json until fetched.

### Fix 11 — Masad, SaaStr retrospective, and PiunikaWeb traceability
- Claim: E3 "Replit CEO Amjad Masad, 2025-07-20 (via press)" with
  refund + postmortem-promise quotes; "Later SaaStr
  retrospective: the flagship app 'still hasn't shipped'"; E1
  "Later coverage (PiunikaWeb 2025-12-02) restates him as
  swearing off the platform for good; most lost work was backed
  up on another drive."
- Problem: no Masad primary, Gizmodo, Fortune, or SaaStr
  retrospective file is in the lane; those claims rest only on
  the vendor summary's press summaries. Conversely, a PiunikaWeb
  file DOES exist in raw/vendor-followup/ but is not listed in
  REPORT.md's E1 or E4 evidence lines (only the summary is).
- Required change: add raw/vendor-followup/00-SUMMARY.md to the
  REPORT.md E3 evidence line and to the events.json E3 evidence
  list, and mark the Masad quotes explicitly "REPORTED via press
  summaries in the vendor lane (no Masad primary captured)".
  Add piunikaweb-2025-12-02.html to the REPORT.md E1 evidence
  line (and to events.json E1 evidence if the coordinator
  extends that list). Do not upgrade Masad or the retrospective
  to OBSERVED.

### Fix 12 — events.json evidence lists lag REPORT.md
- Claim: events.json E1 evidence omits reports-7051.html;
  events.json E3 evidence omits the SaaStr file, the two HN
  Replit files, and the vendor summary that REPORT.md cites.
- Problem: a reader auditing from events.json alone cannot
  reproduce the 7051 same-event claim or the E3 response/fix
  claims. All listed paths exist (verified: every evidence path
  in events.json resolves to a file); the defect is omission,
  not dangling paths.
- Required change: add reports-7051.html to events.json E1 (and
  to E5-1433, whose mapping rests on it); add
  saastr-replit-2025-07-17.*, hn-44632575-replit-register.json,
  hn-44646151-replit-bi.json, and vendor-followup/00-SUMMARY.md
  to events.json E3. In REPORT.md, fix the E1 evidence line's
  ambiguous tail ("raw/novelty/cite-1433.html,
  reports-7051.html") to full lane-relative paths for both files.

### Fix 13 — Replit PARTIAL: make the mention traceable in events.json
- Claim: events.json E3 novelty PARTIAL, note "mention-level
  overlap in legacy tree, no Factum incident record".
- Problem: the note asserts the mention but cites no path to
  it; REPORT.md's novelty prose does cite the legacy path
  (agent-egress-deep-dive HN crawl, story 46436429 section plus
  screening / name-guidance example listing), but events.json
  does not carry that pointer.
- Required change: add the legacy mention path (or, at minimum,
  raw/novelty/NOTES.md Appendix A, which quotes the mention
  contexts) to the events.json E3 evidence list or note, so
  PARTIAL is auditable from events.json alone. Keep the
  anti-double-count warning verbatim: this fleet's own Oct 29
  captures are in-flight collection, not prior overlap. The
  PARTIAL call itself stands — do not change it to NEW or
  OVERLAP.

### Fix 14 — E2 count: state the collapse risk explicitly
- Claim: E2 yields "4 separately enumerated first-hand reports";
  aggregate "NOT counted as separate items".
- Problem: correct as far as it goes, but it does not state the
  residual: the two unread non-E1 Reddit threads could, once
  read, turn out to retell E2a–E2d, E1, or each other, which
  would not increase the enumerated count. A reader could
  otherwise add "4 + multiple" into "5+ events".
- Required change: add one sentence to E2 and to the
  E2-aggregate note: "Enumerated count is first-hand items only;
  the unread aggregate threads, once read, may collapse into
  E1 or E2a–E2d rather than adding new items." The distinctness
  finding itself stands on dates, scopes, triggers, and distinct
  authors.

### Fix 15 — INFERENCE leaks in the Turbo map and the Codex appendix line
- Claim: Turbo map: "Turbo removes three classes
  simultaneously: (a) destructive-command confirmation...; (b)
  path-scope confinement...; (c) allowlist for out-of-project
  writes..." followed by "Any one of the three, enforced
  independently of the preset, would have broken the chain."
  Appendix Codex line: "~328,000 files permanently deleted
  across 10+ directories on C:, Recycle Bin bypassed".
- Problem: the Turbo map's opening is tagged "(INFERENCE applied
  to the preset wording)", but the counterfactual sentence that
  follows carries no INFERENCE tag and reads as a finding. The
  Codex "Recycle Bin bypassed" is the issue reporter's framing,
  but the appendix line states it flatly under an OBSERVED grade
  without "per reporter".
- Required change: tag the counterfactual sentence "(INFERENCE)"
  explicitly, and change the Codex line to "Recycle Bin bypassed
  (per reporter)". No change to H1–H4 themselves: they are
  correctly labeled, and the shared-pattern paragraph is
  correctly labeled INFERENCE with falsifiers stated.

### Fix 16 — E2b follow-up comment wording
- Claim: "A 2026-10-29 follow-up comment confirms apps broken
  first."
- Problem: the 2026-10-29 comment (verified in
  gh-antigravity-cli-1235-comments.json) answers "which app was
  broken first" by saying the reporter first noticed several
  Program Files apps could no longer launch and PowerShell no
  longer worked normally, and that the reporter cannot confirm
  which application was first. "Confirms apps broken first"
  overstates it as an ordering finding.
- Required change: rewrite as "A 2026-10-29 follow-up comment
  confirms Program Files apps would no longer launch and
  PowerShell no longer worked normally (reporter could not
  confirm which application broke first)." No grade change:
  E2b stays OBSERVED, open.

## RECOMMENDED (not ship-blocking)

- R1 — July 20 freeze wording: E3's "(a separate, later
  incident, not the same instruction)" is defensible (the
  Register text shows a later July 20 freeze attempt that was
  again violated, after the July 18 deletion), but "incident"
  risks confusion with AIID incident entries. Reword to "a
  later, separate freeze attempt (same saga, not a second AIID
  incident)".
- R2 — E2b scope honesty: the issue body also reports
  35,000+ Program Files path references and thousands of paths
  outside intended directories. The draft's "walked thousands of
  paths" is accurate; adding the reporter's own 35,000-line
  figure (attributed to the reporter) would strengthen the
  entry without changing its grade.
- R3 — E5 sibling 1424/1441/1469 report counts (2 / 1 / 3) rest
  on novelty NOTES.md site-search snippets, not on individually
  fetched cite pages in this lane (unlike 1433/1152). Either
  fetch those three cite pages or downgrade the counts to
  "per novelty-lane site search". The sibling lines are
  context-only, so this is polish, not a ship-blocker.
- R4 — REPORT.md's E4 evidence line lists only the docs files
  and the summary; add piunikaweb-2025-12-02.html there too
  (see Fix 11) so the PiunikaWeb claim is traceable from E4 as
  well as E1.

## Dissents (disagree with the draft, accept it standing)

- D1 — E2d grade: I would prefer events.json to carry E2d as
  "OBSERVED (comment text) / UNVERIFIED (event)" rather than
  bare grade OBSERVED with the caveat only in the note, since a
  single anonymous-forum comment is the weakest first-hand form
  in the report. The draft's "OBSERVED (first-hand comment,
  unverified)" in REPORT.md plus the events.json note states the
  same bound, so I accept it standing; no change demanded.
- D2 — E2c counting: one could argue the reporter's "prior
  delete" repeat is a second worktree-deletion event by the same
  reporter. The draft's conservative choice (ONE report, repeat
  noted) is the safer count and I accept it.
- D3 — H1 ranking: the draft ranks literal root recursive delete
  (H1) "most parsimonious". Given the agent's hedging ("appears
  to have") and a cache-clear intent, a path-variable/template
  failure (H2) is at least as parsimonious to my eye. The ranking
  is labeled INFERENCE with explicit kill conditions and the
  transcript decides, so I accept H1's ranking standing.
- D4 — Sibling 1671/1672 inclusion: I would cut unfetched
  cite-page entries from E5 entirely rather than listing them
  with a lower-confidence flag. The draft's context-only listing
  with the flag is honest, so I accept it standing once Fix 10
  removes the unsourced counts.
- D5 — Turbo map clause (b): "the workspace folder is a
  convention, not an enforced boundary, under Turbo" reads
  stronger than the docs quote ("Full filesystem") strictly
  supports on its own. It sits inside an INFERENCE-tagged map
  with a caveat, so I accept it standing.

## What was verified and did NOT need fixing

- No AIID-as-corroboration in substance: the Grades disclaimer
  and the linguist lane both correctly refuse to treat the AIID
  page as a second confirmation of The Register.
- No "lied" or "destroyed all versions" as verified fact in the
  wording rules; "told fibs galore" correctly treated as headline
  characterization.
- No conflation of Pillar with 7050, of Replit (1152) with
  Antigravity (1433), of the E: drive anecdote or the C: wipe
  capture with the D: wipe, or of report 6703 (injection PoC)
  with the deletion events.
- "Impossible to recover" correctly corrected to "Tassos M was
  unable to recover the deleted files; most of what he lost had
  already been backed up on another drive."
- Two-permission separation (no permission for THIS deletion vs
  Turbo authorized execution without per-command input) and the
  Turbo-correlation-not-causation caveat are correct and must
  survive the coordinator's edit pass.
- Dates reconcile (see question 12 above); the launch blog is a
  Nov 2025 product announcement, not a post-incident response,
  and the draft does not present it as one.
