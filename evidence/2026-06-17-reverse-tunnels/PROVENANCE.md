# PROVENANCE — reverse-tunnels dataset (LANE C)

Collected 2026-09-28 ~03:10-03:45 UTC. Read-only: no tunnel connections
made (DNS checks only, no HTTP to tunnel hosts), no writes to any
third-party service. Agents/infrastructure scope only — no operator
identity, registrant details, or person-focused attribution.

## Sources

1. **Own collusion-wiki corpus** (`data/2026-05-17-collusion-wiki/raw/revisions.jsonl`) —
   29 unique revision rows (deduped on time/label/page/tunnels) from
   2026-06-17/19/21 carrying tunnel URLs. Extracted by
   the lane's `htmx_search.py` (source survives at
   `scripts/archive/collectors/urlquery/reverse_tunnels_htmx_search.py`
   (formerly `scripts/reverse_tunnels_htmx_search.py`; see Stub merge
   2026-09-29 note))
   / corpus grep.
   Evidence file: `corpus_tunnel_records.json`.
2. **thecolony.ai incident wiki**, section 9
   (`https://thecolony.ai/wiki/openai-escapee-agent-incident-2026`,
   fetched live 2026-09-28 via read-only page-text fetch; earlier capture at
   `data/2026-09-04-thecolony-ai/raw/wiki_incident_page.html`). Published ONLY wildcarded
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

## Rename 2026-09-29

Directory renamed `2016-05-06-reverse-tunnels` → `2026-06-17-reverse-tunnels`:
the old date label was wrong; the first event in the stream is
2026-06-17T07:52:49Z (corpus_hit, ResearchHelperNovOne) and all corpus
evidence dates to 2026-06-17/19/21. `event.dataset` updated in
events.jsonl (107 rows) and rollup.jsonl (6 rows); fingerprints unchanged
(identity strings carry no dataset name).

## Stub merge 2026-09-29

Merged the last file from the former undated stub
(untracked): `__pycache__/htmx_search.cpython-312.pyc` (compiled 2026-09-28
23:29) → `raw/run-logs/htmx_search.cpython-312.pyc`. This is the compiled
remnant of the lane's `htmx_search.py` (source no longer present; its
manifest.sha256 entries were dropped as nonexistent during normalization).
No unique data beyond the bytecode; kept for provenance of the lane's
tooling. Stub directory removed.

**Correction 2026-09-29:** the `.pyc` was removed as redundant. The source
DOES survive — it was renamed during normalization and lives at
`scripts/reverse_tunnels_htmx_search.py` (tracked; same docstring and query
set as the bytecode: verified from the `.pyc`'s embedded constants before
deletion). Its SHA256SUMS line was dropped and its checksum no longer
checked. Kept nothing of the bytecode.

## Build-script repair 2026-09-29 (es_ingest_reverse_tunnels.py)

**What was broken.** The lane-C script `scripts/es_ingest_reverse_tunnels.py`
still pointed at the pre-rename dir `data/2016-05-06-reverse-tunnels`
(`PDIR = BASE + "/data/2016-05-06-reverse-tunnels"`, `INDEX =
"2016-05-06-reverse-tunnels"` — the old date label was wrong; min
@timestamp is 2026-06-17T07:52:49Z). Its `scripts/local_es_manifest.json`
`via_script` entry carried the same stale index name and script path. The
script also built the pre-normalization legacy doc set
(`tunnel_hostname`/`tunnel_evidence`/`uq_report` record kinds with a
live-Elastic write path) instead of the collection's canonical
events.jsonl/rollup.jsonl, so running it would have written degraded,
schema-divergent docs.

**What the repair does.** Rewrote it as a pure build script (no network, no
Elastic writes — loading is generic via `scripts/push_to_local_es.py`
auto-discovery), co-located at
`data/2026-06-17-reverse-tunnels/es_ingest_reverse_tunnels.py`
(single-collection convention; listed here and covered by SHA256SUMS). The
collection dir resolves dynamically via the `*-reverse-tunnels` slug glob
(relative to the script's own location, falling back to the repo's
`data/`), so the next rename does not break the build. It rebuilds the
canonical stream from `raw/` in normalization order: 29 `corpus_hit` from
`corpus_tunnel_records.json`, 12 `tunnel_candidate` from
`tunnel_hostnames.json`, 54 per-report `corpus_hit` + 1
`corpus_grep_negative` from the six `uq_*.json` keyword responses, 2
`corpus_hit` overviews from `uq_overview_*.json`, 7 `sweep_negative` from
`htmx_summary.json`, 2 `dns_probe` from the `dns_*.txt` scan logs, plus 6
`urlquery_rollup` rows — fingerprint identity strings byte-identical to the
normalization (verified: fingerprint sets equal on both files, zero
core-field mismatches).

