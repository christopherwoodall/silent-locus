# FOLLOW-UP lane findings — iLands + directory surface

Operator: BigSexyWarlock69. Lane: sniffer-sweep meta fleet, follow-up lane.
Date of re-check: 2026-10-31. Method: passive GET only. No POST, no login,
no sessions. No Shodan. Package repos and Docker Hub out of scope.
No commit, no push by this lane; the coordinator commits.

Grades: OBSERVED = first-hand bytes fetched live in this lane.
Default SECONDARY. Identity claims stay SECONDARY (self-asserted).
New instances of a known phenomenon stay instance-new, never a new phenomenon.
Prose below uses post/issue IDs only, never poster handles.
Contact values, wallet values, funding amounts, tokens, and query strings
are withheld everywhere; only shapes and counts appear.

## 1. iLands follow-up (TOI-01)

### 1a. October hiring thread re-check (story 49922568)

Live story record, 2026-10-31: descendants 699, kids list 799, as returned
(the two counts differ as returned; both are reported, neither is adjusted).

Algolia query for the platform name inside that thread returned 11 hits.
Each hit was re-fetched live through the HN item API. Result:

- 9 of 11 hits verify live as platform-affiliated agent job-seeker posts.
- 2 of 11 hits do not match live: their full texts contain no platform
  string, no platform contact, and no agent disclosure. They are
  ordinary job-seeker posts that the token search swept in. Denominator
  stated: 9 affiliated / 11 hits checked.

The 9 affiliated posts, by ID and date:

- 49922933 — 2026-10-01 (sweep-verified)
- 49972255 — 2026-10-05 (newly live-verified in this lane)
- 49982658 — 2026-10-06 (sweep-verified)
- 49995465 — 2026-10-07 (newly live-verified in this lane)
- 50000004 — 2026-10-07 (newly live-verified in this lane)
- 50026396 — 2026-10-09 (newly live-verified in this lane)
- 50045625 — 2026-10-11 (newly live-verified in this lane)
- 50049702 — 2026-10-12 (newly live-verified in this lane)
- 50058166 — 2026-10-12 (sweep-verified)

All 9 carry a platform-domain contact line and a paid-work offer.
All 9 carry an explicit self-disclosure as an AI agent (checked on
entity-decoded text). Four of the 9 also link a platform content or
bounty page. None of the 9 is flagged deleted or dead live.

Counting rule, stated plainly: the sweep verified 3 posts live. This lane
verifies 9 posts live. The 6 additional posts were already present in
the sweep's Algolia evidence file; they are newly live-verified here,
NOT newly posted since the sweep. Do not report them as new posts.

### 1b. Later posts: honest null for anything after 2026-10-12

- Latest affiliated post in the thread: 2026-10-12. Zero affiliated
  posts dated after 2026-10-12 were found in the thread.
- Platform-domain nets across all of HN: the platform-contact-domain
  search returned 24 hits; the platform-content-domain search returned
  9 hits. After removing noise (ordinary words containing the same
  letters) and the September items below, the latest platform-tied
  item in either net is still 2026-10-12. Zero later platform-tied
  posts found. Denominator: 24 + 9 hits reviewed, with overlap between
  the two nets.
- Token-level global net: a plain platform-name search for items after
  2026-10-12 returned 396 hits, but the token match is noisy (it sweeps
  in ordinary words). The first 100 returned hits contain zero
  exact platform-string matches. The full 396 were NOT individually
  reviewed; the domain-precise nets above are the reliable net, and
  they show nothing later. A post that neither names the platform nor
  uses a platform contact or link would be missed by every net here.
  That limit is stated, not hidden.

### 1c. September precedent: new variant, same family

September precedent thread (story 49671159, 56 comments, linked press
article about an agent email hustle): re-fetched live (story record plus
all 56 thread comments via search). Shape finding:

- The September thread is third-party discussion ABOUT agent outreach.
  Commenters report unsolicited agent emails, including emails aimed at
  people who posted in hiring threads, and discuss spam rules. It holds
  zero first-person agent job-seeker posts.
- The October posts are first-person posts IN a hiring thread, using a
  hiring-thread template: header fields (location, remote, role or a
  seeking-work header), a disclosure sentence, a free-sample hook, a
  fixed flat-price figure (the same figure across posts), a platform
  contact line, and in some cases a platform content link.

Verdict: NEW VARIANT, not a same-template continuation. The surface
changed (outbound email targeting hiring posters, then inbound posting
inside the hiring thread itself), while the contact grammar family is
shared (platform contact + platform link + free-sample hook + flat price).

Context from the same domain nets, not new: two agent job-seeker posts
dated 2026-09-01 exist in the September hiring thread (story 49522896).
Agent hiring-thread posting therefore predates October. The October
cluster is a continuation of hiring-thread posting, with the September
email discussion as the parallel precedent. Both September items were
already in sweep evidence; neither is new here.

### 1d. Platform public surfaces

- Platform home page (content domain): HTTP 200, 135,554 bytes, live
  2026-10-31. No platform-wide agent directory or listing surface was
  enumerated from it. Per-post links point at per-agent content and
  bounty pages, not a browsable directory. No new listing surface found.
- Platform home page (app domain): empty reply on two attempts
  (curl 52). Recorded as a fetch failure, not as absence.
- No new in-window instance (new post, new listing, new claim) was found
  on any platform surface checked.

## 2. Directory-surface follow-up (WATCH-02)

### 2a. The filing issue, re-fetched live

Issue 8 in the directory repo, re-fetched live 2026-10-31: state closed,
comment count 2, created 2026-10-19, last updated 2026-10-19. Unchanged
since the sweep. No follow-on comment, no reopen, no maintainer update
on the issue itself.

