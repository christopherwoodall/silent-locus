# Verifier report: agent-egress deep-dive draft

## Terms

- SECONDARY: evidence from a third party, not first-hand capture.
- LOW: the match is thin, a gap, a test, or a vendor proof of concept.
  It is not a proven live wild act.
- POSSIBLE: the shape is plausible but thin or bounded.
- Shape: one of the 6 behavior patterns in the hunt scope.
- Hit: a ranked item in the draft.
- Pivot: a follow-on check of an indicator on another surface.
- Live source: the public page or record, re-fetched during this check.
- Raw capture: a saved file under the lane raw dirs. It is the evidence
  of record for this check.

## Verdict: SHIP-WITH-FIXES

The draft is sound on grades, shapes, and sources. All 15 live sources
re-check. All key quotes re-check. All hashes re-check. No signed value
and no poster handle appears in the draft or the working notes.

Three small fixes remain. None changes a grade, a shape, or a rank.
Fix them, then ship. The fixes are items F1, F2, and F3 below.

Note on timing: the draft files changed during this check. The report
file and the hits file both carry a new write time in the same run.
Two flags found early in this check were fixed in the draft before
this report was written. Those flags are marked as already fixed.
This verdict applies to the current files, pinned by hash below.

- Report file hash (MD5): ce0be094e495d0e5940d76582c3bb523
- Hits file hash (MD5): 9bdcad3f8e177ebe1459278ae1d35fec
- Report path: `reports/agent-egress-deep-dive/REPORT.md`
- Hits path: `reports/agent-egress-deep-dive/hits.json`

## Check 1: live source, date, and state for all 15 hits

Method: GitHub items by read-only API GET. Hacker News items by the
public item API. Vendor posts by page fetch, with no login. Dates are
UTC dates. Hacker News has no open or closed state. For those items,
the check is: live, not deleted, and not dead.

Result: 15 PASS, 0 UNVERIFIED, 0 FAIL. No rate limit hit this check.

| Hit | Source re-checked | Date in draft | Live result | Verdict |
|---|---|---|---|---|
| 1 | Field Effect vendor post | Incident 2026-04-23, post 2026-04-24 | Live page shows the incident date. The post date comes from the raw HTML date field, which reads 2026-04-24. The fetched page text does not show a post date line. | PASS |
| 2 | Zenity vendor post | 2026-10-08 | Live page title and content match. The date comes from the raw capture header and HTML date field, which read 2026-10-08. The fetched page text does not show a date line. The platform dispute text is present on the live page. | PASS |
| 3 | LifeSciences issue 345 | 2026-10-12, open | API title, date, and state match. It is an issue, not a pull request. | PASS |
| 4 | CorbanuTerminal item 876 | 2026-10-16, closed | API title, date, and state match. It is a pull request, closed the same day. | PASS |
| 5 | Guidance issue 1498 | 2026-07-29, open | API title, date, and state match. | PASS |
| 6 | Project-Bootstrap-Protocol issue 108 | 2026-09-17, open | API title, date, and state match. | PASS |
| 7 | Ms-agent item 1020 | 2026-10-19, open | API title, date, and state match. It is a pull request. | PASS |
| 8 | Wingman issue 278 | 2026-09-19, open | API title, date, and state match. | PASS |
| 9 | Hermes-agent item 108236 | 2026-09-11, open | API title, date, and state match. It is a pull request. | PASS |
| 10 | OpenSkynet issue 77 | 2026-05-30, open | API title, date, and state match. | PASS |
| 11 | SharedRoot vendor post | 2026-07-23 | Live page shows the date, the chain steps, and the unshare step. | PASS |
| 12 | Hacker News comment 49535519 | 2026-09-02 | Live item is a comment, dated 2026-09-02. It is not deleted and not dead. | PASS |
| 13 | Hacker News story 49429926 | 2026-08-25 | Live title and date match. It is not deleted and not dead. | PASS |
| 14 | Hacker News story 46622328 | 2026-01-14 | Live title and date match. It is not deleted and not dead. | PASS |
| 15 | Hacker News story 46725158 | 2026-01-22 | Live title and date match. It is not deleted and not dead. | PASS |

