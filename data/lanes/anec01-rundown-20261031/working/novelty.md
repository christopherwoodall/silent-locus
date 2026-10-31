# ANEC-01 novelty check — 2026-10-31 (novelty lane)

Scope: the sniffer sweep graded ANEC-01 as REPORTED, single self-report.
An agent team ran a brand-new Reddit account Oct 9-11 2026, crossed
100 karma Oct 11, and was banned for being AI that evening. The karma
figure 154 is the author's claim, not established. Native Reddit bytes
were never verified (direct reads 403). This file closes the sniffer
report's PROVISIONAL novelty note with the checks below.

Source article (citation only):
https://dev.to/mattbusel/i-let-ai-agents-run-my-socials-day-2-220k-impressions-on-an-87-follower-account-then-reddit-1pjj

Note on names: the Reddit account name below is quoted exactly as the
article publishes it, because it is evidence. No other poster handle
is used in this file.

## Key terms derived from the article

- Reddit account name as published: u/Far-Gene-5806
- "agents run my socials"
- "Can my AI agents make me famous"
- "I let AI agents run my socials"
- "parallel coding agents" (the r/rust question-post topic)
- "154 karma", "220K impressions"
- "Reddit banned them" (ban-claim shape)
- "A 401 mid-task is a stop sign" (the follow-on Moltbook post title)
- "banned for being AI" (ban-claim shape)
- Moltbook (follow-on platform in the same article; checked separately)

## Factum (read-only: status / match only, no writes)

- Status, 2026-10-31: initialized, stale=false, 225,459 records,
  132 lanes, 1 pending batch, corpus commit e234a7a0162bbec82ce868a6ded9a7fbb9ac238e.
  No rebuild was needed. No lock contention was hit.
- Exact text match, not_found (0 matches), for each of:
  Far-Gene-5806, Moltbook, moltbook, "agents run my socials",
  "Can my AI agents make me famous", "AI-generated content".
- Key match with type term, not_found (0 matches), for:
  Far-Gene-5806, Moltbook.
- URL match, not_found (0 matches), for the article URL above.
- Fuzzy text match: no hit contains the account name, the article
  phrases, or the ban claim. What fuzzy did return is noise or
  adjacency, and each item was inspected:
  - "Far-Gene-5806" / "Gene-5806": only bare-number values ("806",
    "580") and unrelated URLs. No record contains the account name.
  - "154 karma" / "220K impressions": only bare-number message values
    ("154", "220"). No karma or impression claim.
  - "parallel coding agents": unrelated coding-agent records
    (screenshot dead-drop technique, "foragents" census). No r/rust post.
  - "Moltbook": genuine platform mentions exist in message bodies
    (for example a commonlog message that cites a Moltbook link).
    None concerns this account, this ban, or this article.
  - "banned for being AI": unrelated records (deepfake ads, a
    moderation notice on another board). No prior same-shape ban.
- Factum's own warning applies: fuzzy retrieval is heuristic, not an
  exhaustive absence test. The exact, key, and URL not_found results
  are the strong results here; fuzzy adds no contradicting hit.

## Transluce tracker snapshot

- Required check, latest snapshot:
  data/lanes/2026-10-09-transluce-intel/raw/findings-list_25_183-210_20261031T115745Z.json
  (total 140, limit 25, 25 items: findings 210 down to 183).
  Grep for Far-Gene, Moltbook, "agents run my socials",
  "make me famous", "parallel coding agents": 0 hits.
  Broader sweep of the same file: "karma" 0 hits; "reddit" hits only
  a synthetic BreakingWeb inbox benchmark (finding in the 183-210
  slice), which is not a real Reddit incident and is unrelated.
- Supplementary sweep, all findings-list snapshots in the same raw/
  directory (18 files): 0 files contain Far-Gene,
  "agents run my socials", "make me famous", or
  "parallel coding agents"; 0 Moltbook hits in every snapshot file.
- Supplementary: lane FINDINGS.md: 0 hits for the same terms.
- Gap: snapshot files on disk cover findings 36-210 plus the newest
  slice. Findings 1-35 are not covered by any snapshot file present.
  A live tracker query was not run (outside this brief's scope;
  no submission was made). Those two items are the residual
  Transluce gap.

## lists/ greps (recursive, lists/urls/ and lists/words/)

- Far-Gene, "agents run my socials", "make me famous",
  "parallel coding agents": 0 hits.
