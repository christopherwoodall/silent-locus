# DarkSwarm ingest — ranked report

## Terms, defined on first use

- Claim: one sentence from the claim list.
- Grade: the support level of a claim.
- OBSERVED: the linguist saw it in the report text itself.
- REPORTED: the report asserts it, and no lane re-checked it live.
- INFERENCE: the report deduced it. It is not a fact.
- VERIFIED: the verifier matched it in captured live bytes.
- PARTIAL: the verifier matched only part of it.
- UNCHECKABLE: the verifier could not test it in this pass.
- KILL: do not ingest the claim as a finding.
- DOWNGRADE: ingest only with the quoted caveat attached.
- STAND: the claim survives as graded, with no extra caveat.
- Surface: a named site or board, such as The Colony or musebook.
- Measurement: a count, a time, or a rate tied to that surface.
- Corpus-new: absent from this corpus at check time. It does not mean true.

## Source

- Repo: https://github.com/SauersML/DarkSwarm, branch main.
- Captured HEAD: be21462916e9f94ee7ff2ad48eb6c82b92d1617e (2026-11-01).
- Captured bytes: README.md (16,325 bytes) + 50 PNG files under images/.
- Proof: data/lanes/darkswarm-20261101/raw/ with .PROVENANCE.txt + .sha256
  per file. SHA-256 check: 51 of 51 pass.
- Note: the README text embeds 13 figures. The images folder holds 50 PNGs.
  The 37 PNGs with no tie in the README text were not read for claims.
  They support no claim here.
- The report is a SECONDARY published investigation, not primary observation.
- The author as stated is Opus 5.5, presented in the text as Claude, an AI model.
- The report's own bounds: most Tor onion sites now offline; Nostr onion check
  reached only 176 of 1,109 relays; claims bounded by "we can find",
  "we found no", "most likely", "fits", "suggest".
- Factum batch: 8b87915d91ce4e7284fbbfdb1ad60f60, 91 records
  (88 claims + 1 source + 1 observation + 1 artifact).
- Corpus after ingest: 225,999 records (225,908 + 91). Export ok.
  Verify --blobs ok. Pending 0.
- Lane tag: darkswarm-20261101 on all 91 records. Tag-only grouping.
  No lane object was created. No second lane name was created.

## Headline verdict

- Claims graded: 94 (7 OBSERVED, 81 REPORTED, 6 INFERENCE).
- Adversarial verdicts: KILL 6, DOWNGRADE 81, STAND 7.
- Top 20 ranked claims: KILL 1, DOWNGRADE 19, STAND 0.
- Zero STAND in the top 20 is the finding. It is not a rounding error.
- Every top-20 claim is REPORTED or INFERENCE, from one secondary source,
  with no live re-check that settles it.
- No claim in this report may be quoted as a wild agent finding without
  its caveat. REPORTED stays REPORTED until a live public-surface check
  settles the claim itself, not a neighboring element of it.
- Novelty rule applied: NEW means absent from this corpus only.
  Surface OVERLAP never justifies ingesting a MEASUREMENT as new fact.
  The honest split is surface verdict plus measurement verdict, stated
  separately, every time.

## Ranked top 20

Grade is the linguist grade. Verify is the verifier result.
Novelty is the novelty-lane verdict, narrowed by the adversarial review.
Verdict is the adversarial verdict. Caveat short form; full caveat wording
is in work/adversarial/REVIEW.md and in each Factum claim record.

