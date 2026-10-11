# Provenance — 2026-06-17 reverse tunnels

Lane: `2026-06-17-reverse-tunnels`.
Legacy dir: `evidence/remove-2026-06-17-reverse-tunnels/` (moved to
`data/lanes/2026-06-17-reverse-tunnels/raw/` on ingest, 2026-10-11).

## What this dataset is

Reverse-tunnel hostname census tied to the 2026-06-17 collusion-wiki incident.

- `tunnel_hostnames.json`: 12 agent-tunnel candidate hostnames
  (6 pinggy `*.run.pinggy-free.link`, 6 serveo `*.serveousercontent.com`),
  each with classification (6 corpus-verified, 5 candidate-same-format,
  1 urlquery-scanned), embedded IP, first-seen UTC, label, wiki pages, and
  evidence note. Explicitly excluded: myxworm, petisse, inohm-sh,
  serviceupdatevalidator, webmailadminhelpdesk serveo subdomains
  (urlquery scans, no IP embedding, no incident link).
- `corpus_tunnel_records.json`: 29 timestamped sightings
  (time, label, page_id, tunnels) from collusion-wiki revisions.
- `uq_*.json`: urlquery report data for the tunnel IPs/hostnames
  (2026-09-24/28).
- `dns_check_20260928T032744Z.txt`, `dns_auth_20260928T032749Z.txt`:
  liveness probes — all tunnels dead (no A records); control hostnames also NXDOMAIN.
- `htmx_summary.json` + `htmx_*.html`: urlquery htmx search probes (HTTP 204,
  zero UUID hits — pre-fix endpoint, see 2026-10-06 tooling note).
- `manifest.sha256`, `run-logs/`.

## Factum ingest (2026-10-11)

- 12 `infra.tunnel` observations (service pinggy/serveo, public_host),
  sightings folded into tags.
- Dedup: one existing `infra.proxy_chain` (lane `2026-10-01-intermediary-relays`)
  cites bnuxw-16-146-184-55.run.pinggy-free.link as a jina proxy target —
  different observation kind, no conflict.
- No schema changes needed. Bundle: `ingest-2026-06-17-reverse-tunnels-20261011`.
