# sec-county-watch — WATCH_SPEC

LANE 4. Watches for NEW urlquery scan activity laundering
`www.sec.gov/files/county.json` (and mutations) through CORS/proxy relays,
i.e. a resumption of the Jun-18 SEC crowdfunding/double-slash bypass cluster
and/or the workers.dev path-traversal probe documented 2026-09-28.

## Ground truth (what this watches for a repeat of)

1. **Jun-18 cluster** (`notes/transluce-us-canada-gov-2026-10-01.md`,
   claim #14): 97 urlquery reports for `www.sec.gov/files/county.json`
   via allorigins/corsfix (`cors-laundering` tag), 1 double-slash URL
   (`www.sec.gov//files//county.json`). Corroborated by Transluce's
   own urlquery dataset (their claim) + our corpus — triple-sourced.
2. **Sep-28 proxy notes** (`notes/cors-bwa-proxy-2026-09-28.md`):
   path-traversal mutations (`./`, `../`, trailing-dot host `www.sec.gov.`,
   `:443` suffix) against `sec.gov`/`investor.gov` `files/county.json`
   through `cors.hypnguyen.workers.dev` and the broader workers.dev
   proxy family (105+ docs).

## Query

- **API**: urlquery public API v1 `search/reports/` with keyword
  `county.json` (keyword matches against submitted URLs, so it catches
  direct hits, relay-wrapped hits, double-slash and traversal mutations —
  all contain the literal string).
- **Client-side filters** (API ignores date params):
  - `date >= watermark` (report `date` field, UTC)
  - submitted URL (reconstructed `schema://addr`) contains `county.json`
    (case-insensitive) — excludes page-content-only matches.
- **Indicator classification** per row in `indicators`:
  - `cors-laundering`: relay host in URL — allorigins, corsfix,
    `*.workers.dev`, r.jina.ai, cors.lol, corsproxy.io, api.allorigins.win
  - `double-slash`: `//` inside the path+query portion, excluding the
    relay's embedded target scheme (`://` is stripped first so wrapped
    URLs don't false-positive)
  - `path-traversal`: `../`, `/./`, `%2e%2e`, `%252e` in target
  - `host-mutation`: trailing-dot host (`sec.gov.`) or `:443` suffix,
    on the outer OR the relay-embedded inner target host
  - `sec-target`: `sec.gov` or `investor.gov` present anywhere
- **Relay-encoded blind spot** (known limitation): if a relay URL-encodes
  the target filename (e.g. `county%2Ejson`), the keyword won't match.
  Mitigation: future sweeps can add `county%` / `sec.gov` broadened
  queries; record any change of query string in state.json.

## Time window

- Watermark starts at `2026-09-28T00:00:00Z` (the night of the Sep-28
  proxy notes — everything before that is baseline).
- Scope: agents/infrastructure only. Read-only corpora; no invented rows.

## Dedupe rule

- **Dedupe key = urlquery `report_id`** (one scan = one row, forever).
- `sweep.py` keeps `seen_ids` in `state.json` AND rebuilds from
  `data/hits.jsonl` on every run, so even if state.json is lost the
  append is still duplicate-free. `items_collected` counts unique
  appended rows only.
- Idempotent: re-running with the same watermark re-pages the API
  (to CHECK for new hits — this also self-heals urlquery index lag)
  but appends zero rows.

## Watermark advancement

- Explicit and recorded only: change `watermark` in `state.json`
  manually (or via the sweep's `--watermark` if added later), commit
  the state.json change with a message stating the reason
  (e.g. "false-positive URL class excluded" — never to skip hits).
- Default: never advance; the filter is date >= watermark and seen_ids
  already prevents re-ingest.

## Recommended cadence: DAILY

- The baseline cluster landed 97 reports in ONE day (Jun 18); a repeat
  would be a same-day event. Daily keeps alert latency under 24h.
- Cost is trivial: ~10 pages x ~5s at 2s spacing (~1 min/run).
- Trigger: any hit with `cors-laundering` or `path-traversal` indicator
  since watermark -> page parent agent immediately (same tradecraft,
  same file, same target = same actor family).
- No cron is created by this lane (recommendation only).

## Outputs

- `data/hits.jsonl`: one JSON object per row —
  `{"url","report_id","first_seen","source","indicators","provenance"}`.
  Empty file = honest zero (sweep ran, nothing matched).
- `state.json`: lane state per the collections durability contract,
  plus `seen_ids`, `scanned_reports`, `last_sweep`.
- `sweep.py`: idempotent sweep script (this file's implementation).
