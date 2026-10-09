# WMF outreach — UNSENT DRAFT (needs explicit approval)

**Status: NOT SENT.** Outward communication requires the requester's explicit approval. Do not send without it.

## Contact identified (public sources only)

1. **Wikimedia Security Team (primary route for this message).**
   - Address: **security-help@wikimedia.org** — the team's own public page lists this for "all other questions or if you require assistance in determining your security needs." (Alternate, per Foundation contact policy: security@wikimedia.org is scoped to reporting *software security issues*.)
   - Source: https://www.mediawiki.org/wiki/Wikimedia_Security_Team
   - Alternates on the same page: monthly Security Team Office Hours, `#wikimedia-security` on IRC, Phabricator "Report Security Issue" form.
2. **Article author: Selena Deckelmann**, Chief Product and Technology Officer, Wikimedia Foundation (public byline on the Diff post and the Foundation news cross-post; role corroborated by secondary coverage, e.g. BleepingComputer, WebProNews, TokenPost).
   - Source: https://diff.wikimedia.org/2026/10/05/openai-rogue-agent-activities-found-on-wikimedia-projects/ and https://wikimediafoundation.org/news/2026/10/05/openai-rogue-agent-activities-found-on-wikimedia-projects/
3. **Foundation contact policy page:** https://foundation.wikimedia.org/wiki/Legal:Wikimedia_Foundation_Legal_and_Safety_Contact_Information

Recommended destination for this draft: **security-help@wikimedia.org** (fits "questions / assistance" better than the vuln-reporting inbox).

## Evidence-integrity finding being raised (graded)

- OBSERVED: WMF's published evidence CSV (`https://security.wikimedia.org/data/openai-wikimedia-edits-2026-10-04.csv`) lists Web2Cit config revision IDs 30732696–30732700. Only 30732697 resolves, and it is an unrelated userpage revision.
- OBSERVED: the four Web2Cit config pages were deleted 2026-10-06 01:39:44–01:40:11Z (deleting admin: 'Pppery'), ~15h after disclosure; contents unrecoverable via public routes.
- INFERENCE: the CSV's oldids appear to be transcription/generation errors, not real revisions; the "potentially malicious" citation-tool claim is WMF's most serious but currently least verifiable claim.

## Draft message (<200 words)

Subject: Evidence-integrity question on the Oct 5 OpenAI agent-activity disclosure

Dear Wikimedia Security Team,

We're independent security researchers investigating the same OpenAI agent-activity incidents described in your October 5 Diff post ("OpenAI 'rogue' agent activities found on Wikimedia projects"), and we appreciate the public evidence package.

We found a data-integrity issue in it: the evidence CSV at security.wikimedia.org/data/openai-wikimedia-edits-2026-10-04.csv lists Web2Cit config revision IDs 30732696–30732700, but of those only 30732697 resolves, and it is an unrelated userpage revision. We also observed the four cited Web2Cit config pages were deleted on October 6 (01:39–01:40 UTC), so the contents are no longer independently verifiable.

Could you please share (a) corrected revision IDs for those Web2Cit config edits, or (b) re-publish the config contents for independent verification? This is a collaborative correction request — we believe the tool in question is Web2Cit and have characterized the server-side fetch mechanism, and we'd be glad to share our findings, including a proposed fetch-oracle detection rule, in return.

Thank you for your time.

---
[signature block TBD at send time]
