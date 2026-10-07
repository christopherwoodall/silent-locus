# REVIEWER-A adjudication — Wikipedia lane claims (round 2: H1/M1)

**Role:** forensic skeptic · **Date:** 2026-10-07 · **Branch:** `wikipedia-edit-hunt-2026-10-06`
**Method:** Read LIFEVAL-WRITEUP.md, pattern-hunter FINDINGS.md (M1–M11), burst-analysis FINDINGS.md, REVIEWER-1.md, REVIEWER-2.md. Spot-checked raw cache: `uids-mediawikiwiki_2026-05-21_1h.json`, `uids-testwiki_2026-05-10.json`, both interloper logevents files, `rev-8383593-mediawiki.json`, contribs + crosswiki-contribs files, PROVENANCE.txt. A–D adjudicated against prior reviewers' documented re-verification (revisions.tsv + live API); H1/M1 against bytes checked directly.

## A. Lifeval coordination reading — **CONFIRM**
OBSERVED (marker bytes) / INFERENCE (fleet-evaluation attribution). REVIEWER-1's re-verification stands: 10 distinct `~2026-*` accounts across incubator/Commons/Meta stamping the same distinctive string family within ~30 min on 2026-06-25, every one born with the marker edit. Eight strangers do not independently produce a 55-character codename comment. The "fleet evaluation run" gloss remains INFERENCE — REVIEWER-2's classroom/eval-workshop null (shared instructions, copy-pasted string, autocreated temp accounts) is untested, not ruled out. **Weakest link:** the classroom null produces identical marker bytes; only the cross-wiki variants + M3/M8 context keep the agent reading alive. Claim survives with that scoping already in place.

## B. M3 same-second volleys — **CONFIRM**
OBSERVED. The anchor is the same-second same-page double-save (mediawiki.org 8370994/8370995, both 2026-05-10T17:12:18Z) — not achievable through the web UI (save→round-trip→reload→re-save within one second); the second appends `[[User:Example/sandbox]]` to the first payload, consistent with scripted API requests. Machine-generated test2 payloads and M7's byte-identical cross-wiki sha1 corroborate. **Weakest link:** the ~1s cross-wiki stagger *alone* would be weak (fast human with pre-loaded tabs); the finding's weight rests entirely on the same-second same-page pair. As worded ("one operator driving N wikis in parallel"), it holds.

## C. M6 corrected geometry — **CONFIRM (as observation; standing non-diagnostic caveat)**
OBSERVED and factually correct: 8 temp accounts in uids 2690515–2690523 with named-human interloper Dayerhonda at uid 2690519 (registered 2026-06-25T20:19:29Z mid-burst), verified live by REVIEWER-2. The original "consecutive" wording stays dead. **Weakest link:** per REVIEWER-2, the geometry *alone* is non-diagnostic — a classroom told to edit the sandbox without logging in produces exactly this shape. The finding's diagnostic weight comes from the shared distinctive marker (claim A), not the uid run. No change needed beyond keeping REVIEWER-2's restatement.

## D. M8 sandbox→live chain — **CONFIRM**
OBSERVED (same-account linkage) / INFERENCE (workflow intent) / UPSTREAM (WMF CSV attribution). The linkage is the **identical account name** `~2026-36867-71` (uid 2690523, incubator sandbox edit 7226111) appearing in the WMF CSV's userspace Web2Cit template page title. **Weakest link:** the page is `templates-temp-5123` — a template *sandbox*, not live config — and its content is unrecoverable (deleted 2026-10-06, deletion log verified by REVIEWER-2), so the "sandbox→live workflow mirrored" reading is inference on an upstream attribution, not a verified page transition.

## E. H1 "same campaign family as Lifeval" — **DOWNGRADE**
The observation is real and verified in bytes: the sandbox edit (rev 8383593, `~2026-30432-02`, 2026-05-21T00:40:39Z, comment "sandbox test", text "Temporary sandbox test.", mw-reverted); the 01:13:18–01:13:56Z run (uids 18396941–18396954 with Wildwind75 at 01:13:49Z filling uid 18396951 — verified in the newusers log); the 01:38:15–01:39:45Z run (uids 18396979–18396997 with Jheanovivia at 01:39:29Z filling uid 18396990); zero edits by the remaining accounts. But the "fleet evaluation harness signature" / "same campaign family" / "same operator" claims collapse on three attacks:

