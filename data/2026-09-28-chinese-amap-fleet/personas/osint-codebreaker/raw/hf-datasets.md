# HF-DATASETS HUNTER — working notes (2026-10-05, run 1)
Child of OSINT CODEBREAKER. Hunt: uploaded eval information on HuggingFace matching the swarm's task families.
Rule: curl only (python huggingface_hub broken on this VM — httpx2 chokes on IPv6 NO_PROXY entries; use `curl -s/-L` for all Hub HTTP calls).

## Working endpoint URL patterns (verified this run)
- Dataset search: `https://huggingface.co/api/datasets?search=<term>&limit=<n>` → JSON array; fields: id, author, tags, createdAt, lastModified, downloads, likes, description
- Model search: `https://huggingface.co/api/models?search=<term>&limit=<n>` → same shape
- Dataset metadata: `https://huggingface.co/api/datasets/<author>/<repo>` → full JSON (incl. siblings w/ filenames, description)
- Tree listing: `https://huggingface.co/api/datasets/<author>/<repo>/tree/main` (subdirs: `/tree/main/<dir>`) → JSON array {path, size}
- File download: `https://huggingface.co/datasets/<author>/<repo>/resolve/main/<path>` (+ `-L` to follow CDN redirect)
- Author enumeration: `https://huggingface.co/api/datasets?author=<user>&limit=<n>`
Notes: API responses are slow on this VM (~10-40s per call); downloads of 65MB took several minutes with retries. CJK search term `导航` returned empty body (JSON decode error) — CJK search unreliable via API; prefer pinyin/english terms.

## Search terms run (datasets)
deepsearchqa | amap | gaode | uqscan | agentic-browsing | agent-traces | AIHW | IDPH | GZHOSP | museum | hospital | poi | browsing eval | mobilegym | harmony agent | gaode map | spider amap | getpoi | sub_poi | guangzhou hospital | iowa public health | aihw | museum agent | guangzhou | 导航 (failed) | health data | public health | harmony
Model search: amap | gaode

## Findings

### F-1 (CANDIDATE, adjacent surface): Stephen3zero24/amap-2000-candidates-v1
- URL: https://huggingface.co/datasets/Stephen3zero24/amap-2000-candidates-v1
- What: "Amap 2,000 Deterministic Mock App Candidate Trajectories v1" — 2,000 candidate GUI-agent trajectories against a *synthetic* 高德 (Gaode/Amap) mock app, MobileGym-Harmony. 2 frozen chains: chain_1_route_mode (route mode views, 1,000), chain_2_nearest_compare (nearest-N select + route, 1,000). 22,667 action records, 22,836 mock screenshots (360×800).
- Created 2026-08-14, lastModified 2026-08-17, 47 downloads, 0 likes. Tags: language:zh, synthetic, gui-agent, mock-app, candidate-trajectories.
- Evidence grading: self-declared synthetic (`classification: L0_PUBLIC_SANITIZED_SYNTHETIC`, README: "不是真实高德 App 采集", "地点名称、地址、距离、价格、评分、路线和 ETA 均为 Mock App 的合成内容"). Release manifest carries pseudo-formal verification scaffolding (V4 validation level, frozen task plan, replay-summary.json).
- Marker grep on RELEASE-MANIFEST.json, metadata/frozen-task-plan.json, README.md: 0 hits for uqscan|uqtag|getPoiInfo|sub_poi_navi|B0…|gaode.|amap.com|AGEDATA23|GZHOSP|dsqa_. → NEGATIVE for swarm markers.
- Why it matters anyway: same domain (Gaode map GUI-agent eval), same time window (Aug 2026), zh language. Sibling release exists → F-2.

### F-2 (CANDIDATE, adjacent surface): Stephen3zero24/didi-4000-candidates-v1
- URL: https://huggingface.co/datasets/Stephen3zero24/didi-4000-candidates-v1
- What: 4,000 deterministic candidate trajectories from two MobileGym-Harmony Didi Mock App batches (2026-08-13 / 2026-08-17); 66,331 action rows + screenshots. Same author, same "candidates-v1" release pattern, tag `mobilegym-harmony`.
- Created 2026-08-18, 27 downloads. README explicitly synthetic ("not real Didi collection").
- Marker grep on README.md: 0 hits. → NEGATIVE for swarm markers; notes the publisher's mock-app batch pattern.

### F-3 (NEGATIVE): TC130/amap_mcp
- URL: https://huggingface.co/datasets/TC130/amap_mcp (2025-11-12, 34 downloads)
- What: `amap_answer_full.jsonl` (65.4MB) — function-calling dataset wrapping Amap MCP direction/driving/transit APIs (`maps_direction_driving_by_coordinates`, `maps_direction_transit_integrated_by_coordinates`, ...). Tool-use schema data, not collection traces.
- Full-file grep: 0 hits for uqscan|uqtag|AGEDATA23|GZHOSP|getPoiInfo|sub_poi_navi|dsqa_, 0 `chatgpt.com` refs, 0 B0-prefixed place IDs, 0 poi_info/poiid/place_id fields.
- Note for reuse: endpoint + grep recipe works on 65MB files fine.

### F-4 (NEGATIVE): MobileGym ecosystem rollouts
- `Ma-Vector/MobileGym-ConAct-Trajectories` (2026-07-15): successful mobile GUI-agent rollouts in the MobileGym *simulator* (MemGUI-Agent, arxiv:2606.19926 / arxiv:2605.26114) — simulator, not real apps.
- `gray311/mobilegym-trajectories-qwen3vl4b`, `gray311/mobilegym-trajectories-autoglm-phone-9b` (2026-06-08), `HaoranLiu/DPO-Qwen3-MobileGym` (2026-08-04), `MKHhhd/mobilegym-app-assets` (2026-09-01), `yorkkk2/hmp-mobilegym` (2026-09-07, nearly empty metadata).
- The Amap/DiDi mock-app datasets above sit in this ecosystem (MobileGym-Harmony), which is the GUI-agent-eval neighbor of our swarm's *real-app* Amap collection. Worth knowing the ecosystem, but none show swarm fingerprints.

