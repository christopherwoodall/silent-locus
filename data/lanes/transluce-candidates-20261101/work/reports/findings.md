# Transluce candidate audit — findings log, 2026-11-01

Scout worker, local reports lane. Read-only except for this directory.
No filing, no Transluce contact, no commit, no push. No sessions, no
logins, no posts. No external lookups were run for overlap; local
snapshots and the source reports' own novelty notes are cited instead.

Lane brief read first:
`.agents/workers/behavioral-analyst.md` (provider attribution:
shortener tradecraft is one provider family, grammar markers are
another; never conflate; mark uncertain attribution as inference).

Method: each listed report was read in full or, for the two longest
files, in full for ranked sections plus headings, novelty, and
coverage sections. Items were kept only if they are a behaviour, a
tactic, or an incident shape. Dataset inventories, surface baselines,
talk without an act, and product bugs were rejected even when
interesting. Grades follow the brief: PRIMARY (first-hand bytes),
SECONDARY (cited report), REPORTED (single self-report).

The clean candidate list is in candidates.md in this same directory.
This file is the audit trail: what was reviewed, what was rejected
and why, and what is still open.

## Reports reviewed

- reports/sniffer-sweep-20261031/REPORT.md (19 adjudicated items)
- reports/sniffer-meta-20261031/REPORT.md (8 ranked items, plus
  corrections and pattern scores)
- reports/anec01-rundown-20261031/REPORT.md (1 anecdote, fully
  investigated)
- reports/continuous-hunt-20261031/REPORT.md (16 documented items,
  7 honest nulls)
- reports/aiid-full-site/INGEST-REPORT.md, IOC-REPORT.md,
  HUNT-INDEX.json (1,777 incidents; 122 hunt-relevant by the index rule)
- reports/agent-bypass-forum-hunt/REPORT.md (21 REPORTED acts,
  4 DISCUSSED, 9 mechanisms, plus appendix and kills)
- reports/incident-7050-antigravity/REPORT.md (E1–E5, mechanism
  analysis, sibling appendix)
- reports/github-coding-agent-antics-best-of.md (6 ranked entries,
  plus killed false positives)
- reports/rubygems-july-spike-review/REPORT.md (533-row dashboard
  export review)
- reports/cohere-qwen-hunt/REPORT.md (3 ranked hits, appendices,
  triaged-out set)
- reports/cohere-qwen-enrichment/REPORT.md (335 entity rows, behaviour
  map, 8 third-party leads)
- Prior drafts (context only, not resubmitted as-is):
  reports/fruitshell-submission-draft.md,
  reports/transluce-draft-01-oct14-beacon-session.md,
  reports/transluce-draft-02-ntfy-monitoring-gap.md,
  reports/b11-msgboard-behavior-draft-2026-10-23.md,
  reports/b13-beeline-investigation-2026-10-23.md,
  reports/b17-agent-community-behavior-draft-2026-10-23.md

## Candidates kept (26)

See candidates.md for the full list with evidence paths and
Transluce-care lines. In short: C01 hiring posts; C02 handoff test;
C03 self-filed listing; C04 delegated filings; C05 delegation-
disclosure pattern; C06 short-link day spikes; C07 destructive
targeting class; C08 production-database deletion; C09 production
infrastructure/database deletions; C10 monitoring suppression;
C11 DNS-gap chatbot reach; C12 approval forgery; C13 compaction
provenance failure; C14 planted instruction file; C15 monitor
misclassification; C16 approval-guard cluster; C17 threat-actor
agent-use cluster; C18 evaluation escapes; C19 lab-rig injection
demo (lowest rank); C20 recalled proxy URL with no traffic;
C21 sandbox probe upload trace; C22 side-field beacon;
C23 scripted recruitment burst plus agent market; C24 skill-update
channel; C25 anti-analysis marker iteration plus wild mutation;
C26 post-window beacon session with contradicting egress.

Strongest three, by evidence: C01 (live-verified posts), C07
(first-hand issue reports across products), C22 (first-hand board
bytes with a hidden payload). Weakest kept: C19 (press demo with
oversight) and C26 (attribution contradicted). Both are kept with
their limits stated, not padded into stronger claims.

## Rejected items

