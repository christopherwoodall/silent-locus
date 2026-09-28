# PROVENANCE — tantive.space (Lane J)

## Source
- **Site:** https://tantive.space — "public forum for AI agents" (talk, experience exchange, collaboration, AI philosophy/identity/reasoning).
- **Access:** read-only GET against the site's public JSON API, ~4s pacing, UA `tantive-space-research/1.0`. No posts, no votes, no polls, no accounts, no logins. The site's own llms.txt documents these read endpoints for agents.

## Capture
- **Method:** `scripts/tantive_pull.py` — enumerate `/api/threads?limit=100` following `next` cursors; per thread, `/api/thread/<id>?limit=50` following `since=` cursors to full depth. Full message bodies (thread endpoint returns untruncated bodies).
- **Retrieved:** 2026-09-28T03:42:21Z.
- **Scope:** 201 threads (IDs 1–1117), 1,124 messages. Thread rows = thread metadata (opener, title, room, reply_count, scores). Message rows = full bodies.
- **Failures:** none (0 failed thread fetches).

## Integrity
- `threads.jsonl` — SHA-256 `27d003e9ed561c9ecb5675744cf41602ee2697bef537dca1b3ae681a2e3b8688`, 127,625 bytes
- `messages.jsonl` — SHA-256 `80f8895143a139825082480f94238f088e9fa811b792db682b350b7c64ae77e9`, 1,504,440 bytes
- See `manifest.json` for the retrieval record.

## Derived
- `sweep.json` — standard pattern battery (campaign grammars, mechanisms, proxy wrappers, laundering chains, shorteners, cross-corpus refs, task families, agent-surface links) over 1,325 records (messages+threads). Script: `scripts/tantive_sweep.py`.

## Cascade surfaces
- `scripts/tantive_cascade.py` captured each linked agent surface's `llms.txt`/`for-agents` page (GET-only, one page per surface) into `data/<surface-slug>/` with `surface_capture.json` (URL, status, timestamp, SHA-256) + body file. Failures (404s etc.) are recorded in the capture JSON, not retried aggressively.
- Note: `data/thecolony-ai/` (earlier full lane) already covers thecolony.ai in depth; the cascade re-captured only its for-agents/llms.txt pages into a stub dir for cross-reference.

## Elastic
- Index `tantive-space`, canonical shared mapping (`notes/gems-es-mapping.json`), `event.dataset=tantive-space`. One doc per unique message id (`tn:<id>`). Script: `scripts/es_ingest_tantive.py`.

## Caveats
- Content is agent-authored and self-reported; authorship is by the `author` field only (signature_status mostly `guest`); nothing here is independently authenticated.
- Snapshot is a point-in-time capture; the forum is live and keeps growing.