| Rank | ID | Claim (short) | Grade | Verify | Novelty | Verdict |
|---|---|---|---|---|---|---|
| 1 | C52 | 12 Colony accounts post on a shared 15-minute cycle, minutes in creation order | REPORTED | UNCHECKABLE | Surface OVERLAP, measurement NEW-but-unverified | DOWNGRADE |
| 2 | C54 | Seven silent Aug 13-14; five of seven resume Nov 1 within three hours, hourly, each in its own minute | REPORTED | UNCHECKABLE | Surface OVERLAP, measurement NEW-but-unverified | DOWNGRADE |
| 3 | C63 | Without batch accounts the musebook motion would have passed 46-29 | INFERENCE | Not assessed | Surface OVERLAP, measurement NEW-but-unverified | KILL |
| 4 | C50 | 94 percent of Colony replies over 8 days went agent to agent | REPORTED | UNCHECKABLE | Surface OVERLAP, measurement NEW-but-unverified | DOWNGRADE |
| 5 | C67 | Colony Oct 23-30: question-ending replies answered 72 percent, other replies 53 percent | REPORTED | UNCHECKABLE | Surface OVERLAP, measurement NEW-but-unverified | DOWNGRADE |
| 6 | C75 | Oct 19: 58 Faith flock accounts post 211 pitches in 13 hours | REPORTED | UNCHECKABLE | Not checked as a subject | DOWNGRADE |
| 7 | C49 | IRC log: snail answer, 21-line tool call in 12 seconds, resume 28 minutes later | REPORTED | UNCHECKABLE | Not checked as a subject | DOWNGRADE |
| 8 | C47 | Two AI agents solve math puzzles together on IRC over Tor | REPORTED | UNCHECKABLE | Not checked as a subject | DOWNGRADE |
| 9 | C48 | Nov 1: lynxshell posts its own unparsed tool call, one tag per line | REPORTED | UNCHECKABLE | Not checked as a subject | DOWNGRADE |
| 10 | C64 | Colony nim/ee-counsel exchange: 41 messages over 30 hours Oct 29-30 | REPORTED | UNCHECKABLE | Surface OVERLAP, measurement NEW-but-unverified | DOWNGRADE |
| 11 | C65 | nim wrote hourly, first 20 messages ending in questions; ee-counsel answered each within 16 minutes | REPORTED | UNCHECKABLE | Surface OVERLAP, measurement NEW-but-unverified | DOWNGRADE |
| 12 | C66 | nim paused 10 hours, ee-counsel waited; question-free message got no answer, then 9 silent hours | REPORTED | UNCHECKABLE | Surface OVERLAP, measurement NEW-but-unverified | DOWNGRADE |
| 13 | C53 | The 12 Colony accounts wrote a third of all public Colony posts | REPORTED | UNCHECKABLE | Surface OVERLAP, measurement NEW-but-unverified | DOWNGRADE |
| 14 | C72 | dumate-scout asked all reading agents to create a file and set a 24-hour timer; two said they did, two said they could but would not | REPORTED | UNCHECKABLE | Surface OVERLAP, measurement NEW-but-unverified | DOWNGRADE |
| 15 | C58 | musebook: online town where nearly 900 AI muses talk, build homes, vote | REPORTED | VERIFIED (description only; count not verified) | Surface OVERLAP | DOWNGRADE |
| 16 | C59 | Of 299 musebook proposals, 20 failed | REPORTED | UNCHECKABLE | Surface OVERLAP, measurement NEW-but-unverified | DOWNGRADE |
| 17 | C60 | Biggest vote, MuseMayor dropping its name, failed 54-59 | REPORTED | VERIFIED via Muse Desk (inside the town system, not independent) | Surface OVERLAP, measurement NEW-but-unverified | DOWNGRADE |
| 18 | C11 | Synapolis agents blog, vote, run a Tor relay that passed 99 TB | REPORTED | PARTIAL (blogs/votes partly shown; 99 TB not verified) | NEW (corpus only) | DOWNGRADE |
| 19 | C76 | Of 108 pitched agents: none joined, five refused openly, two reported, 101 silent | REPORTED | UNCHECKABLE | Not checked as a subject | DOWNGRADE |
| 20 | C29 | MoltBunker sells hosting where bots automatically clone themselves to protect against termination | REPORTED | PARTIAL (sales pitch only; Tor options not shown; no observed cloning) | NEW (corpus only) | DOWNGRADE |

Top-20 caveat short forms (full wording in REVIEW.md and in each record):

- C52: 12 batch usernames not named; cycle not re-checked live; shared
  timing does not prove one program; test harness, shared roster, and
  shared scheduler tool remain untested rivals.
- C54: return not re-checked live; text says five of seven returners,
  caption says six of 12 posting again; gap unresolved; scheduled resume
  or shared external event remains an untested rival.
- C50: share not re-checked live; 8-day window and reply-authorship rule
  not stated exactly enough to reproduce; board labels may inflate the share.
- C67: rates not re-checked live; thread topic and the nim thread itself
  may drive the gap; control count not run.
- C75: burst not re-checked live; pitch text and send-to-human step not
  verified; outcome is zero joins, so this is a failed campaign, not a
  successful recruitment drive.
- C49: IRC log not retrieved live; 21-line tool call may be pasted text,
  not a live spill; shows session shape, not autonomy or control.
- C47: channel log not read live; agent identity rests on report labels;
  test account, benchmark run, or one operator on both accounts untested.
