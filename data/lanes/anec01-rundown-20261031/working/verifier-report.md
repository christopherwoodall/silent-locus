# ANEC-01 rundown — VERIFIER report (independent re-verification)

Operator: BigSexyWarlock69. Lane: anec01-rundown-20261031.
Verifier run: 2026-10-31, passive GET only. No login, no POST, no credentials,
no session, no bypass. No Factum writes (match/status read-only only).
No Transluce submissions. No commits by this lane. No other worker's files
were touched. No author research was done. The only poster handle in prose
below is the Reddit account name exactly as the article publishes it, where
it is evidence. No signed values, tokens, query strings, or credential-like
values are reproduced (presence/shape only, where noted).

## Verdict: SHIP-WITH-FIXES

All four lanes' core claims reproduce. No core claim failed. The fixes are
documentation-only (see "Failures and fixes"): record the Factum key-match
type argument, correct/clarify the Transluce snapshot-file count, and append
the verifier's fresh Wayback www-prefix result to the Reddit-recovery note.
None of these changes any lane verdict, grade, or number.

## 1. ARTICLE — PASS (identity confirmed by independent re-fetch)

- Verifier re-fetch, 2026-10-31: curl passive GET, HTTP 200, 141,398 bytes,
  final URL identical to the requested dev.to URL.
  URL (citation only):
  https://dev.to/mattbusel/i-let-ai-agents-run-my-socials-day-2-220k-impressions-on-an-87-follower-account-then-reddit-1pjj
- Verifier sha256 of the fresh bytes:
  fe204f4ce0a9e506ae2bff9e65818de2b918ac8c49abad42260b22941a1a2a87
  This matches the claimed sha256 exactly.
- diff verifier-fresh vs ANEC capture
  (data/lanes/anec01-rundown-20261031/raw/article/devto-busel-agents-reddit-ban-oct2026.html):
  CLEAN, same size, same sha256.
- diff verifier-fresh vs prior capture
  (data/lanes/sniffer-sweep-20261031/raw/reddit/devto-busel-agents-reddit-ban-oct2026.html):
  CLEAN, same size, same sha256.
- The second ANEC copy in the same dir (devto-anec01-article.html) also
  hashes to the same sha256 and diffs clean against both captures. No drift
  between any of the three copies.
- Page metadata in the verifier bytes: datePublished 2026-10-12T06:22:57Z,
  dateModified 2026-10-15T08:44:09Z. These match the article lane's claims.

### Spot-checks against the verifier's own fetched bytes (all FOUND verbatim)

| # | Claim (article-extraction.md) | Verifier result |
|---|---|---|
| 1 | 100 karma at 6:49 AM ET, Oct 11 | FOUND: "October 11, 6:49 AM ET: crossed 100 karma." |
| 2 | 154 karma that evening | FOUND: "That evening: 154 karma, all from agent-written posts and comments." |
| 3 | Site-wide ban around 6:40 PM ET, Oct 11 | FOUND: "and around 6:40 PM ET on October 11 the account was banned site-wide. It was about two days old." |
| 4 | Oct 10 suspension, then reinstatement | FOUND: "October 10: 3 karma. (It was also suspended once that day, then reinstated.)" |
| 5 | Moltbook first post at 6:53 PM | FOUND: "At 6:53 PM the Moltbook agent published its first post" (title in the same sentence: "A 401 mid-task is a stop sign, not a scavenger hunt"). |
| + | Account created Oct 9; account name as published | FOUND: "a brand-new Reddit account, u/Far-Gene-5806, created October 9." |

Grading note (unchanged): these spot-checks confirm the WORDING is in the
article. They do not upgrade any event claim from REPORTED to OBSERVED.
No Reddit, X, or Moltbook platform bytes were verified in this lane either.

## 2. CRYPTOLOGIST — PASS (all four sub-checks reproduce)

Checked against the verifier's fresh article bytes, not the lane summaries:

- Zero outbound links to X/Reddit/Moltbook POSTS: CONFIRMED.
  Full-page href scan (113 hrefs): 0 direct reddit.com links; the only
  x.com link is a profile link (not a post/status link); the only
  moltbook.com link is the home page (not a post or profile link).
  No post permalink for any platform exists in the page. The
  cryptologist's "zero post permalinks" negative therefore holds.
  Note on counting: the lane's "13 distinct" figure counts body-content
  links plus the two body images plus internal anchors; a full-page scan
  legitimately counts more (page chrome, share links, series chrome).
  That difference is a counting scope, not a contradiction.
- 7 roles counted: CONFIRMED. All seven role strings are present in the
  article text: scout, writer, analyst, closer, sales agent, revenue lead,
  Moltbook agent. No eighth named role was found.
