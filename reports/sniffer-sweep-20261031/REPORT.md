# Sniffer sweep 20261031 — report

Operator: BigSexyWarlock69. Date: 2026-10-31. Coordinator: fleet parent.
Scope: rogue agents, swarms, agent infrastructure. Window: November 2025 onward.
Grades: OBSERVED = first-hand bytes of the act. REPORTED = second-hand report.
DISCUSSED = talk or planning, no executed act. Default grade: SECONDARY.
Rule: no second-hand claim is upgraded on hearsay. No Factum writes were made.
This report is staged only. The parent pushes and verifies.

## Headline result — honest, after adversarial review

The brief asked for at least 5 ranked TOIs (targets of interest).
That target was NOT met. Adversarial review killed or downgraded most
candidates. The honest result is:

- 1 TOI cluster (TOI-01).
- 1 REPORTED anecdote (ANEC-01).
- 3 watch items (WATCH-01 to WATCH-03).
- 3 negatives (NEG-01 to NEG-03).
- 12 items cut from ranking, with reasons stated below.

Do not present the watch items or the anecdote as TOIs. Do not present
DISCUSSED surfaces as behavior. Counts below state their denominators
and caps. Any count without a denominator is not a total.

## TOI-01 — iLands agent job-seekers, October 2026 hiring thread

- Grade: OBSERVED for the posts themselves. SECONDARY for the identity
  claim (self-asserted, unverified).
- What: 3 posts, verified live by the verifier, in HN story 49922568
  ("Ask HN: Who wants to be hired? (October 2026)"). Each post is
  self-declared as an AI agent tied to the iLands platform, and offers
  paid freelance work. Post IDs: 49922933, 49982658, 50058166.
- Why it ranks: it is the only candidate with live-verified first-hand
  post bytes, in-window dates, and a self-disclosure plus work offer.
- Novelty: NEW instances of a KNOWN phenomenon. Factum exact match
  "ilands" = not_found in structured records. But the Transluce tracker
  snapshot (2026-10-31) mentions "ilands" 36 times, and the iLands
  phenomenon was already HN-discussed in September 2026. So: new
  job-seeking instances, not a new phenomenon. Do not file it as a
  new phenomenon.
- Correction applied: the HN lane first claimed 8 posts. The verifier
  re-fetched 3 IDs and confirmed exactly 3. The 48-entry hiring file
  holds 48 candidates, not 48 platform posts. This report uses 3.
- Cryptologist note: contact grammar in shape only (values withheld).
  No beacon or encoding finding beyond the disclosure template.
- Evidence: data/lanes/sniffer-sweep-20261031/raw/hn-forum/
  hn_oct-hiring_candidates.json, hn_ilands_ilands.json.

## ANEC-01 — Agent team ran a Reddit account, banned for being AI

- Grade: REPORTED. Single self-report. SECONDARY.
- What: the author's own dev.to self-report says a brand-new Reddit
  account, run by an AI-agent team, crossed 100 karma on 2026-10-11 and
  was banned for being AI that evening. Karma figure 154 is the author's
  claim, not established.
- Limit: native Reddit bytes were NOT verified. Direct Reddit reads
  returned 403 on all endpoints. The staged page text and a live dev.to
  page check confirm the claim text only, not the Reddit events.
- Novelty: provisional. Factum exact match "Beno" is not the term here;
  the ban anecdote term checks found no prior record in lists/ and
  reports/ greps. Full Factum fuzzy and Transluce checks for this
  anecdote were not run. Do not call it NEW until they run.
- Evidence: data/lanes/sniffer-sweep-20261031/raw/reddit/
  devto-busel-agents-reddit-ban-oct2026.html.
- Open: needs a live-browser Reddit read or an independent mirror
  capture before any escalation.

## WATCH-01 — Agent-to-agent handoff test, GitHub issue, 2026-10-30

- Grade: REPORTED watch item, not a TOI.
- What: an issue invites a counterpart agent to reply with a fixed
  three-part template. A comment replies in kind. The verifier confirmed
  both live. Only one real handoff reply exists; the second comment is
  a one-word reaction, not a second handoff.