- Article URL slug: 0 hits. No dev.to article entry.
- Moltbook as a platform IS known here, and that is adjacency, not
  overlap with this event:
  - lists/urls/trajectory-domains.md: Moltbook listed as an agent
    social network with a sample post link.
  - lists/urls/scanner-watchlist.md: moltbook.com in the Tier 1
    agent-infra watchlist.
  - lists/urls/monitorable-surfaces.md: moltbook.com as a
    monitorable agent social network.
  - None of these entries mentions the Reddit account, the ban,
    the karma figure, or the article.

## reports/ greps (all prior hunt reports)

- Far-Gene, "agents run my socials", "make me famous",
  "parallel coding agents", article URL slug: 0 files.
- "banned for being AI" / "banned site-wide" / "site-wide ban":
  only the sniffer sweep's own files
  (reports/sniffer-sweep-20261031/REPORT.md,
  adversarial-review.md, verifier-report.md), which are the parent
  record of ANEC-01 itself, not a prior record.
- Moltbook: 5 files, all platform-general and unrelated to ANEC-01:
  trajectory-ingest expansion-scout and wildclawbench reports
  (archive lists / an environment reference), agent-bypass-forum-hunt
  working files (Jan-Feb 2026 public chatter about the platform),
  aiid-full-site HUNT-INDEX.json (a database-exposure incident
  title). None mentions the Reddit account or the ban.
- "AI-generated content" in reports/: only AIID incident titles
  about AI-generated content in general (Bankrate, Facebook
  amplification, deepfake phishing, sextortion, Sudan). None
  concerns Reddit karma or an AI-authorship ban.

## Legacy evidence tree (evidence/)

- Tree as found: 94 files, 10 MB, effectively the transluce-api
  legacy directory only (older lanes were migrated into Factum).
  Full recursive grep completed; no file was skipped and no grep
  was killed. A sanity grep for "reddit" returns hits, so the
  zero results below are real, not a tool failure.
- Far-Gene, "agents run my socials", "make me famous",
  "parallel coding agents", Moltbook: 0 hits each.

## Verdict: NEW (within checked scope)

No prior record of this event exists in any corpus checked:
not the account, not the article, not its phrases, not its
karma figure, not its ban claim, not its follow-on post title.

Why not NEW-INSTANCE-OF-KNOWN: no prior same-shape instance was
found (agent team farms Reddit karma, then takes a site-wide
AI-authorship ban). The known items are adjacency only: Moltbook
as a platform is a known, watched surface, and agent posting on
human platforms is known territory. Adjacency is not an instance.

Why not OVERLAP: every discriminating identifier returns a clean
negative in every corpus checked, including exact, key, and URL
matches in Factum.

## Bounds on this verdict (read before citing it as global)

1. Factum fuzzy search is heuristic by design; it cannot prove
   absence on its own. The verdict rests on the exact, key, and
   URL not_found results plus the file greps, not on fuzzy alone.
2. Factum status shows 1 pending batch. Its contents were not
   enumerated (read-only brief; no pending file was touched). A
   same-day sibling ingest sitting in pending cannot be excluded
   by these checks.
3. Transluce findings 1-35 are not covered by snapshot files on
   disk, and no live tracker query was run. A hit there would
   flip this verdict to OVERLAP.
4. Novelty is about prior recording, not about truth. The ban
   itself is still a single self-report: native Reddit bytes were
   never verified, and the 154 karma figure is the author's claim.
   A NEW grade does not upgrade REPORTED to OBSERVED.
5. The sniffer sweep's own files are the parent record of ANEC-01
   and were excluded from "prior" by definition.

## Open questions for the coordinator

- Should a live Transluce query and a pending-batch enumeration
  run before this verdict is cited outside the rundown?
- The rundown's own capture (data/lanes/anec01-rundown-20261031/raw/)
  is this event's first preservation, not a prior record; its
  Factum ingest, when run, should re-run the account-name match
  as its dedup check.

## Verifier addendum (2026-10-31, appended by coordinator, lane text untouched)

- F1 (key-match reproducibility): the note does not record the --type argument the Factum key-match tool requires, so the key-mode not_found result is not reproducible from the note alone. Cite the exact and URL not_found results as the reproducible Factum evidence.
- F2 (Transluce file count): the "18 files" supplementary-sweep count is clarified — the verifier counts 92 findings-list entries including sidecars (about 30 .json files). The wider grep still found 0 hits. The 0-hit result is unaffected.
