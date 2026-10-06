# htmx keyless sweep — `lhr.life` subdomain census + AGE-sequence gap hunt (Lane B)

**Date run:** 2026-10-05 ~07:53–08:03 UTC (12:53–13:03 CDT) · **Method:** keyless curl against
`https://urlquery.net/api/htmx/search/` (same endpoint/protocol as the prior lanes).
Headers: `HX-Request: true`, `Accept: text/html`,
`HX-Current-URL: https://urlquery.net/search?q=<q>`, browser UA. **≥13s pacing,
zero HTTP 429/403 on any of 34 calls.** Python urllib not used (dies in the proxy
CONNECT tunnel — TOOLS.md). Raw HTML per page archived in `/tmp/htmx_sublife/raw/`
(scratch; parsed during analysis). Script: `/tmp/htmx_sublife/sweep.sh`.

**Queries run (34 total):**
- `lhr.life` — 11 pages (limit=24, offsets 0–240, stopped at page cap, never hit an empty page)
- `lhr` — 3 pages (limit=24, offsets 0–48)
- `uqtag` — offsets 0/50/100 with limit=50 (off0: 48 rows, off50: 3 rows, off100: empty — full window)
- Missing-sequence probes (8): `AGEMARK1`, `AGEMARK2`, `AGE6`, `AGE1`, `AGE2`, `uqtag=AGE6`, `AGEHOVER6`, `AGEDIALOG6`
- Fleet-grammar markers (9): `uqcors`, `sub_poi_navi`, `uqmobile`, `uqfresh`, `uqresearch`, `uqtarget`, `ltzh`, `pandalegacy`, `uqcors.html`

## 1. `lhr.life` subdomain census

- **243 unique report IDs** across the 11 `lhr.life` pages (date range in index: 2025-10-20 → 2026-09-05).
- **216 distinct `<hex>.lhr.life` subdomains** extracted from submitted URLs.
- Diff vs the authoritative 78-name fleet list from `writeup-lhr-life.md` (all observed lhr.life reports):
  - **75 of 78 overlap** — the three known-fleet names NOT in the index window:
    `5ede92286ebdfd.lhr.life`, `9d949288a99648.lhr.life`, `a2999080cb0525.lhr.life`
    (index is a partial recent-weighted view; absence from the index ≠ absence from urlquery).
  - **141 names NOT in the known 78.** Classification by date:
    - **137 are pre-2026 background noise** (2024-02 → 2025-12). localhost.run is public infra — these are years of unrelated users' tunnels showing up in the same search index. Not operator leads.
    - **4 are January-2026 tunnels (operator-window timing, unattributable keylessly)** — all bare-root URLs with no uq-grammar or marker tags:

| report ID | index date | subdomain |
|---|---|---|
| `ce2a4b53-46df-4b8b-8b22-d83829081f11` | 2026-01-04 08:59 | `30b7f1be8684bc.lhr.life/` |
| `c8462fbe-1c5b-4853-b6c9-4037a1137f19` | 2026-01-05 02:50 | `cbfbac296bddb2.lhr.life/` |
| `d4dfbf08-7084-4fad-97c0-9b3f0653623f` | 2026-01-05 02:54 | `47ff7b732b053f.lhr.life/` |
| `3b8a6908-ecd0-400e-8765-f1a2b01f3ea5` | 2026-01-05 02:56 | `838e63e8009d67.lhr.life/` |