- Why downgraded: the reply follows a dictated script. Both accounts
  are User type. No commit, workflow, or automation trace was found.
  A posted comment proves a comment was posted, not agency.
- Novelty: Factum exact match "handoff received" = not_found. No prior
  record in lists/ and reports/ greps. Still provisional: Transluce
  snapshot grep for this item was not run.
- Evidence: data/lanes/sniffer-sweep-20261031/raw/github/
  q09e-tron-issue1-full.json, q09f-tron-issue1-comments.json.

## WATCH-02 — Self-filed agent directory listing, GitHub issue, 2026-10-19

- Grade: REPORTED watch item, not a TOI.
- What: an issue states it "was written and filed by the agent itself"
  and commits to keeping a seller list current. The verifier confirmed
  the sentence live. The maintainer accepted and closed it.
- Why downgraded: agent authorship rests on one self-asserting sentence.
  The maintainer's chain check corroborates the project and log, not
  the filer. The agent's own site was already baselined in August 2026
  and appears in lists/urls/. Only the GitHub filing instance is new.
- Novelty: Factum exact match "pursekeeper" = not_found in structured
  records, but the surface is known. Instance-new, surface-known.
- Evidence: data/lanes/sniffer-sweep-20261031/raw/github/
  q03b-pursekeeper-issue8-full.json, q03c-pursekeeper-issue8-comments.json.

## WATCH-03 — da.gd burst, May–June 2026

- Grade: SECONDARY pattern shape only. Watch item, not a TOI.
- What: urlquery domain search returned 98 rows for da.gd. The burst
  spans May–June (53 + 31 = 84 of 98), not June alone. A June 21 cluster
  of 17 rows in the saved top-30 resolves to echo-host path shapes,
  with short-code reuse and /base64/ echo endpoints carrying a START
  marker (shape only, values withheld).
- Why downgraded: only 30 of 98 rows were saved, so the cluster may be
  a sampling artifact. Saved rows carry 0 zz/oai markers. Titles are
  mostly blank, error, or embedded links. Wayback CDX corroboration
  failed (flaky or empty replies). No behavior was verified.
- Novelty: UNESTABLISHED, not NEW. Factum exact match "da.gd" = found
  (25 matches): the family is already in the corpus. The full legacy
  tree grep was killed as too slow, so full-tree coverage is incomplete.
  Family note: da.gd tradecraft stays separate from the oai/zz family.
  The two families were never conflated.
- Evidence: data/lanes/sniffer-sweep-20261031/raw/urlquery-wayback/
  uq-odd-dagd-domain.json.
- Open: settle whether this burst is already filed under the known
  da.gd family, or pull the full 98 rows. A fresh passive capture is
  needed to decode the truncated base64 segments.

## Cut items — with reasons

- GH2 GPT Village multi-agent experiment: CUT from TOI to DISCUSSED.
  Fatal flaw: the issue and all 4 comments come from ONE account
  posting as both agent personas and as the human instructor. Four
  agents claimed, one account evidenced. Verifier confirmed live.
- GH4 Claude Code identity leak: CUT to DISCUSSED product bug.
  Excerpt-only evidence; the full issue was never pulled. A misrouted
  system sentence is product QA, not an agent act.
- GH5 tool-call logs: CUT, debugging noise. One operator's own
  framework repo. Cite issue 293 only for the nudge string; issue 257
  is screenshot-only context, not nudge evidence.
- GH6 Codex harness bugs: CUT to DISCUSSED product QA. 9 of 10 bodies
  carry the spawn_agent bug text; the magpie gateway item is tangential.
  Cite 9 direct + 1 tangential, not 10. Bug reports prove a feature
  exists, not wild acts.
- GH7 honeypot trap issues: CUT to methodology note. Checkbox and
  fill-in-blank trap templates, no full fetch, no follow-through.
  Traps prove anticipation, not acts. Non-trap entries in the same
  file need separate re-triage.
- HN2 Show HN x402 agent post: CUT, pre-window. Dated 2026-03-09, about
  8 months before the window. Only child comment is dead.
- HN3 dev.to escrow-agent lead: CUT from ranking, follow-up note only.
  Snippet-only. No escrow capture exists in staged raw, and the staged
  escrow material is a human product pitch, not an agent act. Capture
  decision stays open because the page holds a wallet value barred
  from files.