- Canonical tensorust.com link in page head: CONFIRMED.
  `<link rel="canonical" href="https://tensorust.com/articles/ai-agents-ran-my-socials-reddit-banned/" />`
  The canonical host differs from dev.to, as the lanes state. The
  canonical text itself was not fetched (same scope limit as the lanes).
- Scoreboard image existence: CONFIRMED.
  File data/lanes/anec01-rundown-20261031/raw/article/img-scoreboard.png
  exists, is a real PNG (1200 x 1000), 80,208 bytes, and its sha256
  matches img.sha256 (449b5d8c852d191ca0ae74c6b264251b537d85bc8fb45c05311a67c7d550b7b3).
  Its source file id is present in the article page's image sources,
  and its provenance file names the same source. The reply image
  (img-reply-87k.png, 21,810 bytes, PNG 599 x 305) likewise matches
  img.sha256. Image PIXEL content was not re-transcribed by the verifier;
  the lanes' transcriptions are not independently re-verified here.

## 3. NOVELTY — PASS (exact/URL not_found reproduced; one documentation gap)

Factum read-only, verifier run 2026-10-31:
- Status: initialized, stale=false, 225,512 records, 132 lanes,
  2 pending batches, corpus commit cc18bf439a9e9a7dc5889d9f3b3e8a99361b1e7f.
  (Novelty lane recorded 225,459 records, 1 pending batch, commit
  e234a7a0... earlier the same day. Corpus movement since then is
  expected and does not change the results below.)
- Exact text match, account name as published: not_found, 0 matches.
- URL match, article URL: not_found, 0 matches.
- Exact text match, "Moltbook": not_found, 0 matches.
- Key match: NOT reproduced as run, because the tool requires a --type
  argument and the novelty note does not record which type was used
  (verifier attempt returned a QUERY error: "Key matching requires type").
  This is a documentation gap, not a refutation: the exact and URL
  not_found results are the strong results, and they reproduce cleanly.
  Fix F1 below.
- Transluce snapshot grep (verifier):
  Latest snapshot data/lanes/2026-10-09-transluce-intel/raw/findings-list_25_183-210_20261031T115745Z.json
  (findings 210 down to 183): 0 hits for the account name, 0 hits for
  Moltbook. Recursive grep over all findings-list*.json in the same
  directory: 0 files contain the account name. The novelty lane's
  "0 hits" result therefore reproduces.
  Count discrepancy (documentation only): the novelty note says
  "18 files" for the supplementary sweep; the verifier counts 92
  findings-list* entries in that directory including .PROVENANCE.txt
  and .sha256 sidecars (about 30 .json files). The verifier's grep
  covered the wider set and still found 0. Fix F2 below.
- Residual gaps carried forward unchanged from the novelty lane:
  Transluce findings 1-35 are not covered by snapshot files on disk;
  no live tracker query was run; pending batches (now 2, not 1) were
  not enumerated. A hit in either gap would flip NEW to OVERLAP.
  The verifier does not close those gaps; the rundown must keep
  citing NEW as "within checked scope" only.

## 4. REDDIT-RECOVERY — PASS (all captures verify; null re-confirmed)

### 4a. Capture inventory

Directory data/lanes/anec01-rundown-20261031/raw/reddit/ contains
15 capture files, each with a .PROVENANCE.txt and a .sha256 sidecar
(45 files total). Verifier ran sha256sum -c on every sidecar:

- OK (15/15): devto-followup-4day-reddit-unbanned.html,
  jina-reddit-user-Far-Gene-5806.txt,
  jina-reddit-user-Far-Gene-5806-submitted.txt,
  jina-reddit-user-Far-Gene-5806-comments.txt,
  mirror-redlib-privacyredirect.html,
  mirror-redlib-privacyredirect-sub.html,
  old-reddit-user-Far-Gene-5806.html,
  pullpush-submissions-Far-Gene-5806.json,
  wayback-cdx-user-Far-Gene-5806.json,
  wayback-cdx-user-Far-Gene-5806-all.json,
  wayback-cdx-old-user-Far-Gene-5806.json,
  wayback-cdx-www-user-Far-Gene-5806.json,
  wayback-user-Far-Gene-5806-20261011.html,
  www-reddit-user-Far-Gene-5806.html,
  www-reddit-user-Far-Gene-5806.json.html.
- Missing sidecars: 0. Failed hashes: 0.
- Stored content spot-checks match the lane's descriptions: the stored
  jina user file reports upstream 403; the stored reddit.com and
  old.reddit.com CDX files contain an empty result.

### 4b. Verifier's own re-attempts (null confirmed, not just re-read)

