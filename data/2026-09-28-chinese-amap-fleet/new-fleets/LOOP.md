## Retry loop started 2026-10-05T05:17:18Z
- 2026-10-05T05:17:18Z: egress still down (uq_htmx.py failed)
- 2026-10-05T05:37:35Z: egress still down (uq_htmx.py failed)
- 2026-10-05T05:52Z: egress RECOVERED (curl to urlquery.net verified by parent; uq_htmx.py search returns live reports).
  Gap-fill collection launched: collect_gapfill.py — `http` @ offsets 0/50/100/150 + 15 targeted queries
  (webhook.site, ngrok, eval, harness, appwrite.network, jmail.world, nonce=, task=, batch=, museum,
  cachedview.nl, wasmer.app, replit.app, ovou.com, .shop), 6s sleeps, → raw/window_gapfill.json.
  Coverage gap being backfilled: submissions from ~04:00 UTC onward (window1.json covered ~03:00–03:58 UTC).
- 2026-10-05T05:56:26Z: respawned agent manual probes (limit 96, limit 24) BOTH got partial data then IncompleteRead (36KB/45KB) — proxy truncates mid-response; egress NOT cleanly recovered. retry_loop.sh relaunching.
## Retry loop started 2026-10-05T05:56:26Z
- 2026-10-05T05:56:26Z: egress still down (uq_htmx.py failed)
- 2026-10-05T06:37:07Z: egress still down (uq_htmx.py failed)