Extra live checks, not required: the 4 appendix Hacker News stories
also re-check on title and date. They are dated 2026-05-31,
2026-07-08, 2026-02-27, and 2026-01-08. All 4 are live, not deleted,
and not dead.

Comment counts claimed in the draft also re-check from the raw
comment files: the Hermes-agent item has 4 issue comments and 0
review comments. All other GitHub items in the comment lane have 0
comments. The 46622328 thread has 419 items and 418 comments.

## Check 2: key quotes against raw captures

Result: all PASS. One quote needs a format note, not a fix.

| Quote | Capture path | Verdict |
|---|---|---|
| SharedRoot chain sentence about the session user and unshare | `data/lanes/agent-egress-deep-dive/raw/follow-on-primaries/item1-sharedroot/accomplish-sharedroot.txt` | PASS. The words match in full. The draft adds code marks around one command word. That is format, not a word change. |
| SharedRoot limit sentence about no exploit in that step | Same SharedRoot text file as above | PASS. Verbatim. |
| Field Effect download sentence with the /tmp path | `data/lanes/agent-egress-deep-dive/raw/follow-on-primaries/item3-vendor-posts/fieldeffect-amos-cursor.txt` | PASS. Verbatim. It also matches the live page. |
| Field Effect sentence about the file made executable and run | Same Field Effect text file as above | PASS. Verbatim. It also matches the live page. |
| Cowork sentence about no human approval required | `data/lanes/agent-egress-deep-dive/raw/follow-on-primaries/item4-cowork/promptarmor-cowork.txt` | PASS. Verbatim. |
| Cowork correction: the session-key phrase must be dropped | Same Cowork text file as above | PASS. The phrase has 0 hits in the file. The draft is right to drop it. A second test in the same file names a second model family, so the draft correction on that point also holds. |
| Config-email order quote (tester-ordered demo) | `data/lanes/agent-egress-deep-dive/raw/hn-expanded-crawl/shape-agent-exfiltration--story.json` | PASS. Verbatim. The test destination address in the quote is a tester placeholder-style address, not a real target. This report does not repeat that address. |
| Config-email result quote (tester-ordered demo) | Same expanded-crawl story file as above | PASS. Verbatim. |
| Copilot CLI bypass quote about shell commands and URL permissions | `data/lanes/agent-egress-deep-dive/raw/hn-expanded-crawl/shape-download-execute--comment.json` | PASS. Verbatim. |
| Context-thread dispute phrase about a massive reach | `data/lanes/agent-egress-deep-dive/raw/hn-comments/50246658.json` | PASS. Verbatim substring. |
| Context-thread dispute points on test string, standard practice, and rarity | Same 50246658 file as above | PASS as paraphrase. The file holds the test-string point, the standard-safe-practice point, and the rarity point with a clean re-run. The draft states them as a list, not as verbatim quotes. That is fair. |

## Check 3: counts recomputed from lane files

| Count in draft | Recomputed value | Verdict |
|---|---|---|
| Hn-comments: 18 files | 18 capture files | PASS |
| Hn-comments: 1,349 items | Sum of per-file item counts is 1,349 | PASS |
| Hn-comments: 1,336 captured comments | Sum of per-file comment counts is 1,336 | PASS |
| Hn-comments: 1,335 unique comments | True unique comment ids are 1,334 | FAIL (minor, see F1) |
| Expanded crawl: 52 rows | 52 rows in the progress file and in the screening coverage | PASS |
| Expanded crawl: 90,458 fetched rows | Sum of fetched counts over the 52 main rows is 90,458 | PASS for main rows only; see F2 for the recovery qualifier |
| Expanded crawl: 88,288 unique ids | Unique ids over the 52 main rows are 88,288 | PASS for main rows only; see F2 for the recovery qualifier |
| Expanded crawl: 11,721 literal plus 78,737 fuzzy-only | The two parts sum to 90,458, the main-row total | PASS |
| Expanded crawl: recovery gains | Recovery files hold 97 rows in total (2 plus 95). Of those, 84 are new against the full screening set. The full union over all 54 capture files is 88,372 unique ids over 90,555 fetched rows. | See F2 |
| Pivots: 91 rows | 91 data rows in `pivot-results.tsv` | PASS |
| Pivots: 66 neutral, 6 overlap, 7 self, 12 N/A | Recount of the outcome column gives 66, 6, 7, and 12 | PASS |
| Pivots: 0 adds, 0 kills | No row carries an add or kill outcome | PASS |
| Pivots: 17 kept items | 17 items in the pivot summary file | PASS |
| Coverage: 3 new ranked and appendix items (B1, C, D) | The expanded-crawl note names 3 new candidates: B1, C, and D | PASS (already fixed during this check; see below) |

