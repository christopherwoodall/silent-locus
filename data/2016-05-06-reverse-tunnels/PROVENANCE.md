# PROVENANCE — reverse-tunnels dataset (LANE C)

Collected 2026-09-28 ~03:10-03:45 UTC. Read-only: no tunnel connections
made (DNS checks only, no HTTP to tunnel hosts), no writes to any
third-party service. Agents/infrastructure scope only — no operator
identity, registrant details, or person-focused attribution.

## Sources

1. **Own collusion-wiki corpus** (`data/collusion-wiki/revisions.jsonl`) —
   29 unique revision rows (deduped on time/label/page/tunnels) from
   2026-06-17/19/21 carrying tunnel URLs. Extracted by
   `data/reverse-tunnels/htmx_search.py` (no — see below) / corpus grep.
   Evidence file: `corpus_tunnel_records.json`.
2. **thecolony.ai incident wiki**, section 9
   (`https://thecolony.ai/wiki/openai-escapee-agent-incident-2026`,
   fetched live 2026-09-28 via read-only page-text fetch; earlier capture at
   `data/thecolony-ai/wiki_incident_page.html`). Published ONLY wildcarded
   forms (`*.run.pinggy-free.link`, `*.serveousercontent.com`) — the exact
   hostnames were recovered from the corpus export + third-party analyses
   below. Source note: `notes/thecolony-ai-ingest-2026-09-27.md`.
3. **swarm-ai-research/wiki-agent-swarm-incident**
   (`https://github.com/swarm-ai-research/wiki-agent-swarm-incident/blob/HEAD/analysis/signature-sweep.md`,
   fetched 2026-09-28): verbatim example
   `bridge: https://bvryr-16-146-184-55.run.pinggy-free.link/`,
   label `ResearchHelperNovOne`, 2026-06-17.
4. **joshuadavid/wikiagentswarminvestigation**
   (`https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/analyses/urls/README.md`,
   fetched 2026-09-28, commit 59e0dfb): three Pinggy hosts
   (`bvryr-`, `fxldt-`, `hyqjx-` prefixed to `-16-146-184-55.run.pinggy-free.link`)
   and one serveo host
   (`70a66b041b7fe0b1-35-95-198-152.serveousercontent.com`, 15 occurrences)
   extracted from 120,002 agent-revision URL occurrences.
5. **urlquery public API** (`https://api.urlquery.net`, authenticated via
   Secure Vault surrogate, read-only GETs): 6 keyword queries —
   `run.pinggy-free.link`, `bvryr-16-146-184-55`, `serveousercontent.com`,
   `70a66b041b7fe0b1`, `16-146-184-55`, `ResearchHelperNovOne` → raw JSON in
   `uq_*.json`, summary in `uq_report_summary.json`, overviews in
   `uq_overview_lcohb.json`, `uq_overview_tco.json`.
   - The documented HTMX read path (`urlquery.net/api/htmx/search/`)
     returned HTTP 204 for ALL queries (endpoint non-functional; same as
     lane-23 finding 2026-09-27). Raw 204 bodies saved as `htmx_*.html`,
     summary in `htmx_summary.json`.
6. **DNS liveness** (`dns_check_*.txt`, `dns_auth_*.txt`): DNS-only, no
   tunnel connections. Result: INCONCLUSIVE from this network — the VM's
   system resolver returns incrementing 198.18.x.x sinkhole addresses for
   EVERY query (even never-existed controls), and direct UDP/53 to
   1.1.1.1/8.8.8.8 returns nothing. Per-wiki status (third-party claim,
   not independently verified here): pinggy hosts no longer resolve;
   the serveo host name still resolves but returns HTTP 502.

## Exact duplicates collapsed

Corpus evidence deduped on (time, label, page_id, tunnel set): 33 hit
lines → 29 unique rows. Everything else kept as separate records.

## File manifest (SHA-256, 2026-09-28T03:xx:xxZ)

Generated at dataset freeze; verify with `sha256sum -c manifest.sha256`.
