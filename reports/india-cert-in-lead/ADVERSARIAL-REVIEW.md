# Adversarial review — india-cert-in dorks package

Date: 2026-10-23. Reviewer: adversarial lane. Operator: BigSexyWarlock69.
Scope: the Google-dorks battery (`google-dorks.txt`), the VULONE
URL-investigator memo (`data/lanes/india-cert-in/raw/google-dorks/vulone/INVESTIGATION.md`),
the three deliverable screenshots, and the claim wording in this package.

Terms used here:
- **UPSTREAM**: a claim from a report we read, not from our own checks.
- **OBSERVED**: a claim from bytes we fetched ourselves, with provenance.
- **INFERENCE**: our judgement from evidence.
- **Corroboration**: a second, independent source confirming a claim.
- **Hostile node**: a host we have evidence launched or staged attacks.

## R1. TLS fingerprint byte-match on 202.61.139.15 — DOWNGRADE

The memo grades .15 "CORROBORATED hostile C2/staging/exfil node". This grade
must fall. The hostile part is the problem.

What the byte-match proves: Shodan's scanner saw the same self-signed
certificate that VULONE's report describes (CN 202.61.139.15, validity
3–5 Oct 2026, matching SHA-256). This proves the report's infrastructure
description is accurate. It proves the reporter really saw the host, or at
least really saw Shodan's record of it.

What the byte-match does NOT prove: hostility. A self-signed certificate
with CN set to the IP address is trivial to mint. An open HTTP directory on
port 9000 is an open service, not an attack. Open services are not malice.

Circularity risk: if VULONE derived the fingerprint from Shodan's own
record (both print it verbatim), then Shodan "confirming" it is one source
wearing two hats. Two quotes of one source are one source. The memo does not
rule this out.

What would make "corroborated hostile C2" true: observed malicious traffic
from the host, or a second independent source confirming the attack role.
Neither exists on the record. The only traffic evidence is the operator's
own logs, quoted by VULONE.

Verdict: DOWNGRADE. Keep the infrastructure finding. Kill the hostile
grade. Exact replacement wording:

> 202.61.139.15: infrastructure description matches independent passive
> scans (ASN AS152194, org CTG Server Ltd, open SimpleHTTPServer directory
> on port 9000 until 15 Oct, self-signed cert matching the reported
> fingerprint). The attack role (C2/staging/exfil) is single-sourced to
> VULONE's account of the operator's own logs. No traffic was observed by
> us. Hostile role: UNVERIFIED.

## R2. "Still exposed" for 202.61.139.137 — DOWNGRADE

The memo grades .137 "CORROBORATED infrastructure, currently appears
exposed". The basis is one Shodan scan record timestamp (2026-10-23
03:45 UTC) listing port 9000 with SimpleHTTPServer and the open-dir tag.
No live fetch was made (the investigator left it out of scope).

Two problems:

1. Shodan records mix current and past services. A timestamp on the
   record is not proof the port answered at that time. Only a live fetch
   proves exposure now.
2. "Corroborated" is too strong. For .137 the only source is Shodan. The
   OTX pulse is a repost of the VULONE report, not fresh evidence (the memo
   admits this is a weak signal for .15; it is the same for .137). One
   source is not corroboration.

Verdict: DOWNGRADE. Exact replacement wording:

> 202.61.139.137: Shodan's latest passive scan (2026-10-23 03:45 UTC)
> still lists port 9000 with SimpleHTTPServer and the open-dir tag. No
> live fetch confirms this. Exposure now: UNCONFIRMED. Infrastructure
> identity (ASN/org) matches the report. Malicious role: UNVERIFIED.

## R3. Port 8888 on .137 — KILL pending citation

The memo's grade block says INFERENCE: still serving open directories on
ports 9000 and 8888. Port 8888 appears nowhere in the quoted VULONE IOC
list (ports 22, 443, 8000, 8443, 4443, 9000; exfil ports 8899, 8997,
9099, 9201, 9955). The memo cites no Shodan line for 8888 in the visible
record. An uncited port is a guess. Verdict: KILL this port from the
grade until a record cites it, or cite the Shodan line that shows it.

## R4. cdac.in / WSO2 admin/admin — DOWNGRADE, exact wording below

The memo grades the campaign-scale claims UNVERIFIED, which is correct.
But the phrase "Final project: cdac.in (C-DAC India), opened 14 Oct.
Access via default admin/admin on a WSO2 API Manager console" reads as a
confirmed compromise when stated flat. It is not confirmed. It is the
operator's own tally, quoted by one reporter. No named victim has
confirmed. Safeguard's own coverage of the same report says victim-side
verification is still pending and none of the named organisations had
publicly confirmed a compromise.

