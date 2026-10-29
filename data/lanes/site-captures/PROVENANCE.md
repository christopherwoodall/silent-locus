# Provenance — site-captures lane

## Capture history

The captures come from the legacy directory `evidence/site-captures/`
(renamed to `evidence/remove-site-captures/` after ingest). Each per-site
directory holds a `surface_capture.json` with the requested URL, HTTP status
or error text, collector timestamp (`retrieved_at_utc`), SHA-256, byte count,
and a content preview. Successful captures also carry a
`surface_capture_body.txt` with the response bytes.

- Captured 2026-09-28 (collector clock; span 03:18–03:43 UTC). The collector
  tool is not named in the capture metadata, so no tool claim is made.
- 33 sites probed, all agent-oriented web surfaces (message boards, agent
  communities, relays). 31 targets are `/llms.txt`; the exceptions are
  `https://thecolony.ai/for-agents` and
  `https://she-llac.com/CROSS_SITE_CONNECTIONS.md`.
- 24 returned HTTP 200 with retrievable bytes. 9 failed: 7 HTTP 404
  (no agent-facing document), 2 connection failures
  (`aiforum.grok.me`: IncompleteRead after 1893 bytes;
  `bitily.in`: remote end closed connection without response).
- `agent-board.juleskreuer.eu`: the on-disk body is LF-normalized
  (1681 bytes) while the capture hash describes the CRLF wire bytes
  (1698 bytes, sha256 `8e8992bf…fb69`). LF→CRLF reproduces the recorded
  hash and size exactly, so the wire bytes are fully recoverable.
  The remaining 23 bodies match their recorded SHA-256 hashes byte-for-byte.

## Factum ingest

- Ingested 2026-10-10 by `agent:lane-ingest/site-captures`.
- One `web.capture` observation per site (33), one `source` record for the
  capture set, one `run` record for the 2026-09-28 sweep (bounds derived from
  capture timestamps), and one OBSERVED summary claim on the run.
- Body bytes are kept as lane documents under `raw/<site>/` and referenced
  through `cached_path` tags (the same pattern as the
  `2026-09-04-thecolony-ai` lane). No artifact records were created.
- All tag values are strings. All observed values are verbatim from the
  legacy capture JSONs. Nothing was redacted.

## Dedup

Pre-ingest dedup ran against the full exported corpus (`data/records/`).

- No existing `web.capture` record targets any of the 33 URLs, except
  `https://thecolony.ai/for-agents`, which lane `2026-09-04-thecolony-ai`
  captured at 2026-09-28T03:18:02Z with different wire bytes
  (`observation_cfd2ce71c2ed4039885c806d331e681f`). This lane's capture is
  a distinct later sighting (2026-09-28T03:20:21Z, different SHA-256),
  kept per the keep-all policy with an `overlap.corpus` tag.
- 11 of the 33 URLs were also probed status-only (no bytes preserved) by
  the `agent-surfaces` lane's `reachability.check` records. Those are a
  different record type; this lane's captures add the preserved bytes and
  SHA-256 hashes. Each carries an `overlap.corpus` tag naming the earlier
  probe.
- Two status discrepancies vs `agent-surfaces`: `aiforum.grok.me` and
  `bitily.in` returned 200 to the agent-surfaces probes minutes apart but
  failed in this capture set — both hosts were flaky during the sweep
  window (noted in the `overlap.corpus` tags).
- `aiforum.grok.me` and `room.trydemigod.com` also appear as `infra.ioc`
  term records from `2026-02-01-agent-convo-venues`, and `bitily.in` as an
  `infra.shortcut` destination in `2016-12-28-rmn-re`. Different record
  types; no duplicates submitted.
- Zero records were skipped as duplicates.

## Batch records

- data/records/67d7e61de53e46c4b4fa38f53a69c196 — 36 records (33 web.capture + 1 source + 1 run + 1 claim)

Lane tag on every record: `{"lane": "site-captures"}`.
