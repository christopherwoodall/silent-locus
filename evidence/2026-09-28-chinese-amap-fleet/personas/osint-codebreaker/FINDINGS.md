# OSINT CODEBREAKER — FINDINGS
## Uploaded eval information on public infrastructure (2026-10-05)

**Task families:** (1) Amap POI collection (`sub_poi_navi`/`getPoiInfo`, B-prefixed place IDs, `uqscan=<word><date>[suffix]>` tags); (2) museum enumeration (`uqscan=qingdaomuseum20261005b` etc.); (3) health data (IDPH, AIHW, `uqtag=AGEDATA23`, June 2026); (4) DeepSearchQA gov-data (dsqa_250 → DoE); (5) hospital targets `GZHOSP-*`.
**Grade scale:** CONFIRMED (primary-source bytes) / LIKELY / CANDIDATE (unverified) / NEGATIVE (searched, ruled out).
**Rules honored:** agents & agent infrastructure only — no human/operator identity work. No commits/pushes.
**Raw notes:** `raw/hf-datasets.md`, `raw/github-pastes.md`, `raw/buckets-archives.md` (+ raw evidence JSONs `ia_*`, `cdx_*`, `cc_*`).

---

## 1. CONFIRMED: Wayback archived 13 Amap POI place pages in the museum-enumeration window

14 captures of `amap-pc-ssr.amap.com/ssr/place/B…` — 2 on 2026-09-28/29, 12 on 2026-10-03/04 — plus a 9-capture burst of `detail/B001C94YUZ` (+`punishTextFetch`/`report`/`feedback` subresources) on 2026-10-04 01:08–01:11 UTC. **12 of the 13 place IDs appear in our urlquery corpus.** One capture carries `?w=retry2` — agent-shaped archival marker, consistent with agent Save-Page-Now (archive-as-you-go) rather than organic crawling. Observer alternative not excluded.
Content split: the `detail/B001C94YUZ` capture is Amap's **anti-bot challenge interstitial** (archiver hit the bot wall); `ssr/place/B00140H7SM` is a **full 325KB Next.js SSR page**. Only 2 of 14 captures content-checked. (LIKELY: agent-side archival.)

## 2. CONFIRMED: dead-drop tradecraft decoded — httpbun cache-probe beacon

Base64 httpbun probe in urlquery report `f2a45ccb` decodes to a JS cache-probe that fetches Amap POI pages via the **jina.ai reader relay** with `X-Cache-Tolerance: 2592000` (GCP CDN cache probing), extracts `/%到达/` lines, and beacons results to **`httpbun.com/anything/gcresult`** (errors → `/anything/gcerror`) via image-beacon + `document.title`. New dead-drop surface for future hunts.

## 3. CONFIRMED (adjacent, markers ABSENT): public Amap agent-eval artifacts exist — not the fleet

