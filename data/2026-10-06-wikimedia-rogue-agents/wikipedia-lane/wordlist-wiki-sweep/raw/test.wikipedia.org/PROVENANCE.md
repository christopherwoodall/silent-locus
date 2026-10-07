# PROVENANCE — test.wikipedia.org wordlist insource sweep
**Worker:** wikipedia-lane/wordlist-wiki-sweep (test.wikipedia.org lane), 2026-10-06/07.
**Grade:** OBSERVED (API bytes) for all cached JSON; INFERENCE for verdicts in FINDINGS.md.

## Source terms
- `../search-terms.json`: 1,148 terms, built from BigSexyWarlock69's shared IOC wordlist
  (3,822 terms) filtered to the Wikipedia-plausible subset. Categories:
  launcher_toolkit (717), relays (242), dead_drops (115), targets (59), evals (15).
  Fields per term: `term`, `category`, `provenance` (ioc-wordlist/wordlist.json), `note`.
- Dropped (out of scope): `../dropped-terms.json` with per-term reasons.

## insource: sweep (1,148 requests)
- **Method:** for each term, `action=query&list=search&srsearch=insource:"<term>"`,
  `srlimit=50`, `srnamespace=*`, `format=json` against
  `https://test.wikipedia.org/w/api.php`, paced to keep >=6s between request
  starts (task floor: 5s). URL-encoded via `urllib.parse.quote`.
- **CRITICAL METHOD NOTE:** MediaWiki CirrusSearch `insource:"..."` is a
  *full-text phrase* search against the page-source index, NOT a regex
  (regex requires the `insource:/.../` form). This was verified mid-run:
  escaping every regex metacharacter in `${7*7}` (`\$\{7\*7\}`) still
  returned 36,620 hits — the tokenizer reduces it to tokens `7`,`7`,
  matching File: pages' EXIF dumps. Escaping changes nothing in full-text
  mode, so the sweep uses the plain quoted phrase exactly like the prior
  vocab/ngram sweeps (unescaped, URL-encoded). The one term containing a
  double quote (`<meta name="go-import"`) had the quote stripped to avoid
  breaking the quoted-phrase syntax. Terms that tokenize to junk
  (`${7*7}`, 2-char tokens like `cb`) produce token-noise hits and are
  graded as **noise** — an honest, documented artifact class, not a bug.
  3 early requests run before this was settled (n=0,1,2) were discarded
  and re-run in the final form.
- **Cache:** `insource-<n>.json` (raw API response, hits AND zeros),
  one file per term index `n` in `../search-terms.json` order.
- **Run log:** `run-log.jsonl` — one line per request:
  `n`, `term`, `category`, `ts_utc`, `http_status`, `totalhits`, `error`.
- **Script:** `../sweep_testwiki.py` (resumable via run-log; re-run skips
  already-logged indices).
- **Caveat (inherited from vocab/ngram sweeps):** insource: searches
  CURRENT page content only. Cleaned sandboxes erase content markers; the
  sandbox comment grep below covers part of the gap.

## Sandbox comment grep
- **Method:** `action=query&prop=revisions&titles=Project:Sandbox`
  (`rvprop=ids|timestamp|user|comment|tags`, `rvlimit=200`) on
  test.wikipedia.org at 2026-10-07T00:41Z. Resolves to Wikipedia:Sandbox.
  Span: 2025-11-01 → 2026-09-21 (200 revs, low-traffic test sandbox).
- **Cache:** `sandbox-revisions.json` (raw API response).
- **Grep:** case-insensitive substring match of all 1,148 terms against
  each revision's `comment`. Result: **0 matches** — cached in
  `sandbox-comment-matches.json` (empty array).
- **Caveat:** 200 revs is a spot check; a full comment-history sweep would
  need paginated rv traversal. Note the 200-rev window (Nov 2025 – Sep 2026)
  DOES cover the May–Jun 2026 incident window, unlike the en/commons
  200-rev spot checks in prior sweeps.

## Hit grading
- For each nonzero term: `prop=revisions` on the hit pageids for current
  revision (content, timestamp, user, comment, tags); grade per rubric:
  known-incident (oldid in the 54-set) / incident-shaped-new (~2026-* or
  disposable account, sandbox/test page, machine markers, NOT in the 54) /
  organic (docs, discussions, human pages) / noise (search-syntax artifact).
- Diff link form: `https://test.wikipedia.org/w/index.php?diff=<revid>`.
