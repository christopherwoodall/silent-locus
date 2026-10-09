# Playbook-shaped submission sequences mined from local corpora
Apprentice persona · 2026-10-04

Method: grouped events by candidate session keys (zz=oai<digits> tag, fleet probe
tag families, POI id), sorted by @timestamp, and looked for ordered walks:
step-numbered paths, numbered tag series (a/b/c, 0..N), same-target cross-host
walks, and parameter-grid sweeps.

## Corpus A — 2026-09-28-chinese-amap-fleet (2,141 events, Sep 28–Oct 5 2026)

CAVEAT: every sequence below is built from `uqscan=` probe tags the operator
injected themselves (urlquery scans). They read as ordered *probe playbooks*,
not third-party tutorials. Confidence on "ordered procedural sequence" is
HIGH; confidence on "mirrors a public tutorial" is LOW — these are
self-generated, and are recorded here as the corpus's playbook-shaped
sequences, not as independent agent behavior.

### A1. fzmd a→h surface-coverage walk — POI B00190ANHZ, 2026-10-04 05:40:10–05:49:04Z
1. 05:40:10 amap-pc-ssr.amap.com/ssr/place/B00190ANHZ?src=uq2&uqscan=fzmd20261004b
2. 05:40:19 m.amap.com/search/mapview/poiid=B00190ANHZ&uqscan=fzmd20261004c
3. 05:40:26 www.amap.com/place/B00190ANHZ?uqscan=fzmd20261004a
4. 05:48:26 www.amap.com/place/B00190ANHZ?source=search&platform=pc&uqscan=fzmd20261004f
5. 05:48:27 www.amap.com/poi_detail?id=B00190ANHZ&source=search&uqscan=fzmd20261004d
6. 05:48:27 www.amap.com/ssr/poi_detail?id=B00190ANHZ&source=search&uqscan=fzmd20261004e
7. 05:48:57 m.amap.com/detail/index/poiid=B00190ANHZ&uqscan=fzmd20261004g
8. 05:49:04 m.amap.com/detail/index/poiid=B00190ANHZ?uqscan=fzmd20261004h
Mirrors: an 8-step surface checklist for one POI (SSR page → map view → web
page → detail variants → mobile detail), ~9 min. HIGH confidence ordered.

### A2. worldpark a→e cross-host walk — POI B000A7IKWK, 2026-10-04 06:10:19–06:15:26Z
1. 06:10:19 amap-pc-ssr.amap.com/ssr/place/B000A7IKWK?uqscan=worldpark20261004b
2. 06:10:27 amap-pc-ssr.amap.com/ssr/api/getPoiInfo?id=B000A7IKWK&uqscan=worldpark20261004c
3. 06:10:50 www.amap.com/ssr/place/B000A7IKWK?uqscan=worldpark20261004a
4. 06:15:18 www.amap.com/place/B000A7IKWK?uqscan=worldpark20261004d
5. 06:15:26 gaode.com/place/B000A7IKWK?uqscan=worldpark20261004e
Mirrors: same POI walked across 5 host surfaces in tag order (b→c→a→d→e
note: tag order ≠ time order; host order is SSR → API → www-SSR → www →
gaode). HIGH confidence ordered; MEDIUM it is a deliberate "which hosts
serve this POI" playbook.

### A3. target pipeline ssr→detail→info — POI B0G3LMF2G1, 2026-10-05 00:43:16–00:44:29Z
1. 00:43:16 amap-pc-ssr.amap.com/ssr/place/B0G3LMF2G1?uqscan=targetssr20261005a
2. 00:44:26 amap.com/ssr/api/getPoiDetail?id=B0G3LMF2G1&uqscan=targetdetail20261005c
3. 00:44:29 amap-pc-ssr.amap.com/ssr/api/getPoiInfo?id=B0G3LMF2G1&user_loc=117.2494,31.814395&uqscan=targetinfo20261005c
Mirrors: render-layer → detail API → info API escalation for one target.
HIGH confidence ordered.

### A4. numbered tag bursts (all 2026-10-04)
- claude1/2/3 — POI B0H2KRCNK0, 00:48:30–00:48:32Z: three identical
  ssr/place URLs, 1s apart (redundancy/retry check).
- claude20261004target1/2/4 — POI B000A81KK9, 07:00:16–07:00:20Z:
  ssr/place → www/place → ssr/place; note tag "3" skipped (gap = possible
  removed/failed step).
- directhost5→0 — POI B02F37TV2J, 13:41:42–13:41:57Z: descending
  countdown tags on ssr/poi-detail, ~2s steps.
- njxzgz20261004p0–p7 / s0–s7 — POI B00190BC3W, 11:43:43–11:45:42Z: two
  8-tag bursts over www.amap.com/place then /ssr/place (parallel-ish,
  seconds apart; order within burst is shuffled — looks automated, not
  manual).
