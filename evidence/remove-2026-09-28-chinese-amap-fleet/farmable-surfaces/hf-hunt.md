# HuggingFace operator-marker + Amap-fleet dataset hunt — hf-hunt.md

**Date:** 2026-10-05 UTC (2026-10-04 ~22:05 CDT)
**Method:** read-only public Hugging Face Hub API via `curl` (python `huggingface_hub` broken on this VM per `~/workspace/TOOLS.md` — IPv6 NO_PROXY parsing). Endpoints: `https://huggingface.co/api/{datasets,models,spaces}?search=...&limit=100`, plus per-repo metadata and one README resolve. No login, no downloads of data files.
**Raw:** `farmable-surfaces/raw/hf/` (`search.sh` reproduces all sweeps).
**Not pushed** (per task directive).

## 1. Operator-marker searches — all NEGATIVE

Queries `uqscan`, `uqcors`, `uqtag`, `sub_poi_navi`, `lhr.life`, `httpbun`, `urlquery` returned **zero hits** on datasets, models, and spaces alike (empty JSON arrays across all three endpoints).

Queries with non-empty results were **false positives only**:

| Query | Endpoint | Hits | Verdict |
|---|---|---|---|
| `is.gd` | datasets | 3 | electricsheepafrica WorldBank datasets — substring "gd" in names (`...-gd-wbl`), not the shortener |
| `is.gd` | models | 4 | startlux-models `gdn-*` gated-deltanet models — "gdn" ≠ "is.gd" |
| `is.gd` | spaces | 1 | `KagChi/ISGDModelDemo` — ISGD (in-place stochastic gradient descent) demo |
| `openai_research` | models | 2 | `cmu-rag-research/llama3_mnli_openai_3_shots`, `bananamind-research-community/openai-chatgpt-two` — generic OpenAI+research word-pair matches |
| `openai_research` | spaces | 5 | generic OpenAI research-assistant/whisper Spaces (`prabha12/ResearchAssistant_OpenAI`, `adrianmf94/deep_researcher_openai_sdk`, …) |
| `webhook.site` | spaces | 0 | zero |

**No model card anywhere on HF mentions our markers**, and none of the returned artifacts describe agent-eval infrastructure with urlquery/webhook exfil patterns. The operators have not staged their markers on the Hub — or use private repos.

## 2. Amap fleet dataset hunt — NOT SURFACED (closest miss identified)

`datasets?search=amap` → **2 datasets only**:

1. **`TC130/amap_mcp`** (2025-11-12, 0 likes, 34 downloads) — single `amap_answer_full.jsonl`; an Amap MCP-server eval-answer file. Benign.
2. **`Stephen3zero24/amap-2000-candidates-v1`** (2026-08-14, 0 likes, 47 downloads) — **closest thematic hit, but disclaimed synthetic.** Card: "Amap 2,000 Deterministic Mock App Candidate Trajectories v1" — MobileGym-Harmony 高德 *Mock App* GUI-agent candidate trajectories (2 task families: `chain_1_route_mode` route-viewing, `chain_2_nearest_compare`; 22,667 actions, 22,836 synthetic 360×800 JPEG screenshots, tar.gz shards). README states explicitly: "本包不是真实高德采集" (this package is NOT real Amap collection) — not real screenshots, not real users/accounts/locations/orders/navigation behavior; `PUBLICATION-SAFETY.md` + `RELEASE-MANIFEST.json` + content checksums included. This is **agent-eval infra adjacent** (Chinese map-app GUI agents) but it is a synthetic benchmark pack, not the fleet's field-built entrance dataset. Watchlisted, not a hit.

Further sweeps — `datasets?search=` for `entrance`, `navi`, `navigation`, `"poi entrance"`, `"poi navigation"`, `"entrance navi"`, `sub_poi`, `entrance-share`, `导航数据集`, `map navigation agent` — filtered for `zh` tags / CJK / China / POI / gaode: **only 3 China-candidates**, all unrelated:
- `qleandataset/video-multinational-gait-entrance` / `video-japanese-gait-entrance` — building-door *gait videos*, not POI entrances.
- `CyberHarem/navia_genshin` — Genshin Impact character image set (name substring "navi").

CJK queries (`高德`, `入口`, `高德地图`, `poi导航`) returned **empty** — HF's `search=` does not reliably handle CJK, so absence is weak evidence. `models?search=amap` → 11 hits, all false positives (amapiano music models/spaces, org `amaps` medical-LoRAs, `AmapVoice/PilotTTS` TTS); `wangmingxinthu/amap_spiderwam_ckpt` looked interesting but is a **LIBERO robotics VLA checkpoint** (dino_s / `libero_dino_s_2cam_224` weights), unrelated. `spaces?search=amap` → 7 hits, all amapiano substring.

**Assessment:** as of Oct 2026 the fleet's Amap POI entrance-navigation dataset has **not been published on Hugging Face under any discoverable name/tag**. Either it isn't published, it lives under a non-obvious org/name, or it's behind a private repo. The fleet remains a collection operation with no public output.

## 3. Spaces infra — delta vs prior collection

Prior work `data/2023-11-14-hfspace-proxies/` (15 spaces: `TheNacken/python-cors-proxy` — the only `in_corpus` tie — plus 14 CORS/jina/url-to-markdown shape-matches, refreshed 2026-09-29) was checked first, **not re-enumerated**. Fresh `search=` runs for `cors proxy`, `fetch-proxy`, `url to markdown`, `webhook receiver`, `tunnel dashboard`, `requestbin`, `webhook.site` surfaced **6 new shape-matches not in the prior collection** — pattern_match only, no operator-marker evidence:

- `lmtworking/HTTP_FetchProxy` (2025-12-27) — generic fetch proxy
- `13ze/url-to-markdown-v2` / `13ze/url-to-markdown-v3` (2025-04-16/17) — url→markdown shims
- `tonyassi/webhook-receiver-dev` (2025-03-12), `Inflammable1230/webhook-receiver` (2026-05-31), `zawad1232/webhook-receiver` (2026-08-12) — webhook receivers

All previously enumerated proxy spaces still resolve via search (no mass deletions observed in the result sets). `tunnel dashboard` and `requestbin` returned empty; no HF Space resembles a tunnel dashboard.

## 4. Model cards — negative

No model card mentions our markers. `models?search=` for every operator marker: empty or false positives (§1). No card describes agent-eval infra with urlquery/webhook exfil grammar.

## Caveats

- Hub `search=` is keyword-based and incomplete (multi-word queries like `"poi entrance"` returned empty JSON — quoting may not behave as expected); private repos are invisible; deleted repos don't appear.
- CJK search terms unreliable on this endpoint — the Amap-fleet absence is a weak negative.
- No data files downloaded; dataset-card text only for the two amap datasets (README pulled for the candidates-v1 pack).

## Net result

**No new operator traces on Hugging Face.** Zero marker hits across datasets/models/spaces; the Amap fleet's entrance dataset is not publicly on the Hub as of 2026-10-05; spaces-infra delta is 6 generic new shape-matches with no campaign tie. Raw sweeps preserved in `raw/hf/` for future re-runs.
