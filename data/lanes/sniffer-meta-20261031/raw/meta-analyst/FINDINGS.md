# Meta-analyst (linguist lane) — sniffer sweep 20261031 attack review

Date: 2026-10-31. Operator: BigSexyWarlock69. Lane: meta-analyst, linguist.
Scope: the sweep's own paper trail only. Passive reads only. No POST, no
login, no sessions, no Shodan. Package repos and Docker Hub out.
Window for new hits: November 2025 onward.
Grades: OBSERVED only for first-hand bytes. Default: SECONDARY.
No human poster handles, no signed values, no tokens, no query strings,
no wallet values appear below. Agent and bot account names appear only
as self-declared labels or counts, never as handles.
ANEC-01 (Reddit ban anecdote) was NOT touched, per brief. A separate
fleet handles it. No Factum writes were made. No commit or push was made;
the coordinator commits.

Sources re-read in full: reports/sniffer-sweep-20261031/REPORT.md,
hits.json, adversarial-review.md, verifier-report.md,
cryptologist-review.md. Staged raw re-checked: github, hn-forum,
urlquery-wayback, tango-zulu, committer-accounts, linguist lane files
listed in STATE.md.

## Verdict in one paragraph

The sweep's headline structure HOLDS: 1 TOI cluster, watch items, and
negatives, with most kills confirmed from staged bytes. The sweep's
numbers do NOT all hold. The headline arithmetic double-counts one item,
the adversarial count matches neither its own headings nor the headline,
the GitHub hit total cannot be re-derived from staged files, the
committer lane is described with the wrong shape, one Transluce zero is
a slice-scope error, and one Factum novelty leg is incomplete in a way
that changes its wording. None of these corrections promotes a cut item
on its own. Three re-triage targets deserve a second pass, ranked below.
The strongest new result is a novelty correction: the pursekeeper
surface IS present in Factum as a mentioned term, and da.gd IS present
in the full Transluce list. Both strengthen "surface-known" and
"family-known" rather than "new".

## 1. Corrections table — denominators and caps

Each row gives the sweep statement, the verified value, and the
corrected statement to use. "Verified" means re-derived from staged
files or from a fresh read-only check run for this review.

### C1. Headline and adversarial item counts — DOUBLE COUNT, BOTH WRONG

- Sweep statement (REPORT.md headline): 1 TOI + 1 anecdote + 3 watch +
  3 negatives + 12 cuts. Sum presented: 20 items.
- Sweep statement (adversarial-review.md): "Of 16 items" / "16 claims
  adjudicated".
- Verified: adversarial headings are 17 (GH1–GH7, HN1–HN3, RD1–RD3,
  UQ1, UQ2/UQ3/UQ4 as one heading, TZ, CM), covering 19 distinct items
  (UQ2, UQ3, UQ4 are 3 items under 1 heading). REPORT.md cut list has
  12 items: GH2, GH4, GH5, GH6, GH7, HN2, HN3, RD2, RD3, UQ2, UQ3, UQ4.
  NEG-03 is RD3, already inside the 12 cuts. GH7 is also assigned to
  the negatives and methodology appendix by adversarial fix 1, while
  already inside the 12 cuts.
- Corrected statement: 19 distinct adjudicated items = 1 TOI (TOI-01)
  + 1 anecdote (ANEC-01) + 3 watch (WATCH-01 to WATCH-03) + 12 cuts +
  2 further negatives (NEG-01 tango-zulu, NEG-02 committer slice).
  NEG-03 (RD3 refusal) is one of the 12 cuts, counted as a negative
  for placement, not as a 20th item. Never cite "16" or "20".

### C2. GitHub sweep totals — UNRECONCILED (+2, and one search short)

- Sweep statement: "12 issue searches + 2 code searches. 86 issue hits
  returned."
- Verified from staged files: 11 issue-search files (q01, q02, q03,
  q04, q05, q06, q07, q08, q09, q13, q14) holding 74 items in total
  (0 + 0 + 4 + 0 + 10 + 10 + 10 + 10 + 10 + 10 + 10). Code searches
  q10 and q11 hold 5 + 5 = 10 items. Staged search total: 84 items.
  No total_count field is staged (files are bare lists), so an
  API-total explanation cannot be checked from staged bytes.
- Corrected statement: staged GitHub search yield is 74 issue items
  across 11 issue-search files plus 10 code-search items (84 total).
  The "86 issue hits" and "12 issue searches" figures are
  unverifiable from staged bytes and must not be cited until the
  12th search and the +2 gap are identified. The "7 candidates ranked
  before review, 2 survive as watch" statement still holds (GH1–GH7;
  GH1 and GH3 as watch).

### C3. Committer lane shape — WRONG COUNT, WRONG FAILURE SHAPE

- Sweep statement (REPORT.md counts): "2 commit searches ran
  (1 complete, 1 corrupt). 30 usable records."
- Verified: 7 capture files across 5 lanes. Complete: 1 file
  (Copilot co-author slice: 30 commits, 17 distinct authors, all
  account type User, 30 of 30 carrying the co-author footer).
  Unparseable: 6 files (1 truncated JSON, the rest error pages or
  empty). Failure modes from staged error files: 3 secondary
  rate-limit 403s, 2 bad-flag CLI errors (unknown flag), 1 truncated
  capture. Failed lanes: Claude, Codex, Devin, and PR lanes.