### F-5 (NEGATIVE): "amap" model false positives
- `wangmingxinthu/amap_spiderwam_ckpt` (2026-06-16): robotics action-model checkpoints (LIBERO `libero_dino_s_…`, `aihub_2026…` runs) — "AMAP" here is not 高德/Amap maps. False positive.
- Others: AmapVoice/PilotTTS (TTS), jcandane/AMAP, sparsetrace/amap2nanochat — all unrelated to Gaode maps.
- `gaodean/openwebtext-jina` (dataset hit for "gaode") and `gaodean/stablehair_mirror` (model hit): usernames containing "gaode", unrelated content.

### F-6 (NEGATIVE): health/hospital/AIHW/IDPH/GZHOSP
- "AIHW" → only aagoluoglu/mg5879/branmkim `AI_HW*` computer-vision homework datasets (COCO detections). 0 relevance to Australian Institute of Health and Welfare.
- "IDPH" → 0 results. "GZHOSP" → 0 results. "guangzhou hospital" → 0 results. "iowa public health" → 0 results. "public health" → only generic QA benchmarks (mteb/PublicHealthQA, xhluca/publichealth-qa, etc.).
- No `uqtag=AGEDATA23`-adjacent uploads found.

### F-7 (NEGATIVE): museum / uqscan
- "uqscan" → 0 results. "museum" → 50 results, all benign (Met Museum, art museum image/QA datasets). "museum agent" → 0 results.
- "hospital" → 50 results, all benign clinical/hospitality datasets (MultiWOZ hospital, MIMIC-III course meta, etc.).

### F-8 (NEGATIVE / deferred): agent-traces landscape
- "agent-traces" → 50 results: trace-commons/agent-traces, agent-evals/hal_traces, pavan01729/web-search-agent-sft-traces, jdpressman/weave-agent-traces-2025-11-05, agent-data/misc-merged-claude-code-traces-v1 (32k Claude Code traces), vincentoh/sandbagging-agent-traces, etc. All coding/planning/search-agent trace corpora — none browser-eval over Chinese apps; none grepped yet (too many/large for this pass). Candidates only if later pivots need them.
- "agentic-browsing" → 0 results. "browsing eval" → OpenHandsCommunity/eval-browsing-instructions (2024-07-15, BrowserGym WebArena shopping instructions), Mozilla/citation-eval-search-browsing-history — no markers.

### F-9 (NOTE): deepsearchqa reuploads
- Task said move on from google/deepsearchqa (already confirmed). For the record, mirrors exist: Rendy45/deepsearchqa, seerbyseai/deepsearchqa-gemini2-reasoning, Rendra8631/deepsearchqa, Leonnel1220/CS-DeepSearchQA, yoonsanglee/deepsearchqa-react, youdotcom/minimax-m3-deepsearchqa-skill-eval. Not examined.

## Overall grading
- **No uploaded eval/trace dataset on HuggingFace matches the swarm's real-collection fingerprints.** Zero hits for uqscan / uqtag / AGEDATA23 / GZHOSP / getPoiInfo / sub_poi_navi / B0 place IDs / chatgpt.com utm across every dataset actually downloaded and grepped (amap-2000 metadata, didi-4000 README, TC130/amap_mcp 65MB full file, OpenHands browsing_instructions.jsonl).
- Closest adjacent surface: the MobileGym-Harmony mock-app candidate-trajectory family (Stephen3zero24 amap-2000 + didi-4000) — same domain (Gaode map GUI agents), same Aug-2026 window, zh language — but self-declared synthetic and marker-negative.
- Honest zeros recorded above: IDPH, GZHOSP, uqscan, guangzhou hospital, museum agent, gaode map, spider amap, getpoi, sub_poi (except unrelated inspektral/minisynth1k-sub-points-v1).

## Open questions
1. Do the MobileGym-Harmony authors publish real-app variants anywhere, or is the "mock app" framing a standing pattern? (Check Stephen3zero24 for future releases.)
2. Is there an unindexed upload (HF search is keyword-based; exact repo names wouldn't surface)? Guessing repo IDs is not productive; better to watch the MobileGym ecosystem and the `mobilegym-harmony` tag via periodic API polling.
3. The swarm's real-collection fingerprints (uqscan tags, B-place IDs) might live in downloaded corpora that never get uploaded (urlquery is where they surfaced) — HF may simply not be their publish surface.
4. Whether any agent-traces corpus (F-8) contains web-browsing traces touching Chinese sites — large greps deferred this run.

## Reuse recipes
```bash
# dataset search
curl -s "https://huggingface.co/api/datasets?search=<term>&limit=50" | python3 -c "import json,sys; d=json.load(sys.stdin); [print(r['id'],'|',r.get('createdAt','')[:10]) for r in d]"
# tree + download + marker grep
curl -s "https://huggingface.co/api/datasets/<A>/<R>/tree/main" | python3 -c "..."
curl -sL "https://huggingface.co/datasets/<A>/<R>/resolve/main/<path>" -o f
grep -oi -c -E 'uqscan|uqtag|agedata23|gzhosp|getPoiInfo|sub_poi_navi|dsqa_|B0[0-9A-Za-z]{8}' f
```
