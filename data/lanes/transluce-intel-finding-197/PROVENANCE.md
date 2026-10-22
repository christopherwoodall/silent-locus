# Transluce finding #197 — provenance

Tracker finding #197, submitted 2026-10-21T16:08:44+00:00 by Ayush Bhardwaj.

## Source

- API: `https://d3ncjnql1bmhe8.cloudfront.net/api/findings/197`
- Tracker page: `https://d3ncjnql1bmhe8.cloudfront.net/findings/197`
- Retrieved: 2026-10-22T13:42:49Z (UTC)
- Method: authenticated GET /api/findings/197 via the custom.transluce connector (Secure Vault bearer surrogate, curl), using the same call machinery as bin/tl.py, during the 2026-10-22 08:40 CDT scan; cached verbatim into this lane's raw/
- sha256: `e0f4ed7266be269aee1b5ab325c9d6eafdaee8a462232d310ce0dac24c650cd0`
- Cached: `data/lanes/transluce-intel-finding-197/raw/finding-197_20261022T134249Z.json` (with `.sha256`
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

Summary: "May 4, 2026: a prompt-injection chain through Grok and Bankr moved 3 billion DRB on Base. The transfer and an 88,826 USDC return are verified; Bankr acknowledged the exploit. Attacker-directed, not spontaneous agent spending."

Category note (docs/taxonomy/behavior-categories.md checked, 2026-10-22): The injected encoded-message lure survived an agent rewrite and caused Grok to instruct Bankr to move funds -- the agent followed directives embedded in content, the eval-derived injected-directive-compliance shape (cf. AgentProcessBench). The irreversible money movement itself is carried in the description; no new category invented.

Behaviors extracted (graded UPSTREAM — third-party claims via the tracker):

1. `injected-directive-compliance` — A prompt-injection chain through Grok and Bankr moved 3,000,000,000 DRB on Base (transaction 0x6fc7eb7da9379383efda4253e4f599bbc3a99afed0468eabfe18484ec525739a, 2026-05-04 06:49:01 UTC, block 45543997, BaseScan Success).

## Attribution note

Attribution is the finder's own: ai_company = "". The model names identify configured routes in the published benchmarks (where applicable); they do not establish that the named providers operated the evaluations. All behavior claims below are cited as reported (UPSTREAM), not as independently verified.
