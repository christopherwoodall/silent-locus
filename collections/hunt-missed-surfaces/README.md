# Hunt: what has Transluce missed and where do we find it

Charter: find MORE sites/surfaces the agents could have used, beyond Transluce's coverage
(arquivo.pt captures, urlquery, allorigins, corsfix, r.jina.ai, markdown.new, sirjosh proxy,
test.cors.workers.dev) and beyond the 23 surfaces in `collections/re-hunt-relays/`.

## Lanes
- `enumerate/` — Lane 1: new-surface inventory (research), graded A–D by keyless queryability.
- `probe/` — Lane 2: fingerprint probing of queryable surfaces, full probe log.
- `hot-leads/` — Lane 3: urlscan.io deep queries + Common Crawl CC-MAIN-2026-25 exact-URL CDX.

## Conventions
- `state.json` per lane (watermarks, counts, status); raw logs in `data/`.
- Polite: ≤1 req/2s per host. Blocks recorded, never retried aggressively.
- Honest negatives are findings. No invented rows. Agents/infra scope only.
- Commits by coordinator on `local`; no pushes, never `main`.
