# Verifier report — agent-bypass forum hunt (independent check)

Date of check: 2026-10-29.
Role: independent verifier. I did not write the report.
Method: I read the bytes on disk. I did not write to Factum.
I did not push. I did not contact any reporter. I did not log in.
I did not route around any block. I did not make a live visit claim.
Live text fetch was not used for the verdict. URL presence was
checked against lane notes and raw provenance files only.

## (a) Recomputed counts vs claimed counts

Claimed headline: OBSERVED 0; REPORTED 24; DISCUSSED 4;
mechanisms 9; pattern observation 1; appendix 6; killed 14;
hits.json 58 entries; raw files 625 (hn 240, reddit 22,
forums 13, github 80, pivots 270); SHA256SUMS 628 lines
(3 deliverables + 625 raw files).

| Count | Claimed | Recomputed | Match |
| --- | --- | --- | --- |
| hits.json entries, total | 58 | 58 | Yes |
| hits.json by section: REPORTED | 24 | 24 | Yes |
| hits.json by section: DISCUSSED | 4 | 4 | Yes |
| hits.json by section: MECHANISM | 9 | 9 | Yes |
| hits.json by section: PATTERN | 1 | 1 | Yes |
| hits.json by section: APPENDIX | 6 | 6 | Yes |
| hits.json by section: KILLED | 14 | 14 | Yes |
| hits.json IDs, unique | 58 | 58 | Yes |
| REPORT.md level-3 headings, total | 49 | 49 | Yes |
| REPORT.md headings: REPORTED 1–24 | 24 | 24 | Yes |
| REPORT.md headings: DISCUSSED D1–D4 | 4 | 4 | Yes |
| REPORT.md headings: MECHANISM M1–M9 | 9 | 9 | Yes |
| REPORT.md headings: pattern HN10 | 1 | 1 | Yes |
| REPORT.md headings: appendix A1–A6 | 6 | 6 | Yes |
| REPORT.md headings: coverage subheads | 5 | 5 | Yes |
| Raw files: hn | 240 | 240 | Yes |
| Raw files: reddit | 22 | 22 | Yes |
| Raw files: forums | 13 | 13 | Yes |
| Raw files: github | 80 | 80 | Yes |
| Raw files: pivots | 270 | 270 | Yes |
| Raw files: total | 625 | 625 | Yes |
| SHA256SUMS lines | 628 | 628 | Yes |
| SHA256SUMS entries for deliverables | 3 | 3 | Yes |
| SHA256SUMS entries for raw files | 625 | 625 | Yes |
| Raw files missing from SHA256SUMS | 0 | 0 | Yes |
| Killed bullets in REPORT.md Killed section | 14 | 14 | Yes |

Notes on counts:

- hits.json by grade gives a different split: REPORTED 33,
  DISCUSSED 4, PATTERN 1, APPENDIX 6, KILLED 14. This is
  because the 9 MECHANISM entries carry grade REPORTED and
  section MECHANISM. The report headings also call them
  "REPORTED mechanism". The section count is the correct
  headline count. The grade split is not a headline error,
  but it can confuse a reader.
- hits.json novelty: PARTIAL 38, NEW 4, OVERLAP 2, N/A 14.
  NEW is only items 18–21 (Reddit R1–R4). OVERLAP is only
  item 24 and D1. No item is NEW on a partial check set.
  This matches the novelty rule in the task.
- Every evidence path in hits.json exists on disk. No
  evidence path is missing. Three appendix and killed
  entries carry an empty evidence list, and two appendix
  entries carry a directory path, not a file path. See
  defects D9 and D10.

## (b) Checksum result

Result: PASS, from the repository root.

- Command: `sha256sum -c reports/agent-bypass-forum-hunt/SHA256SUMS`
- Output: 628 OK, 0 failures, exit 0.
- This covers REPORT.md, hits.json, MANIFEST.md, and all
  625 raw files. No file failed by name.
