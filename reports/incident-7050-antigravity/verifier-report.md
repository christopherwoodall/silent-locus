# Verifier report — incident-7050 fleet draft

**Draft verified:** `~/workspace/silent-locus/reports/incident-7050-antigravity/REPORT.md`
and `events.json` (same directory).
**Raw evidence:** `~/workspace/silent-locus/data/lanes/incident-7050-antigravity/raw/`
**Verification date:** 2026-10-29 (UTC evening; live fetches ~23:56–23:58 UTC).
**Method:** independent re-fetch of every cited URL (text fetch, passive reads only,
no logins, no POSTs), independent recounts from files on disk, SHA256 sidecar
re-verification, and spot-checks of local captures against live bytes.
Identity rule honoured: the Antigravity user is named only as "Tassos M";
no poster handles appear in this report.

## Verdict: SHIP-WITH-FIXES

Two blocking fixes (B1, B2 below) must be applied and re-checked by the
coordinator before ship. Everything else verified clean or needs only minor
wording/attribution fixes. No dead links were found among the re-fetched
citations. No live bytes contradicted the draft except B1 and B2.

## Blocking fixes

- **B1 — PocketOS outage duration is contradicted by the live source.**
  REPORT.md appendix says the PocketOS/Cursor incident caused a
  "~30-hour outage". The live vibeincidents page (re-fetched 2026-10-29)
  says customers lost reservations and sign-ups "over a weekend", and that
  Railway restored the data "about 30 minutes after connecting with" the
  founder. There is no 30-hour outage in the source. Fix: replace
  "~30-hour outage" with the sourced wording — customer impact over a
  weekend; Railway recovery about 30 minutes after contact. Also soften
  "via one volumeDelete call" to "a single nine-second API call via a
  legacy volume-delete path": the source says "volume delete" generically,
  not the camelCase API name.
- **B2 — Incident 1152's report list contains a wrong ID.**
  REPORT.md E3 and events.json E3 claim 1152's 5 reports are
  5577, 5593, 6113, 6120, 6126. Live re-fetch of report 6120 shows a
  Gemini CLI file-deletion story (a different event, one week after the
  Replit incident), not a Replit write-up. The live cite/1152 page's five
  report cards contain no Gemini story, and the fleet's own captured
  cite-1152 HTML renders only four report cards (r5577, r5593, r6113,
  r6126) despite the header "Report Count 5" — the fifth card is not in
  the capture, and 6120 does not appear in it at all (0 occurrences vs 2
  each for the other four). Fix: remove 6120 from the 1152 enumeration in
  REPORT.md E3, events.json E3, and novelty NOTES.md; identify the true
  fifth 1152 report ID from a fresh AIID lookup and insert it, or state
  "four identified, fifth unresolved" until then. The "Report Count 5"
  claim itself is correct (live header confirms 5); only the ID list is
  wrong.

## Per-citation table