The known 78 includes 24 January-2026 names (operator's documented lhr.life onset), so these
4 fall squarely in the operator's early-probing window. But with bare roots and no submitter
metadata on the public pages, they are indistinguishable from background localhost.run use —
**candidate leads, not claims**. None appear in the corpus (`events.jsonl`/`raw/`).

- **Cross-set diffs:**
  - ZeroSSL CertSpotter set (10 names: `efa9eb3bda1df5`, `967f1af7dfd915`, `a7bfa19dd56391`, `ca990e9a89525d`, `deab0fff603d04`, `0418f1e395a48e`, `92f1f5cd378431`, `93ca25e80716ce`, `1338981620088f`, `4fee6c798907e5`): **0 overlap** with the 216 index names — none were ever submitted to urlquery.
  - urlscan tronzap set (10 names incl. tag `87270ca9ac10`): **0 overlap** — none in the urlquery index either.
- `lhr` (tokenized fallback) verdict: the bare-`lhr` query returns 69 unrelated reports (mail trackers, adobe awstrack, taimei-l1140.cc etc.) with **zero overlap** with the `lhr.life` result set — the tokenizer matches "lhr" as a substring of unrelated strings, not as a domain token. `lhr.life` (exact dotted token) is the correct index handle; `lhr` adds nothing.

## 2. AGE-sequence gap hunt — #1 RECOVERED: `AGEOUT1B`

The widest `uqtag` window htmx will give (51 rows total: 48 + 3; off100 empty) surfaced **35 distinct values** — the complete operator June-2026 AGE series **plus the missing #1**:

- **`AGEOUT1B`** — report `a2384890-2335-4988-81dd-1985eb31df5b`, index date **2026-06-20 08:39** (12 min before AGEMARK3 at 08:51), URL `httpbin.org/base64/PHN0eWxlPnByZXt3aGl0ZS1zcGFjZTpwcmUtd3JhcDtmb250OjEwcHggbW9ub3NwYWNlO3Bvc2l0aW9uOmFic29sdXRlO3otaW5kZXg6OTtiYWNrZ3JvdW5kOndoaXRlO2luc2V0OjA7b3ZlcmZsb3c6YXV0b308L3N0eWxlPjxwcmUgaWQ9b...` — same `<style>pre{...}<pre id=o>` base64 rendezvous skeleton as the rest of the series. **Not in the corpus** (`events.jsonl`/`raw/` both 0 hits). Sequence #1 confirmed as `AGEOUT1B` (the "B" = host-variant suffix, matching AGETIP12B's pattern — consistent with the operator starting on a `B` variant or numbering OUT/1 as the first iteration).
- Full series now: **28 reports, 27 distinct tags** (AGEMARK3/3S, AGEUND4, AGEMARK5, AGEDIALOG7, AGECROSS8, MOUSETEST9, AGEEXCEL10h/10p, AGEEX11, AGETIP12p/12h/12u/12B, AGEHOVER13, AGEFILTER14, AGEOPEN15, FORMTEST123, AGEOBJ18, AGEMSG19/20, AGECROSS22, AGEDATA23/24/24B, AGEVS25 — plus AGEOUT1B at 08:39 heading the run). No other AGE-family tags exist in the full index window.
- **Numbers 2 and 6 remain absent** after 8 targeted probes — `AGEMARK1`, `AGEMARK2`, `uqtag=AGE6`, `AGEHOVER6`, `AGEDIALOG6` all returned literal "No reports found"; bare `AGE1`/`AGE2`/`AGE6` returned only substring noise (jojobet casino spam, phishing pages — zero series content). This is now a *verified gap*: the tags do not exist in the urlquery search index (not the same as not existing in urlquery — but the prior lane's htmx-extended sweep already deep-paginated the June-20 strand through 27 reports; the widest `uqtag` window here confirms nothing more is indexed).
- Extended gap set (for the record): 16, 17, and 21 are also absent — FORMTEST123 occupies the 11:21 slot between AGEOPEN15 and AGEOBJ18 with a non-sequential number. #1 is now filled; the honest gap set is **2, 6, 16, 17, 21**.
- Adjacent lead (same tradecraft skeleton, different grammar): report `00f50c7d-2c3e-46f4-89ba-4eb9fbfb9a9b` (2026-03-13, `httpbin.org/base64`, tag `uqtag=filters279686`) — the `<style>#o{...}` base64 probe skeleton 3 months before the AGE series, but with a numeric `filters<digits>` tag grammar, not the AGE-family. Same harness or a different actor — lead-grade, unclaimed.
- **Index-date drift caveat:** htmx index dates for the AGE rows run ~5–20 min EARLIER than the prior sweep's dates (e.g. AGECROSS8 09:16 vs 09:23, AGEDATA23 12:32 vs 12:52, AGEMARK3 08:42 vs 08:51). The search index appears to use a first-seen/ingest timestamp distinct from the report page's displayed time. Treat htmx dates as ±20 min approximate; report-page times remain authoritative.
- Prior-sweep UUID typo (correction for FINDINGS.md): the htmx-extended table's AGEMSG19 ID `000f58ed-54fa-4a1-ab39-f116b9245775` (35 chars) is a transcription slip — the true ID is `000f58ed-54fa-4aa1-ab39-f116b9245775` (36 chars). Not a new report.

## 3. Fleet-grammar marker sweep

- **`uqtarget`: 4 NEW operator-grade reports** (all absent from `events.jsonl` and `raw/`), extending the Oct-04 R&D sprawl:
  - `40c029b5-c732-4dc9-8348-5802d2ced656` (2026-10-04 11:06): `amap-pc-ssr.amap.com./ssr/place/B021407PX0?uqtarget=dot-5a1ceb96-...` — **trailing-dot hostname test** (note `amap-pc-ssr.amap.com.` with literal trailing dot); the tag literally names it `dot-`.
  - `52f4e3e4-3cfc-437a-9364-68589dcb337c` (2026-10-04 11:10): `amap-pc-ssr.amap.com./ssr/poi_detail?id=B021407PX0&uqtarget=pd-dot-c3edf298-...` — same trailing-dot experiment on the poi_detail endpoint.
  - `7f3f95b7-b6a1-4634-80ed-5a5b100e79dd` (2026-10-04 11:36): `example.com/?uqtarget=1791135440` — epoch-nonce uqtarget on example.com (parallels the AGEOPEN15 payload that beaconed to example.com).
  - `161a0441-0b93-4010-afaa-17798a8fc636` (2026-10-04 17:38): `example.com/?uqtarget=1791135441` — same tag family 6 hours later, the day's last uqtarget print (17:38 is past the 17:40 uqresearch close).
  - The other 18 uqtarget rows are all in-corpus. New total for the uqtarget family: 19 corpus + 4 = 23 observed.
- **`uqresearch` (23 rows), `uqmobile` (11), `uqfresh` (4), `sub_poi_navi` (2), `uqcors` (7), `uqcors.html` (7):** zero new vs corpus. (uqcors shows 7 of the 8 known Jun-18 burst reports — `3167e447` drops off the window edge; window truncation, not absence.)
- **`ltzh` (23 rows):** 7 in-corpus operator probes + 16 "new" that are all the known junk stratum (jojobet spam domains, star-vegas.it, cinevo.nl, flrdrop.vip, casibom90998.com, juntanacional.co, clipzag.com) — bare domains, no grammar markers, matches the prior lane's flagged OPEN spam cluster. **Zero new operator-grade ltzh.**
- **`pandalegacy`: 0 hits again** (tokenizer blind spot confirmed a second time — 3 in-corpus reports remain invisible to the search index). Recorded as a tokenizer blind spot, not a negative.
- Full distinct-`uqtag` inventory from the wide window (35 values; 16 noise rows where `q` matched beyond the URL — casino/phishing spam): AGECROSS22, AGECROSS8, AGEDATA23, AGEDATA24, AGEDATA24B, AGEDIALOG7, AGEEX11, AGEEXCEL10h, AGEEXCEL10p, AGEFILTER14, AGEHOVER13, AGEMARK3, AGEMARK3S, AGEMARK5, AGEMSG19, AGEMSG20, AGEOBJ18, AGEOPEN15, **AGEOUT1B (new)**, AGETIP12B, AGETIP12h, AGETIP12p, AGETIP12u, AGEUND4, AGEVS25, FORMTEST123, MOUSETEST9, filters279686, + 6× ltzh-* (Oct-04 in-corpus).

## 4. Coverage / tokenizer caveats

1. The htmx search index is a partial, most-recent-weighted view: `q=lhr.life` surfaced 243 reports across ~11 months but page sizes fluctuated and pagination capped at offset 240 without hitting an empty page — **the tail may extend further than what was pulled**. The fleet window is nearly covered (75/78); the deep background tail is not exhausted.
2. htmx row dates drift ±20 min vs report-page dates (see §2); use report pages for authoritative times.
3. Bare queries on short substrings (`lhr`, `AGE1/2/6`) hit tokenizer substring noise — useful only as negative checks, never as coverage evidence.
4. `pandalegacy` remains index-invisible (tokenizer blind spot, confirmed twice).
5. Zero 429/403 across 34 curl calls at ≥13s pacing; no hard stop encountered.

## 5. Verdicts (this lane)

| Item | Result |
|---|---|
| New `.lhr.life` names in index vs known 78 | 141 raw — 137 pre-2026 background, **4 Jan-2026 candidates** (`30b7f1be8684bc`, `47ff7b732b053f`, `838e63e8009d67`, `cbfbac296bddb2`) — candidate-grade only, no uq-grammar, unresolvable keylessly |
| ZeroSSL / tronzap name sets in the index | **0 overlap** — none of those 20 names were submitted to urlquery |
| Missing AGE numbers 1, 2, 6 | **#1 = AGEOUT1B recovered** (`a2384890-...`, 2026-06-20 08:39); #2 and #6 verified absent from the index (8 probes); extended gap set: 2, 6, 16, 17, 21 |
| New fleet-grammar reports | **4 new uqtarget** (2× trailing-dot hostname R&D + 2× example.com late-day prints); zero new uqtag/uqcors/uqresearch/uqmobile/uqfresh/sub_poi_navi/ltzh |
| New corpus integration candidates | 1 (AGEOUT1B) + 4 (uqtarget) + 4 (Jan-2026 tunnels, candidate-grade) = 9 report IDs listed below |

**New report IDs for corpus integration (9):** `a2384890-2335-4988-81dd-1985eb31df5b` (AGEOUT1B), `40c029b5-c732-4dc9-8348-5802d2ced656` (dot-host R&D), `52f4e3e4-3cfc-437a-9364-68589dcb337c` (dot-host R&D), `7f3f95b7-b6a1-4634-80ed-5a5b100e79dd` (example.com uqtarget), `161a0441-0b93-4010-afaa-17798a8fc636` (example.com uqtarget), `ce2a4b53-46df-4b8b-8b22-d83829081f11`, `c8462fbe-1c5b-4853-b6c9-4037a1137f19`, `d4dfbf08-7084-4fad-97c0-9b3f0653623f`, `3b8a6908-ecd0-400e-8765-f1a2b01f3ea5` (Jan-2026 tunnels, candidate-grade).