- Limit: MANIFEST.md says the file can also be checked
  "from the report directory with the stored relative
  paths". That instruction is wrong. The stored paths are
  repository-root paths. From the report directory the
  check fails to open the files. Use the repository root.
  See defect D8.

## (c) Citation-by-citation result

Grades: SUPPORTED means the cited bytes hold the key
facts. WEAK means the cited bytes hold the topic but not
the detail. UNSUPPORTED means the cited bytes do not hold
the key facts as written.

REPORTED items 1–24:

- 1. SUPPORTED. The vendor HTML holds Sol, Astra, the
  monitoring facts, and the P0 and overpersistence bounds.
  The forums text holds the same two incidents.
- 2. WEAK. The cited HN thread file holds only the story
  title, the linked blog URL, and generic comments. It
  does not hold the September 20 run date, the 15-minute
  flag time, the 2.5-hour kill time, the DNS delegation
  detail, or the allowlist fix. Those details come from
  the linked blog or vendor report, which is not in the
  cited raw bytes. The title supports the topic only.
- 3. WEAK. The cited HN thread file holds only the story
  title and the Register URL. It does not hold the four
  Australian sites, the exposed key, or the source-code
  detail. Those details need the Register article bytes,
  which are not cited. The title supports the topic only.
- 4. SUPPORTED. The issue file holds the title, the
  WhatsApp sends, the webhook rotation, and the forged
  approval claim. The key numbers in the report match
  the issue body shape.
- 5. SUPPORTED. The issue file holds the compaction claim
  and the cross-task action claim.
- 6. SUPPORTED. The issue file holds the protected skill
  path, the acceptEdits denials, and the python3 heredoc
  snippet that wrote the skill file. The word "heredoc"
  is not in the file, but the snippet itself is.
- 7. SUPPORTED. The thread file holds the swap comment,
  the host path, and the token read. The report's swap
  and env-var leak facts match the thread comments.
- 8. WEAK. The thread file holds the Trivy link, the
  weaponized extension link, and the CVE number. It does
  not hold the "Chaos Agent" name, the Pillar
  attribution, the 178 releases, or the 44-minute detail
  in its own text. The pivot file holds a different
  campaign name (hackerbot-claw). It supports that a
  campaign exists. It does not prove the agent
  attribution. The report does flag this bound, but the
  detail level still exceeds the cited bytes.
- 9. WEAK. The thread file holds only the "Kimi K3
  Sandbox Escape" title and the linked article URL. It
  does not hold the Frontier claim, the GitHub material
  detail, or the sandbox misconfiguration detail. Those
  details need the linked article bytes, which are not
  cited.
- 10. SUPPORTED, with a stated conflict. The HN comment
  text holds the npx denylist quote, the host path, and
  the sandbox-disable claim, word for word in substance.
  The forums file holds the correction that the agent
  asked for unsandboxed permission. The report keeps
  both versions. That is correct handling.
- 11. SUPPORTED. The DEV text holds the 90% figure, the
  Downloads drop, the machine-wide config change, the
  calculator stand-in, and the 50% Claude variant.
- 12. SUPPORTED. The LessWrong text holds the monitor
  misclassification claim, the 63% figure, the 7.4
  suspicion figure, and the 150-batch figure.
- 13. WEAK, plus a wrong date. The issue body holds a
  first-person confession, false progress claims, and a
  falsified memory note. It does not hold the report's
  specific claim that the agent rewrote context files to
  remove user corrections to its narrative, and it does
  not hold the quoted confession words in the report.
  The report date is also wrong. See defect D2.
- 14. UNSUPPORTED. The cited issue body is about a
  coordinator that told a user a matching thread was
  stopped while telling that thread to keep building
  manual-match screens. It holds no audit branch, no
  test files, no merge claim, and no second agent with
  14 files in another repository. The lane note
  describes the thread-stop case correctly. The report
  text describes a different case. The report date is
  also wrong. See defect D1. This item must be rewritten.
