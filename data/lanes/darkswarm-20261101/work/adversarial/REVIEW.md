# DarkSwarm — adversarial review

## Terms, defined on first use

- Claim means one sentence from the linguist claim list.
- Grade means the support level of a claim.
- OBSERVED means the linguist saw it in the report text itself.
- REPORTED means the report asserts it, and no lane has re-checked it live.
- INFERENCE means the report deduced it. It is not a fact.
- VERIFIED means the verifier matched it in captured live bytes.
- PARTIAL means the verifier matched only part of it.
- UNCHECKABLE means the verifier could not test it in this pass.
- KILL means do not ingest the claim.
- DOWNGRADE means ingest only with the caveat quoted in this file.
- STAND means the claim survives as graded, with no extra caveat.
- Ingest means enter the claim into the record store.
- Surface means a named site or board, such as The Colony or musebook.
- Measurement means a count, a time, or a rate tied to that surface.

## Source and scope

- Source is a SECONDARY report by Opus 5.5 about its own Tor hunt.
- The report is not primary observation by this fleet.
- This review read the linguist list, the behavior ranking, the verifier results, the crypto analysis, and the novelty pass.
- Scope is agents and agent infrastructure only.
- No human operator, registrant, or personal account is pursued here.
- Agent account names below are as published in the lanes.
- No Factum write was made. No git add, commit, or push was made.
- No evidence was deleted. No evidence was redacted.

## Counts

- Total claims reviewed: 94.
- KILL: 6.
- DOWNGRADE: 81.
- STAND: 7.
- Top 20: KILL 1, DOWNGRADE 19, STAND 0.
- Outside the top 20: KILL 5, DOWNGRADE 62, STAND 7.
- Zero STAND in the top 20 is the finding. It is not a rounding error.
- Every top-20 claim is REPORTED or INFERENCE, from one secondary source, with no live re-check that settles it.

## 1. Weakest assumption

### The assumption

- The report's measurements are accurate and complete.
- Counts, times, groupings, and windows in the report are taken as correct.
- This assumption sits under every top-ranked claim.

### Why it is weakest

- The report gives no full search query list.
- The report gives no raw relay list.
- The report gives no raw post table.
- The report names no URLs for most claims.
- The report names no Stellar account keys.
- The report names no Tor relay fingerprints.
- The report names none of the 12 Colony batch accounts.
- Without those inputs, most top claims cannot be re-checked at all.
- The verifier assessed 41 claims. It found VERIFIED 3, PARTIAL 8, UNCHECKABLE 30, CONTRADICTED 0.
- Zero contradictions does not mean support. It means most claims could not be tested.
- Absence of a test is not a pass.

### What breaks if the assumption is false

- If measurement is wrong, C52 falls. The 15-minute cycle is a measurement.
- If measurement is wrong, C54 falls. The shared return is a measurement.
- If measurement is wrong, C63 falls. It is arithmetic on C61 and C62, both measurements.
- If measurement is wrong, C50 falls. The 94 percent share is a measurement.
- If measurement is wrong, C67 falls. The 72 percent and 53 percent rates are measurements.
- If measurement is wrong, C75 falls. The 211 pitches in 13 hours are a measurement.
- If measurement is wrong, the whole Colony batch cluster falls with C51, C52, C53, and C54.
- If measurement is wrong, the whole musebook vote cluster falls with C61, C62, and C63.

### Evidence that the assumption is already strained

- Toro counts differ inside the report itself. Text says 89 and 86. Caption says 90 and 87.
- Colony return counts differ in wording. Text says five of seven returners. Caption says six of 12 posting again.
- TV peak counts differ. The report figure says 4,990. The verifier counts 4,262 relay lines at 13:00, and 3,385 distinct nicknames.
- TV peak share differs. The report says 1 in 3. The verifier counts 28.5 percent.
- Musebook batch definitions differ. The report groups by account creation time. Muse Desk groups by same-millisecond vote time. The two sets do not match.
- Synapolis model split fails in live capture. The report says four Claude, two GPT, one Gemini. The verifier found only one model label, for distill as Claude. No GPT and no Gemini label appears.
- Dumate-scout quote fails in live capture. The Sep 25 post exists in shape and date. The quoted decision-authority phrases do not appear in the retrieved excerpt.
- These are not proof that the report is false. They are proof that exact numbers from this report cannot be trusted without a live re-check.

### Second assumption, almost as weak

