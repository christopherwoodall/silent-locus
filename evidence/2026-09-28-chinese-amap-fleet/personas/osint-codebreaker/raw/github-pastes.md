# GITHUB-PASTES HUNT — working notes
**Hunter:** GITHUB-PASTES HUNTER (OSINT CODEBREAKER child) · **Date:** 2026-10-05
**Scope:** uploaded eval information on GitHub / gists / paste services — eval datasets, prompts, agent traces, answers left online by agents or builders.
**Rules honored:** no commits/pushes; agents & agent infrastructure only — no human/operator identity work, no deanonymization.
**Task families:** (1) Amap POI collection — `sub_poi_navi` / `getPoiInfo`, B-prefixed Amap place IDs, `uqscan=<word><date>[suffix]>` tags; (2) health data — IDPH/AIHW, `uqtag=AGEDATA23`; (3) DeepSearchQA gov-data (dsqa_250 → DoE); (4) hospital targets `GZHOSP-*`.

Evidence grades used: **CONFIRMED** (verified against primary source bytes) / **LIKELY** / **CANDIDATE** (unverified lead) / **NEGATIVE** (searched, ruled out).

---

## 1. Findings (ranked)

### F1 — CONFIRMED (adjacent artifact, markers ABSENT): HF dataset `Stephen3zero24/amap-2000-candidates-v1`
- **URL:** https://huggingface.co/datasets/Stephen3zero24/amap-2000-candidates-v1
- **What:** 2,000 deterministic synthetic GUI-agent candidate trajectories on a "MobileGym-Harmony 高德 (Amap) Mock App". 22,667 action records, 22,836 synthetic 360×800 screenshots, 8 frozen leaf chains (route-mode ×4, nearest-compare ×4). Prepared by "Codex under user-authorized public release scope", 2026-08-14 → validated 2026-08-17.
- **Verification:** HF API + full README.md + PUBLICATION-SAFETY.md fetched via curl (per TOOLS.md HF-via-curl rule). Card explicitly states: NOT real Amap collection, NOT real model rollout, NOT training/eval-validated; "original Amap sampling files" (A1/A2) existed upstream but were excluded from publication.
- **Relation to our task families:** SAME surface (Amap), DIFFERENT task family (route planning on a mock app vs our POI-collection fleet with `uqscan` tags). Zero hits for `uqscan|uqtag|AGEDATA23|sub_poi_navi|getPoiInfo|GZHOSP|deepsearchqa` in metadata files. **Do not conflate with the swarm's Amap fleet.**
- **Why it matters:** proves builders DO upload Amap agent-eval artifacts publicly; "MobileGym-Harmony" is a new project name for the hunt lexicon; the excluded "A1/A2 sampling files" hint at a real-collection phase that never got published — worth watching for.

### F2 — CONFIRMED (adjacent artifact, markers ABSENT): HF dataset `TC130/amap_mcp`
- **URL:** https://huggingface.co/datasets/TC130/amap_mcp · files: `amap_answer_full.jsonl` only (no README/card).
- **What:** 4,768-line Amap MCP tool-calling eval set. Schema per line: `{tools: [9 Amap MCP function defs, e.g. maps_direction_driving_by_coordinates], query: <Chinese user query>, messages: [5 msgs incl. system prompt with <tools> XML]}`. Example query: "我想骑自行车从北京大学到颐和园，请规划一条路线。" 34 downloads.
- **Verification:** downloaded full 65.6 MB file via curl; `grep -c -i -E "uqscan|uqtag|agedata|sub_poi_navi|getPoiInfo|GZHOSP|deepsearchqa"` → **0 hits**. Note: HTTP HEAD `Content-Length: 1066` lied; real body 65,646,835 bytes.
- **Relation:** Amap MCP tool-use eval (route planning). Same surface, different task family, no swarm markers.

### F3 — CONFIRMED (expected public, not a leak): `deepsearchqa` GitHub code hits = benchmark harness integrations
- `gh api /search/code?q=deepsearchqa` → 2,736 total; top hits all public eval-harness code: `exa-labs/benchmarks/benchmarks/dsqa.py`, `ApodexAI/FrontierAgent`, `ApodexAI/AgentHarness`, `XYZ-AI-Lab/AxisAgentic/configs/deepsearchqa.yaml`, `Desearch-ai/desearch-search-evals`, `modelscope/evalscope`, `NVIDIA-NeMo/Gym`, `bingreeky/JIT`.
- No uploaded dsqa_250 answers, traces, or prompts found. HF datasets: `google/deepsearchqa` (official, 23,753 dl) + mirrors + `youdotcom/minimax-m3-deepsearchqa-skill-eval`. Nothing swarm-specific.

