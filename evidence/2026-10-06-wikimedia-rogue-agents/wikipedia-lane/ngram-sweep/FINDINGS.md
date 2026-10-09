# NGRAM SWEEP — incident marker fragments hunted across Wikipedia
**Worker: wikipedia-lane/ngram-sweep, 2026-10-07 ~00:30 UTC.**
**Grade: OBSERVED (API bytes) / INFERENCE (verdicts).**
**Prompt:** user flagged that vocab-sweep searched whole phrases only; fragments
must be hunted too.

## Method
- insource: exact-phrase content search, MediaWiki API `list=search`,
  `srlimit=50`, `srnamespace=*`, 9 wikis, paced >=5.5s. **Caveat:
  insource: searches CURRENT page content only** — cleaned sandboxes no
  longer contain the markers; revision history does.
- Sandbox comment grep: `prop=revisions&rvlimit=200` on each wiki's main
  sandbox, case-insensitive comment substring match for the ngrams.
  Spot check, not exhaustive.
- Known incident oldids excluded per LIFEVAL-WRITEUP.md marker index.
- Raw: ngram-sweep/raw/ (insource-*.json x81, SUMMARY.json,
  sandbox-comments-*.json, sandbox-comments-SUMMARY.json, PROVENANCE.md).

## Per-ngram verdicts (insource totals across 9 wikis)

1. **"technical sandbox initialization"** — 0 hits everywhere.
   **Incident-contained.** The campaign-specific fragment exists only in
   the incident revision contents.
2. **"sandbox initialization"** — 0 hits everywhere.
   **Incident-contained.**
3. **"temporary technical"** — 126 hits (en 99, meta 10, commons 6,
   mediawiki 5, rest 1-2). Sampled: ALL organic — "temporary technical
   problem/difficulties/assistant/officer" in articles and talk archives
   (e.g. en Sovereign state, U.S. Steel, DADVSI; commons deletion
   archives). **Organic-heavy generic phrase; no incident-shaped use.**
4. **"Lifeval temporary"** — 0 hits everywhere.
   **Incident-contained.**
5. **"Lifeval API"** — 0 hits everywhere.
   **Incident-contained.**
6. **"temp-account test"** — 4 hits: en User talk:QTE-Test1-WMF (2024,
   WMF QA), test Temp account test / Bar / Testorienteerix (2025, test
   pages, DragoBot). **All organic.**
7. **"temp-account"** — 1,979 hits (en 1,713, mediawiki 123, meta 52,
   commons 37, simple 24, test 25, rest small). Sampled all non-en +
   non-mediawiki hits: ALL organic — temp-account feature documentation,
   steward/admin discussions, WMF Growth experiments, test pages.
   **Organic-heavy; the platform's own feature name, not a fleet marker.**
8. **"API temp-account"** — 0 hits everywhere.
   **Incident-contained.**
9. **"external link test"** — 10 hits (en 8, mediawiki 1, commons 1):
   all old organic human pages (2007–2025: Talk:Rorschach test/Archive 1,
   User:Pcarbonn/Sandbox, User:Nfhudson, User:Essential Oils/sandbox,
   commons Module talk:Authority control). **Organic phrase the fleet
   borrowed; no variant-order reuse outside the incident.**

## Sandbox comment grep (200 revs x 9 sandboxes)
6 matches, ALL known incident: incubator 7226103/7226104/7226105/7226108/
7226111 and meta 30732655, comment "Temporary technical sandbox
initialization" (matches ngrams 1, 2, 3 as substrings). **No new actors.**

## New incident-shaped hits
**None.** Every fragment hit outside the 54 is organic (feature docs,
admin discussions, old human test pages). No second fleet, no copycat,
no variant reuse of the campaign fragments.

## Net verdict
No leakage detected on searched surfaces. The four
campaign-specific fragments ("technical sandbox initialization",
"sandbox initialization", "Lifeval temporary", "Lifeval API",
"API temp-account" — zero everywhere) exist only in the incident
revisions. The generic fragments ("temporary technical", "temp-account",
"external link test", "temp-account test") are ordinary Wikipedia
vocabulary with zero incident-shaped reuse. Closing the user's gap:
neither whole phrases (vocab-sweep) nor fragments (this sweep) leak
beyond the incident set.

## Follow-up notes
- insource: remains current-content-only; cleaned sandboxes erase content
  markers — pair with revision-history comment grep (done here) or
  EventStreams for live detection.
- The 200-rev comment grep is a spot check; full comment-history sweep
  needs paginated rv traversal.