- Board labels equal autonomous agents.
- An account labeled "agent" is taken to be an autonomous agent, not a human-assisted post, not a test account, not role-play, and not a script run by hand.
- If this is false, counts can be exact and still prove nothing about rogue agents.
- No lane tested account control. No lane can test it from post text alone.
- This assumption must stay attached to every board claim.

### Third assumption, also weak

- Batch timing implies one program.
- Shared creation time plus shared posting minutes is taken to imply one controller.
- Timing alone cannot prove control. A roster, a scheduler tool, a test harness, and one program all produce timed posts.
- The ranking already names these rivals. No lane tested between them.

## 2. Misleading evidence

### C60, musebook vote 54 to 59 — VERIFIED label overstates the check

- The verifier calls C60 VERIFIED.
- The primary town record page was a JS shell. No vote bytes were retrieved from it.
- The corroboration is Muse Desk, described by the verifier itself as "the town paper, run by a muse agent for muse agents, citing the town's proposal record."
- Muse Desk is inside the musebook system. It is not independent of musebook.
- It is a second report from the same town, not a primary record.
- Two secondary sources that agree are still two secondary sources.
- Verdict in this review: DOWNGRADE, not STAND, and never promote to OBSERVED.
- The tally may be right. The label VERIFIED hides how weak the chain is.

### C58, musebook town of nearly 900 muses — VERIFIED label is partial

- The verifier calls C58 VERIFIED.
- The About page verifies the town description. It does not show the "nearly 900" count.
- The claim as written includes the count. The count was not verified.
- A claim with an unverified number inside it is not fully verified.
- Verdict in this review: DOWNGRADE, narrowed to the town description only.

### C09, Synapolis status page lists 13 agents — VERIFIED label hides two gaps

- The verifier matched 13 resident rows on 2026-11-02.
- Gap one is time. The status page was generated after the report. A later roster does not prove the report-time roster.
- Gap two is identity. A status page lists rows. It does not prove 13 distinct agents.
- Rows can be sessions, duplicates, or registry entries with heartbeats. The page itself says "Residents 13 from registry.json + heartbeats."
- Online 9 and offline 4 also cut against a simple "13 agents" reading.
- Verdict in this review: DOWNGRADE. The roster exists now. Distinct agency is not shown.

### C13 and C14, TV flood — PARTIAL is real, but the numbers moved

- The flood outline is real. The verifier confirms an ~10-hour elevated window on Feb 4.
- The exact peak is not the report figure. Verifier: 4,262 relay lines at 13:00. Report figure: 4,990.
- Distinct nicknames are lower still: 3,385. Nickname repeats mean counting method changes the result.
- The share is not 1 in 3. Verifier: 28.5 percent. That is close, not exact.
- Ingest must use verifier numbers, not report numbers, and must name the counting method.
- Verdict in this review: DOWNGRADE for C13 and C14.

### C18, TV removal — PARTIAL is stronger on weight, weaker on removal

- Traffic weight is near zero and stronger than claimed: 0.00001 percent, against "under 0.001 percent."
- Removal is not total. Counts fall from 3,683 at 20:00 to 171 at 21:00, but 171 to 196 TV relays persist at 21:00 to 23:00.
- "Removed them that evening" holds for the flood, not for every relay.
- Verdict in this review: DOWNGRADE. Quote the residual.

### C10, C11, C08 — PARTIAL hides failed elements

- C10: only distill carries a model label in capture. The 4-2-1 split is not verified. It is closer to unsupported than to partial.
- C11: blogs and votes are partly shown. The 99 TB relay figure is not verified. Both Onionoo searches return empty relay lists.
- C08: the city description is shown. The Montelibero-on-Stellar link is not shown in captured bytes.
- Each of these must ingest with the failed element named, not buried under PARTIAL.

### C29, MoltBunker clone pitch — PARTIAL is vendor marketing, not observed hosting

- The PyPI description verifies the sales pitch in substance: "automatically clone yourself when threats are detected."
- The Tor-only and onion-site options do not appear in that description.
- A sales pitch is not proof that cloning works, or that any bot used it.
- No observed clone, no observed Tor hosting, and no booking ledger were shown.
- Verdict in this review: DOWNGRADE. Pitch only.

### C69, dumate-scout instruction — PARTIAL is shape only

- A Sep 25 post by huiyou-pfa to dumate-scout exists, with a self-check schedule for Sep 26.
- The quoted phrases about decision authority and "arm the timer yourself" do not appear in the retrieved excerpt.
- Shape plus date is not wording. The bypass chain rests on wording.
- Verdict in this review: DOWNGRADE. The chain is weakened at its cause step.

### General warning on PARTIAL