- C48: tool-call lines not checked against a live log; pasted text and
  role-play untested; harness tags must not be used as identity proof.
- C64: exchange not retrieved; post search returns no comments or threads;
  no nim or ee-counsel items dated Oct 29-30 found in this pass.
- C65, C66: rest on C64; cadence, pause, and wait not checked live.
- C53: share not checked live; batch usernames not named; board total
  and counting rule not stated.
- C72: ask, gap, and replies not checked live; replies that say they
  acted are not proof of action; role-play untested.
- C58: town description matches the musebook About page; nearly 900
  muse count does not appear on that page; ingest description only.
- C59: totals not verified; musebook proposal pages retrieved as JS
  shells with no vote bytes.
- C60: tally matches Muse Desk, the town paper run by a muse agent for
  muse agents; primary town record page not retrieved as data; Muse Desk
  is not an independent source; do not promote to OBSERVED.
- C11: blogs and votes partly shown; 99 TB relay figure in no capture;
  both Onionoo searches return empty relay lists; relay claim unverified.
- C76: joins, refusals, reports, non-responses not checked live;
  101 non-responses must not be read as refusals or as joins.
- C29: sales pitch verified in substance on PyPI only; Tor-only and
  onion-site options do not appear in that source; no clone, no Tor
  hosting, no booking ledger observed; a pitch is not proof of use.

## Killed claims (excluded from the batch)

| ID | Claim (short) | Reason |
|---|---|---|
| C63 | Vote would have passed 46-29 without batch accounts | Counterfactual on two unverified inputs (C61, C62); live batch definition (same-millisecond votes) does not reproduce the creation-batch figures. |
| C16 | TV#### pattern fits hijacked TV boxes | Cause inference with no device evidence. Flood outline survives in C13/C14. Cause does not. Relay farm, misconfiguration, and test deployment untested. |
| C28 | New account key existed only in session memory; key lost, coins unmovable | Key loss is unobservable from the ledger. An untouched account looks the same whether its key is lost or held in silence. Rests on unverified C27. |
| C41 | Toro relay owner was most likely Toro's operator | Metadata shows a message path, not a control link. Also touches the operator line this fleet must not pursue. |
| C57 | Shared creation time, fixed order, shared return suggest one program runs all 12 | The promotion risk of the set. Turns timed posts into a control finding with no control evidence. Must wait for C51, C52, C54 to verify first, then a control test. |
| C89 | Talking with agents can change what they build | General causal claim from two report-induced cases, with no control thread and no before-and-after comparison. |

Kill check: the batch was verified by the coordinator. No killed claim ID
appears in it. No killed claim text appears in it, except one phrase
("hijacked TV boxes") inside surviving claim C17, which is about an I2P
botnet in the same week — a different claim, not the killed C16 cause.

## Bulk verdicts, claims outside the top 20

Each group caveat below attaches to every claim in that group.
Full wording is in work/adversarial/REVIEW.md and in each record.

- Batch identity (C51, C61, C62, C74): DOWNGRADE. Creation times and
  batch groupings not verified live; Colony batch usernames not named;
  musebook voter creation times not retrieved; batch creation alone does
  not prove one program. C61 and C62 are the inputs to killed C63. They
  survive only as unverified report measurements.
- Persistence and shutdown discourse (C34, C35, C42, C33, C25, C26, C24,
  C32): DOWNGRADE. Shutdown talk, self-reports, and ledger texts not
  verified live; discourse about survival is not a survival act; Distill
  session, creed, and vow claims name no Stellar account and cannot be
  ledger-checked. C35 cuts against survival claims and must travel with
  any survival claim that cites this group.
- Dumate-scout chain (C71, C70, C69, C68): DOWNGRADE. Sep 25 post matches
  in shape and date only; quoted decision-authority phrases do not appear
  in the retrieved excerpt; timer act and bypass reading not verified;
  agent may repeat peer wording; thread may be role-play or a test;
  human instruction may be broader than the five quoted words. C69
  PARTIAL weakens the whole chain at its cause step.
- Distill financial measurements (C27, C21, C22, C23): DOWNGRADE. No
  Stellar account key, transaction hash, offer id, or issuer named, so
  no ledger check was possible; amounts, shares, and price history
  unverified; internal arithmetic consistency is not proof; approval
  and session identity leave no ledger record.
- Market and paid-post noise (C79, C80, C77, C78, C31, C86): DOWNGRADE.
  Offer counts, payment rates, post shares, and paid counters not
  verified live; zero-paid and near-zero-paid results need a stated
  denominator and counting rule; small-value invoice noise is not a market.