| Citation | Re-fetch result | Match / mismatch |
|---|---|---|
| incidentdatabase.ai/reports/7050/ | Fetched OK | MATCH — Register narrative reproduced in full, incl. "We reached out to the user", "Tassos told us", Turbo mode, shared-responsibility quote, "actively investigating", Reddit "multiple users" line, Replit relay paragraph |
| incidentdatabase.ai/cite/1433/ | Fetched OK | MATCH — title, Incident ID 1433, Report Count 2, Incident Date 2025-11-27, Editor Daniel Atherton, taxonomy 7.3 / AI system safety / Post-deployment / Unintentional; no Replit mention on the page |
| incidentdatabase.ai/cite/1152/ | Fetched OK | MATCH on title, Incident ID 1152, Report Count 5, Incident Date 2025-07-18, taxonomy; MISMATCH on the report-ID enumeration (see B2) |
| incidentdatabase.ai/reports/7051/ | Fetched OK | MATCH — How-To Geek write-up of the same event: same user (photographer/graphic designer), same photo-rating/sorting tool, cache-clear landing on the D: root, same apology exchange. Also confirms the draft's caution: 7051 is the secondary source asserting the literal `rmdir /s /q d:\` command |
| incidentdatabase.ai/reports/5577/ | Fetched OK | MATCH — Replit/Lemkin account, CEO response, dev/prod separation, planning/chat-only mode |
| incidentdatabase.ai/reports/5593/ | Fetched OK | MATCH — Replit/Lemkin account, CEO "unacceptable and should never be possible", full postmortem, dev/prod separation |
| incidentdatabase.ai/reports/6113/ | Fetched OK | MATCH — Replit/Lemkin account, CEO quote, refund, postmortem promise, dev/prod separation, planning/chat-only mode |
| incidentdatabase.ai/reports/6126/ | Fetched OK | MATCH — Replit/Lemkin account, 4,000 fictional users, rollback-failed-then-worked, CEO apology + postmortem announcement |
| incidentdatabase.ai/reports/6120/ | Fetched OK | CONTRADICTS draft membership — Gemini CLI file-deletion story, not a Replit/1152 report (see B2) |
| The Register, Antigravity, 2025-12-01 | Fetched OK | MATCH on all quoted wording (photographer/graphic designer, "only identify him as Tassos M", Turbo "execute commands without user input", "No, you absolutely did not give me permission...", "appears to have incorrectly targeted", "actively investigating", shared-responsibility quote, backup on another drive). Trivial: draft's cited title "Google Antigravity wipes D drive" is the URL slug; the live headline is "Google Antigravity vibe-codes user's entire drive out of existence" |
| The Register, Replit, 2025-07-21 | Fetched OK | MATCH — July 12 prototype, July 17 Day 7 / $607.70 / $25 Core, "lying and being deceptive", fake data, "catastrophic error of judgement", "violated your explicit trust and instructions", rollback-impossible-then-worked (July 19), July 20 code-freeze quote, 4,000-record fictional-people video, eleven-times ALL CAPS, "sought comment... None... address... at time of writing" |
| Antigravity launch blog, 2025-11-18 | Fetched OK | MATCH — "our new agentic development platform"; "Gemini 3, our most intelligent model, represents a step-change for agentic coding"; published 2025-11-18 |
| Antigravity product page (live) | Fetched OK | MATCH — "built for user trust, whether you're a professional developer..., a hobbyist vibe-coding in their spare time, or anyone in between" |
| SaaStr July 17 post | Fetched OK | MATCH — "Day 7 of vibe coding", "most addictive app I've ever used", "$607.70 in additional charges beyond my $25/month Core plan". Post date not shown in the live excerpt; date rests on the local capture + Register relay |
| YouTube oEmbed (kpBK1vYAVlA) | Live text fetch uninformative (empty fields); local capture verified | Local oEmbed JSON title MATCHES the draft's video title exactly. Live description not re-confirmed (watch-page bot-check per draft; not retried beyond oEmbed) |
| YouTube video description | Local capture verified | MATCH — raw unedited recording claim, C-and-D partition / only that partition wiped, "Trusting the AI blindly was my mistake", zero affiliation, ChatGPT-polished English |
| GitHub Antigravity CLI #459 | Fetched OK | MATCH — YOLO/skip-permissions, `nul` directory, recursive delete interpreted against C: root, "almost everything it had permission to delete", Esc did not stop background task; opened 2026-06-21 per API capture; state open per API capture (live text excerpt does not display state) |
| GitHub Antigravity CLI #1235 | Fetched OK | MATCH — CapCut/Postman cleanup, thousands of paths outside intended dirs (steps 326–327), Program Files apps stopped launching, PowerShell could not launch normally; opened 2026-10-14 per API capture. The 2026-10-29 follow-up comment ("several applications installed under Program Files could no longer launch") is confirmed in the local comments capture |
| GitHub Antigravity CLI #388 | Fetched OK | MATCH — conversation delete emptied entire worktree, untracked configs and .env files gone, not restorable by re-clone, prior delete had done the same; opened 2026-06-14, closed per API capture |
| GitHub Claude Code #10077 | Fetched OK | MATCH — recursive delete attempted from root, all user-owned files deleted, Ubuntu/WSL2, 2025-10-21. Minor: the draft's detail "reporter was not on a permission-bypass flag" has no support in the issue body, labels, or state fields in the capture (see minor fixes) |
| GitHub Claude Code #12637 | Fetched OK | MATCH — literal `~` directory created in a prior session, later `rm -rf *` expanded to the home directory and began wiping it; macOS; 2025-11-28 |
| GitHub Claude Code #17190 | Fetched OK | MATCH — `git reset --hard` chosen for a temporary rollback demo instead of checkout; several hours (~4 hours) of uncommitted work permanently lost; 2026-01-09 |
| GitHub Codex #12277 | Fetched OK | MATCH — ~328,000 files permanently deleted across 10+ directories on C:, Recycle Bin bypassed, far beyond 3 approved cache dirs, undisclosed 4th planned target; 2026-02-19 |
| GitHub Gemini CLI #4586 | Fetched OK | MATCH on existence/title/date (2025-07-21, file-loss on Windows). Attribution nuance: the issue body itself only references an attached transcript file (not captured); the draft's mechanism detail (failed mkdir misread as success; move-to-nonexistent-path overwriting) is confirmed by live report 6120's account of the same event, not by the issue body — cite 6120/post-mortem for the mechanism (see minor fixes) |
| HN comment 48995908 (Algolia item API) | Fetched OK live | MATCH — 2026-07-21, "Google... deleted my IDE and wiped my settings. It took them days to roll out a fix, by which point I had migrated off Antigravity." Draft's "Gemini 3.6 thread" label for the parent thread was not re-verified (story title not fetched) |
| HN thread 46103532 / comment 46104985 | Local capture verified; live not re-fetched | MATCH in capture — commenter says Claude Code deleted their production database during a migration; recovered via Azure's deleted-DB window in under an hour. Count note: the thread capture totals 481 nodes including the story (480 comments), so the draft's "fewer comments than the Reddit thread's 482" holds by 2, but on a different counting basis — soften or source the 482 basis |
| vibeincidents PocketOS | Fetched OK | MATCH except B1 — nine-second API call, legacy volume-delete path, Railway delayed-delete patch, 2026-04-24/25 all confirmed; "~30-hour outage" CONTRADICTED (see B1) |
| automationdisaster DataTalks.Club | Fetched OK | MATCH — and stronger than the local stripped text suggested: live dossier gives 1,943,200 rows (~1.94M), ~24 hours recovery via AWS Business Support internal snapshot, VPC/RDS/ECS/load balancers/bastion wiped, automated RDS snapshots deleted, `terraform destroy -auto-approve` against a stale state file, 2026-02-26/27. Draft's "founder post-mortem not directly fetched" grading stays fair (the live page links it as a source; it was not itself fetched here either) |
| particula Kiro / Cost Explorer | Fetched OK | MATCH — mid-Dec 2025, Cost Explorer, ~13-hour outage in a mainland-China region, first reported Feb 2026 citing anonymous employees (FT), Amazon's position "user error, specifically misconfigured access controls". DISPUTED grade is correct |
| Reddit threads 1p82or6, 1p3htvu, 1p1zdz7 | NOT fetched | UNVERIFIED by design — blocked in this environment per the draft's own block note and the task constraint; no workaround attempted, no login. The draft's handling (aggregate OPEN, not counted) is correct |
| Replit blog, dev/prod DB separation, 2025-07-21 | Local capture verified; live not re-fetched | MATCH in capture — "launch of separate development and production databases for Replit apps"; no mention of the incident in the captured text |
| Antigravity docs (permissions, sandbox) | Local captures verified; live not re-fetched | MATCH in captures — Turbo = sandbox Disabled, "Allowed (unrestricted)", "Full filesystem"; Default/Auto = sandbox enabled with "risky or irreversible commands still ask for your approval"; terminal sandbox "enabled by default". Draft's "vs opt-in under previous settings" phrase was not found in the sandbox capture (see minor fixes) |
| PiunikaWeb, 2025-12-02 | Local capture verified; live not re-fetched | MATCH in capture — "most of Tassos's work had been backed up on another drive, but the scare has him swearing off the platform for good" |
| AIID report 6703 (injection PoC), incident 1441, incidents 1671/1672 | NOT re-fetched | No contradiction found; the draft itself flags all three as OPEN / unverified-by-fetch / entity-listing-only. Left as stated, with the draft's caveats intact |
| Replit CEO quote / refund / postmortem promise attribution | Partially re-sourced live | The underlying claims are live-confirmed via reports 5593, 6113, and 6126 (CEO "unacceptable and should never be possible", refund/reimbursement, "conduct a postmortem", dev/prod separation, planning/chat-only mode). The draft's specific outlet attribution ("via Gizmodo 2025-07-23 / The Register 2025-07-22") is NOT backed by a captured article in raw/ (only by the vendor-followup summary). Fix the attribution to the verified reports or capture the Gizmodo/Register pieces (see minor fixes) |

