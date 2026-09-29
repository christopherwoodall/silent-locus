# silent-locus

Phase-two corpus for the agent-activity research: the public SwarmTraces
Hugging Face incident dataset (189,579 records, 91,037 payloads).

## Relationship to the wrapped hunt

`../urlquery-api-hunt/` is **wrapped and frozen** (commit 22d65bb, 2026-09-26).
This project does NOT extend it. It ingests the SwarmTraces data in its native
schema and correlates the two corpora via shared fingerprints. The hunt repo is
a read-only reference here — never write into it.

## RubyGems go-import campaign collection (SEPARATE — pending relocation)

`data/gem-*`, `data/raw/gems/`, `scripts/*gem*.py`, `notes/gem-*`,
`notes/rubygems-rescan-2026-09-27.md`, and `data/gem-pins-diffend.txt`
belong to an **independent Diffend-sourced collection** — our own pull of
the May 11–12, 2026 RubyGems go-import meta-tag injection campaign
(Christopher's screenshots, harvested from my.diffend.io). It is **NOT**
part of the SwarmTraces dataset and NOT part of this project's corpus.
It is temporarily co-located here and will move to its own project home
(`../rubygems-goimport-campaign/`) with its own provenance record; its
Elastic index is `rubygems-goimport-campaign`.

## Standing rules (inherited)

- Agents and infrastructure only — no human/operator attribution work.
- Keep-all + annotate: nothing deleted, overlap noted in metadata.
- Provenance record for every external source (source URL, retrieval date,
  SHA-256) before it enters the corpus.
- Read-only research posture: no submissions, no accounts, no logins.
- Never execute decoded payloads.
- Every finding carries direct evidence (URL or file path + offset).

## Local ELK stack

A single-node Elasticsearch + Kibana runs locally via Docker Compose
(ingestion is the python bulk-loaders in `scripts/`, so no Logstash).
The Makefile is self-documenting — `make` prints every target.

```sh
make up            # start ES (:9200) + Kibana (:5601), creds elastic/changeme
make wait          # block until cluster health is green/yellow
make dry-run       # preview ALL ingest paths; writes nothing
make ingest        # full load: corpus manifest -> swarmtraces -> dashboards
make validate      # record-schema + collection naming/registration checks
make status        # _cat/indices
make clean         # delete all data indices (containers + ./elk/data stay)
make reset         # full wipe incl. ./elk/data
```

Overrides: `STACK_VERSION`, `ELASTIC_PASSWORD`, `ES_HEAP`, `ES_PORT`
(compose env); `ES_URL` / `ES_USER` / `ES_PASS` (Makefile + scripts).

## Layout

- `docker-compose.yml`, `Makefile` — local ELK stack + self-documenting tasks.
- `schema/` — corpus rules: `record.schema.json` (record shape),
  `collections.md` + `collections.json` (collection naming taxonomy and
  registry). Validators: `scripts/validate_schema.py`,
  `scripts/validate_collections.py`.
- `data/` — one directory per collection, named per `schema/collections.md`.
  Each collection follows the canonical layout: an event layer
  (`events.jsonl`, schema-conformant, plus `rollup.jsonl` where a rollup
  layer exists) and a raw layer (`raw/`, upstream-named transform
  inputs/captures, exempt from the event schema but checksummed); the root
  holds nothing else but `PROVENANCE.md` + `SHA256SUMS`. Loading is
  generic: `push_to_local_es.py` discovers every `events.jsonl` and loads
  it into the index named by its records' `event.dataset`. Reserved: `data/raw/` (datasets
  as published, untouched; MANIFEST.json lands here), `data/processed/`
  (normalized working copies), `data/site-captures/<host>/` (read-only
  surface captures, not datasets), `data/aggregates/<name>/` (multi-source
  conglomerate collections). Every collection dir is date-prefixed
  `YYYY-MM-DD-<slug>` (first-event date, see `schema/collections.md`), and
  the prefix is part of the dataset slug / ES index name.
- `elk/` — local cluster runtime state (git-ignored).
- `kibana-exports/` — dashboard saved-object NDJSON; imported by
  `make ingest-dashboards`.
- `scripts/` — ingestion, fingerprint extraction, overlap joins.
  ES drivers: `push_to_local_es.py` (corpus manifest),
  `es_ingest_swarmtraces.py` (raw dataset).
- `notes/` — working notes, verification reports, the overlap plan.
- `archive/` — retired artifacts, kept for reference (e.g. the old
  cloud-snapshot restore script; the snapshot itself was deleted 2026-09-29,
  obsoleted by the collection rename/schema rebuild).
- `temp/` — agent scratch scripts (visible working, not pipeline code).
