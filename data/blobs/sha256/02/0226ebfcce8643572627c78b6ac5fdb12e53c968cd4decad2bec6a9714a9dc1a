# HUNT LANE 9 — HuggingFace Hub — 2026-09-27

**Verdict: CLEAN.** No GemStuffer fingerprints on HuggingFace Hub across models, datasets, or Spaces.

## Method

Read-only public HF Hub API (`https://huggingface.co/api/{models,datasets,spaces}?search=...`), no auth, no downloads. First pass at ~1/s was tarpitted by the API (~17s/req); reran with a 5-worker pool after deduping completed rows. Zero failed requests in the final run.

## Coverage

- **185 campaign gem names** (extracted from `data/gem-iocs-2026-09-27.jsonl` Diffend source_links) × 3 endpoints = 555 queries. **All zero hits.** None of the campaign's names exist as HF repos.
- **14 pattern queries** × 3 endpoints = 42 queries: `go-import`, `zzjina`, `oaitest`, `tryf3zz`, `southwarkssrfhack`, `londonyardtestabc`, `southfetchprobe42`, `yard exploit`, `builder alive`, `YARD RAN`, `r.jina.ai`, `s.jina.ai`, `modern.gov`, `county.json`.
- **6 July-7-wave supplemental queries** × 3 endpoints = 18 queries (added after the JFrog GemStuffer report surfaced via lane 11): `oast.online`, `webhook.site`, `southpxdatapp6pi`, `zzjinavcs`, `southwarkssrfhack`, plus `mod ` (discarded — see below).
- **Total: 615 queries, 0 errors.**

## Hit adjudication

| Query | Endpoint | Hits | Adjudication |
|---|---|---|---|
| `go-import` | models | 2 | `JCener/import-google-takeout-*` — 2023 Google Takeout import repos, token match on "import". Unrelated. |
| `oaitest` | spaces | 1 | `OAITest/X` — plain Gradio test space by the OAITest org, created 2024-05-13 (a year pre-campaign), 0 likes. Fuzzy match. Unrelated. |
| `r.jina.ai` | models | 5 | jina-reranker / jinaai-reader-lm models — the legitimate Jina AI ecosystem (same pattern as the npm lane's finding). Unrelated. |
| `s.jina.ai` | models | 2 | jina-embeddings-v2 models — legitimate. Unrelated. |
| `modern.gov` | models | 3 | `gte-modernbert-*` models — token split on "modern"+"bert"/"gov". Unrelated. |
| `modern.gov` | spaces | 2 | "modern government UI" demo spaces — token noise. Unrelated. |
| `mod ` | all | 20×3 | Discarded: tokenizes to "model(s)", pure noise. |

Beacon strings (`builder alive`, `YARD RAN`, `yard exploit`), the laundering domains as URL markers, `county.json`, `oast.online`, `webhook.site`, and the July-7 dead-drop name `southpxdatapp6pi`: **all zero everywhere, including Spaces** (the hosted-compute surface — extra attention paid, nothing found).

No repo was created in the May 5–Jun 18 2026 window among any hit; all adjudicated hits predate or postdate it with unrelated content.

## Caveats

- HF Hub search is tokenized/fuzzy, not exact-phrase: short markers can't be matched literally, and full model-card/readme body text is only shallowly indexed. A marker buried deep in an unindexed card body would not surface.
- This was a metadata/index-layer sweep — no repo contents, model weights, or datasets were downloaded.

## Bottom line

The operator class's footprint remains RubyGems-only across every lens so far. HuggingFace — the most agent-native platform in the hunt — shows zero trace of the campaign's names, beacons, laundering URLs, or the July-7 wave's markers.

Raw sweep logs: `/tmp/lane9/results.jsonl` (615 rows), `/tmp/lane9/results_july7.jsonl` (18 rows). Ephemeral.
