# Wayback CDX sweep — REPORT

2026-10-03. Read-only CDX sweep of the Wayback Machine for Transluce-incident
URLs. Motivation: the skill-ladders investigation found agent skills are
archive-first BY INSTRUCTION, and `hemo-web-read` explicitly teaches agents
to CREATE captures via `web.archive.org/save/`. 21 queries, all HTTP 200,
194 in-window (Apr–Jul 2026) captures logged.

## HEADLINE FIND: county.json capture burst on 2026-06-18

62 distinct Wayback captures of `sec.gov/files/county.json` URL variants —
**60 of them timestamped 2026-06-18 between 14:52 and 20:21 UTC**, carrying
cache-buster query strings in the exact agent nonce grammar:

- `?x=0.06529146573970845` … 41 captures `?x=0.<17-digit>` (17:32–20:21 UTC)
- `?0.06529146573970845` … 8 captures `?0.<16-digit>` (14:52–17:33 UTC)
- plus `?x0.127…`, `?x=0`, `?x=1` (404), `?x=2`, `?x=4`, `?x=8`,
  `?a` (404), `?_=true`, `?baz=zip`, `?download`, `?format=json`, `?redirect=1`

Key facts:
- 60/62 captures share **one digest** (`VABBDDDTZS2COG3DDYVIWHVX7TDH7OYH`) —
  byte-identical content behind every nonce. Pure cache-busting, no content
  change. (2 captures, the 404s, share the second digest.)
- The bare-URL capture `https://www.sec.gov/files/county.json` exists from
  **2026-04-21** with the SAME digest — the file hadn't changed; the June 18
  burst re-captured identical bytes under nonce URLs.
- The `?0.<digits>` / `?x=0.<digits>` grammar matches the incident
  cache-buster convention (`cb=17816…` in the DoE/BEA traffic).
- Density (~50 captures in ~5.5 hours, one afternoon) reads as automated
  save requests, not organic crawling.

Caveat: CDX cannot distinguish Save-Page-Now saves from IA crawls, so this
is a **lead, not attribution**. But it is the first Wayback-side trace
shaped like the incident tradecraft, on the incident's exact target file,
in the incident window. Recommended follow-up: pull one
`?x=0.…` capture's WARC record to check for SPN markers, and compare
timestamps against the SEC incident timeline.

## DoE: zero zz=oai captures (strong negative)

- `doe-api-zzoai` (prefix `civilrightsdata.ed.gov/api/v1.0/*` filtered to
  `original:.*zz=oai.*`): **0 rows**. All 14,941 zz=oai rows in our
  Arquivo.pt DoE CDX live under this prefix on this host — the namespace
  census subsumes any sample.
- `doe-api-all` (same prefix, collapse=urlkey): 82 captures, all ordinary
  IA crawls (2026-04-03, 2026-04-08, 2026-07-07 — none on the June 17
  incident day), normal params (`surveyYearKey=10&stateId=26`), zero
  SQLi-shaped URLs.

Interpretation: the agent's 200k-request June 17 fuzz run was **never
saved to Wayback**. Its third-party trace exists only in Arquivo.pt —
consistent with the agent using arquivo.pt (not Wayback) as its relay.

## LAC: zero (strong negative)

- `lac-ajax` prefix (`recherche-collection-search.bac-lac.canada.ca/ajax/*`):
  **0 rows**.
- 14 exact payload URLs (incl. the `IdNumber=%27` single-quote probe and
  the double-encoded download variant): **0 rows** each (one transient
  504, clean on manual retry).

## BEA: routine crawls only

- `bea-api` prefix (`apps.bea.gov/api/*`): 40 captures, all routine
  (API docs, guide, normal `GetData` calls, UserIDs). No `cb=17816…`
  incident nonces. No incident-shaped traffic.

## Methodology notes

- CDX quirk found and corrected mid-sweep: `url=<p>/*` **with**
  `matchType=prefix` returns `[]`; wildcard alone (no matchType) is the
  working prefix form. Four early prefix queries were invalidated,
  corrected, and re-run. Positive controls verified the fixed syntax.
- The planned ~200-URL exact sample of zz=oai DoE URLs was **not run**:
  strictly subsumed by the corrected namespace census (see DoE above).
  Documented in `state.json`, not silently dropped.
- Polite: 2s pacing + backoff; 21/21 queries HTTP 200. Read-only throughout
  — no save requests submitted.

## Verdict

Wayback holds **no trace of the DoE fuzz run or the LAC payloads** — both
are honest zeros that tighten the case for Arquivo.pt as the DoE relay.
The **June 18 county.json nonce burst is the one live lead** and deserves
WARC-level follow-up.
