# PROVENANCE — simple.wikipedia.org insource sweep
**Worker: wikipedia-lane/wordlist-wiki-sweep, simple.wikipedia.org.**
**Started: 2026-10-07 ~00:52 UTC.**

## Method
- `https://simple.wikipedia.org/w/api.php?action=query&list=search&srsearch=insource:"<term>"&srlimit=50&srnamespace=*&format=json`, term URL-encoded, paced >=5.2s between requests, User-Agent `silent-locus-wordlist-sweep/1.0 (research; contact: swarmtracers)`.
- 1,148 terms from `wordlist-wiki-sweep/search-terms.json` (built 2026-10-07T00:45:00Z from `~/workspace/silent-locus/ioc-wordlist/wordlist.json` status=active; question_terms/sqli/xss/encoded-payloads/bare-ips/pure-hex excluded).
- EVERY response cached (hits AND zeros): `insource-<n>.json` (n = term index in search-terms.json). Run log: `run_log.tsv` (index, term, category, utc timestamp, http status, returned hits, totalhits).
- Sandbox comments: `sandbox-comments-simple.json` — `prop=revisions&rvlimit=200` on Wikipedia:Sandbox (2026-09-21T06:59:45Z → 2026-10-06T02:12:16Z), case-insensitive grep of all 1,148 terms against edit comments. Result: 0 matches.
- Script: `sweep.py` (resumable; skips indices already cached).

## Known artifact (grader must handle)
CirrusSearch strips punctuation (`$`, `{`, `}`, `*`, `/`, `.`) from insource: queries — e.g. term `${7*7}` matches any "7 7" token pair (38,336 estimated totalhits). Punctuation-heavy terms produce token-collision noise; the grading pass verifies literal-term presence in page content before calling anything a hit.

## Status
- [ ] sweep complete (1,148/1,148 cached)
- [ ] per-hit grading done
- [ ] FINDINGS.md written
