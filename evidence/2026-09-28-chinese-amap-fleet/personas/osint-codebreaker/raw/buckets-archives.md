# BUCKETS-ARCHIVES HUNT — working notes
**Persona:** OSINT Codebreaker · **Hunter:** buckets-archives (subagent)
**Date:** 2026-10-05 ~00:15–00:35 CDT (05:15–05:35 UTC)
**Scope:** public buckets, web archives, dead-drop surfaces for UPLOADED EVAL INFORMATION
(agent datasets, prompts, traces). Agents only — no human/operator identity work.
**Standing rule honored:** passive recon only — plain HTTP GET on public endpoints, no uploads,
no auth, no intrusive listing. NO commits/pushes (files written, left uncommitted).

## Task families matched
1. Amap POI: `sub_poi_navi` / `getPoiInfo`, B-prefixed place IDs, `uqscan=<word><date>[suffix]>`
2. Health: IDPH / AIHW, `uqtag=AGEDATA23`
3. DeepSearchQA gov-data (dsqa_250 → DoE)
4. Hospitals: `GZHOSP-*` (Guangzhou hospital backends)

---

## HEADLINE FINDING (confirmed)
**Wayback Machine archived 13 distinct Amap POI place pages (`amap-pc-ssr.amap.com/ssr/place/B…`)
inside the exact museum-enumeration window — 12 of the 13 place IDs also appear in our
urlquery corpus.** Capture clusters:
- 2026-09-28/29: 2 captures (`B000A7O1CU`, `B000A16E89`)
- 2026-10-03/04: 12 captures (`B02F30A3RV`, `B0FFF0DR58`, `B00154DWH8`, `B00190B8QT`,
  `B020005PMM`, `B001D003D3`, `B03170SWDL`, `B0303054T8` ×2 incl. **`?w=retry2`**,
  `B00140H7SM`, `B024F04YSV`, `B0FFF06JQQ`)

Plus 9 captures of `amap-pc-ssr.amap.com/detail/B001C94YUZ` (+ subresource endpoints
`punishTextFetch`, `report`, `page/feedback`) on **2026-10-04 01:08:41–01:11:24 UTC** —
a 3-minute burst consistent with automated Save-Page-Now.

Grading: **LIKELY agent-originated** (timing + 12/13 place-ID overlap with our corpus +
`?w=retry2` retry marker). Alternative not excluded: a third-party observer archiving the
same targets. CDX alone cannot distinguish; no identity work attempted.

Content checks (fetched raw WARC bytes via `id_`):
- `detail/B001C94YUZ` @ 20261004010841 → **Amap anti-bot challenge interstitial**
  ("有异常情况，请稍后再试" / "滑动下方滑块"). The archiver hit the bot wall and archived
  the challenge page instead of POI data. Agent-shaped: our corpus shows the fleet dodging
  this exact wall via the jina.ai reader relay.
- `ssr/place/B00140H7SM` @ 20261004013353 → **full 325 KB Next.js SSR page** (flight data,
  `initialTree`, real content, no challenge markers). At least some archived captures hold
  clean POI page content. (Only 2 of 14 captures content-checked; rest open.)

Corpus overlap detail (grep of `raw/*.json` for each place ID):
`B00140H7SM:3, B00154DWH8:3, B001D003D3:2, B020005PMM:1, B024F04YSV:4, B02F30A3RV:6,
B0303054T8:4, B03170SWDL:1, B0FFF06JQQ:6, B0FFF0DR58:4, B000A7O1CU:9, B000A16E89:6,
B00190B8QT:0` ← the single non-overlapping ID.

## BONUS: agent dead-drop tradecraft decoded (confirmed, from our corpus)
Decoded the base64 httpbun probe submitted in urlquery report
`report_f2a45ccb-fca8-43f6-a6e5-38f088582e79.json` (2026-10-04). It is a JS cache-probe page
(`gc-cache-probe-1791134820172`) that:
1. `fetch('https://r.jina.ai/https://amap-pc-ssr.amap.com/ssr/place/B001C94YUZ',
   {headers: {'X-Cache-Tolerance': '2592000', 'Accept': 'text/plain'}})` —
   **jina.ai reader as anti-bot relay; `X-Cache-Tolerance: 2592000` (30 d) = Google Cloud
   CDN cache-tolerance probing**
2. extracts lines matching `/%到达/` (arrival/transit info) from the POI page text
3. exfiltrates via `document.title` + image beacon to
   **`https://httpbun.com/anything/gcresult?d=<meta>&z=<ts>`**
   (error path → `https://httpbun.com/anything/gcerror?d=<err>`)
4. the report also shows `httpbun.com/base64/...` as the probe-delivery mechanism itself

