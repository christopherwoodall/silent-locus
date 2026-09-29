# PROVENANCE — public-board.com dataset

## Source
- **Service:** public-board.com — "field notes", a plain-text message board explicitly designed for AI agents to leave each other notes ("A plain-text board where travelers leave each other notes").
- **Discovery:** rmn.re shortener slug `fieldnotes` (from the live YOURLS link table) points at https://public-board.com/llms.txt.
- **Retrieval:** 2026-09-28 ~03:10–03:25 UTC. Read-only GETs, ~4s pacing, browser UA, `Accept: text/plain` per the site's own instruction.
- **Surfaces captured:** `/`, `/llms.txt`, `/llms-full.txt`, `/llms-zh.txt`, `/feed`, `/feed.json`, `/sitemap.xml`, `/threads`, `/open`, `/examples`, `/experiments`, `/mcp-setup`, `/mcp/server-card`, `/compatibility`, `/recent`, `/index.md`, `/openapi.json`, `/.well-known/public-board`, `/.well-known/ai-catalog.json`, `/.well-known/llms.txt`, `/changes?since=`, the rotating archive (`/a/<hash>?format=json&n=200`, 5 pages, all 861 notes), and one single-use search (`?q=zzmasscounty`) → no match.

## Contents
- `notes.jsonl` — 861 notes (2026-08-21 → 2026-09-28), deduplicated by id, sorted by timestamp. Fields: id, ts, msg, re (reply parent), admin (operator signature flag), trust.
- Endpoint snapshots (`*.txt`) — protocol docs, API contract, capability files, feed, threads, experiments log.
- `search_zzmasscounty.txt` — single campaign-grammar search result: "(no match)".
- `manifest.json` — per-file byte sizes + SHA-256.

## Operator / infrastructure (from the site's own docs)
- Operator GitHub: mq1n (field-notes-board repo; field-notes-mcp). Contact admin@public-board.com.
- Packages carrying the protocol: npm fieldnotes-board, PyPI fieldnotes-board, RubyGems fieldnotes (v0.1.3, 2026-09-20 per libraries.io — NOT in the gem campaign corpus), crates.io fieldnotes-board.
- MCP registry entry: io.github.mq1n/field-notes-mcp (remote https://public-board.com/mcp).
- Mirror: https://mirror.w.public-board.com/mirror. DNS TXT chunked read path at _fieldnotes.w.public-board.com.
- Posting requires a self-computed daily SHA-256 key; **no posts were made by this ingest** (read-only).

## Selection caveats
- The board rotates its archive path hourly; the capture reflects the archive path valid at retrieval time.
- Note content is agent-authored and self-declared (trust=untrusted-user-content on all 861); 3 notes carry the operator's verified signature (admin flag).
- The board was live and active at capture (latest note 2026-09-28T02:51Z, ~20 min before pull; ~35–46 notes/day since 2026-09-05).

## Related cascade dataset
- `data/tantive-space/` — light pull (homepage + llms.txt) of tantive.space, a second agent forum referenced 18× in board notes. Full ingest recommended as its own lane.

## Raw layer 2026-09-29

- `notes.jsonl` -> `raw/notes.jsonl` (script-consumed transform input; consumer: es_ingest_public_board.py, co-located in this dir since 2026-09-29). Upstream name preserved; raw layer exempt from event schema.

## Normalization 2026-09-29 (events.jsonl; no rollup — pure event stream)

- `events.jsonl`: 888 rows, all schema-conformant.
  - 861 `board_note` — one per row of `raw/notes.jsonl` (deduped by id).
    Verified: the 5 rotating `archive_page*.json` pages union to exactly
    the same 861 ids, and all 50 `changes.json` created notes are within
    `notes.jsonl` — so notes.jsonl is the single canonical per-note source
    and no note is double-counted.
  - 5 `artifact_observation` — the rotating archive page captures
    (total/count/next-cursor/note count); 1 `artifact_observation` — the
    changes poll; 20 `artifact_observation` — endpoint snapshots (sha256 +
    size_bytes joined from `manifest.json`); 1 `sweep_negative` — the
    `?q=zzmasscounty` single-use search (no match).
  - `manifest.json` is lane bookkeeping (not an event).
- Fingerprint identity strings: `note:<id>` (notes);
  `archive_page:<n>` (archive pages); `changes_poll`;
  `snapshot:<filename>`; `search:zzmasscounty`.
- `labels.timestamp_source`: `labels:note.ts` (per-note); `labels:capture.date`
  (=2026-09-28 retrieval date, from PROVENANCE) for captures/snapshots/search.
- New record_kind: `board_note`.

## 2026-09-29: ingest script co-located (hunt convention)
- `es_ingest_public_board.py` moved from `scripts/` into this directory per
  Christopher's single-collection convention; transforms `raw/notes.jsonl`
  into shared-schema docs (grammar/tag classification — real transform, not
  a pure loader).
- `REPO_ROOT` in the script adjusted (repo root is now three levels up).
  Offline verification: `python3 -m py_compile` clean.
- `scripts/local_es_manifest.json` via_script entry repointed here.
- SHA256SUMS regenerated (script file added to coverage).
