# PROVENANCE — hfspace-proxies dataset

**Source:** Hugging Face Hub public Spaces API (`https://huggingface.co/api/spaces`), public
Space repos (README/Dockerfile/app code), and public web search.
**Retrieved:** 2026-09-27/28 (recon lane B).
**Method:** read-only. Hub API `?search=` queries for `cors-proxy`, `cors_proxy`,
`jina`, `reader-proxy`, `proxy`, `markdown-reader`, `web-reader`, `url-to-markdown`,
`jina-reader`, `fetch-markdown`; per-space detail + README fetch; repo file listing;
grep of the collusion-wiki corpus for `*.hf.space` references.

**What this is:** an enumeration of proxy-shaped HF Spaces relevant to the
agent-laundering tradecraft (generic CORS `?url=` shims, jina-reader clones).
15 Spaces staged in `spaces.jsonl`.

**Tie-strength labels** (in `spaces.jsonl`, field `tie_strength`):
- `in_corpus` — the Space URL literally appears in the collusion-wiki corpus
  (1 Space: `TheNacken/python-cors-proxy`, 3 uses).
- `pattern_match` — matches the proxy-shape pattern by name/function only;
  NO evidence of swarm use.

**Keep-all + annotate policy applies:** no records dropped; swarm linkage is
annotated per record, never assumed. Nothing here identifies operators —
Space owners are public Hub usernames as published by Hugging Face.

**Limitations:** Hub search is keyword-based and incomplete; private Spaces are
invisible; app behavior verified by code read only for `TheNacken/python-cors-proxy`
(the rest are shape-matched, shims unverified). Live Spaces change over time —
re-run the Hub queries to refresh.

## Refresh 2026-09-29 (authorized)
- Re-ran the Hub `?search=` sweep (12 keywords: the original 10 plus `cors-anywhere`
  and `urltomarkdown`, both defensible proxy-shape terms). Read-only, ~2s pacing.
  239 unique public Spaces returned; 224 not already held.
- Tight name-shape filter (space name, not owner) for CORS-shim / jina-reader /
  fetch-markdown / web-reader shapes: 25 shortlisted. Per-space detail + README +
  repo tree fetched; app code read for 9 (Dockerfile/app.py/server.py) to confirm
  fetch-proxy behavior rather than name-only matching.
- **23 new Spaces added** (raw + schema rows; `@timestamp` = space.created;
  `event.created` = 2026-09-29T16:15:04Z run):
  - 5 soiz1/CORS-PROXY forks: `AndiGr`, `Jynx88`, `alx1880`, `markmcfc`,
    `public-soiz1` (the 2026-09-27 row already anticipated these forks).
  - 12 cors-anywhere clones: `bobwatcherx/corsanywhere{,2..6}`,
    `darenx/corsanywhere{,2..6}` (node; the `2..6` variants are titled
    "Poophdserver" — recorded in `shape`, not treated as evidence of anything).
  - 2 url-to-markdown: `13ze/url-to-markdown-v2` (playwright+markdownify,
    code-read), `13ze/url-to-markdown-v3` (sibling).
  - 4 web readers: `jasonhan888/web-reader` (hectorqin/reader image),
    `santhoshsharuk/web-article-reader-api` (FastAPI POST /convert/ {url}),
    `G-W/web-article-reader` (gradio fetch+readability),
    `sunnyzhifei/web-reader-ai` (FastAPI crawler) — all code-read.
- **2 excluded with reasons:** `JannisJulian/tts-web-reader` (Kokoro TTS backend,
  not a fetch proxy); `Zangtungtung/mediaflow-proxy` (HLS/DASH media-stream proxy,
  not web-fetch laundering shape). ~200 other candidates excluded: `openai-reverse-proxy`
  / `oai-proxy` family (API-key proxying, different tradecraft), `jina-embeddings*`
  (embedding models), owner-username substring matches.
- Corpus check: all 23 grepped against `data/2026-05-17-collusion-wiki` (live
  `*.hf.space` hostname + space id) — **zero hits; all 23 labeled `pattern_match`**.
  `in_corpus` remains only `TheNacken/python-cors-proxy`.
- Dedupe: 15 held space.ids skipped; 0 duplicates among the 23.
- Collection now 38 events / 38 raw rows. SHA256SUMS regenerated.

## Raw-layer restoration 2026-09-29
- The raw source capture `spaces.jsonl` (15 pre-schema flat records, the input
  consumed by `temp/backfill_w2.py` line 251, `("data/hfspace-proxies/spaces.jsonl", t_hfspace)`)
  was dropped during the 84edfb3 "Update data directory layout" commit
  (deleted there, not renamed) and replaced by the backfilled `hfspace-proxies.jsonl`
  (renamed to `events.jsonl` in 21312cf). It was never on disk at
  `data/2023-11-14-hfspace-proxies/`.
- Recovered byte-identical from git history (`af5c6d9:data/hfspace-proxies/spaces.jsonl`;
  no intermediate modifications between af5c6d9 and 84edfb3) and staged as
  `raw/spaces.jsonl`. All 15 `events.jsonl` rows (venue_probe, one per
  `space.id`) are covered by the 15 restored raw rows; SHA256SUMS regenerated
  and `sha256sum -c` green. This collection is no longer a raw-missing
  exception.

## Schema backfill 2026-09-29
- Transform: `temp/backfill_w2.py`. Pre-schema flat records brought onto the
  shared schema. Renames: `url` -> `source_url`; `id`, `live`, `sdk`,
  `created`, `modified`, `likes` -> `labels` as `space.id`, `space.live_url`,
  `space.sdk`, `space.created`, `space.modified`, `space.likes`; `shape`,
  `swarm_tie`, `tie_strength` -> `labels` unchanged.
- `@timestamp` = `space.created` (Hub Space creation date, date-only ->
  midnight UTC); `labels.timestamp_source = "labels:space.created"`.
- record_kind: `venue_probe` (enumeration/probe of proxy-shaped HF Spaces as
  potential laundering venues).
- fingerprint identity string: `sha256(space.id)` — the Hub Space id
  (`owner/name`) is the natural unique key.
- event.dataset = `hfspace-proxies`; event.created = backfill run time.

## Factum ingest 2026-10-09 (Batch 3, lane-ingest worker)

- Ingested as 38 `infra.proxy_instance` observations + 38 `source` records.
- Batch: `data/records/a3892bb8b0824e059adb92512d167785/`.
- Lane record: `lane_f2a273fa0e3d4131bec8807d2f9021b8`; all records carry
  tag `{"lane": "2023-11-14-hfspace-proxies"}`.
- Transform: `data/lanes/2023-11-14-hfspace-proxies/build_bundle.py`.
- Dedup: 29 `match --text --mode fuzzy` queries (6 shape terms + 23 owner
  names) against the Factum corpus — all `not_found`; batch-internal
  uniqueness asserted on all 38 space ids.
- Host mapping: 24 hostnames from observed `space.live_url`; 14 derived from
  the HF Spaces URL pattern (verified against all 24 observed) and flagged
  in record notes. Liveness unprobed; `access` is "open" only for the
  code-read `TheNacken/python-cors-proxy`, "unknown" elsewhere.
- No edges created during ingest (separate pass).
- Legacy directory renamed to `evidence/remove-2023-11-14-hfspace-proxies/`
  after ingest; original bytes unchanged.