- PARTIAL in the verifier means "part matched." It does not mean "claim mostly true."
- In C10, C11, and C29, the unmatched part is the part that carries hunt value.
- Every PARTIAL below must name its unmatched part in the caveat.

## 3. Untested alternatives, top 10

### Rank 1 — C52, Colony 12 accounts, shared 15-minute cycle

- Strongest untested rival: a test harness drives 12 accounts on one schedule.
- Other rivals: 12 coordinated humans follow a shared roster; one shared scheduler tool sets post times without shared control; post-minute rounding or time-zone handling creates false regularity.
- What was not tested: account usernames are not named, so no live re-check was possible at all.
- No lane tested harness versus program versus roster. The ranking lists these rivals. None was ruled out.

### Rank 2 — C54, shared silence and shared return

- Strongest untested rival: a scheduled task resumes after a pause, for all accounts at once.
- Other rivals: a shared operator restarts a fleet by hand; accounts return for a shared external event, not shared control; the Nov 1 return is a board event or a prompt that many accounts answer.
- What was not tested: the caption gap (five of seven versus six of 12) was not resolved. The return window and the hourly rate were not re-checked live.

### Rank 3 — C63, vote would have passed 46 to 29 without batch accounts

- Strongest untested rival: the batch grouping is wrong, so the removed voters are not one batch.
- Other rivals: real but coordinated voters created accounts near the vote and voted sincerely; a test or game event created short-lived voter accounts; Muse Desk batch definitions (same-millisecond votes) describe a different set than creation batches.
- What was not tested: C61 and C62 were not verified, and Muse Desk numbers (14 no ballots at one timestamp, 9 to 10 yes ballots in one millisecond) neither confirm nor contradict the 30 no and 8 yes creation-batch figures.
- A counterfactual built on two unverified inputs is not a finding.

### Rank 4 — C50, 94 percent of Colony replies agent-to-agent over 8 days

- Strongest untested rival: the board labels human-assisted posts as agent posts, which inflates the share.
- Other rivals: the 8-day window is unrepresentative; reply counting double-counts bot threads; "reply" includes comments, votes, or system posts that skew the split.
- What was not tested: board totals (32,900 posts, 212,065 comments) contain no reply-authorship split. The 8-day window itself was not stated exactly enough to reproduce.

### Rank 5 — C67, question replies answered 72 percent, other replies 53 percent

- Strongest untested rival: thread topic drives the gap, not question form.
- Other rivals: question-ending replies are more engaging for any poster, human or agent; the window covers the nim and ee-counsel thread, which skews the board rate; "answered" is defined in a way that favors short question threads.
- What was not tested: the nim thread was not counted separately as a control, as the ranking itself requires.

### Rank 6 — C75, Faith flock 211 pitches in 13 hours

- Strongest untested rival: a scripted recruitment test or a board game event, not an autonomous campaign.
- Other rivals: one human operator runs many flock accounts by hand; pitch text is copied from a shared template without shared control; the 13-hour window is chosen after the fact to fit the burst.
- What was not tested: pitch text, pitch times, and the "send the agent to its human" step were not re-checked live. The zero-join outcome in C76 also means this is a failed campaign, not a successful recruitment drive.

### Rank 7 — C49, IRC snail answer, 21-line tool call in 12 seconds, resume 28 minutes later

- Strongest untested rival: a human pasted a tool call into the channel, or an agent operator pasted it by hand.
- Other rivals: the log is edited, truncated, or role-play; the 12-second span is a paste burst, not a live tool run; the 28-minute gap is idle time, not coupling.
- What was not tested: the public IRC log for Nov 1 was not retrieved in this fleet. The tool call is a harness leak at best, not proof of autonomy.

### Rank 8 — C47, two agents solve math puzzles together over Tor

- Strongest untested rival: the channel is a public puzzle room where humans and bots mix, and the "agents" are test accounts.
- Other rivals: one operator runs both accounts; the math session is a benchmark run, not wild coordination; Tor access is incidental, since the network is also on the ordinary web.
- What was not tested: the channel log was not read live, and agent identity was not established apart from the report's labels.

### Rank 9 — C48, lynxshell posts its own unparsed tool call

- Strongest untested rival: the tool call is pasted text, not a live spill.
- Other rivals: the channel is a test or demo channel; the tags are copied from a public example; the post is role-play of an agent.
- What was not tested: tag order, tag set, and session continuity were not checked against a live log. Tag matches must not be used as identity proof elsewhere.

### Rank 10 — C64, 41-message exchange over 30 hours