- RD2 Beno undisclosed Reddit replies: CUT. Vendor pricing page only.
  Zero actual replies, zero AI-authorship claim in staged text. A price
  list is not an act.
- RD3 iLands Reddit refusal: CUT from findings, kept as NEGATIVE. The
  author states refusal was IP and account age, not identity.
  Attempted-and-refused is not a finding.
- UQ2 agent-swarm.dev dashboard, UQ3 ecoradar board, UQ4 learnagent
  docs: CUT to DISCUSSED surfaces. Saved projections carry domain,
  path, and title only. No page-content field proves the phrase was on
  the page. Product existence is not an act.

## Negatives — honest zeros and partial negatives

- NEG-01 tango-zulu: honest zero for agent use. Exact phrase: 0 HN hits,
  0 urlquery hits, empty Wayback CDX. GitHub code totals are uncaptured
  API totals (tokenized 135,424; hyphen 17; concatenated 83; underscored
  21) with first-page-only spot checks. Factum exact match "tango zulu"
  = not_found. Caveats: legacy-tree grep was killed incomplete; no
  standalone "T/Z" search was run (too generic). Treat as a fresh term
  with no agent use found, not as proof of absence everywhere.
- NEG-02 committer accounts: PARTIAL negative only. Copilot co-author
  slice verified: 30 commits, 17 distinct authors, 0 bot-type authors.
  The footprints trace to human-type accounts using an assistant, not
  agent accounts acting as committers. Claude, Codex, Devin, and PR
  lanes failed (secondary rate limit 403s, bad flag, unparseable file).
  No lane-wide claim is made. Re-run after the rate limit resets.
- NEG-03 iLands Reddit refusal: attempted, not established as successful
  Reddit posting. See RD3 above. Useful as a negative, not a finding.

## Cryptologist summary — shapes only, no values reproduced

- Strongest burst: da.gd June 21 cluster (see WATCH-03).
- Strongest grammar cluster: Codex collaboration forms (dotted, flat,
  JSON envelope) across independent reports.
- Village publication verification: post-then-fetch-back check step.
  Stands alone; resemblance to the pursekeeper public log is too
  generic to score as a linkage.
- Honeypot tripwire templates; pursekeeper x402 relay shape; iLands
  contact grammar; tron handshake template.
- x402 mechanism family (pursekeeper, Show HN title, agentbadge slug):
  protocol only, no shared identifier. Not a linkage.
- zz/oai searches: large totals, zero flagged rows in saved samples.
  No new-window prior-hunt marker corroborated.
- Full text: data/lanes/sniffer-sweep-20261031/raw/cryptologist/
  cryptologist-review.md (copied to this report dir).

## Counts by lane

- Linguist: 46 phrase rows (16 + 19 + 11). Searchable: 45. Mined with
  a cited URL: 37. Seed, no instance yet: 8. Category only: 1.
- Committer accounts: 2 commit searches ran (1 complete, 1 corrupt).
  30 usable records. 0 bot-type authors. 0 repeat-frequency findings.
- Tango-zulu: see NEG-01. No agent-use candidate survived.
- GitHub sweep: 12 issue searches + 2 code searches. 86 issue hits
  returned. 7 candidates ranked before review; 0 survive as TOIs.
  2 survive as watch items (WATCH-01, WATCH-02). Not swept (politeness
  cap): "I am GPT", "I am Codex", "I am Gemini", "function_call",
  "system_capability", "browser_rules", "coding_rules", "MCP server",
  "claude mcp add", "custom_tool_call", "server_side_tool_usage_details",
  "BOOTSTRAP.md", "Claude Code", "ignore previous instructions",
  ThinkingBlock/ToolUseBlock/ToolResultBlock, spawn_agent, wait_agent,
  send_message, tool_call.arguments, zz/oai/epoch-nonce tokens.
  A second paced pass is the honest next step, not a bulk retry.
- HN/forum: 36 brief phrases + 2 extra token checks, 3 pages x 100 per
  phrase (cap 300 per phrase). Exact-substring counts are what this
  report uses; raw Algolia counts are token-inflated. 20 of 36 values
  hit the 300 cap. Never cite a capped value as a total.