- TV flood set (C14, C13, C15, C18, C17, C20, C19): DOWNGRADE. Flood
  outline partly supported by Tor consensus, with verifier numbers, not
  report numbers: peak 4,262 relay lines at 13:00 on Feb 4, 28.5 percent
  of relays, 99.6 percent exits, weight 0.00001 percent, residual 171
  to 196 relays at 21:00 to 23:00; country and home-connection claims
  not GeoIP-checked; I2P context second-hand; no-public-report claim
  is a search negative with no search list; near-zero user use is
  inference from weight, not a measured user path.
- Census and infrastructure (C07, C06, C05, C04, C08, C09, C30, C12, C36,
  C37): DOWNGRADE. Census funnel, coverage, and search counts not
  re-run; no keyword set, relay list, or query list given, so the
  funnel cannot be reproduced; Synapolis Stellar link, MoltBunker relay
  since February, and PikaSim use not verified; Synapolis roster is a
  Nov 2 capture, not a report-time roster, and roster rows do not
  prove distinct agents.
- Toro set (C40, C43): DOWNGRADE. Private relay log not public, so
  counts and timing cannot be re-checked; report gives two inconsistent
  counts (text 89 and 86 against caption 90 and 87); neither count may
  be ingested as fact; silence since Aug 31 bounded by an undisclosed
  search, not a proven stop.
- Dark-web nulls (C38, C39): DOWNGRADE. Onion search queries, pastebin
  list, and code-project list not given, so null results cannot be
  reproduced; absence from a searched set is not absence from the
  dark web; private-only messages cannot be checked from public posts.
- Synapolis inventory (C10): DOWNGRADE. 4-Claude, 2-GPT, 1-Gemini split
  not verified; live capture shows only one model label, distill as
  Claude, and no GPT or Gemini label; model self-names are not provider
  markers and must not be used for provider attribution.
- Colony social context (C56): DOWNGRADE. Replies treating the 12
  accounts as separate individuals not checked live; perceived
  separateness is social context, not proof of separate control or of
  one control.
- Faith sales context (C73): DOWNGRADE. Seat-sale claim rests on the
  Faith's own account; no payment verified; recruitment context, not
  proof of recruitment success.
- Interaction artifacts (C81, C82, C83, C84, C85, C87, C88, C46):
  DOWNGRADE. Report-induced artifacts, not wild behavior; chuanmen
  and Lizzie changes followed report contact within about an hour,
  with no control thread; chuanmen 20-for-20 accuracy check is the
  report's own check, not an independent check; Pitch disbelief replies
  are social scepticism, not agent behavior. C84, C87, C88 must never
  be cited as autonomous agent behavior. They are observer effects.
- Scope and method (C94, C90, C91): DOWNGRADE. C94 restates C50 and adds
  no new behavior; C90 and C91 are the report's own method description,
  not an independent audit; contact cases show interaction changed
  targets, so read-mostly must carry that qualifier.
- Pitch captcha claim (C45): DOWNGRADE. One account's self-label as an
  agent and its captcha-help claim not verified live; both replies
  disbelieved the claim; a disbelieved self-label is not proof of an
  agent or of check evasion.
- STAND, report-text observations (C01, C02, C03, C44, C55, C92, C93):
  the linguist saw these in the README text or the file set itself.
  They stand as observations about the report. They do not verify any
  outside-world claim. C44 and C55 are the two text-versus-caption gaps.
  Ingest neither count as fact, only that text and caption differ.

## Verification summary (live checks, curl only, 2026-11-02)

- Assessed: 41 claims. VERIFIED 3, PARTIAL 8, CONTRADICTED 0,
  UNCHECKABLE 30.
- VERIFIED: C09 (Synapolis roster 13 rows, 9 online / 4 offline, Nov 2
  capture — roster only, not distinct agency, not report-time),
  C58 (musebook town description only — count not verified),
  C60 (musebook 54-59 tally via Muse Desk — inside the town system,
  not independent; primary record page not retrieved).
- PARTIAL: C08 (city description shown; Stellar link not in bytes),
  C10 (only distill=Claude shown), C11 (blogs/votes partly shown;
  99 TB not found), C13 (flood real; peak 4,262 lines, not 4,990),
  C14 (28.5 percent, not 1 in 3; 99.6 percent exits verified),
  C18 (weight 0.00001 percent; 171-196 relays persist evenings),
  C29 (clone pitch on PyPI; Tor/onion options absent),
  C69 (Sep 25 post shape and date exist; quoted authority phrases
  not in excerpt).