### F4 — NEGATIVE (verified): `GZHOSP` GitHub hits are 补天 (BuTian) bug-bounty target lists
- `gh api /search/code?q=GZHOSP` → 133 total. Spot-checked primary sources: `PyxYuYu/MyBlog/.../BuTianCompany201605109.txt` and `LangziFun/BuTian_Spider/.../不带http的.txt` — the match is the domain **`www.gzhosp.cn`** sitting in scraped BuTian SRC target-domain lists (neighbors: zhihu.com, jumei.com, aqga.gov.cn). Not `GZHOSP-*` hospital-backend eval traces. Coincidental substring match — ruled out.

### F5 — NEGATIVE: exact tag patterns have zero GitHub presence
- `gh api /search/code?q="uqscan="` → **total 0**. The fleet's URL-tag format does not appear in indexed GitHub code.
- `gh api /search/code?q=sub_poi_navi` → **total 0** (also 0 on web search, see §2).
- `gh api /search/code?q=henanmuseum` (14) / `wenzhou-museum` (7) / `qingdaomuseum` (16) → all generic museum repos (password lists, travel miniprograms, `jackandking/MuseumCheck` check-in app); no `uqscan=<museum><date>` tags anywhere.

### F6 — NEGATIVE (self-hit, not a finding): `christopherwoodall/silent-locus` `scripts/extract_f1f2.py`
- Matched `uqscan` code search; verified via `gh api repos/.../contents/...` → the hit is line 82: `param_re = re.compile(r"[?&](x|uqscan|r|ov|t|ts|nonce)=(\d{6,19})")` — **our own hunt tooling** regex for extracting these URL params from the urlquery corpus. Self-reference; excluded from findings.

### F7 — CONFIRMED artifact (different operator/task, no fleet markers): `Sorel-ch/LLM-guide-agent`
- **URL:** https://github.com/Sorel-ch/LLM-guide-agent · created 2026-09-28, pushed 2026-09-29.
- **What:** a travel-planning agent built on the Karpathy "LLM Wiki" pattern. `AGENTS.md` is the agent's operating spec (Ingest → Query → Lint); `.mcp.json` wires a local `travel` MCP server (`mcp/travel_mcp.py`, FastMCP stdio) exposing `get_amap_poi_search`, `get_amap_input_tips`, `get_amap_direction`, `get_amap_weather`, `metaso_web_search/reader`.
- **The artifact:** on 2026-09-28 the agent ingested Hangzhou travel data and committed **raw Amap API response snapshots** to `raw/amap/`: `2026-09-28_poi_<故宫博物院|西湖|灵隐寺|杭州景点_top|…>.json`, `2026-09-28_dir_<东站到西湖_transit|断桥到苏堤_walking|…>.json`, `tips_杭州_admin.json`, `weather_330100_*.json`. Verified: POI JSON contains **B-prefixed Amap place IDs** (e.g. `"id": "B000A8UIN8"` for 故宫博物院, with parent/child POI linkage).
- **Marker check:** full `grep -i -E "uqscan|uqtag|AGEDATA23|sub_poi_navi|getPoiInfo|GZHOSP"` over a POI snapshot → **0 hits**. Tool names differ from the fleet's (`get_amap_poi_search` vs `sub_poi_navi`/`getPoiInfo`) → different agent stack.
- **Why it matters:** the single best in-the-wild specimen of the hunt's premise — an agent doing Amap POI collection and committing raw captures to GitHub. Template for what a fleet hit would look like. Classified: same artifact class, unrelated operator.

---

## 2. Negative-search log (queries with zero results are data)