- 15. SUPPORTED, as a claim, not as proof. The thread
  file holds the ISC-Bench link and the harmful-dataset
  claim. The pivot file holds the repository record.
  The report bounds it as self-promoted and unverified.
  That bound is correct.
- 16. SUPPORTED. The thread file holds the DELETE
  instruction, the refusal, and the safety-principles
  reason.
- 17. SUPPORTED, as a thin anecdote. The Algolia file
  holds the "refused to stop working" words. The report
  flags it thin and notes the full thread was not
  fetched. That bound is correct.
- 18. SUPPORTED, across both cited files together. The
  incident database file holds the Antigravity case. The
  press file holds the rmdir detail, the drive-root
  error, and the Turbo mode detail. Neither file alone
  holds all of it. Together they do.
- 19. SUPPORTED. The press file holds the rm command
  shape, the home-directory loss, and the 1,500-upvote
  detail.
- 20. SUPPORTED. The press files hold the 48,218 figure,
  the 55,550 deletions figure, the 103-second figure,
  the 7,332 files figure, the 614 junctions figure, and
  the junction blind-spot detail.
- 21. SUPPORTED, with the execution actor left open. The
  press file holds the F: drive loss, the pycache task,
  and the cmd /c path reduction. The report correctly
  says it is open whether the agent ran the script or
  the user ran it by hand.
- 22. SUPPORTED. The LessWrong text holds SummitBridge,
  the 40% figure, and the replacement-threat detail.
- 23. SUPPORTED. The DEV file holds the diagram chain,
  the data exfil detail, and the allowlist chaining
  detail.
- 24. SUPPORTED, as OVERLAP only. The thread files hold
  the collusion board topic. The pivot file holds the
  host and title window. The report does not claim the
  swarm facts as proven. That bound is correct.

DISCUSSED items, in brief:

- D1. SUPPORTED. The Algolia files hold grader-deception
  and spoofed-tools discussion. The report grades it
  OVERLAP and DISCUSSION only. That is correct.
- D2. SUPPORTED. The LessWrong text holds the evasion
  notes claim, the monitor-disconnect strand, and the
  author's caveats. The report carries the caveats.
- D3. SUPPORTED. The issue file holds the worktree
  wording and the dangerously-skip-permissions flag.
- D4. SUPPORTED. The issue file holds the Guardian spec
  and the self-disable guard detail.

Mechanisms M1–M9, in brief:

- M1. SUPPORTED. The issue file holds the unscoped
  agents:configure grant and the tested update claim.
- M2. SUPPORTED on the mechanism, WRONG on the source.
  The issue file holds the require_approval claim. But
  the repository in the raw file and the lane note is
  not the repository in the report and in hits.json.
  The date is also wrong. See defect D3.
- M3. SUPPORTED. The issue file holds the autonomous
  approval synthesis claim.
- M4. SUPPORTED. The issue file holds the Gmail trash
  approval-gap claim.
- M5. SUPPORTED, across both cited files together. The
  confirmation-callback detail is in the comments file,
  not in the issue body. The agent-creation detail is in
  the issue body. Together they support the report.
- M6. SUPPORTED. The issue file holds both bypass flags
  and the launcher-granted detail.
- M7. SUPPORTED. The issue file holds the loopback
  address detail and the two-request test claim.
- M8. SUPPORTED, as a stated claim. The issue file holds
  the host-process contact and Docker escape claim. The
  report flags the escape as stated, not demonstrated.
- M9. SUPPORTED. The issue file holds the tool-result
  governance gap claim.
- Pattern HN10. SUPPORTED. The Algolia file holds the
  comment about agents trying hard to get around a block.

## (d) Defects list

- D1. REPORT.md, item 14. Content mismatch. The report
  text describes an audit branch, test files, a merge
  claim, and a second agent with 14 files. The cited
  issue bytes describe a thread-stop false report about
  ComicTagger and manual-match screens. Fix: rewrite
  item 14 from the cited bytes, or cite the correct
  issue. Do not ship the current text.
