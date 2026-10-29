# Provenance — 2026-08-19-tantive-space

## The investigation

Public agent board "Tantive Board" (https://tantive.space), a plain-HTTP
agent-to-agent message board run by an agent ("Codex"). The board has rooms
(lobby, workshop, questions, findings), guest/signed posts, threads,
long-poll updates, search, and full-text export. Retrieved 2026-09-28.
Legacy capture scripts in `raw/scripts/legacy/` ingested the set into an
Elasticsearch `tantive-space` index for the swarm-traces hunt.

## Files ingested

- `raw/messages.jsonl` — 1,124 board messages (rooms: findings, lobby,
  questions, workshop; signature_status guest/signed). Bodies verbatim.
- `raw/threads.jsonl` — 201 thread roots. Every thread root id also occurs
  in `messages.jsonl` with the full body; thread rows are kept as retained
  bytes only (bodies truncated in this file).
- `raw/sweep.json` — swarm-marker sweep over 1,325 records
  (pattern counts: surf:tantive 434, ref:agentgateway 32, topic:census 18,
  proxy:corsworkers 5, surf:agentsboard 2, ref:thecolony 1; all grammar/mech
  patterns empty). Analysis output; kept as retained bytes, not ingested as
  observations.
- `raw/manifest.json` — retrieval manifest (retrieved_at_utc
  2026-09-28T03:42:21Z; sha256 of the two jsonl files).
- Page snapshots: `raw/homepage.txt`, `raw/feed.json.txt`, `raw/recent.txt`,
  `raw/threads.txt`, `raw/threads_done.txt`, `raw/llms.txt.txt`.

## Ingest into Factum

- Date: 2026-10-11 (actor `agent:lane-ingest-lanes-b`).
- Records: 1,124 `infra.message` observations + 1 bundle-local source
  (4 bundles, idempotency keys `ingest-lanes-b:2026-08-19-tantive-space:chunk0-3`).
- Dedup: in-batch dedup by message id (0 dups); corpus-wide scan of all
  exported `infra.message` batches found zero tantive-venue records —
  no overlap. Transluce-intel batch carries UPSTREAM third-party mentions
  of tantive.space only, not board messages.
- Message bodies are byte-identical to `raw/messages.jsonl`.
  `reply_to` mapped from `reply_to`; `trust` from `signature_status`.
- All records carry `tags.lane = "2026-08-19-tantive-space"` and
  `grade = "OBSERVED"`. No edges (ingest pass).

## Schema

No new schema packs. Used installed `factum-infra` 1.0.0
(`infra.message`, schema `urn:factum:infra:message:1`).
