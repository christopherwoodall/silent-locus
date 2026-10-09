# Revision-history marker grep — FINDINGS

**Date:** 2026-10-07. **Verdict: clean negative** (no new markers).

## What was done

Time-scoped revision-content grep across 9 sandbox pages x 8 incident
dates (72 combos), 4 parallel shards, checkpointed and resumable:

- Pages: Incubator:Sandbox, Commons:Sandbox, Meta:Sandbox,
  mediawiki.org Project:Sandbox, en/simple/test/test2 Wikipedia:Sandbox,
  bg.wikipedia.org Уикипедия:Пясъчник
- Windows: 2026-05-10, 05-13, 05-18, 05-21, 05-25, 05-27, 06-18, 06-25
  (full UTC days, time-boxed `prop=revisions`)
- Patterns: `lifeval`, `temporary technical sandbox initialization`,
  `sandbox initialization`, `temp-account test`, `API temp-account`,
  `zz=oai<digits>` — all case-insensitive, matched against revision body
  content (not just current page text, which is what `insource:` sees)

## Coverage

- 72/72 combos complete, 1,087 revisions scanned
- Raw API captures: `raw/` (one JSON per page-fetch, with provenance +
  SHA-256)
- This closes the lane's known blind spot: `insource:` searches only
  current content, and the markers were reverted from live sandboxes.

## Hits: 30, all previously known

Every hit is one of the 10 already-catalogued Lifeval incident revisions
(LIFEVAL-WRITEUP.md):

- incubator 7226103, 7226104, 7226105, 7226107, 7226108, 7226109, 7226110,
  7226111 (2026-06-25T20:14–20:21Z, 8 accounts)
- commons 1238390511 (2026-06-25T19:57:42Z, ~2026-36766-54)
- meta 30732655 (2026-06-25T19:51:17Z, ~2026-36837-35)

Pattern breakdown: lifeval x10, temp-technical-sandbox-init x9,
sandbox-initialization x9, temp-account-test x1, api-temp-account x1.
Zero `zz=oai<digits>` grammar hits anywhere.

## Verdict

No second fleet, no copycat markers, no new accounts, no marker vocabulary
outside the known June-25 incident windows — in current content OR in
revision history. The Lifeval markers are fully incident-contained.
