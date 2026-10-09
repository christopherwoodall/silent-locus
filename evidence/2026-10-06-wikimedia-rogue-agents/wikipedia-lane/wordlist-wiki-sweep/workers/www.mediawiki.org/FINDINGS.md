# WORDLIST-WIKI-SWEEP — IOC wordlist hunted on www.mediawiki.org
**Worker: wikipedia-lane/wordlist-wiki-sweep, www.mediawiki.org lane, 2026-10-07 ~00:42–02:25 UTC.**
**Grade: OBSERVED (API bytes) / INFERENCE (verdicts).**

## Method
- 1,148 IOC wordlist terms (launcher/toolkit markers, relay hostnames,
  dead-drop services, eval names, target refs) → MediaWiki API
  `insource:"<term>"` exact-phrase content search, `srlimit=50`,
  `srnamespace=*`, paced >=5.2s, every response (hits AND zeros) cached in
  `raw/www.mediawiki.org/insource-<n>.json` with a JSONL run log.
- Sandbox revision spot check: 200 most recent Project:Sandbox revs
  (2026-08-19→2026-10-06) — all 1,148 terms case-insensitive matched
  against edit comments; plus full contents of the 63 temp-account
  (~2026-*) revs within them.
- **Caveat: `insource:` is current-content-only** — cleaned sandboxes erase
  content markers; the comment/content grep covers the gap partially.
- Raw: `raw/www.mediawiki.org/` (insource-*.json x1148, run-log.jsonl,
  sandbox-comments*.json, sandbox-tempaccount-revs.json, PROVENANCE.md,
  SUMMARY.json).

## Per-category hit tally (insource, current content)
<!-- filled after collection -->

## Sandbox revision greps
- **Comment grep (200 revs):** 0 matches for any of the 1,148 terms.
- **Temp-account content grep (63 revs):** 0 matches. The ~2026-* sandbox
  editors in the window are ordinary humans ("Jus messin round n testin",
  "pruebas", "Банае", "the testing area") — no machine markers, no links
  to relay/dead-drop services.

## Hit grading
<!-- per-hit grading after collection -->
- known-incident (oldid in incident set): —
- incident-shaped-new: —
- organic: —
- noise: —

## Net verdict
<!-- after collection -->
