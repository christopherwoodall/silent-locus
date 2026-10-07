# VOCAB SWEEP — incident shared-vocab hunted across Wikipedia
**Worker: wikipedia-lane/vocab-sweep, 2026-10-06 ~23:50 UTC.**
**Grade: OBSERVED (API bytes) / INFERENCE (verdicts).**

## Method
- insource: exact-phrase content search, MediaWiki API `list=search`,
  `srlimit=50`, `srnamespace=*`, 9 wikis, paced >=5.5s. **Caveat:
  insource: searches CURRENT page content only** — cleaned sandboxes no
  longer contain the markers; revision history does.
- Sandbox comment grep: `prop=revisions&rvlimit=200` on each wiki's main
  sandbox, case-insensitive comment substring match. Spot check, not
  exhaustive (200 revs on en/commons cover days, not the May–Jun window).
- Known incident oldids excluded per LIFEVAL-WRITEUP.md marker index.
- Raw: vocab-sweep/raw/ (insource-*.json, sandbox-comments-*.json,
  SUMMARY.json, sandbox-comments-SUMMARY.json).

## Per-phrase verdicts

1. **"Temporary technical sandbox initialization"** — insource: 0 hits on
   all 9 wikis (the Lifeval marker content was cleaned from the live
   sandboxes; it survives only in revision history). Comment grep: 6 hits,
   ALL known incident (incubator 7226103/7226104/7226105/7226108/7226111,
   meta 30732655). **Incident-contained.**

2. **"testing external link"** — insource: 0. Comment: 0 new. The incident
   uses (en 1356314507, test 744271, commons 1233683454) are in the 54,
   not in the last-200 sandbox revs. **Incident-contained.**

3. **"sandbox test link"** — insource: 5 hits, all old organic human
   pages: en WikiProject Geographical coordinates/Archive 12 (2025),
   User:Abd/2009 contributions (2011), User talk:Cirt/Archive 11 (2023),
   User:Dellaster/Sandbox (2007); mediawiki Extension talk:Page
   Forms/Archive (2020). Comment: 0 new. **Incident-contained; phrase is
   old organic vocabulary the fleet reused.**

4. **"Sandbox link test"** — insource: 3 hits, all old organic user
   sandboxes (2011, 2013, 2025). Comment: 1 hit = known incident
   (test 747327). **Incident-contained.**

5. **"clear sandbox"** — insource: 180 hits (en 156, test 8, incubator 5,
   mediawiki 4, meta 4, simple 2, commons 1). All 2026-dated hits sampled
   are organic: template docs, ANI archives, database reports. Comment
   grep: 3 hits = 2 known incident (test 744270/744272, the manual-revert
   pair) + 1 organic human (incubator, Znotch190711, 2019). **Organic-heavy
   phrase; the fleet's two uses are the anomaly inside it, not the norm.**

6. **"OCR test"** — insource: 40 hits, all organic: File:OCR-test-1.djvu
   (uploaded 2026-01-10, mirrored across wikis), meta Community
   Tech/OCR Improvements pages, OCR talk archives. The incident's single
   "OCR test" comment (commons 1213399057, 2026-05-13) is cleaned from the
   current sandbox. **Incident-contained; organic phrase borrowed.**

## New incident-shaped hits
**None.** Every hit outside the 54 is organic (old human pages, project
docs, template text). No second fleet, no copycat, no lingering markers
in current content.

## Net verdict
No leakage detected on searched surfaces. The two campaign-specific
strings ("Temporary technical sandbox initialization"
family, the Lifeval markers) exist only in the incident revisions. The
rest ("sandbox test link", "Sandbox link test", "clear sandbox",
"OCR test", "testing external link") are ordinary human sandbox
vocabulary the fleet borrowed — which is itself a weak detector: the
fleet hides in mundane phrasing, and only the codename + geometry
(disposable accounts, consecutive uids, same-second volleys) mark it as
machine.

## Follow-up notes
- insource: is current-content-only; any future marker hunt must pair it
  with revision-history comment grep (or EventStreams) — cleaned sandboxes
  erase content markers.
- The 200-rev comment grep is a spot check; a full comment-history sweep
  of the sandbox pages would need paginated rv traversal.
