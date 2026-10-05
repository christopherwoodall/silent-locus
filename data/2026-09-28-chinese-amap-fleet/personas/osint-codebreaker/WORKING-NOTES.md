# OSINT Codebreaker — working notes

## Task families to match (from local corpora)
1. Amap POI collection: `sub_poi_navi` / `getPoiInfo` / place IDs `B…`, tags `uqscan=<word><date>[suffix]`
2. Museum enumeration: `uqscan=qingdaomuseum20261005b`, `henanmuseum_20261005a`, `wenzhou-museum-20261004`
3. Health data: IDPH (Iowa), AIHW (Australia, `uqtag=AGEDATA23`, June 2026)
4. DeepSearchQA gov-data (dsqa_250 → DoE; 900 questions banked locally)

## Direct findings so far
- DeepSearchQA (google/deepsearchqa, 900 Qs): 5 museum Qs (dsqa_107/208/239/569/648), 3 hospital Qs
  (dsqa_043/234/565), 1 China Q (dsqa_875) — ALL US/arts/clinical flavored. ZERO match to
  Amap museum family (Qingdao/Henan/Wenzhou) or GZHOSP targets. Clean negative, recorded.
- Muse Glimmer eval methodology (hideme.live mirror of research.meta.ai): DeepSearchQA = "agentic
  browsing evaluation... single browsing tool with three functions: search, open and find."
  Confirms the eval-run framing for dsqa-linked incidents.
- Chinese-language web search: NO public benchmark with Amap/POI task definitions found.
  Amap task family appears proprietary/internal — either a private eval or a production
  data-collection workload, not a published eval.
- HuggingFace Hub API: direct curl failing (000) from this VM session; HF child subagent
  dispatched with instructions, will route around.

## Children dispatched
- hf-datasets.md (HuggingFace dataset hunt)
- github-pastes.md (GitHub/gist/paste hunt)
- buckets-archives.md (DONE 2026-10-05: Wayback archived 13 Amap POI pages in the 10-03/04 museum window, 12/13 IDs in our corpus, `?w=retry2` marker; decoded httpbun/jina/X-Cache-Tolerance dead-drop tradecraft; all marker searches on IA/CC/buckets/web negative; GCS `dsqa` 403-exists-private unverifiable)

## Post-restart run (2026-10-05 ~05:14–05:40 UTC)
All three surface hunters respawned and completed. Final report: FINDINGS.md.
- hf-datasets.md: no uploaded eval/trace data matches fleet markers. Closest: Stephen3zero24/amap-2000-candidates-v1 + didi-4000-candidates-v1 (synthetic, mock-app); TC130/amap_mcp (MCP eval, 0 markers).
- github-pastes.md: "uqscan=" / sub_poi_navi = 0 GitHub hits; GZHOSP = BuTian target-list noise; "uqtag" commit hits = random-filename batch-publisher repos (verified negative via file bytes); Sorel-ch/LLM-guide-agent = best in-the-wild Amap-POI-collection artifact template, unrelated stack. grep.app blocked (Vercel challenge), searchcode dead, sourcegraph unreliable.
- buckets-archives.md: Wayback holds 13 Amap POI captures in museum window (12/13 IDs in our corpus; ?w=retry2 agent-shaped archival); archive.org marker searches negative; decoded httpbun dead-drop probe (f2a45ccb): jina relay + X-Cache-Tolerance cache probe → beacons httpbun.com/anything/gcresult|gcerror. GCS "dsqa" = 403 (exists, private — passive dead end, flagged).
