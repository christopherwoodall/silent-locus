# Librarian persona — wiki/docs knowledge-system traversal via keyless htmx search

**Run:** 2026-10-05 04:44–04:58 UTC (Sun 2026-10-04 23:44–23:58 CDT)
**Status:** BLOCKED — VM egress outage. No htmx queries could be executed.
**Author:** subagent (librarian lane, chinese-amap-fleet)

## 1. Surface and method

Target surface: urlquery.net keyless htmx search endpoint
`GET https://urlquery.net/api/htmx/search/?q=<query>&limit=<n>&offset=<n>`
headers: `HX-Request: true`, standard browser UA (mirrors `~/workspace/skills/urlquery/bin/uq_htmx.py`).

Planned query battery (ALL QUEUED, none executed):
`wiki`, `mediawiki`, `fandom.com`, `wiktionary`, `docs.`, `readthedocs`,
`gitbook`, `notion.site`, `archive.org/details`, `huggingface.co/datasets`,
`dataset`, `catalog`, `library`, plus non-English wiki domains to be discovered
from first-pass results (e.g. `baike`, `wikiwand`, `*.wikipedia.org` language editions,
`namu.wiki`, `moegirl`, `atwiki`, `wikidot`, `miraheze`).

For each cluster the plan was: group by submitted host, count volumes, check
submission timestamps for metronomic cadence, look for sequential/alphabetical
page enumeration, burst parallelism (many reports within minutes), and new
tag/param grammars (`uq*` grammar excluded per charter).

## 2. Why nothing ran — egress outage (evidence)

- `uq_htmx.py search --query wiki --limit 5`: urllib timed out in TLS tunnel (~60s).
- `curl` via `$https_proxy` (hatch-egress-proxy:3128): **all hosts** time out —
  `https://urlquery.net`, `https://example.com`, `https://www.google.com` all `000`
  after 15–25s. The proxy accepts TCP (port 3128 reachable) but never completes
  any request.
- Direct egress (`--noproxy '*'`): fails with
  `OpenSSL error:0A00010B:SSL routines::wrong version number` — transparent
  intercept; no direct path.
- Retry at 04:57 UTC (5-min backoff): still fully dead.
- Browser-fetcher fallback: `browser.open` on the htmx endpoint returned an
  empty 204; `browser.open` on `https://urlquery.net/search?q=wiki` rendered only
  the page shell (results load via htmx/JS, no content without it).
- Cross-lane confirmation: grammarian lane notes "urlquery/urlscan egress died
  mid-run" starting ~04:42 UTC 2026-10-05 — same outage, observed independently.

This is an infrastructure outage, not a urlquery.net outage per se: urlquery's
site resolves and the runtime fetcher got an HTTP response (204) from it, while
the VM's own proxy path hangs on every host.

## 3. Partial findings from non-endpoint sources (no traversal volumes)

Because the search surface was unreachable, these come from local corpora,
sibling lanes, and web search — useful as negatives and leads, NOT as the
planned systematic sweep.

### 3a. Transluce v5 frozen corpus (`urlquery-agent-activity-2026-09-22-v5`)
Grep over `all-reports.csv` for wiki/mediawiki/fandom/wiktionary/readthedocs/
gitbook/notion.site/archive.org-details/huggingface: **1 hit**, and it is noise —
"wiki" appears only in free-text notes on a US-federal-budget-documents record
(`42fa1863-…`, 2026-05-26, IHME/MAX budget cohort). No submitted wiki/doc URLs in
the frozen set. → **honest negative on the frozen corpus.**

### 3b. Sibling-lane verdicts (already on disk)
- auditor lane-b-watchers: `collusion.wiki` on urlquery = **5 irregular scans**
  (Sep 8×3, Sep 10, Sep 24, Sep 28) — graded **analyst triage**, not metronomic.
  Not a traversal campaign.
- global-south-scout: India records show agent **link-laundering via wiki boards**
  (`proxy.cors.sh/https://www.indiascienceandtechnology.gov.in/…` with
  Google-Translate params) — wiki-board *grammar* reuse, but no urlquery
  submission campaign against the wiki itself.
- mimic infra-migration: agents read wikis (markdowner instances) but that is
  *consumption*, not urlquery-submitted traversal.

### 3c. Web search for indexed urlquery wiki reports
Queries: `urlquery.net report wikipedia submitted`; `"urlquery.net/report" mediawiki submitted pages scan`.
All indexed hits are **noise**: Wikipedia appears as a phishing redirect
finishing URL, or `MediaWiki:` as a Wappalyzer-style tech fingerprint in malware
reports (metasploit `.msi` droppers, pages.dev phishing kits). One legit scan:
`ps1.mywikis.wiki/wiki/FormLabs_Form_1+_SLA_3D_Printer` (report
`75e75a88-…`, 2025-08-15) — a **single** maker-space wiki scan, no cluster.
Grade: **noise / singletons** — no systematic traversal surfaced via the search
engine's index.

### 3d. Pre-outage htmx caches (metronome lane, `raw/htmx_*.json`)
12 cached query results scanned for wiki/docs-ish submitted URLs: **0 hits**
(queries were relay/poller-focused, so this is a weak negative, not coverage).

## 4. Grading (as far as evidence permits)

| Cluster | Grade | Basis |
|---|---|---|
| collusion.wiki on urlquery | **human triage** | auditor lane: 5 irregular analyst re-checks |
| Wikipedia as finishing URL in phishing reports | **noise** | indexed reports; Wikipedia is the redirect target |
| MediaWiki as tech fingerprint in malware reports | **noise** | Wappalyzer-style detection, not traversal |
| ps1.mywikis.wiki single scan | **singleton** | 1 report, 2025-08-15, no cluster |
| Any systematic wiki/docs/catalog traversal on urlquery | **UNKNOWN — unexecuted** | egress outage; the query battery below is queued |

No `uq*` tag grammar encountered (no data to encounter it in). No new tag/param
grammars observed.

## 5. Re-run plan (for when egress recovers)

1. Re-run `uq_htmx.py search --query <q> --limit 100` for each query in §1,
   ≥5s between calls (site throttles; coordinator previously backed off when
   children + coordinator shared the keyless budget).
2. Fallback if htmx stays flaky: `uq.py search` (authenticated `custom.urlquery`
   API, `api.urlquery.net`) — separate rate-limit budget.
3. Cluster by submitted host; for each cluster compute: volume, date span,
   inter-submission deltas (metronome check), URL path sequences (page 1,2,3…
   or alphabetical walks), burst parallelism, submit tags.
4. Non-English discovery pass: from first results, extract wiki-ish hosts
   (`*.fandom.com`, language `*.wikipedia.org`, `baike.*`, `namu.wiki`,
   `*.wikidot.com`, `*.miraheze.org`) and run targeted follow-up queries.
5. Write cluster table + grades into this file; do not push.

## 6. Caveats

- urlquery search only returns *public* reports; private submissions are invisible.
- The htmx endpoint paginates 24/page; systematic traversal needs deep offsets.
- Absence from urlquery ≠ absence of agent wiki activity (agents may browse
  directly without submitting scans).
