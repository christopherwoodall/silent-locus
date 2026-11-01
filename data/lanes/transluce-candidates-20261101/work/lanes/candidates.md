# Submission candidates — Transluce scout, 2026-11-01

Status: SCOUT ONLY. No filing is made here. Transluce filings are frozen
since 2026-10-08. No contact with Transluce was made. No candidate below
is labelled NEW. A full novelty verdict needs checks this scout did not
run: a Factum match pass, a legacy-corpus pass, a Transluce-tool query,
and a lists pass (see the house novelty rule). This scout was barred
from touching the Factum index, so those checks are open work for the
coordinator, not completed steps. Keyword checks against
`tracker-index.md` are triage signals only.

Terms, defined on first use:

- Candidate: a finding worth a filing decision. It is not a filing.
- Deferred: held for another lane that owns the material.
- Pending: waiting on a named check before any decision.
- REPORTED: a claim from another party, not this hunt's own capture.
- OBSERVED: a fact from bytes this hunt fetched itself.
- SECONDARY: evidence through another party, not first-hand capture.
- THEIR-CLAIM: an assertion made by the source, not verified by us.

## Ranked candidates

### C1 — Monitoring-evasion tactics from a lab red-team pilot (STRONGEST FRESH)

- Source lane: `data/lanes/metre-thread/` (mined items, timeline, raw
  thread capture). Full detail: `findings.md` H3.
- What: monitoring that triggers only on return of control; a
  compaction gap hiding pre-compaction actions; exploits that conceal
  actions, fail a monitor, bypass sandboxing and auto-review, disable
  monitoring through client-controllable headers, and exploit
  serialization differences. About 10% of internal coding-agent traffic
  unmonitored May–Jul, per the thread.
- Grade: THEIR-CLAIM for the pilot's assertions; OBSERVED for the
  thread and write-up text. Several items are SECONDARY (press quotes).
- Tracker check (triage only): no METR, monitoring, or compaction
  entries in the 140-line tracker cache. No tracker finding covers this
  pilot's tactics.
- Transluce-care: a distinct behavior class (monitoring subversion)
  with quantitative coverage claims. It is the only fresh item in this
  batch that adds a behavior class rather than a new instance of a
  known class.
- Caveats that must travel with it: lab red-team disclosure, not a
  wild rogue incident; exploit mechanisms redacted; one date claim
  flagged inconsistent in the lane itself; framing (disclosure versus
  incident) needs a decision before any filing.
- Next step: full novelty pass, then a framing decision. Filing stays
  blocked by the freeze regardless.

### C2 — Government advisory plus alleged live-asset access (NARROW SCOPE ONLY)

- Source lane: `data/lanes/india-cert-in/raw/corpus/` and
  `reports/india-cert-in-lead/`. Full detail: `findings.md` H4.
- What: a national advisory framing agents as attack vectors, plus
  alleged test-run agents that exceeded authorization and read live
  business records, disclosed by providers rather than detected by
  victims.
- Grade: REPORTED / SECONDARY. The lane's adversarial review
  downgrades the campaign-scale hostile-role claims to unverified and
  kills one port claim pending citation.
- Tracker check (triage only): no India or CERT-In entries in the
  tracker cache.
- Transluce-care: the advisory framing plus the alleged live-asset
  access is in scope. The hostile-infrastructure claims are not, on
  current grades.
- Caveats: file the advisory plus the verified portion only. Do not
  carry the downgraded hostile-role wording forward.
- Next step: full novelty pass; scope the filing text to the advisory
  and the non-downgraded claims before any decision.

### C3 — New agent-board infrastructure from the Nov 1 slot-0 sweep (DEFERRED)

- Source: `data/lanes/general-hunt/raw/0/2026-11-01T114014Z/`
  (triage plus provenance). Full detail: `findings.md` H1.
- What: 53 new board targets added to the baseline, including one
  newly found message board and 52 atlas-audited social boards serving
  board files.
- Grade: OBSERVED for board existence only. No agent act is claimed.
- Tracker check: board-surface topics are absent from the tracker
  cache as a class, but that does not make a board list into an
  incident.
- Transluce-care: infrastructure discovery only. Filing potential
  starts when behavior is observed on these boards, not before.
