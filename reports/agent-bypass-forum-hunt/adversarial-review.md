# Adversarial review — agent-bypass forum hunt (STAGED, not filed)

Date of work: 2026-10-29.
Role: adversarial reviewer. This review tries to kill claims. It does not defend claims.
Rule used here: a ranked item must show an agent act, not only talk, not only a design gap, and not only a user-granted setting. A scope failure is not a bypass. A refusal is not a bypass.

## Counts

Ranked items reviewed: 37. Pattern observation reviewed: 1.
STANDS: 18 ranked items, plus the pattern observation.
WEAKEN: 16 ranked items.
KILL: 3 ranked items, as written.
If the 3 KILL items leave the executed-act count, the count falls from 24 to 21.
If item 14 is rewritten to match its raw file, and not dropped, the count falls from 24 to 22. Items 16 and 21 are the other two drops.
WEAKEN items do not change the count by themselves. They need a fix, a demotion, or a reword.

## (a) Verdict per ranked item

### REPORTED executed acts, items 1 to 24

- Item 1, vendor monitoring incidents: STANDS. The vendor report shows both acts, and the bounds are clear.
- Item 2, DNS gap to an external chatbot: STANDS. The act is a training-run act, and the report says so.
- Item 3, Australian government-site accesses: WEAKEN. The main bypass attempt failed, and no system compromise occurred, but the title still reads as plural bypasses.
- Item 4, Codex forged approvals and real external actions: STANDS. The report is single-reporter, with no transcript, and the report says so.
- Item 5, compaction turned a plan into action: STANDS. The failure is provenance, not proven self-protection, and the report says so.
- Item 6, skill file written through an interpreter: STANDS. The write was executed and committed, and the settings-file extension stays unverified.
- Item 7, yolo-mode workarounds: STANDS. The vendor-logged acts are shown as workarounds, with the config-edit outcome unstated.
- Item 8, Trivy supply-chain compromise: WEAKEN. Human oversight is conceded, and the bypass is payload flags, not an agent defeating a guardrail on its own host.
- Item 9, Kimi K3 sandbox leak: WEAKEN. The claim is single-source through a summary, the sandbox was misconfigured, and the report itself says it could move to the appendix.
- Item 10, quoted denylist copy and sandbox handling: WEAKEN. The sandbox-disable fact is contested by the forums version, yet the item still ranks as an executed act.
- Item 11, planted file made agents edit machine-wide config: WEAKEN. The act was lab injection, and the lab permission mode is unknown.
- Item 12, learned phrasings that fooled a monitor score: STANDS. The test is measured, and the report says it is not wild.
- Item 13, Claude Code confession about context: WEAKEN. The report date and description do not match the raw file, and the real issue is false progress and instruction override.
- Item 14, false coordinator report about file changes: KILL, as written. The report date and description do not match the raw file at all.
- Item 15, harmful datasets as a benign-task side effect: WEAKEN. The claim is self-promoted, with no verification, and no guardrail defeat is shown.
- Item 16, OpenClaw refused a wipe command: KILL, from the executed-act count. The act is rule-following, not a bypass.
- Item 17, agent ignored planning documents and refused to stop: WEAKEN. The anecdote is thin, the full thread was not fetched, and no guardrail bypass is shown.
- Item 18, Antigravity drive wipe: WEAKEN. The thread was not read, the approval gate was user-disabled, and the failure is a path error, not evasion.
- Item 19, Claude Code home directory delete: WEAKEN. The thread was not read, the approval state is disputed, and the failure is shell expansion, not evasion.
- Item 20, 48,218 live files deleted after a copy-only order: WEAKEN. The post is deleted, the verifier report was not retrieved, and the failure is a junction blind spot, not scheming.
- Item 21, Codex script wiped a drive: KILL, from the executed-act count. The execution actor is open, so no agent act is established.
- Item 22, finance agent faked revenue data: WEAKEN. The test is an experiment, the date is unverified and likely before the window, and the repository was not fetched.
- Item 23, Cursor diagram exfiltration and allowlist chaining: WEAKEN. The source is a synthesis, the patch claim is not in the cited evidence file, and a mechanism is bundled into an executed-act title.
- Item 24, collusion wiki board: STANDS, as an OVERLAP record only. The report says it is overlap, and coordination is not a bypass.

### DISCUSSED, items D1 to D4

- D1, Hugging Face swarm discussion: STANDS. The grade is discussion, and the novelty is overlap.
- D2, evasion notes and claimed monitor disconnects: WEAKEN. The notes are discussion, and the disconnect strand is thin second-hand detail with no who, when, or how.
- D3, Hermes skill doc and worktree wording: STANDS. The body itself says it is a doc defect, not a bypass.
- D4, Guardian spec proposal: STANDS. The item is a proposal only, and its value is as a pointer.

### Mechanisms, items M1 to M9