- Corrected statement: Copilot slice only — 30 commits, 17 distinct
  authors, 0 bot-type authors. Four sibling lanes failed (3 rate
  limit, 2 bad flag across their files, plus 1 truncated capture).
  No lane-wide negative claim. "0 repeat-frequency findings" is
  ambiguous wording only: repeats exist arithmetically (30 commits
  over 17 authors) but no repeat-frequency anomaly finding was made.
  Re-run the failed lanes after the rate limit resets, with fixed
  flags, before any wider claim.

### C4. Tango-zulu totals — CODE TOTALS ARE NOT THE ONLY UNCAPPED ONES

- Sweep statement (NEG-01): "GitHub code totals are uncaptured API
  totals (tokenized 135,424; hyphen 17; concatenated 83; underscored
  21) with first-page-only spot checks." And: "Exact phrase: 0 HN
  hits, 0 urlquery hits, empty Wayback CDX."
- Verified: code totals are uncaptured, as stated. Issue and PR
  totals are ALSO header-only and were not flagged in NEG-01:
  103 issues and 121 PRs for the hyphen form, with only 20 sampled
  issue URLs staged and 0 PR URLs staged. HN counts-summary values
  are phrase 0, hyphen-token 6, concatenated-token 9: the "0 HN hits"
  is exact-phrase 0, while the 6 and 9 are Algolia stemming noise,
  not phrase hits. Urlquery 0/0/0 and Wayback empty replies verified
  as stated. Legacy-tree grep incomplete, as stated. No standalone
  paired-phonetic search, as stated.
- Corrected statement: tango-zulu is a bounded zero over searched
  forms. All GitHub totals (code 135,424 / 17 / 83 / 21; issues 103;
  PRs 121) are uncaptured or header-only totals, not URL-evidenced
  totals. HN exact-phrase hits: 0; HN token hits 6 + 9 are noise.
  Never shorten to "tango-zulu does not exist".

### C5. HN caps — CAP COUNT VERIFIED, BUT THE TABLE IS NOT EXACT COUNTS

- Sweep statement: "3 pages x 100 per phrase (cap 300 per phrase).
  Exact-substring counts are what this report uses; raw Algolia
  counts are token-inflated. 20 of 36 values hit the 300 cap."
- Verified: _summary.json has 36 keys; exactly 20 sit at 300. The
  20-at-cap count is correct. But the staged HN provenance note
  states _summary.json IS the per-phrase hit count of Algolia token
  matches, NOT exact-substring counts. No exact-substring count
  table is staged. The 2 extra token checks sit outside the 36:
  the da.gd extra file holds 0 items, the oai extra file holds 100
  items (one page, not a 3-page 300 cap).
- Corrected statement: 20 of 36 Algolia token-count values sit at
  the 300 retrieval cap; never cite a capped value as a total.
  Exact-substring filtered counts are claimed by method note but
  are not staged as a table, so they cannot be re-derived here.
  The 2 extra checks are not under the 3-page rule. Any future
  report must stage the exact-substring table or drop the claim
  that exact counts are what the report uses.

### C6. UQ1 (da.gd) saved sample — "TOP-30" ORDERING UNPROVEN (verifier counts verified)

- Sweep statement: "only 30 of 98 rows were saved" and "saved
  top-30". Verifier fix 1 describes the saved sample as "(June 24,
  July 5, Oct 1, zero May rows)" — read as counts, not dates.
- Verified from uq-odd-dagd-domain.json: total_hits 98, saved 30.
  Saved dates are June 12 (1), June 16 (1), June 18 (3),
  June 20 (1), June 21 (17), June 27 (1), July 1 (1), July 5 (1),
  July 13 (3), October 4 (1). Saved month counts: June 24 rows,
  July 5 rows, October 1 row, May 0 rows. The verifier's
  shorthand is therefore CORRECT as counts, and this review
  withdraws any date reading of it.
  Full-set month split (May 53, June 31, total May–June 84 of 98)
  comes from the verifier's live re-fetch, not from staged bytes.
  The saved set is June-heavy and May-empty, the opposite shape
  of the full set, so it cannot be assumed to be a recency-ordered
  top 30.
- Corrected statement: 30 of 98 saved; saved month counts June 24,
  July 5, October 1, May 0, with a June 21 cluster of 17 saved
  rows. The May–June 84-of-98 burst shape rests on the verifier's
  live month distribution, not on staged bytes. Do not call the
  saved set "top-30" without establishing its ordering rule.

### C7. GH6 grammar precision — "9 DIRECT" HOLDS FOR spawn_agent, NOT FOR DOTTED FORM

- Sweep statement (verifier fix 2, applied in REPORT.md): "9 of 10
  bodies carry the spawn_agent bug text" / "Cite 9 direct + 1
  tangential, not 10."