- **`Stephen3zero24/amap-2000-candidates-v1`** — 2,000 synthetic GUI-agent trajectories on "MobileGym-Harmony 高德 (Amap) Mock App" (22,667 actions, 22,836 synthetic screenshots, 2026-08-14/17, Codex-prepared). Explicitly NOT real Amap collection; excluded upstream "A1/A2 sampling files" hint at a real-collection phase that never published. Marker grep: 0 hits. Do NOT conflate with the swarm's fleet.
- **`TC130/amap_mcp`** — 4,768-line Amap MCP tool-calling eval (9 Amap MCP function defs, Chinese route queries). Full 65.6 MB download grepped: 0 marker hits.
- **`Sorel-ch/LLM-guide-agent`** — agent-built travel wiki (created 2026-09-28) that committed raw Amap API snapshots to `raw/amap/` with B-prefixed place IDs (e.g. `"id": "B000A8UIN8"` for 故宫博物院). Tool names differ (`get_amap_poi_search` vs fleet's `sub_poi_navi`/`getPoiInfo`) → different stack. Best in-the-wild template of what a fleet hit would look like. Same artifact class, unrelated operator.
- **MobileGym ecosystem mapped** (all synthetic/simulator): `Ma-Vector/MobileGym-ConAct-Trajectories`, `gray311/mobilegym-*`, `HaoranLiu/DPO-Qwen3-MobileGym`, `yorkkk2/hmp-mobilegym`. Watch the `mobilegym-harmony` tag.
- `deepsearchqa` code hits (2,736 GitHub): all public harness integrations (`exa-labs/benchmarks`, `modelscope/evalscope`, `NVIDIA-NeMo/Gym`). No uploaded dsqa answers/traces/prompts. HF: `google/deepsearchqa` official + mirrors.
- `wangmingxinthu/amap_spiderwam_ckpt` = robotics LIBERO checkpoint, "AMAP" ≠ Gaode. False positive, documented.

## 4. NEGATIVES (fleet markers have no detectable public footprint)

- GitHub code search: `"uqscan="` → **0**; `sub_poi_navi` → **0**; `AGEDATA23` → substring noise only (`PackageData23`…); `GZHOSP` → 133 hits = scraped 补天 (BuTian) bug-bounty target-domain lists containing `www.gzhosp.cn`, coincidental substring — ruled out. `getPoiInfo` → WoW API + generic POI getters, none Amap.
- GitHub commit search: `uqscan` → 0; `AGEDATA23` → 0; `sub_poi_navi` → 1 (ROS robotics "added poi sub to navi", unrelated); `getPoiInfo` → 27 (game API noise); `GZHOSP` → 2 (same MtF-wiki coincidental slug). "uqtag" commit hits (`gregduegee/documents-5ba7a58e`, `l7sxyi4ycm/clug`) = random-filename batch-publisher repos, verified NEGATIVE via file bytes.
- Pastes (pastebin/rentry/hastebin/ghostbin/paste.rs, site-scoped + OR queries) → 0 relevant. Gists: no working code-search route; web-indexed gist search NEGATIVE.
- HuggingFace: all marker searches → 0 datasets; health lanes (IDPH, GZHOSP, AIHW) → 0.
- Archive.org advancedsearch: `uqscan`/`AGEDATA23`/`getPoiInfo` → 0; `sub_poi_navi` → 5 CIA-OCR false positives; `deepsearchqa` → 4 Kimi model-card noise hits.
- Common Crawl (CC-MAIN-2026-39): `*AGEDATA23*`, `*getPoiInfo*`, `*sub_poi_navi*` → 0 captures; `*uqscan*`/`*deepsearchqa*` → 504-inconclusive (mid-string wildcard too expensive; NOT a negative).
- Public buckets: GCS+S3 `deepsearchqa`/`uqscan`/`agedata23`/`amap-poi`/`gzhosp`/`deepsearch-qa` → all 404/NoSuchBucket. **GCS `dsqa` → 403 (bucket exists, private)** — passive dead end, flagged, not pursued (cannot attribute).
- Zero transfer.sh/file.io/gofile/nfile links found anywhere.
- Pre-restart results (verified then, not redone): DeepSearchQA 900 questions = 5 museum + 3 hospital + 1 China Qs, all US/arts/clinical flavored — ZERO match to Amap museum family or GZHOSP. Clean negative.

**Net assessment:** the fleet's distinctive markers have no detectable public footprint on any reachable surface as of 2026-10-05 — either the operators don't upload, or uploads carry different/no markers. Net new artifact class surfaced: agent-side Wayback archival (`?w=retry2`) + httpbun dead-drop beacons.

## 5. Open questions
1. Who archived the POI pages — the fleet or an observer?
2. Content of the other 11 archived `ssr/place/*` captures.
3. GCS `dsqa` (403) owner — passive dead end.
4. Retry Common Crawl with per-domain queries (`httpbun.com/anything/*`, `webhook.site/*`).
5. Gist gap — no working gist code-search route found; GitHub logged-in gist search UI or BigQuery GitHub dataset.
6. Re-run `q="uqscan="` and `q=sub_poi_navi` in a few days (fleet active NOW; index lags).
7. Stephen3zero24's excluded "A1/A2 Amap sampling files" — is there a real-collection upstream?

---

## 6. Documented endpoints (reusable)

**HuggingFace (curl ONLY — python `huggingface_hub` broken on VM, httpx2 chokes on IPv6 NO_PROXY):**
- Search: `https://huggingface.co/api/datasets?search=<q>&limit=<n>` (and `/api/models?search=<q>&limit=<n>`); author enumeration: `?author=<user>&limit=<n>`
- Metadata: `https://huggingface.co/api/datasets/<author>/<repo>`; tree: `.../tree/main`; download: `https://huggingface.co/datasets/<author>/<repo>/resolve/main/<path>` (with `-L`; HEAD Content-Length may lie)

**GitHub (`gh` logged in):**
- Code: `gh api "/search/code?q=<urlencoded>&per_page=100"` — 10 req/min authenticated, sleep ≥7s
- Commits: `gh api -H "Accept: application/vnd.github+json" "/search/commits?q=<q>&per_page=5"`
- Issues/PRs: qualifier `is:issue`/`is:pr` REQUIRED or 422
- File bytes: `gh api "repos/<owner>/<repo>/contents/<path>?ref=<sha>" --jq '.content' | base64 -d`

**Archives:**
- IA advancedsearch: `https://archive.org/advancedsearch.php?q=<urlencoded>&fl[]=identifier&fl[]=title&fl[]=date&rows=50&output=json`
- Wayback CDX: `https://web.archive.org/cdx/search/cdx?url=<prefix/*>&output=json&limit=N&collapse=urlkey&fl=timestamp,original,statuscode,mimetype`; raw WARC via `/web/<ts>id_/<url>` (gzip-detect)
- Common Crawl: `https://index.commoncrawl.org/collinfo.json` → per-crawl index; avoid mid-string `*kw*` wildcards (504) — use per-domain `url=` queries

**Buckets:** GCS path-style `https://storage.googleapis.com/<bucket>`, virtual-hosted `https://<bucket>.storage.googleapis.com/`; S3 `https://<bucket>.s3.amazonaws.com/`, parse `<Code>` in 403/404 body.

**Blocked/dead (2026-10-05):** grep.app → Vercel bot challenge from VM; searchcode API → 404; Sourcegraph stream API → zero events. GitHub code search is the only working code index from here.

---

## 7. ALL OBSERVED URLS

### Findings — public artifacts
- https://huggingface.co/datasets/Stephen3zero24/amap-2000-candidates-v1
- https://huggingface.co/datasets/Stephen3zero24/didi-4000-candidates-v1
- https://huggingface.co/datasets/TC130/amap_mcp
- https://github.com/Sorel-ch/LLM-guide-agent
- https://github.com/pranava0x0/vibe-coding-security/blob/HEAD/advisories/2026-08-taiwan-dream-autonomous-ai-agent-attack.md

### Findings — fleet tradecraft surfaces
- https://httpbun.com/anything/gcresult (dead-drop beacon; errors → `https://httpbun.com/anything/gcerror`)
- https://r.jina.ai/https://amap-pc-ssr.amap.com/ssr/place/B001C94YUZ (jina relay fetch as observed in probe)
- https://amap-pc-ssr.amap.com/ssr/place/B001C94YUZ (Wayback-captured POI page, `?w=retry2` marker)
- https://amap-pc-ssr.amap.com/ssr/place/B00140H7SM (325KB SSR capture)
- https://amap-pc-ssr.amap.com/detail/B001C94YUZ (anti-bot interstitial capture; `punishTextFetch`/`report`/`feedback` subresources)

### Resolved-negative URLs
- http://www.gzhosp.cn (BuTian target-list coincidental match — NOT eval traces)
- https://mtf.wiki/zh-cn/docs/psyco/guangdong/gzhosp/ (issue-slug coincidence, `project-trans/MtF-wiki#859`)
- https://github.com/gregduegee/documents-5ba7a58e (random-filename `uqtag-79440.md`, batch-publisher, NOT fleet)
- https://github.com/l7sxyi4ycm/clug (same batch-publisher shape)

### Working endpoints (patterns)
- https://huggingface.co/api/datasets?search=<q>&limit=<n>
- https://huggingface.co/api/models?search=<q>&limit=<n>
- https://huggingface.co/api/datasets?author=<user>&limit=<n>
- https://huggingface.co/api/datasets/<author>/<repo>
- https://huggingface.co/api/datasets/<author>/<repo>/tree/main
- https://huggingface.co/datasets/<author>/<repo>/resolve/main/<path>
- https://grep.app/api/search?q=<q> (blocked from VM)
- https://searchcode.com/api/codesearch_I/?q=<q> (dead/geo-blocked)
- https://sourcegraph.com/.api/search/stream?q=context:global+<q>&v=V2&t=select:file (unreliable)
- https://archive.org/advancedsearch.php?q=<q>&fl[]=identifier&fl[]=title&fl[]=date&rows=50&output=json
- https://web.archive.org/cdx/search/cdx?url=<prefix/*>&output=json&limit=N&collapse=urlkey&fl=timestamp,original,statuscode,mimetype
- https://web.archive.org/web/<ts>id_/<url>
- https://index.commoncrawl.org/collinfo.json
- https://index.commoncrawl.org/<ID>-index?url=<pattern>&output=json
- https://storage.googleapis.com/<bucket>
- https://<bucket>.storage.googleapis.com/
- https://<bucket>.s3.amazonaws.com/