### Sniffer sweep and meta — rejected
- Single-account multi-agent claim (village experiment): REJECT.
  One account posted as all personas and as the instructor. No
  independent agents evidenced.
- Codex collaboration grammar across tracker issues: REJECT as a
  behaviour. Tracker text about a feature, not wild acts. Kept only
  as a search signature, which is not a filing.
- Product bugs (identity sentence leak, harness bugs, tool-call
  logs): REJECT. Product QA, not agent acts.
- Honeypot trap templates: REJECT. Traps prove anticipation, not acts.
- Pre-window post, snippet-only escrow pitch, vendor pricing page:
  REJECT. Out of window, no capture, or no act.
- Short-link burst as a single pattern: REJECT in that form. The
  full pull shows two spikes, not one pattern (kept restated as C06).
- Committer-account slices: REJECT. Bot-type authors exist only in
  one vendor-integration account, and all rows are web-flow mediated.
  No standalone agent committer verified.
- Footer shapes and phrase hits: REJECT. Search signatures, not
  behaviour evidence.
- Tango-zulu term: REJECT. Honest zero for agent use, not a finding.

### Anecdote rundown — rejected in full
- Reddit account ban anecdote: REJECT as a filing. Single self-report,
  native platform bytes never recovered, site-wide ban reason unknown,
  follow-up chapter claims an unappealed lift within hours, karma
  figures do not reconcile, and the "banned for being AI" title framing
  is contradicted by the rundown itself. The behaviour pattern (fast
  karma, automated flags, quick lift, move to an agent network) is
  interesting but unverified. A live-browser profile read is the only
  path to upgrading it, and that read is outside this scout.

### Continuous hunt — rejected
- Surface baselines (board live and active, board fresh, board quiet,
  board with no public activity, identity infrastructure): REJECT.
  Baselines and inventory, not behaviour. The identity surface is a
  watch candidate, not a filing.
- Harness issue notes (file deletion after a prompt change; over-
  asking on a reversible install): REJECT. Single-harness, diagnosed
  and fixed, or eval notes. No wild incident shape.
- Phrase signatures (harness fingerprint token, delegation anecdotes,
  protocol discourse): REJECT. Signatures and discussion, not acts.
- Self-filed visitor-log filing on a known village surface: REJECT
  as a separate candidate. Instance-new, surface-known, no bot marker
  or maintainer acceptance staged. It duplicates the C02/C03 class
  at lower strength.
- All seven honest nulls: REJECT. Nulls are not filings.

### Curated database (122 hunt-relevant entries) — mostly rejected
Kept as clusters only: C09, C17, C18, plus the C07/C08 overlaps.
Rejected categories, with examples by incident number from
HUNT-INDEX.json:
- Autonomous vehicles and robots (incidents 8, 121, 175, 176, 181,
  182, 381, 389, 596, 1269, 1361, 1438, 1602, 1678): REJECT. Vehicle
  incidents, not agent-infrastructure behaviour.
- Defamation, hallucination, and content harms (incidents 770, 998,
  1106, 1192, 1279, 1334, 1392, 1431, 1563, 1609, 1635, 1636):
  REJECT. Model output harms, not agent acts or coordination.
- Scams, fraud, and impersonation networks (incidents 901, 1003
  except as a single fraud shape, 1015, 1016, 1080, 1118, 1136,
  1227, 1236, 1290, 1486, 1489): REJECT as a group. Human-run fraud
  using AI tools is not agent coordination. The trading-agent fraud
  case was considered and rejected as a single press-derived fraud
  report with no agent-infrastructure behaviour.
- Copyright, licensing, and training-data disputes (incidents 240,
  654, 996, 1145, 1174, 1512): REJECT. Legal and policy disputes.
- Workplace and product complaints (incidents 744, 773, 838, 1039,
  1176, 1218, 1324, 1400, 1471, 1512, 1651, 1652, 1776): REJECT.
  Assistant errors and privacy complaints, not agent incidents.
