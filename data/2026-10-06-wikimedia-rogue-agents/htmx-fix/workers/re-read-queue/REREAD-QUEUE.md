# HTMX re-read queue — suspect prior zero-result claims

**Compiled:** 2026-10-06 ~19:30 CDT (2026-10-07 ~00:30 UTC) · **Worker:** re-read-queue (read-only text mining; no network calls)
**Base dir:** `~/workspace/silent-locus/data/` (paths below are relative to it)

## The bug being queued against

The urlquery htmx search endpoint `GET https://urlquery.net/api/htmx/search/?q=<q>&limit=<n>&offset=<n>`
changed its contract: the old pattern now returns **`204 No Content` for every query** instead of
result HTML. Parsers that scrape `/report/<uuid>` hrefs turn an empty 204 body into
`{"reports": []}` / "0 reports" / "0 hits" — a failed request misfiled as a clean negative.

- **Discovered:** 2026-10-06 ~23:19–23:24 UTC by the `lifeval-cross-corpus/workers/urlquery-live` worker
  (verified 204 for `q=Lifeval` AND the `q=wikipedia` control, with and without custom UA).
- **Corroborated:** `2026-09-28-chinese-amap-fleet/farmable-surfaces/FINDINGS.md:226`
  ("needs `HX-Request: true` + `HX-Current-URL`; returns 204 without them").
- **Earliest observed 204 in the wild:** russian-agent-hunter, 2026-10-05 ~05:45 UTC
  ("`тест`, `проверка` via `uq_htmx.py`: HTTP 204 / `{\"reports\": []}`") — the break predates
  its discovery by ~42h.
- **Working pattern** (urlquery-live, 2026-10-06): the live site's form fields
  (`type=reports&view=list&limit=24&offset=0&q=`) **plus** full htmx header set:
  `HX-Request: true`, `HX-Trigger: search_query`, `HX-Target: search_results`,
  `HX-Current-URL: https://urlquery.net/search`, `Referer: https://urlquery.net/search`.

### Pattern classes used below

| Class | Meaning |
|---|---|
| `PARTIAL` | `uq_htmx.py` / `uq_htmx_curl.py` / `cartographer/sweep-curl.py` / full-sweep's documented curl — sends `HX-Request: true` + `HX-Current-URL` (+UA/Accept) but **not** `HX-Trigger`/`HX-Target`/`Referer` and **not** the `type=reports&view=list` form fields. Every prior lane used this class. |
| `HEADERLESS` | Bare GET, no HX headers at all (plain curl, `browser.open`). |
| `UNCERTAIN` | File says "htmx" but names no tool; pattern class could not be determined from the text. |
| `ERROR-AS-ZERO` | Not a 204: the "zero" was filed from a network/urllib exception (IncompleteRead, proxy-CONNECT failure). Same re-read need, different root cause — flagged so the fix-verification step doesn't conflate them. |

### Why everything below is queued even though some queries worked

In several runs the PARTIAL pattern returned real data for *some* queries while zeroing others
in the same session (polyglot `gov.br`→6 reports vs `gov.eg`→0; de-linguist q2/q6/q7→hits vs
q1/q3/q4/q5/q8→`{"reports": []}`; arabic keyword queries→data vs `url.domain:`→zeros;
lighthouse `marinetraffic`→hits vs `mmsi`→0). The 204 is therefore **not cleanly time-gated** —
it may be query-dependent, rolling, or throttling-adjacent. No old-pattern zero can be trusted
without a re-read against the fixed pattern.

### Scope notes

- **Included:** zero-result claims from urlquery *htmx searches* (keyless `/api/htmx/search/`), any pattern class.
- **Excluded:** zeros from authenticated `api.urlquery.net` (`uq.py`), urlscan.io, web search engines,
  Sourcegraph/GitHub code search, local corpus greps, shortener stats APIs, stash.legible.sh probes,
  `httpbun /status/204` beacon evidence (that 204 is payload tradecraft, not a search artifact),
  archive.today "No results", methodology-refresh bookkeeping, and zeros already filed with the
  FIXED pattern (urlquery-live worker, 2026-10-06).

---

## The queue

