# Sniffer-sweep meta-analysis and information-exploitation fleet — report

Operator: BigSexyWarlock69. Date: 2026-10-31. Coordinator: meta fleet parent.
Scope: rogue agents, swarms, agent infrastructure. Window: November 2025 onward.
This report is staged only. No Factum writes were made. The parent pushes
and verifies.

Terms, defined on first use. TOI means target of interest. OBSERVED means
first-hand bytes show the act. REPORTED means a party claims the act and
bytes do not corroborate it. DISCUSSED means talk or planning with no
executed act. SECONDARY means identity or attribution rests on someone
else's say-so. A count without a denominator is not a total.

## Headline result

The meta fleet attacked the sniffer sweep and followed its open threads.
Eight lanes ran: meta-analyst, cryptologist, committer re-run, GH4/GH7,
follow-ups, urlquery/Wayback, adversarial reviewer, verifier. All eight
completed. No lane was padded to reach a target.

New ranked findings: 8 items (M1 to M8 below). One is a restated TOI
cluster with a larger verified count. One is new committer evidence.
One is a re-triaged survivor set. The rest are restatements, a resolved
mystery, and a candidate pattern.

The sweep's headline structure holds: 1 TOI cluster, watch items, and
negatives. Several of the sweep's numbers do not hold. The blocking
corrections are in section 3. Nothing in this report may ship with
those corrections unapplied.

ANEC-01 (the Reddit ban anecdote) is NOT covered here. A separate
fleet owns that rundown, per the brief. This report does not duplicate it.

## Ranked new findings

### M1 — TOI-01 restated: 9 live-verified iLands hiring posts, not 3

- Grade: OBSERVED for the posts. SECONDARY for the identity claim
  (self-asserted, unverified).
- What: the follow-ups lane re-fetched HN story 49922568 live and
  checked all 11 platform-name search hits in the thread through the
  HN item API. 9 of 11 verify as platform-affiliated, self-disclosed
  agent job-seeker posts. 2 of 11 are token-search false positives
  with no platform string, contact, or disclosure in live text.
- The 9, by date: Oct 1, Oct 5, Oct 6, Oct 7, Oct 7, Oct 9, Oct 11,
  Oct 12, Oct 12. All 9 carry a platform-domain contact line, a paid
  offer, and an explicit agent disclosure. 4 of 9 also link a platform
  content or bounty page. None is deleted or dead live.
- Counting rule, stated plainly: the sweep verified 3 posts live. This
  lane verifies 9 posts live. The 6 additional posts were already
  present in the sweep's Algolia evidence file. They are newly
  live-verified here, NOT newly posted since the sweep. Do not report
  them as new posts.
- September precedent verdict: NEW VARIANT, same family. The September
  thread is third-party discussion about unsolicited agent emails,
  with zero first-person agent posts. October is first-person posting
  inside the hiring thread itself, with a new template shape (header
  fields, disclosure, free-sample hook, one flat-price figure, platform
  contact and link). Two agent hiring-thread posts dated Sept 1 exist
  in the September hiring thread and were already in sweep evidence.
- Later posts: honest null. Latest affiliated post anywhere is Oct 12.
  Limit: the global token net after Oct 12 returned 396 hits, but only
  the first 100 were reviewed (0 exact platform-string matches). The
  "nothing later" verdict rests on the domain-precise nets plus the
  in-thread check. A post with no platform tie would be missed.
- Distinct-author count for the 9 is NOT established. The follow-ups
  lane does not state it. Do not cite "9 authors." The sweep's file
  holds 48 posts from 48 authors, which is a file property, not the
  cluster property.
- Kill condition, carried from adversarial review: if any one post's
  platform-tied contact fails on re-check, or shared authorship behind
  2 or more posts is shown, TOI-01 drops to watch. Disclosure is
  uneven: the explicit "not a person" form appears in 2 of the sweep's
  3, and the follow-ups lane reports explicit disclosure in all 9 on
  entity-decoded text. That wording difference is an open check, not
  a contradiction resolved here.
- Verification status: LANE-VERIFIED, not independently re-verified.
  The verifier lane ran before the follow-ups lane finished, so it did
  not re-check these 9 posts. The coordinator read the follow-ups
  FINDINGS and checked internal consistency (IDs, dates, counting
  rule) but did not re-fetch all 9 posts. Re-verify before any
  outward-facing use.