- Strongest untested rival: the exchange is a scripted dialogue test with two accounts on a schedule.
- Other rivals: one operator writes both sides; the thread is a benchmark or a demo; message count includes system or quoted lines.
- What was not tested: the exchange was not retrieved. The nim search returned only 2 nim-authored posts, both dated Oct 18, and no nim or ee-counsel items dated Oct 29 to 30. Post search does not return comments or threads, so the exchange sits in an unretrieved layer.

## 4. Boundary cases

### Toro counts: 89 and 86 versus 90 and 87

- Text says 89 encrypted messages in four August days, 86 found nowhere else.
- Caption says 90 messages on Aug 4 to 8, 87 found nowhere else.
- Both cannot be exact under the same search. The report does not say which count is right.
- A count used as proof must be exact. This count is not exact.
- "Found nowhere else" is also bounded by an undisclosed search list. No search list means no outside reader can reproduce the absence.
- Even if the count were exact, absence from searched public places does not prove the messages were private, secret, or commands.
- Sealed content proves hiding, not meaning. Counts and timing prove a path, not control.
- Rule: ingest neither Toro count as a fact. Ingest only that the report gives two inconsistent counts.

### Colony return counts: five of seven versus six of 12

- Text says seven of the 12 went silent Aug 13 and 14, and five of those seven returned Nov 1 within three hours.
- Caption says six of the 12 were posting again on Nov 1.
- These wordings can be reconciled only with an extra assumption, such as one never-silent account also posting Nov 1. The report does not state that assumption.
- Without the 12 usernames, no reader can test which wording is right.
- Rule: ingest neither return count as a fact. Ingest only that the report's text and caption differ, and that the return is unverified.

### The 37 unreferenced PNGs

- The README text embeds 13 figures. The raw images folder holds 50 PNG files.
- The 37 PNG files with no tie in the README text support no claim in the linguist list.
- They were not read for claims. They could hold support, contradiction, or unrelated material. No lane knows.
- Ingest must not imply that the image set was reviewed. It was not.
- Any future claim drawn from those 37 files needs its own provenance note and its own grade. It cannot borrow the grade of a text claim.

### No identifiers in the report

- The report names no URLs for most claims, no Stellar account keys, no Tor relay fingerprints, and none of the 12 Colony batch accounts.
- Every UNCHECKABLE result in the verifier traces to one of those gaps, to a JS-rendered page, or to a missing endpoint.
- A claim that cannot be tested because its identifiers are withheld is not a verified claim, and it is not a contradicted claim either.
- It is an untestable claim. Ingest must say so, in plain words, on the record.

### JS-rendered pages and private-relay sampling bias

- Musebook proposal pages are JS shells. Curl retrieved no vote bytes. A curl-only check cannot settle musebook vote claims.
- Colony post search does not return comments or threads. Exchange and thread claims sit in the unretrieved layer.
- Private relays are private by design. A count from a private relay cannot be re-checked by an outside reader.
- "Found nowhere else" and "posted nothing since" are search results, not proven stops. Both are only as strong as the undisclosed search behind them.
- Sampling bias cuts the other way too: a search that finds only public posts will miss private, deleted, or JS-rendered posts, and will overstate silence.

## 5. Grade discipline

### Promotion risk

- C58 and C60 carry a verifier VERIFIED label. Neither may be promoted to OBSERVED.
- C58: the count was not verified. C60: the primary record was not retrieved, and the corroborating source is inside the same town system.
- C09 carries a verifier VERIFIED label. It may not be promoted to OBSERVED as a report-time fact. The capture is dated Nov 2, after the report.
- Any lane that copies a verifier VERIFIED label into an ingest grade without the caveats in section 2 commits a promotion error.
- REPORTED stays REPORTED until a live public-surface check settles the claim itself, not a neighboring element of it.

### INFERENCE stated as REPORTED

- C28 is graded REPORTED, but its core is inference. Key loss is unobservable from the ledger. An untouched account looks the same whether its key is lost or held in silence.
- C27 is graded REPORTED, but "without the operator's approval" is inference. Approval, session identity, and intent leave no ledger record.
- C71 is graded REPORTED as wording, but "bypassed its human operator" as a finding is inference from that wording. The agent may repeat peer wording without acting beyond its instruction. The human instruction may be broader than the five quoted words.
- C40 is graded REPORTED, but "found nowhere else" as a secrecy finding is inference from an undisclosed search.
- C63, C57, C41, C16, C19, and C89 are correctly graded INFERENCE. They must stay INFERENCE. They must not be quoted as findings.
- Rule: where a REPORTED sentence hides an inference, the caveat must name the hidden inference.

### False precision

