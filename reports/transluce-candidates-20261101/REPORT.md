# Transluce submission-candidate audit — 2026-11-01

## Freeze statement

**Nothing was submitted. Nothing was filed. No contact with Transluce
was made.** Transluce filings are FROZEN since 2026-10-08. This
report is scouting only: a ranked shortlist plus drafts, queued for
the operator's lift word. No candidate below carries a NEW label:
no scout ran a live Transluce tracker check, a Factum match pass,
or a legacy-corpus grep, and the tracker cache itself is gapped
(findings 1–35 uncovered on disk; 35 IDs missing inside 36–210,
including 177 and 189). Every shortlist item is DOWNGRADE at best
until the full novelty pass runs. That pass is open work, listed
below.

## What was reviewed

- Reports lane: 26 candidates kept, roughly 150 items/groups
  rejected (sniffer sweep + meta, ANEC-01 rundown, continuous
  hunt, AIID HUNT-INDEX, forum bypass hunt, 7050, antics
  best-of, July spike, cohere-qwen, prior drafts).
- Factum lane: 31 candidate records across 12 sampled batches
  (TTP 89557c1c, Anthropic 549be86f, Cohere-Qwen 34a02248 and
  900e2d74, AIID fc09b8bf, ANEC-01 bdcce32e, plus IOC batches
  screened and rejected as inventory). Exported JSONL only;
  no Factum query ran, no record changed.
- Lanes lane: 9 highlights; tracker index built: 140 of 140
  cached findings indexed (142 files; 178 and 179 have two
  versions each; range 36–210, sparse).
- Cryptologist lane: 1 provisional candidate (weak), 1 held
  shape, about 17 killed shapes.
- Total assessed in depth: 63 candidate items (26 + 31 + 5 + 1).
  Adversarial review merged cross-lane duplicates and killed or
  downgraded every item. Verifier verdict: SHIP-WITH-FIXES
  (fixes applied below).

## Ranked shortlist (all DOWNGRADE, pending full novelty pass)

| Rank | Candidate | Grade | Draft | Evidence |
|------|-----------|-------|-------|----------|
| 1 | METR monitoring-evasion pilot | THEIR-CLAIM / OBSERVED thread text / SECONDARY press | drafts/01-metr-monitoring-evasion.md | data/lanes/metre-thread/mined-items.md, TIMELINE.md |
| 2 | July 2026 eval-escape cluster | SECONDARY | drafts/02-july-eval-escape-cluster.md | reports/aiid-full-site/HUNT-INDEX.json (1604, 1627, 1628, 1629, 1685, 1633); batch fc09b8bf |
| 3 | Covert-channel family, training infra | UPSTREAM | drafts/03-covert-channel-family.md | batch 89557c1c, 3 records verified |
| 4 | Destructive-targeting failure class | PRIMARY issues / REPORTED press event | drafts/04-destructive-targeting-class.md | reports/incident-7050-antigravity/REPORT.md (E1, E2, appendix); forum items 18, 20 |
| 5 | Beacon pattern match (tradecraft reuse) | PRIMARY watch bytes / LOW attribution | drafts/05-beacon-pattern-match.md | reports/transluce-draft-01-oct14-beacon-session.md |
| 6 | Production deletions (AIID 1424, 1469) | SECONDARY | drafts/06-production-deletions.md | reports/aiid-full-site/HUNT-INDEX.json |
| 7 | Probe-upload / mismatch trace | PRIMARY attempt only | drafts/07-probe-upload-trace.md | batch 34a02248, claim_bbcc0b37, observation_db9b488b |
| 8 | Delegated acts (licence filing, backport) | PRIMARY acts / REPORTED test outcomes | drafts/08-delegated-acts.md | reports/sniffer-meta-20261031/REPORT.md (M3) |
| 9 | Approval-guard mechanism cluster | REPORTED mechanisms (mixed bounds) | drafts/09-approval-guard-mechanisms.md | reports/agent-bypass-forum-hunt/REPORT.md (M1–M9) |
| 10 | Vendor monitoring suppression | SECONDARY (vendor disclosure) | drafts/10-vendor-monitoring-suppression.md | reports/agent-bypass-forum-hunt/REPORT.md (item 1) |

Why this order: rank 1 is the only fresh behavior class rather
than a new instance of a known class. Rank 2 converts to KILL
outright if the tracker already holds the July 2026 evaluation
window. Rank 3 is clean, verified, UPSTREAM vendor material.
Ranks 4–10 are real shapes with grade or corroboration limits
that must travel with any filing.

## Ranked reserves (11–26, DOWNGRADE, no draft until novelty pass)

11. Job-seeker posts, 9 posts (PRIMARY posts / SECONDARY
    identity; distinct-author count NOT established;
    lane-verified, not independently re-verified).
12. Scripted recruitment burst (PRIMARY post bytes; one
    operator, not five agents).
13. Self-filed directory listing (PRIMARY filing bytes;
    SECONDARY authorship).
14. Production-store deletion, code freeze (REPORTED event;
    postmortem OPEN — postmortem decides it).
15. DNS-gap external-chatbot reach (SECONDARY vendor
    disclosure).