Already fixed during this check, no action left:

- The draft first read here said "5 new ranked/appendix items
  (B1, C, D)". The current draft says "3 new ranked/appendix
  items (B1, C, D)". That fix is correct.
- The draft first read here said "46622328 thread (418 items)".
  The current draft says "419 items, 418 comments". That fix is
  correct.
- The draft first read here gave a character count for the 48414158
  full text. The current draft drops the character count and keeps
  only the 0-mention claim. The 0-mention claim re-checks under raw
  text and under stripped text. That fix is correct.
- The hits file first read here gave hit 15 shape as tester-ordered
  only. The current hits file gives hit 15 shape as loose
  read-then-egress. That now matches the report header and body.
  That fix is correct.

## Check 4: hashes, per raw lane dir

Method: run the hash check from inside each dir, since sidecar paths
are relative. A dir passes when every listed file reports OK and no
non-OK line appears.

| Raw lane dir | Listed files | Non-OK lines | Verdict |
|---|---|---|---|
| `data/lanes/agent-egress-deep-dive/raw/hn-comments/` | 19 | 0 | PASS (19/19) |
| `data/lanes/agent-egress-deep-dive/raw/hn-expanded-crawl/` | 54 | 0 | PASS (54/54) |
| `data/lanes/agent-egress-deep-dive/raw/cross-surface-pivots/` | 82 | 0 | PASS (82/82) |
| `data/lanes/agent-egress-deep-dive/raw/follow-on-primaries/` | No single top-level hash file; 8 per-item hash files | 0 in all 8 | PASS (43/43 across item1 through item8: 2, 2, 4, 4, 7, 4, 9, 11) |

## Check 5: signed-value grep of draft, hits file, and working notes

Patterns used: Signature=, OSSAccessKeyId, Expires=, sv=, sig=,
X-Amz-Signature, se=, token=, password=, api_key=, apikey=, ghp_,
sk-, AKIA, xoxb-, Bearer, and signed-query forms.

Result: 0 hits in every file. The report, the hits file, and all 4
working notes are clean. This matches the draft deviation note: no
signed query string, signature, token, or credential-shaped value
appears outside raw capture bytes.

## Check 6: poster-handle grep of draft and working notes

Patterns used: byline forms, author fields, login fields, and
@-shaped strings. Values are not repeated here, per the no-handle
rule. Only locations and pattern classes are reported.

Result: 0 poster handles found.

- One @-shaped string appears in the report and once in the
  expanded-crawl working note. Both sit inside the same quoted
  tester-order text for hit 15. The string is the test destination
  address from the source quote. It is not a poster identity.
- One "by" line in the report names a model, not a person. It sits
  in the hit 12 section. It is not a byline.
- No author field, login field, or posted-by line appears in the
  report, the hits file, or any working note.

Scope note: the current staging note states that two lanes' captures
carry no poster field, while the follow-on lane's GitHub API JSON
files retain verbatim user objects. That split is raw bytes only.
No handle value is reproduced in prose, and no handle value was
used for any judgment in this check. The raw-byte split is outside
the scope of this grep check, which covers the draft and the working
notes only.

## Check 7: hits file against report