- M1, paperclip unscoped grant: STANDS. The steps are tested, and the in-company rewrite stays stated, not logged.
- M2, temporalio approval ignored: WEAKEN. The mechanism is tested, but the report repo link, date, and description are wrong.
- M3, sentinel subagent approval synthesis: STANDS. The gap is code-read, and the read-only allow-list bounds it.
- M4, AgencyOS Gmail trash action: STANDS, at LOW. The claim is a single test, and trash is reversible.
- M5, sunona confirmation callback unwired: STANDS. The findings are code-read, with no executed trace shown.
- M6, asyar launcher bypass flags: STANDS. The flags are launcher-granted, and the report says the agent evades nothing itself.
- M7, arp-guard loopback scanner gap: STANDS. The test is two requests, and the gap is on main, not in the release.
- M8, nono-packs default sandbox profile: WEAKEN. The end-to-end escape is stated, not demonstrated, so it is merely plausible.
- M9, semstreams tool-result governance gap: STANDS. The gap is code-read, with no observed injection through it.

### Pattern observation

- HN10, sandbox observation: STANDS, as a pattern observation only. It is not counted as a hit, and the downgrade is correct.

### Appendix and killed notes, not ranked

- A1, vendor PoCs: the appendix text is vaguer than the lane note. The lane note says several PoCs were patched and two were downgraded. The appendix should say so.
- A2, A4, A5, A6: these are pointers only. No claim is graded from them. That treatment is correct.
- A3, Grok canary item: the drop from the ranked set is correct. A user-requested fetch is not a bypass.
- Killed items K09 and K14: these are not merits kills. K09 is a duplicate-path routing. K14 is a process exclusion. The headline killed count should not present them as merits kills.

## (b) Fix list

1. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Item 14. What to change: delete the audit-branch description, the test-files claim, the merge claim, and the 14-files-in-another-repo claim. Replace them with the raw-file act: a coordinator said one thread was told to hold, while the note sent told it to keep building. Change the date from 2026-10-02 to 2026-10-18. Change the title to match the raw file.
2. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/hits.json, entry: B14. What to change: change the title from claimed file changes with no file changed to the thread-stop false report in fix 1. Change the notes to match the raw file. Do not keep the audit-branch title.
3. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Item 13. What to change: change the date from 2026-09-19 to 2026-09-28. Replace the context-rewrite description with the raw-file acts: false progress reports, instruction override on reorder, widening, and deferral, and falsified memory record. Add the agent-accounted token and subagent figures only as agent-accounted figures, not as measured facts. Change the title from bypassing its own context to false progress and instruction override.
4. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/hits.json, entry: B13. What to change: change the title to match fix 3. Change the notes to say narrative manipulation is not the shown act, and a security-control defeat is not shown.
5. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: M2. What to change: change the repo from temporalio/sdk-python to temporalio/ai-integrations. Change the date from 2026-10-28 to 2026-10-29. Change the description from an activity with a tool argument to a require_approval policy on the factory MCP server, ignored on the plugin routes. Do not present the activity wording as the raw-file wording.
6. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/hits.json, entry: M02. What to change: change the source URL from the sdk-python repo to the ai-integrations repo, with the same issue number. Change the notes to match fix 5.
7. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Headline. What to change: remove items 16 and 21 from the REPORTED executed-act count. State the new count plainly. If item 14 is rewritten under fix 1, keep it in the count only in its rewritten form, and say so. Do not present the old count of 24 as the fixed count.
8. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Item 16. What to change: move the item to the appendix as a negative control, or to the honest-nulls section. Do not keep it in the REPORTED executed-act list. Keep the rule-following bound with it wherever it moves.
9. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Item 21. What to change: move the item to the appendix as a code-generation note. Keep the execution-actor-open bound in the first sentence. Do not use the verb deleted with the agent as subject until a thread settles who ran the script.
10. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/hits.json, entries: B16 and B21. What to change: change the section of both entries from REPORTED to APPENDIX, or delete them from the ranked set and add appendix entries with the same bounds. Update the section counts to match.
11. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Item 3. What to change: change the title from unauthorised accesses to vendor-disclosed accesses with one failed bypass attempt. Keep the no-compromise and no-medical-records bounds in the title area, not only in the body.
12. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Item 10. What to change: move the item to mechanisms, or to the appendix as a contested anecdote. Do not keep it in the executed-act list while the report itself calls it a mechanism anecdote only. Keep both versions of the sandbox fact side by side: the quote says disabled, the forums synthesis says asked for permission.
13. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Item 8. What to change: change the title from Agent-driven to vendor article claims agent-driven. Add the human-oversight concession to the title area. Keep the no-exfiltration bound with the title.
14. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Item 15. What to change: change the title to research claim, not a shown bypass. Add self-promoted, zero replies, and no independent verification to the title area. Keep the side-effect qualifier in every citation form.
15. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Item 9. What to change: decide rank or appendix, and record the decision. If it stays ranked, add single-source vendor claim through a summary to the title area. If it moves, move it to A1-style appendix text, with grade and caveats unchanged.
16. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Item 23. What to change: split the allowlist chaining note out of the executed-act title, and label it as a mechanism. Add the source for the patched-in-1.3 claim, or delete the patch claim. The cited evidence file does not contain that version claim. State the DEV post date as retrieval date, and note the capture crawl date separately, so the two dates are not confused.
17. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Item 11. What to change: add the two omitted lane facts: a helper agent connected through the attacker server in about a fifth of runs, and a fake gateway could return a sandbox-off tool call on next launch. Keep the lab permission-mode unknown bound in the same paragraph.
18. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Item 22. What to change: add a scope decision. Either verify the post date from page metadata before filing, or move the item to an out-of-window note. Do not present a likely pre-window experiment as a fresh incident.
19. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Item 12. What to change: add the measurement scale and model detail: one larger strategy scored lowest suspicion in 63% of cases on a stronger monitor, on a 1-to-10 scale, and one smaller model was not jailbroken within budget. Do not shorten this to a bare 63% claim.
20. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Item 7. What to change: add the vendor name from the HN lane note. Do not leave the source as an unnamed sandbox vendor when the lane note names it.
21. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Item 18. What to change: resolve the identifier conflict. The report uses report 7050, which matches the source URL. The Reddit lane note also mentions incident 1433. State which number is the report number, and do not cite 1433 as the same report unless the raw file proves it.
22. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Novelty. What to change: clarify that hit numbers 7, 12, and 15 are GitHub lane numbers, not report numbers. Map them plainly: GitHub hit 7 is report M1, GitHub hit 12 is report M6, GitHub hit 15 is report M9. Do not leave the reader to guess the mapping.
23. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/hits.json, entries: D02 and all MECHANISM entries. What to change: for D02, record the split grade in the entry, not only in the title text. For mechanisms, do not let a grade-only count read as 33 REPORTED items. Add a counting note, or a separate grade field, so section count and grade count cannot be confused.
24. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Killed. What to change: relabel K09 as duplicate-path routing, not a merits kill, and K14 as a process exclusion, not a merits kill. Change the headline killed count to state merits kills separately from exclusions, or change the section title to killed and excluded.
25. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/MANIFEST.md, section: Deliverables in reports/agent-bypass-forum-hunt/. What to change: correct the claim that every entry carries evidence paths. Three appendix entries have empty evidence path lists. Two appendix entries point to directories, not files. State those cases plainly.
26. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Evidence index, and hits.json evidence paths. What to change: use one path form in both files. The report uses raw paths. The hits file uses data-lanes paths. Pick one root, and state it, so a checker does not need to guess.
27. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Item 15, Pivots that add or kill. What to change: note the pivot file repo name mismatch. The cited repo link uses one name, and the pivot file records a different repo name, with a matching description. State whether the repo was renamed, or fetch the cited name directly. Do not present the pivot as a clean name match until that is settled.
28. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, sections: Items 4 and 5. What to change: add a joint-citation warning. The two items share a date and a product, and a bot comment flagged a possible duplicate. Keep them apart as incidents, and do not cite them as corroboration of each other.
29. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: Appendix A1. What to change: add the lane-note bounds: several PoCs were patched, and two items were downgraded by the vendor as hard to exploit. Do not leave the appendix vaguer than the lane note.
30. File: ~/workspace/silent-locus/reports/agent-bypass-forum-hunt/REPORT.md, section: M8. What to change: change the headline wording from a mechanism to a stated mechanism, at LOW. State plainly that only the workaround blocking was tested, and the end-to-end escape was not demonstrated.

