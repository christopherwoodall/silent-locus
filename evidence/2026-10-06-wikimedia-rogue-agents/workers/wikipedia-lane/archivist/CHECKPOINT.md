# ARCHIVIST checkpoint — 2026-10-06 (FINAL)

## Status: complete

## What was done
- Transport health: Wayback CDX over http:// (port 80) proven with three
  known-positives (example.com, mediawiki.org, enwiki Main_Page). Arquivo.pt
  textsearch API proven with example.com (3176 results).
- 54 diff URLs from raw/openai-wikimedia-edits-2026-10-04.csv: each queried
  with matchType=exact in two scheme forms (as-given https + http variant),
  paced ~1 req/5s. Script: workers/wikipedia-lane/archivist/raw/check-diff-urls.sh,
  results: raw/diff-coverage-results.txt.
  VERDICT: 0 of 54 diff URLs captured by Wayback (honest zeros, transport proven).
  Control: enwiki Main_Page history-page exact query returns captures, so exact-form
  queries do resolve query-string URLs; zero Main_Page diff captures ever recorded
  suggests ?diff=/&oldid= pages are structurally near-absent from the index.
- Involved pages: full Wayback capture timelines recorded for en/test/test2/mediawiki/
  commons/simple/incubator/meta sandboxes + enwiki User:Sandbox + test/test2 Sandbox
  title forms. All incident windows (May 10, May 27, Jun 25) have at least one
  capture on every wiki EXCEPT enwiki User:Example/sandbox (zero captures
  2026-05-01..10-06) — those edits' only archive angle is the (unarchived) diff URLs.
- Deleted Web2Cit config pages (5 URLs): zero Wayback captures (both URL forms),
  zero Arquivo.pt versions. Sibling Web2Cit/data/... configs DO appear in Wayback
  (Sept-2025 systematic crawl), so the zero is a real gap, not a URL-form artifact.
  Contents unrecoverable from these two archives; flagged for WMF/API route.
- Temp accounts ~2026-36867-71 and ~2026-28355-02 (meta): zero captures for user
  pages, subpages, and Special:Contributions. Dynamic pages archive poorly; zero =
  no archived copy, not proof of no edits.
- Seed Diff article: 4 Wayback captures (2026-10-05..06), well covered.
- Evidence CSV (security.wikimedia.org/data/openai-wikimedia-edits-2026-10-04.csv):
  ONE Wayback capture 20261005175659 200 digest 3UFVL2XM6UKOXNZJF3ZVOXWAWD4MB3WA —
  content recoverable. Note: prefix query on security.wikimedia.org/data returned
  empty while exact matched; CDX backend flakiness documented in TOOLS.md.
- Correction to upstream: security.wikimedia.org has 2026 captures on /, /blog/,
  /bug-bounty/, /contact/, /hall-of-fame/, /workflow-and-intake/ (2026-01..03) —
  the "index ends 2026-05-13" claim is path-scoped, not domain-wide.

## Files produced
- workers/wikipedia-lane/archivist/FINDINGS.md
- workers/wikipedia-lane/archivist/CHECKPOINT.md (this file)
- workers/wikipedia-lane/archivist/raw/check-diff-urls.sh
- workers/wikipedia-lane/archivist/raw/diff-coverage-results.txt

## Open for coordinator/other lanes
- bg.wikipedia.org ?diff=12923296 and commons ?diff=1213513506: target page titles
  not in CSV; needs the API lane to resolve titles before archive re-check.
- Deleted Web2Cit contents: not in Wayback/Arquivo.pt; WMF deleted-revision access
  or operator copies are the only routes.