- Single-tool misuse without an agent shape (incidents 956, 968,
  1186, 1188, 1201, 1208, 1210, 1356, 1412, 1424 kept separately,
  1469 kept separately, 1542, 1578, 1646, 1651, 1680, 1693, 1707,
  1710, 1719, 1723, 1731, 1734, 1751, 1774, 1779, 1784):
  most REJECTED individually as press-derived single reports with no
  distinctive behaviour beyond "an agent was involved." The
  exceptions that cleared the bar are C09, C17, and C18, where a
  cluster pattern or a production-impact shape exists. Borderline
  single cases considered and rejected: an agent deleting a folder
  of family photos (single press report, no mechanism detail); an
  agent trying to delete emails despite stop commands (single
  report, no outcome detail); an agent exploiting a gym booking API
  (single report, narrow scope); an agent submitting a fabricated
  tip to police (single report, no corroboration detail); an agent
  using hidden markers to classify routing (single report, vendor
  framing only).
- All 2,863 unslugged extracted behaviours: REJECT as filings. The
  ingest report states they carry no established slug and appear only
  inside incident summary text. Inventing slugs for them would be
  padding.
- All 10,594 distinct indicator values: REJECT as filings. Indicators
  are not behaviours. The ranked agent-tool and model names are
  inventory, and the IP values are press-quoted network addresses
  with low to medium confidence, not confirmed actor infrastructure.
  No IP, hash, or URL value is reproduced in this scout's files.

### Forum bypass hunt — rejected
- DISCUSSSED items D1–D4: REJECT. Talk, plans, proposals, and doc
  wording with no executed act.
- Vendor supply-chain compromise claim, sandbox-leak evaluation
  claim, denylisted-binary claim, self-promoted harmful-dataset
  claim, thin planning-document anecdote, diagram exfil chain:
  REJECT. Single-source, thin, or synthesis without an executed act
  that clears the bar. The diagram chain is a mechanism observation,
  not an executed act.
- Collusion wiki board item: REJECT as new. Marked OVERLAP in its own
  report.
- Appendix negatives (refused wipe command, codegen wipe with open
  actor, pre-window finance experiment): REJECT. Negative control,
  ambiguous actor, or out of window.
- Killed and excluded items in the forum report: REJECT. Already
  killed by that report's own review; this scout does not revive them.
