# MAPPING.md — urlscan.io + Common Crawl feeds (Lane 3)

**Date:** 2026-10-03 · **Branch:** `local` · **Lane dir:** `collections/urlscan-cc-feeds/`
**Outputs:** `openai-agent-traces/data/urlscan.jsonl`, `openai-agent-traces/data/commoncrawl.jsonl`

Lane 1 had not yet written `openai-agent-traces/SCHEMA.md` at the time of this
lane's work, so field names are based on the canonical
`schema/record.schema.json`. Both output files carry all required schema
fields with correct types; they also carry a top-level `title`, matching Lane
1's existing practice (`traces.jsonl` carries `_id`, `attribution`, `digest`,
`features`, `mime`, `notable_query_params`, `trace_id`, none of which are in
the canonical schema either) — strict `additionalProperties:false`
validation is not enforced by existing lane files. `title` is the only
deviation on this lane's records (verified by jsonschema run 2026-10-03).

## record_kind registry additions (this lane)

- `urlscan_scan` — one record per unique urlscan.io scan returned by the
  keyless search API (`/api/v1/search/`), deduped by scan (task) UUID.
  Identity string: `urlscan:` + task UUID.
- `commoncrawl_index_record` — one record per Common Crawl CDX index record
  returned by exact-URL queries against `CC-MAIN-2026-25`. No WARC bytes are
  staged; the record describes where the bytes live (`cc.warc_file`,
  `cc.offset`, `cc.length`). Identity string:
  `cc:` + crawl + `:` + urlkey + `:` + capture timestamp + `:` + digest.

Fingerprint = SHA-256 hex of the identity string (deterministic ⇒ same
identity always yields the same fingerprint ⇒ same ES doc ID, append-safe).

## Field mapping — urlscan_scan

| record field | source |
|---|---|
| `@timestamp` | scan `task.time` (scan execution time, UTC). Sentinel `1970-01-01T00:00:00Z` + `labels.timestamp_source=fallback:no_recoverable_date` if unparseable |
| `event.dataset` | `openai-agent-traces` (also the local-ES index name) |
| `record_kind` | `urlscan_scan` |
| `labels.query.string` | the search query that surfaced this scan |
| `labels.query.class` | one of `oai-fingerprint`, `dsqa-domain`, `filename` |
| `labels.scan.uuid` | task UUID (dedupe key) |
| `labels.scan.task_url` / `.page_url` / `.domain` / `.visibility` / `.source` / `.country` / `.ip` / `.server` / `.status` | verbatim from API result |
| `labels.attribution.provider` | `openai` ONLY when the scan's task URL, page URL, or filename carries a genuine `oai*` **tag** — defined as the regex `(?i)(?:zz=\|[^a-z0-9_])oai(?:\d\|[_-]?(?:research\|agent))` (the corroborated DoE `zz=oai<digits>` cache-buster form, `oai<digits>` labels, and `oai_research`/`oai-agent` forms). Plain substring "oai" hits (e.g. `occupyai`, `oai-pmh`, OpenAI-brand phishing infra) do NOT qualify. **2026-10-03 repair:** the initial run set provider on all substring matches; audit found zero genuine tag matches, so the repair (`repair_urlscan_attribution.py`) stripped provider attribution from all 315 oai-class records — none currently carry it. Omitted otherwise. |
| `labels.attribution.eval_family` | not set on any urlscan record (no task-shape evidence at scan level) |
| `matched_string` | the URL/filename carrying the oai* fingerprint (present only with provider evidence) |
| `source_url` | `https://urlscan.io/result/<uuid>/` |
| `tags` | `urlscan`, `sweep-2026-10-03`, the query class, plus `oai-fingerprint` when provider evidence exists |
| `confidence` | `medium` (public scan metadata, no payload inspection) |
| `retrieved_via` | `urlscan-api-v1-search` |
| `file` | `collections/urlscan-cc-feeds/probe-log.jsonl` (source artifact pointer) |
| `note` | states whether attribution was set or explicitly withheld and why |

