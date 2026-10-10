# PROVENANCE — wordlist-wiki-sweep, incubator.wikimedia.org worker

## What was done
- **Source terms:** `search-terms.json` (1,148 terms, Wikipedia-plausible subset
  of the 3,822-term shared IOC wordlist; built_utc in that file; 2,674 dropped
  terms recorded in `dropped-terms.json`).
- **insource: sweep:** for every term, `GET
  https://incubator.wikimedia.org/w/api.php?action=query&list=search&srsearch=insource:"<term>"&srlimit=50&srnamespace=*&format=json`
  via curl (Python subprocess, single-URL invocation), paced >=5.2s between
  request starts. Term URL-encoded per-request. Query string was
  `insource:"<term>"` as a literal exact-phrase search.
- **Every response cached** (hits AND zeros): `raw/incubator.wikimedia.org/insource-<n:04d>.json`
  (n = index into search-terms.json "terms"). Run log:
  `raw/incubator.wikimedia.org/RUNLOG.jsonl` (term, category, UTC timestamp,
  HTTP status, hit count).
- **Sandbox comment grep:** 200 most recent revisions of `Incubator:Sandbox`
  (pageid 2908) via `prop=revisions&rvlimit=200`, cached as
  `raw/incubator.wikimedia.org/sandbox-revisions-Incubator-Sandbox.json`;
  all 1,148 terms matched case-insensitively as substrings against the 200
  edit comments.
- **Revision fetch for literal hits:** distinct pages whose search snippet
  contains the literal term cached as
  `raw/incubator.wikimedia.org/revfetch-<pageid>.json`
  (current revision: ids, timestamp, user, comment, tags).
- **Analysis:** `workers/incubator.wikimedia.org/{sweep.py,analyze.py,revfetch.py}`.

## Run metadata
- Worker: wiki-search-worker (subagent), branch `wikipedia-edit-hunt-2026-10-06`.
- Run start (UTC): 2026-10-07T00:41:38Z (probe terms 0–2), full sweep 00:42Z.
- Run end (UTC): PENDING.
- Requests completed: PENDING / 1,148 (RUNLOG.jsonl is authoritative).

## Method caveats (carried from prior sweeps)
1. `insource:` searches **current page content only**. Sandboxes that were
   cleaned no longer contain the markers — revision history does.
2. The comment grep is a 200-revision spot check, not exhaustive history.
3. CirrusSearch mangles punctuation-only/glob terms: a query like
   `insource:"${7*7}"` degrades (observed: matches pages containing "7",
   38,309 totalhits). API hits are graded against the **literal term as a
   case-insensitive substring of the search snippet**; terms whose hits never
   contain the literal term are recorded as degenerate queries, not real hits.
4. `srlimit=50`: for terms with >50 totalhits only the first 50 results were
   cached; totalhits is recorded in RUNLOG.jsonl and SUMMARY.json.

## Nothing committed or pushed (per task instructions).
