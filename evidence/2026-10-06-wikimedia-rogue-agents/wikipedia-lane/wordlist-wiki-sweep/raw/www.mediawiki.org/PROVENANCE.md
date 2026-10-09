# PROVENANCE — wordlist-wiki-sweep worker for www.mediawiki.org
**Worker: wikipedia-lane/wordlist-wiki-sweep, www.mediawiki.org lane.**
**Run: 2026-10-07 ~00:42 UTC (collection), analysis same night.**
**Grade: OBSERVED (API bytes) / INFERENCE (verdicts).**

## Source data
- `../search-terms.json`: 1,148 search terms (array under `"terms"`, fields
  `term` + `category` + `provenance` + `note`). Categories:
  launcher_toolkit 717, relays 242, dead_drops 115, targets 59, evals 15.
- BigSexyWarlock69's shared IOC wordlist subset (Wikipedia-plausible terms);
  terms like `${7*7}`, `/home/oai/share/heartbeat_r5.sh`,
  `<meta name="go-import"` (the one term containing double quotes — escaped
  as `\"` inside the insource phrase query).

## Collection method
- `collect-mediawiki.py` (in this sweep's root): for term n of 1,148,
  `GET https://www.mediawiki.org/w/api.php?action=query&list=search`
  `&srsearch=insource:"<term>"&srlimit=50&srnamespace=*&format=json&formatversion=2`,
  URL-encoded, UA `silent-locus-wiki-sweep/1.0 (research)`, paced **>=5.2s**
  between request starts (5s minimum per task + margin).
- **Every** response cached (hits AND zeros) as
  `raw/www.mediawiki.org/insource-<n>.json` (n = index in search-terms.json).
- Run log: `raw/www.mediawiki.org/run-log.jsonl` — one record per term:
  n, term, category, timestamp_utc, http_status, hit_count. Raw curl stdout
  from the collector: `raw/www.mediawiki.org/collect-stdout.log`.
- Resume-safe: terms with an existing `insource-<n>.json` are skipped on
  rerun.
- Sandbox revision comment grep: `prop=revisions&titles=Project:Sandbox`
  `&rvlimit=200&rvprop=ids|timestamp|user|comment&formatversion=2`,
  cached as `raw/www.mediawiki.org/sandbox-comments.json` (+ `-SUMMARY.json`).
  All 1,148 terms case-insensitive substring-matched against the 200 edit
  comments. Temp-account (~2026-*) sandbox revisions also fetched for
  context (`raw/www.mediawiki.org/sandbox-tempaccount-revs.json`).

## Caveat (carried from vocab-sweep / ngram-sweep)
`insource:` searches **current page content only** — cleaned sandboxes no
longer contain markers; revision history does. The sandbox comment grep
(200 revs) covers the gap only partially; full comment-history coverage
needs paginated rv traversal.

## Collection stats
- Terms queried: 1,148 / 1,148
- HTTP 200 responses: (see SUMMARY.json)
- Terms with >=1 hit: (see SUMMARY.json)
- Raw hit records returned: (see SUMMARY.json)
- Sandbox comment-grep matches (200 revs, 2026-08-19→2026-10-06): 0