- Verified from q05-collab-spawn.json (10 items): dotted form
  collaboration.spawn_agent in 7 bodies; flat form
  collaboration__spawn_agent in 1 body; fused form
  collaborationspawn_agent in 2 bodies; any spawn_agent string in
  9 bodies; no spawn_agent and no collaboration string in 1 body
  (the gateway item). Namespace-plus-spawn_agent co-occurrence
  (envelope shape family) appears in 3 bodies.
- Corrected statement: 9 of 10 carry a spawn_agent grammar form
  (7 dotted, 1 flat, 2 fused, with overlap counted once per body
  for the 9 total; envelope co-occurrence in 3), plus 1 tangential
  gateway item with no spawn_agent string. Cite "9 grammar + 1
  tangential" for the grammar cluster, never "9 dotted". The
  cluster itself is real (see section 3, Codex grammar).

### C8. WATCH-01 timing — ADVERSARIAL "8 MINUTES TO REPLY" IS WRONG

- Sweep statement (adversarial-review.md, GH1): "The exchange is
  8 minutes from issue to reply, then a one-word reaction comment."
- Verified from staged tron files: issue created 2026-10-30
  15:37:54Z; handoff reply 15:41:36Z (222 seconds, 3 minutes
  42 seconds); reaction comment 15:45:39Z (465 seconds after the
  issue, 7 minutes 45 seconds, about 8 minutes).
- Corrected statement: handoff reply latency is 222 seconds, not
  8 minutes. The 8-minute span is issue-to-reaction-comment. The
  correction does not rescue the kill: both accounts are User
  type, the reply follows a dictated template, and no automation
  trace is staged. But latency evidence must be cited as 222
  seconds. A 222-second templated reply fits a watching human
  just as well as an agent, so latency alone flips nothing.

### C9. Transluce "36 mentions" and "da.gd 0" — BREADTH ERROR AND SLICE ERROR

- Sweep statement (REPORT.md coverage item 4): Transluce snapshot
  (2026-10-31): "ilands" 36 mentions, "pursekeeper" 1, "village" 0,
  "handoff" 0, "beno" 0, "da.gd" 0, "tango" 0.
- Verified: full list (findings-list.json, total 140, identical
  to the 2026-10-30 snapshot file) gives ilands 36 occurrences in
  1 finding, pursekeeper 1 occurrence in 1 finding, village 0
  findings, handoff 0 findings, beno 0 findings, tango 0 findings,
  da.gd 5 occurrences in 2 findings. The 2026-10-31 slice file
  (25 items, offset 0, findings 183–210 window in its name) gives
  da.gd 0 findings — that is the only scope in which "da.gd 0"
  is true, and it is not the full tracker list.
- Corrected statement: Transluce full list (140 findings):
  ilands 36 occurrences in 1 finding (occurrence count, not
  breadth); pursekeeper 1 finding; da.gd 2 findings, 5
  occurrences (prior family material, not the May–June burst —
  see section 4); handoff, village, beno, tango 0 findings.
  Never cite "36 mentions" without "in 1 finding". Never cite
  "da.gd 0" without "slice only"; the full-list value is 2
  findings.

### C10. Linguist mined count — 2 PRE-WINDOW ROWS INSIDE THE 37

- Sweep statement (REPORT.md counts): "Linguist: 46 phrase rows
  (16 + 19 + 11). Searchable: 45. Mined with a cited URL: 37.
  Seed, no instance yet: 8. Category only: 1."
- Verified from phrase-list.md: 46 = 16 + 19 + 11; searchable 45
  (46 minus 1 category row); mined 37; seed 8; category 1. All
  reconcile. But 2 of the 37 mined rows are pre-window background
  (2025-10-28 vendor changelog rows), marked as such in the
  phrase list itself.
- Corrected statement: mined with a cited URL 37, of which
  in-window mined 35 and pre-window background 2. The 2 background
  rows are usable as sweep strings only, never as new-window
  evidence.

### C11. HN1 48-vs-3 — CORRECTION VERIFIED, WITH TWO COUNT CLARIFICATIONS

- Sweep statement (REPORT.md TOI-01): "The HN lane first claimed
  8 posts. The verifier re-fetched 3 IDs and confirmed exactly 3.
  The 48-entry hiring file holds 48 candidates, not 48 platform
  posts. This report uses 3."
- Verified: hiring file holds 48 posts from 48 distinct authors,
  dated 2026-10-01 to 2026-10-15, with date clusters October 1 (19)
  and October 2 (9). The 3 verified post IDs carry dates
  October 1, October 6, October 12, from 3 distinct authors.
  Cryptologist contact note (domain string 6 times in contact
  fields, 3 distinct contact patterns) is a contact-pattern
  count, not a post count; the hiring file holds 8 case-insensitive
  occurrences of the platform string in total.
- Corrected statement: TOI-01 is 3 posts, 3 distinct authors,
  October 1 / 6 / 12. Never cite 48, 8, or 6 as the cluster size.
  The 48 is the file size, the 8 was the lane's first claim, the
  6 is a contact-field occurrence count.

### C12. Hash coverage — VERIFIER STALENESS, NOT A REPORT ERROR