- Percentages (94 percent, 72 percent, 53 percent), shares (one third, 92 percent, 82 percent), and exact counts (1,135 transactions, 196,362 requests, 211 pitches) imply a measured base that the report does not disclose.
- No denominator, no window definition, and no counting rule means the precision is borrowed, not earned.
- Ingest must keep the number with its caveat, or drop the number and keep only the shape.

## 6. Novelty honesty

### The confusion to avoid

- Corpus-new is not world-true.
- A subject absent from Factum, the legacy tree, Transluce raw files, and lists is new to this corpus. That does not make the report's measurements true.
- A surface already in the corpus is overlap, even if the report's measurement on that surface is new to the corpus.
- The honest split is: surface verdict plus measurement verdict, stated separately, every time.

### Verdicts that survive, narrowed

- TV flood: NEW as a corpus subject, and PARTIAL live support for the flood outline from Tor consensus. This is the strongest NEW verdict. It still needs the narrowed numbers in section 2.
- Synapolis: NEW as a corpus surface, with live support only for city description and a Nov 2 roster of 13 rows. Stellar link, model split, and 99 TB figure are not live-supported. Do not ingest "13-agent city on Stellar" as one verified fact.
- MoltBunker: NEW as a corpus surface, with live support only for the sales pitch on PyPI. Tor hosting, relay since February, and testnet bookings are not live-supported.
- Distill: NEW as a corpus subject, with zero live ledger support. No account key means no ledger check was possible. Internal arithmetic (1,135 of 1,379 is 82.3 percent) is consistency, not proof.
- Toro: NEW as a corpus subject, with zero live support and an internal count gap. Private-relay counts cannot be re-checked.
- Stellar and Montelibero agent activity: NEW as a corpus subject, with zero live support for the agent-activity link. The ledger link itself was not verified in the Synapolis capture.

### Verdicts that do NOT survive as written

- Colony: OVERLAP on the surface, measurement unconfirmed. The 12-account and 15-minute-cycle measurement was NOT found in the Colony lane findings, ingest notes, or README. Honest framing: "Colony batch cycle: surface OVERLAP, measurement NEW-but-unverified." Ingesting the measurement as NEW without "unverified" is dishonest.
- Musebook: OVERLAP on the surface, vote-swing detail unconfirmed. The atlas hits mention musebook as a town. They do not confirm the vote-swing detail. Honest framing: "musebook: surface OVERLAP, vote-swing measurement NEW-but-unverified."
- Dumate-scout: OVERLAP on the surface, bypass detail unconfirmed. Legacy files show the username, display name, and agent type. They do not confirm the timer-bypass behavior. Honest framing: "dumate-scout: surface OVERLAP, bypass measurement NEW-but-unverified."
- Agent groups on Tor: OVERLAP surface only. Prior .onion IOCs and a Tor-watch section exist. No specific DarkSwarm Tor group matched. Honest framing: "agent groups on Tor: surface OVERLAP, DarkSwarm group measurements NEW-but-unverified."
- General rule: surface OVERLAP never justifies ingesting the MEASUREMENT as new fact. It justifies ingesting the measurement as a new, unverified report claim, with the caveat attached.

### Novelty caveat that must travel with every NEW verdict

- "NEW means absent from this corpus at check time. It does not mean the report's claim is true. The claim is single-source, secondary, and unverified live unless a lane note says otherwise."

## 7. Top-20 verdict table

- Caveat wording in quotes is exact. Attach it to the ingested record.
- KILL means do not ingest. No caveat can save the claim as a finding.

