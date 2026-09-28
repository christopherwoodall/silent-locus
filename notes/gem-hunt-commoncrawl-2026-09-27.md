# Hunt Lane 12 — Common Crawl (2026-09-27)

**Question:** Did Common Crawl capture any yanked campaign gem pages
(`rubygems.org/gems/<name>`) or their rubydoc.info counterparts before/during removal?

**Method:** Read-only exact-URL queries against the Common Crawl index API
(`https://index.commoncrawl.org/`). 185 campaign gem names extracted from
`data/gem-iocs-2026-09-27.jsonl` (`source_link` → `/gems/<name>`). Target crawls:
- `CC-MAIN-2026-21` (2026-05-08 → 2026-05-21) — covers the May 11–12 burst
- `CC-MAIN-2026-25` (2026-06-05 → 2026-06-18) — covers the June 18 wave
- `CC-MAIN-2026-30` (2026-07-10 → 2026-07-23) — post-yank notices, if any

**API health / control:** `rubygems.org/gems/rake` returns a real capture in
CC-MAIN-2026-21 (timestamp 20260515201758, status 200, WARC
`crawl-data/CC-MAIN-2026-21/segments/1778213378177.22/warc/CC-MAIN-20260515190610-20260515220610-00654.warc.gz`),
confirming the index path works and gem pages are crawled — clean negatives are
real absences, not API blindness.

## Confirmed findings (from healthy-API window)

- `rubygems.org/gems/tryf3zz` — **no captures** in CC-MAIN-2026-21 (clean
  `{"message": "No Captures found ..."}` JSON response).
- `rubygems.org/gems/southwarkssrfhack` — **no captures** in CC-MAIN-2026-21
  (clean JSON response).
- `rubydoc.info/gems/tryf3zz`, `rubydoc.info/gems/southwarkssrfhack`,
  `rubydoc.info/gems/londonyardtestabc` — **no captures** in CC-MAIN-2026-21
  (one transient timeout re-queried clean).

## Full 185-name sweep — status: RUNNING (backend degraded)

A resilient background sweep (`hidden_files/lane12/sweep3.py`, results →
`hidden_files/lane12/results.jsonl`, resumable state → `hidden_files/lane12/state.json`)
is querying all 185 names × 3 crawls with per-query retries and 10-minute
cooldowns on backend outages, deadline ~02:35 UTC.

**Caveat:** the Common Crawl CDX backend became broadly unhealthy mid-lane
(persistent 504s / empty responses on the control query that previously worked;
`collinfo.json` still serves fine, so this is the query backend, not the
front-end). A VM restart also wiped the first sweep's `/tmp` state — all lane
state now lives durably under `hidden_files/lane12/`. As of 00:59 UTC: 0 hits,
fewer than 40 of 555 queries completed; the sweeper is in cooldown/retry loops.

## Pattern-hunt expansion (Christopher's directive: hunt by PATTERN, not exact phrase)

**CDX server-side pattern filtering is infeasible on this backend:** `matchType=prefix`
queries (even narrow ones like `rubygems.org/gems/zzjinavcs`) consistently 504 —
the backend cannot do range scans right now; empty key ranges return fast, any
range containing data times out. `filter=urlkey:<regex>` needs a scannable range,
so it fails the same way. Exact-URL queries are the only working query shape.

**Client-side grammar enumeration instead** (379 new candidates, exact-queried on
CC-MAIN-2026-21):
- `try[a-z][0-9]zz` full 26×10 grid (16 known in corpus → 244 new)
- Numbered series with generous ranges: `zzpdfvar0-24`, `zzfadgivar0-24`,
  `zztxtwtmp0-24`, `wandshack0-15`, `lambQ4330-4360`, `lambprobe4330-4360`, `rfetch0-10`
- Deduplicated against the 185 known names (covered by the exact sweep)

**Laundering-URL hunt:** 139 `r.jina.ai`/`s.jina.ai` IOC URLs extracted from the
IOC file; `example.com` decoys excluded; the rest exact-queried on CC-MAIN-2026-21.

**Content-pattern plan:** CDX has no content index, so mechanism patterns
(go-import tags, r.jina.ai wrapping, `/api/v1/web_hooks`, A000/ZZEND markers)
are grepped from fetched WARC record bytes (HTTP Range request, single record
only — no full WARC downloads). Fetcher: `hidden_files/lane12/fetch_warc.py`.
Applies to any captures the sweeps surface.

**Status:** pattern sweep running in background (`hidden_files/lane12/pattern_sweep.py`
→ `pattern_results.jsonl`); 0 hits as of 01:24 UTC. The exact-URL sweep
(`sweep3.py` → `results.jsonl`, resumable via `state.json`) is also still running.

**Backend health note:** the CC index backend is intermittently dropping
connections (empty responses in ~1s, or 504s) after ~2h of sustained querying —
consistent with rate limiting. Both sweeps self-throttle with 10-minute cooldowns
after consecutive failures; no manual queries are being issued to let limits reset.

## Interim conclusion

The headline campaign pages (tryf3zz, southwarkssrfhack) were **not crawled**
by Common Crawl in the May window despite the control proving gem pages are
crawlable — consistent with the gems' <24h lifespan (published May 11–12,
yanked within hours; the May crawl's next pass simply never saw them live).
No pre-yank page content is recoverable from Common Crawl for the tested names.
If the background sweep completes with hits, this note will be updated.