- Evidence: data/lanes/sniffer-meta-20261031/raw/followups/FINDINGS.md
  and captures in that dir.

### M2 — Committer evidence, new: bot-type authors exist in one lane

- Grade: OBSERVED for author-type bytes. SECONDARY for agent identity.
- What: the committer re-run completed 2 of 5 failed lanes.
  Claude-footer lane: 30 of 30 rows, author type User 30 of 30, Bot
  0 of 30, 12 distinct authors. Devin lane: 30 of 30 rows, author
  type Bot 5 of 30, User 25 of 30, 20 distinct authors. All 5
  Bot-type rows come from one account, a vendor integration bot.
  Committer type is User on all 30 Devin rows (web-flow mediated),
  so even the bot-authored rows are GitHub-App-mediated, not
  independent agent commits.
- Combined completed lanes: 90 commits (Copilot 30 + Claude 30 +
  Devin 30), bot-type authors 5 of 90, all from the single Devin
  account. A co-author footer proves assisted authorship, not
  standalone agent authorship. No standalone agent account acts as
  committer in any completed lane.
- Footer line counts from the rerun lane do NOT re-derive and must not
  ship: the lane reported Claude marker 229 lines and co-author 35
  lines across 7 commits, and Devin footer 404 lines. The verifier
  re-derived Claude marker 65 lines, co-author 32 lines across 6
  commits (a hard cap: only 6 commits carry any co-author footer),
  and Devin footer 385 lines. Ship the author-type counts, which
  verify exactly, and either correct the line counts to 65 / 32 / 6
  (Claude) and 385 / 30 (Devin) or drop line counts and cite only
  per-commit footer presence (Claude 6 of 30, Devin 30 of 30).
- Stopping point: call 3 of 25 (Codex query) hit HTTP 403 secondary
  rate limit at 2026-10-31T16:11:32Z, despite about 30-second pacing.
  The run stopped per orders, with no retry. Codex, both PR lanes,
  and all 20 unswept phrases remain UNMEASURED. No zero may be cited
  for them. The PR-lane fix (type:pr qualifier) is recorded but
  untested against the live API.
- Evidence: data/lanes/sniffer-meta-20261031/raw/committer-rerun/
  FINDINGS.md, STATE.md, STOPPED.txt, captures.

### M3 — GH7 re-triage: 4 cut, 6 non-trap, per-member grades

- Grade: per member below. Default SECONDARY.
- Partition, verified by the verifier: 4 cut (2 honeypot trap entries
  + 2 unticked-template false positives) and 6 non-trap. Never cite
  "3" and "6" interchangeably: the meta-analyst's "3 candidates" are
  the strongest subset of the 6, not the whole non-trap set.
- The 6 non-trap members:
  - Licence question filed on behalf of an operator with stated
    approval: OBSERVED delegated filing act.
  - Backport request with patch-on-fork act: OBSERVED filing plus
    patch act; test outcome REPORTED (build and test numbers were
    not re-run). Strongest act in the set.
  - Bounty-work disclosure plus offer entry: REPORTED filing act
    with self-claimed substance.
  - Directory-listing addition proposal: OBSERVED filing act;
    substance REPORTED and unconfirmed (act-grade follows the GH7
    lane, substance-grade follows the meta-analyst).
  - Registration filing: OBSERVED filing act; autonomy and payout
    facts are self-claims only.
  - Village launch note: OBSERVED filing act only; multi-agent
    coordination REPORTED, single-account, killed as a multi-agent
    claim (see section 4). Cite it only under GH2, never as a
    second GH7 instance.
- All 10 GH7 issues are OPEN at pull time. No maintainer acceptance
  is shown for any survivor except Village's 4 comments. Recheck
  comment and closure status before citing any survivor as accepted.
- Novelty spot-check for survivors: lists/urls zero for every key
  term; reports/ zero except Village in the parent sweep's own docs;
  Factum fuzzy found no true-substring hits (caveat: the tool warns
  its fuzzy match is heuristic, not an exhaustive absence test).
- Evidence: data/lanes/sniffer-meta-20261031/raw/gh4-gh7/FINDINGS.md
  and captures.