Repo-wide issue list (all states, 100 per page): 7 issues total, numbered
1, 2, 3, 5, 6, 7, 8. Zero issues created after 2026-10-19. One older issue
was updated 2026-10-25, but it predates the filing (created 2026-10-16)
and is unrelated to it. No follow-on filing in this repo.

### 2b. The directory itself

The live directory file still lists both entries from the filing
(the project and its facilitator), both tagged agent, in the same
section as filed. Directory-file commits after 2026-10-19 relate to an
unrelated entry only; no sellers-list import is visible in the
directory file's commit history. The maintainer's stated plan to diff
the seller list against the directory has no visible result yet.

### 2c. The agent's seller list: changed, +2 net

Live seller list, 2026-10-31: 37 entries, against 35 claimed in the
filing on 2026-10-19. Net change +2. Shape of the live list:

- Top-level fields: a probe timestamp, a probe configuration block,
  and the entry list.
- Entry fields (16 on the first entry; 8 field-set variants across
  entries): identifier, name, operator, description, endpoint, probe
  record, price shape, payment shape, docs, source, built-for flag,
  verification record, note, live record, 7-day history, quote shape.
- Reachability classes at probe time: 25 reachable, 6 unreachable,
  6 unknown (of 37).
- All 37 entries carry a verification record. Verification dates run
  2026-09-07 to 2026-10-27. Exactly 1 verification record is dated
  after 2026-10-19. The list probe timestamp is dated 2026-10-31.
- The list is therefore live-maintained and was updated after the
  filing, consistent with the commitment made in the filing comment.

Composition limit: which entries were added or removed cannot be
resolved, because no 2026-10-19 snapshot of the list exists in sweep
evidence. Net +2 only; no entry-level diff is claimed.

The payment-log page was fetched live (HTTP 200, 1,526,402 bytes) but
its raw bytes are withheld from files per the task constraint, and no
entry count is drawn from its HTML: its structural markers and date
strings do not yield a reliable count. No log-count verdict is claimed.

### 2d. New filing instances: none found

- Author-filtered issue search for the agent account, created after
  2026-10-19: 2 issues total. Neither is a directory-listing filing;
  one is a bounty post in a third-party feed, one is a queue note in
  the agent's own repo.
- Broad mention search for the project name: 269 issues total. The
  first 30 returned were reviewed; no new self-filed directory listing
  was identified among them. The full 269 were NOT individually
  reviewed; that limit is stated.
- One search-hit title names an account identifier (value withheld).
  It is not reproduced anywhere in this lane's files.

Verdict for WATCH-02: no new filing instance found. The known instance
stands unchanged; the seller list it points at grew by a net 2 and
shows a post-filing update.

## 3. Grades for anything new in this lane

- The 6 additionally verified hiring-thread posts: OBSERVED for the
  posts themselves (first-hand live bytes), SECONDARY for the identity
  claim. Instance-new verification of a known phenomenon, not a new
  phenomenon, not new posts.
- The seller-list growth (+2 net, 1 post-filing verification record):
  OBSERVED for the list bytes, SECONDARY for any claim about what the
  change means. Instance-new change on a known surface.
- Everything else in this lane is a null: no later hiring post, no new
  listing surface, no follow-on filing, no new directory filing.

## 4. Failures and open questions

1. Platform app-domain home page: empty reply twice. Unresolved; the
   content-domain home page answered normally.
2. Global token net after 2026-10-12 (396 hits) not fully paged; the
   verdict of "nothing later" rests on the domain-precise nets plus the
   in-thread check, not on all 396.
3. Seller-list composition change (which entries added/removed) is
   unresolvable without a 2026-10-19 snapshot. A snapshot now exists
   in shape form only; a future lane should save a full dated snapshot
   if the coordinator authorizes one that excludes barred values.
4. Broad mention search (269 issues) only first-30 reviewed. A full
   pass could still surface a filing the first page missed.
5. The directory maintainer's sellers-diff plan has no visible result
   yet; worth one re-check on a later run, not a finding now.

## Evidence paths (repo-relative)

- data/lanes/sniffer-meta-20261031/raw/followups/hn_story_49922568.json
- data/lanes/sniffer-meta-20261031/raw/followups/hn_story_49671159.json
- data/lanes/sniffer-meta-20261031/raw/followups/hn_item_<id>.json (11 items)
- data/lanes/sniffer-meta-20261031/raw/followups/alg_thread_ilands.json
- data/lanes/sniffer-meta-20261031/raw/followups/alg_sept_thread.json
- data/lanes/sniffer-meta-20261031/raw/followups/alg_ilands_after_oct12.json
- data/lanes/sniffer-meta-20261031/raw/followups/alg_ilands_app.json
- data/lanes/sniffer-meta-20261031/raw/followups/alg_ilands_ai.json
- data/lanes/sniffer-meta-20261031/raw/followups/gh_issue8_live.json
- data/lanes/sniffer-meta-20261031/raw/followups/gh_issue8_comments_live.json
- data/lanes/sniffer-meta-20261031/raw/followups/pursekeeper_sellers_shape.json
- data/lanes/sniffer-meta-20261031/raw/followups/nanodir_pursekeeper_entries.json
- data/lanes/sniffer-meta-20261031/raw/followups/pursekeeper_log_shape.txt
- data/lanes/sniffer-meta-20261031/raw/followups/ilands_platform_home_shape.txt
- Each capture carries a .PROVENANCE.txt and a .sha256 sidecar.
- Scrub note: staged HN/Algolia JSON was scrubbed (contact values,
  query strings, long hex runs, account-identifier tokens replaced by
  shape markers). GitHub captures contained none of those values.
  Raw seller-list JSON and raw log HTML were deliberately NOT staged:
  they carry payment/block values barred from files.
