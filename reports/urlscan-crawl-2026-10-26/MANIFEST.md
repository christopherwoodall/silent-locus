# Manifest — urlscan crawl report, 2026-10-26

## Terms

- **Artifact**: a file in this directory that forms part of the deliverable.
- **SHA256SUMS**: a file that lists a hash for each artifact, used to check
  that files did not change.

## Deliverables

| File | What it is |
|---|---|
| REPORT.md | Final report: coverage, ranked hits, novelty, behavior notes, ingest, exclusions, open items. |
| THIRD-PARTY-REPORTS.md | Third-party reports that bear on the findings, each graded, with what each corroborates and does not. |
| VERIFICATION.md | Verifier re-fetch results and final adversarial review of REPORT.md. |
| hits.json | Machine-readable hit list (Rank 1 ingested, Rank 2 sibling-owned, crawl haul zero). |
| hits-draft.json | Crawl executor draft: empty list (0 triage-passing crawl hits). |
| coverage.md | Crawl coverage table, exclusions, limits. |
| crawl-progress.log | Per-query status lines. Local-only: gitignored (`*.log`), present on disk and hashed in SHA256SUMS, but not in the commit. |
| linguist-review.md | Linguist lane output. |
| cryptologist-review.md | Cryptologist lane output. |
| adversarial-review-crawl.md | Adversarial lane output (crawl pass). |
| adversarial-review-final.md | Final adversarial review of REPORT.md, with required fixes (all applied). |
| third-party-reports-draft.md | Third-party lane draft (promoted verbatim to THIRD-PARTY-REPORTS.md). |
| ingest-note.md | Ingest lane output (Oct 25 bundle, ipv6 gap). |
| crawl.py, triage.py | Executor working scripts (not deliverables). |

## Raw evidence

- `raw/<query-label>/search.json` — verbatim urlscan search response per
  query (6 queries).
- `raw/<query-label>/.PROVENANCE.txt` — source address, retrieval time
  (UTC), method per query.
- `raw/<query-label>/*.sha256` — one hash file per captured file.
- `raw/screenshots/` — empty (no triage-passing hits, so no screenshots
  were fetched).

## Factum artifacts (outside this directory)

- Batch `data/records/a3fc917d22794d0eb9dbea8ba6b1d405/` — 3 records,
  all `tags.lane=urlscan` (Rank 1 hit). Already tracked in git via
  commit `0c1ef707`.
- Lane dir `data/lanes/urlscan/` — `PROVENANCE.md`,
  `bundle-20261025T145711Z-ingest.json`, `raw/` verbatim copies.

## Integrity

`SHA256SUMS` covers every file in this directory except itself and this
manifest. All 39 entries verified OK after the final-review fixes
(regenerated to include VERIFICATION.md and
adversarial-review-final.md). Re-check with:

```
sha256sum -c SHA256SUMS
```
