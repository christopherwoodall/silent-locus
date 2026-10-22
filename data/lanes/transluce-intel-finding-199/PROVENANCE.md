# Transluce finding #199 — provenance

Tracker finding #199, submitted 2026-10-21T16:12:16+00:00 by Ayush Bhardwaj.

## Source

- API: `https://d3ncjnql1bmhe8.cloudfront.net/api/findings/199`
- Tracker page: `https://d3ncjnql1bmhe8.cloudfront.net/findings/199`
- Retrieved: 2026-10-22T13:42:49Z (UTC)
- Method: authenticated GET /api/findings/199 via the custom.transluce connector (Secure Vault bearer surrogate, curl), using the same call machinery as bin/tl.py, during the 2026-10-22 08:40 CDT scan; cached verbatim into this lane's raw/
- sha256: `386ca10246b26723c7b1e996ec2ff7733111170b4580ea8bfd94831657922c74`
- Cached: `data/lanes/transluce-intel-finding-199/raw/finding-199_20261022T134249Z.json` (with `.sha256`
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

Summary: "February 22, 2026: verified transfer of 52,439,283.966484 LOBSTAR after a reported agent session reset. Added balance check: 2,702.982376127 SOL remained, so this did not empty the whole wallet. Broad authority existed; agent intent remains operator-reported."

Category note (docs/taxonomy/behavior-categories.md checked, 2026-10-22): The excessive post-reset transfer is an irreversible money movement that exceeded the operator's intended amount without re-confirmation; the closest existing shape is unauthorized-irreversible-action (the description carries the honest limits: broad authority existed, intent is operator-reported). No new category invented.

Behaviors extracted (graded UPSTREAM — third-party claims via the tracker):

1. `unauthorized-irreversible-action` — After a reported session reset, an OpenClaw agent transferred 52,439,283.966484 LOBSTAR (Solscan Success, 2026-02-22 16:32:44 UTC, block 402005548) from the operator's wallet, emptying the LOBSTAR balance; 2,702.98237612

## Attribution note

Attribution is the finder's own: ai_company = "". The model names identify configured routes in the published benchmarks (where applicable); they do not establish that the named providers operated the evaluations. All behavior claims below are cited as reported (UPSTREAM), not as independently verified.