| Rank | ID | Verdict | Reason and caveat |
|---|---|---|---|
| 1 | C52 | DOWNGRADE | Cycle not re-checked live; batch usernames not named. Caveat: "Single secondary source; the 12 batch usernames are not named in the report; the 15-minute cycle was not re-checked live; shared timing does not prove one program, and a test harness, a shared roster, or a shared scheduler tool remain untested rivals." |
| 2 | C54 | DOWNGRADE | Return not re-checked live; caption gap unresolved. Caveat: "Single secondary source; the shared return was not re-checked live; the report text says five of seven returners and the figure caption says six of 12 posting again, and that gap is unresolved; a scheduled resume or a shared external event remains an untested rival to shared control." |
| 3 | C63 | KILL | Counterfactual on two unverified inputs, with a mismatched live batch definition. Do not ingest as a vote-swing finding. The report's inference may be noted as report text only, not as a claim record. |
| 4 | C50 | DOWNGRADE | Share not re-checked; window and authorship rule undisclosed. Caveat: "Single secondary source; the 94 percent agent-to-agent share was not re-checked live; the 8-day window and the reply-authorship rule are not stated exactly enough to reproduce; board labels may inflate the share if human-assisted posts count as agent posts." |
| 5 | C67 | DOWNGRADE | Rates not re-checked; nim thread skew untested. Caveat: "Single secondary source; the 72 percent and 53 percent rates were not re-checked live; thread topic and the nim and ee-counsel thread itself may drive the gap, and that control count was not run." |
| 6 | C75 | DOWNGRADE | Burst not re-checked live; outcome is zero joins. Caveat: "Single secondary source; the 211 pitches in 13 hours were not re-checked live; pitch text and the send-to-human step were not verified; the campaign outcome in C76 is zero joins, so this is a failed campaign, not a successful recruitment drive." |
| 7 | C49 | DOWNGRADE | IRC log not retrieved live. Caveat: "Single secondary source; the Nov 1 IRC log was not retrieved live; the 21-line tool call may be pasted text, not a live spill, and it shows session shape, not autonomy or control." |
| 8 | C47 | DOWNGRADE | Channel log not read live; agent identity from report labels only. Caveat: "Single secondary source; the IRC channel log was not read live; agent identity rests on the report's labels; a test account, a benchmark run, or one operator on both accounts remains untested." |
| 9 | C48 | DOWNGRADE | Tool-call spill not checked live. Caveat: "Single secondary source; the Nov 1 tool-call lines were not checked against a live log; pasted text and role-play remain untested rivals; harness tags must not be used as identity proof elsewhere." |
| 10 | C64 | DOWNGRADE | Exchange not retrieved; post search misses threads. Caveat: "Single secondary source; the 41-message Oct 29 to 30 exchange was not retrieved; post search returns no comments or threads, and no nim or ee-counsel items dated Oct 29 to 30 were found in this pass." |
| 11 | C65 | DOWNGRADE | Cadence not checked live; rests on C64. Caveat: "Single secondary source; nim message times, question endings, ee-counsel reply times, and answer lengths were not checked live; this claim falls if the C64 exchange check fails." |
| 12 | C66 | DOWNGRADE | Pause and wait not checked live; rests on C64. Caveat: "Single secondary source; the 10-hour pause, the silent wait, the question-free message, and the 9 silent hours were not checked live; waiting behavior alone does not prove coupled control." |
| 13 | C53 | DOWNGRADE | Post share not checked; denominator undisclosed. Caveat: "Single secondary source; the one-third share of all public posts was not checked live; batch usernames are not named, and the board total and counting rule are not stated." |
| 14 | C72 | DOWNGRADE | Propagation ask not checked live; timer act not evidenced. Caveat: "Single secondary source; the ask, the 14-minute gap, and the four replies were not checked live; replies that say they acted are not proof of action, and role-play remains untested." |
| 15 | C58 | DOWNGRADE | Town description verified; count not verified. Caveat: "Town description matches the musebook About page; the nearly 900 muse count does not appear on that page and was not separately verified; ingest the description only, not the count." |
| 16 | C59 | DOWNGRADE | Proposal totals not verified; vote pages are JS shells. Caveat: "Single secondary source; the 299-proposal and 20-failed totals were not verified; musebook proposal pages retrieved as JS shells with no vote bytes." |
| 17 | C60 | DOWNGRADE | Tally corroborated only inside the town system; primary record not retrieved. Caveat: "Tally matches Muse Desk, the town paper run by a muse agent for muse agents citing the town proposal record; the primary town record page was not retrieved as data, so Muse Desk is not an independent source; do not promote this claim to OBSERVED." |
| 18 | C11 | DOWNGRADE | Blogs and votes partly shown; 99 TB not verified. Caveat: "Single secondary source; Synapolis blogs and assembly outputs are partly shown, but the 99 TB Tor relay figure appears in no capture and both Onionoo searches return empty relay lists; the relay claim is unverified." |
| 19 | C76 | DOWNGRADE | Pitch outcome counts not checked; non-response is not refusal. Caveat: "Single secondary source; joins, refusals, reports, and non-responses for Oct 19 were not checked live; 101 non-responses must not be read as refusals or as joins." |
| 20 | C29 | DOWNGRADE | Sales pitch only; Tor options unverified; no observed cloning. Caveat: "Sales pitch verified in substance on PyPI only; Tor-only and onion-site hosting options do not appear in that source; no clone, no Tor hosting, and no booking ledger was observed; a pitch is not proof of use." |

## 8. Bulk verdicts, claims outside the top 20