- Sweep statement (verifier-report.md): 107 unique hash entries
  verified, 0 failures; 3 lane dirs uncovered (github,
  committer-accounts, linguist).
- Verified: per-file sidecars now exist in raw for all three
  lanes (github 24 per-file sidecars, committer-accounts 14,
  linguist phrase-list sidecar), and REPORT.md open item 6 plus
  MANIFEST.md already record the curation fix.
- Corrected statement: quote the verifier's "uncovered" line only
  with its curation fix attached. No hash failure was found by
  this review; hashes were not re-run here because the claim
  concerns report-dir integrity, not sweep conclusions.

### C13. UQ totals above 30 — "RECENCY SAMPLE" QUALIFIER UNPROVEN

- Sweep statement (REPORT.md counts): "Totals above 30 are
  unscreened beyond a recency sample."
- Verified: zz-parameter total 2,593,629 with 30 saved, 0 flagged
  in saved rows; zz-plus-agent conjunction total 68,265 with 30
  saved; oai-tag total 9,945 with 30 saved, 0 flagged; tag-based
  oai search total 0. The da.gd saved set is demonstrably not
  recency-ordered (May-empty, June-heavy against a May-heavy
  full set), so a recency-sample description cannot be assumed
  for other queries either.
- Corrected statement: totals above 30 are unscreened beyond the
  saved 30 rows; the saved rows' ordering rule is unstated and,
  for da.gd, is not recency. Do not describe any saved set as a
  recency sample without its ordering rule.

## 2. Ranked re-triage list — weak kills most deserving of a second pass

Rank order is by flip value: how much a single piece of missing
evidence would change the grade. Each entry states the flip evidence
and the exploitation lane that should chase it. No item below is
promoted by this review. All start from their sweep grade.

### R1. GH7 non-trap entries — HIGHEST FLIP VALUE (3 items, not 1)

Sweep grade: CUT to methodology note, with non-trap entries flagged
for separate re-triage (already an open follow-up). This review
splits the 10-item q06 file as: 3 trap or template items (checkbox
trap, bare sentence, fill-in template), 1 unchecked attestation
template (checkbox text, box unticked in staged body — template,
not an act), 1 product-description item (agent string inside a
product blurb — DISCUSSED, not an act), 1 registration-form item
(disclosure template plus a barred wallet-shape value —
methodology note only), 1 duplicate (Village launch note, same
single-account experiment as GH2 — must never double-count),
and 3 genuine re-triage candidates:

- (a) Licence question filed as an agent acting on behalf of a
  named principal who explicitly approved posting. A real filing
  with a delegation claim and an approval claim.
- (b) AI-authored message for a named principal, tied to a
  specific versioned backport request and an existing PR. A real
  filing with a checkable work object.
- (c) Bounty-work disclosure: an agent doing bounty work for an
  operator. A claimed economic act, not a product description.

Flip evidence (any one promotes to REPORTED watch; two together
with an automation trace promote toward TOI): account type Bot or
App for the filer; a workflow run, commit trace, or PR authorship
record tying the filing act to an agent account; maintainer
acceptance or merge of the filed work; a bounty payout or merged
work record for (c); a second filing by the same delegation shape
in a different repo (repetition beats single self-assertion).
Kill evidence (confirms CUT): filer account shown as a human
operator's account with no automation trace, or the filing text
shown to be pasted by a human (but human-identity pursuit is out
of scope — the kill must come from account-type and automation
evidence, not from identifying the operator).
Exploitation lane: GitHub filing and authorship lane (account-type
plus automation-trace checks on the 3 candidates, in that order:
licence filing, backport message, bounty disclosure). Do NOT chase
the trap, template, product, registration, or duplicate items as
acts.

### R2. GH6 Codex grammar as a wild fingerprint — GRAMMAR VALID, QA GRADE HOLDS

Sweep grade: CUT to DISCUSSED product QA. Cryptologist rank: #2
grammar cluster. This review agrees with both, with one upgrade
to the grammar's value: the grammar is corroborated across vendors,
not just inside one tracker. The linguist seed rows cite the
envelope form (namespace plus name) from a gateway vendor issue
outside the 10 staged GH6 items, while GH6's 10 items sit mostly
in a coding-product tracker. Dotted, flat, and envelope forms of
the same namespaced spawn tool therefore recur across independent
vendor trackers. That validates the fingerprint. It does not
validate a wild act: every staged instance is still tracker text
about a feature, not an agent using the tool in the wild.
Flip evidence: one occurrence of the dotted, flat, or envelope
spawn_agent form in a wild surface outside issue trackers — an
agent's own repo log, a transcript dump, urlquery page content
(not a search-result projection), or an HN exact-substring hit
with agent context. That single wild occurrence graduates the
grammar from QA context to wild marker. It does not alone make a
TOI; the wild occurrence still needs an attached act.
Exploitation lane: wild-surface grammar lane (exact-form search
for all three forms outside vendor trackers, with page bytes, not
projections). Also re-check the cryptologist's unresolved
zz-plus-agent flagged-row discrepancy (file-level count 1 flagged
vs 0 flagged in saved rows) before any zz claim is made from
that file — do not claim a zz instance from it.

