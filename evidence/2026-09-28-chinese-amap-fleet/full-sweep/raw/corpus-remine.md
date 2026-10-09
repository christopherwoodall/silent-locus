# Corpus re-mine: submitter-metadata clustering of the Chinese Amap fleet corpus

**Corpus:** `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/`
**Date run:** 2026-10-04/05 (UTC) · **Scope:** 2,159 unique urlquery reports across `raw/` (pages 000–019, gaode, infra/*, pivots/*, single report_*.json) + `events.jsonl` (2,141 normalized records)
**Method:** cluster by SUBMITTER metadata only — `settings.useragent`, `settings.exit_node`, tag-grammar from submitted URL, submission timestamp, target host. Per hunt doctrine: metadata tells the story; off-frame findings are leads, never negatives.
**Caveat:** urlquery's public schema has NO submitter-IP field — the `ip`/`asn` block is the *target's* resolved IP (e.g. DigitalOcean = httpbun target, Ali = Amap target). So ASN/country diversity here is target-side, not submitter-side. True submitter-side fields are only `useragent`, `device_type` (invariant: all `desktop`), `exit_node`, `referer`, date, URL.

## 0. Integration check — CLEAN NEGATIVE

- Unique reports in `raw/`: **2,159**. Unique `report_id` in `events.jsonl`: **2,141**. Gap: **0** — every raw report is integrated, and every integrated ID exists in raw. (18-report difference = `iter_reports` double-counts; both dedup to the same 2,141. No orphan files.)
- The two empty files `raw/lanes/wayback/cdx_*.json` are corrupt/empty Wayback CDX dumps, not report-bearing — no report IDs lost there.
- `ALL_LINKS.md` lists 2,673 unique report IDs; 698 are NOT in `raw/`. **Those are 2025-10 (Oct 2025) background reports** (informa/eloqua marketing emails, darkreading, nikse.dk, etc.) — a year-old unrelated stratum swept into the links list, not fleet activity. Zero fleet-relevant IDs missing.

## 1. Submitter-side fingerprint: ONE pipeline

- **`settings.exit_node`: only 2 values across 2,159 reports.**
  - `qguvgzjxzsgb3vs`: 2,130 reports (all 18 UAs, all grammars, all hosts, 2026-09-29 → 2026-10-05).
  - `31pu2ilhjrkmwpf`: 29 reports, details below.
- **`settings.useragent`: 19 distinct values (task brief said 18 — recount below).** 98.2% are the urlquery Firefox default `Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0`.
- **`settings.device_type`: invariant `desktop` (2,159/2,159)** — even on `m.amap.com` mobile pages and Android UAs. The submitter never touches the device-type field.

### The 19 UAs (amap.com query slice, n=1,970)

| # | UA | grammar/host fit | verdict |
|---|---|---|---|
| 1,931 | Firefox/134.0 (urlquery default) | all grammars, all amap hosts, all days | main fleet |
| 15 | `Chrome/140.0.0.0` Win64 (no version subfields on most) | 10× uqscan + 5× untagged, www/m/amap, 2026-10-04 04:34–20:57 | operator UA-variant R&D (interleaved with main fleet; `uqscan=fjmuseum-alt31-20261004` also on exit_node B — see §3) |
| 4 | Android 14 Pixel 8 Pro Chrome/140 | untagged m.amap.com | R&D |
| 3 | UA = `0` | uqscan=pandalegacy*, uqscan=claude20261004mochou | operator UA-spoof R&D (known `pandalegacy` family) |
| 2 | Android 13 Pixel 7 Chrome/120 | uqscan | R&D |
| 2 | X11 Linux Chrome/121 | uqresearch=mobilechrome20261004 / desktopchrome20261004 | R&D |
| 2 | Chrome/120 Win64 | uqfresh | R&D |
| 1 | Android 14 Pixel 8 Pro Chrome/126 | uqscan | R&D |
| 1 | Android 15 Pixel 9 Pro Chrome/140 | untagged m.amap.com | R&D |
| 1 | `Mozilla/5.0` (bare) | uqscan, amap-pc-ssr | R&D |
| 1 | Android 13 Pixel 7 Chrome/120 (no patch) | — | R&D |
| 1 | Android 14 Pixel 8 Pro Build/AP1A Chrome/130.0.6723.58 | uqmobilefull=1791101300 | R&D (mobile-full probe, paired with MAIN-UA uqmobile probe same POI 16 min earlier) |
| 1 | `mobile` (literal) | untagged m.amap.com | R&D |
| 1 | Googlebot/2.1 | `x=uqcustomua20261004` on www.amap.com | operator custom-UA test (known `customua` family) |
| 1 | `desktop` (literal) | uqscan, amap-pc-ssr | R&D |
| 1 | Edge/140 Win64 | uqscan | R&D |
| 1 | Android 15 Pixel 9 Pro Build/AP4A Chrome/140 | untagged amap-pc-ssr | R&D |

**UA verdict: no second fleet by UA.** Every exotic UA sits on the same exit node, same amap hosts, same tag grammar family, interleaved in the same hours as the main fleet. The exotic values (`0`, `mobile`, `desktop`, bare `Mozilla/5.0`, Googlebot) are deliberate spoof experiments — the known UA-test R&D lane (pandalegacy/customua/mochou/taersi-mobile-ua), not an independent operator. A genuinely separate fleet would need its own exit node / grammar / timing shape; none exists.

## 2. Tag-grammar clustering

Known grammar was `uqscan=<word><date>[a-z]`. The corpus actually contains **36 distinct `uq*` param names**. All 35 exotic grammars map to the MAIN UA + exit node A (single operator experimenting), with 4 records on variant UAs:

- **`uqresearch=` (41):** epoch-sec values (e.g. `1790812500`) AND word values (`mobileproper20261004`, `claude20261004xzs1`, `hzoo-*-20261004`, `target20261004`). Earliest 2026-09-30, bulk 2026-10-04 05:07–17:40. Paired `...600/601` nonce pairs on the same POI across hosts (www + ssr + api) = operator's host-coverage R&D.
- **`uqtarget=` (19):** same operator, denser word grammar (`laoshan20261004a`, `pd-www-<uuid>`, `direct-<uuid>`, `cookie-test-17558273-<uuid>`, `mobileapi1791103668`). 2026-10-04 05:07–11:36 burst, one POI family (B021407PX0) swept across www/ditu/ssr/api hosts with per-host nonce tags — host-coverage mapping experiment.
- **`uqtag=` (6, all httpbin.org/base64/):** the `ltzh` R&D cluster — base64-embedded HTML payloads that (a) fetch `r.jina.ai` POST + JSON-cache probes and (b) iframe-embed amap SSR pages, exfiltrating via Image beacons to `/status/204?uqtag=<tag>&part=N&data=<b64>`. Tag names: `ltzh-jina-post-inject-20261004a`, `ltzh-jina-json-cache7d-20261004{a,b}`, `ltzh-iframe-ssr-20261004a`, `ltzh-iframe-www-20261004a`, `ltzh-iframe-ssr-big-20261004a`. 2026-10-04 12:58–13:15, MAIN UA, exit node A. **This is the operator's jina-laundering R&D lane** — same launcher tradecraft as the collusion-wiki corpus (jina relay), now tested through urlquery submissions. NOT a second fleet (same exit node, same UA).
- **`uqmobile=` (5):** epoch+letter nonces on m.amap.com mapview/detail, paired a/b/c triples on one POI (B001C80821, 2026-10-04 17:44). Operator R&D.
- **`uqmobilefull=` (1):** the Android-UA mobile-full probe (see UA table).
- **`uqfresh=` / `uqtop=` / `uqdirect=` / `uqretry=` / `uqhost=` / `uqrun=` / `uqprobe=` / `uqp
...[truncated 10840 chars]d=` / `uqhs=` / `uqstatus=` / `uqinteractive=` / `uqasset=` / `uqstatic=` / `uqroute=` / `uqmicro=` / `uqlive=` / `uqsource=` / `uqstack=` / `uqquery=` / `uqpd=` / `uqpd2=` / `uqd=` / `uqd2=` / `uqproxy=` / `uqlegacy=` / `uqowner=` / `uqts=` / `uqfirstparty=` / `uqtop=` / `uqopts20261004a=` (1 each or small n):** one-off experiment names on Amap POI/API/static-asset URLs, all MAIN UA + exit node A, 2026-10-04 daytime. Including `uqasset=`/`uqstatic=` on `ssr-next.amap.com/_next/static/chunks/webpack-…` (static-asset probing) and `uqfirstparty=1790860710282` with `source=research` (2026-10-01). Same operator's R&D sprawl.
- **`uqtag=` on non-httpbin (0 in corpus)** — the 6 corpus hits are all httpbin.org/base64; see §5 for unseen extension.
- **UUID-shaped `uqscan=` values (14 records, 2026-10-04 04:15–10:01, all POI B035300ESE):** per-request nonces on `service/poiInfo` / `detail/get/detail` / `getPoiInfo` endpoints, incl. `#:~:text=` fragments and `callback=foo` JSONP. One record on Chrome/140 UA. Operator endpoint-behavior probing — nonce-per-request, not a separate fleet.

**Grammar verdict: no second fleet by grammar.** The 36-way split is one operator's experiment sprawl, all anchored on the same UA + exit node + Amap targets.

## 3. Exit-node clustering: the 29-record B cluster (lead)

`31pu2ilhjrkmwpf` (29 records) vs `qguvgzjxzsgb3vs` (2,130):
- 23×: **2026-09-28 20:57–21:32** — the corpus's earliest records, all untagged `amap-pc-ssr.amap.com/ssr/place/B000A7O1CU`, MAIN UA. Reads as the operator's first session (different submission account/key, then migrated to exit node A for the rest of the campaign).
- `uqscan=exit31` (2026-09-30T02:33, MAIN UA) — the operator literally named the node in the tag. **This confirms the operator knows about and tests both exit nodes.**
- `?uq=exit` + `?uq=ua` pair (2026-10-04 10:28, same POI B03DF05V64, one MAIN UA + one Chrome/140 UA) — deliberate exit/UA matrix probe.
- `?oldnodeprobe=1791119665` (2026-10-04 13:15, MAIN UA).
- `uqscan=fjmuseum-alt31-20261004` (2026-10-04 14:41, **Chrome/140 UA** — the same variant UA as the 15-record cluster in §1).
- 1× httpbun.com/base64 (2026-10-04 14:35, MAIN UA) — base64 probe via node B.

Verdict: **same operator, second submission identity** (node-named tags `exit31`, `oldnodeprobe`, `?uq=exit` prove operator awareness). Not a second fleet — but worth a dedicated htmx pull of `exit31`/`oldnodeprobe` markers (done in §5: zero unseen reports, corpus complete).

## 4. Burst analysis: no unexplained bursts

Hour grid for 2026-10-04 (top): T10=183, T11=164, T13=154, T05=152, T06=140, T12=136, T08=128, T04=110, T07=107, then a long tail T17=72 → T00=32. Every hour is a `uqscan`+`untagged` mix with the exotic-grammar R&D sprinkled through 05:00–17:56. No hour is dominated by a grammar/UA/host combo that doesn't appear elsewhere. The pre-10-04 days are sparse (09-28: 23, 09-29: 3, 09-30: 110+, 10-01: 52) — ramp-up, not a parallel fleet. **CLEAN NEGATIVE on unexplained bursts.**

## 5. Doctrine application: keyless htmx expansion of singleton markers

Per the no-API-key doctrine, queried urlquery's undocumented htmx endpoint (see §7) for every singleton/exotic marker: `ltzh`, `uqtag`, `oldnodeprobe`, `exit31`, `fjmuseum-alt31`, `uqmobilefull`, `uqfirstparty`, `uqdirect`.
- `oldnodeprobe`, `exit31`, `fjmuseum-alt31`, `uqmobilefull`, `uqfirstparty`: **1 hit each, all already in-corpus** — corpus is complete for these markers.
- `uqdirect`: 5 hits, all in-corpus.
- `uqtag`: **24 unique hits, 9 NEW vs corpus** —
  - **4× httpbun.com/base64, 2026-06-20 12:52–13:02** — base64 payloads embedding a Tableau module from `vizprod.aihw.gov.au` (Australian Institute of Health and Welfare, .gov.au) with **`uqtag=AGEDATA23`**. Same base64-probe + uqtag-marker tradecraft as the in-corpus ltzh R&D, but 3.5 months earlier and against an Australian government target. Report IDs: `fbda6df4-8a64-4372-b410-31e63c23154e`, `9188235a-4159-416e-bddf-0dd464991163`, `1fd1c390-e00c-456b-84f5-1851da2da83e`, `81dc5646-5c8c-4e78-b019-66943b754280`.
  - **2× httpbin.org/base64, 2026-09-01 (`probe2-start`) and 2026-10-04 10:25/10:37 (`probe2-start`, `qjprobe-start`)** — same XOR-obfuscated `b(tag,data)` Image-beacon exfil skeleton as the ltzh payloads (`/status/204?uqtag=<tag>&part=N&data=<b64>`). The 10-04 pair lands inside the fleet's operational day, ~2.5h before the ltzh burst. Report IDs: `2d8361e9-63e9-4f3b-a39f-46defcefaa82`, `271fa985-0317-4396-98a0-dac9cd5080cb`.
  - 3× spam noise (casino/vimeo bare domains — `q` matches beyond visible URL; not operator grammar).
- `ltzh`: 18 unique hits — our 6 in-corpus + **6 casino domains at the exact ltzh burst minutes** (2026-10-04 12:58/13:08/13:15: `star-vegas.it`, `cinevo.nl`, `casibom90998.com`, `flrdrop.vip`, `juntanacional.co`, `jojobet-resmi-gir.vip`) + an Aug–Sep jojobet spam stratum. Submitted URLs are bare domains (no uqtag/grammar markers); the public report page exposes no `settings` (no UA/exit_node), and `q` demonstrably matches beyond the visible URL. **Attribution unresolvable keylessly — flagged as an open lead, not claimed.**
- Submitter-metadata check on the 9 NEW uqtag hits: **not possible without the keyed API** (public report pages render summaries only; `main.js` exposes no settings-bearing endpoint). Technique continuity (base64-embedded HTML probes + `uqtag=` markers + httpbun/httpbin echo services + Image-beacon exfil) is the attribution basis, stated as lead-grade.

## 6. Verdicts

| Candidate | Verdict |
|---|---|
| Integration gaps in `raw/` | **CLEAN NEGATIVE** — 0 missing report IDs either direction; only empty/corrupt CDX files |
| Second fleet by UA | **CLEAN NEGATIVE** — 19 UAs, all on one exit node, one grammar family, interleaved timing |
| Second fleet by grammar | **CLEAN NEGATIVE** — 36 `uq*` param names, all attributable to one operator's R&D (incl. ltzh/uqtag jina-laundering lane) |
| Second fleet by timing | **CLEAN NEGATIVE** — no unexplained bursts; 10-04 is one continuous operational day |
| Exit-node-B cluster | **LEAD, likely same operator** — one same-day Chrome-140 museum record + 3 node-probe markers; htmx shows zero unseen reports |
| UUID-shaped `uqscan=` nonces | **KNOWN operator behavior** — per-request nonces on endpoint-behavior probes (text-fragment, JSONP, API) |
| `ltzh`/`uqtag` base64-probe family beyond corpus | **LEAD — 9 unseen reports**: June 2026 AIHW (.gov.au Tableau, `uqtag=AGEDATA23`) strand + 2026-09-01 / 2026-10-04 `probe2-start`/`qjprobe-start` siblings. Same tradecraft as in-corpus ltzh R&D; submitter attribution needs API-key settings access |
| `q=ltzh` casino-spam hits | **OPEN** — 6 casino domains at the exact ltzh burst minutes vs longstanding Aug–Sep jojobet spam stratum. Bare-domain URLs, no grammar markers; public pages expose no submitter metadata. Do not attribute on timing alone |

**Bottom line: the corpus contains ONE operator with a large, metadata-visible R&D surface — not two fleets.** The prize-grade finding is negative on the second-fleet hypothesis, but the re-mine paid off elsewhere: (a) the previously uncatalogued `ltzh`/`uqtag` jina-laundering R&D lane inside our own corpus, and (b) its unseen extension — a June 2026 Australian-government (AIHW Tableau) probe strand using identical tradecraft.

## 7. Undocumented endpoints found (doctrine: document for reuse)

All verified live 2026-10-05, no auth, found via reading page source + `/static/javascript/main.js`.

1. **`GET https://urlquery.net/api/htmx/search/?q=<query>&limit=<n>&offset=<n>`**
   - Headers: `HX-Request: true`, `Accept: text/html`, `HX-Current-URL: https://urlquery.net/search?q=<query>`, normal browser UA.
   - Returns HTML table rows; parse `href="/report/<uuid>"` + anchor text (submitted URL) + `YYYY-MM-DD HH:MM` dates in row order.
   - Rate behavior: ~60s stalls under burst use (python urllib timed out); curl `-m 90` + ≥8s spacing worked.
   - Wrapper: `~/workspace/skills/urlquery/bin/uq_htmx.py` (existing; `search --query --limit --offset --delay`).
   - Caveat: `q` keyword-matches beyond the visible submitted URL (tags/detections) — verify hits by URL content before attributing.
2. **`GET https://urlquery.net/report/<uuid>`** (public report page) — server-rendered summary only; exposes NO `settings` (no UA/exit_node/referer). Full submitter metadata requires the keyed API.
3. **`GET https://urlquery.net/static/javascript/main.js?v=<hash>`** — frontend bundle; contains no additional `/api/` routes beyond the htmx search (checked 2026-10-05).