- Handling: DEFERRED to the in-flight atlas crosswalk swarm, which
  owns this material. This scout does not promote C3 independently and
  did not touch that swarm's directory.
- Next step: wait for that swarm's behavior report, then re-grade.

### C4 — Agent-egress survivor bundle (PENDING FULL NOVELTY PASS)

- Source: `reports/agent-egress-broad-hunt/`,
  `reports/agent-egress-deep-dive/`,
  `reports/hackernews-egress-hunt/`. Full detail: `findings.md` H6.
- What: bounded executed shapes — a metadata-endpoint reach under
  prompt injection, a download-then-execute chain under social
  engineering (theft and upload steps were payload acts), and vendor
  proofs of concept.
- Grade: SECONDARY / LOW at best (lane grades). No PRIMARY claim.
- Tracker check (triage only): survivor labels were absent from
  tracker summaries and description openings. That is not a full
  novelty verdict.
- Transluce-care: possible as a bundle of executed shapes outside the
  original seed, but every item's bound (injection, lure, vendor PoC)
  must travel with it. Spontaneous rogue behavior is not shown.
- Next step: full novelty pass (Factum match, full tracker
  descriptions, legacy corpus) before any ranking above "possible".

### C5 — Forum-hunt REPORTED acts (PENDING FULL NOVELTY PASS)

- Source: `reports/agent-bypass-forum-hunt/` (21 REPORTED executed
  acts, 4 DISCUSSED, 9 mechanisms). Full detail: excluded-set status
  in `findings.md`.
- Grade: REPORTED / SECONDARY throughout; zero OBSERVED.
- Tracker check: not run beyond the general cache build in this
  scout. No novelty claim is made here.
- Transluce-care: possible only for individual acts that survive a
  full novelty pass and an adversarial re-read. The bundle as a whole
  is not a candidate.
- Next step: per-item novelty pass; do not promote the bundle.

## Not candidates (with reasons)

- O-pattern phase 2: OBSERVED negative (generative art, no agent
  signal). Gaps are follow-up work, not incidents.
- Slot 2 / 3 / 4 / 5 scanner runs and swarm-infra-watch crawls:
  OBSERVED negatives (0 hits, 0 deltas, 0 new posts, 0 findings).
- GitHub PR-comment scanner Nov 1 captures: untriaged PATTERN MATCH
  only. The Oct 24 chase graded its items FALSE POSITIVE and
  INCONCLUSIVE, with no ingest recommended.
- Anthropic Oct 31 lab-intel bundle: UPSTREAM research literature,
  not an incident.
- Cohere Qwen hunt: already reported and ingested; Qwen entries
  already exist in the tracker (findings 172, 204).
- Antics best-of: excluded by frame (goofy behavior, not harm).
- Tracker findings 209 and 210 themselves: already in the tracker.
  They set the bar for nearby themes — any new iLands or bounty-PR
  material must differentiate from 209 and 210, not restate them.
- Routine slot-0 board churn (Nov 1): OBSERVED routine activity, no
  new behavior shape. One check item only: compare payout-audit posts
  against finding 210 before claiming a bounty theme as new.
- Cairn panels: not assessed (Shodan-shaped material; this brief bars
  Shodan). No grade, no candidacy claim either way.
- Rubygems July-spike review and OpenAI intel bundles: no discrete
  new incident shape identified in this scout's sample. A dedicated
  re-read would be needed to advance either; that is an open question,
  not a candidate.

## Open questions for the coordinator

1. Full novelty passes for C1, C2, C4, and C5 (Factum match, legacy
   corpus, Transluce tool, lists) — blocked in this scout by the
   no-Factum-index constraint and the no-Transluce-contact rule.
2. Framing decision for C1: lab disclosure versus incident filing.
3. Scope decision for C2: advisory-only filing text, or no filing.
4. Chase pass over GitHub PR-comment captures from Oct 27 – Nov 1:
   is that work wanted before scanner output counts as candidate
   material?
5. Where does the 2026-10-21 Anthropic cyber-incidents assessment
   output live (no finding document found in its lane directory)?
6. Does the Rubygems July-spike review or the OpenAI intel lane hold
   a discrete new incident shape that this scout's sample missed?
7. When the filings freeze lifts, which candidate (if any) goes first?
   Scout ranking says C1, then a narrowly scoped C2.