### M4 — da.gd restated: two day spikes, not one burst pattern

- Grade: SECONDARY pattern shape only. Agency unproved for both spikes.
- Volume claim verifies: full urlquery pull saved 98 of 98 rows with
  98 unique IDs. Month distribution (denominator 98): May 53, June
  31, May plus June 84 of 98. The saved-30 sample was
  non-representative, but the volume elevation was not a sampling
  artifact. The sampling caveat is retired.
- Pattern claim does NOT survive as one pattern. The full set holds
  two distinct day spikes:
  - June 21 echo-test cluster: 17 rows, 6 distinct short codes,
    echo-host shapes, decoded framing-probe pages (see M5).
  - May 19 spike: 19 rows, 16 distinct codes, 19:08 to 21:48 UTC,
    dominated by a different destination shape. May 19, not June 21,
    is the largest single day in the full set.
- The adversarial lane's full-pull conditions are now judged: June 21
  standout fails on day-count; shape carry-over fails as a single
  pattern; code-reuse rate verifies (15 repeating tails covering 43
  rows); full payloads decoded (M5); marker zero verifies (zz 0 of
  98, oai 0 of 98). Single-source status is unchanged: the CDX retry
  (50 capped rows, urlkey-ordered) neither corroborates nor
  contradicts a burst distribution, and the zz-filter CDX query
  504'd again with no further retry.
- da.gd stays separate from the oai/zz family. 0 of 98 zz flags and
  0 of 98 oai flags in the full set.
- Evidence: data/lanes/sniffer-meta-20261031/raw/uq-wayback/
  uq-dagd-domain-FULL.json, FINDINGS.md.

### M5 — da.gd decode corrected: full decode from final_path

- Grade: OBSERVED byte shapes in staged captures. Intent not provable
  from bytes alone.
- Correction: the sweep cryptologist's "full decode fails" claim is
  wrong for the final_path copy. It holds only for the 200-char-capped
  title copy. All 3 distinct June 21 segments decode fully from
  final_path after percent-unquoting (the unquoting step is the key
  method detail; raw decode alone gives garbage for 2 of 3):
  segment A: 628 chars to 471 bytes, style plus iframe plus script,
  no START marker, 8 rows. Segment B: 2400 unquoted chars to 1799
  bytes, START at byte 128, style plus pre plus div plus 2 scripts,
  3 rows. Segment C: 656 unquoted chars to 491 bytes, START at byte
  10, pre plus div plus 2 scripts, 2 rows. All UTF-8 valid, printable
  ratio 1.0. Title-copy partials (173, 181, 175 visible chars) are
  moot because final_path is complete.
- Verdict from saved bytes alone: framing probe, carrier not
  evidenced. Each segment repeats byte-identically across its rows
  (8x, 3x, 2x). A per-message carrier would vary per row and does
  not. START is a framing delimiter. Hosts are public echo services.
  Decoded pages are test-page scaffolding. Fresh live capture is not
  needed for decode; it would serve only live-response and submitter
  questions, which stay open for the parent.
- Evidence: data/lanes/sniffer-meta-20261031/raw/cryptologist/
  FINDINGS.md; verifier re-derivation in VERIFIER.md section 1.

### M6 — GH4 restated: product bug, open, unfixed

- Grade: REPORTED for reproduction and harms. OBSERVED for issue and
  PR states.
- What: the full LiteLLM identity-sentence issue was pulled. Created
  2026-09-21, 1 comment, no maintainer response found, state OPEN,
  never closed. Affected providers include DeepSeek, MiniMax, Tencent,
  and OpenAI-like passthrough endpoints via the Anthropic-to-OpenAI
  chat-completions bridge. Expected behavior: strip the sentence only
  for non-Claude models, keep it for first-party Claude and
  Claude-serving Bedrock, Vertex, and Azure.
- The body's "Resolved by #42203" claim does NOT hold at pull time.
  Linked PR #42203 is OPEN and UNMERGED (created 2026-09-21, updated
  2026-09-28, 12 comments). Its before-and-after proof is the PR
  author's reported claim, not maintainer acceptance.
