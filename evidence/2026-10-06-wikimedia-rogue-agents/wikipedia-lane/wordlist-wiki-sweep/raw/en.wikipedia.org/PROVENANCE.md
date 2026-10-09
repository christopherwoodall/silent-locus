# Provenance — en.wikipedia.org wordlist wiki sweep

**Worker:** wikipedia-lane/wordlist-wiki-sweep, en.wikipedia.org worker (subagent), 2026-10-06/07.
**Wiki / API host:** en.wikipedia.org (`https://en.wikipedia.org/w/api.php`).
**Terms:** 1,148, from `wordlist-wiki-sweep/search-terms.json`
(`built_utc 2026-10-07T00:45:00Z`, sourced from `~/workspace/silent-locus/ioc-wordlist/wordlist.json`
status=active; question_terms/sqli_payloads/xss_ssti/URL-encoded-payload exclusions applied upstream —
see `wordlist-wiki-sweep/dropped-terms.json`).
**Categories:** launcher_toolkit (717), relays (242), dead_drops (115), targets (59), evals (15).

## Retrieval method
- Per term: `action=query&list=search&srsearch=insource:"<term>"&srlimit=50&srnamespace=*&format=json`
  via Python `urllib` with UA `wordlist-wiki-sweep/1.0 (research; en.wikipedia.org IOC hunt; contact via repo)`.
- Term URL-encoded; literal `"` inside the single quoted term (`<meta name="go-import"`)
  backslash-escaped so the `insource:"..."` phrase stays intact.
- Paced >=5.2s between requests; up to 3 retries with 10s backoff on transport errors.
- EVERY response cached (hits AND zeros) as `raw/en.wikipedia.org/insource-<n>.json`
  (n = term index; `_sweep` envelope records n/term/category/fetched_utc/http_status).
- Run log: `raw/en.wikipedia.org/run-log.csv` (n, term, timestamp_utc, http_status, totalhits, error).
- Summary: `raw/en.wikipedia.org/SUMMARY.json`.
- Sweep script: `wordlist-wiki-sweep/sweep-en.py` (committed on branch, not pushed).

## Sandbox comment grep
- `action=query&prop=revisions&titles=Project:Sandbox&rvlimit=200`
  (`rvprop=ids|timestamp|user|comment|tags|flags`, no content) →
  `raw/en.wikipedia.org/sandbox-revisions.json` (200 revs,
  2026-10-05T00:22:25Z → 2026-10-07T00:39:50Z).
- Case-insensitive substring grep of all 1,148 terms against the 200 edit comments →
  `raw/en.wikipedia.org/sandbox-comment-matches.json`.
- This is a spot check only: on en.wikipedia the sandbox turns over ~100 revs/day,
  so 200 revs cover ~2 days, not the May–Jun 2026 incident window.

## Caveats
- `insource:` searches CURRENT page content only. Sandboxes that were cleaned
  (the incident's markers were) no longer contain the strings; only revision history
  does. The comment grep covers the gap partially (comments, not content).
- Search hit counts (`totalhits`) are CirrusSearch estimates, not exact counts.
- `srnamespace=*` sweeps all namespaces (articles, users, project, file, etc.).
- Incident oldids on en.wikipedia (known-incident set, from the incident CSV):
  1353490694, 1353490935, 1353491551, 1353492663, 1353498400, 1353501383,
  1353507315, 1353518652, 1353543060, 1356314507, 1356419247.

## Run outcome
- (filled after sweep completes)
