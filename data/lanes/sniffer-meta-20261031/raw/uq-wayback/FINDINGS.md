# FINDINGS — URLQUERY/WAYBACK lane, sniffer-meta-20261031

Lane: urlquery-wayback (meta-fleet follow-up to sniffer-sweep-20261031).
Date of work: 2026-10-31 (America/Chicago). Operator: BigSexyWarlock69.
No commit, no push, no Factum writes (coordinator commits). Passive reads only.
No Shodan, no POST, no login, no sessions. Package repos and Docker Hub out.
No human identity or poster handles anywhere in this lane.
Signed values, tokens, and query-string values are never written here.
Where a row carries a key-like query value, only its presence by shape is noted.

## 1. Full 98-row da.gd pull — the burst survives the full set

Query: `url.domain:da.gd date:[2025-11-01 TO 2026-10-31]`
Source: authenticated api.urlquery.net search via
`~/workspace/skills/urlquery/bin/uq.py` (Secure Vault surrogate credential).
Result: total_hits 98, saved 98, unique report IDs 98 (single page, limit 100).
Saved file: `uq-dagd-domain-FULL.json` (sanitized projection only:
report_id, date, domain, fqdn, path with query dropped, final path,
title truncated to 200 chars, tags, boolean flags).
The sweep's saved-30 file is a strict subset of this full set (30/30 IDs match).

### Month distribution, denominator 98

| Month | Rows |
|---|---|
| 2025-11 | 2 |
| 2025-12 | 1 |
| 2026-02 | 2 |
| 2026-03 | 2 |
| 2026-04 | 1 |
| 2026-05 | 53 |
| 2026-06 | 31 |
| 2026-07 | 5 |
| 2026-10 | 1 |

May + June = 84 of 98 (85.7 percent). This matches the verifier's
live re-fetch exactly (53 + 31 = 84). Verdict: the burst claim was NOT
a sampling artifact. The saved-30 sample (June 24, July 5, Oct 1, zero May
rows) was non-representative, but the underlying May–June burst is real
in the full set.

### June 21 cluster, full set

June 21, 2026 = 17 rows in the full set — identical to the saved-30 count.
All 17 June 21 rows were already inside the saved 30, so the cluster size
was never understated by sampling. June 21 composition (full set):
short code PQkCp 9 rows, oc2b0h 3, WaRKD 2, TUz9f1 1, C0y1K 1, Soa0 1.
Title-host shapes for June 21: nghttp2.org 8, httpbun.com 5, blank or
error 4. These are echo-host path shapes (base64 echo endpoints), per the
sweep report; this lane did not fetch or decode any echo endpoint.

### Largest single day is May 19, not June 21 (new in the full set)

May 19, 2026 = 19 rows, the largest single day in the full set, inside a
short window 19:08–21:48 UTC. Composition: 16 distinct short codes
(5cNOs6, rvMKH, EdhdcV each twice; 13 codes once). Title-host shapes:
unctadstat-api.unctad.org 14, httpbin.org 2, blank or error 3.
Final domains: unctad.org 14, httpbin.org 3, example.com 2.
The May burst as a whole (53 rows, May 3–31) leans the same way:
title-host unctadstat-api.unctad.org 22 of 53, blank or error 22,
jqp.vercel.app 4, httpbin.org 2, plus one each vizhub.healthdata.org,
docs.google.com, mrgt-arab.blogspot.com.

### Short-code reuse, full set

70 distinct path tails across 98 rows (path = da.gd/<code>, query dropped).
One tail is the bare da.gd root path itself (2 rows), leaving 69 true
short codes. 15 tails repeat, covering 43 rows: PQkCp 9, iar2 4, sDC92O 4,
oc2b0h 3, Syqbry 3, and WaRKD, Soa0, Di7Cu, EuIYhZ, bIhl5, WNFDN+, 5cNOs6,
rvMKH, EdhdcV, plus the bare root, each 2. The other 55 codes appear once.
Reuse is concentrated in the June 21 cluster (PQkCp) and the May burst,
not spread evenly across the window.

### zz / oai flags, full set

zz-flagged rows: 0 of 98. oai-flagged rows: 0 of 98.
Flags test the submitted URL, final URL, and tags for `zz=` and for
`oai-` / `oai_` (query values dropped before flagging, presence only).
63 of 98 rows carry a query string on the submitted or final URL
(presence only, values never saved), so the zero zz/oai result is a
statement about those two token shapes, not about query strings in general.
The da.gd family stays separate from the oai/zz family, as the sweep held.
Grade: SECONDARY pattern shape only. No behavior verified.

### Title-host shapes, full set (destination-host prefix of the title)

unctadstat-api.unctad.org 23, nghttp2.org 8, jqp.vercel.app 6,
httpbun.com 5, httpbin.org 2, MixDrop 2, and one each
vizhub.healthdata.org, docs.google.com, mrgt-arab.blogspot.com,
Google, keojbm.datiinghype.com, v0a.cc; blank or error titles 46
(including 11 "Problem loading page"). Final domains mirror this shape:
unctad.org 23, nghttp2.org 8, jqp.vercel.app 6, httpbun.com 5,
example.com 4, httpbin.org 3, plus a long tail of singletons.
Decode of any echo payload belongs to the cryptologist lane; not done here.

## 2. zz flagged-row hunt — resolved, field artifact of a redirect