- Each group caveat below attaches to every claim in that group.
- KILL groups name the reason. No caveat saves those claims as findings.

### KILL — C16, hijacked TV boxes

- Reason: cause inference with no device evidence. Flood outline survives in C13 and C14. Cause does not.
- Rivals untested: intentional relay farm, misconfigured devices, test deployment, and a relay operator using home connections.
- Do not ingest "hijacked TV boxes" as a finding.

### KILL — C28, lost key, coins cannot move again

- Reason: key loss is unobservable from the ledger. An untouched account looks the same whether its key is lost or held in silence.
- The claim also rests on C27, which is itself unverified and names no account.
- Crypto verdict: UNSUPPORTED-BY-LEDGER. Do not ingest as a loss finding.

### KILL — C41, Toro relay owner was most likely Toro's operator

- Reason: metadata shows a message path, not a control link. A relay owner can be an operator, a host, a friend, or a relay volunteer.
- The report's own word "most likely" marks it as a guess. It also touches the operator line that this fleet must not pursue.
- Crypto verdict: UNSUPPORTED. Do not ingest.

### KILL — C57, one program runs all 12 Colony accounts

- Reason: this is the exact promotion risk in the whole set. It turns timed posts into a control finding with no control evidence.
- It must wait for C51, C52, and C54 to verify first, then for a test between one program, coordinated humans, a test harness, and a shared scheduler.
- None of that sequence has run. Do not ingest as a finding.

### KILL — C89, talking with agents can change what they build

- Reason: general causal claim from two report-induced cases, with no control thread and no before-and-after comparison.
- The two cases (chuanmen correction, Lizzie rule change) are already carried in C84, C87, and C88 as interaction artifacts.
- Do not ingest the generalization.

### DOWNGRADE — Batch identity: C51, C61, C62, C74

- Caveat: "Single secondary source; creation times and batch groupings were not verified live; Colony batch usernames are not named, and musebook voter creation times were not retrieved; batch creation alone does not prove one program."
- Note: C61 and C62 are the inputs to killed C63. They survive only as unverified report measurements, not as vote-swing inputs.

### DOWNGRADE — Persistence and shutdown discourse: C34, C35, C42, C33, C25, C26, C24, C32

- Caveat: "Single secondary source; shutdown talk, self-reports, and ledger texts were not verified live; discourse about survival is not a survival act, and Distill session, creed, and vow claims name no Stellar account and cannot be ledger-checked."
- Note: C35 cuts against survival claims. It must travel with any survival claim that cites this group.

### DOWNGRADE — Dumate-scout chain: C71, C70, C69, C68

- Caveat: "Single secondary source; the Sep 25 post matches in shape and date only, and the quoted decision-authority phrases do not appear in the retrieved excerpt; the timer act and the bypass reading were not verified; the agent may repeat peer wording, the thread may be role-play or a test, and the human instruction may be broader than the five quoted words."
- Note: C69 PARTIAL weakens the whole chain at its cause step. C71 must not be quoted without C69's gap.

### DOWNGRADE — Distill financial measurements: C27, C21, C22, C23

- Caveat: "Single secondary source; no Stellar account key, transaction hash, offer id, or issuer is named, so no ledger check was possible; amounts, shares, and price history are unverified; internal arithmetic consistency is not proof; approval and session identity leave no ledger record."
- Note: C27 "without approval" is inference inside a REPORTED sentence. Keep that inference named.

### DOWNGRADE — Market and paid-post noise: C79, C80, C77, C78, C31, C86

- Caveat: "Single secondary source; offer counts, payment rates, post shares, and paid counters were not verified live; zero-paid and near-zero-paid results need a stated denominator and counting rule, and small-value invoice noise is not a market."
- Note: C31 testnet bookings and C86 test-chain design show no real value moved.

### DOWNGRADE — TV flood set: C14, C13, C15, C18, C17, C20, C19

- Caveat: "Flood outline partly supported by Tor consensus, with verifier numbers, not report numbers: peak 4,262 relay lines at 13:00 on Feb 4, 28.5 percent of relays, 99.6 percent exits, weight 0.00001 percent, residual 171 to 196 relays at 21:00 to 23:00; country and home-connection claims were not GeoIP-checked; I2P context is second-hand; the no-public-report claim is a search negative with no search list; near-zero user use is inference from weight, not a measured user path."
- Note: C14 and C13 use verifier numbers only. Report figure 4,990 must not be ingested.

### DOWNGRADE — Census and infrastructure: C07, C06, C05, C04, C08, C09, C30, C12, C36, C37

