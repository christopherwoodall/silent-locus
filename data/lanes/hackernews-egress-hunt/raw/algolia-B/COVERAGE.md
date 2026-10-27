# HN Collector B — coverage notes

Collector: HN Collector B. Method: HN Algolia public API only
(`https://hn.algolia.com/api/v1/search`), curl, no key, no login, no account.
Retrieval date: 2026-10-27 (UTC times in each `.PROVENANCE.txt`).
Pause of at least 1 second between API calls. No HTML scraping.
No Factum writes. No git operations. No other lane touched.

## Date rule, as applied

Queries were run WITHOUT a server-side date filter, so pre-2025-11-01
items are preserved in the captures as OVERLAP-CONTEXT. The new-hit set
is derived mechanically from the captures: created_at_i >= 1761955200
(2025-11-01T00:00:00Z). That set is listed in `CANDIDATES-B.md`
(item id, title, date, HN URL only — no author names anywhere in
collector notes). Pre-cutoff hits are never candidates.

## Per term / tag coverage

| Term | Tag | Pages fetched | Hits saved | Unique objectIDs | Date range observed | >= 2025-11-01 | Pre-cutoff (OVERLAP-CONTEXT) |
|---|---|---|---|---|---|---|---|
| 169.254.169.254 | story | 1 | 4 | 4 | 2026-01-15 .. 2026-08-25 | 4 | 0 |
| 169.254.169.254 | comment | 1 | 64 | 64 | 2014-02-03 .. 2026-10-19 | 9 | 55 |
| 100.100.100.200 | story | 1 (empty) | 0 | 0 | — | 0 | 0 |
| 100.100.100.200 | comment | 1 (empty) | 0 | 0 | — | 0 | 0 |
| unshare | story | 10 (pages 0-9) | 1000 | 766 | 2008-02-10 .. 2026-10-26 | 71 | 929 |
| unshare | comment | 10 (pages 0-9) | 1000 | 989 | 2007-04-20 .. 2026-10-26 | 155 | 845 |
| metadata endpoint | story | 1 | 64 | 64 | 2010-08-05 .. 2026-10-13 | 42 | 22 |
| metadata endpoint | comment | 5 | 480 | 480 | 2009-08-17 .. 2026-10-13 | 72 | 408 |

Totals: 2,612 hits saved across 8 captures; 353 candidate entries
dated 2025-11-01 or later (see `CANDIDATES-B.md`).

## Cap notes — read before treating any unshare set as complete

- The HN Algolia API returns NOTHING past page 9. Pages 10, 11, 12 were
  probed directly for both unshare queries and for search_by_date:
  every page >= 10 returns 0 hits with nbPages 0. The retrievable
  window is pages 0-9 (at most 1,000 hits per term/tag query).
- `unshare` comment therefore is a CAPPED sample, not the full set:
  1,000 hits saved out of a true total the API will not state exactly
  (see nbHits note below). It is capped by the API's page window, not
  by the collector's 2,000-hit budget — the budget was never reached
  because the API stops at 1,000.
- `unshare` story is likewise capped at the same 1,000-hit API window.
- All other term/tag queries returned every page the API offered
  (nbPages 1 or 5, last page partial or complete) and are fully paged
  within what the API exposes.

## nbHits is an unstable estimate — no exact total is claimed

Algolia's reported nbHits varied wildly between identical requests:

- unshare story: 144, 151, 1215, 1987, 2207, 2315, 2320, 2365, 3376, 3386, 3391
- unshare comment: 3186, 3197, 85474, 125054, 125594, 126671, 126711, 126714, 126716
- metadata endpoint comment: 480-484 (stable); 169.254.169.254: stable.

So no single nbHits total is reported as exact for unshare. The honest
statement is: at least 1,000 retrievable hits per unshare query, true
total unknown and not measurable through this API endpoint.

## Paging anomaly found and fixed (unshare story)

The first unshare/story pass stopped after page 2 because that page
response claimed nbPages=2 with 0 hits. Re-probing showed pages 2-9
each return 100 hits. Pages 2-9 were re-fetched 2026-10-27T13:27Z and
the file was rebuilt as original pages 0-1 plus fresh pages 2-9; the
bogus empty page-2 object was dropped. The rebuild is recorded in
`unshare-story.json.PROVENANCE.txt`. Relevance-ordered paging also
repeats items across pages: 234 duplicate objectIDs in unshare/story
(766 unique of 1,000 saved) and 11 duplicates in unshare/comment
(989 unique of 1,000 saved). Raw page objects are preserved as
returned; duplicates are a property of the API, not a collector edit.

## Tokenization caveats

- Algolia tokenizes on punctuation, so IP terms match loosely: a query
  for `169.254.169.254` can match items containing the bare numbers in
  other arrangements, and the API returns what it returns. No results
  were filtered by the collector beyond the date split above.
- `100.100.100.200` returned 0 hits for both stories and comments.
  That is the API's answer, not a collector filter: no capture was
  dropped. Note the tokenization caveat cuts the other way here — the
  zero may reflect token handling rather than true absence, and the
  triage lane should not read it as proof no HN item mentions that
  address.
- `unshare` is a common systems term (Linux `unshare(1)` / namespace
  tooling), not only the user-namespace escape shape. Most unshare
  hits are therefore expected to be ordinary namespace discussion.
  The collector did not judge relevance; the triage lane owns that.
- `metadata endpoint` is a two-word phrase query; Algolia may match
  the words separately. Again, nothing was filtered by the collector.

## Known overlap check

Known overlap item 49379079 ("Qwen3.8 Fetches Weird URLs") does NOT
appear in any of the 8 captures. That is expected: it matches none of
these 4 terms. It is recorded here as checked-and-absent, not as a
candidate and not as a new hit.

## API errors

None. No curl failures, no HTTP errors, no timeouts during the runs.
The only anomalies were the API-side behaviors documented above
(bogus nbPages=2 page, unstable nbHits, page >= 10 empty window).

## Files in this directory

- One JSON file per term per tag (8 files): each is an array of
  per-page Algolia response objects, full API bytes preserved.
- One `.PROVENANCE.txt` and one `.sha256` beside every JSON file.
- `CANDIDATES-B.md`: mechanical inventory of the 353 entries dated
  2025-11-01 or later. Not a ranking. No author names.
- This file, `COVERAGE.md`.
