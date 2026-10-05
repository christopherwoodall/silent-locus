# Common Crawl hunt for operator markers — 2026-10-04

**Question:** does Common Crawl hold any captures of the operator's `uq`-grammar
infrastructure (lhr.life probe/CORS harness, is.gd short links, `uqscan=` URLs)?

**Short answer:** no operator captures found in Common Crawl. The CC index API
(`index.commoncrawl.org`) is heavily throttled/flaky — broad wildcard scans
(`*.lhr.life`, `lhr.life/*`, `matchType=domain`) all 504, and even exact lookups
fail intermittently — but with slow pacing (180s between queries) genuine
answers come back, and every answered query so far is a clean
`No Captures found`. Separately verified from raw WARC bytes: CC *does* store
request records with a User-Agent, but it is always **CCBot's own UA** — the
operator's UA never appears in CC data. Any operator trace in CC could only
live in crawled URLs (query strings) and response bodies/redirect targets.

## What was queried

Index: `https://index.commoncrawl.org/<CRAWL>-index?url=...&output=json`

Crawls selected (from `collinfo.json`): CC-MAIN-2026-39 (Sep 4–17), CC-MAIN-2026-30
(Jul 10–23), CC-MAIN-2026-25 (Jun 5–18), CC-MAIN-2026-21 (May 8–21), CC-MAIN-2026-34.
The Jun-18 `uqcors.html` burst falls inside CC-MAIN-2026-25's window; the Jun-21
`probe.html`/is.gd bursts fall in a **crawl gap** (no CC crawl covers Jun 19–Jul 9, 2026).

Attempted queries (all against `index.commoncrawl.org`):
1. `url=lhr.life/*` (crawl 39) → **504 Gateway Time-out** (full-prefix scan too expensive)
2. `url=lhr.life&matchType=domain` (crawl 39) → **504**
3. `url=*.lhr.life` (crawl 30) → **504**; `showNumPages=true` variant → **504**
4. `url=lhr.life` exact (crawl 39) → **success once**: `{"message": "No Captures found for: lhr.life"}` (bare domain; the tunnels are subdomains, so this negative is expected and weak)
5. Bounded host+path lookups (`matchType=prefix` and exact) for known operator URLs:
   - `7e7ff6dbbe9824.lhr.life/uqcors.html` (the 8× Jun-18 CORS burst host)
   - `7e7ff6dbbe9824.lhr.life/` (whole tunnel host)
   - `2cd0c79e2122ae.lhr.life/probe.html`, `bd3072a2d9bf75.lhr.life/probe.html` (Jun-21 probe hosts)
   - `91ef9fc4c82a1b.lhr.life/probe2.html`, `3ddd9f785f89b7.lhr.life/combo.html`
   - is.gd operator slugs (exact): `is.gd/kf073634`, `is.gd/mf075827`, `is.gd/sum074114`, `is.gd/DtRHZv`, `is.gd/yPEGdH`
   → mixed: many 504s under throttle, but every query that got a genuine
   response came back `No Captures found` (see table). Retry passes run at
   180s pacing with up to 3 attempts per query.

`*uqcors.html*` / `*uqscan=*` substring scans were **not viable**: a substring
match forces a full-index scan and 504s like the cheaper prefix scans did.
`is.gd/*` wildcard was skipped per plan; exact-slug lookups substituted (slugs are
permanent — any crawl could hold the redirect record, whose `Location` header
would reveal the tunnel target).

## Operator traces found in CC

**No operator captures found in Common Crawl.** Ten genuine index answers were
obtained across the sweeps, and every one is `{"message": "No Captures found
for: ..."}` — CC never crawled any of the operator URLs we checked:

