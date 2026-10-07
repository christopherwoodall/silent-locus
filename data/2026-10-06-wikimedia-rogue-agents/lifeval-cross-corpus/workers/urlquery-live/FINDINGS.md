# FINDINGS — urlquery-live worker, LIFEVAL cross-corpus sweep

**Worker:** urlquery-live · **Run:** 2026-10-06 ~23:19–23:24 UTC (18:19–18:24 CDT)
**Method:** curl, keyless, read-only, paced ≥6s between requests (standing ≥5s doctrine)
**Coverage:** 11 htmx search queries, all HTTP 200, no rate-limiting or blocks
**Raw evidence:** `../raw/htmx_qNN_*.html` + `../raw/htmx_qNN_*.meta.json` (sha256 per file);
provenance in `../raw/PROVENANCE.md`. Parser: `grade_rows.py`.

## Headline (grade: OBSERVED)

**No urlquery report in the htmx search index contains any Lifeval marker string.**
Both full marker forms (`Lifeval temporary technical sandbox initialization`,
`Lifeval API temp-account test`), the standalone codename `Lifeval`, and all three
`url.domain:`-scoped Lifeval queries (incubator/commons/meta.wikimedia.org) return
the site's "No reports found" template. **Zero surviving hits.** The generic
phrase queries (`sandbox test link`, `testing external link`, `Sandbox link test`,
`Temporary technical sandbox`, `Temporary technical sandbox initialization`)
return only unrelated commercial scans — every one graded NOISE (see appendix).

## Endpoint documentation (for the coordinator)

The htmx search endpoint documented in prior scripts
(`https://urlquery.net/api/htmx/search/?q=<q>&limit=50&offset=0`) is **stale**:
called bare it returns `204 No Content` for *every* query, including the
`wikipedia` control (OBSERVED: 204 for `q=Lifeval`, `q=wikipedia`, with and
without a custom UA; response headers carry no rate-limit or block signals).

The live site's own search form (`https://urlquery.net/search`, fetched
2026-10-06, form `#search_query`, `hx-get="/api/htmx/search/"`) serializes
form fields: `type=reports` (default radio), `view=list`, `limit=24`,
`offset=0`, `q=<text>`. Emulating a real htmx request with that exact
parameter set **plus** `HX-Request: true`, `HX-Trigger: search_query`,
`HX-Target: search_results`, `HX-Current-URL: https://urlquery.net/search`,
`Referer: https://urlquery.net/search` returns `200` with result rows
(verified on `q=wikipedia`: 24 rows, 1+ distinct report UUIDs — response is
HTML fragments, NOT JSON). Custom UA `silent-locus/lifeval-sweep` works fine
with the HX headers; the headers are the gating factor, not the UA.

Response shape: table rows of (date, UQ/IDS/TDS detection badges, submitted
domain linked to `/report/<uuid>`, resolved IP + country flag). The URL column
shows domain or domain+path; matches can be on submitted-URL paths, tags, or
backend-indexed page content not visible in the fragment (e.g. q05's
`sandbox+test+link` pagination link is the only literal "sandbox" in its
response — the matches are on indexed data, not the rendered text).

## Per-string results

| # | Query (raw) | HTTP | Rows / real report UUIDs | Verdict |
|---|---|---|---|---|
| q01 | `Lifeval temporary technical sandbox initialization` | 200 | 0 | ZERO (weak) |
| q02 | `Lifeval API temp-account test` | 200 | 0 | ZERO (weak) |
| q03 | `Lifeval` | 200 | 0 | ZERO (weak) — **not even Tokyo Gas sponsor noise** |
| q04 | `Temporary technical sandbox initialization` | 200 | 1 | 1 hit → NOISE (Exclaimer, see appendix) |
| q05 | `sandbox test link` | 200 | 17 rows / 16 reports | all NOISE (e-commerce cohort) |
| q06 | `testing external link` | 200 | 20 rows / 19 reports | all NOISE (commercial mix) |
| q07 | `Sandbox link test` | 200 | 18 rows / 17 reports | all NOISE (e-commerce cohort, 10 overlap q05) |
| q08 | `Temporary technical sandbox` | 200 | 23 rows / 22 reports | all NOISE (commercial mix) |
| q09 | `Lifeval url.domain:incubator.wikimedia.org` | 200 | 0 | ZERO (weak) |
| q10 | `Lifeval url.domain:commons.wikimedia.org` | 200 | 0 | ZERO (weak) |
| q11 | `Lifeval url.domain:meta.wikimedia.org` | 200 | 0 | ZERO (weak) |