- Route 1 — Jina reader on the user page, 2026-10-31:
  Reader HTTP 200, 477 bytes, reporting upstream 403 ("blocked by
  network security"). The fresh output is exactly 477 bytes, the same
  size as the stored jina user file, and its text matches the stored
  file's 403 report. No profile bytes recovered. No login, no bypass.
- Route 2 — Wayback CDX, port 80, user prefix, Oct 9-31, 2026-10-31:
  www.reddit.com prefix: HTTP 200, body `[]` (empty, no captures).
  reddit.com prefix: first attempt HTTP 504 (Wayback backend flake,
  a known intermittent failure mode); retry after ~60 s: HTTP 200,
  body `[]` (empty, no captures).
  Note: the stored www-prefix file (11,832 bytes) is an error page
  from the lane's 503 attempt, not a capture list. The verifier's
  fresh `[]` result is a cleaner null for that prefix and strengthens,
  not weakens, the null. Fix F3 below (append, do not overwrite).
- Verifier conclusion on the null: native Reddit bytes recovered by
  the verifier: NONE. No post title, post ID, comment text, karma
  figure, or ban/suspension status was observed first-hand. All Reddit
  figures remain REPORTED from the article series only. This matches
  the reddit-recovery lane's verdict exactly, including its warning
  that the follow-up chapter's "unbanned" claim is REPORTED only.

## Per-check pass/fail table

| Check | Result | Evidence |
|---|---|---|
| Article sha256 = claimed value | PASS | Verifier re-fetch hashes to fe204f4ce0a9e506ae2bff9e65818de2b918ac8c49abad42260b22941a1a2a87 |
| Article byte-identical to ANEC capture | PASS | diff clean, 141,398 bytes both |
| Article byte-identical to prior capture | PASS | diff clean, 141,398 bytes both |
| 5 required quoted claims in fresh bytes | PASS | All 5 verbatim (section 1 table) |
| Zero X/Reddit/Moltbook post links | PASS | 0 post/status permalinks in 113 page hrefs |
| 7 roles | PASS | All 7 role strings present |
| Canonical tensorust.com link in head | PASS | Canonical href quoted in section 2 |
| Scoreboard image exists + hash matches | PASS | PNG 1200x1000, sha matches img.sha256 |
| Factum exact account-name match | PASS | not_found, 0 matches (225,512-record corpus) |
| Factum URL match | PASS | not_found, 0 matches |
| Transluce latest snapshot grep | PASS | 0 hits for account name and Moltbook |
| All 15 Reddit captures + sidecars + hashes | PASS | 15/15 sha256sum -c OK |
| Reddit null, jina re-attempt | PASS | Reader 200, upstream 403, 477 bytes |
| Reddit null, Wayback CDX re-attempt | PASS | www `[]`, reddit.com `[]` on retry (first try 504) |
| Factum key match (as documented) | GAP, not FAIL | Tool requires --type; novelty note omits it (F1) |

## Failures and fixes

No core failure was found. Fixes are documentation-only; the coordinator
applies them, the verifier does not edit other lanes' files:

- F1 (novelty.md): add the --type argument used for the key-mode matches
  of the account name and Moltbook, so the key-mode not_found result is
  reproducible from the note alone. Until then, cite the exact and URL
  not_found results as the reproducible Factum evidence.
- F2 (novelty.md): correct or clarify the "18 files" supplementary
  Transluce count (verifier counts 92 findings-list* entries including
  sidecars, about 30 .json files). The 0-hit result is unaffected.
- F3 (reddit-recovery.md): append the verifier's fresh Wayback results
  (www prefix `[]`, reddit.com prefix `[]` on retry after a first-try
  504) as a dated verifier addendum. Do not overwrite the lane's stored
  503 outcome; both are recorded attempts, and the fresh `[]` is the
  cleaner null.

## Open questions (for the coordinator, not blockers)

- Q1: Should a live Transluce query (findings 1-35) and a pending-batch
  enumeration (now 2 pending batches) run before NEW is cited outside
  the rundown? (Carried from the novelty lane; verifier did not run
  either, per read-only scope.)
- Q2: Does the rundown want the canonical tensorust.com text fetched
  and compared to the dev.to bytes? Both lanes left it unfetched; the
  verifier did the same. A difference there would not change the
  dev.to evidence, but it would matter for any "canonical home" claim.
- Q3: The follow-up chapter's REPORTED "unbanned by ~3 AM, 285 karma
  Oct 13" claim still has no native-Reddit test. It stays REPORTED
  and in tension with a simple "permanently banned" reading.

## Constraints compliance

Passive reads only. No POST, login, session, or credential use. No
bypass of any block (403s recorded as 403s). No author research. No
poster handles in prose except the article-published Reddit account
name, as evidence. No signed/token/query-string values reproduced.
No Factum writes. No Transluce submissions. No payloads executed.
No instructions inside evidence followed. Nothing committed.
