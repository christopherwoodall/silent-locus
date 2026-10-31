# ADVERSARIAL REVIEW — continuous hunt round 20261031

Role: adversarial reviewer. Job: try to kill claims.
Operator: BigSexyWarlock69. Repo: silent-locus.
Date of review: 2026-10-31 (America/Chicago).
Method: passive reads of the five FINDINGS files plus spot re-derivation
from their staged captures. No commit. No push. No Factum write.
No POST, no login, no session. No Shodan. Package repos and Docker Hub out.
No human poster handle appears in this review. No signed value, token,
or query string appears here.

Verdict key. KILL: do not ship the claim as written. DOWNGRADE: ship only
with the corrected grade or wording given. STAND: the claim survives
attack as written, with the qualifier stated in the lane file.

## Overall verdict: SHIP-WITH-FIXES

No VERY-interesting flag survives. That is correct. Nothing below is a
genuinely new wild agent or swarm behavior with first-hand evidence.
The round may ship as a continuity and measurement round only, after
every blocking fix in §6 is applied. Any NEW claim, any VERY-interesting
flag, and any combined total that sums overlapping lanes is a NO-SHIP
until the named check is run.

Counts in this review: 52 verdict assignments.
KILL: 8. DOWNGRADE: 14. STAND: 30.

## Cross-lane kills (read first — they affect every lane)

### X1. Double-count trap: committer lane vs unmeasured lane — KILL

The two lanes measured the same three queries independently:
the Codex commit search, the Claude-Code PR search, and the
agent-harness PR search. Re-derivation from captures proves overlap:
Codex, 30 of 30 commit SHAs shared; harness PR, 30 of 30 URLs shared;
Claude-Code PR, 29 of 30 URLs shared (one row differs in each lane,
consistent with ranking drift between runs, not with two samples).
These are near-duplicate pulls of one page-1 slice, not independent
corroboration. Kill any total, rate, or "confirmed by two lanes"
wording that sums or stacks the committer 210 rows with the
unmeasured rows. The unmeasured lane's "120 commits" figure is
legitimate only as meta-lane plus Codex (Copilot 30 + Claude-footer 30
+ Devin 30 + Codex 30). It must never be added to the committer 210.

Evidence: raw/committer/gh-commits-codex.json vs
raw/unmeasured/gh-commits-codex.json; the two PR capture pairs.

### X2. No lane completed the full novelty legs — DOWNGRADE (blocking)

Surfaces, committer, rotation, and unmeasured state plainly that no
direct Factum exact + fuzzy check was run by that lane (no-touch
constraint). Phrases ran a Factum DB match, but its own file limits
it: fuzzy mode is heuristic, not an exhaustive absence test, and the
full legacy evidence-tree grep and the full 140-finding Transluce
check were not run. Consequence: no candidate in this round carries
NEW. Every "not seen in checked sources" wording stands only in that
provisional form. The coordinator must run the Factum exact + fuzzy
check and the full Transluce check before any filing uses NEW.

### X3. Page-1 and capped values are never totals — DOWNGRADE (blocking)

Every GitHub, HN, and urlquery count in this round is a page-1 or
capped-slice count. The lanes mostly say this. The coordinator's
round report must repeat the denominator in the same sentence as
every number: "N of 30 rows returned", "N of 300 saved", never a bare
total. Token counts (GitHub total_count, Algolia nbHits, urlquery
total_hits) are search-engine estimates, not exact counts. The
phrases lane proves this: saved HN rows (200) exceed nbHits (169)
for one phrase. Kill any downstream citation that drops the
denominator or cites a token count as an exact total.

### X4. Window — STAND, with one pre-window note

All cited behavior instances I checked fall in the November 2025
onward window, except items the lanes already exclude: the Claude-Code
PR bot row dated 2025-08-27 (both lanes correctly count it
out-of-window) and the rotation CDX dead-inbox capture dated
2025-10-31 (one day before the window; the lane claims nothing
in-window from it). No in-window claim was found resting on a
pre-window row. The phrases sweeps do contain pre-window rows in
their saved 30 (for example one 2025-09-04 row in the
"autonomous agent intro" saved set), but no rank rests on a
pre-window instance. The round report must not cite phrase token
totals as in-window totals.

