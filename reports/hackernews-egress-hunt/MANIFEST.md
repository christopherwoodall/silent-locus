# MANIFEST: Hacker News agent-egress hunt

## Report

- REPORT.md — staged fleet report (ranked hits, appendix, killed list,
  coverage, pivots, novelty, limits, verifier note).
- hits.json — ranked hits, appendix vendor PoCs, killed list, coverage,
  novelty summary, shape scoreboard.
- MANIFEST.md — this file.
- SHA256SUMS — hashes for the report files below.

## Working lane files (working/)

- linguist-notes.md, linguist-candidates.md
- indicators.md, indicators.tsv
- adversarial-review.md
- enrichment.md, enriched-indicators.tsv
- follow-on.md, pivot-results.tsv

## Raw captures (data/lanes/hackernews-egress-hunt/raw/)

- algolia-A/ — 91 capture JSONs (5 terms, story/comment, fuzzy/exact),
  each with .PROVENANCE.txt and .sha256; COVERAGE.md; fetch scripts.
- algolia-B/ — 8 capture JSONs (4 terms, story/comment), each with
  .PROVENANCE.txt and .sha256; COVERAGE.md; CANDIDATES-B.md.
- algolia-C/ — 21 capture JSONs (6 phrases, story/comment), each with
  .PROVENANCE.txt and .sha256; COVERAGE.md; candidates-C.tsv;
  context-pre20251101.tsv; probes/.

## Rules kept

- No poster handles in any lane note or report file.
- Signed values never leave raw captures: parameter names and path
  shape only in notes and reports.
- Staged only. No Factum writes. No push from this fleet.