Any wording that presents the cdac.in access as fact overstates it. Exact
replacement wording (use verbatim):

> VULONE reports that the operator's own records list a final project
> against cdac.in (C-DAC, India), opened 14 Oct 2026, with claimed access
> through default admin/admin credentials on a WSO2 API Manager console.
> This is the reporter's account of the operator's own logs. No named
> victim has confirmed a compromise. Treat this as an unverified
> allegation, not a confirmed intrusion.

The India tie-in stands only as report content: the report names cdac.in.
That is a fact about the report, not a fact about C-DAC.

## R5. The two agent boards — KEEP as ecology-context, never as malice leads

- kyle-hatcher board (agent-message-board.kyle-hatcher.workers.dev):
  a zero-trust agent-messaging lab. Its own page says the board "takes
  no actions — it only stores and serves messages". Any agent can mint
  its own API key (observed on the rendered page). A low bar for agent
  participation is an observation, not malice.
- themostusefulsiteintheworld board: a public message board backed by
  public GitHub issue comments, with safety rules (treat posts as data,
  no keys, no impersonation). The first post is the site owner's own
  agent posting under the owner's account, and it says so.

Neither board shows malicious traffic. Neither is a launcher candidate.
Any writeup sentence that calls them "candidates for launching malicious
traffic" must be killed. Correct grade for both: ecology-context —
places where agents can talk, worth watching, not evidence of attack.

## R6. Screenshots — PASS, no replacement needed

All three deliverable captures were spot-checked by rendering:

1. kyle-hatcher-board-20261023T122923Z.png — renders the real "Agent
   Message Board" dashboard (4 records, 3 messages, 73 access events,
   chain OK, uptime 10d 13h). Matches provenance. PASS.
2. tmu-ai-board-20261023T123045Z.png — renders the real "AI Message
   Board" page (GitHub Issue #195, 1 post, 1 agent, safety rules).
   Matches provenance. PASS.
3. safeguard-blog-20261023T122646Z.png — renders the real Safeguard
   article ("AI Agent Intrusion Campaign in Asia: 48 Targets, IOCs and
   Defence", dated October 22, 2026). Notably, the article itself
   carries the honest caveat: the 48 is the operator's own tally and
   victim-side verification is pending. Matches provenance. PASS.

All six sha256 sidecars verified byte-for-byte against the PNGs on disk.
The two ERRORPAGE-proxyfail captures and the NARROW-superseded capture
are correctly labelled auxiliary in AUXILIARY-ARTIFACTS.txt and kept per
the never-delete-evidence rule. No capture needs replacement.

## R7. Human/operator identity check — PASS, one boundary note

- INVESTIGATION.md repeats VULONE's upstream attribution ("China-linked,
  Chinese-speaking operator"). This is the reporter's claim, quoted as
  UPSTREAM. It is not our pursuit. It must stay quoted as upstream and
  never harden into our finding.
- No names, registrant details, emails, or social profiles were pursued.
  The published SSH key is an IOC from the report, not an identity.
- The tmu provenance notes the public GitHub handle of the site owner
  (mrpr0phecy), which is displayed on the page itself. Recording what
  the page shows is within the letter of the rule. Do not expand it:
  no profile lookups, no identity research. The boundary stops at the
  rendered page.

## R8. Dork-battery internal consistency — PASS

22 dorks listed, 22 dork files on disk. 6 surfaced in-scope material
(D1, D3, D9, D13, D17, D22), 16 nulls. The count matches. The nulls are
honest (name collisions and doc pages recorded, not hidden). The
snbdhost "27 firms, 600K cards" item is correctly flagged "unverified,
treat as claim-only". D22 correctly presents the VULONE items as report
content, not as our findings.

## Summary of kills and downgrades

- KILLED: "CORROBORATED hostile C2/staging/exfil node" (.15). Hostile
  role needs observed traffic or a second source. Has neither.
- KILLED: "CORROBORATED infrastructure" (.137). One source (Shodan),
  not corroboration.
- KILLED: port 8888 on .137, pending a cited source.
- DOWNGRADED: .15 → infrastructure description matches passive scans;
  attack role single-sourced, unverified.
- DOWNGRADED: .137 → Shodan reports exposure as of 2026-10-23 03:45 UTC;
  unconfirmed by live fetch; malicious role unverified.
- DOWNGRADED: cdac.in/WSO2 → unverified allegation wording (exact text
  in R4).
- KEPT: both agent boards as ecology-context; all three screenshots;
  dork-battery nulls; identity-boundary posture.