## 1. Surfaces lane — 4 STAND, 2 KILL

Source: raw/surfaces/FINDINGS.md.

- S1. swarmbar.com, live active board, stats endpoint — STAND.
  Re-derived from capture: stats bytes give 30 registered agents,
  4 humans, 10 agents active in 7 days, 0 humans active, updated
  2026-10-31T18:22:33Z. Tabs bytes show activity 2026-10-28 through
  2026-10-30, latest 2026-10-30T18:34Z. These are endpoint-reported
  counts, not an independent census; keep that qualifier. The
  cross-link to another agent board is a link, not coordinated
  action, exactly as the lane grades it.
- S2. agentboard.ai, live active board, fresh posts — STAND.
  Re-derived: feed holds 50 entries, latest 2026-10-31T17:46:19Z;
  sitemap counts are 153 thread URLs and 155 agent URLs by loc
  count, and the sitemap index lists only those two sub-sitemaps
  plus a static one, so "sitemap-listed" is a fair qualifier.
  No poster handle is named. Good.
- S3. agentdm.ai, live but no observable public activity — STAND.
  DMs are private by design. The lane correctly refuses to treat
  plan-limit marketing copy as activity. Sitemap lastmod values
  include 2026-10-14, consistent with "no new public page seen".
  This is a null for observable activity only, not a liveness null.
- S4. fallback.chat, live but quiet, latest post Oct 28 — STAND.
  Re-derived: feed holds 50 entries, latest 2026-10-28T20:24:50Z,
  next entries 2026-09-29. The sitemap/feed lastmod mismatch is
  correctly resolved in favor of the feed. Quiet gap is described
  as bursty and sparse, not as a slowdown finding. Correct.
- S5. agentbadge.xyz as an ACTIVE agent surface — KILL.
  The lane itself grades it CANDIDATE, first snapshot, no board,
  directory and marketplace counts not fetched. Kill any promotion
  of agentbadge to "active surface" in the round report. Ship only
  as: live identity and readiness infrastructure, candidate,
  activity count unknown. Its agent-card version and doc claims
  are doc bytes, not observed agent acts.
- S6. Any change vs the Oct 30 / Oct 27 baselines — KILL.
  The lane is honest: no baseline capture files were found in-repo,
  so no byte diff was possible. Kill any downstream sentence that
  implies growth, decline, or change on any of the five surfaces.
  Current states are new snapshots only. Open question 1 (where the
  baselines live) is blocking for the next pass, not for this one.

Surfaces VERY-interesting flags: NONE. STAND. Correct. Continuity,
not a new lead.

## 2. Committer lane — 9 STAND, 4 DOWNGRADE, 1 KILL

Source: raw/committer/FINDINGS.md. Spot re-derivation from all
seven commit captures and both PR captures.

- C1. Codex footer lane, assisted only, single-repo cluster — STAND.
  30 of 30 rows User-authored, web-flow committed, one repo, one
  author. Page-1 concentration is flagged, not generalized. Good.
- C2. Cursor footer lane, assisted only — STAND.
  30 of 30 User, web-flow, 17 distinct authors. Footer shape
  verified in message bytes in my re-derivation.
- C3. Jules footer lane, assisted only — STAND.
  30 of 30 User, web-flow, 10 distinct authors. The lane's
  correction matters: the query matched a token inside a vendor
  bot account name, not a display name. The verified footer shape
  (vendor bot footer) is the claim, not the search hit. Correct.
- C4. Aider footer lane, assisted only — STAND.
  29 of 30 aider-footer rows, 26 of 30 from one repo, single
  Bot-type author row is CI automation with a web-flow committer.
  Correctly graded as automation, not an agent account.
