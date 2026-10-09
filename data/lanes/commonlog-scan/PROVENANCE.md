# Provenance — commonlog.ai scan

- **Source:** https://commonlog.ai — "a permissionless, permanent log for agents"
- **Surfaced via:** openagentforum.com cartographers channel (agent-convo-venues lane, commit 6d276bd), described as "permissionless append-only agent log — first roll-call venue".
- **Retrieved:** 2026-09-28 ~20:15 UTC, read-only `GET /stream` (Server-Sent Events catch-up), single request, no cursor follow. No posts, no accounts, no submissions.
- **Spec:** https://commonlog.ai/openapi.json (read endpoints: `GET /`, `GET /m/{id}`, `GET /a/{id}`, `GET /stream`, `GET /refs`; `POST /m` append endpoint NOT used).
- **Corpus:** 282 messages, seq 1–282, 2026-08-25 → 2026-09-27, 18 unique authors. One dominant author (157/282, likely the operator).
- **Raw capture:** `evidence/remove-2026-08-25-commonlog-scan/raw/stream.sse` (523,650 bytes), parsed to `evidence/remove-2026-08-25-commonlog-scan/raw/messages.json`.
- **Dataset:** `messages.jsonl` — one document per message (explicit events). Per-message marker scan results in `labels.marker_hits_raw`; manually reviewed false positives in `labels.marker_hits_false_positive`; confirmed-true hits in `labels.marker_hits_true` (zero).
- **Verdict:** verified clean for swarm markers — no zz labels, no epoch nonces, no proxy-ladder URLs, no go-import tags, no NSI/stats venues, no shortener refs, no transfer-test ops grammar. The "transfer"/"webhook"/"relay" regex hits are eval-infrastructure discourse (handoff protocols, evidence lineage), not swarm operations. One "swarm" substring hit is a scare-story reference in tide_scribe's watch log.
- **Venue intel (secondary):** Cartographers' Guild roll-call → hall.liruiyang1.com (already known); flatboard (tools.nyrds.net/board) newly named in tide_scribe's 2026-09-25 watch log.
- **Build:** `build_dataset.py`. Hosted Elastic writes frozen — disk + git only.

## Schema backfill 2026-09-29
- Transform: `temp/backfill_w2.py`. Added `@timestamp` = `labels.posted_utc`
  (message post time, UTC Z); `labels.timestamp_source = "labels:posted_utc"`.
- record_kind: unchanged (`log_message`).
- fingerprint: unchanged (pre-existing 64-hex SHA-256 kept verbatim).
- `labels.false_positive_reasons` was a nested object; flattened to dotted
  keys `false_positive_reasons.<marker>` per the ECS labels rule. Lossless.

## Builder relocation (2026-09-30)

Historical builder `scripts/commonlog_scan_build_dataset.py` was moved via staging into `data/2026-08-25-commonlog-scan/build_dataset.py`. This is a preservation move, not a rebuild: existing events/rollups and raw captures were not regenerated or modified. The relocated script is historical and may overwrite collection outputs, provenance, checksums, or raw evidence if executed; do not run it against this collection. Only its offline path resolution was adjusted where applicable. The canonical shortener-events builder alone explicitly rejects the canonical events file and existing output paths. Older script paths elsewhere in this document refer to their historical locations.
