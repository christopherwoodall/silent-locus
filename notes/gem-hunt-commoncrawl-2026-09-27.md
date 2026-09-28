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

## Respawn (lane 12b) — 2026-09-28 ~01:15–03:45 UTC

The CC index query backend (`index.commoncrawl.org/...-index`) was **fully
down for the entire respawn window** (~2.5h): HTTPS requests hang with no
response, plain HTTP returns "Empty reply from server" (curl 52). The
`collinfo.json` endpoint answered normally throughout — query-backend outage,
not a network block. All three CC sweeps (`sweep3.py` exact names × 3 crawls,
`sweep4.py` rubydoc.info exact × 2 crawls, `pattern_sweep.py` grammar + jina
candidates) ran with retry/cooldown logic and durable state but completed
**zero queries**; they remain alive in the background and will make progress
if the backend recovers. New working files: `sweep4.py`, `collinfo-2026-09-27.json`.

### Wayback Machine alt-route (backend healthy)

With CC down, the lane pivoted to `web.archive.org/cdx` (exact-URL and
`matchType=prefix` queries — the prefix shape CC 504s on works fine on
Wayback, ~3s per family).

**Control:** `rubygems.org/gems/rake` archived 2026-01-30, 2026-03-14,
2026-04-15, 2026-05-15, 2026-05-18 (all 200) — Wayback archives gem pages in
the campaign era, so clean negatives are real absences.

**Hit — one campaign gem page archived:**
`https://rubygems.org/gems/zztargettest18587` (in JFrog's GemStuffer CSV)
captured once: **2026-08-10 00:49:52 UTC**
(CDX: https://web.archive.org/cdx/search/cdx?url=rubygems.org%2Fgems%2Fzztargettest18587&output=json —
page: https://web.archive.org/web/20260810004952id_/https://rubygems.org/gems/zztargettest18587).
The 37KB snapshot is the **post-yank notice page** ("Yanked by …", name
reserved) — no go-import meta tags, no jina URLs; the payload metadata was
wiped at yank. It proves the gem existed and was yanked, but no pre-yank
content is recoverable.

**Family-prefix sweeps** (`matchType=prefix`, `collapse=urlkey`,
`filter=statuscode:200`) — campaign-name cross-check against the 185 exact
names + 379 grammar candidates:
- `rubygems.org/gems/zz*`: 72 archived → 1 campaign hit (zztargettest18587 above)
- `rubygems.org/gems/try*` + regex `try[a-z][0-9]zz`: **0 archived**
- `rubygems.org/gems/oai*`: 126 archived → 0 campaign
- `rubygems.org/gems/wand*`: 25 → 0 campaign; `chat*`: 115 → 0; `lamb*`: 78 → 0
- `hgprobe*`, `southwark*`, `rfetch*`: 0 archived
- 10-digit-epoch filter on 2026+ gem URLs: 13 hits, all student-homework gems
  (`alu0101*` series) — **0 campaign**

**rubydoc.info:** `zz|try|oai|chat` prefixes → 1/3/1/12 archived (all
legitimate gems: zzzzzz, try_again, oai, chat-1, …) — **0 campaign gems**.
The `.yardopts` exfil loop left no rubydoc.info trace in the archive.

**jina laundering URLs:** spot-checked campaign `r.jina.ai/...moderngov...`
URLs on Wayback CDX — 0 captures (e.g.
`https://r.jina.ai/http://moderngov.lambeth.gov.uk/mgCalendarMonthView.aspx`).

Raw prefix results + the yanked-page snapshot saved durably under
`hidden_files/lane12/wayback_prefix/` (JSON per family + `SUMMARY.txt`).

**Exact-URL Wayback sweep** (`wb_sweep.py`: 185 gem names + 185 rubydoc URLs)
is running in the background with durable state (`state_wb.json`); Wayback
throttled mid-run (2s → 15–40s per query), pace reduced to 5s sleeps. Early
exact checks (tryf3zz, chatoaifetch177855288717, agentoaitestabc123) all `[]`.

## Final conclusion

Two independent historical indexes now agree: **the campaign's gem pages were
essentially never archived**. Common Crawl captured the headline May gems not
at all (control proved gem pages are crawlable); Wayback archived exactly one
campaign gem page — a post-yank notice from August, payload metadata already
wiped. The rubydoc.info surface is equally clean. This is consistent with the
<24h gem lifespan (published and yanked within hours on May 11–12): no
crawler's scheduled pass ever saw them live, and the one Wayback hit came
~3 months later against the yank stub. **No pre-yank gem-page content
(go-import tags, jina chains, descriptions) is recoverable from either
archive.** The Diffend snapshots and the live `.gem` reconstructions remain
the only pre-yank sources.

Caveat: the CC exact-name/grammar sweeps never got a healthy backend in this
lane; if `index.commoncrawl.org` recovers, the background sweeps
(`sweep3.py`, `sweep4.py`, `pattern_sweep.py` with durable state files) will
fill in the CC side. Re-check `hidden_files/lane12/results.jsonl`,
`rubydoc_results.jsonl`, `pattern_results.jsonl`.