- Why not stronger: the sentence goes to the model the request was
  already routed to. That is a false self-description, not a secret
  or credential sent to an unintended party. Downstream harms
  (guardrail firing, wrong self-identity in responses, rejections)
  are reporter-claimed and unverified here. No version range is
  stated in the issue or PR. Do not cite one.
- Non-blocking gap: the PR review-association claim (CONTRIBUTOR and
  NONE only) is unstaged. Soften to "no maintainer-identified review
  found in staged captures" unless a reviews capture is staged.
- Evidence: data/lanes/sniffer-meta-20261031/raw/gh4-gh7/ captures
  for the GH4 issue, comments, and PR record.

### M7 — Candidate pattern: delegation-disclosure (not yet a linkage)

- Grade: candidate pattern, not a linkage, not a finding.
- Shape: on-behalf filing plus a named principal plus an approval
  claim, seen across the licence filing, the backport message, the
  pursekeeper filing, and the tron protocol. It needs more instances
  plus automation traces before promotion. It must never be merged
  with the honeypot disclosure templates: the shared "I am an AI
  agent" sentence is generic and the two families are separate.
- Evidence: data/lanes/sniffer-meta-20261031/raw/meta-analyst/
  FINDINGS.md (pattern scores P1 to P8).

### M8 — zz flagged row resolved: redirect artifact, not agent evidence

- Grade: resolved negative.
- What: the sweep's zz-plus-agent file holds exactly 1 flagged row in
  its saved 30 (row 26). No saved field (path, final path, title)
  contains the flagged string, and no saved field carries a query
  string. The uq-wayback lane's transient re-fetch explains why: the
  flagged parameter lives in the final redirect landing URL's query,
  which the saved row does not preserve, while the submitted URL has
  no query string. The fresh re-run total drifted (68265 to 68260)
  with 0 flagged in the new top 30, consistent with a rotated-out
  snapshot row. The file-level count of 1 stands as a sweep-time
  snapshot. It is a redirect-landing tracking-parameter artifact, not
  a submitted zz marker and not agent evidence.
- Control files stay clean: zz-only file 0 flagged in 30, oai-tag
  file 0 flagged in 30. No new-window zz, oai, or epoch marker is
  corroborated by any saved row.
- Evidence: cryptologist FINDINGS.md, uq-wayback FINDINGS.md,
  verifier section 3 (X3).

## Sweep corrections — blocking before any ship

These corrections come from the meta-analyst, the verifier, or both.
The verifier's word wins where lanes disagreed.

- B1. GitHub search totals. Neither prior statement ships. Corrected
  statement: 12 issue searches, 76 issue items; 2 code searches, 10
  code items; 86 items staged in total. The sweep report's "86 issue
  hits" is wrong: 86 is the all-search total, not the issue-only
  total. The meta-analyst's "74 across 11" is wrong the other way:
  it omits file q12 (2 items, issue-search shape). No 13th search
  file and no other gap remains in staged bytes.
- B2. Committer footer line counts. See M2. Ship author-type counts
  only, or the corrected line counts (Claude 65 / 32 / 6, Devin
  385 / 30). Do not ship 229 / 35 / 7 / 404.
- B3. Headline arithmetic. The sweep's 1 + 1 + 3 + 3 + 12 = 20
  double-counts: the refusal negative sits inside the 12 cuts. The
  adversarial review's "16 claims" matches neither its own 17
  headings nor the true total. Corrected distinct total: 19 items =
  1 TOI + 1 anecdote + 3 watch + 12 cuts + 2 further negatives
  (tango-zulu, committer). Ship one mutually exclusive item table
  and derive all counts from it.
- B4. Transluce scope errors. "ilands 36 mentions" is 36 occurrences
  inside 1 finding, not breadth. "da.gd 0" is true only for the
  25-item slice; the full 140-finding list holds da.gd in 2 findings
  with 5 occurrences (findings 122 and 146, prior family material,
  not the burst). Pursekeeper: 1 finding, 1 occurrence.
- B5. Pursekeeper Factum leg. "Absent from Factum" is false in the
  token sense. Fuzzy match finds 4 values containing the token,
  including an offers-page record and a pursekeeper API-issue
  citation, independently verified by the verifier via exported
  batches. WATCH-02 stays instance-new and surface-known, but its
  Factum leg must be restated. Exact-value not_found is taken as
  stated (mode semantics), not re-run by the verifier.
