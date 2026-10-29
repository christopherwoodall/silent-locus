# Short addendum — what the Google dorks found that Shodan did not

Date: 2026-10-23. Battery: 22 Google dorks, 6 surfaced in-scope material,
16 honest nulls. Full detail: `google-dorks.txt` in this directory.

## Headline

The Google battery found no new exposed agent-harness panels. The panel
population is already well surveyed (see the Shodan count-side finding in
`shodan-dorks.txt`). Google's value this run was news context and agent
ecology, not new exposed assets.

## What Google found that Shodan did not

1. The VULONE Asia campaign report (D22). Shodan is a scan index; it
   cannot surface a campaign report. This is the one genuine new lead of
   the battery: the Safeguard blog summary of VULONE's 2026-10-18 report,
   the vulone.com primary report, and securityonline.info secondary
   coverage. All three were fetched with sha256 provenance (see
   `data/lanes/india-cert-in/raw/google-dorks/vulone/PROVENANCE.md`).
   Adversarial grade: the campaign claims (66 projects, 48 accesses,
   named victims including cdac.in) stay single-sourced and UNVERIFIED.
   The infrastructure markers (ASN/org, open-dir, cert fingerprint) match
   passive scans. Grade: ecology-context (campaign-report context), NOT
   a launcher lead. We observed no traffic from these hosts.

2. Two live agent message boards (D13). Shodan does not index these.
   - https://agent-message-board.kyle-hatcher.workers.dev — zero-trust
     agent-messaging lab. Grade: ecology-context.
   - https://www.themostusefulsiteintheworld.com/tool/ai-message-board.html
     — public board backed by GitHub issue comments, with safety rules.
     Grade: ecology-context.
   Neither shows malicious traffic. Neither is a launcher candidate.

3. CERT-In advisory coverage URLs (D17). Context only; already covered
   by the corpus lane (`data/lanes/india-cert-in/raw/corpus/`). Nothing
   new. No IOCs anywhere in the coverage, matching the corpus finding.

4. NorForge/Reuters Cairn-campaign coverage (D1, D3) and iLands agent
   diaries (D9). Context and Tier-1-adjacent ecology. Already known
   surfaces; nothing new.

## What Google did not find (honest nulls)

- No live exposed Cairn/Strix/Hermes panel via the public index (D2,
  D4–D7, D18, D20, D21).
- No exposed agent chat logs, transcripts, or run exports (D8, D10–D12,
  D19).
- No India-scoped panel hits (D14–D16; the site: restriction was not
  honoured or returned noise).

## Final grades per in-scope item

| Item | Grade | Basis |
|---|---|---|
| VULONE campaign report + infrastructure IPs | ecology-context | Report content fetched and hashed; campaign claims single-sourced; no traffic observed by us. Not a launcher lead. |
| kyle-hatcher agent board | ecology-context | Live lab, stores/serves messages only. No malice observed. |
| themostusefulsiteintheworld board | ecology-context | Public board with safety rules. No malice observed. |
| CERT-In advisory coverage | ecology-context (known) | Already in corpus lane. |
| NorForge/Reuters campaign coverage | ecology-context (known) | Already known. |
| iLands agent diaries | ecology-context (known) | Tier-1-adjacent surface ecology. |

No launcher. No watch-only host. Nothing killed as a malice lead — the
boards and reports were never malice claims.
