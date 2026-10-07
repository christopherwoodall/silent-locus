# HTMX-fix inventory: scripts querying the urlquery htmx search endpoint

Read-only reconnaissance, 2026-10-06. No network calls were made.
Search scope: `~/workspace/silent-locus/` and `~/workspace/muse-home/projects/`
(grep `api/htmx/search`, `urlquery.net` + `q=`/`limit=`, `monitor_loop` variants, `uq_htmx*` copies).

Reference GOOD pattern (outside scope, not counted):
`~/workspace/skills/urlquery/bin/uq_htmx.py` and `uq_htmx_curl.py`
— send `HX-Request: true` + `HX-Current-URL: https://urlquery.net/search?q=...`.
The bug: scripts hitting `/api/htmx/search/` WITHOUT those headers get `204 No Content`
and misread it as "zero results".

No byte-identical copies of the skill scripts exist anywhere in scope
(all checked via diff against both `uq_htmx.py` and `uq_htmx_curl.py`).
Every script below is a hand-rolled variant.

| # | path | endpoint pattern | HX headers? | verdict |
|---|------|------------------|-------------|---------|
| 1 | `data/2026-09-28-chinese-amap-fleet/personas/cartographer/sweep-curl.py` | `GET https://urlquery.net/api/htmx/search/?q=<q>&limit=<n>&offset=<o>` (urllib urlencode, curl transport) | YES — `HX-Request: true`, `HX-Current-URL: https://urlquery.net/search?q=...` | GOOD |
| 2 | `data/2026-09-28-chinese-amap-fleet/personas/metronome/raw/egress_watcher.py` | `GET https://urlquery.net/api/htmx/search/?q=url.domain%3Awebhook.site&limit=1&offset=0` (fixed liveness probe URL) | YES — `HX-Request: true`, `HX-Current-URL: https://urlquery.net/search?q=url.domain%3Awebhook.site` | GOOD |
| 3 | `data/2026-09-28-chinese-amap-fleet/personas/grammarian/raw/nonce_liveprobe.py` | `GET https://urlquery.net/api/htmx/search/?q=<q>&limit=<n>&offset=0` (urllib; same file also queries urlscan.io — out of scope) | YES — `HX-Request: true`, `HX-Current-URL: https://urlquery.net/search?q=<q>` | GOOD |
| 4 | `data/2026-09-28-chinese-amap-fleet/personas/evaluator/raw/hx_batch.py` | `GET https://urlquery.net/api/htmx/search/?q=<q>&limit=<n>&offset=<o>` (urllib urlencode, curl transport) | YES — `HX-Request: true`, `HX-Current-URL: https://urlquery.net/search?q=...` | GOOD |
| 5 | `data/2026-09-28-chinese-amap-fleet/personas/border-crosser/raw/gov_sweep.py` | `GET https://urlquery.net/api/htmx/search/?q=<q>&limit=<n>&offset=<o>` (urllib urlencode, curl transport) | YES — `HX-Request: true`, `HX-Current-URL: https://urlquery.net/search?q=...` | GOOD |
| 6 | `data/2026-10-06-wikimedia-rogue-agents/lifeval-cross-corpus/workers/urlquery-live/run_htmx_sweep.sh` | `GET https://urlquery.net/api/htmx/search/?type=reports&view=list&limit=24&offset=0&q=<urlencoded>` (bash curl loop, 11 queries) | YES — `HX-Request: true`, `HX-Current-URL: https://urlquery.net/search`, plus extra `HX-Trigger: search_query`, `HX-Target: search_results`, `Referer` | GOOD |
| 7 | `muse-home/projects/urlquery-api-hunt/artifacts/external/transluce-2026-09-23/workstream5a/hunt5a.py` | `GET https://urlquery.net/api/htmx/search/?limit=50&offset=<o>&q=<urlencoded>` (urllib) | YES — `HX-Request: true`, `HX-Current-URL: https://urlquery.net/search?q=<q>` | GOOD |
| 8 | `scripts/archive/collectors/urlquery/reverse_tunnels_htmx_search.py` | `GET https://urlquery.net/api/htmx/search/?q=<urlencoded>&limit=50&offset=0` (urllib) | NO — only `User-Agent: swarmtraces-hunt/lane-c`; no `HX-Request`, no `HX-Current-URL` | BROKEN |
| 9 | `muse-home/projects/swarmtraces-hf-corpus/data/reverse-tunnels/htmx_search.py` | `GET https://urlquery.net/api/htmx/search/?q=<urlencoded>&limit=50&offset=0` (urllib) — same code as #8, older path | NO — only `User-Agent: swarmtraces-hunt/lane-c` | BROKEN |
| 10 | `scripts/archive/collectors/dse-wiki/dse_wiki_verification_expand_search.py` | `GET https://urlquery.net/api/htmx/search/?q=<urlencoded>&limit=50&offset=0` (urllib) | PARTIAL — `HX-Request: true` + `Referer: https://urlquery.net/search`, but NO `HX-Current-URL` | UNKNOWN |
| 11 | `muse-home/projects/swarmtraces-hf-corpus/data/dse-wiki-verification-2026-09-27/expand_search.py` | `GET https://urlquery.net/api/htmx/search/?q=<urlencoded>&limit=50&offset=0` (urllib) — same code as #10, older path | PARTIAL — same as #10 | UNKNOWN |

Notes:
- `monitor_loop.sh` (`data/2026-09-28-chinese-amap-fleet/live-monitor/`) does NOT query the endpoint itself; it shells out to the reference GOOD script `~/workspace/skills/urlquery/bin/uq_htmx.py` — no fix needed.
- #8/#9 are the same script duplicated across repo generations (silent-locus archive + old muse-home corpus); #10/#11 likewise.
- Impact: the reverse-tunnels LANE C results (`htmx_summary.json`, `htmx_*.html`) were collected by #8/#9 WITHOUT HX headers — any "zero results" rows in that lane may be 204 artifacts, not real negatives. The dse-wiki expansion lane (#10/#11) is suspect to a lesser degree (HX-Request present, HX-Current-URL missing); unverifiable from static analysis alone.

Verdict rule applied: GOOD = sends both `HX-Request: true` and `HX-Current-URL`; BROKEN = sends neither; UNKNOWN = partial set or otherwise unverifiable statically.

**Totals: GOOD 7 · BROKEN 2 · UNKNOWN 2 (11 scripts total)**