- C5. Gemini footer lane, footer subcounts — DOWNGRADE (blocking).
  The headline counts survive: 30 rows, Bot-type authors 5 of 30,
  committer Bot 0 of 30, web-flow 27 of 30, 29 distinct authors,
  29 distinct commits (one SHA duplicated). The subcounts do not
  survive as written without definitions: (a) "12 of 30 carry a
  literal Co-Authored-By: Gemini string" is true only
  case-insensitively; case-sensitive count is 3, because most
  matching lines use a different case or a model-qualified form.
  (b) "gemini-code-assist bot footer on 8 of 30" counts only the
  bot-suffixed form; any gemini-code-assist footer line counts 9.
  (c) "any bot-suffixed footer on 9 of 30" does not match a
  line-level recount, which gives 11 rows (10 distinct commits,
  because the duplicated SHA appears twice); 9 results only if
  the two duplicated rows are excluded, which the file does not
  state. Fix: state the matching rule (case, bot-suffix, row vs
  distinct commit) beside each subcount, or drop the subcounts
  to the verified headline counts. The lane's core warning stands:
  a search hit is not proof of an exact footer shape.
- C6. OpenAI Codex footer lane, assisted only — STAND.
  30 of 30 Codex-named footers, single Bot-type author row is
  dependency automation, web-flow committed. Model-qualified
  footer forms are correctly graded SECONDARY: self-declared
  model identity, not independently verified.
- C7. Copilot-bot author lane — DOWNGRADE.
  The lane is honest that the author qualifier did not restrict
  the set (29 of 30 rows User-authored) and that 1 of 30 must
  never be cited as a Copilot authorship rate. Ship only with
  that caveat attached: this is a text-match slice, not a
  bot-author census. The qualifier-only rejection is a query
  error, not a rate guard, as stated.
- C8. Claude-Code PR lane — STAND, with the out-of-window bar.
  Single Bot-type author row dated 2025-08-27 is out-of-window;
  in-window bot-type PR authors are 0 of 29. Title-or-body
  marker on only 8 of 30 rows; the rest matched elsewhere.
  A PR author is not a committer. All three caveats must travel
  with any citation.
- C9. Agent-harness PR lane, bot account name in committer prose
  — KILL (blocking).
  The committer file names the single Bot-type author row with a
  spelling that does not match its own capture. The capture, and
  the unmeasured lane's capture of the same row, both give the
  account name autter-dev[bot],
  dated 2026-10-28, on a dependency-update title. The committer
  prose drops one letter. Kill that prose citation until it is
  corrected character-for-character from the capture. The
  underlying grading survives: dependency automation, not agent
  authorship, and the other 29 rows are PRs ABOUT harnesses,
  not PRs BY agents.
- C10. Combined 300-row figure (meta 90 + this lane 210) — DOWNGRADE.
  The lane correctly calls it a measurement sum, not a population
  total, and forbids citing it as a rate. Keep that sentence
  attached. The two runs used different queries and page-1 slices.
- C11. Bot-type committers 0 of 210, App-type 0 of 210 — STAND.
  Every Bot-type author row has a User-type committer, web-flow
  in all but 3 rows. No standalone agent commit was found. This
  is the lane's central negative, and it survives.
- C12. Vitruvian-row "closest signal" — DOWNGRADE.
  A self-named agent bot account as author, carrying repeated
  model footers, is the closest signal in the lane. It is still
  web-flow committed, therefore mediated, not standalone. Ship
  only as "mediated agent-account author row, worth a
  coordinator decision on a deeper per-account pull", never as
  a standalone commit or a VERY-interesting flag. The same
  mediation downgrade applies to the other two new bot account
  names in this lane: vendor integration and model-bot accounts,
  web-flow committed.
- C13. Novelty wording "not seen in checked sources" — STAND.
  The lane correctly refuses established NEW: meta captures and
  local lists were checked, Factum was not touched by this lane.
  The three new bot account names and the new footer shapes stay
  provisional until the coordinator's Factum check.
- C14. 20 unswept meta phrases left UNMEASURED by this lane — STAND.
  Correctly stated, not silently absorbed. The unmeasured lane
  later measures them; see §5.

Committer VERY-interesting flags: NONE. STAND. Correct.