Honesty constraints observed by the urlscan sweep:
- Keyless search covers only the **last 30 days** of scans
  (`search_date_limit_days: 30` in every response). June-2026 incident-era
  scans are outside this window; results therefore cover recent scans only.
- Wildcard behaviour in `q` is API-defined; every query is logged with its hit
  count (zeros included) in `probe-log.jsonl` regardless of result.
- Pagination capped at 2 pages (200 results) per query; truncation is logged
  per query.

## Field mapping — commoncrawl_index_record

| record field | source |
|---|---|
| `@timestamp` | index record capture timestamp (`20260617201637` → ISO-8601 UTC) |
| `event.dataset` | `openai-agent-traces` |
| `record_kind` | `commoncrawl_index_record` |
| `labels.cc.crawl` | `CC-MAIN-2026-25` (2026-06-05 → 2026-06-18; covers the full DoE window) |
| `labels.cc.urlkey` / `.status` / `.mimetype` / `.digest` / `.warc_file` / `.offset` / `.length` / `.capture_timestamp` | verbatim from index API |
| `labels.source.slug` | incident slug whose arquivo-pt capture list supplied the URL |
| `labels.attribution.eval_family` | `deepsearchqa` ONLY for `doe-crdc` hits (DoE task shape = dsqa_250, verified by the deepsearchqa lane 2026-10-03). Omitted for all other slugs. |
| `labels.attribution.provider` | never set on CC records (no direct evidence) |
| `source_url` | the exact original URL queried |
| `tags` | `commoncrawl`, `CC-MAIN-2026-25`, `sweep-2026-10-03`, incident slug |
| `confidence` | `high` (byte-exact index record from CC's own API) |
| `retrieved_via` | `commoncrawl-index-api` |
| `file` | the read-only raw CDX path the URL was drawn from |
| `note` | index-record-only; no WARC downloaded; justification required before any WARC fetch |

Candidate-URL selection (deterministic, per slug):
1. Read the committed read-only CDX list `data/2026-10-01-arquivo-pt/raw/<slug>.cdx.jsonl.gz`.
2. Parse the original `url` field; dedupe preserving first-seen order.
3. Sort lexicographically; take the first 200 (cap). Slugs with fewer than 200
   distinct URLs are queried in full.
4. Zero-byte slugs (doj-ojjdp, sec, cdc-wonder, texas-dshs) contribute nothing.

Exact-URL queries only (wildcards 504 server-side per re-hunt-relays probing).
Every query is logged in `probe-log.jsonl` (zeros included: lines with
`{"message":"No Captures found..."}` count as zero-hit queries).

## Sweep results (2026-10-03)

### urlscan.io — 11 queries, 427 unique scan records staged
`openai-agent-traces/data/urlscan.jsonl` (427 records, 427 unique fingerprints,
0 duplicates; idempotent re-run verified — second run staged only 10 genuinely
new scans from the live 30-day window).

| query | total reported | fetched | new staged |
|---|---|---|---|
| `task.url:*zz=oai*` | — | 0 | 0 (blocked: HTTP 403, leading-wildcard forms rejected) |
| `page.url:zz=oai*` | 0 | 0 | 0 |
| `task.url:zz=oai*` | 0 | 0 | 0 |
| `page.url:oai*` | 177 | 100 | 100 |
| `task.url:oai*` | 172 | 100 | 15 (85 already seen) |
| `filename:oai*` | 10000 | 200 | 200 |
| `domain:civilrightsdata.ed.gov` | 0 | 0 | 0 |
| `domain:bea.gov` | 3 | 3 | 3 |
| `domain:recherche-collection-search.bac-lac.canada.ca` | 0 | 0 | 0 |
| `domain:bac-lac.gc.ca` | 0 | 0 | 0 |
| `domain:sec.gov` | 83 | 83 | 83 |
| `filename:county.json` | 16 | 16 | 16 |

**Attribution outcome:** zero records carry `attribution.provider` — audit of
all 315 oai-class matches found no genuine `oai*` tag (`zz=oai<digits>`) forms;
they are unrelated recent scans (OpenAI-brand phishing infra, `occupyai`,
`oai-pmh`, etc.). The initial over-attribution was repaired in place
(`repair_urlscan_attribution.py`); fingerprints unchanged. All hits are benign
recent scans (county-government sites, sec.gov EDGAR PDFs); no incident links.

### Common Crawl CC-MAIN-2026-25 — 1,586 candidate URLs, 17 index records staged
`openai-agent-traces/data/commoncrawl.jsonl` (17 records, 17 unique
fingerprints). 1,508/1,586 candidate URLs definitively answered (~95.1%
after 3 passes; the remaining 78 are persistent transient failures —
504/502/timeouts plus 404s without a readable "No Captures" body — left
retryable in `data/seen.json`, never marked queried). Full per-query log
(zeros included) in `probe-log.jsonl` (2,365 CC lines).

Hits (all index-record-only; no WARC downloads):
- **nysed-enrollment ×14:** `https://data.nysed.gov/` captured 2026-06-06 →
  2026-06-16 (status 200, real WARC segments) — CC's routine recrawls of the
  NYSED homepage overlapping the incident window, not agent traffic.
- **illinois-iquery ×2:** `https://iquery.illinois.gov/robots.txt`
  (2026-06-14, 2026-06-16, status 503, CC robotstxt segments) — CC's own
  robots.txt fetches.
- **kansas-kansasmemory ×1:** `https://www.kansasmemory.gov/item/211020`
  (2026-06-17, status 200, real WARC segment) — genuine CC capture of an
  incident-list URL during the crawl window.

No agent fuzz-traffic URLs (the `zz=oai`-tagged DoE SQLi ladders, LAC payload
URLs, etc.) appear in CC-MAIN-2026-25 — consistent with the sibling lane's
independent finding that the agent fuzz traffic exists only in Arquivo.pt
captures. `attribution.eval_family=deepsearchqa` set on doe-crdc hits only
(none occurred); `attribution.provider` never set on CC records.

### Engineering notes
- urlscan rejects leading-wildcard query forms with HTTP 403 (not a block of
  the endpoint — non-leading forms work).
- CC index API was flaky on 2026-10-03 (~30-40% transient 502/504/timeouts);
  the collector treats only HTTP 200 and 404-with-"No Captures" as definitive.
- Fixed mid-lane: `api_get` crashed on HTTPError responses whose bodies were
  unreadable (broken chunked encoding) — now returns `(code, "")` and the URL
  stays retryable. Checkpointing every 25 queries + per slug makes runs
  interruption-safe; a probe-log recovery step rebuilt the definitive set
  after an early killed run.

## State and idempotency

- `state.json` — watermarks, per-lane progress, counts, status.
- `data/seen.json` — `urlscan_uuids`, `cc_urls_queried`, `cc_index_pairs`.
- Re-runs skip everything already seen; output JSONL files are append-only.
- `probe-log.jsonl` — one line per API query with hit count (zeros included).

## ES ingest (deferred — local ES unreachable)

Follow-up when local ES is back:

```bash
# create index with keyword-friendly mapping, then bulk-index with doc IDs
# equal to each record's fingerprint (deterministic, idempotent upsert):
python3 - <<'EOF'
import json, urllib.request
ES="http://localhost:9200"
for f in ("openai-agent-traces/data/urlscan.jsonl",
          "openai-agent-traces/data/commoncrawl.jsonl"):
    with open(f) as fh:
        for line in fh:
            rec=json.loads(line)
            req=urllib.request.Request(
                f"{ES}/openai-agent-traces/_doc/{rec['fingerprint']}",
                data=json.dumps(rec).encode(),
                headers={"Content-Type":"application/json"}, method="PUT")
            urllib.request.urlopen(req)
print("done")
EOF
```

Hosted ES is frozen — local only, never touch it. Doc IDs = fingerprints make
the ingest append-safe: re-running replaces identical docs (no clobbering of
other lanes' docs since IDs are lane-namespaced via the identity strings).

## Scope

Agents and agent infrastructure only. No human/operator attribution pursued.
