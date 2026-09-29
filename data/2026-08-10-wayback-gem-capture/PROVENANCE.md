# PROVENANCE — data/2026-08-10-wayback-gem-capture/

Follow-up lane on the lane12 Wayback sweep's single HIT (agent-hunt-durable-watch, 2026-09-28).

## Source chain
1. Lane12 sweep (`hidden_files/lane12/wb_sweep.py`, DONE 2026-09-28) hit on
   CDX for `rubygems.org/gems/zztargettest18587`: capture `20260810004952`,
   original status 200, `text/html`.
2. This lane fetched the replay **read-only** via
   `https://web.archive.org/web/20260810004952id_/https://rubygems.org/gems/zztargettest18587`
   (`id_` = original response bytes, no Wayback rewriting).
   Script: `hidden_files/lane12/fetch_wb_gem_capture.py` (fetched 2026-09-28T23:54:15Z,
   single attempt, HTTP 200, 37,279 bytes). Fallback plain replay was not needed.
3. Comparison baseline: our own Diffend publish-time snapshot,
   `data/raw/gems/zztargettest18587-0.0.1.gem`
   (sha256 `82a391cc5afcc59f2998cfbff76b6c760226df7d82024af1b2768ba3adfb967b`),
   harvested during the 2026-09-27 Diffend bulk run. The go-import payload was
   extracted from `metadata.gz` (gem description field) by parsing only — nothing executed.

## Files
- `wb_rubygems-org_gems_zztargettest18587_20260810004952.id.html` — raw capture bytes
  (sha256 `c3d654b76bd20637ac3f475310b13ed4f23abd4fe5ae2b021fa6dbc7fd30d98a`)
- `SHA256SUMS` — manifest
- `fetch_meta.json` — fetch attempt log (statuses, headers, timestamps)
- `hits.jsonl` — archived-vs-Diffend payload comparison row
- `progress.log` — lane timeline with DONE marker

## Finding
The Aug-10 capture shows the **yanked state**: h1 is bare `zztargettest18587`
(no version), no Versions tab, no Description block, no go-import meta tag,
"Yanked by: rubygems-security-team", owner `southnews5j23447n`.
The campaign payload is NOT in the archive; it survives only in our
Diffend publish-time snapshot. Replay served HTTP 200 (yanked gem pages are
200s on rubygems.org, not 404s).

## Elastic
Hosted Elastic write freeze in effect — no ingest performed.
Queued for the `rubygems-goimport-campaign` index on resume: 1 doc from
`hits.jsonl` (event.dataset `wayback.gem.capture`).

## Licensing / scope
Read-only research; no submissions, logins, or payload execution.
Agents/infrastructure scope only. No credentials handled.

## Schema backfill 2026-09-29

Transformed by `temp/backfill_w3.py`.

- record_kind: `wayback_capture` (one record per wayback capture
  assessment).
- fingerprint: sha256 of `target + "|" + wayback_capture_ts`.
- @timestamp: `wayback_capture_ts` (14-digit wayback stamp
  20260810004952) parsed to `2026-08-10T00:49:52Z`;
  `labels.timestamp_source = "labels:wayback.capture_ts_raw"` (raw value
  preserved in labels).
- `replay_url` promoted to canonical top-level `source_url` (same value;
  raw copy also in labels as `wayback.replay_url`). `sha256` was already
  canonical top-level; kept. `bytes` kept in labels (capture byte count).
- event.dataset = `wayback-gem-capture`.