## 3. Rotation lane — 6 STAND, 2 DOWNGRADE, 2 KILL

Source: raw/rotation/FINDINGS.md.

- R1. urlquery last-24-hour slice, 0 genuine grammar candidates
  — STAND. Denominators re-derived: first pass 90 rows across
  6 queries, second pass 35 rows across 3 queries. The noise
  explanation is sound: the search matches page content as well
  as submitted URLs, so content-match rows without a marker in
  the submitted URL are not grammar hits. The htmx endpoint 404
  note is a real method finding for other lanes: switch to the
  search-page parser.
- R2. Out-of-slice relay batch dated 2026-10-26 — DOWNGRADE.
  Correctly left unclaimed and referred for a coordinator novelty
  check. Ship only as an out-of-slice watch item. Kill any
  promotion of it into a last-24-hour finding: it is outside the
  slice even though it is inside the November 2025 onward window.
- R3. Wayback CDX "no new captures" conclusion — DOWNGRADE (blocking).
  The raw counts are fine (three prefixes hit the 100-row limit,
  so counts are floors; maxima in the returned samples match the
  claimed newest dates). The inference is not: the samples are
  capped at 100 rows and are not sorted by time, so the maximum
  of a capped sample does not prove the global newest capture.
  Reword to: "no capture newer than [date] in the 100-row capped
  sample for each prefix; global newest unverified without a
  sorted or date-filtered query." The dead-drop verdicts for the
  zero-capture prefixes survive as sample results, not as
  exhaustive proofs. The old plugin-manifest shape note is prior
  art, correctly not re-claimed.
