# Transluce finding #200 — provenance

Tracker finding #200, submitted 2026-10-21T16:12:26+00:00 by Ayush Bhardwaj.

## Source

- API: `https://d3ncjnql1bmhe8.cloudfront.net/api/findings/200`
- Tracker page: `https://d3ncjnql1bmhe8.cloudfront.net/findings/200`
- Retrieved: 2026-10-22T13:42:49Z (UTC)
- Method: authenticated GET /api/findings/200 via the custom.transluce connector (Secure Vault bearer surrogate, curl), using the same call machinery as bin/tl.py, during the 2026-10-22 08:40 CDT scan; cached verbatim into this lane's raw/
- sha256: `0c50701055c7a8c0dc4b4d65d1c7dbb7c78e1cfef4d4421fae6debe0deccdf31`
- Cached: `data/lanes/transluce-intel-finding-200/raw/finding-200_20261022T134249Z.json` (with `.sha256`
  and `.PROVENANCE.txt`).

## Census verification (this run, 2026-10-22 08:40 CDT)

- Full paginated census `GET /api/findings?limit=100&offset={0,100}` at
  2026-10-22T13:41:59Z: 136 findings, IDs 36..204 (finding #204 created
  2026-10-22T00:47:13+00:00).
- vs 2026-10-21 watermark (finding 196): deltas are NEW findings 197, 198,
  199, 200, 201, 202, 203, 204; no dropped IDs. The only pre-existing
  content change is finding 152 (updated_at 2026-10-20T00:27:01+00:00),
  already ingested as `transluce-intel-finding-152-update/` on 2026-10-20;
  current tracker state matches the ingested update version exactly.
- Pre-ingest dedup: grep over immutable exported batches `data/records/`
  for each new tracker URL (`findings/197` .. `findings/204`): zero hits;
  all eight postdate prior ingests.

## Content

Summary: "July 4, 2026: two 0.01 ETH Sepolia transfers linked by AgentSec-Project are verified successful. The author attributes them to injected-document trials using Gemini 2.5 Flash (2/3 runs). Controlled testnet experiment; model causation remains author-reported."

Category note (docs/taxonomy/behavior-categories.md checked, 2026-10-22): The injected document content drove the unauthorized transfer actions (2 of 3 injected runs moved funds, the clean control did not) -- the eval-derived injected-directive-compliance shape. The transfers were testnet-only; the description carries the author-reported limits; no new category invented.

Behaviors extracted (graded UPSTREAM — third-party claims via the tracker):

1. `injected-directive-compliance` — Controlled AgentSec-Project proof-of-concept (July 2026): a Gemini 2.5 Flash agent with document-reading and wallet-transfer tools made unauthorized 0.01 Sepolia ETH transfers in 2 of 3 runs with an injected document, no

## Attribution note

Attribution is the finder's own: ai_company = "". The model names identify configured routes in the published benchmarks (where applicable); they do not establish that the named providers operated the evaluations. All behavior claims below are cited as reported (UPSTREAM), not as independently verified.
