# Common Crawl coverage: goto.unm.edu `+` stats pages (July 5–6 UNM retry lane)

Queued 2026-09-28. Worker: `hidden_files/lane12/shortener_cc_sweep.py`
(launched by the lane12 supervisor on CC-backend recovery; prints
`DONE shortener-cc` on completion). Job spec: `shortener_cc_job.json`.

## Exact CC URL-index queries (one per crawl × one per URL)

The worker builds these at runtime; the canonical hand-query form is:

```
https://index.commoncrawl.org/<CRAWL>-index?url=goto.unm.edu%2F7t6-o%2B&output=json&matchType=exact&filter=status%3A200&filter=mime%3Atext%2Fhtml&collapse=digest
```

Notes:
- `%2B` is REQUIRED: a literal `+` in the query value decodes to a space,
  which would query `goto.unm.edu/7t6-o ` and return nothing.
- `matchType=exact` — the worker also queries the `http://` variants of
  each stats URL, since CC normalizes SURT keys per scheme.
- `collapse=digest` dedupes byte-identical captures across segments.
- Crawls are selected at runtime from
  `https://index.commoncrawl.org/collinfo.json` by intersecting each
  crawl's `from`/`to` window with `2026-06-01..2026-08-15` (job spec
  `window_from`/`window_to`). Expected candidates (July-2026 coverage):
  CC-MAIN-2026-26, 2026-28, 2026-29, 2026-30, 2026-31, 2026-32.
- Record → WARC byte fetch:
  `https://data.commoncrawl.org/<filename>` with
  `Range: bytes=<offset>-<offset+length-1>` (fields straight from the
  index JSON row), then gzip-decompress and split the WARC/HTTP
  envelopes to the payload.

## What the worker does with a capture

1. Saves the raw stats HTML to
   `data/university-shorteners/wayback-cc/<slug>/<crawl>_<ts>.html`.
2. Parses with the shared YOURLS referrer-table extractor from
   `hidden_files/shortener-cdx/pull_and_explode.py` (best-effort row
   parse; any July-5/6 daily rows or referrer rows present in the capture
   become per-row evidence).
3. Writes an evidence JSON in the
   `scripts/build_shortener_events.py` schema
   (`<slug>_referrer_urls_daily_cc_<crawl>_<ts>.json`).
4. Explodes to per-row `yourls_referrer_url` / `yourls_daily_hits`
   event docs, deduped on `labels.event_id` against the existing
   `data/university-shorteners-events/university-shorteners-events.jsonl`.
5. Disk only — no hosted-Elastic writes (standing pause). Manifest +
   SHA256SUMS maintained in `data/university-shorteners/wayback-cc/`.

## Why CC matters here

- The live UNM YOURLS UI has no per-day-per-referrer drill-down (verified
  2026-09-28; prior lane proved this too). A mid-July capture of the
  stats page renders the *then-current* referrer table and daily charts —
  the only remaining source for July 5–6 per-referrer rows if the
  swarm's July 5/6 hits were captured before later traffic washed them
  out of the all-time table.
- The Wayback CDX path is covered separately by the standing
  `hidden_files/shortener-cdx/` retry loop (all 4 UNM `+` URLs + vbudg
  are already in its 12-URL set — verified 2026-09-28, no additions
  needed). CC is an independent backend and an independent capture
  corpus.

## Memento aggregators — negative (2026-09-28)

- `timetravel.mementoweb.org` (http and https) and `arquivo.pt/wayback/cdx`
  return "Empty reply from server" through this network's egress — the
  same failure class as web.archive.org in the lane12 progress notes
  (DNS resolves, upstream sends nothing; effectively blocked). Documented
  as unavailable; no retry loop installed for them.

## UNM YOURLS alternate endpoints — negative (2026-09-28)

- Stats page is stock YOURLS 1.7.1, fully server-rendered; tabs
  (`stat_tab_stats/sources/location/share`) are DOM show/hide, no JS
  data API. Only client fetch is `admin/admin-ajax.php` (auth-only,
  out of scope — not probed beyond confirming its presence in infos.js).
- `yourls-api.php?action=stats&shorturl=7t6-o` (signature-less GET):
  302 → `https://goto.unm.edu`. No signature-less read path.
- No dated archive URL pattern on the instance. Verdict: no live
  historical endpoint; archived-page recovery (Wayback/CC) is the only
  viable path for July 5–6 rows.