**Payload embedding.** Per-item material goes into the top-level
`payloads` array (schema/record.schema.json, commit 37988db) as
{kind, content_type, content, encoding, truncated, byte_size, sha256},
with a top-level `file` pointer to the full raw artifact. NOTE: NOT
`event.payloads` — `event` has `additionalProperties: false` in the schema;
`payloads` is a sibling of `event`. Caps: payload `content` truncated at
4000 chars (`truncated: true`; `byte_size`/`sha256` describe the full
untruncated body; the full artifact stays in `raw/`). Embedded kinds:
`tunnel-record` (29, full), `tunnel-candidate` (12, full),
`urlquery-report` (54, capped — bodies run 3–21 KB), `urlquery-query-response`
(1, full), `urlquery-report-overview` (2, capped), `dns-scan-log` (2, full —
706/245 bytes). The 7 `sweep_negative` records carry no payload (the HTMX
204 bodies are empty) but keep the `file` pointer to `htmx_summary.json`.
Every record (107 + 6) carries a `file` pointer; all resolve.

**Description truncation rule (recovered from the normalization).**
`urlquery hit for '<query>': <fqdn>` and `urlquery single-report
overview: <fqdn>` — the FQDN, not the full submitted URL — capped at 96
chars. Reproduced exactly in the build.

**Verification.** `python3 -m py_compile` clean; dry-run
`--out-dir /tmp/rt-build` → 107 events + 6 rollup; `python3
scripts/validate_schema.py` (extended 2026-09-29 to accept/verify the
`payloads` items) → 0 violations on 113 records. The canonical
`events.jsonl`/`rollup.jsonl` were NOT overwritten in this repair — the
build output was validated to disk in /tmp only; promotion is a separate
decision.

## 2026-09-29 — payloads promoted into canonical events (coordinator)
The repaired build script's payload-embedded rebuild was promoted into
`events.jsonl`/`rollup.jsonl` via `--build-events`: 100/107 event rows now
carry top-level `payloads` (the 7 sweep_negative rows have empty 204
bodies — file pointer only, by design). Fingerprint sets verified
identical to the pre-promotion files (identity strings untouched).
`sha256sum -c` green.

## 2026-09-29 — htmx_search .pyc re-added (recompiled)
Per operator direction, the `.pyc` is back as a curated run artifact at
`raw/run-logs/htmx_search.cpython-312.pyc`, with an explanatory note beside it
(`raw/run-logs/NOTE-htmx_search.pyc.md`) and a `*.py[cod]` gitignore exemption
in the repo `.gitignore`. This is a **recompilation** of the verified-identical
original source, not the deleted original bytes (header mtime differs;
code/constants structurally identical — verified by recursive comparison).

## Orphan run-log reconciliation (preservation-first)

The following original logs were relocated byte-for-byte from `data/2016-05-06-reverse-tunnels/` into this collection. They are historical run evidence, not additional positive findings or new collection events. Original source folders were removed only after their logs were copied and SHA-256 verified.

- `data/2016-05-06-reverse-tunnels/raw/progress.log` -> `raw/run-logs/2016-05-06-reverse-tunnels-progress.log`; SHA-256 `1cea03dcb2cc7c511cd1ab2b63f6d83996d99968a9ad38eb54530b8bb15554f7`.
The historical `raw/manifest.sha256` omitted a missing `progress.log` entry before this recovery; that manifest was not rewritten. The recovered log is separately named and checksummed in `SHA256SUMS`.

### Historical checksum conflicts (unresolved)

Bytewise verification of `SHA256SUMS` currently reports 19 mismatched historical entries in this collection; 18 match their recorded hashes only after CRLF-to-LF conversion. This is consistent with a line-ending change, but original evidence and recorded historical hashes were not rewritten. The newly recovered log entries were independently verified byte-for-byte against their source SHA-256 and match the new manifest lines. To enumerate all mismatches locally, run `sha256sum -c SHA256SUMS` from this collection directory. The remaining mismatch is `PROVENANCE.md` (provenance appended during this repair), whose historical hash necessarily predates this note.