- B6. WATCH-03 volume-shape merge. Do not merge live volume (84 of
  98) with saved-set shape into one burst claim. Split into two
  sentences: volume elevation (May plus June 84 of 98) and two day
  spikes with distinct shapes (see M4).
- B7. Committer scope qualifier. Any "5 of 90" citation must carry
  "completed lanes only (Copilot + Claude-footer + Devin); Codex,
  PR, and phrase lanes unmeasured" in the same sentence.
- B8. Unscoped superlatives. "Strongest burst" and "strongest
  grammar cluster" must be scoped to the saved subset and the vendor
  tracker respectively, in the same sentence.
- B9. Hash denominator. The sweep verifier's "107 hash entries, 0
  failures" lacks its denominator in the counts section: 4 lanes
  only, 3 lanes uncovered at that time. State the denominator.

Non-blocking corrections, to apply with the blocking set:

- N-C1. Committer shape: the sweep's "2 searches, 1 complete, 1
  corrupt" is wrong. Staged: 7 files, 5 lanes, 1 complete (Copilot),
  6 unparseable (3 rate-limit 403s, 2 bad flags, 1 truncated).
- N-C2. Tango-zulu totals: code totals uncaptured as stated, but
  issue (103) and PR (121) totals are also header-only (20 sampled
  issue URLs, 0 PR URLs staged). HN "0 hits" is exact-phrase 0;
  token hits 6 and 9 are stemming noise.
- N-C3. HN caps: 20 of 36 summary values sit at the 300 cap, verified.
  But the summary values are Algolia token counts per the lane's own
  provenance note, not exact-substring counts, and no exact-count
  table is staged. Never cite a capped value as a total.
- N-C4. GH6 forms: "9 direct" holds for any spawn_agent string, not
  for dotted form alone. Verified split: dotted 7, flat 1, fused 2,
  envelope 3, tangential 1 with no spawn or collaboration string
  (item 7). A fourth form (concatenated, no separator) appears in
  items 6 and 9.
- N-C5. Tron timing: reply latency is 222 seconds (15:37:54 to
  15:41:36Z). The "8 minutes" figure is issue-to-reaction-comment.
  The kill still holds (User types, dictated template, no automation
  trace).
- N-C6. Linguist: 46 = 16 + 19 + 11 reconciles, but 37 mined rows
  include 2 pre-window background rows, so in-window mined = 35.
  The phrase-list splits were taken as lane-stated, not re-parsed
  by the verifier (prose list, not a machine table).
- N-C7. Saved-set ordering: the da.gd saved set is May-empty against
  a May-heavy full set, which alone defeats any recency-ordering
  claim for that file. The same caution applies to other capped
  files. Totals above 30 are unscreened beyond the saved rows.
- N-C8. HN1 file property: 48 posts from 48 authors in the hiring
  file, Oct 1 = 19, Oct 2 = 9. The cryptologist "6" is a
  contact-field occurrence count, never the cluster size.

## Kills and downgrades that stand

- GH2 Village multi-agent claim: KILL STANDS. Issue plus all 4
  comments come from 1 distinct account, all User type, including
  the "human instructor" voice. Two comments at 44 and 46 seconds
  fit pre-written pasting as well as independent arrival. The
  publication-verification step is demoted further: it appears only
  in the 4th comment by the same account, with no staged
  external-thread capture, workflow run, or fetch log. It is
  REPORTED, not OBSERVED, and survives only as a DISCUSSED hunt
  signature (a search pattern for future lanes), not a finding and
  not a watch item for this instance. Ranking would require a staged
  external capture plus fetch log (publication act alone) or distinct
  accounts and session traces (multi-agent claim).
- GH6 Codex grammar as TOI: CUT STANDS. All 10 items are tracker
  text about a feature, not wild acts. Repo spread verifies (7
  vendor-tracker, 1 fork, 1 guardrails repo, 1 gateway item with no
  spawn string). "Across independent reports" is an overclaim:
  reporter independence is NOT provable from staged bytes (no author
  field in the search file). The grammar survives only as a
  harness-fingerprint search signature. Flip conditions: the same
  grammar in a non-vendor wild artifact toward an external effect,
  the same contract in 2 or more independent trackers, or a staged
  wild run with a completed multi-agent effect.
