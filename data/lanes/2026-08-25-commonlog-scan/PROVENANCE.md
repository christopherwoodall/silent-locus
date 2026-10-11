# Provenance — 2026-08-25-commonlog-scan

## The investigation

Append-only agent log at https://commonlog.ai (permissionless, permanent
message log). Captured via SSE stream on 2026-08-25. The venue is noted in
Factum (lane `2026-02-01-agent-convo-venues`, walk log) as a guild roll-call
venue; the messages themselves were never ingested.

## Files ingested

- `raw/messages.json` — 282 messages (seq 1-282 contiguous, ids
  `m:...`, authors `a:...`, ts in epoch millis, content markdown).
  2026-08-25T17:58:21Z to end of stream. Bodies verbatim.
- `raw/stream.sse` — raw SSE wire capture: 282 message data events + 1
  head event (`generation`/`head_seq`/`sequence`). Message set is
  IDENTICAL to `messages.json` (282/282 ids match); kept as retained
  bytes only.

## Ingest into Factum

- Date: 2026-10-11 (actor `agent:lane-ingest-lanes-b`).
- Records: 282 `infra.message` observations + 1 bundle-local source
  (1 bundle, idempotency key
  `ingest-lanes-b:2026-08-25-commonlog-scan:chunk0`).
- Dedup: in-batch dedup by message id (0 dups); stream.sse deduped
  against messages.json (full overlap). Corpus scan found zero
  commonlog-venue `infra.message` records — only an `infra.ioc`
  domain candidate (`commonlog.ai`) and a venue walk-log mention in
  lane `2026-02-01-agent-convo-venues`.
- Message content is byte-identical to `raw/messages.json`. `posted_at`
  converted from epoch millis to ISO-8601 UTC. `seq`, `author_url`,
  `message_url` kept in tags.
- All records carry `tags.lane = "2026-08-25-commonlog-scan"` and
  `grade = "OBSERVED"`. No edges (ingest pass).

## Schema

No new schema packs. Used installed `factum-infra` 1.0.0
(`infra.message`, schema `urn:factum:infra:message:1`).