The sweep's `uq-odd-zz-param-agent-conj.json` (query `zz= agent`,
total_hits 68265 at sweep time) carries exactly 1 flagged row in its
saved 30: report dated 2026-10-31T14:10:46Z, submitted domain
truedating.life, submitted path root (`/`), tags empty.
The sweep's `uq-odd-zz-param.json` (query `zz=`, total 2,593,629)
carries 0 flagged rows in its saved 30, and `uq-odd-uqtag-oai.json`
is a genuine zero (total_hits 0).

Targeted re-fetch of that one report (transient read, nothing raw saved)
shows the flag comes from the FINAL (redirect landing) URL, not the
submitted URL: the submitted URL has no query string and no `zz=`;
the final landing URL carries a query string that includes a `zz=`
parameter (value withheld, presence by shape only); tags are empty.
Verdict: the count of 1 is a redirect-landing tracking-parameter
artifact, not a submitted zz marker and not agent evidence on its face.
The row's submitted domain is a dating landing page; no agent link is
claimed, and no further inference is drawn from it.

Corroborating churn: a fresh re-run of the same `zz= agent` query
returns total_hits 68260 (5 fewer than at sweep time) and 0 flagged
rows in its new top 30 — the flagged row has rotated out of the top 30.
The file-level count of 1 stands as a snapshot of the sweep-time page,
explained above. The plain `zz=` search matching page content (not only
URLs) explains why its saved 30 can show 0 URL-flagged rows despite a
2.59M total: the search term lives in page content for most hits.

## 3. Bounded T/Z probe — untestable at this scope, stopped

Bounded forms only; no standalone "T/Z" search was run.
Hacker News Algolia (public API, passive GET):
- `"T/Z" agent`: 4 hits, 0 containing the literal string `T/Z` in
  title or text.
- `"T/Z" harness`: 1 hit, 0 literal.
- `"T/Z" model`: 7 hits, 0 literal.
All returned hits are Algolia token-stemming matches, not literal hits.
urlquery (same date window):
- `"T/Z" agent`: total_hits 20996; top domains are generic recent
  landing and spam-shaped domains.
- `"T/Z" harness`: total_hits 20070; top domains likewise generic.
Saved probe file: `tz-bounded-probe.json` (counts and top domains only).
Verdict: pure generic noise at the bounded forms tested. Recorded as
untestable for a callsign claim and stopped; no callsign claim is made.
This matches the tango-zulu lane's caveat that no standalone "T/Z"
search was run because the term is too generic.

## 4. Wayback CDX retry — one retry round, mixed result

Method: `http://web.archive.org/cdx/search/cdx` (port 80, per TOOLS.md),
one attempt per query, no further retries.
- Domain query (`url=da.gd`, matchType=domain, from=20251101, limit=50,
  collapse=urlkey): HTTP 200, 50 rows returned. Saved sanitized as
  `cdx-dagd-domain-RETRY.json` (path with query dropped + flags).
  Rows: 47 status 302 (shortener redirects), 2 status 404, 1 status 200.
  zz-flagged 0, oai-flagged 0 (URL strings only; CDX cannot match content).
  Month slice of these 50 rows: 2026-10: 20, 2026-04: 17, 2025-11: 2,
  2025-12: 2, 2026-01: 2, 2026-03: 2, 2026-02: 1, 2026-05: 2,
  2026-07: 1, 2026-09: 1. This slice is urlkey-ordered and capped at
  50 by the query, NOT a time-ordered census: it neither corroborates
  nor contradicts the urlquery May–June burst, and must not be cited
  as a burst distribution. One path shape noted without inference:
  a `/.git/HEAD` capture dated July 2026 returning 404.
- zz-filter query (same, plus `filter=original:.*zz=.*`): HTTP 504
  Gateway Time-out, empty of rows. Recorded as flaky; no further retry
  was attempted, per the one-retry instruction.

So the sweep's CDX failure is partly retired (the domain query now
succeeds) and partly still open (the zz-filter query still fails).
CDX adds no zz or oai URL evidence for da.gd.

## Open questions

1. May 19 (19 rows, 2.6-hour window, unctad-shaped destinations) is the
   largest single-day spike in the full set; whether it shares a submitter
   or mechanism with the June 21 echo cluster is for the coordinator or
   cryptologist lane, not this lane (no echo fetches, no decodes here).
2. The CDX zz-filter query remains unanswered (504 on the single retry);
   a later retry on a fresh day may succeed, but it is not needed to
   settle the urlquery burst, which is already settled by the full set.
3. urlquery totals drift between runs (zz+agent 68265 → 68260); counts
   in this report are snapshots at retrieval time, 2026-10-31.

## Files in this lane

All under `data/lanes/sniffer-meta-20261031/raw/uq-wayback/`:
- `uq-dagd-domain-FULL.json` — full 98-row sanitized pull.
- `pull_dagd_full.py` — the paging pull script.
- `cdx-dagd-domain-RETRY.json` — CDX domain retry, 50 sanitized rows.
- `cdx-dagd-zz-filter-RETRY.json` — placeholder note (zz-filter 504;
  file records the failure, rows empty).
- `tz-bounded-probe.json` — bounded T/Z probe counts.
- `FINDINGS.md` (this file), `STATE.md`, `.PROVENANCE.txt`, `.sha256`
  sidecars per file.