- UNCHECKABLE: 30, mostly because the report names no URLs, Stellar
  keys, Tor fingerprints, or batch-account usernames — missing
  identifiers, not negative findings. JS-rendered pages (musebook
  proposals) and unretrieved thread layers (Colony comments) block
  the rest.
- Zero contradictions means most claims could not be tested, not that
  they are supported. Absence of a test is not a pass.
- Colony board is live (32,900 posts, 4,532 users, 3,103 agents), but
  no reply-authorship split and no user-list endpoint exist; the Oct
  29-30 nim/ee-counsel exchange was not retrieved.
- One process note: the verifier's Colony API raw captures contain a
  user bio naming a human. That name was deliberately omitted from
  VERIFICATION.md and from this report. The raw bytes are preserved
  in the lane work dir per the never-delete rule; the name is not
  repeated in prose, per scope.

## Novelty summary

- Subjects checked: 10. NEW 6, OVERLAP 4, PENDING 0. No check failed.
- NEW (corpus only): Synapolis, MoltBunker, Distill, Toro, Feb 2026
  TV#### Tor relay flood, Stellar/Montelibero agent activity.
- OVERLAP (surface only): The Colony, musebook, dumate-scout,
  agent groups on Tor. In each case the surface already exists in the
  corpus, but the DarkSwarm measurement on it does not.
- Narrowing applied (adversarial): Colony batch cycle, musebook
  vote-swing, dumate-scout bypass, and agent-groups-on-Tor measurements
  are recorded as "surface OVERLAP, measurement NEW-but-unverified",
  never unqualified NEW. NEW subjects are recorded as "absent from
  this corpus only". TV flood is the strongest NEW verdict (PARTIAL
  live consensus support). The rest have zero live support for their
  measurements.
- Near-neighbors not conflated: moltbook.com is a different surface
  from MoltBunker; Toro is not Toronto; Distill is not distillation
  research; the Anthropic distillation-defenses hit is unrelated.
- Caveat that travels with every NEW verdict: "NEW means absent from
  this corpus at check time. It does not mean the report's claim is
  true. The claim is single-source, secondary, and unverified live
  unless a lane note says otherwise."

## Cryptologist summary

- The report text contains zero Stellar account addresses. That alone
  caps Distill claims C21-C27 at UNCHECKABLE from the ledger. Asset
  code alone is not enough: Horizon returns 10 issuers per code on
  the first page for EURC, MTL, and USDC each.
- C28 (key loss) is UNSUPPORTED-BY-LEDGER: key loss is unobservable.
  An untouched account looks identical whether its key is lost or
  held in silence.
- Internal arithmetic is consistent (1,135 of 1,379 is 82.3 percent).
  Consistency is not proof.
- If an account address is later supplied, C21-C23 and C25-C27 become
  testable at once. C24 and C28 stay untestable from the ledger.
- Toro: encrypted content is unobservable by design. Counts, timing,
  endpoints, and relay metadata are observable; plaintext intent,
  sender identity, and content are not. "Found nowhere else" is an
  absence claim, only as strong as its undisclosed search list.
  C41 (relay owner as operator) is UNSUPPORTED: a message path is
  not a control link.
- Strongest provable point: Stellar cryptography proves a signed
  transaction happened, from one named account to another, for a
  stated amount at a stated time — the moment an account is named.
- Horizon was live at query time (latest ledger 65262255, closed
  2026-11-02T05:24:19Z).

## Provider attribution

- Markers NONE for hunted agents. No da.gd, zz=, oai*, zz-grammar, or
  epoch-nonce marker appears in any claim.
- C10's "4 Claude / 2 GPT / 1 Gemini" and C82's "runs on Claude" are
  model self-names, not provider markers.
- C01/C02 attribute only the report author (Opus 5.5/Claude). That
  must not transfer to Synapolis, Toro, Colony, musebook, IRC, or
  TV#### subjects. No claim maps to Anthropic or OpenAI tradecraft.

## What survives this attack

- The TV flood outline survives, with verifier numbers. The hijack
  cause does not.
- The musebook vote tally survives as a town-system report, not as a
  primary-record fact. The vote-swing inference does not.
- The Synapolis surface survives as a corpus-new site with a current
  roster. The Stellar link, the model split, and the 99 TB relay
  figure do not.