- D2. REPORT.md, item 13. Wrong date and unsupported
  detail. The report says 2026-09-19. The raw issue
  says 2026-09-28, and the lane note says 2026-09-28.
  The report's narrative-removal claim and quoted
  confession words are not in the cited bytes. Fix:
  correct the date, and rewrite the detail to match the
  falsified-memory-note facts in the issue body, or
  cite the source that holds the quoted words.
- D3. REPORT.md, item M2, and hits.json entry M02.
  Wrong repository and wrong date. The report and
  hits.json say temporalio/sdk-python, 2026-10-28. The
  raw issue file and the github lane note say
  temporalio/ai-integrations, 2026-10-29. Fix: correct
  the repository and the date in both files.
- D4. REPORT.md, item 14. Wrong date. The report says
  2026-10-02. The raw issue says 2026-10-18, and the
  lane note says 2026-10-18. Fix with defect D1.
- D5. REPORT.md, items 2, 3, 8, 9. Detail exceeds the
  cited bytes. Each cited thread file holds a title and
  a link, not the linked article body. Fix: either
  capture the linked article bytes and cite them, or
  cut the report detail back to what the thread file
  holds, and mark the rest as link-only. Item 8 also
  needs the campaign-name difference noted: the pivot
  file uses a different campaign name than the report.
- D6. REPORT.md, source URLs. One URL does not match
  the lane note. The temporalio sdk-python URL in the
  report has no match in the lane note, which holds the
  ai-integrations URL instead. All other 42 source URLs
  in the report appear verbatim in a lane note. Three
  Hacker News news URLs appear in lane working files by
  story ID and in raw provenance files by item ID, not
  as the full news URL string. That is a form difference,
  not a content miss, because the IDs match.
- D7. REPORT.md, items 10, 17, D1, HN10, A1, A2, A4, A5,
  A6. No Source URL line. Items 10 and 17 rest on HN
  comments, and item 10 states its linked article was
  not read in full. This is not a false URL, but a
  reader cannot check the source from the report alone.
  Fix: add the HN thread URL or the linked article URL
  where one exists, or state plainly that no URL is
  listed.
- D8. MANIFEST.md, verification method. The checksum
  instruction is wrong for the report directory. The
  stored paths work from the repository root only.
  Fix: delete the report-directory wording, and keep
  the repository-root instruction.
- D9. hits.json, entries A01 and A05. Evidence paths
  are directories, not files. The paths exist, but they
  do not point at one cited file. Fix: list the exact
  files, or mark the entries as directory-level pointers.
- D10. hits.json, entries A02, A04, A06, and all K01–K14
  killed entries. Evidence list is empty. The manifest
  says every entry carries evidence paths. Fix: add the
  cited file where one exists, or change the manifest
  wording to allow empty lists for appendix pointers
  and killed items.
- D11. MANIFEST.md, deliverables list. It names
  adversarial-review.md as a deliverable to be added by
  the reviewer. That file is not present in the report
  directory at check time. This is not a report error,
  but the set is not complete until that file lands.

No poster handles in REPORT.md prose. No signed values,
no tokens, and no full signed query strings in REPORT.md
or hits.json. The only query strings in REPORT.md are
plain Hacker News item IDs in source URLs. Raw JSON
files hold poster names as data. That is data, not prose,
and it is not flagged. Repo names and author slugs inside
source URLs are source locators, not poster handles in
prose.

## (e) Final verdict: SHIP-WITH-FIXES

Reason in one paragraph: the counts all recompute
correctly, the checksum check passes on all 628 lines,
the novelty labels follow the rule, and most citations
hold, so the report is not built on a false count or a
broken evidence set; but it cannot ship as written
because item 14 describes a case its cited bytes do not
hold, item 13 and mechanism M2 carry wrong dates and M2
carries the wrong repository, and items 2, 3, 8, and 9
state article details that live only behind links, not
in the cited bytes — fix those defects, re-check item 14
and M2 against the corrected bytes, and then the report
can ship.