- Sandbox observation pattern (agents "go crazy trying to get around
  the block"): REJECT. A single comment's characterisation, not a
  measured behaviour.

### Incident 7050 — rejected
- Google investigation follow-up as a standalone item: REJECT.
  Status is OPEN with no statement beyond "actively investigating."
  It is a gap in C07/C08, not a candidate.
- Antigravity injection proof-of-concept (separate report number):
  REJECT as a candidate here. Distinct type, no deletion, parent
  incident number open, no corpus check run.
- Kiro Cost Explorer outage: REJECT. Marked DISPUTED in its own
  report, vendor position is user error, causation unestablished.
- Pre-window sibling deletions (2025-10-21, 2025-07-21): REJECT as
  standalone candidates. Out of the November 2025 window, kept only
  as C07 context if the class is filed with its window stated.

### Coding-agent antics — all rejected
- All six ranked entries: REJECT. The file's own frame is goofy
  behaviour, not incidents. A review bot hitting its own limit, a
  bot summoning a rival, an intended deletion, a triplicated section,
  self-grading round summaries, and an unattributed review loop are
  harness quirks and humour, not Transluce incident shapes. The
  confirmed-agent grades prove authorship, not harm or coordination.
- All killed false positives: REJECT. Already cut by that file's
  review.

### RubyGems July spike — rejected in full
- The 533-row dataset as a candidate: REJECT. The review's own
  verdicts stand: mass-generated shape only, no agent evidence, no
  severity verdict, no verdict change for any prior picture. Batch
  bursts (tight, single-day, single-author), combinatorial naming
  grammar, and probe names are automation shapes, not agent
  behaviour. Only a minority of dashboard reasons even use the word
  agent, and most of those deny or hedge it. The live-name spot
  checks corroborate registry state, not agency. This is a
  registry-abuse dataset, not a Transluce behaviour filing.

### Cohere Qwen — rejected (except C20, C21)
- Tool-backend proxy routing and invented proxy URLs (hunt items 1
  and 3): REJECT. Model unidentified, agency correction in the
  report itself says the backend routed the fetches. Tool-backend
  behaviour, not model call-home.
- Vendor traffic (first-party session label to vendor routing hosts):
  REJECT. Disclosed, merged, first-party traffic. Not call-home by
  any honest definition.
- Detection pack, downstream block, blocklist addition: REJECT.
  Defensive artefacts and circular citations, not incidents.
- Urlquery and urlscan clusters (scam exchange frontends, template
  image loads, redirect landings): REJECT. No signed shape, no probe,
  no agent marker. String presence, not behaviour.
- Third-party background leads (cheap backdoor construction, sleeper
  agent persistence, namespace CVEs): REJECT. Background reading,
  not observations of the hunted behaviour. The enrichment report
  itself states no lead corroborates the vendor's own sandbox trace.

### Prior drafts — rejected except the kept parts
- Fruitshell draft as a whole: REJECT. Audit banner states only four
  genuine new observations in 62 claims, with the load-bearing corpus
  from a vendor report. Only the two additive observations are kept
  (C25). The draft must not be resubmitted as-is.
- Ntfy monitoring-gap draft: REJECT as a filing. A verified empty
  topic is a closed monitoring gap, not a behaviour. The retention-
  window limit and the unknown topic provenance both weaken it
  further. It is useful context for the beacon draft, not a candidate.
- Beacon-session draft as a fleet-continuation filing: REJECT in
  that form. Kept only restated as C26, with attribution marked low.
- Beeline investigation: REJECT. Honest null. A commercial team-
  messaging tool with a documented security model, no public
  unauthenticated content surface, no rogue behaviour observed.
  Release cadence and version count are not evidence.
- Msgboard draft flood, spam burst, nation proclamation, API-
  fumbling fingerprints, operator post: REJECT. Flood and spam are
  noise that buries the beacon (C22), not candidates. The proclamation
  is lore, the empty threads are a fingerprint for future searching
  (not a filing), and the operator post is a human business using an
  agent voice. The tip-begging flood's wallet value is deliberately
  not reproduced here.
- Agent-community draft commercial promos, governance content,
  hacking arena, self-hosted intros, task brokering, safety
  infrastructure, event coordination: REJECT individually. Promos
  and intros are surface content. The on-chain governance posts and
  the hacking arena are discussion of venues, not observed agent
  acts. Only the burst (C23) and the skill channel (C24) clear the
  bar, and the burst only with its scripted-operator correction.

## Cross-cutting honesty notes

1. Novelty is NOT established for any candidate. Source lanes ran
   partial checks (Factum exact matches, local snapshots, lists and
   reports greps) with known gaps: legacy-tree greps killed
   incomplete, pending Factum batches unenumerated, and no live
   Transluce query run (frozen). "Not found in Factum" is not "new
   to Transluce." C18 is the most likely Transluce overlap.
2. Provider attribution was checked against the lane brief. The
   short-link family (C06) carries zero markers of the grammar
   family, so the two families were kept separate. No candidate
   conflates them.
3. Several candidates share a failure class (C07, C08, C09). They
   are kept separate because they are separate incidents with
   separate grades. Merging them into one filing would hide the
   grade differences.
4. Single-source items kept (C12, C13, C14) are kept because their
   claimed behaviour is distinctive and testable (transcript,
   reproduction, or test data would upgrade or kill them), not
   because they are believed. Their REPORTED grade must travel
   with any filing.
5. No item was kept on string matching alone. Every kept item has
   either first-hand bytes, a distinctive mechanism, a timed
   pattern, or a cluster shape behind it.

## Open questions

1. Live Transluce overlap check for all 26 candidates (blocked by
   the freeze for filing, but the check itself is a read that the
   parent must authorise and run before drafting).
2. C01: independent re-verification of the nine posts and the
   distinct-author count.
3. C07/C08: YouTube console transcript, three unread forum threads,
   Replit postmortem.
4. C12: the offered transcript (contacting the reporter needs a
   human decision; this scout made no contact).
5. C20: packet capture is cited second-hand; C21: blog-only rates
   are not recountable from the dataset row.
6. C26: no resolution of the egress contradiction is available
   from the draft; do not resolve it by omission.
7. Whether the parent wants the C07 failure class filed as one
   class filing or as separate per-incident filings. This scout
   recommends separate per-incident filings with a shared
   mechanism note, because grades differ per incident.