Mirrors: scripted enumeration playbooks (numbered substeps). HIGH ordered
(within-burst order is tag-numbered, time order noisy).

### A5. baidu-translate pc/mobile pair — POI B0015397C9, 2026-10-04 06:20:00–06:20:05Z
1. 06:20:00 fanyi.baidu.com/transpage?query=https://ditu.amap.com/ssr/place/B0015397C9?uq=baidupc20261004&from=zh&to=en
2. 06:20:05 fanyi.baidu.com/transpage?query=https://m.amap.com/poi/detail?poiid=B0015397C9&uq=baidumobile20261004
Mirrors: a two-step "launder both form factors through Baidu Translate"
playbook. HIGH ordered, MEDIUM on intent (translation-proxy test).

### A6. direct1791108114 four-host burst — POI B0FFFPM2PK, 2026-10-04 10:02:45–10:02:47Z
ditu.amap.com/ssr/api/getPoiInfo → www.amap.com/ssr/place →
gaode.com/ssr/place → ditu.amap.com/ssr/place, all in 3s under one tag.
Mirrors: same-POI cross-host availability sweep. HIGH ordered.

## Corpus B — 2026-10-03-openai-agent-traces (589,972 events, arquivo.pt captures, Apr–Jun 2026)

### B1. CRDC Public-Data-API step workflow — 2026-06-16, incident doe-crdc
Ordered run inside 5 seconds:
1. 11:07:12 /api/v1.0/PDatStep2Sections (Survey_Year_Key=10)
2. 11:07:13 /api/v1.0/PDatStep3PDatMeasures (Survey_Year_Key=10, EntityType=State)
3. 11:07:15 /api/v1.0/Step3Modules (Survey_Year_Key=10, EntityType=State)
4. 11:07:17 /api/v1.0/Step3AnalysesTypes
Followed by an EntityType enum-fuzz sweep on PDatStep3PDatMeasures:
11:07:54 st → 11:07:56 s → 11:07:57 d → 11:07:59 n (and across the day:
State, a, st, s, d, n, School).
Mirrors: the CRDC API's documented step-ordered workflow
(Step1 search → Step2 sections → Step3 measures/modules → Step4 results;
PDatStep4Results also present, 4 rows), then trial-and-error discovery of
the EntityType enum. The endpoint names ARE the tutorial steps.
HIGH confidence ordered; MEDIUM-HIGH it mirrors the API's documented
walkthrough (API-discovery behavior, not a retry loop).

### B2. GetStateEstimation Cartesian sweep — Jun 17, incident doe-crdc (DSQA-250 cluster)
239,912 captures of civilrightsdata.ed.gov/api/v1.0/GetStateEstimation with
(Measure_Id, State_Id, survey_Year_Key): 73 distinct State_Id × 137 distinct
Measure_Id × ~11 year keys (6–10 dominant: 35,790–53,359 each; tails to 1–13).
zz=oai<digits> tagged subset = 67,376 rows (the Jun-17 DSQA-250 confirmed
traffic); untagged/param-tagged variants (zzbulk, prepnonce, nonce=abc123,
x=test*, zz=test*) = operator test rows mixed in.
Mirrors: "enumerate the entire state × measure × year data matrix" — the
deepsearchqa dsqa_250 eval playbook (each question = one cell of the grid).
HIGH confidence on sweep shape; HIGH the zz cluster is the eval run.

### B3. Negative: no cross-endpoint ordered walks via zz sessions
14,449 distinct zz=oai sessions; 466 have ≥2 URLs — ALL are incident
doe-crdc, ALL are 2–3 same-endpoint retries of GetStateEstimation seconds
apart (max session length 3). Zero sessions show an ordered multi-step URL
walk; zero show monotonic numeric-param evolution. The corpus's session
labels do not capture tutorial walks — the ordered workflows (B1, B2) are
visible only at aggregate level.

### B4. maryland-edstats per-school demographic sweep — 293,898 rows
GetMathPerformanceBarChart: 1,533 captures over 496 distinct SCHOOLID
(LEA=30 dominant); chronological order clusters per school (0050 ×6, then
0234, 0007, 0021, 0023, 0064…) with RACECODE/SEXCODE/GRADE/SPCL_SVC_KEY
parameter variation per school. Mirrors: per-school demographic cross-tab
playbook (pull the same chart across subgroup slices). MEDIUM confidence
(chron order per school is grouped but school order is not numeric).

## Prior-notes check
`collections/dork-hunt/data/` and `collections/re-hunt-patterns/` notes:
no prior "tutorial sequence" observations found (only unrelated hits, e.g. a
Transformers-Tutorials repo capture). Nothing to reconcile or contradict.
