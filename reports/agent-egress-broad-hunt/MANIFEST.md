# Manifest — broad agent-egress hunt

Status: STAGED, not filed to Factum. A sibling phase-2 ingest owns all
Factum writes. Parent push pending.

## Report files (this directory)

- REPORT.md — ranked hits, lead, appendix, triaged-out, coverage,
  novelty verdicts, honest nulls, exclusions, open items.
- hits.json — machine-readable ranked hits, lead, appendix,
  triaged-out, coverage, zero surfaces.
- adversarial-review.md — kill/downgrade/survive verdicts per claim,
  final endorsed ranking.
- verifier-report.md — per-citation PASS/FAIL/UNVERIFIED, SHA256SUMS
  results per raw dir, signed-URL-rule grep result. Verdict:
  SHIP-WITH-FIXES. Required fix F1 applied in REPORT.md (urlscan rig:
  5 distinct scans in 6 search rows).
- lanes/*.md — one lane summary per executor: github-issues,
  github-code, huggingface, urlquery, urlscan-wayback-crtsh,
  linguist-notes, cryptologist-notes.
- SHA256SUMS — hashes of the report files above (this file and
  MANIFEST.md excluded by construction; verify with
  `sha256sum -c SHA256SUMS` from this directory).

## Raw evidence

- `data/lanes/agent-egress-broad-hunt/raw/` — 1,468 files, 43 MB.
  Per-surface subdirs: github-issues, github-code, huggingface,
  urlquery, urlscan-wayback-crtsh, linguist, cryptologist.
  Each capture carries .PROVENANCE.txt (source URL, retrieval time,
  method) and .sha256, plus a per-dir SHA256SUMS. Verifier: all 7 raw
  dirs PASS (cryptologist 4, github-code 16, github-issues 12,
  huggingface 948, linguist 2, urlquery 162, urlscan-wayback-crtsh 54
  files hashed). Raw files are never redacted. Derived reports carry
  parameter names and path shapes only, never signed query values.

## Known gaps (see REPORT.md open items)

- No lane ran full Factum novelty checks. Ranked items are not NEW
  claims until phase-2 ingest runs them.
- Linguist raw dir holds only the two akasecurity bodies; no saved page
  text for the Zenity, Field Effect, or bex posts.
- Linguist SHA256SUMS covers only its 2 JSON files, not provenance
  files (verifier F3, completeness gap).
- Live re-checks UNVERIFIED by the shared-IP GitHub rate limit (3 GitHub
  issues, 1 code repo): on-disk PASS stands.
