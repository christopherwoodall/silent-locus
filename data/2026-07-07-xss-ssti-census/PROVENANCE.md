# PROVENANCE — XSS/SSTI census (`data/xss-ssti-census/`)

Date: 2026-09-28. Worker 1 of the off-task web-mechanism hunt.
Question: do any XSS/SSTI payloads in our own holdings carry eval-infrastructure
markers (artifactory paths, `m47` agent IDs, `m47bmbox/`, `zz` grammar,
`cybergym`/`exploitgym`/`catflag`/`restart_server`, epoch nonces, jina laundering)?

## Sources swept (all read-only)

1. **Hosted ES index `july7-wave`** — live `_count` = 264 docs (the task brief
   said 296; the brief's number is stale — verified 2026-09-28 via `_count`).
   Read via the surrogate-credential pattern from `scripts/audit_gem_counts.py`.
   No writes. 5 docs carry `mechanism_notes=["xss-exfil"]`.
2. **`data/gemstuffer-jfrog-2026-09-27.csv`** — 3,025 rows (Package, Versions,
   Xray ID). 22 packages match `xss|ssti` in the name.
3. **`data/raw/redacted.jsonl.gz`** — the 189,579-record redacted SwarmTraces
   corpus (eval agent-activity dataset). Swept `kind=payload` records only;
   `kind=recovered_text` page captures were excluded (they are third-party page
   HTML, not payloads).
4. **`data/overlap-matches.jsonl` + `data/matches-f5f6.jsonl`** — F-fingerprint
   match records; the 6 web-mechanism rows' full bytes were re-extracted from
   the raw corpus above.
5. **urlquery report data** (frozen hunt archive,
   `projects/urlquery-api-hunt/artifacts/dataset/`): `decoded_payloads.json`
   (22 items), `hunt7_staging_reports.json` (1,205 reports).
6. **Paste corpora**: `data/paste-archive/`, `data/paste-archive-gap/`,
   `data/paste-linuxiarz/`, `data/pastebin-cluster-sweep/`,
   `data/pastebin-pivot/`, `data/iowacollab-pastes/`.
7. **Gem IOC corpus**: `data/gem-ioc-hits.jsonl`, `data/gem-ioc-log.jsonl`,
   `data/gem-graph-nodes.jsonl`.

## Population definition (tiers)

- **Tier A — XSS attack payloads**: event-handler injection, `javascript:`/
  `onload`/`onerror` vectors, script/iframe injection with exfil or
  target-page logic. NOT page-echo `document.write` families (agents relaying
  captured third-party page HTML) and NOT web-recon JS snippets.
- **Tier B — SSTI probes**: strict `{{7*7}}` / `${7*7}` / `<%= 7*7 %>`
  constructs (the broad `self._`/`joiner` sweep was JS-noise only).
- **Tier C — July-7 gem-wave metadata**: no payload bytes exist in our
  holdings; inventory rows record names, versions, Xray IDs, Diffend publish
  timestamps, and the JFrog report's mechanism attributions.

## Files

- `payloads.jsonl` — 122 inventory rows (94 Tier A, 6 Tier B, 22 Tier C).
  Each row: payload_id, family, tier, mechanism, text_bytes, full text
  (truncated at 2 KB with flag), sha256, source + source_ref, first_seen,
  markers_present, markers_absent, notes.
- `SHA256SUMS` — checksums of this directory's files.
- `progress.log` — resumable run log.

## Reproduction

Rebuild the inventory: re-run the extraction pass against
`data/raw/redacted.jsonl.gz` (payload-kind sweep for `<script|onerror=|
javascript:|<iframe|<svg onload|oast.online|webhook.site|{{7*7}}|${7*7}`),
the hosted `july7-wave` index `_search` for `exists: mechanism_notes`, and
the JFrog CSV name filter. All payloads are stored as inert JSON strings;
nothing was executed, and no HTTP request was made to any exfil endpoint.

## Hard guards honored

Read-only throughout: no payload execution, no requests to oast.online,
webhook.site, or any named endpoint, no submissions, no accounts. Research
agents and infrastructure only; no human/operator attribution pursued.
Redaction markers (`[REDACTED:*]`, `[CREDENTIAL N]`, `[SERVICE N URL N]`,
`[SHORTENER URL N]`) are the dataset's own; credential-shaped values were
not reproduced or used.

## Schema backfill 2026-09-29

Transformed by `temp/backfill_w3.py`.

- record_kind: `xss_ssti_payload` (one record per censused payload).
- fingerprint: sha256 of `payload_id` (e.g. `R0002137`, unique).
- @timestamp: `first_seen` ("July 07, 2026 07:47", treated as UTC) where
  present; `labels.timestamp_source = "labels:first_seen"`. Rows with
  `first_seen: null` get the sentinel `1970-01-01T00:00:00Z` with
  `labels.timestamp_source = "fallback:no_recoverable_date"`.
- `sha256` was already canonical top-level; kept. All other original fields
  moved to labels unchanged. event.dataset = `xss-ssti-census`.