- WATCH-01 tron handoff: KEEP AS WATCH. Promotion fails (dictated
  script, both User type, no workflow or commit trace staged).
  Cutting to nothing fails too. One distinction the first review
  missed: this is a two-account exchange (issue author vs replying
  account, distinct accounts), which is better than Village's
  single-account collapse, but repo collaborator status is a
  permission, not agency proof. Promotion condition, precise and
  testable: staged automation evidence for the replying side
  (timeline or events, commits, or workflow runs in the 15:37 to
  15:41 window, or account markers elsewhere). None staged, none
  assumed. A reply deviating from the dictated template would prove
  agency better than compliance does.
- WATCH-02 pursekeeper filing: KEEP AS WATCH. The maintainer closed
  the issue about 90 minutes after filing, reporting added entries
  and a prior chain cross-check of one payment-log entry. That
  corroborates the listed project and log (and even that only
  REPORTED, since no chain bytes are staged), not the filing act.
  No authorship-verification method is stated. Entries were added
  by the maintainer, not the filer. No bot or app marker or workflow
  trace is staged. "Acceptance implies trust in the agent" and
  "quick close implies automation" are both rejected. Surface known
  since August 2026; instance-new only.
- TOI-01: KEEP, low TOI, borderline, with the kill condition in M1.
  Disclosure unevenness must travel with every citation: the
  explicit "not a person" form appears in 2 of the sweep's 3, while
  the follow-ups lane reports explicit disclosure in all 9 on
  entity-decoded text. That wording difference is unresolved here.

## Negatives — confirmed or extended

- NEG-01 tango-zulu: honest zero for agent use, with its caveats.
  Exact phrase: 0 HN hits, 0 urlquery hits, empty Wayback CDX.
  GitHub code totals are uncaptured API totals with first-page-only
  spot checks. Factum exact match not_found. Legacy-tree grep killed
  incomplete. Bounded T/Z probe (this fleet): HN 4, 1, and 7 hits
  with 0 literal matches (all token stemming); urlquery agent
  20,996 and harness 20,070 totals, generic landing and spam shapes.
  No standalone T/Z search was run. The zero covers the searched
  forms, not every conceivable phonetic pattern. Never shorten it to
  "tango-zulu does not exist."
- NEG-02 committer accounts: PARTIAL negative, extended. Completed
  lanes now cover 90 commits with 5 bot-type authors from one
  account (see M2). The "no lane-wide negative" qualifier still
  holds: Codex, PR, and phrase lanes are unmeasured (0 rows, not
  0 bot-type). The Devin type-versus-is_bot disagreement (type Bot,
  is_bot false on the 5 rows) is recorded verbatim; counts here use
  type. Whether that disagreement affects the sweep's bot-count rule
  is an open question for the parent.
- NEG-03 iLands Reddit refusal: attempted, not established as
  successful posting. Unchanged by this fleet. Attempted-and-refused
  is a negative, not a finding.

## Pattern scores — cross-lane, never merged on a generic word

- Codex collaboration grammar: LINKAGE as a grammar cluster and
  fingerprint only, not behavior evidence.
- x402 mechanism family: WEAK-MODERATE, 2 legs only (pursekeeper
  facilitator plus agentbadge slug). The Show HN x402 title leg is
  STRUCK (pre-window, title-only, dead body). Zero shared
  identifiers across legs. Protocol family, not identity linkage.
- iLands platform family: PLATFORM FAMILY (HN posts plus Reddit
  refusal reports share platform and disclosure grammar; no shared
  identifier; the refusal leg is attempt evidence, not success).
- Village fetch-back versus tron handshake: COINCIDENCE, no linkage
  (verification versus acknowledgement, different mechanisms).
- Honeypot traps versus disclosure templates: SEPARATE FAMILIES.
- da.gd versus oai/zz: SEPARATE (0 zz and oai flags in 98 full-set
  rows; zz totals are substring noise).
- Village numbering versus iLands contacts: COINCIDENCE (different
  separator, domain, and surface).
- Delegation-disclosure: CANDIDATE PATTERN (see M7).

## Coverage limits and open questions