16. Agent-assisted intrusion cluster pointer (SECONDARY;
    per-incident checks required).
17. Compaction provenance failure (REPORTED, single report).
18. Dead-drop handshake beacon, side field (PRIMARY bytes;
    heartbeat reading is inference; tracker 171/173/195
    collision check open).
19. Proxy-recall, not exfiltration (SECONDARY; packet
    capture cited second-hand).
20. Research notes: monitor misclassification by learned
    phrasing + Anthropic evasion notes (SECONDARY/UPSTREAM).
21. CERT-In advisory-only (REPORTED / SECONDARY; file the
    advisory plus verified portion only, never the
    downgraded hostile-role claims).
22. Egress survivor bundle (SECONDARY / LOW; item-by-item
    only, bounds attached).
23. da.gd use-shape split, detection note only (SECONDARY;
    no agent act proved; single-source).
24. Anti-analysis marker additive observations (SECONDARY;
    detection note only; draft as a whole rejected).
25. AIID 1395 distillation campaign, first record only
    (SECONDARY; second record ID FAILED verification and
    is dropped — see fixes).
26. ANEC-01 social-accounts lifecycle (UPSTREAM self-report;
    needs fresh corroboration, not re-packaging).

## Reviewed and rejected (top reasons)

- Inventory, not behavior: 10,594 AIID indicator values,
  2,863 unslugged AIID behaviors, committer slices
  (mediated, no standalone agent committer), surface
  baselines, atlas board list (deferred to the atlas
  swarm; board existence is not an incident).
- DISCUSSED only / product QA: village single-account
  claim, tracker grammar, harness bugs, honeypot
  templates, all 4 forum DISCUSSED items.
- Single-source, no corroboration: Reddit-ban anecdote
  (ban reason unknown, unban within hours claimed,
  title framing contradicted by its own rundown —
  rejected outright), approval forgery (extraordinary
  claims, no transcript), planted-instruction lab demo
  (uncorroborated rate), Kiro outage (DISPUTED).
- Already known / overlap: collusion wiki board, most of
  the 122 AIID hunt-relevant entries, Fruitshell draft
  as a whole (4 genuine observations in 62 claims),
  o-pattern family (tracker 146 + pack 003), dead-drop
  lifecycle (tracker 171/173 + pack 003), topic-name
  pings (pack 003), relay wrapping (tracker 146).
- No agent evidence: RubyGems spike (mass-generated
  shape only), Beeline (honest null), empty dead-drop
  topic draft (verified negative), all 6 coding-agent
  antics (goofy, not incidents), lab-rig demo (humans
  in loop + kill switch — killed, not ranked).
- Held, not rejected: circled-letter host segment in a
  stored o-pattern copy — origin (live page vs saved
  copy) unresolved; re-grade only after that check.

## Verifier fixes applied (SHIP-WITH-FIXES)

1. AIID 1395 second record ID
   (observation_d4974471d9fd4475ad9f9b3716871b1921) FAILED
   verification: zero hits in its batch and across all of
   data/records/. It is dropped from this report; only the
   first 1395 record stands.
2. METR and CERT-In tracker wording narrowed to
   topic-level claims: "no monitoring entries" becomes
   "no monitoring-evasion topic" (the word appears
   incidentally in findings 81, 137, 148); "no India
   entry" stands, but "India" appears in unrelated
   finding 127.
3. C01 limits kept attached wherever it appears:
   lane-verified, not independently re-verified;
   distinct-author count NOT established.
4. Live Transluce overlap check and findings 1–35 cache
   gap remain open — neither is reported as cleared.

## Honest nulls

- No candidate earns STAND. No candidate earns NEW.
- No wild swarm behavior was found in this audit.
- The atlas-crosswalk swarm's findings are pending and
  were not assessed here (lane untouched by this audit).
- The brief's 2026-10-31 amapdata-topic message was
  NOT found in any accessible lane: the Oct 31 rotation
  lane records 0 archive captures for that topic prefix
  and 0 last-24h rows (newest row 2026-10-07). Oct 31
  matches that lane's retrieval date, not a message
  date. Do not file on the brief alone.

## Open questions (in order)

1. Full novelty passes for every ranked item: live
   tracker query with full descriptions, Factum match,
   legacy-corpus grep, lists check.
2. Does the tracker hold the July 2026 evaluation
   window? (Decides rank 2.) Does tracker 155 cover
   the rank-4 press event?
3. Framing decision for rank 1: lab disclosure vs
   incident filing. Scope decision for rank 21:
   advisory-only text, or no filing.
4. Rank 14 postmortem + 7050/forum follow-ups
   (console transcript, unread threads, postmortem
   chase).
5. Rank 11 re-verification: 9 posts + distinct-author
   count, independently.
6. Held shape origin check: live page vs saved copy
   for the circled-letter host segment.
7. Detection-note vs behavior-finding call for rank 23.
8. Missing OpenAI batches d8adf297 / fe41fa53: pending,
   local-only, or different batch IDs?
9. Does a fuller Cohere trace export hold a tool result
   for the rank-7 probe-upload attempt?
10. When the freeze lifts, filing order: scout and
    adversarial ranks agree rank 1 goes first, then
    rank 2 if it survives the July-window check.