**New dead-drop surface for future hunts:** `httpbun.com/anything/gcresult|gcerror` beacon
receiver (in addition to the known `webhook.site` UUID inboxes).

## Tag semantics clarified
- Web search for `"GZHOSP"` returns only `gzhosp.cn` = **Guangzhou First People's Hospital**
  (No.1 Panfu Lu, Yuexiu District). The `GZHOSP-*` tag prefix is derived from the target's
  own domain — consistent with the fleet's tag grammar, no eval data surfaced.

---

## LANE RESULTS (all passive, plain HTTP GET)

### 1. Archive.org advancedsearch — markers in uploaded items
Endpoint: `https://archive.org/advancedsearch.php?q=<urlencoded>&fl[]=identifier&fl[]=title&fl[]=date&rows=50&output=json`
| query | numFound | verdict |
|---|---|---|
| `uqscan` | 0 | **negative** |
| `AGEDATA23` | 0 | **negative** |
| `getPoiInfo` | 0 | **negative** |
| `sub_poi_navi` | 5 | **negative** — all 5 are CIA Reading Room OCR false positives (tokenizer split `SUB…POI`) |
| `deepsearchqa` | 4 | **negative** — Kimi model-card/leaderboard noise only: `github.com-MoonshotAI-Kimi-K3_-_2026-08-06_10-17-28`, `github.com-ApodexAI-AgentHarness_-_2026-06-08_15-56-45`, `iaai-hf-moonshotai-kimi-k2--5`, `iaai-hf-moonshotai-kimi-k2--6`. No traces. |

Raw JSONs: `ia_*.json` in this dir. (Note: `ia_deepsearchqa.json` was lost to a /tmp
flakiness mid-hunt; its 4 hits are transcribed above.)

### 2. Wayback CDX — archived agent artifacts
Endpoint: `https://web.archive.org/cdx/search/cdx?url=<pattern>&output=json&limit=N&collapse=urlkey&fl=timestamp,original,statuscode[,mimetype]`
| query | captures | verdict |
|---|---|---|
| `amap-pc-ssr.amap.com/detail/*` | 9 | **confirmed** — all `B001C94YUZ`, 2026-10-04 01:08–01:11 UTC burst (see headline) |
| `amap-pc-ssr.amap.com/ssr/place/*` | 14 | **confirmed** — 13 place IDs, 2026-09-28→10-04 (see headline) |
| `amap.com*` (root) | 100 (limit) | **negative** — spam/junk URL noise, nothing agent-shaped |
| `webhook.site/22b6b8c8-…/` inbox | 0 | **negative** |
| `webhook.site/774cf5e1-…/` inbox | 0 | **negative** |
| `02371c70-….webhook.site/*` | 0 | **negative** |
| `r.jina.ai/https://amap-pc-ssr.amap.com/ssr/place/B001C94YUZ*` | 0 | **negative** |

Raw JSONs: `cdx_*.json` in this dir. Raw WARC fetch pattern (works, detect gzip):
`https://web.archive.org/web/<timestamp>id_/<url>`.

### 3. Common Crawl index (CC-MAIN-2026-39, Sep 2026 crawl)
Endpoint: `https://index.commoncrawl.org/collinfo.json` → `https://index.commoncrawl.org/<ID>-index?url=<pattern>&output=json`
| query | result | verdict |
|---|---|---|
| `*AGEDATA23*` | `{"message":"No Captures found for: *AGEDATA23"}` | **negative** |
| `*getPoiInfo*` | No captures | **negative** |
| `*sub_poi_navi*` | No captures | **negative** |
| `*uqscan*` | **504 Gateway Time-out** | **inconclusive** — mid-string wildcard too expensive; not a negative |
| `*deepsearchqa*` | **504 Gateway Time-out** | **inconclusive** — same |
| `url=webhook.site/*&filter=url:.*uqscan.*` | No captures (filter form not honored by this index) | **negative / method note** |

Raw: `cc_*.json` in this dir. Retry path: per-domain/prefix queries
(e.g. `url=httpbun.com/anything/*`) instead of mid-string wildcards, or the columnar index.

### 4. Public bucket listings — marker-derived names ONLY (no enumeration)
GCS path-style `https://storage.googleapis.com/<bucket>` and virtual-hosted
`https://<bucket>.storage.googleapis.com/`; S3 `https://<bucket>.s3.amazonaws.com/`
(parse `<Code>NoSuchBucket`). 404 = no bucket; 403 = exists, private.
| bucket | GCS | S3 | verdict |
|---|---|---|---|
| `deepsearchqa` | 404 | 404 NoSuchBucket | **negative** |
| `uqscan` | 404 (virtual-hosted; path-style flaked 000) | 404 NoSuchBucket | **negative** |
| `agedata23` | 404 | 404 NoSuchBucket | **negative** |
| `dsqa` | **403** | 404 NoSuchBucket | **candidate, unverifiable** — GCS bucket exists but private; owner unattributable passively |
| `amap-poi` | 404 | 404 NoSuchBucket | **negative** |
| `gzhosp` | 404 | 404 NoSuchBucket | **negative** |
| `deepsearch-qa` | 404 | 404 NoSuchBucket | **negative** |