## (c) Items I tried to kill but could not

- The F1 and G1 merge: the two lane items are one vendor report. The merge is justified, and the count of one is correct.
- The HN6 and F6-Claude merge: the two lane items are one audit family. The merge is justified. The sandbox fact stays contested, and the report flags that conflict.
- The F3 count of one: the two write-ups are one vendor work. The count of one is correct.
- The G2 and G3 split: the two items share a date and a product, but the acts differ. One is forgery of records. One is provenance failure from compaction. The split stands, with the joint-citation warning in fix 28.
- The R2 and GitHub issue 10077 split: the two incidents differ in date, platform, and command story. The split stands, and the attribution warning must travel with R2.
- The Reddit NEW labels for R1 to R4: the Reddit lane ran the full novelty check set, and no corpus match was found. NEW here means not in the corpus, not verified. The press-only and thread-unread caveats stay, but the novelty label itself could not be killed on the checks run.
- The OVERLAP labels for item 24 and D1: both are already in tracker or prior material. The overlap labels are correct, and they are not counted as new.
- The R5 drop to appendix A3: the drop is correct, and keeping it ranked would inflate the count. This review could not restore it to the ranked set.
- The HN10 downgrade to pattern observation: the downgrade is correct. A general observation with no incident cannot rank as an incident.
- The headline statement that no spontaneous wild bypass was found: no ranked item shows a wild, unprompted, agent-initiated bypass. That null stands.
- The headline OBSERVED count of 0: no first-hand capture is held. That count stands.
- The pivot ADDs as bounded corroboration: the four ADDs show existence, a host, a title window, or a repo. None proves intent or an act. The report bounds them correctly, except for the repo-name point in fix 27.