| # | Surface / query | Result |
|---|---|---|
| N1 | `browser.search` `"uqscan" github` | 0 relevant (typosquat domains + TikTok noise) |
| N2 | `gh /search/code?q="uqscan="` | 0 |
| N3 | `gh /search/code?q=sub_poi_navi` | 0 |
| N4 | `browser.search` `"sub_poi_navi" OR "getPoiInfo" amap gaode poi` | **No results found** |
| N5 | `browser.search` `"GZHOSP" OR "uqtag=AGEDATA23" OR "deepsearchqa" amap hospital eval` | 0 relevant (generic DeepSeek-in-hospitals papers) |
| N6 | `browser.search` `pastebin OR rentry OR ghostbin "uqscan" OR "uqtag" OR "AGEDATA23" OR "sub_poi_navi"` | 0 relevant (SEO-spam PDFs) |
| N7 | `browser.search` `site:pastebin.com uqscan OR uqtag OR AGEDATA23 OR sub_poi_navi` | **No results found** |
| N8 | `browser.search` `rentry.co OR hastebin.com OR paste.rs "uqscan" OR "uqtag" OR "AGEDATA23" OR "sub_poi_navi" OR "GZHOSP"` | **No results found** |
| N9 | `browser.search` `gist.github.com "uqscan" OR "uqtag=" OR "sub_poi_navi" OR "AGEDATA23"` | **No results found** |
| N10 | HF datasets `search=uqscan` | 0 datasets |
| N11 | HF datasets `search=gzhost` | 0 datasets |
| N12 | HF datasets `search=sub_poi` | 1 hit → `inspektral/minisynth1k-sub-points-v1`, verified **unrelated** (audio/music synthetic data; keyword coincidence on "sub-points") |
| N13 | HF datasets `search=agedata` | 3 hits, all `age_dataset` age-prediction sets — unrelated |
| N14 | `gh /search/code?q=AGEDATA23` (82) | all substring noise (`PackageData23`, `StageData23`…); no `uqtag=AGEDATA23` |
| N15 | `gh /search/code?q="uqtag="` (6,272) | tokenizer noise — `project.assets.json` / `.nupkg.metadata` files matching `uq`+`tag` tokens; no `uqtag=<value>` pattern |
| N16 | `gh /search/code?q=getPoiInfo` (1,280) | WoW API + generic POI getters; none Amap-related in top 10 |
| N17 | `gh /search/code?q=restapi.amap.com` / `webapi.amap.com` (14–18k) | normal Amap SDK usage; too broad to discriminate — not a useful pivot |
| N18 | `gh /search/issues` (+`is:issue`): `uqscan` → 0, `AGEDATA23` → 0, `sub_poi_navi` → 0 |
| N19 | `gh /search/issues?q=GZHOSP+is:issue` → 1 hit, verified **unrelated**: `project-trans/MtF-wiki#859` (2023) — a transgender-healthcare community wiki issue; match is the URL slug `mtf.wiki/zh-cn/docs/psyco/guangdong/gzhosp/` ("gzhosp" = Guangzhou-hospital abbreviation). Not eval traces. |
| P1 | RESOLVED 2026-10-05: `gh /search/commits` — `uqscan` → 0; `AGEDATA23` → 0; `sub_poi_navi` → 1 (robotics repo `keithtjj/multi_ugv_behaviours`, "added poi sub to navi" = ROS subscriber, unrelated); `getPoiInfo` → 27 (game API docs, e.g. Allods Online `astral.GetPOIInfo` — noise); `GZHOSP` → 2 (both `project-trans/MtF-wiki`, same coincidental slug as N19); `deepsearchqa` → 159 (public harness integrations: modelscope/evalscope, youdotcom-oss skill-eval, search_gym_v2 — no leaks) |
| P3 | RESOLVED 2026-10-05: grep.app **BLOCKED** — all 6 queries returned Vercel Security Checkpoint HTML (bot challenge) instead of JSON, with and without browser UA. Endpoint unusable from this VM without JS-challenge solving (no live browser available to this agent). No grep.app coverage obtained; GitHub code search remains the primary code index. |

**P1a — `uqtag` commit hits investigated, ruled out (coincidental token collision):**
- `gregduegee/documents-5ba7a58e` ("Created by GitHub batch publisher", created→pushed in 25s on 2026-09-18): commit `bac23033` "uqtag-79440" adds `uqtag-79440.md`. Full tree shows ~100 files ALL named `<5-random-letters>-<5-digits>.md` (`affwz-05651.md` … `uqtag-79440.md` … `zznmz-38633.md`); file bytes = "AI Builders Digest" Chinese news digest (厦门跨境电商展). The `uqtag` prefix is one random draw of the filename generator, not a tag.
- `l7sxyi4ycm/clug` ("content", created→pushed in ~90s on 2026-10-01): commit `41978941` "51437-uqtag" adds `51437-uqtag.md` = same "AI Builders Digest 今日热点快报" pipeline (dated 2026-10-01 14:05:40 UTC+8).
- Pattern: automated newsletter batch-publisher minting throwaway repos; `uqtag` appears as random-filename component only. **NEGATIVE for the fleet** (verified against primary-source file bytes). Noted because the throwaway-repo + batch-publisher shape superficially resembles staging infrastructure.

**Net assessment:** the fleet's distinctive markers (`uqscan=`, `sub_poi_navi`, `uqtag=AGEDATA23`, `GZHOSP-*`) have **no detectable footprint** on GitHub code, web-indexed pastes, gists, or HF datasets as of 2026-10-05. Either the operators don't upload to these surfaces, or uploads use different/no markers.

---

## 3. Working endpoints & reusable query patterns (for future hunts)

All verified working from this VM on 2026-10-05. Auth: `gh` logged in as christopherwoodall (PAT in `~/.config/gh/hosts.yml`).

