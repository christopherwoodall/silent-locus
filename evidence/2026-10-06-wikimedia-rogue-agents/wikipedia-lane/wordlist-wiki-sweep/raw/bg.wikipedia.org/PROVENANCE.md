# PROVENANCE — wordlist-wiki-sweep / bg.wikipedia.org

**Worker:** wordlist-wiki-sweep, bg.wikipedia.org (worker session 2f38aa50-4461-4c82-a624-c02cc3d03627)
**Run date:** 2026-10-06 (started ~19:45 CDT / 2026-10-07 ~00:45 UTC)

## Search terms
- Source: `../search-terms.json` — the Wikipedia-plausible subset (1,148 terms)
  carved out of BigSexyWarlock69's shared IOC wordlist (3,821 terms:
  launcher/toolkit markers, relay hostnames, dead-drop services, eval names).
- Terms file carries `built_utc`, `source`, `exclusion_note`, `drop_counts` at
  top level; each term has `term`, `category`, `provenance`, `note`.
- Category counts in this run: launcher_toolkit 717, relays 242,
  dead_drops 115, targets 59, evals 15.

## insource: content sweep
- Method: one MediaWiki API `list=search` request per term:
  `srsearch=insource:"<term>"`, `srlimit=50`, `srnamespace=*`,
  `format=json`. Full srsearch value URL-encoded via
  `urllib.parse.urlencode`.
- Endpoint: `https://bg.wikipedia.org/w/api.php` via curl (no auth,
  stock UA `silent-locus-wordlist-sweep/1.0 (academic research)`).
- Pacing: >=5.5 s between request starts; request duration counted toward
  the interval. One retry-with-backoff (3 attempts) on curl failure.
- Every response cached as `insource-<n>.json` where `<n>` is the 0-based
  index into `search-terms.json` terms array (resumable: skips n already
  present in the run log). **Hits AND zeros are cached** — the corpus is
  complete either way.
- Each cached file: `{term, category, ts_utc, http_status, totalhits, response}`.
- Run log: `run-log.jsonl`, one line per request:
  `{n, term, category, ts_utc, http_status, totalhits}`.
- SHA256 of the terms file at sweep start: `f7c6b0cf7aa216a4edcdb73226c3274132787a73187ad694d804f314033ce69c`.
- **Caveat (carried from vocab/ngram sweeps):** `insource:` searches
  CURRENT page content only. Cleaned sandboxes erase content markers;
  revision history retains them. The sandbox-comment grep (below) covers
  the gap partially.

## Sandbox comment grep
- Page: Уикипедия:Пясъчник (pageid 163605, the bg.wikipedia.org main sandbox).
- Method: `prop=revisions&titles=<sandbox>&rvlimit=200` with
  `rvprop=ids|timestamp|user|comment|tags`, single API request, cached as
  `sandbox-revisions-200.json`.
- All 1,148 terms matched case-insensitively as substrings against every
  revision comment. Matches cached as `sandbox-comments-matches.json`
  (empty array = honest zero).
- Revision window covered: 2025-10-30T10:47:36Z → 2026-10-03T17:51:19Z
  (spot check, not exhaustive; paginated rv traversal would be needed for
  full history).

## Retrieval integrity
- All retrieval done over HTTPS directly from bg.wikipedia.org's public API.
- Raw bytes cached before any analysis; nothing filtered at ingest.
