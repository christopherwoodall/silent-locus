# Provenance — lifeval-cross-corpus urlquery-live htmx sweep

**Worker:** urlquery-live (subagent sweep, 2026-10-06)
**Source:** urlquery.net keyless htmx search endpoint
**Endpoint:** `GET https://urlquery.net/api/htmx/search/?type=reports&view=list&limit=24&offset=0&q=<urlencoded>`
**Method:** curl, direct HTTPS, no auth, no API key, read-only search
**Pacing:** >=6s between requests (standing collection doctrine: >=5s)
**User-Agent:** `silent-locus/lifeval-sweep`
**Request headers:** `HX-Request: true`, `HX-Trigger: search_query`, `HX-Target: search_results`,
`HX-Current-URL: https://urlquery.net/search`, `Referer: https://urlquery.net/search`
(emulating the live site's own htmx search form at https://urlquery.net/search)

**Why these parameters:** the live search page (`/search`, fetched 2026-10-06) wires its
`#search_query` form to `hx-get="/api/htmx/search/"` with form fields
`type=reports` (default radio), `view=list`, `limit=24`, `offset=0`, `q=<text>`.
hx-get serializes the form into the query string; the sweep mirrors exactly that.

**Response format:** HTML fragments (htmx partials), NOT JSON. Saved byte-for-byte as
`htmx_<slug>.html`. Per-request metadata (HTTP status, bytes, sha256, retrieval time,
distinct report UUIDs extracted) in the sibling `htmx_<slug>.meta.json`.

**Caveats (standing):**
- Per `~/workspace/skills/urlquery/HTMX_ENDPOINTS.md`: htmx search does NOT surface
  known-live records (5 Indonesia `go.id` reports resolve live via curl but return zero
  from htmx search) — every htmx zero is a WEAK negative, not proof of absence.
- `q` matches against submitted-URL indexing; marker strings live in page *content*,
  so plain-keyword zeros are expected even if content were indexed.
- Grading legend: OBSERVED (bytes seen in a response) / INFERENCE (coordination
  reading from observed facts) / UPSTREAM (claim rests on another source, unverified
  here). Tokyo Gas "Lifeval" hits = NOISE (real-world name collision).

**Files:**
- `probe_*.html`, `control_*.html`, `search_page.html` — endpoint-discovery probes
- `htmx_qNN_*.html` — the 11 vocabulary queries
- `htmx_qNN_*.meta.json` — per-request metadata + sha256

---

# Provenance — lifeval-cross-corpus urlquery-cached sweep

**Worker:** urlquery-cached (respawn, run 2026-10-06)
**Method:** passive `rg -i` grep over cached corpora in `~/workspace/silent-locus/data/`
(6,757 searchable files; excluded `.git` dirs and `2026-10-06-wikimedia-rogue-agents/`).
No live fetching, no auth, no exploitation. Retrieval time: 2026-10-06T23:38:10Z
(bytes copied verbatim, one JSON record per file).

## sandbox-link-test-hit-1.json
- Source file: `~/workspace/silent-locus/data/2026-05-17-collusion-wiki/raw/revisions.jsonl` (line 10893)
- sha256: 782bc25cd11a398fb2c73fba2342cec038eb4ee0d5765bba78a531f462f1b50e
- NOTE: byte-identical record also present at line 10893 of
  `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1/agent-logs/prowiki/revisions.jsonl`
  (duplicate copy of the same collusion-wiki dataset; not a second event).

## sandbox-link-test-hit-2.json
- Source file: `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1/agent-logs/dse/revisions.jsonl` (line 5201)
- sha256: bd63b84aad55a97b4fb441ce24abaa9118d2c172dac60ae5c30d548498b5f6fa
- Distinct revision (`dse~WillkommenImWiki@13`, seq 13) from hit-1 (`dse~WillkommenImWiki@23`, seq 23).