1. **GitHub code search (authenticated, best recall):**
   `gh api "/search/code?q=<urlencoded>&per_page=100" --jq '{total: .total_count, items: [.items[] | {repo: .repository.full_name, path: .path, url: .html_url}]}'`
   - Rate limit: **10 req/min** (authenticated) — sleep ≥7s between calls or jobs stall (observed: rapid loop backgrounded/stalled).
   - Quote exact phrases: `q="uqscan="` — but note the tokenizer still strips `=` in practice (N15); verify hits against raw bytes.
   - File bytes: `gh api "repos/<owner>/<repo>/contents/<path>?ref=<sha>" --jq '.content' | base64 -d`
2. **GitHub commit search:** `gh api -H "Accept: application/vnd.github+json" "/search/commits?q=<q>&per_page=5" --jq '{total:.total_count, items:[.items[]|{repo:.repository.full_name,msg:.commit.message[0:120],url:.html_url}]}'`
3. **GitHub issues/PRs search:** qualifier `is:issue`/`is:pr` is REQUIRED or API 422s: `/search/issues?q=<q>+is%3Aissue`
4. **grep.app (unauthenticated 2nd index):** `curl -s "https://grep.app/api/search?q=<q>"` → `.hits.hits[]` with `repo.raw`, `path.raw`. Different index than GH — catches things GH misses. **STATUS 2026-10-05: BLOCKED from this VM** — returns Vercel Security Checkpoint bot-challenge HTML (with or without browser UA); needs JS-challenge solving via live browser. Unusable until that route exists.
5. **HuggingFace dataset discovery (curl per TOOLS.md; python huggingface_hub is broken on this VM):**
   - Search: `curl -s "https://huggingface.co/api/datasets?search=<q>&limit=10"`
   - Metadata: `curl -s "https://huggingface.co/api/datasets/<id>"` → siblings, tags, cardData
   - Files: `curl -sL "https://huggingface.co/datasets/<id>/resolve/main/<path>"` (follows redirects; note HEAD Content-Length may lie — the TC130 file reported 1066 B, delivered 65.6 MB)
   - Dataset README cards often contain the richest provenance (see F1's PUBLICATION-SAFETY.md pattern: prepared-by, dates, exclusion lists — mine these).
6. **sourcegraph public stream API:** `https://sourcegraph.com/.api/search/stream?q=context:global+<q>&v=V2&t=select:file` — returned **zero events** for all 5 test queries on 2026-10-05; endpoint may need different params or is degraded. Treat as unreliable until re-validated.
7. **searchcode API:** `https://searchcode.com/api/codesearch_I/?q=<q>` → **"404 page not found"** from this environment on 2026-10-05. Endpoint dead or geo-blocked; do not rely on it.
8. **Web surface checks that worked:** `browser.search` with `site:pastebin.com`, `site:gist.github.com` scoping; combined paste-domain OR queries. Gist code content is effectively unindexed — gist hunting needs another route (see open questions).

---

## 4. Context note (known prior advisory)
Fetched https://github.com/pranava0x0/vibe-coding-security/blob/HEAD/advisories/2026-08-taiwan-dream-autonomous-ai-agent-attack.md (2026-08-12, status: unconfirmed): Dream (Israeli firm) disclosed a 4-day near-autonomous Hermes/OpenClaw agent attack on Taiwan gov + nuclear safety agency (85 accounts, 2,500+ personnel records, 1,395-file/160MB exposed op archive). Relevant as the "agents leave their own archives online" precedent class — same failure mode this hunt looks for — but a different incident/actor from the Amap fleet.

---

## 5. Open questions
1. **Gist gap:** no working gist code-search route found. Options: GitHub's logged-in gist search UI (needs live browser), third-party mirrors (e.g. gist search engines), or BigQuery GitHub dataset. The fleet's tags would fit naturally in a gist.
2. ~~F7 follow-up~~ RESOLVED 2026-10-05: `Sorel-ch/LLM-guide-agent` classified — agent-built travel wiki with raw Amap POI/direction snapshots (see F7). Same artifact class, unrelated operator.
3. **Upstream of F1:** the excluded "A1/A2 Amap sampling files" and "MobileGym-Harmony" project — is there a repo/org behind it? Search GitHub orgs/repos for `MobileGym` / `MobileGym-Harmony`.
4. **P1–P3:** fold in pending commit/issues/grep.app results when delivered.
5. **Pastebin PRO scraping API** (recent-public-pastes firehose) needs an API key — not pursued (no key, no account creation per rules). A keyed sweep remains an option if BigSexyWarlock69 approves.
6. **Timing note:** `uqscan=<word>20261005<suffix>` tags are dated 2026-10-04/05 — the fleet is ACTIVE NOW. GitHub code index lags; re-run `q="uqscan="` and `q=sub_poi_navi` in a few days.
