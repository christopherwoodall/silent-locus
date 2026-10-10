# Checkpoint — lane (d) wmf-outreach (2026-10-06)

## Done
- Read HUNT-SUMMARY.md and methodology.md.
- Found public contacts via passive OSINT (no personal-email digging, no non-public sources):
  - WMF Security Team: security-help@wikimedia.org (recommended route) — https://www.mediawiki.org/wiki/Wikimedia_Security_Team ; vuln-reporting inbox security@wikimedia.org — https://foundation.wikimedia.org/wiki/Legal:Wikimedia_Foundation_Legal_and_Safety_Contact_Information
  - Article author: Selena Deckelmann, WMF Chief Product and Technology Officer — byline corroborated by the Diff post, Foundation news cross-post, and secondary coverage (BleepingComputer, WebProNews, TokenPost).
  - Draft message written (182 words, factual, non-accusatory, collaborative-correction framing): raises the CSV oldids 30732696–30732700 nonexistent-revision finding + the Oct 6 config deletions; asks for (a) corrected revision IDs or re-shared evidence, (b) re-publication of config contents; offers our Web2Cit mechanism characterization and fetch-oracle detection rule.
- Files saved:
  - `followups/wmf-outreach/DRAFT.md` (contact + sources + the UNSENT draft + graded evidence summary)
  - `followups/wmf-outreach/CHECKPOINT.md` (this file)
- **NOTHING SENT.** Draft is UNSENT and requires the requester's explicit approval before any outward communication.
- Committed `followups/wmf-outreach/` on branch `wikimedia-rogue-agents-followups-2026-10-06` (pre-existing modified files in `data/2026-09-28-chinese-amap-fleet/` left untouched, per task).

## What's next
- Requester's call: approve send (to security-help@wikimedia.org, signature block still TBD), revise the draft, or hold.
- Claim grades in DRAFT.md: oldids nonexistent = OBSERVED; deletion timestamps = OBSERVED; transcription-error reading = INFERENCE; Deckelmann's role = UPSTREAM (secondary corroboration, not a Foundation page fetch).
- Open question: whether security-help@ or the Phabricator "Report Security Issue" form is the best intake for a non-vuln evidence-correction request — flag to requester if approving.
