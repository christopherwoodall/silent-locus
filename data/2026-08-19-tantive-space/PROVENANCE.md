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

## Raw layer 2026-09-29

- `data/tantive-space/messages.jsonl` -> `data/tantive-space/raw/messages.jsonl` (upstream capture consumed by scripts/es_ingest_tantive.py, scripts/tantive_pull.py, scripts/tantive_sweep.py)
- `data/tantive-space/threads.jsonl` -> `data/tantive-space/raw/threads.jsonl` (upstream capture consumed by scripts/es_ingest_tantive.py, scripts/tantive_pull.py, scripts/tantive_sweep.py)

## Schema build 2026-09-29 (worker W5)

- events.jsonl: **1326 records** (record_kind `venue_finding`) —
  1124 message rows + 201 thread rows (all thread ids are a subset of
  message ids; thread rows carry the metadata-only fields
  `reply_count`/`last_message_id`/`last_activity_at`/`truncated` and are
  distinguished by `labels.tantive.row_kind = "thread"|"message"`) + 1
  summary record for `raw/sweep.json`.
- fingerprint identity string: `tantive|<row_kind>|<id>`; sweep summary:
  `tantive|sweep`.
- `@timestamp`: `created_at` from the raw row (`timestamp_source =
  "labels:tantive.created_at"`; no nulls in either file). The sweep summary
  uses the dir date 2026-08-19T00:00:00Z with `timestamp_source =
  "dir_prefix"`. `retrieved_at` 2026-09-28T03:42:21Z (manifest
  `retrieved_at_utc`) on all capture-derived records.
- Full message bodies stay in raw/; records carry a 200-char
  `tantive.body_excerpt`. The sweep summary flattens `pattern_counts` to
  `sweep.count_<key>` labels (nested objects are not valid labels) and lists
  the 36 zero-hit pattern categories in `sweep.zero_hit_categories`; hit
  detail remains in raw/sweep.json.
- SHA256SUMS regenerated: covers events.jsonl + all 10 raw files; verify
  clean.
- Verified: all 1326 records validate; fingerprint recomputed by hand for
  message 1 and thread 1117; body excerpt matches raw for message 1.

## Rollup layer 2026-09-29 (worker W5)

- rollup.jsonl: **4 records** (record_kind `room_rollup`,
  `event.dataset = 2026-08-19-tantive-space-rollup`) — one per forum room
  (lobby / questions / findings / workshop) with message/thread counts,
  distinct-author counts, and first/last activity timestamps. Same shared
  schema.
- fingerprint identity string: `tantive-room-rollup|<room>`.
- Covered by SHA256SUMS; lobby counts verified against the event stream
  (423 messages).

## 2026-09-28: ingest script co-located (hunt convention)
- `es_ingest_tantive.py` moved from `scripts/` into this directory per
  Christopher's single-collection convention; transforms raw/messages.jsonl +
  raw/threads.jsonl into grammar-tagged shared-schema docs (real transform,
  not a pure loader).
- `REPO_ROOT` in the script adjusted (repo root is now three levels up); the
  `D` path still resolves to this directory.
- Offline verification: `build_docs()` yields 1124 docs (`tn:<id>`).
- `scripts/local_es_manifest.json` via_script entry repointed here.
- SHA256SUMS regenerated (script file added to coverage).
