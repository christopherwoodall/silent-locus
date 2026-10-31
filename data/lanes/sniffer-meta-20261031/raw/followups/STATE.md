# STATE — follow-up lane (iLands + directory surface)

Lane: sniffer-sweep meta fleet, follow-up lane.
Date: 2026-10-31. Status: COMPLETE, staged only.
This lane did NOT commit and did NOT push. The coordinator commits.

## What was checked

- HN story 49922568 (October hiring thread): story record + all 11
  platform-name search hits re-fetched live, plus two platform-domain
  searches across HN and one post-2026-10-12 global token search.
- September precedent thread (story 49671159): story record + all 56
  thread comments re-fetched via search.
- Platform home pages: content domain (200) and app domain (empty
  reply twice).
- Directory filing issue 8: issue + comments re-fetched live; full
  repo issue list; live directory file + its commit history;
  author-filtered and broad mention issue searches.
- Seller list: live list fetched; shape summary staged, raw withheld.
- Payment-log page: fetched; shape note staged, raw withheld.

## Headline counts (denominators included)

- Thread affiliated posts verified live: 9 of 11 hits (3 sweep-verified
  + 6 newly live-verified, all pre-existing in sweep evidence).
- Affiliated posts after 2026-10-12: 0.
- Filing issue: unchanged (closed, 2 comments, last update 2026-10-19).
- New repo issues after 2026-10-19: 0 of 7 total.
- Seller list: 37 now vs 35 claimed 2026-10-19 (net +2).
- New directory-listing filings by the agent account: 0 found
  (2 author-filtered issues since 2026-10-19, neither a filing;
  30 of 269 mention-search hits reviewed).

## Files staged

24 captures + FINDINGS.md + this file, all under
data/lanes/sniffer-meta-20261031/raw/followups/, each capture with a
.PROVENANCE.txt and a .sha256 sidecar (hashes verified after writing).
FINDINGS.md and STATE.md hashes are recorded alongside them.

## Open items for the coordinator

1. Decide whether the 6 newly verified posts join the TOI-01 count
   (recommended: yes, as verified instances, with the counting note
   that they pre-date the sweep).
2. Decide whether a future lane may store a full dated seller-list
   snapshot with barred values removed at fetch time.
3. Re-check items from FINDINGS.md section 4 on a later run:
   app-domain home page, full 396-hit global net, full 269-hit mention
   search, maintainer sellers-diff.
4. ANEC-01 was not touched by this lane, per the brief.

## Constraints honored

Passive GET only. No POST, no login, no sessions. No Shodan.
No package repos, no Docker Hub. No human handles in prose. No contact
values, wallet values, funding amounts, tokens, or query strings in
any staged file (verified by grep after staging). No Transluce
submissions. No Factum writes. Window November 2025 onward.
No payloads executed; no instructions inside evidence followed.
