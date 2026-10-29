# Hunt Lane 8 — Docker Hub (2026-09-27)

## Verdict: negative — no GemStuffer tradecraft on Docker Hub

Read-only sweep of Docker Hub's public v2 search API
(`https://hub.docker.com/v2/search/repositories/?query=...`), ~1.2s pace, no
auth, no logins. Metadata only — no image blobs pulled.

## Battery 1 — campaign-specific names (28 queries)

Every distinctive campaign gem name returned **count=0**:
`tryf3zz`, `southwarkssrfhack`, `southfetchprobe42`, `londonyardtestabc`,
`wandsworthprobe1778551714`, `uxjinalamb2`, `slnleaker4`, `probejiqptzco`,
`yardbreaker`, `zzsouthrunner`, `trya1zz`, `zzjina`, `chatoaifetch`.
No squats, no mirrors under campaign names.

## Battery 1 — payload/beacon markers

- `r.jina.ai`: 0
- `modern.gov`: 0
- `county.json`: 0
- `yardopts`: 0
- `go-import`: 5,107 (tokenized noise — matches "import"; zero literal
  `go-import` strings in the 25 sampled descriptions)
- `builder alive`: 57,725 (phrase noise; zero literal matches in sampled
  descriptions, zero suspicious repo names)
- `YARD RAN`: 32,282 (noise; same — zero literal/suspicious)
- `yard exploit`: 3,246 (noise; same)

## Battery 2 — target-name and adjacent queries

- `southwark`: 1 hit — `johankustner/southwark-dab-dev` (499 pulls).
  Tags: single `latest`, pushed **2025-04-29**. Unrelated, predates campaign.
- `lambeth`: 5 hits — all personal/test repos (`lambeth101/tekk-match-server`,
  `lambeth101/chess-endgame-ai-agent`, `678876678876/ofbiz-suspension-lambeth`,
  `aklambeth/gitlist`, `kevinlambeth/testingdockerrepo`). None campaign-related.
- `wandsworth`: 1 hit — `pritam290/wandsworth-scrapper` (543 pulls, no
  description). Tags: single `latest`, pushed **2026-06-22** — four days
  *after* the Jun 18 campaign boundary, misspelled "scrapper", no campaign
  markers. Coincidence.
- `goimport` (no hyphen): 26 hits — all legitimate `goimports`
  (golang.org/x/tools) CI images (`cytopia/goimports`, `unibeautify/goimports`,
  etc.). Noise.
- `jina-ai`: 12,687 — the entire legitimate Jina ecosystem
  (`jinaai/jina`, `airbyte/source-jina-ai-reader`, embeddings/rerankers).
  None reference the campaign's laundering usage.
- `rubydoc`: 17 hits — mostly "my first docker repo" tutorials.
  `docmeta/rubydoc.info` ("Runs rubydoc.info!") is the legitimate site
  deployment; tags date to **2019-07/12**. Ancient, unrelated to the campaign.

## Window check (May 5 – Jun 18 2026)

No repo with any campaign marker was pushed inside the window. The only
target-name repo pushed in 2026 (`pritam290/wandsworth-scrapper`,
2026-06-22) falls outside it and carries no campaign fingerprints.

## Caveats

- Docker Hub search is keyword/tokenized, not regex or exact-phrase: a
  literal `<meta name="go-import">` buried in a long README/description that
  the index doesn't surface wouldn't be found this way. A true content sweep
  would need bulk metadata (not attempted).
- Full descriptions were not fetched for all 57k+ `builder alive` noise hits;
  only the top-25 relevance samples per query were inspected, screened for
  literal markers and suspicious name grammars.

## Bottom line

Docker Hub joins deps.dev, PyPI, npm, urlscan.io, urlquery, and the doc
pipelines as a clean negative. The campaign's observable footprint remains
RubyGems-only (Diffend + Wayback as the surviving sources).
