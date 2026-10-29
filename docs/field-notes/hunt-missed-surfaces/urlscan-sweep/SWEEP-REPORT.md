# urlscan.io sweep — REPORT

2026-10-03. Finishes the urlscan.io query sweep for the "what has Transluce
missed" hunt. 32 queries, all HTTP 200, every one logged in
`data/query-log.jsonl` (raw responses for hit-queries in `data/raw/`).

## Methodological finding: the "403 block" was query syntax, not IP blocking

The prior lane (`../hot-leads/`) hit 403s from query 7 onward and stopped
per its hard guard, assuming it was blocked. It wasn't. urlscan.io's
anonymous search API rejects certain query shapes with:

> "Regular Expressions and leading wildcard searches are not supported for
> anonymous users, please create a user-account."

Empirically (2026-10-03):
- **403:** leading wildcards (`task.url:*civilrightsdata*`) and unquoted
  values containing `/` (`task.url:sec.gov/files/county.json`).
- **200:** trailing wildcards (`task.url:civilrightsdata*`), quoted path
  values (`task.url:"sec.gov/files/county.json"`), plain terms, and
  historical `date:>`/ `date:<` ranges.

All 21 previously-"blocked" queries were rerun in compliant shapes, plus 9
new IOC follow-ups. No rate-limit stop was triggered; polite 4s pacing held
throughout.

## Results

**Incident hosts in submitted URLs** — `civilrightsdata*`: 0;
`bac-lac.gc.ca*`: 0; `bac-lac.canada.ca*`: 0; `kansasmemory*`: 0;
`bea.gov*`: 2 (routine bea.gov homepage scans, Sep 2026 — not incident);
`census.gov*`: 3 (routine homepage scans + one ACS summary-file download,
Sep–Oct 2026 — not incident).

**Incident windows** — all ten window queries returned 0, plus the two
broader June windows:
DoE Jun 16–19: 0 · BEA Jun 16–18: 0 · Census Jun 16–22: 0 · SEC Jun 18: 0 ·
Kansas May 7: 0 · LAC May 28: 0 · LAC Jun 9 (both hosts): 0 ·
MAX.gov May 25–27: 0 · CDC WONDER Jul 18: 0.

**Filenames** — `virginia-projection*`: 0; xls on ed.gov: 0; xls on
census.gov: 1 (2008 population-estimates file, unrelated); xls on bea.gov: 0;
`county.json` on sec.gov: 0; exact `sec.gov/files/county.json` path: 0.
(The earlier lane's `filename:county.json` 16 hits were all
ramseycountymn.gov noise — re-confirmed.)

**Launcher IOC markers** — `zz=oai` in task.url: 0; in page.url: 0;
`openai_research` variants in task.url / page.url: 0 / 0;
`survey_Year_Key` in page.url: 0; `GetStateEstimation` in task.url: 0.

**Noise grading** — `page.url:oai*`: 177 results, all noise (oai-academy
sites, oaipya, S3 backup buckets, phishing-shaped domains). Bare `oai` is
undorkable on urlscan, as expected.

## Verdict

**urlscan.io is a confirmed negative for every incident fingerprint.**
The corpus demonstrably indexes .gov scans (bea.gov, census.gov hits prove
coverage), so the zeros are meaningful, not a coverage gap. No submission
in the index touches the DoE CRDC API shapes, the LAC collection-search
service, the SEC county.json path, or any launcher IOC marker, in-window or
otherwise.

Combined with the earlier lane's finding — agent fuzz traffic for the DoE
cluster exists only in Arquivo.pt captures — urlscan.io drops out as a
trace source for these incidents. It remains a valid surface in general
(Transluce's method is proven), just not for these fingerprints.

## Rerun

`python3 sweep.py` — idempotent via `state.json`; skips completed queries.