Note on UUID counts: the sweep script's raw grep also matched UUID-shaped
strings embedded in submitted URLs (e.g. `imprintMessageId=acd219da-…` in
q04; goldcast/ziphq/cloudbeds path UUIDs in q06). The "real report UUIDs"
column counts only `/report/<uuid>` hrefs.

## Surviving hits

**None.** Every non-zero result is graded NOISE and documented in the
appendix. No report in the index links any Lifeval marker string to any
submitted URL, and no wikimedia.org domain appears in any response.

## Honest zeros (and why they are weak negatives)

1. `q` matches submitted-URL indexing (per standing hunt knowledge). The
   Lifeval markers live in wiki *page content*, not URLs — a scan of
   `https://incubator.wikimedia.org/wiki/Incubator:Sandbox` would index
   under "incubator.wikimedia.org", never under "Lifeval". Zeros on q01–q03
   are therefore *expected* even if such scans exist in the corpus.
2. Standing caveat (`~/workspace/skills/urlquery/HTMX_ENDPOINTS.md`): htmx
   search demonstrably misses known-live records (5 Indonesia `go.id`
   reports resolve live via curl but return zero from htmx search). Every
   htmx zero is a WEAK negative, not proof of absence.
3. Only the first result page was fetched (`limit=24, offset=0`); none of
   the queries returned more than 24 rows, so pagination was not exercised.
4. q03's zero is itself informative: the expected Tokyo Gas "Lifeval"
   sponsor noise does not appear in the urlquery htmx index at all — the
   index simply has no `lifeval`-in-URL scans, or the term is unindexed.

## Killed-by-noise appendix

- **q04** — 1 report, `083c9d47-1fb7-4381-9d52-a64d1f4159b9`
  (https://urlquery.net/report/083c9d47-1fb7-4381-9d52-a64d1f4159b9),
  scanned 2025-06-06 15:23 UTC: `eu.content.exclaimer.net/?url=https://allledvalve.com/…`
  — an Exclaimer email-signature click-tracking URL (social-media-icon
  template). Zero UQ/IDS/TDS detections. Match is on backend-indexed
  content; nothing wikimedia, nothing agent-shaped. Grade: OBSERVED hit,
  NOISE (unrelated commercial surface, predates incident by a year).
- **q05** — 16 reports, all scanned 2026-10-05/06: e-commerce shops on
  Shopify infra (`23.227.38.x`, CA): kvdveganbeauty.com, designeroptics.com,
  blazepod.eu, duckworthco.com, eskute.com, mojosw.com, mikss.store,
  sekkiseibeauty.com, leatherman.com, fluxfootwear.com,
  vanbeekumspecerijen.nl, hunterboots.com, curlyme.com, plus techcrunch.com
  and biomechanic.info. Grade: NOISE.
- **q06** — 19 reports, scanned 2026-07-22 → 2026-10-05: commercial mix —
  cherrymoonkitchen.com, subfireshousepd.delivery, events.goldcast.io,
  mobilesentrix.com, rockwellautomation.com, promedica.org, app.ziphq.com
  (×2), cheryls.com, brz.ai (×2), pay-by-link.cloudbeds.com,
  ridgecapitalsolutions.io, whatispiping.com, aruplab.com, fruitbouquets.com,
  my.mondae.com, berries.com. Grade: NOISE.
- **q07** — 17 reports: the same e-commerce cohort as q05 (10 shared UUIDs)
  plus mysticmonkcoffee.com, eleven--eleven.com, gem.health, get-selene.com,
  global.arzopa.com, moonbird.life, shopfreshspawns.com. Grade: NOISE.
- **q08** — 22 reports, scanned 2025-03-28 → 2026-08-03: unrelated commercial
  (wm.com, nbcf.org.au, simonthuta.com ×2, migratemate.co, issworld.com ×3,
  facility-services.ai, gatestoneinstitute.org, petrobras.com.br,
  breezeboxshop.com, preflight.paperpal.com, box.com, digistor.com ×2,
  firstaid4sport-news.co.uk, theartofcto.com, knotly.shop, cl.betinia.se,
  plus the q04 Exclaimer URL again). Grade: NOISE.

## Coverage gaps / notes for the coordinator

- No rate-limiting or blocking observed; the 204-without-HX-headers
  behavior is an endpoint contract change, not a block — recorded here so
  future workers don't misread 204 as "zero results".
- Endpoint-discovery probes (`probe_*.html`, `control_*.html`,
  `search_page.html`, `ua_test.html`) are cached in `../raw/` alongside the
  sweep; `search_page.html` (200, 19,896 bytes) is the live form that
  documents the working parameter set.
- Suggest the authenticated urlquery API (or a live-browser session) as the
  follow-up for any strong-negative claim about `lifeval` scans; htmx
  search cannot carry that claim.
- NOT committed or pushed, per task instructions.
