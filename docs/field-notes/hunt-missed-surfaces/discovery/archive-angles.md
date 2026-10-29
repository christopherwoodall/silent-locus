# Discovery: untested archive angles

Scout date: 2026-10-03. Read-only, keyless, polite pacing (1.5–3s between requests).
Every query logged in `logs/query-log.txt`; raw evidence in `logs/`. Honest zeros are findings.
Scope: agents and agent infrastructure only. No commits (merger handles that).

Incident fingerprints: DoE `civilrightsdata.ed.gov` Jun 17 2026 (`zz=oai` fuzz run);
LAC `recherche-collection-search.bac-lac.canada.ca` May 28 / Jun 9 2026 (SQLi payloads);
SEC `www.sec.gov/files/county.json`; BEA Jun 16–21 2026.

## 1. archive.today's own index — FERTILE but CAPTCHA-BLOCKED

**How to query it (new):** the index is directly searchable at `https://archive.ph/<query>`
(the homepage `/search/?q=` form 302-redirects there). The result page documents its own
grammar: `<domain>` = all snapshots from host, `*.<domain>` = subdomains,
`http://<url>` = exact URL, `http://<url>*` = URL prefix. No key needed.

**Completed probes (HTTP 200, pre-block):**
- `civilrightsdata.ed.gov` → 5 snapshots, newest **29 Aug 2025** — all pre-incident, zero 2026 captures.
- `sec.gov/files/county.json` → "No results".
- `bac-lac.gc.ca` → "No results".

**Blocked:** prefix/deep probes (`http://civilrightsdata.ed.gov/*`, `bea.gov`,
`recherche-collection-search.bac-lac.canada.ca`, `http://www.sec.gov/files/county.json*`)
returned HTTP 429, then a "One more step" CAPTCHA. **Hard stop — no bypass attempted.**
The single most valuable unrun query is the `/api/v1.0/*` prefix form.

**Verdict: FERTILE, unfinished.** Recommend live-browser follow-up (parent can delegate)
or a cooldown retry; archive.today is hermes-ladder rung 2, so its prefix index is
high-EV.

## 2. Wayback CDX for relay-wrapped URLs — METHOD PROVEN, incident window negative

Wayback CDX accepts mid-URL wildcards (`url=r.jina.ai/http*://<host>*`), HTTP 200 throughout.

- `r.jina.ai/http*://civilrightsdata.ed.gov*` → **0 rows** (retried, confirmed).
- `r.jina.ai/http*://www.sec.gov/files/county.json*` → **0 rows**.
- `api.allorigins.win/*civilrightsdata*` → **0 rows**.
- `r.jina.ai/https://www.sec.gov*` → 4 rows: one EDGAR filing wrapped 2025-08-04 (benign),
  **two jina-wrapped `county.json` captures dated 2026-09-11 and 2026-09-24** (post-incident;
  likely researcher/observer traffic after the Sep 23 Transluce report — the Sep 11 one
  predates the report and deserves a WARC peek to rule out agent origin).

**Verdict: FERTILE AS A METHOD, negative for the incident window.** Wrapped-URL CDX
probing works and should be extended to more wrappers (`corsproxy.io`, allorigins `/raw`
paths, `r.jina.ai/http://` variants for LAC/BEA hosts) — cheap to run.

## 3. Arquivo.pt for relay-wrapped URLs — DEAD END (validated)

Controls first: `url=example.com` and `url=r.jina.ai` return records (API works, JSONL format);
exact `https://www.sec.gov/files/county.json` returns empty (consistent with no SEC coverage
in our Arquivo.pt holdings). Wrapped probes, all HTTP 200 empty:
- `r.jina.ai/https://www.sec.gov/files/county.json*` → 0
- `r.jina.ai/http*://civilrightsdata.ed.gov*` → 0
- `api.allorigins.win/*sec.gov*` → 0

**Verdict: DEAD END.** Genuine zeros, API confirmed working.

## 4. Ghost Archive: wrapped + deep paths — DEAD END for our targets

Ghost Archive's curl-accessible substring search **does** index relay-wrapped URLs in
general: `r.jina.ai` → 9 result pages, `allorigins` → 8 pages, `jina.ai/http` → 8 pages.
Targeted probes:
- `r.jina.ai/https://www.sec.gov` → "No archives for that site" (0/0 pages).
- `r.jina.ai/http://civilrightsdata` → 0/0 pages.
- All 8 pages each of `allorigins` and `jina.ai/http` (16 pages total) scanned for
  `sec.gov|civilrightsdata|bea.gov|bac-lac|canada.ca|county.json|zz=oai` → **zero hits**.
- Deep-path search is unsupported: any term containing `/` or `=` (`civilrightsdata.ed.gov/api/v1.0`,
  `zz=oai`, `county.json`) 302-redirects to the dead `/vidsearch` page. (Prior art stands:
  bare `bac-lac.gc.ca` had 2 hits incl. one in-window May 10 2026 capture.)

**Verdict: DEAD END for our targets.** The method is sound; the holdings don't include us.

## 5. Memento aggregator — DEAD END (service down)

`timetravel.mementoweb.org` DNS resolves (198.18.124.93) but TCP connections fail on
both port 80 and 443 (HTTP 000, three attempts). Matches the earlier "liveness unverified"
assessment — the aggregator is unreachable, not just quiet.

**Verdict: DEAD END.** No cross-archive rollup available from this VM.

## Ranked verdicts

1. **archive.today prefix probing** — highest-value unfinished work. Index is queryable,
   three base probes are clean negatives, but the `/api/v1.0/*`-style prefix queries are
   CAPTCHA-blocked. Needs live browser or a cooled-down IP.
2. **Wayback wrapped-URL CDX** — method proven; extend wrapper/host matrix (cheap, unblocked).
   Follow-up: WARC-peek the two Sep 2026 jina-wrapped county.json captures.
3. **Ghost Archive** — exhausted for our targets (16 wrapped-relay pages scanned, deep paths unsupported).
4. **Arquivo.pt wrapped** — exhausted (validated zeros).
5. **Memento** — service down; revisit only if it comes back.

Net new leads: one — the Sep 11/24 2026 jina-wrapped county.json Wayback captures
(post-incident; verify before claiming anything).