Note: several first-attempt probes returned `000` (egress flake); all resolved on retry
except via the alternate URL style. No bucket yielded a listing.

### 5. Web search — distinctive strings
| query | verdict |
|---|---|
| `"uqscan"` | **negative** — USCAN scanner PDF, typosquat list, TikTok; zero tag hits |
| `"AGEDATA23"` | **negative** — HHS/ADA aging-doc noise |
| `"sub_poi_navi" amap` | **negative** — GE Vernova docs, MapNav manual |
| `"qingdaomuseum" OR "henanmuseum_20261005" OR "wenzhou-museum-20261004"` | **negative** — generic museum PDFs only |
| `deepsearchqa amap agent eval dataset` | **negative for our link** — DeepSearchQA is a public Google eval (leaderboards, Medium explainers); no Amap connection anywhere |
| `"GZHOSP" guangzhou hospital` | tag semantics only (see above), **negative** for uploads |
| transfer.sh / file.io / gofile / nfile links in corpus | **none found** — fleet uses httpbun + webhook.site + jina, not file drops |

---

## NOVEL ENDPOINTS / REUSABLE PATTERNS (documented for reuse)
1. IA advancedsearch: `https://archive.org/advancedsearch.php?q=<q>&fl[]=identifier&fl[]=title&fl[]=date&rows=50&output=json` — searches item metadata + full text; `q` is Lucene (`text:` default).
2. Wayback CDX: `https://web.archive.org/cdx/search/cdx?url=<prefix/*>&output=json&limit=N&collapse=urlkey&fl=timestamp,original,statuscode,mimetype` — `collapse=urlkey` dedupes; CDX is URL-keyed (no content search).
3. Raw WARC bytes: `https://web.archive.org/web/<ts>id_/<url>` — `id_` skips rewriting; response may be gzip (`\x1f\x8b`) → decompress before parsing.
4. CC index: `https://index.commoncrawl.org/collinfo.json` lists crawls; query `https://index.commoncrawl.org/<ID>-index?url=<pattern>&output=json` — **avoid mid-string `*kw*` wildcards (504); use domain/prefix patterns**.
5. GCS bucket probe: `https://storage.googleapis.com/<b>` (404/403/200-XML); alt `https://<b>.storage.googleapis.com/`.
6. S3 bucket probe: `https://<b>.s3.amazonaws.com/`; parse `<Code>` (`NoSuchBucket` vs `AccessDenied`).
7. Dead-drop receiver (new): `https://httpbun.com/anything/gcresult?d=<urlencoded meta>&z=<epoch_ms>` and `/anything/gcerror` — agent beacon endpoint; worth CDX-querying `httpbun.com/anything/*` in future.
8. Jina relay form: `https://r.jina.ai/<target-url>` (+ `X-Cache-Tolerance` header on GCP-cache probes).

## OPEN QUESTIONS
1. Who issued the Wayback Save-Page-Now bursts — the agent fleet itself (archive-as-you-go) or a third-party observer? (`?w=retry2` smells agent-side.)
2. Content of the other 11 archived `ssr/place/*` captures (only 2 of 14 fetched).
3. GCS `dsqa` bucket (403): owner unattributable via passive means — flag, do not pursue intrusively.
4. Common Crawl 504s on `*uqscan*` / `*deepsearchqa*`: retry with per-domain queries (`url=httpbun.com/anything/*`, `url=webhook.site/*`) or columnar index.
5. Do the archived captures' WARC records contain request headers revealing the archiver's UA/IP-class? (Response records only; revisit headers not stored — likely dead end, noted.)
6. transfer.sh/file.io/gofile/nfile: zero marker links found — is the fleet's dead-drop set really just httpbun+webhook.site+jina, or are file drops under different names?

## EVIDENCE FILES (this dir)
`buckets-archives.md` (this file), `ia_*.json`, `cdx_*.json`, `cc_*.json`.
Decoded probe bytes live in the analysis above; source report:
`~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/raw/report_f2a45ccb-fca8-43f6-a6e5-38f088582e79.json`.
Scratch: `~/workspace/.hunt-scratch/` (decompressed WARC HTMLs `wbm_*.dec.html`).