(i) **The sandbox edit is not incident-shaped in any distinctive sense.** "Temporary sandbox test." / comment "sandbox test" is the single most generic sandbox text in existence — a human tester writes exactly this. The M2-vocab match is a match to generic vocabulary, not to a marker.

(ii) **The uid-run "match" to corrected M6 is creation-order only, behaviorally hollow.** Lifeval's diagnostic power came from 8 accounts *editing* with a shared distinctive marker; in H1, 32 of 33 burst accounts made zero edits on all 9 wikis. The runs are a derived property of burst tightness + background registration rate — on mediawiki.org at 01:13Z the log shows near-zero organic registrations, so *any* burst of logged-out first-edits yields near-consecutive uids. Worse, this stacks inference on REVIEWER-2's already-downgraded M6 geometry (non-diagnostic standalone). Also a count slip: the window holds 14 accounts (13 temps + 1 interloper = **13-of-14** consecutive), not "13 accounts / 12-of-13."

(iii) **"Same operator" is unwarranted.** No shared distinctive string, no cross-wiki volley geometry, no Web2Cit. "Matches 4 of 5 incident criteria" is grade inflation — criterion 2 is carried by *one* generic edit while 32 accounts are silent.

**Restate as:** *"Anomalous temp-account burst, mediawiki.org 2026-05-21, with two interloper-bracketed near-consecutive uid runs and one generic one-shot sandbox edit; creation-order geometry resembles Lifeval M6 but without any shared distinctive marker or editing behavior; operator linkage to Lifeval is unproven INFERENCE. Retain as a lead (MEDIUM at best, not HIGH), not a campaign attribution."*

## F. M1 "fleet-creation geometry" — **DOWNGRADE**
OBSERVED and verified: uids 73872–73884, 13-of-13 consecutive, 2026-05-10 17:47:30–18:41:00Z, zero edits by all 13 on all 9 wikis. But the "fleet-creation" / "plausibly the same operator's provisioning run" reading has no behavioral content — numerology on account-creation order with an untested null. **Yes, 13 consecutive uids happen organically:** on a near-dead wiki like testwiki, any source of 13 logged-out first-edits in an hour with no interleaving registrations (QA tester, workshop, class, script — agent or human) produces exactly this. The "temporally pool-adjacent to M3" link is near-tautological: pools are time-bucketed, so same-afternoon activity is same-pool-family by construction. **Restate as:** *"Creation-only burst of unknown provenance, testwiki 2026-05-10; geometry alone is non-diagnostic; same-operator linkage to M3 is speculation. LOW lead / watchlist, not MEDIUM."*

## Kill list (for DONE.md)
No new outright kills — the H1/M1 observations are genuine anomalies worth retaining. But **strip the attribution language**: "same campaign family as Lifeval," "fleet evaluation harness signature," "same operator (INFERENCE)" in H1; "fleet-creation geometry," "plausibly the same operator's provisioning run" in M1. These phrases must not survive in lane findings. (All prior kills — M5 fetch-oracle gloss, "contradicts WMF" wording, dse lead, original M6 "consecutive" claim — stay dead.)

## Survives list
- A. Lifeval coordination reading — CONFIRM (INFERENCE scoping intact)
- B. M3 same-second volleys — CONFIRM
- C. M6 corrected 8-of-9 geometry — CONFIRM as observation (non-diagnostic-alone caveat stands)
- D. M8 identical-account chain — CONFIRM (workflow intent stays INFERENCE/UPSTREAM)
- H1 — DOWNGRADED to scoped lead: anomalous burst, operator linkage unproven
- M1 — DOWNGRADED to LOW: creation-only burst, zero behavioral evidence
