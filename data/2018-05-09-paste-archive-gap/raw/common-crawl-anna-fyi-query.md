# Common Crawl URL-index coverage for anna.fyi/* — queued for the lane12 supervisor

**Status: QUEUED, do NOT run while the CC backend is down.**
Verified down 2026-09-28 19:10 UTC (`hidden_files/lane12/supervisor.log`:
"CC index still down"; last check 19:10:45Z). The lane12 supervisor polls
`https://index.commoncrawl.org/CC-MAIN-2026-21-index?url=commoncrawl.org&output=json&limit=1`
every 10 min through 2026-09-30 12:00 UTC and will pick this up on recovery.

## Exact query (CDX-style, index.commoncrawl.org)

Per crawl `C` (see crawl selection below), two prefix queries — read-only:

1. **Paste-page discovery (the ID-yielding query):**
   `https://index.commoncrawl.org/{C}-index?url=anna.fyi/view/*&output=json&matchType=prefix&fl=url,timestamp,status,mime,digest,length&filter=status:200&filter=mime:text/html&collapse=urlkey`
   — paste IDs are the URL path segment (`anna.fyi/view/<8hex>`). One row per
   paste per crawl after `collapse=urlkey`; `timestamp` gives capture order.

2. **API census snapshot (point-in-time recents):**
   `https://index.commoncrawl.org/{C}-index?url=anna.fyi/api/recent&output=json&fl=url,timestamp,status,mime,digest,length,offset,filename&filter=status:200`
   — any captured `api/recent` body can be range-fetched from
   `data.commoncrawl.org/<filename>` at `offset/length` for its 15-pid list.

Where `{C}` is e.g. `CC-MAIN-2026-34` (index name = `<crawl>-index`).

## Crawl selection (via collinfo.json, read-only)

Fetch `https://index.commoncrawl.org/collinfo.json` (works even when the
per-crawl index is degraded — the supervisor already uses it). Keep crawls
whose `from`/`to` windows intersect **2026-03-01 .. 2026-09-28** (the anna.fyi
paste corpus window: earliest new ID `f8905d76` created 2026-03-12, latest
search-index crawls ~2026-09-28). Per the `shortener_cc_sweep.py` precedent,
expect on the order of ~6–10 qualifying crawls in the CC-MAIN-2026-* series.

## What to do with results

- Extract `anna.fyi/view/<pid>` IDs from query 1; dedupe against
  `data/paste-archive/anna.fyi/titles.jsonl` (our 55) and the Lane-1
  `data/paste-archive-gap/manifest.json` (106 as of 2026-09-28) before any
  fetch — ID harvesting first, body fetch only for genuinely new IDs.
- Range-fetch WARC records for new IDs via `fetch_range` on
  `https://data.commoncrawl.org/<filename>` with the returned
  `offset`/`length` (same helper as `hidden_files/lane12/fetch_warc.py`).
- Stage per-ID records under `data/paste-archive-gap/commoncrawl/` (one doc
  per observable — explicit-events rule), then commit + push.
- **DISK ONLY**: hosted-Elastic writes are frozen; no ingest, no index
  creates.

## Why this matters

Lane 1 (2026-09-28) recovered 51 new anna.fyi IDs from a third-party GitHub
corpus + search-engine index. Common Crawl is the only remaining passive
surface that could hold IDs published in neither source (crawled view pages
and `api/recent` snapshots). Wayback CDX covers the same ground when it
recovers; see `wayback-anna-fyi-coverage.md` for the complementary query set —
the two are complements, not competitors.

## Scope guard

This note is a queue document only. It launches no loop, touches no running
worker, and competes with no lane12 sweep (all lane12 sweeps target gems,
patterns, or shortener stats — none query `anna.fyi/*`). It is safe for the
supervisor to hand this to a fresh one-shot worker on backend recovery.