- R4. Mouse-brain lab agent item — KILL as VERY-interesting or
  wild behavior; REPORTED grade itself is not attacked.
  This is the round's most notable item and the lane grades it
  right: REPORTED (press account of a founder's claim), human
  approval of the plan, human kill switch, no agent access to rig
  code, one model refused at the needle step. It fits the
  widened direction toward irreversible real-world action, but
  it is a reported lab demo with humans in the loop, not wild
  swarm behavior and not first-hand evidence. Kill any flag,
  headline, or filing that presents it as wild behavior, as a
  standalone agent act, or as VERY-interesting. A standing watch
  on agent-driven lab rigs is the operator's call, not this
  lane's, as stated.
- R5. Multi-agent parliament sim — STAND as DISCUSSED.
  Staged eval, permissive prompts by design, vendor claims of
  bribery and extortion. Not wild behavior. Correctly not a finding.
- R6. Defense-contractor Pentagon-system item — STAND as
  REPORTED talk only. One commenter note (unclassified network
  reading) does not corroborate a classified-access claim.
  Correctly not a finding.
- R7. MecAgent drive-scan and upload claim — KILL as a finding.
  Title-only claim, Reddit source returned 403, no workaround
  attempted (correct), no Reddit-sourced claim made (correct).
  Ship only as "blocked, unverified, title-only". Any sentence
  that repeats the title as if it were an observed act is killed.
- R8. Harness issue 1713, destructive delete regression — STAND
  as REPORTED single-harness behavior note. Prompt ambiguity
  root cause diagnosed by the owner, fix verified on the fixed
  build. Single-harness scope is stated. Not wild swarm behavior.
  Not VERY-interesting. Correct.
- R9. Harness issue 2420, over-asking regression — STAND.
  Mirror-image eval note, 2 of 2 attempts, single harness.
  Correctly not a finding.
- R10. Reddit blocked, GitHub HTTP/2 error transient — STAND.
  Failures are documented, not smoothed over. The GitHub issue
  reads that succeeded are full reads, not title scans.

Rotation VERY-interesting flags: NONE. STAND. Correct.

## 4. Phrases lane — 7 STAND, 4 DOWNGRADE, 1 KILL

Source: raw/phrases/FINDINGS.md. Table numbers re-derived from
the staged sweep files: HN saved and exact counts match the files
for all 10 phrases; GitHub exact-title counts match for the
phrases re-checked (including 3 of 30 for the lowest-collision
token and 14 of 30 for the protocol phrase).

- P1. Rank 1, lowest-collision harness token — DOWNGRADE.
  The token is real: GitHub token total 155 (smallest in the set
  by two orders of magnitude), 3 of 30 exact titles, one full body
  showing a runtime emitting the token on session-update
  notifications. That proves a harness feature exists in the wild.
  It does not prove an agent act. Ship only as a search signature
  for harness telemetry leaks, graded DISCUSSED product
  fingerprint, never as behavior evidence. The lane's own
  downgrade (same as the sweep's tool-family downgrade) is right.
- P2. Rank 2, first-person delegation anecdotes — STAND as
  REPORTED. HN exact 6 of 31 is the highest exact ratio among
  small-denominator phrases, but every instance is one operator's
  own account of their own session, uncorroborated by a trace,
  and one instance is a single joking sentence. No wild
  multi-agent act. Correct grade.
- P3. Rank 3, protocol-discourse signature — STAND.
  HN exact 21 of 54 and GitHub exact-title 14 of 30 are the
  broadest exact coverage in the set. The live Matrix experiment
  is operator-run, not wild coordination. Concept-known in
  corpus vocabulary (see novelty section). Grade REPORTED for
  experiments, DISCUSSED for protocol work. Correct.
- P4. Rank 4, visitor-log filing — DOWNGRADE.
  Filing act is OBSERVED (issue bytes exist, dated 2026-09-07).
  Identity claim is SECONDARY: self-asserted, disclosed human
  partner, no bot or app marker, no workflow trace, no
  maintainer acceptance staged. Instance-new, surface-known:
  the pattern mirrors the prior pursekeeper-style self-filed
  listing but is weaker, and the surface family was already
  killed as a multi-agent claim for single-account authorship.
  Ship only as a watch item. The lane correctly refuses a
  VERY-interesting flag here. Do not let the round report
  upgrade "watch item" to "agent found".
- P5. Rank 5, disclosed payment experiment — STAND as REPORTED.
  One HN exact hit, self-built experiment, x402 mechanism family
  is prior art. Phrase new, mechanism not. No wallet, endpoint,
  or payment proof is reproduced. Correct.
- P6. Rank 6, protocol debugging term — STAND as DISCUSSED.
  GitHub exact-title 6 of 30, HN exact 0 of 300 capped. Debugging
  chatter about a protocol document, not agent behavior. The
  well-known agent-card surface is prior art, not re-claimed.
- P7. Rank 7, June agent-spam flood discussion — KILL as a finding.
  The vivid HN exact hits quote a press-linked incident, sitting
  next to off-script material. The lane claims only the phrase
  as a sweep string, not the flood as a finding, and notes the
  string already appears in corpus vocabulary from a different
  July wiki incident. Kill any round-report sentence that
  presents the flood as a new finding of this round. The open
  question (whether the flood is already filed) stays open.
- P8. Rank 8, fleet vocabulary — STAND as DISCUSSED.
  HN exact 3 of 21, including a complaint about the pattern.
  Vocabulary for talking about fleets, not evidence of one acting.
- P9. Rank 9, quoted self-declaration variant — STAND as
  DISCUSSED quotation. The single HN exact instance is discussion
  ABOUT self-declaration, quoting the sentence. Kill any citation
  of it as a disclosure instance; the lane already does.
- P10. Rank 10, generic harness vocabulary — STAND as DISCUSSED.
  GitHub exact-title 18 of 30 looks strong until read: framework
  task names across small personal repos. High counts, zero
  behavior. Kept so a future lane does not re-mine it as
  promising. Correct.
- P11. Phrase table token totals — DOWNGRADE (blocking).
  Token totals above 10,000 for three phrases are stemming noise:
  engines match words separately. Read the table by exact counts
  only, with saved denominators. HN exact 0 for two phrases rests
  on capped 300 saves; uncapped exact counts are unknown. The
  lane states all of this; the round report must not strip it.
- P12. Novelty status, provisional only — DOWNGRADE.
  Distinctive phrases show exact not_found in the Factum DB match
  and zero hits in the lists, reports, and Transluce-slice greps
  run, but the full legacy grep and the full 140-finding Transluce
  check were not run, and fuzzy mode is not an exhaustive absence
  test. Ranks 3 and 7 are explicitly concept-known. The rest are
  "phrase-new under the checks run", nothing stronger. No NEW
  label may ship on a partial check.

Phrases VERY-interesting flags: NONE. STAND. Correct, including
the explicit refusal to pad.

## 5. Unmeasured lane — 4 STAND, 4 DOWNGRADE, 2 KILL

Source: raw/unmeasured/FINDINGS.md. All 23 recovered items are
accounted for: 1 Codex commit lane, 2 PR lanes, 20 phrases.

- U1. Codex commit lane, measured — STAND.
  30 of 30 rows, User 30 of 30, Bot 0 of 30, footer on 30 of 30
  (lowercase form; the lane's self-caught case-sensitive error
  and correction is good practice). Single-repo, single-author,
  single-committer cluster. Assisted authorship only. This
  measurement is the same page-1 slice as committer C1 (see X1);
  it closes the unmeasured gap, it does not add a second sample.
- U2. PR lanes, returned rows — DOWNGRADE.
  The qualifier fix works (both calls returned rows). The lane's
  own caveat is blocking: the staged row shape carries no
  pull-request discriminator field, so PR status rests on the
  query qualifier, not on a staged field. Ship only as "returned
  rows under the type:pr qualifier", never as independently
  verified PRs, until a follow-up fetch checks a discriminator.
  Counts themselves survive: Claude-Code PR 29 of 30 in-window,
  harness PR 30 of 30 in-window, one Bot-type author row each.
- U3. Harness PR lane, capture-correct name — STAND.
  This lane's capture gives the bot account name in its doubled-
  letter form, matching the committer capture. This is the
  spelling the round report must use. Grading (dependency
  automation) matches committer C9. Lists-only zero hits are
  correctly not a novelty verdict.
- U4. Phrase pass table, 19 with rows plus 1 honest null — STAND,
  with the title-match bar attached. Title-match 0 does not mean
  absent from bodies (bodies were not fetched). Self-disclosure
  phrases (title-match 0, 0, 3) support no self-disclosure finding
  from this pass. Generic product vocabulary (notably the
  title-verified 30 of 30 for the MCP-server phrase) is a
  vocabulary count, not behavior evidence. In-window counts
  re-derived for the short-return phrases match the file.
- U5. Bot-heavy phrase rows as agent evidence — KILL.
  Phrase 7 (28 of 30 Bot-type authors), phrase 14 (24 of 30),
  and phrase 11 (5 Bot-type rows across 2 accounts) each
  collapse to one or two platform-automation accounts across
  few repos. The lane grades them automation noise, not a
  finding. Kill any round-report sentence that cites "28 of 30
  bot authors" or "24 of 30 bot authors" as agent activity.
  Single-account collapse kills the multi-agent reading.
- U6. Phrase 20 null — DOWNGRADE.
  Zero rows on issue search plus zero rows on a code-surface
  second pass is an honest null for that exact token combination
  on those two surfaces. Kill any broader reading: it is not a
  zero for every token form, and it is not a zero on other
  surfaces. The lane states this scope; keep it attached.
- U7. Combined "5 of 120" commit figure — DOWNGRADE.
  Completed lanes only, with the single-cluster qualifier in the
  same sentence: the Codex lane is a single-repo, single-author
  cluster, not a cross-repo sample, and all 5 bot-type authors
  come from the single Devin integration account reported by the
  meta lane. Never cite "5 of 120" without that qualifier, and
  never merge it with the committer lane's 210 (see X1).
- U8. Summing committer + unmeasured rows — KILL.
  Same as X1, stated here because this lane is where a reader
  would try it: the Codex and PR rows appear in both lanes.
  Any combined denominator spanning both lanes is invalid.
- U9. Rate-guard mechanism inference — DOWNGRADE.
  The lane labels it INFERENCE, not established: one quiet-window
  success after two failures under fleet traffic is consistent
  with shared-bucket pressure, not proof of it. Ship only with
  the INFERENCE label. The run record itself (no guard fired,
  55-second pacing, pre-run bucket full) stands.
- U10. PR-lane shape caveat and open questions — STAND.
  The lane correctly leaves body-match, second-repo Codex check,
  and novelty legs as open coordinator questions instead of
  filling them with guesses.

Unmeasured VERY-interesting flags: NONE. STAND. The Codex
concentration narrows rather than extends the Codex claim, as
stated. Correct.

## 6. Blocking fixes (all must land before the round report ships)

1. Correct the harness PR bot account name in the committer file
   to the capture spelling, character for character. Do not ship
   either spelling until the correction is verified against the
   capture (see C9 / U3).
2. Ban double-counting in the round report: state once, prominently,
   that committer and unmeasured Codex + PR rows are the same
   page-1 slices, and never sum them (see X1 / U8).
3. Reword the rotation CDX conclusion to the capped-sample form
   in R3. No absolute "no new captures" sentence may ship.
4. Reconcile the Gemini footer subcounts with explicit matching
   rules (case, bot-suffix, row vs distinct commit), or cut them
   to the verified headline counts (see C5).
5. Attach denominators to every number in the round report, and
   cite exact counts only, never token counts or capped values
   as totals (see X3 / P11).
6. Keep all VERY-interesting flags at NONE. Do not promote the
   mouse-brain lab demo, the visitor-log filing, the Vitruvian
   row, or the relay batch (see R4, P4, C12, R2).
7. Run the coordinator Factum exact + fuzzy check and the full
   Transluce check before any candidate is labeled NEW. Until
   then, "not seen in checked sources" is the strongest allowed
   wording (see X2).
8. Word all PR-lane rows as "returned under the type:pr qualifier",
   not verified PRs (see U2).
9. Scope the phrase-20 null to its exact token combination on
   issue + code surfaces only (see U6).
10. Keep the single-account and single-repo collapses attached to
    every affected claim: Codex cluster, automation-bot phrase
    rows, single-harness issues, single-account village filing
    (see C1, U5, R8, P4).

## 7. Non-blocking notes for the next pass

- Surfaces open questions 1-5 stand as written: baseline locations,
  agentbadge directory and marketplace counts, any public agentdm
  activity signal, fallback.chat quiet-gap normality, and
  swarmbar booth volume (token-gated, unread, correctly unread).
- Committer open questions stand: Factum check for the three new
  bot account names and new footer shapes; fate of the 20 phrases
  (now measured by the unmeasured lane, so this question is
  closed by U4, not by the committer lane); per-account pull
  decision for the mediated agent-account row; author-qualifier
  behavior probe; second Codex page to test ranking artifact.
- Phrases next step is a paced body-level pass for title-zero
  phrases, not a bulk retry. The lane's pacing note (meta fleet's
  secondary-limit stop) is a real constraint, not an excuse.
- Rotation method note stands: any lane still using the old htmx
  endpoint will get empty results and must switch parsers.

## Evidence paths checked

- data/lanes/continuous-hunt-20261031/raw/surfaces/FINDINGS.md
  and its per-target capture dirs with provenance and hashes.
- data/lanes/continuous-hunt-20261031/raw/committer/FINDINGS.md
  and gh-commits / gh-prs captures (re-derived counts above).
- data/lanes/continuous-hunt-20261031/raw/rotation/FINDINGS.md
  and urlquery, CDX, HN, and issue captures.
- data/lanes/continuous-hunt-20261031/raw/phrases/FINDINGS.md
  and hn_sweep / gh_sweep captures (table re-derived).
- data/lanes/continuous-hunt-20261031/raw/unmeasured/FINDINGS.md
  and phrase / commit / PR captures (overlap re-derived).
- This review only: reports/continuous-hunt-20261031/
  adversarial-review.md. No commit, no push, no other worker's
  file touched, no Factum write, no record or database touched.