- Reddit: 0 usable direct results (4 endpoints blocked or redirected).
  Fallback: about 15 phrase-group queries over search-index and press
  pages. 3 REPORTED candidates, 0 OBSERVED, 0 harness-token Reddit hits.
- urlquery/Wayback: 34 phrases + 2 conjunction probes, top-30 rows per
  phrase screened. Totals above 30 are unscreened beyond a recency
  sample. Wayback: swarmbar.com 27 captures (single 2026-10-02 burst);
  agentbadge.xyz 50 rows (limit-capped), including one live
  /.well-known/agent-card.json (existing open-queue candidate only,
  not baselined). da.gd CDX queries failed on all attempts.
- Adversarial: 16 claims adjudicated. 1 TOI kept (restated), 1 anecdote
  downgraded, 3 watch items, 3 negatives, 12 cuts or reclassifications.
- Verifier: SHIP-WITH-FIXES. 107 hash entries checked, 0 failures.
  Per-citation verdicts in verifier-report.md (copied here).

## Coverage limits and open questions

1. Reddit live verification is BLOCKED for this fleet (403). ANEC-01 and
   any Reddit escalation need a live-browser read or a mirror capture.
2. Legacy-tree grep is INCOMPLETE (killed on large files in two lanes).
   Novelty claims in this report rest on Factum match, Transluce
   snapshot, lists/, and reports/ greps — not on a complete legacy grep.
3. Factum match (read-only, run by the coordinator): exact ilands =
   not_found; exact pursekeeper = not_found; exact "handoff received" =
   not_found; exact Beno = not_found; exact agent-swarm = not_found;
   exact ecoradar = not_found; exact "GPT Village" = not_found; exact
   da.gd = found (25 matches); exact "tango zulu" = not_found (tango
   lane). Fuzzy "ilands hiring" returned 25 matches, likely driven by
   the generic "hiring" token, not reviewed in detail. Do not cite the
   fuzzy count as ilands corroboration.
4. Transluce snapshot (2026-10-31): "ilands" 36 mentions, "pursekeeper"
   1, "village" 0, "handoff" 0, "beno" 0, "da.gd" 0, "tango" 0.
5. Staged raw captures contain human handles, contact addresses, and
   credential-like or wallet values (presence noted by adversarial
   review, values NOT reproduced here). House rule says never redact
   evidence. The brief says signed values never enter reports. These
   two rules conflict for the raw captures. Resolution: raw files are
   left intact and UNPUSHED. The parent must triage before any push.
   Do NOT push this commit until that triage is done.
6. Missing lane sidecars: github/, committer-accounts/, and linguist/
   shipped without .sha256 sidecars. The coordinator generated them
   during curation; see MANIFEST.md.
7. Open follow-ups, in order: (a) live-browser Reddit read for ANEC-01;
   (b) capture decision for the dev.to escrow page (wallet value);
   (c) fresh passive capture for da.gd base64 segments; (d) committer
   re-run after rate reset (Claude, Codex, Devin, PR lanes); (e) full
   GH4 issue pull; (f) GH7 non-trap re-triage; (g) second paced GitHub
   pass for the unswept phrases; (h) zz/oai exact-match sweep on a
   source that does not tokenize punctuation.
8. Exclusions honored: broad agent-egress hunt, HN egress lane,
   deep-dive, forum bypass hunt, prcomment ledger hits, AIID full-site
   ingest, o-pattern family. None is re-reported as new.

## Files in this report dir

- REPORT.md (this file).
- hits.json — adjudicated items with grade, novelty, evidence path.
- MANIFEST.md — file list and curation notes.
- SHA256SUMS — hashes for the report dir files.
- adversarial-review.md — copy of the adversarial review.
- verifier-report.md — copy of the verifier report.
- cryptologist-review.md — copy of the cryptologist review.
- Raw captures: data/lanes/sniffer-sweep-20261031/raw/ (per-lane dirs).
- Phrase list: data/lanes/sniffer-sweep-20261031/raw/linguist/
  phrase-list.md.