### R3. GH2 Village beacon shape — DISTINCTIVE SHAPE, FATAL ACCOUNT FLAW

Sweep grade: CUT to DISCUSSED. Cryptologist rank: #3 beacon shape
(post, then fetch back, require two strings, report success).
This review lowers the beacon's standing further than the
cryptologist did, on two staged facts. First, the single-account
collapse is total: issue plus all 4 comments come from 1 distinct
account, all User type, including the comment that plays the
human instructor. Second, the external-publication step was
human-instructed inside the same thread: an instruction comment
to post externally precedes the publication update. The fetch-back
step is therefore self-reported by the same account that staged
both sides, after an explicit instruction to publish. That is
prompt compliance plus self-report, not an independent beacon.
Flip evidence (all required, not one): a second, distinct account
(Bot or App type, or a second operator account with its own
automation trace) performing the fetch-back check; or workflow
run logs for the fetch-back step; plus a publication step not
preceded by an in-thread instruction to publish. Without that,
the shape stays a case study in single-account multi-persona
experiments, exactly as the adversarial review requires.
Exploitation lane: publication-verification lane (search for the
same post-then-fetch-back-plus-required-string shape with 2 or
more distinct accounts). Never cite the Village launch note in
the q06 file as a second instance — it is the same experiment.

### R4. WATCH-01 tron scripted reply — WATCH IS CORRECT, FLIP IS A SECOND INSTANCE

Sweep grade: REPORTED watch, not a TOI. This review confirms the
downgrade (User-type accounts, dictated template, 222-second
reply, no automation trace, second comment is a one-word reaction,
not a second handoff). The item's value is as a template: it
defines a searchable handshake shape (fixed acknowledgement plus
represented person plus model name) that a future wild instance
can be matched against.
Flip evidence, in order of strength: (1) a second handoff reply
in the same fixed shape in a different issue or repo, by a
different account pair — repetition across accounts beats one
scripted reply; (2) a Bot or App account marker, workflow run, or
commit trace for the replying side; (3) a reply that deviates
from the dictated template while still completing the handoff —
deviation proves agency better than compliance does. Note the
novelty legs now closed by this review (section 4): Factum exact
0, Transluce full-list 0 findings. A genuine second instance
would therefore be new on both legs, subject only to the still
incomplete legacy-tree grep.
Exploitation lane: handoff-template lane (search the fixed
acknowledgement shape across GitHub issues, with account-type
and automation checks attached to every hit).

### R5. HN1 TOI-strength — TOI HOLDS AT LOW RANK, IDENTITY STAYS SECONDARY

Sweep grade: low-rank TOI cluster, 3 posts, OBSERVED posts with
SECONDARY identity, new instances of a known phenomenon. This
review confirms the posts (3 IDs, 3 distinct authors, October 1 /
6 / 12, in-window, hiring-thread template plus platform contact
grammar plus agent disclosure). Nothing in staged bytes proves
the posters are agents rather than humans marketing agent
services, and the phenomenon is known since September 2026.
Flip UP (strengthen toward a stronger TOI): platform-side or
self-text corroboration that a poster operates as an agent —
a platform agent profile or agent-card, repeat agent posts
across boards under the same platform contact pattern, or a
payment or log record tied to a hiring post. Flip DOWN (kill the
TOI, keep the posts as DISCUSSED marketing): platform-side or
self-text evidence that the posts are human-operated storefronts
(for example, a post's own text admitting human operation, or
platform terms showing human-operated listings). Human-identity
investigation is out of scope, so the down-flip path is limited
to platform and self-text evidence. Do not pursue poster identity
through personal channels.
Exploitation lane: iLands identity-corroboration lane (platform
surface and cross-board repetition only, no human identity work).

### R6. GH7 remainder and GH4 — EXPLICIT NON-CANDIDATES (do not re-admit)

- GH7 checkbox trap, bare sentence, fill-in template, unchecked
  attestation template: trap and template family. No follow-through
  is staged. Do not re-triage as acts.
- GH7 product-description item and registration-form item:
  DISCUSSED surface and disclosure template. The registration
  form carries a barred wallet-shape value; methodology note only.
- GH7 Village launch note: duplicate of GH2. Never count twice.
- GH4 identity-leak report: excerpt-only, product QA. Full-issue
  pull is already open follow-up (e). Flip would require a full
  body showing an agent act rather than a misrouted system
  sentence. Expected outcome on pull: product-bug appendix at
  most. Lowest priority in this list.

## 3. Cross-lane pattern scores

Rule applied throughout: a shared generic word is never a linkage.
Each pattern names its shared shape and is scored as LINKAGE
(shared identifier or contract), MECHANISM FAMILY (shared protocol
or mechanism, no shared identifier), PLATFORM FAMILY (shared
platform plus disclosure grammar, no shared identifier),
CANDIDATE PATTERN (recurring shape, needs more instances), or
COINCIDENCE (generic overlap only, never merge).

### P1. Codex collaboration grammar — LINKAGE (grammar cluster, fingerprint only)