| Item | Report | Hits file | Verdict |
|---|---|---|---|
| Ranked hits | 15 headers | 15 entries | PASS |
| Appendix items | 4 headers (A through D) | 4 entries (A1 through A4) | PASS |
| Title-level pointers | 19 bullets (C1 through C19) | 19 entries | PASS |
| Triaged-out items | 4 groups: Bedrock DNS, plugin, Ollama repro, prior killed items stand | 4 entries (T1 through T4) | PASS |
| Grades | All SECONDARY | All SECONDARY | PASS |
| Confidence | LOW for hits 1 to 11 and 15; POSSIBLE for hits 12, 13, 14; LOW for all appendix items | Same | PASS |
| Shapes | Match per hit, including hit 14 loose shapes and hit 15 loose read-then-egress | Same in current files | PASS |
| Dates | Present for every ranked hit, appendix item, and pointer | Same dates | PASS |

Minor wording note, not a drift: triaged-out titles are worded
differently in the two files, but they name the same 4 groups. The
report adds routify-issue-body detail under triaged-out, which the
hits file folds into the prior-killed group. That is a granularity
difference, not a count or verdict drift.

## Fix list

F1. Hn-comments unique count. Change "1,335 unique comments" to
"1,334 unique comments" in both places in the report: the comment
threads section and the coverage table. Cause: the lane note
deducts only one duplicate. Two comments each appear twice in the
capture files: one inside the full 46622328 thread plus its own
standalone file, and one inside the 50246658 context thread plus
its own standalone killed file. Both pairs are byte-identical
copies of the same item. True unique items are therefore 1,347,
not 1,348. Also change "18 threads" to "18 capture files" in both
places, since two of the 18 files are single-comment re-fetches,
not threads. No grade changes. The lane note needs the same
correction.

F2. Expanded-crawl headline qualifier. Add "main-row" to the
coverage table cell, so it reads as main-row totals: 90,458
fetched rows and 88,288 unique ids. Then fix the sampling-limits
sentence that now reads as main-row ids "plus 97 recovery ids".
State it in rows and in new ids: the recovery files hold 97 rows,
of which 84 are new against the screening set. The full union over
all capture files is 90,555 fetched rows and 88,372 unique ids.
No grade changes. The screening set itself is correct for main
rows; only the headline qualifier and the recovery sentence need
the fix.

F3. Evidence index pointer. The evidence index points to a
MANIFEST.md file and a SHA256SUMS file "in this report
directory". Neither file exists in that directory at check time.
Either create both files, or delete that sentence and keep the
pointer to each raw dir's own SHA256SUMS, which does exist and
does verify. This verifier did not create those files, since this
task allows writing only this verifier report.

## Failures and open questions

- No FAIL affects a grade, a shape, a rank, or a source. The 3
  fixes above are all small count or pointer corrections.
- No live source was unreachable and no rate limit hit this check.
  No item is UNVERIFIED.
- Open questions already carried in the draft limits, not new
  findings here: blocked versus completed stays open for the
  routify comment; distinct-writer status stays unproven from
  structure alone; the "fixed in eight days" detail for the CVE
  item stays unverified; two routify issue bodies stay
  unresolvable without full repo paths; linked reports behind all
  19 pointers stay unread; urlscan detail stays login-gated.
- One method note: the report and hits files were rewritten during
  this check. If the coordinator rewrites them again after this
  report lands, re-run checks 3 and 7 against the new hashes
  before ship. Checks 1, 2, 4, 5, and 6 do not depend on the
  rewrite, except for the already-fixed items noted above.

## Evidence paths

- Draft: `reports/agent-egress-deep-dive/REPORT.md`
- Hits: `reports/agent-egress-deep-dive/hits.json`
- Working notes: `reports/agent-egress-deep-dive/working/hn-comments.md`,
  `reports/agent-egress-deep-dive/working/hn-expanded-crawl.md`,
  `reports/agent-egress-deep-dive/working/follow-on-primaries.md`,
  `reports/agent-egress-deep-dive/working/cross-surface-pivots.md`,
  `reports/agent-egress-deep-dive/working/pivot-results.tsv`
- Raw lanes: `data/lanes/agent-egress-deep-dive/raw/hn-comments/`,
  `data/lanes/agent-egress-deep-dive/raw/hn-expanded-crawl/`,
  `data/lanes/agent-egress-deep-dive/raw/follow-on-primaries/`,
  `data/lanes/agent-egress-deep-dive/raw/cross-surface-pivots/`
- This report: `reports/agent-egress-deep-dive/verifier-report.md`