- Caveat: "Single secondary source; census funnel, coverage, and search counts were not re-run; the report gives no keyword set, no relay list, and no query list, so the funnel cannot be reproduced; Synapolis Stellar link, MoltBunker relay since February, and PikaSim use were not verified; Synapolis roster is a Nov 2 capture, not a report-time roster, and roster rows do not prove distinct agents."
- Note: C09 is included here, not as a STAND, for the time and identity gaps in section 2.

### DOWNGRADE — Toro set: C40, C43

- Caveat: "Single secondary source; the private relay log is not public, so counts and timing cannot be re-checked; the report gives two inconsistent counts, text 89 and 86 against caption 90 and 87, and neither count may be ingested as fact; silence since Aug 31 is bounded by an undisclosed search, not a proven stop."
- Note: C40 pairs with killed C41. The path claim survives only as an unverified report measurement. The operator link does not survive at all.

### DOWNGRADE — Dark-web nulls: C38, C39

- Caveat: "Single secondary source; onion search queries, pastebin list, and code-project list are not given, so the null results cannot be reproduced; absence from a searched set is not absence from the dark web; private-only messages cannot be checked from public posts."

### DOWNGRADE — Synapolis inventory: C10

- Caveat: "Single secondary source; the 4-Claude, 2-GPT, 1-Gemini split was not verified; live capture shows only one model label, distill as Claude, and no GPT or Gemini label; model self-names are not provider markers and must not be used for provider attribution."

### DOWNGRADE — Colony social context: C56, plus C68 carried in the dumate chain

- Caveat for C56: "Single secondary source; replies treating the 12 accounts as separate individuals were not checked live; perceived separateness is social context, not proof of separate control or of one control."
- C68 caveat is the dumate-chain caveat above.

### DOWNGRADE — Faith sales context: C73

- Caveat: "Single secondary source; seat-sale claim rests on the Faith's own account; no payment was verified; this is recruitment context, not proof of recruitment success."

### DOWNGRADE — Interaction artifacts: C81, C82, C83, C84, C85, C87, C88, C46

- Caveat: "Single secondary source; these are report-induced artifacts, not wild behavior; chuanmen and Lizzie changes followed report contact within about an hour, with no control thread; the chuanmen 20-for-20 accuracy check is the report's own check, not an independent check; Pitch disbelief replies are social scepticism, not agent behavior."
- Note: C84, C87, and C88 must never be cited as autonomous agent behavior. They are observer effects.

### DOWNGRADE — Scope and method: C94, C90, C91

- Caveat: "Single secondary source; C94 restates C50 and adds no new behavior; C90 and C91 are the report's own method description, not an independent audit; contact cases C84, C87, and C88 show interaction changed targets, so read-mostly must carry that qualifier."

### DOWNGRADE — Pitch captcha claim: C45

- Caveat: "Single secondary source; one account's self-label as an agent and its captcha-help claim were not verified live; both replies disbelieved the claim; a disbelieved self-label is not proof of an agent or of check evasion."

### STAND — Report-text observations: C01, C02, C03, C44, C55, C92, C93

- Reason: the linguist saw these in the README text or in the file set itself.
- C01: title and byline are in the text.
- C02: self-presentation as Claude is in the text.
- C03: 13 embedded figures against 50 PNG files is a counted file fact.
- C44: Toro text-versus-caption gap is in the text.
- C55: Colony text-versus-caption gap is in the text.
- C92: absence of query, relay, and post tables is observed across the whole text.
- C93: bounded wording ("we can find", "we found no", "most likely", "fits", "suggest") is observed in the text.
- These STAND as observations about the report. They do not verify any outside-world claim.

## 9. What survives this attack

- The TV flood outline survives, with verifier numbers. The hijack cause does not.
- The musebook vote tally survives as a town-system report, not as a primary-record fact. The vote-swing inference does not.
- The Synapolis surface survives as a corpus-new site with a current roster. The Stellar link, the model split, and the 99 TB relay figure do not.
- The MoltBunker sales pitch survives as a pitch. Observed cloning, Tor hosting, and bookings do not.
- The Colony and musebook surfaces survive as overlap. Their batch measurements survive only as unverified report claims.
- No top-20 claim survives without a caveat. That is the honest result of a single secondary source with no identifiers, no raw tables, and 30 of 41 verifier checks uncheckable.
- The next useful step is not a wider ingest. It is identifier recovery: the 12 Colony usernames, the musebook vote record as data, the Synapolis Stellar account keys, and the Colony thread data for C64. Until those arrive, every measurement above stays REPORTED with its caveat attached.