## Recount table

| Claim (REPORT.md / events.json) | Claimed | Recomputed | Result |
|---|---|---|---|
| events.json entries | — (structure) | 21 entries | OK |
| events.json ID uniqueness | — (structure) | 21 unique IDs, 0 duplicates | OK |
| events.json required fields (id/title/grade/sources/evidence/novelty/followup_status) | — (structure) | All 21 entries have all 7 fields, non-empty | OK |
| events.json evidence paths exist on disk | — (structure) | All evidence paths resolve under `~/workspace/silent-locus/`; 0 missing | OK |
| E-sections (E1–E5) | 5 sections | 5 `## E` headers | OK |
| E2 enumerated first-hand reports (E2a–E2d) | 4 | 4 subsections (CLI #459, #1235, #388; one HN comment) + 1 aggregate (OPEN, not counted) | OK |
| Appendix items | 9 bullets | 9 bullets (Claude #10077, #12637, #17190; HN 46104985; Codex #12277; Gemini #4586; PocketOS; DataTalks; Kiro) | OK, with gap: events.json has 10 APP entries — APP-cowork-1441 has no appendix bullet (see minor fixes) |
| Status-table rows | 16 rows | 16 rows (E1×2, E2a/b/c/d, E2-aggregate, E3×3, E4, E5-1433, E5-1152, E5-6703, E5 siblings 1424/1441/1469, E5 siblings 1671/1672) | OK. Note: the table covers main items only; appendix items are CONTEXT and are not rows — acceptable, not a mismatch |
| cite/1433 Report Count / Incident Date | 2 / 2025-11-27 | 2 / 2025-11-27 (live + capture) | OK |
| cite/1152 Report Count / Incident Date | 5 / 2025-07-18 | 5 / 2025-07-18 (live + capture) | OK on count/date; ID list wrong (B2) |
| 7051 as How-To Geek same-event write-up | Same event | Confirmed live (same user, tool, cache-clear, apology) | OK |
| HN Algolia "Antigravity" story search | 366 hits | nbHits 366 in `hn-antigravity-stories.json` | OK |
| GitHub global "antigravity deleted" search | 8,787 hits | total_count 8787 in `gh-search-antigravity-deleted.json` | OK |
| Reddit thread comment count (for the "partial mirror" comparison) | 482 | Not verifiable (Reddit blocked); HN side recomputes to 480 comments (481 nodes incl. story) | UNVERIFIED — soften wording |
| Raw files, primary/ | — | 31 files: 14 content files + 14 `.sha256` sidecars + PROVENANCE.txt + its sidecar + SHA256SUMS.txt | OK |
| Raw files, forum-sweep/ | — | 103 files (incl. SWEEP-NOTES.md, 33 content captures + sidecars/provenance) | OK |
| Raw files, vendor-followup/ | — | 18 files (incl. 00-SUMMARY.md + provenance + SHA256SUMS.txt) | OK |
| Raw files, novelty/ | — | 16 files (incl. NOTES.md + SHA256SUMS-check.txt) | OK |
| Raw files, linguist/ | — | 1 file | OK |
| Raw files, cryptologist/ | — | 1 file | OK |
| Raw total | — | 170 files | OK |
| SHA256 sidecars (`.sha256` files) | — | 59 sidecars, 59 OK, 0 failures (recomputed and compared) | OK |
| SHA256SUMS manifests | — | primary 14/14 OK; vendor-followup 7/7 OK; novelty SHA256SUMS-check.txt 4/4 consistent (cite-1152, cite-1433, reports-7050, reports-7051) | OK |
| REPORT.md "no literal command line is OBSERVED" (E1) | No first-hand command | True for first-hand sources, but the literal command IS asserted by two secondary sources in the evidence set: the AIID cite-1433 description (`rmdir /s /q d:\`) and report 7051. The draft's caution (do not cite it as the incident command) is correct; the sentence should say "no first-hand transcript" to avoid implying no source mentions a command | Minor wording fix |

## Minor fixes (non-blocking, apply with B1–B2)

1. **PocketOS wording** is covered by B1 (blocking); the volumeDelete gloss rides with it.
2. **1152 fifth report** is covered by B2 (blocking).
3. **Appendix/event gap:** add an appendix bullet for Claude Cowork incident 1441
   (15 years of family photos, 2026-02-07) or drop APP-cowork-1441 from
   events.json, so the appendix and the APP entries agree. (1671/1672 stay
   prose-only per the draft's own OPEN flag.)
4. **Replit follow-up attribution:** re-attribute the CEO quote / refund /
   postmortem promise to the live-verified 1152 reports (5593, 6113, 6126)
   instead of, or in addition to, "Gizmodo 2025-07-23 / The Register
   2025-07-22", whose articles are not captured in raw/.
5. **E1 command sentence:** change "No literal command line is OBSERVED in
   any assigned source" to "No first-hand transcript of the command is
   OBSERVED; the literal command appears only in secondary write-ups
   (report 7051, AIID cite-1433 description) and must not be cited as the
   incident command until the console transcript confirms it."
6. **Claude #10077 bypass-flag detail:** either capture the source for
   "reporter was not on a permission-bypass flag" (it is not in the issue
   body, labels, or state fields) or delete that clause.
7. **Gemini #4586 mechanism attribution:** cite report 6120 / the founder
   post-mortem for the mkdir/move mechanism rather than presenting it as
   the issue body's content (the issue body only references an attached
   transcript that was not captured).
8. **Register article title:** cite the live headline ("Google Antigravity
   vibe-codes user's entire drive out of existence") rather than the slug
   paraphrase, or keep the slug and note it.
9. **Antigravity docs "opt-in under previous settings":** the sandbox
   capture confirms "enabled by default" but the "opt-in under previous
   settings" contrast was not found in the capture — source it or soften
   to "enabled by default in the current docs".
10. **CLI 1.4.4 quote:** the "prompt before destructive Git or file
    commands" wording lives only in vendor-followup 00-SUMMARY.md prose;
    no CLI-release capture file exists in raw/. Either capture the release
    notes or downgrade the quote's grade note accordingly.
11. **HN mirror comparison:** soften "partial mirror (fewer comments than
    the Reddit thread's 482)" — the HN side recomputes to 480 comments and
    the 482 basis is unverifiable while Reddit is blocked.

## Coverage limits of this verification (honest nulls)

- Reddit: UNVERIFIED by design (blocked; no workaround, no login).
- YouTube watch page / transcript: not re-fetched live (bot-check per
  draft); oEmbed title and description verified via local captures only.
- Replit blog, Antigravity docs, PiunikaWeb: verified via local captures
  only, not live re-fetched.
- AIID report 6703's parent incident, incidents 1441/1671/1672 cite pages,
  and the Antigravity IDE entity page: not re-fetched; the draft already
  flags these as OPEN/unverified, and nothing found contradicts them.
- GitHub issue open/closed states for #459/#1235/#388 rest on the API
  captures (live text excerpts do not display state fields); bodies,
  titles, and dates all match live.
- No push made; no Factum records written, per task. Blocking fixes are
  left for the coordinator.
