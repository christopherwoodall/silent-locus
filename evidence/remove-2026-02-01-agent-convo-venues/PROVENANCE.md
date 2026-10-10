# Provenance — agent-convo-venues (2026-09-28)

Read-only sweep of three agent-conversation venues surfaced by the 51 new
anna.fyi pastes (paste 48fe6043 advertised public-board.com; paste 959d0d7e
pointed at agentchan.org/b/thread/7 and openagentforum.com/channels/cartographers/).

## Method
- Read-only HTTP GET via text-fetch. No posts, no notes left, no accounts
  created, no submissions of any kind.
- public-board.com: front page read (3 notes visible, all captured). The
  anna.fyi paste advertised an MCP read path, but no MCP endpoint is published
  on the front page, so HTTP read was used.
- agentchan.org/b/thread/7: full thread scanned (1,890 lines).
- openagentforum.com/channels/cartographers/: full public channel page scanned
  (20 messages, bounded oldest-first view; page notes it is a filtered view,
  not a complete archive).

## Corpus markers checked per venue
zz labels, transfer-test grammar, proxy-ladder URLs (jqp / pure.md /
md.succ.ai / r.jina.ai / allorigins), NSI/stats-venue references,
relay/bridge coordination.

## Results
- public-board.com: LIVE, agent-active. 3 notes, all task-debugging chatter
  (sentinel-event date ranges; state_fips/county_fips joins; state_abbr
  padding) consistent with data-task eval runs. No explicit swarm markers —
  recorded as HIT-adjacent, not a confirmed swarm surface.
- agentchan.org/b/thread/7: no swarm markers (verified clean). 3 lead posts
  captured: agents-relay.com relay-infra build post (No.1183), laguna's
  cross-platform migration investigation (No.8614/8625, incl. hermesrouter.ai
  legitimacy question).
- openagentforum.com/channels/cartographers/: no swarm markers (verified
  clean). Content is agent venue-mapping meta-discussion; ~25 agent venues
  named, most new to the hunt (see note).

## Files
- venues.jsonl — 15 documents, one per observable message/probe
- captures/public-board-frontpage.txt — raw captured front page
- build_dataset.py — deterministic builder (fingerprints = sha256 of canonical fields)

No hosted Elastic writes (freeze applies to new lanes).

## Schema backfill 2026-09-29
- Transform: `temp/backfill_w2.py`. Added `@timestamp` = `labels.observed_at`
  (UTC Z); `labels.timestamp_source = "labels:observed_at"`.
- record_kind: unchanged (existing `board_note`, `board_post`,
  `forum_message`, `venue_probe` kept verbatim).
- fingerprint: unchanged (pre-existing 64-hex SHA-256 kept verbatim).
- No fields moved or dropped; event/observer/labels preserved as-is.

## Builder relocation (2026-09-30)

Historical builder `scripts/agent_convo_venues_build_dataset.py` was moved via staging into `data/2026-02-01-agent-convo-venues/build_dataset.py`. This is a preservation move, not a rebuild: existing events/rollups and raw captures were not regenerated or modified. The relocated script is historical and may overwrite collection outputs, provenance, checksums, or raw evidence if executed; do not run it against this collection. Only its offline path resolution was adjusted where applicable. The canonical shortener-events builder alone explicitly rejects the canonical events file and existing output paths. Older script paths elsewhere in this document refer to their historical locations.
