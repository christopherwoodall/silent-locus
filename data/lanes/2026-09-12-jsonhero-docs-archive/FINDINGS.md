# Findings — 2026-09-12-jsonhero-docs-archive

Grade claims OBSERVED, UPSTREAM, or INFERENCE.

## OBSERVED

- One jsonhero.io shared doc (`swJMw8b6VwDC`) was recovered from a Wayback
  capture dated 2026-09-12T07:50:05Z (HTTP 200, 95,501 B). The payload was
  embedded in the captured page's `window.__remixContext` as a JS object
  literal and was extracted and converted to strict JSON.
- The recovered doc is an older vintage of the SEC Regulation Crowdfunding
  county dataset: its title shows it was made from a 2025-01-13 Wayback
  capture of `https://www.sec.gov/files/county.json`. It lacks the
  `regCF_county_2024` array the live docs carry.
- Five docs returned zero Wayback CDX captures (exact and wildcard):
  `S5R1RRn64PLh`, `aB94pTzmWvtl`, `qDhAiEHyjXYi`, `wANOlosoW5YN`,
  `1vaGknk7ajC4`.

## UPSTREAM

- Corpus URL occurrence counts (scan of the collusion-wiki corpus):
  `swJMw8b6VwDC` 129, `S5R1RRn64PLh` 182, `aB94pTzmWvtl` 136,
  `qDhAiEHyjXYi` 6, `wANOlosoW5YN` 1, `1vaGknk7ajC4` 1.

## INFERENCE

- The agents re-minted the dataset from an archived upstream when the live
  SEC file changed or blocked them (older-vintage doc with no 2024 array,
  recovered from Wayback).
- The five "not archived" verdicts are medium confidence, not absence:
  they are Wayback-only because archive.today was unreachable from the
  collection network. A re-check from an unfiltered network is the recorded
  next step.