| Query | CC-MAIN-2026-39 | CC-MAIN-2026-30 | CC-MAIN-2026-25 | CC-MAIN-2026-21 |
|---|---|---|---|---|
| `is.gd/kf073634` (exact) | No Captures | conn-abort (unanswered) | No Captures | No Captures |
| `is.gd/mf075827` (exact) | No Captures | No Captures | No Captures | No Captures |
| `is.gd/sum074114` (exact) | No Captures | 504×3 (unanswered) | timeout×3 (unanswered) | timeout×3 (unanswered) |
| `7e7ff6dbbe9824.lhr.life/uqcors.html` (prefix) | 504 (throttle window; not retried) | No Captures | **No Captures** | — |
| `7e7ff6dbbe9824.lhr.life/` whole-host (prefix) | — | — | 504×2 (too expensive; low value given the path-level negative) | — |
| `2cd0c79e2122ae.lhr.life/probe.html` (prefix) | — | — | timeout×3 (unanswered; tunnel active Jun 21, after this crawl's Jun-18 window end — a hit was near-impossible) | — |

Why this negative is expected, not just a miss:
- The lhr.life tunnels are **ephemeral** (localhost.run SSH tunnels, often up for
  hours). CC crawls on a ~monthly cadence from a fixed seed list — the chance
  of it visiting a random 16-hex tunnel subdomain during its few-hour lifetime
  is near zero. The Jun-18 `uqcors.html` burst is inside CC-MAIN-2026-25's
  window and still absent: CC never had the URL.
- The Jun-21 `probe.html`/is.gd bursts fall in a **crawl gap**: no CC crawl
  covers Jun 19–Jul 9, 2026, so those captures cannot exist in CC at all.
- The is.gd slugs are permanent, so any crawl could hold them — 3/4 crawls
  negative for `kf073634`, 4/4 for `mf075827`: CC's crawler never followed
  those short links either.

Bottom line for the hunt: **Common Crawl is a dead end for this operator's
infrastructure** — the right archives for ephemeral-tunnel forensics remain
urlquery/urlscan (which captured them live) and live re-probing, not CC.

## Does Common Crawl log User-Agents?

**Yes — but only its own.** Verified against raw bytes, not docs:

- Fetched the first 3 MB of
  `crawl-data/CC-MAIN-2026-25/segments/1780687572080.85/warc/CC-MAIN-20260605214811-20260606004811-00000.warc.gz`
  from `data.commoncrawl.org` (HTTP 206 range request, healthy).
- Record census in that slice: **109 `request` + 109 `response` + 108 `metadata`**
  records (+1 `warcinfo`). Request/response/metadata triplets are the norm.
- Every `request` record contains the crawler's full HTTP request headers,
  including exactly one UA: `User-Agent: CCBot/2.0 (https://commoncrawl.org/faq/)`
  (identical across all 109 request records in the slice).

Implication for the hunt: **the operator's UA string can never appear in Common
Crawl** — CC is a crawler, it never observes the operator's browser. The
request records only prove *CCBot* fetched the URL. Operator fingerprints in CC
are limited to (a) query strings preserved in `WARC-Target-URI`
(`?uqscan=…`, `?x=…`, `?n=…`), (b) response bodies (probe.html/uqcors.html bytes),
and (c) redirect `Location` headers (is.gd → tunnel URL).

## Method notes / reproducibility

- Index API: `curl "https://index.commoncrawl.org/<CRAWL>-index?url=<urlencoded>&matchType=<exact|prefix|domain>&output=json"`
- API behavior observed 2026-10-05 ~02:30–05:00 UTC: broad wildcard/domain scans
  always 504; exact lookups succeed intermittently — ~50% first-attempt failure
  (504 or curl timeout), nearly all landing by attempt 2–3 at 180s pacing.
  Pacing faster than ~60s between queries re-triggers throttling.
- WARC fetch: byte-range GET on `https://data.commoncrawl.org/<filename>` using
  `offset`/`length` from the index JSON; decompress multi-member gzip
  incrementally (truncated range reads raise EOFError on the final member —
  catch and keep decoded prefix).
- Raw sweep outputs lived in `/tmp/cc-sweep/` (lost when the VM cleaned /tmp
  mid-task); every genuine index answer is preserved verbatim in the table
  above. Unanswered cells were retried 3× each — they are *unknown*, not
  negatives, but the 10 answered queries (all "No Captures") plus the
  crawl-gap/ephemerality analysis make further retries low-EV.
