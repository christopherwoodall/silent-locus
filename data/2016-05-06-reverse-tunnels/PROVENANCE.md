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

## Normalization 2026-09-29 (events.jsonl + rollup.jsonl)

- `events.jsonl`: 107 rows, all schema-conformant.
  - 29 `corpus_hit` — one per row of `corpus_tunnel_records.json`
    (deduped upstream on time/label/page/tunnels).
  - 12 `tunnel_candidate` — one per hostname in `tunnel_hostnames.json`
    (6 corpus-verified, 1 urlquery-scanned, 5 candidate-same-format). The
    `excluded` note in that file (myxworm/petisse/inohm-sh/
    serviceupdatevalidator/webmailadminhelpdesk subdomains) is preserved as
    `labels.uq.candidate_excluded=true` on the matching urlquery report
    events; it is not applied to the event stream itself.
  - 54 `corpus_hit` — one per (query, report) across the 6 `uq_*.json`
    keyword responses (6+6+6+7+29 reports); 1 `corpus_grep_negative` —
    the zero-hit `70a66b041b7fe0b1` query; 2 `corpus_hit` — the
    `uq_overview_*.json` single-report detail fetches.
  - 7 `sweep_negative` — the HTMX read-path 204s (one per query in
    `htmx_summary.json`); 2 `dns_probe` — the DNS resolution and
    authoritative checks (INCONCLUSIVE: sinkholed resolver).
  - `uq_report_summary.json` is a derived digest (covered by per-report
    events); `raw/manifest.sha256` is lane bookkeeping — corrected
    2026-09-29 to drop its three nonexistent entries (`progress.log`,
    `htmx_search.py`, bare `PROVENANCE.md`); all remaining entries verify.
- `rollup.jsonl`: 6 rows, `urlquery_rollup` — per-query `total_hits` /
  `reports_retrieved` (genuine aggregate layer of the 6 keyword queries).
- Fingerprint identity strings: `<time>|<label>|<page_id>|<tunnels>`
  (corpus rows); `<hostname>` (candidates); `urlquery:<query>:<report_id>`
  and `urlquery:overview:<report_id>` (reports); `urlquery:<query>`
  (zero-hit query); `htmx_read_path:<summary key>`; `dns:<filename>`;
  `urlquery_rollup:<query>` (rollup).
- `labels.timestamp_source`: `labels:record.time` (corpus rows);
  `labels:tunnel.first_seen` (candidates); `labels:uq.date` (reports);
  `labels:lane.date` (=2026-09-28) for query/htmx/rollup rows;
  `labels:probe.at` (dns, from filename timestamp).
- New record_kinds: `tunnel_candidate`, `dns_probe`, `urlquery_rollup`.
