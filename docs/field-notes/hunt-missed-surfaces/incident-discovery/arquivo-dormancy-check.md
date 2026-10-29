# Arquivo.pt dormancy check — 2026-10-03/04

**Question:** Is the June machinery REALLY dormant, or did it just move out of the feeds we watched (urlscan/GreyNoise/urlquery)? Arquivo.pt was the one venue where agent traffic was PROVEN (DoE fuzz run, county.json burst) — and the dormancy claim never covered it.

**Verdict: UNDETERMINED — the venue degraded, not dormancy confirmed.** Arquivo.pt's search APIs stopped serving the on-demand-save collections where 100% of proven agent traffic lived, sometime between 2026-10-01 and 2026-10-03. The dormancy question cannot currently be answered in this venue. This is itself the highest-value finding: our strongest trace venue went dark two days after we swept it.

## What broke (evidence)

1. **Exact replay of a working Oct-1 query now returns empty.** `url=kansasmemory.gov&matchType=domain&from=20260430&to=20260514` → 36,577 records on Oct 1 → **0 records** on Oct 3 (HTTP 200, empty body). Same params, same endpoint.
2. **Count collapse across hosts** (matchType=prefix, no date bounds, Oct 3):
   - kansasmemory.gov: 36,577 (Oct 1) → **18** (Oct 3)
   - portal.max.gov → **17** total records
3. **Date filtering below year granularity is broken.** `from`/`to` at 14-, 8-, or 6-digit precision returns 0 records for every host tested; year-only (`from=2026&to=2026`) works. The wiki docs claim ≤14-digit timestamps are padded — the padding logic is dead.
4. **`matchType=domain` vanished from the docs.** Wiki now documents only exact/prefix/host.
5. **`filter=` appears unsupported.** `filter=original:.*zz=oai.*` returns 0 even on the June-17 DoE positive control (14,941 known captures).
6. **API routing is mid-migration.** `textsearch` now 400s with: "Please use the following Arquivo.pt APIs to search for URLs: CDX server API: https://arquivo.pt/cdxserverapi / Memento API: https://arquivo.pt/memento". But `/cdxserverapi` 302-redirects to a GitHub wiki page, and the memento timemap serves **0 2026 captures** for civilrightsdata.ed.gov.
7. **Only FAW (broad-crawl) collections are served.** Returned records carry `WEB-*.arquivo.pt.warc.gz` / collection `FAW` filenames. The `save-merged-*` files holding all June 2026 agent traffic are absent from every served result.

## Sweep results (2026-09-01 → 2026-10-03 window, grammar: zz=oai|zzbulk|prepnonce|openai_research|fresh=x|x=0.\d{6,}|cb=0.\d{6,})

| host | total served | Sep/Oct 2026 | grammar hits | newest served |
|---|---|---|---|---|
| civilrightsdata.ed.gov | 4,178 | 0 | 0 | 2025-09-03 |
| www.sec.gov | 205,609 | 0 | 0 | 2026-02 |
| apps.bea.gov | 11,144 | 0 | 0 | 2025-12-24 |
| bac-lac.gc.ca | 14,593 | 0 | 0 | 2026-01-31 |
| wonder.cdc.gov | 7,906 | 0 | 0 | 2025-12-20 |
| viz.aihw.gov.au | 1,325 | 0 | 0 | — |
| aihw.gov.au | 54,230 | 0 | 0 | 2025-12-21 |
| kansasmemory.gov | 18 | 0 | 0 | — |
| cal-access.sos.ca.gov | 1,312 | 0 | 0 | — |
| portal.max.gov | 17 | 0 | 0 | — |
| environment.nsw.gov.au | 29,228 | 0 | 0 | — |

All "0" values above are venue artifacts: the index currently serves nothing newer than ~Jan/Feb 2026 for any host, so Sep/Oct 2026 could not be tested at all. **The zeros prove nothing about the machinery.**

## Interpretation

- The dormancy claim (from urlscan/GreyNoise/urlquery, last 30 days) still stands **for those feeds** — but it was never tested in arquivo.pt, and now it can't be.
- Two hypotheses for the outage: (a) arquivo.pt is mid-migration and the save-collections will return to the index; (b) on-demand-save data was deliberately or accidentally dropped from the served index. Indistinguishable from outside.
- If (b), the June 2026 agent-traffic record at arquivo.pt — the evidentiary backbone of Transluce's reports and our corpus — is currently unverifiable by anyone. Our Oct-1 local pull (589,972 captures, in-repo) may now be the only accessible copy.
- The Oct-1 raw pulls under `data/2026-10-01-arquivo-pt/raw/` just became significantly more valuable. Do not discard.

## Method notes (for future sweeps)

- Working form right now: `https://arquivo.pt/wayback/cdx?url=<host>&matchType=prefix&limit=<n>` with NO from/to; filter timestamps client-side. Date-bounded queries silently return empty — a trap for anyone trusting zeros.
- `matchType=domain` + date bounds (the Oct-1 recipe) is dead.
- Polite pacing held throughout: ≥2s between requests, no 429s hit (rate headers show 250/60s per IP; we stayed far under).

## Recommended follow-ups

1. Re-probe the CDX endpoint weekly — if the save-collections return, re-run this check immediately; Sep/Oct 2026 grammar data may appear retroactively.
2. Treat `data/2026-10-01-arquivo-pt/raw/` as the canonical arquivo.pt evidence copy until further notice.
3. Check whether arquivo.pt announced the migration (status page / blog) — would distinguish (a) from (b).

*Read-only sweep, 2026-10-03/04. No commits made.*
