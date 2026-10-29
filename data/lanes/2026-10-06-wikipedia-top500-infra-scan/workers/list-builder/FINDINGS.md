# List-builder FINDINGS — Wikipedia top-500 infra scan (2026-10-06)

## Steps taken
1. Read `silent-locus/docs/methodology.md` (curl for HTTP per VM constraint).
2. Queried the Wikimedia pageviews "top articles" endpoint for the most
   recent full month (September 2026; run date 2026-10-06).
3. Cached the FULL raw JSON to `raw/pageviews-top-2026-09.json`.
4. Extracted the top 500 entries in API order into `raw/top500-articles.tsv`
   (columns: `rank`, `article_title`, `views`, `note`).
5. Spot-verified 3 titles via the MediaWiki API
   (`https://en.wikipedia.org/w/api.php?action=query&titles=...&format=json`):
   all resolve in main namespace (ns 0).

## API endpoint (exact, working)
`https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/2026/09/all-days`
- Retrieval: 2026-10-06T20:42:32Z via curl (UA: `silent-locus-list-builder/research`).
- sha256 of cached JSON: `3389c6169c11c3bb1cccbc035650b35a2534938c8c71dbf5e28d69240d3112b8`
- Cached at: `raw/pageviews-top-2026-09.json` (1000 entries, ranks 1–1000;
  one `items[0]` block with `year=2026, month=09, day=all-days`).

## Endpoint notes / anomalies
- The URL given in the brief (`.../2026/09` with no day segment, and with
  `en.wikipedia.org` instead of `en.wikipedia`) returns a 404
  `{"detail":"invalid route"}` on BOTH `wikimedia.org/api/rest_v1` and
  `api.wikimedia.org`. Two fixes were required:
  1. project segment must be `en.wikipedia` (not `en.wikipedia.org`);
  2. a day segment is REQUIRED — `all-days` returns the whole-month ranking.
  Corrected form: `/metrics/pageviews/top/{project}/{access}/{year}/{month}/all-days`.
- Response returned **1000** entries (ranks 1–1000), not exactly 500 — more
  than enough; we took the first 500 in API order. No truncation of the
  cached raw file.
- **Rank tie in the API data itself:** `Barry_Melrose` and
  `List_of_countries_by_GDP_(nominal)` both report rank 433 with 339,999
  views; rank 434 is skipped (sequence runs 432, 433, 433, 435). The TSV
  keeps the API's ranks verbatim — it contains 500 rows with 499 distinct
  rank values. This is an upstream quirk, not a collection error.
- API titles are URL-encoded with underscores; normalization choice:
  percent-decode, then replace `_` with spaces (matches MediaWiki canonical
  title display). Colon-containing titles kept verbatim (e.g.
  `Avengers: Endgame` is a real main-namespace article, verified ns 0).

## TSV
`raw/top500-articles.tsv` — 500 data rows + header, API ordering preserved.
Columns: `rank`, `article_title`, `views`, `note`.

- Non-article entries are flagged in `note` (never dropped silently): 11 of
  the 500 (489 main-namespace articles). Flagged (rank, title):
  2 Special:Search · 3 Wikipedia:Featured pictures · 7 Special:RecentChanges ·
  34 Portal:Current events · 70 File:Traffic Sign GR - KOK 2009 - R-54.svg ·
  80 File:WhatsApp.svg · 201 Help:IPA/English ·
  202 File:Traffic Sign GR - KOK 2009 - Π-26α.svg · 289 File:WNBA logo.svg ·
  301 Wikipedia:Contact us · 322 Wikipedia:About.
- Flagging rule: title prefix before the first `:` is in the known-namespace
  set (Special, Wikipedia, Portal, File, Help, Category, Template, Talk,
  User, User_talk, Draft, MediaWiki, Module, Book, Wikipedia_talk, Project,
  TimedText, Gadget). Legit main-namespace titles containing colons
  (e.g. `Avengers: Endgame`, `Fall 2: Deadpoint`, `The Vvaan: Force of the Forrest`)
  are NOT flagged.
- Edge cases kept as returned: `.xxx` and `.xyz` (rank 290-ish region) are
  literal top-level-domain articles; `Main Page` (rank 1, 204,438,595 views)
  is kept with rank 1 and no flag (it is a real page, but revision pullers
  may want to exclude it — listed here explicitly).

## Spot-verification (MediaWiki API, all ns 0, no `missing`)
- `Lizzie Borden` (rank 4) → resolves, ns 0
- `Avengers: Endgame` (rank 116) → resolves, ns 0
- `Anthropic` (rank 118) → resolves, ns 0

## Grading
- OBSERVED: 1000 ranked entries from the official pageviews API for
  September 2026, all-access, en.wikipedia.
- Note for downstream workers: pageview ranking is all-access/all-agents
  (includes bots per the legacy API contract); the scan's edit-attribution
  logic is unaffected since it only needs the article list.

## Open question
Whether downstream workers want the raw 500 (as listed) or only the 489
main-namespace articles — recommendation: exclude the 11 flagged
non-articles (Special/File/Help/Wikipedia/Portal pages have no revision
history to scan the same way).