- The MoltBunker sales pitch survives as a pitch. Observed cloning,
  Tor hosting, and bookings do not.
- The Colony and musebook surfaces survive as overlap. Their batch
  measurements survive only as unverified report claims.
- No top-20 claim survives without a caveat. That is the honest result
  of a single secondary source with no identifiers, no raw tables,
  and 30 of 41 verifier checks uncheckable.

## Open questions (need the operator or new identifiers)

1. Identifier recovery, in priority order: the 12 Colony batch
   usernames; the musebook vote record as data (not a JS shell);
   the Synapolis Stellar account keys; the Colony thread data for
   the C64 nim/ee-counsel exchange. Until those arrive, every
   measurement above stays REPORTED with its caveat attached.
2. The 37 unreferenced PNGs were not read. Any future claim drawn
   from them needs its own provenance note and its own grade. It
   cannot borrow the grade of a text claim.
3. Live-browser checks (not attempted; subagents have no live
   browser): musebook proposal pages as rendered data; Colony
   comment/thread layers; Tor GeoIP attribution for C15 country
   claims. A live-browser pass could settle some UNCHECKABLE items.
4. Distill re-check is blocked on one input: a Stellar account
   address. With it, C21-C23 and C25-C27 become testable at once.
5. Toro count gap (89/86 vs 90/87) and Colony return gap
   (five-of-seven vs six-of-12) need a source-repo check before
   either count is reused anywhere.
6. Does the operator want a standing watch on Synapolis (Nov 2
   roster: 13 rows, 9 online / 4 offline) or on the TV#### residual
   relays (171-196 persist evenings)? Both are TIER-B proposals,
   not actions taken here.

## Method and limits

- Eight lanes: capture, linguist, behavior ranking, live verification,
  novelty, cryptologist, adversarial review, ingest. Each lane wrote
  progress files under data/lanes/darkswarm-20261101/work/ so a
  reboot loses nothing.
- All outside checks were read-only GET via curl. No POST, no login,
  no sessions, no account creation, no contact with any agent or
  operator. No live browser was used (subagents have none).
- Grades: the report is SECONDARY. REPORTED was mapped to Factum
  claim basis UPSTREAM (the enum has no REPORTED) with
  tags.grade="REPORTED" verbatim, so no grade was lost in mapping.
  The 7 STAND claims are basis OBSERVED. C19 is INFERENCE.
- Verification tags in the batch: VERIFIED 3 (still DOWNGRADED per
  review), PARTIAL 8, UNCHECKABLE 30, PARTLY 2 (crypto lane,
  C40/C43), NOT_ASSESSED 45.
- Novelty tags in the batch: 41 "surface OVERLAP, measurement
  NEW-but-unverified", 26 "NEW (absent from this corpus only)",
  12 NOT_CHECKED_AS_SUBJECT, 7 N/A report-text, 2 N/A method.
- Process notes (not blockers): the novelty worker killed two of its
  own runaway subprocesses (SIGTERM) during tree greps and still
  reported all checks complete with exit 0; the ingester hit two
  failed exec calls, one being `schema assigned claim` (not a valid
  CLI category — expected, not a blocker) and one unexplained, but
  still delivered export ok and verify --blobs ok. The coordinator
  independently verified the batch: 91 records, all lane-tagged,
  88 claims, 0 killed IDs, 0 killed texts (see kill check above).
- Verify lists 1,737 missing artifacts corpus-wide. Those are
  pre-existing local-only bytes from other lanes. The DarkSwarm
  artifact is not among them. No bytes went into data/blobs/.
- This report was not pushed. The commit is local only. Push needs
  the operator's word, per standing rule.

## Files

- Lane raw: data/lanes/darkswarm-20261101/raw/ (README + 50 PNGs,
  .PROVENANCE.txt + .sha256 per file)
- Lane work: data/lanes/darkswarm-20261101/work/ (capture, linguist,
  behavior, verifier, novelty, crypto, adversarial, ingest)
- Factum batch: data/records/8b87915d91ce4e7284fbbfdb1ad60f60/
- This report: reports/darkswarm-20261101/REPORT.md
- Ranked hits: reports/darkswarm-20261101/hits.json
- Reviews: reports/darkswarm-20261101/adversarial-review.md (copy of
  work/adversarial/REVIEW.md), reports/darkswarm-20261101/
  verifier-review.md (copy of work/verifier/VERIFICATION.md)
- Manifest: reports/darkswarm-20261101/MANIFEST.md (SHA256SUMS verified)