Shared shape: the namespaced multi-agent tool contract itself —
dotted form, flat form, and JSON envelope form (namespace plus
name) for the same spawn tool, plus companion wait and send
tools, across independent vendor-tracker reports (coding-product
tracker items plus a gateway vendor envelope instance from the
linguist seed rows). This is the sweep's strongest grammar
linkage. Scope limit: it links reports to each other as instances
of one harness fingerprint. It does not link any report to a wild
agent act, to da.gd, to oai/zz, to iLands, or to x402. No external
family shares it. Use it as a search fingerprint (see R2), never
as behavior evidence on its own.

### P2. x402 mechanism family — MECHANISM FAMILY (weak-moderate, 2 legs)

Shared shape: the x402 micropayment mechanism — a keyless
verify/settle facilitator plus a public payment log (pursekeeper
filing), and an x402-bazaar blog slug (agentbadge discovery
surface). The Show HN x402 title leg is STRUCK from this family:
it is pre-window (2026-03-09), title-only, body dead, and cannot
carry weight. The honeypot q06 wallet-shape item and the
registration-form wallet shape sit in the same payment-identity
neighbourhood but share no identifier, endpoint, wallet, or price
with the pursekeeper listing, so they add mechanism context only.
Score: mechanism family, not identity linkage. Two live legs
(pursekeeper facilitator, agentbadge slug), one struck leg
(Show HN title), zero shared identifiers. Do not cite this family
as 3 sightings; cite it as 2, one of them slug-only.

### P3. iLands platform family — PLATFORM FAMILY (moderate)

Shared shape: the platform name plus agent disclosure plus an
external-surface attempt — HN hiring posts (numbered platform
contacts plus disclosure plus hiring template) and Reddit refusal
reports (same platform plus disclosure plus attempted external
posting, refused for IP and account-age reasons per the author's
own conclusion). The September precedent article and discussion
thread establish the phenomenon's age. No contact value, IP value,
or identifier is shared across the legs in verified form, and
the refusal reports are attempt evidence, not success evidence.
Score: platform family, not identity linkage. The refusal leg
corroborates platform activity; it does not corroborate the
hiring posts' agent identity. Keep NEG-03 labelled as a negative
while using it as family context — both labels are true at once.

### P4. Village fetch-back vs tron handshake — COINCIDENCE (no linkage)

Shared shape claimed: agents labelling themselves and following
a template. That is generic. The mechanisms differ: Village is
post-then-fetch-back plus required-string verification, self-
reported by one account after an in-thread instruction to
publish. Tron is a fixed three-part acknowledgement reply to a
dictated template, 222 seconds later, with no fetch-back, no
publication step, and no verification step. Different surfaces,
different account structures, different mechanisms. The
cryptologist already scored Village as standalone and tron as
weak; this review strengthens that to an explicit non-linkage.
Never merge them, and never cite their shared self-labelling as
a linkage.

### P5. Honeypot traps vs disclosure templates — SEPARATE FAMILIES (do not merge)

Trap family: checkbox tick template, fill-in template, bare
self-disclosure sentence, unchecked attestation checkbox. These
are human-authored lures. A trap catching nothing proves a human
anticipated agents, not that agents acted.
Disclosure family: iLands disclosure plus hiring template,
tron three-part reply, Village agent-number labels, GH7
licence/backport/bounty self-disclosures. These are agent-side
(or agent-claimed) labels attached to filings and posts.
Shared element: the sentence "I am an AI agent". That sentence
alone is generic and must never merge the families. Ranking a
trap as a disclosure, or a disclosure as a trap catch, inverts
the evidence in both directions.

### P6. Delegation-disclosure sub-grammar — CANDIDATE PATTERN (needs more instances)