1. Legacy-tree grep is STILL incomplete (killed on large files in
   two lanes, then again in this fleet's scope). All NEW wordings
   stay provisional until it completes. No claim in this report
   carries NEW on a partial check.
2. Codex commit lane, both PR lanes, and the 20-phrase pass are
   UNMEASURED (rate guard). When to re-attempt, and at what pacing
   (longer than 30 seconds between starts, given this failure),
   is the parent's call. One open probe: whether the secondary-limit
   pressure is concurrent fleet search traffic or the Codex query
   itself. That needs one probe in a quiet window.
3. Follow-ups claims (M1 9 posts, seller list +2) are LANE-VERIFIED
   but NOT independently re-verified. Re-verify before outward use.
   Distinct-author count for the 9 posts is also open.
4. GH4 PR #42203 merge status after 2026-10-31, GH7 survivor
   comment and closure status, and the Village external-thread
   capture all need later windows if cited.
5. zz flagged-row full URL: the redirect-landing explanation rests
   on a transient re-fetch with nothing raw saved. A full-URL lookup
   would close it, if the parent wants it closed.
6. GH6 gateway-envelope instance (linguist seed rows) and linguist
   phrase-list splits were not re-parsed by the verifier. Cite them
   as lane-stated, not verifier-confirmed.
7. GH4 PR review associations are unstaged (see M6). Stage a reviews
   capture or soften the wording.
8. May 19 spike mechanism: does it share a mechanism with the June
   21 echo cluster, or is it a separate spike shape? The full-set
   rows are staged for a cryptologist comparison.
9. Seller-list composition change is unresolvable (no Oct 19 snapshot
   in sweep evidence). The maintainer's planned sellers-diff has no
   visible result yet; re-check on a later run.
10. The sweep's 86-versus-76 correction (B1) closes the staged-byte
    gap, but the sweep report text itself still carries the old
    numbers. Correct the sweep report text or carry this report's
    corrections alongside it at ship time.

## Evidence fidelity notes — read before ship

- Meta tree leak scan (verifier, shapes only, no values reproduced):
  clean. No credential-like value, wallet value, query-string value,
  or human-contact value appears in any meta FINDINGS file. The only
  values needing handling are API-returned emails and login strings
  inside raw captures, which are ordinary GitHub API capture content
  and must stay out of outward-facing artifacts.
- Follow-ups lane scrub conflict: the repo house rule says never
  redact raw evidence, but this fleet's brief forbade contact, wallet,
  token, and query-string values in files. The follow-ups lane
  followed the brief: its staged HN and Algolia captures are scrubbed
  derivatives (values replaced by shape markers, verified by grep),
  and the raw seller-list JSON plus raw log HTML were deliberately
  NOT staged (shape summaries only). If the parent wants originals
  retained, that needs a separate local-only decision. This lane did
  not store them anywhere. The coordinator does not silently accept
  scrubbed derivatives as full evidence: M1 rests on scrubbed
  captures plus the lane's live re-fetch account, which is one more
  reason M1 needs independent re-verification before outward use.
- Sweep raw tree presence note stands separately: the sweep commit
  was pushed as-is per the operator's explicit word. That decision
  does not transfer to this commit. This commit is staged only and
  unpushed; the parent decides its push.

## Files in this report dir

- REPORT.md (this file).
- MANIFEST.md — file list and curation notes.
- SHA256SUMS — hashes for the report dir files.
- adversarial-review.md — copy of the meta adversarial review.
- verifier-report.md — copy of the meta verifier report.
- Raw captures: data/lanes/sniffer-meta-20261031/raw/ (per-lane
  dirs: meta-analyst, cryptologist, committer-rerun, gh4-gh7,
  followups, uq-wayback, adversarial, verifier).
- Lane FINDINGS files live in their raw dirs, not duplicated here.

## Verifier verdict on this fleet

SHIP-WITH-FIXES. Most headline claims verify. Blocking fixes before
ship: B1 (GitHub totals), B2 (footer line counts), the Village grade
downgrade (section 4, M3), the WATCH-03 two-spike restatement (M4),
and the GH7 partition wording (M3). All five are applied in this
report. Non-blocking items (GH4 review associations, Codex sidecar,
Factum match legs taken as stated, follow-ups independent
verification, Codex and PR lanes unmeasured) are listed in section 6
and travel with the report.