| # | File (line) | Query (as stated) | Script / pattern | Load-bearing? | Status |
|---|---|---|---|---|---|
| 1 | `2026-09-28-chinese-amap-fleet/personas/russian-agent-hunter/FINDINGS.md:13` | `тест`, `проверка` — filed as "HTTP 204 / `{\"reports\": []}`" | `uq_htmx.py` — PARTIAL | **YES** — Lane 1 of the "no Russian agent find" verdict | QUEUED |
| 2 | `2026-09-28-chinese-amap-fleet/personas/russian-agent-hunter/FINDINGS.md:13` | `url.domain:gov.ru` → `{"reports": []}` (same session; keyword `gov.ru` sweep separately returned 45 reports) | `uq_htmx.py` — PARTIAL | partial — Lane 1; keyword sweep worked in parallel | QUEUED |
| 3 | `2026-09-28-chinese-amap-fleet/personas/arabic-agent-hunter/FINDINGS.md:8` | 13× `url.domain:gov.{sa,ae,eg,qa,kw,bh,om,jo,iq,lb,ma,tn,dz}` — all `{"reports": []}` (raw cached in `raw/htmx_url_domain_gov_*.json`; `gov_jo` file is 0-byte/error) | `uq_htmx.py` — PARTIAL | partial — lane already disavowed these in §5 ("later proven unreliable"); the "no agent-shaped clusters" verdict rests on keyword queries that returned data | QUEUED |
| 4 | `2026-09-28-chinese-amap-fleet/personas/polyglot/FINDINGS.md:60-61` | `url.domain:gov.vn`, `url.domain:gov.in`, `url.domain:gov.eg` → `{"reports": []}` (raw cached); `url.domain:go.id` → `{"reports": []}` (proven coverage gap — 5 known-live records resolve via curl) | `uq_htmx.py` — PARTIAL (11/17 queries in the run returned data) | **YES** — honest zeros underpinning "no agent-shaped non-English activity" | QUEUED |
| 5 | `2026-09-28-chinese-amap-fleet/german-french-swarm-hunt/workers/de-linguist/FINDINGS.md:123-125` | `httpbun aufgabe`, `httpbun ergebnis`, `claude httpbun`, `uqscan berlin`, `sub_poi_navi berlin` — all `{"reports": []}` (raw cached `raw/q1,q3,q4,q5,q8_*.json`; q2/q6/q7 in the same run returned hits) | `uq_htmx.py` — PARTIAL (documented at FINDINGS.md:163) | **YES** — HONEST NEGATIVE grades feeding the EUROSWARM "no German swarm" verdict | QUEUED |
| 6 | `2026-09-28-chinese-amap-fleet/behavior-hunt/lang-hindi-japanese-korean/FINDINGS.md:10` | ~30 queries via `uq_htmx.py` (e.g. `url.domain:map.naver.com` → 0); verdict "NO FLEET FOUND… All three lanes are honest zeros" | `uq_htmx.py` — PARTIAL | **YES** — entire lane verdict | QUEUED |
| 7 | `2026-09-28-chinese-amap-fleet/behavior-hunt/lang-polish-turkish-arabic/FINDINGS.md:16-18` | PL/TR/AR tag-grammar queries (`wyszukiwanie2026`, `arama2026`, `bahth2026`, …) — 0 hits each | `uq_htmx.py` — PARTIAL | **YES** — "no fleet" verdict for PL/TR/AR | QUEUED |
| 8 | `2026-09-28-chinese-amap-fleet/behavior-hunt/lang-vietnamese-indonesian-thai/FINDINGS.md` | 26 queries via `uq_htmx.py`; verdict "No Vietnamese, Indonesian, or Thai agent fleet found on any of the 26 behavioral checks" | `uq_htmx.py` — PARTIAL | **YES** — entire lane verdict | QUEUED |
| 9 | `2026-09-28-chinese-amap-fleet/behavior-hunt/FINDINGS.md:48` | `<word>2026` FR/DE/ES agent words (`recherche2026`, `suche2026`, `busqueda2026`, …) — all 0 hits | htmx — UNCERTAIN (summary of delegated lanes) | **YES** — "No language-switching in tag grammar observed" | QUEUED (covered by #6–#8 lane re-reads; listed for the summary claim) |
| 10 | `2026-09-28-chinese-amap-fleet/personas/french-agent-hunter/FINDINGS.md:43` | `url.domain:scaleway.com` — 0 hits (empty result set); sibling `url.domain:ovh.com` in the same section returned 5 hits | htmx — UNCERTAIN | partial — OVH/Scaleway section of "no French agent fleet" verdict | QUEUED |
| 11 | `2026-09-28-chinese-amap-fleet/personas/lighthouse-keeper/FINDINGS.md:22-24` | `url.domain:aisstream.io`, keyword `marinetraffic.com/en/ais`, keyword `mmsi` — 0 reports each; sibling queries returned hits | `uq_htmx_curl.py` — PARTIAL | **YES** — verdict "no agent-shaped maritime activity found" | QUEUED |
| 12 | `2026-09-28-chinese-amap-fleet/personas/ham-radio/FINDINGS.md:26-29` | `url.domain:pskreporter.info`, `url.domain:openwebrx.de`, `url.domain:sdr.hu`, `url.domain:rx-tx.info`, `url.domain:satnogs.org` — 0 each; sibling keyword queries returned hits | htmx curl variant — PARTIAL | partial — HONEST NEGATIVE also rests on corpus + urlscan zeros | QUEUED |
| 13 | `2026-09-28-chinese-amap-fleet/personas/birdwatcher/FINDINGS.md:50-52` | `url.domain:gbif.org`, `url.domain:api.ebird.org`, `url.domain:api.inaturalist.org` — 0 reports each | htmx curl variant — PARTIAL | partial — "No evidence of agents farming the actual biodiversity APIs" | QUEUED |
| 14 | `2026-09-28-chinese-amap-fleet/personas/watchmaker/FINDINGS.md:22` | `url.domain:timeapi.io` — 0 reports; sibling `url.domain:worldtimeapi.org` returned 1 | htmx — UNCERTAIN | partial — "Live surfaces confirm it" (agents don't phone time APIs) | QUEUED |
| 15 | `2026-09-28-chinese-amap-fleet/personas/cartographer/FINDINGS.md:44` | `tronzap` on urlquery htmx (pre-outage, 2026-10-05) — 0 reports → "no urlquery-side footprint; campaign is urlscan-visible only" (cited by new-fleets FINDING 12) | `sweep-curl.py` — PARTIAL (`HX-Request` + `HX-Current-URL` only) | **YES** — the urlscan-only characterization of the TronZap campaign | QUEUED |
| 16 | `2026-09-28-chinese-amap-fleet/full-sweep/FINDINGS.md:14` | 8 ZeroSSL tunnel names (`a7bfa19dd56391`, `ca990e9a89525d`, …) — 0 reports each → "Zero overlap" with the 78 fleet tunnel names → INDEPENDENT verdict | documented curl — PARTIAL (`-H "HX-Request: true" -H "HX-Current-URL: …"`, `limit=25`, no Trigger/Target/Referer/form fields) | **YES** — "Zero overlap" is the INDEPENDENT verdict's load-bearing leg | QUEUED |
| 17 | `2026-09-28-chinese-amap-fleet/personas/global-south-scout/CHASE.md:60` | `gov.th` — `{"reports": []}` (raw `raw/chase/live-gov.th.json`, htmx-shaped output) → "clean live negative" | `uq_htmx.py`/`uq_htmx_curl.py` — PARTIAL | **YES** — the Thailand "clean live negative" | QUEUED |
| 18 | `2026-09-28-chinese-amap-fleet/german-french-swarm-hunt/workers/warnung-check/FINDINGS.md:30` | `url.domain:warnung.bund.de` (limit 50) — 0 reports on htmx while the keyword form returned 1 (attributed in-file to a `url.domain:` syntax quirk) | htmx — UNCERTAIN (limit=50 matches the old documented pattern) | no — singleton claim rests on the keyword search, which returned 1 | QUEUED |
| 19 | `2026-09-28-chinese-amap-fleet/personas/italian-agent-hunter/FINDINGS.md:131` | `star-vegas.it` — zero on urlquery htmx AND zero on urlscan | `uq_htmx_curl.py` — PARTIAL | no — lead stays "flagged, not claimed" either way | QUEUED |
| 20 | `2026-09-28-chinese-amap-fleet/personas/registrar/FINDINGS.md:11` | `url.domain:pages.dev uqscan` = 0 (same paragraph notes the known htmx weak-negative quirk) | htmx — UNCERTAIN | no — the pages.dev fleet finding is corpus-verified | QUEUED |
| 21 | `2026-09-28-chinese-amap-fleet/personas/hebrew-agent-hunter/FINDINGS.md:54` | keyword `gov.il` returned an empty/errored file while `url.domain:gov.il` returned 3 reports | ERROR-AS-ZERO — raw `htmx_err.log` shows `IncompleteRead` tracebacks, file is 0 bytes | no — tradecraft note only; lane findings rest on `url.domain:` + `/related/*` endpoints | QUEUED |
| 22 | `2026-09-28-chinese-amap-fleet/personas/fileshare-farmer/FINDINGS.md:35` | `gofile.io`, `catbox.moe`, `filebin.net`, `temp.sh`, `mirrorace.com` — filed as "0 reports" each, BUT `raw/urlquery_domains.json` shows **urllib tracebacks** (IncompleteRead / proxy-CONNECT failures) for all five | ERROR-AS-ZERO — `uq_htmx.py` raised; nothing was ever searched | partial — "clean honest negatives across five major share domains" | QUEUED |

**Totals: 22 suspect claims QUEUED — 11 load-bearing YES, 7 load-bearing partial, 4 load-bearing no.**
(20 are 204-suspects; #21 and #22 are error-as-zero misfiles, same re-read need.)

---

## Already handled — do NOT re-queue

| File | What happened | Status |
|---|---|---|
| `2026-09-28-chinese-amap-fleet/personas/auditor/FINDINGS.md:57` | 11 htmx archive-term queries returned 0 despite ≥103 known-live `cachedview.nl` reports. **Diagnosed in-file as egress-outage artifact** (2026-10-05 ~04:28–04:40, inside the 04:55–05:20 UTC outage window); live re-test 2026-10-05 ~05:24 UTC proved fragments ARE indexed. Re-run already planned in the file. | ALREADY-QUEUED (diagnosed) |
| `2026-09-28-chinese-amap-fleet/personas/librarian/FINDINGS-wiki-swarm-2026-10-05.md:53` | htmx-wikis lane **never ran** — every htmx attempt timed out / 204'd during the outage; filed as BLOCKED with partial negatives only. Re-run procedure + queued query battery in `personas/librarian/htmx-wikis.md`. | ALREADY-QUEUED (own re-run spec) |

## Noted but not queued (no zero claim filed)

- `new-fleets/FINDINGS.md:187` — 2026-10-05 ~04:55–05:20 UTC egress outage: `uq_htmx.py` timeouts ×2, `browser.open` htmx → HTTP 204 empty. Filed as a **collection gap**, not a zero. No re-read needed beyond the gap-fill already armed.
- `trade-labourer/FINDINGS.md:44,72` — htmx for tunn3l.sh/pinggy/liveport/portal/agentwebhook filed as **throttled (empty responses) — retry pending**. No negative finding was built on it.

## Exclusion log (checked, deliberately out of scope)

- Corpus greps (all `events.jsonl` / frozen-corpus zeros), authenticated `api.urlquery.net` (`uq.py`) zeros, urlscan.io zeros (incl. ham-radio:36, metronome:79, model-whisperer:41, iranian:85), web-search zeros, Sourcegraph/GitHub code-search zeros, shortener stats-API zeros, `stash.legible.sh` probe zeros, `httpbun /status/204` beacon evidence, archive.today "No results", METHODOLOGY.md refresh bookkeeping.
- `lifeval-cross-corpus/workers/urlquery-live/FINDINGS.md` zeros — filed with the FIXED pattern (full HX headers + form fields), not suspect.
- `german-agent-hunter-2/FINDINGS.md:53` (`bmi.bund.de | 0 results | Clean`) — urlscan API-method sweep (Lane 2), not htmx. Out of scope.
- `toddler-watcher/FINDINGS.md:57` "honest zeros" — from the frozen unified corpus, not live htmx (live htmx never recovered in that lane's window).
- `contrarian/raw/htmx-anomalies.md:23` — corpus 48h-window zeros (live htmx was impossible during the outage; fallback was the local corpus).
- `seasia-summary.md:7` — 0-byte JSON with `.err` traceback sidecars; explicitly filed as "No live-search verdicts were obtained", not as zeros.

## Re-run instructions (for the coordinator)

1. Verify the fixed pattern (full HX header set + `type=reports&view=list&limit=24&offset=0&q=` form fields) against a control query with known-live results (e.g. `q=wikipedia` → expect rows).
2. Re-run every QUEUED row above with the fixed pattern; cache raw HTML + per-request meta (provenance per the standing cache-everything rule).
3. For rows #21/#22 (ERROR-AS-ZERO), the re-run is a first real search, not a re-read — grade accordingly.
4. Do **not** re-run the ALREADY-QUEUED rows here; they have their own re-run specs.
5. Priority order: load-bearing YES rows first (#1, #4, #5, #6, #7, #8, #9, #11, #15, #16, #17), then partials, then no's.