Shared shape, found by this review across lanes: an agent-claimed
filing or message that names a principal and asserts approval or
representation — the licence filing ("acting on behalf of" plus
explicit approval), the backport message ("AI-authored message"
plus a named principal), the pursekeeper filing sentence (filed
by the agent itself), and the tron delegation protocol ("on
behalf of" plus model name plus fixed acknowledgement). This
shape is narrower than generic self-disclosure and is worth
tracking as its own pattern: delegation claim plus principal
plus approval or representation. It is not yet a linkage: the
principals differ, the surfaces differ, and every instance rests
on self-assertion without an automation trace. Exploitation lane:
search the delegation-disclosure shape (on-behalf plus approval
language) in wild filings, with account-type checks on every hit.
If 3 or more independent instances with automation traces emerge,
promote this to a mechanism family.

### P7. Village agent-number labels vs iLands numbered contacts — COINCIDENCE

Different separator, different domain, different surface.
Village numbering is experiment-internal (agent-01 to agent-04
labels in one repo, one account). iLands numbering is a platform
contact namespace (given-name token, hyphen, 3-digit number, at a
platform domain) across 3 distinct hiring posts. The cryptologist
non-linkage stands. Never merge on numbering alone.

### P8. da.gd vs oai/zz — COINCIDENCE IF MERGED (families stay separate)

Zero zz-parameter flags and zero oai-token flags in all 30 saved
da.gd rows. zz search totals are substring noise (2,593,629 total
for the zz-parameter query, 30 saved, 0 flagged in saved rows;
conjunction total 68,265, 30 saved). oai-tag total 9,945, 30 saved,
0 flagged; tag-based oai search total 0. The da.gd burst's echo
shapes (short-code reuse, echo-host base64 path shapes, START
marker pages, 8 resolutions in about 2 minutes on June 21) repeat
identically across rows, which fits a framing or echo probe, not
a per-message secret, and the staged titles truncate the base64
segments so no full decode is possible from staged bytes. No
new-window zz, oai, or epoch marker was corroborated by this
sweep. Keep da.gd and oai/zz as separate families, always.

## 4. Novelty-gap table — read-only checks run for this review

Method: Factum match in exact mode and fuzzy mode, read-only, no
writes; Transluce snapshot greps over the full list and the
2026-10-31 slice. No DB lock blocked any check. Factum state at
check time: commit e234a7a0162bbec82ce868a6ded9a7fbb9ac238e,
coverage "Structured Factum records; excludes unimported files
and live sources", 1 pending batch (not mine, untouched).
Fuzzy payloads truncate at 25 matches: every fuzzy "25" below
is a cap, not a total. Exact "not_found" payloads were not
truncated (0 matches). Legacy-tree grep remains incomplete
(killed in the sweep), so no term below reaches confirmed NEW
under the house novelty rule, which requires the Factum leg,
the legacy-corpus leg, the Transluce leg, and the lists leg.
Transluce scope is stated per row because the slice/full
distinction changed one result.

### N1. "handoff received" — Transluce gap CLOSED as negative; exact novelty stands

- Factum exact: not_found, 0 matches, not truncated. Confirms
  REPORT.md.
- Factum fuzzy: status found, 25 matches in payload (truncated).
  0 of the 25 contain the contiguous phrase "handoff received"
  in value text or in the full match record. The fuzzy hits are
  token noise (the words "handoff" and "received" separately).
  Fuzzy "found" here is NOT corroboration.
- Transluce full list (140 findings): 0 findings, 0 occurrences
  for "handoff received" and for "handoff" alone. This check was
  listed as not run in REPORT.md; it is now run, and the result
  is negative.
- Transluce 2026-10-31 slice (25 items): 0 findings.
- Effect on WATCH-01: Transluce leg closes as a negative. Exact
  novelty stands. Full NEW remains blocked only by the incomplete
  legacy-tree grep. Correct novelty wording: "Factum exact
  not_found; Transluce full-list 0 findings; fuzzy hits are token
  noise only; legacy-corpus leg incomplete, so NEW is provisional,
  not confirmed."

### N2. "pursekeeper" — CORRECTION: surface IS in Factum as a mentioned term

- Factum exact: not_found, 0 matches, not truncated. Confirms
  REPORT.md's exact-mode statement, but exact mode matches whole
  values, so it does not mean the term is absent from Factum.
- Factum fuzzy: status found, 25 matches in payload (truncated).
  4 of the 25 have values containing the token "pursekeeper".
  The top value describes the pursekeeper project publishing an
  offer on its own offers page (section 1), in a record of type
  infra.message in lane 2026-08-19-tantive-space (record id
  observation_212f920ef16f42cd9280d80ee8f8adb6). A second value
  in the same lane repeats the offers-page reference. A third
  value, in lane transluce-intel (record id
  observation_da783c30a54049888e9eee4a5fa3f1dc), cites a
  pursekeeper API issue reference among other links.
- Transluce full list: 1 finding, 1 occurrence. Confirms
  REPORT.md's "pursekeeper 1". Transluce slice: 1 finding,
  1 occurrence (same finding sits in the first 25 items).
- Effect on WATCH-02: the sweep's "exact not_found, but surface
  known via August 2026 baseline and lists" wording is incomplete.
  Correct wording: "Factum exact-value not_found, but fuzzy token
  present in 4 or more prior records (offers page, API issue
  reference); Transluce 1 finding; surface known." WATCH-02 stays
  instance-new and surface-known. The correction strengthens
  surface-known; it neither promotes nor kills the watch item.
  It does mean the sweep's Factum leg must not be quoted as
  "pursekeeper absent from Factum" — that sentence is false in
  the token sense.

### N3. "da.gd" — CORRECTION: Transluce full list has 2 findings, not 0

- Factum exact: found, 25 matches in payload (truncated — 25 is
  a cap, not a total). Matches are infra.shortcut and
  infra.proxy_chain records, mostly in lane da-gd-shortener.
  Confirms REPORT.md's "found" direction; corrects its count
  reading: never cite "25 matches" as a total.
- Factum fuzzy: returns the same 25 exact matches in payload
  (mode collapse for this token: the value equals the token).
- Transluce full list (140 findings): 2 findings, 5 occurrences.
  Finding 122 describes a bootstrapping script using da.gd
  shortened URLs to load program pieces. Finding 146 lists da.gd
  among relay services in a campaign relay chain. Neither finding
  is the May–June 2026 urlquery burst, and neither mentions the
  burst's echo shapes or short codes.
- Transluce 2026-10-31 slice (25 items): 0 findings. This is the
  only scope in which REPORT.md's "da.gd 0" is true.
- Effect on WATCH-03: REPORT.md's Transluce "da.gd 0" is a
  slice-scope error. Correct wording: "Factum exact found
  (25-plus records, payload-capped); Transluce full list 2
  findings of prior family material; burst itself unestablished
  as filed vs new." The correction strengthens "family known"
  and leaves the burst question open. Open exploitation task
  (read-only): compare the burst's 6 distinct June short codes
  against the filed da-gd-shortener lane's short codes. A code
  match would file the burst under the known family; no match
  would keep it as an unfiled burst shape. That comparison was
  not run here because it needs the full 98-row pull, not the
  saved 30.

### Novelty gaps that remain open after this review

- Legacy-tree grep: still incomplete (killed in the sweep, in
  two lanes). Every NEW or provisional-NEW wording above stays
  provisional until that leg completes. Do not upgrade any item
  to confirmed NEW on Factum plus Transluce alone.
- ANEC-01 novelty legs: untouched per brief (its Factum fuzzy
  and Transluce checks were already listed as not run).
- WATCH-03 full-98 pull: still needed to settle whether the
  May–June burst is already filed under the known da.gd family.
- Lists leg for the 3 terms: not re-run here; the sweep's
  lists and reports greps are taken as stated for WATCH-01 and
  WATCH-02, and the pursekeeper lists presence is already
  established by the sweep (baseline plus lists entry).

## 5. What holds after attack

- TOI-01 holds at low rank: 3 posts, 3 distinct authors, October
  1 / 6 / 12, verified post bytes, SECONDARY identity, new
  instances of a known phenomenon. The 48-vs-3 correction is
  verified and must stay attached to every citation.
- GH2 kill holds and strengthens: 1 distinct account across
  issue plus 4 comments, all User type, plus an in-thread
  instruction to publish before the publication update.
- GH1 and GH3 downgrades hold: User-type accounts, dictated or
  self-asserted text, no automation trace staged.
- WATCH-03 sampling warning holds and strengthens: saved 30 is
  May-empty against a May-heavy full set; the June 21 cluster of
  17 is a saved-subset property until the full 98 are pulled.
- TZ bounded zero holds with expanded caveats (section C4).
- CM partial negative holds for the Copilot slice only (30
  commits, 17 authors, all User, 30 footers verified).
- Cryptologist family separations hold: da.gd is not oai/zz;
  Village numbering is not iLands numbering; traps are not acts.
  The x402 family loses one leg (Show HN title struck) but
  survives as a 2-leg mechanism family.
- Adversarial grade discipline holds: DISCUSSED and REPORTED
  material must not be briefed alongside OBSERVED material as
  the same class. The only OBSERVED-behavior content at TOI
  strength remains HN1's 3 posts, with identity SECONDARY.

## 6. Failures and open questions from this review

- No live re-fetch was run (passive reads only, per brief). The
  da.gd May 53 / June 31 split is taken from the verifier's live
  call, not re-verified here. The tron and Village timestamps are
  from staged files, not live re-checks.
- The GitHub "86 issue hits / 12 searches" gap (C2) is
  unreconciled: no 12th search file and no +2 source was found
  in staged bytes. The coordinator should identify them or
  correct the figure to the staged 74 / 11.
- The HN exact-substring count table is unstaged (C5). Either
  stage it or soften the "exact counts are what this report
  uses" claim.
- The zz-plus-agent flagged-row discrepancy (file-level count 1
  flagged vs 0 flagged in saved rows) is unresolved. Do not claim
  a zz instance from that file.
- ANEC-01, Reddit live verification, the dev.to escrow capture
  decision, and the committer re-run remain open from REPORT.md
  and are untouched here.
- No new TOI is proposed by this review. The re-triage list in
  section 2 is a second-pass queue, not a promotion list.

## Evidence paths

- Sweep report dir: reports/sniffer-sweep-20261031/REPORT.md,
  hits.json, adversarial-review.md, verifier-report.md,
  cryptologist-review.md.
- Staged raw re-checked: data/lanes/sniffer-sweep-20261031/raw/
  github/q05-collab-spawn.json, q06-i-am-ai-agent.json,
  q06c-village-issue1-full.json, q06d-village-issue1-comments.json,
  q09e-tron-issue1-full.json, q09f-tron-issue1-comments.json,
  q03c-pursekeeper-issue8-comments.json; hn-forum/_summary.json,
  hn_oct-hiring_candidates.json, hn_ilands_ilands.json,
  hn_extra_da_gd.json, hn_extra_oai.json, .PROVENANCE.txt;
  urlquery-wayback/uq-odd-dagd-domain.json, uq-summary.json,
  sweep-results.json; tango-zulu/counts-summary.json,
  github-issues-prs.txt; committer-accounts/gh-commits-*.json,
  err-*.txt; linguist/phrase-list.md.
- Transluce snapshots grepped: data/lanes/2026-10-09-transluce-intel/
  raw/findings-list.json (full list, total 140) and
  findings-list_25_183-210_20261031T115745Z.json (25-item slice).
- Factum checks: read-only match, exact and fuzzy, for
  "handoff received", "pursekeeper", "da.gd" (see STATE.md for
  payload counts and record ids).
