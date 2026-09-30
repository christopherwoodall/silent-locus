# Local ELK runtime state (git-ignored).

`elk/data/` is the Elasticsearch data directory, bind-mounted by
`docker-compose.yml` (`./elk/data:/usr/share/elasticsearch/data`).

- Created automatically by `make up`.
- Survives `make down` and `make restart`.
- Wiped only by `make reset` (asks for confirmation).
- Never committed: cluster data stays on your machine.

Run `make ingest` from the repository root to start the stack, ingest the
registered corpus and the redacted Swarmtraces dataset, and check every
index's document count. `make verify-ingest` checks an already running
cluster without loading documents. `make ingest-dashboards` is optional:
the historical exports contain patterns for indices that are not present
in the local corpus, so imported dashboards may still show no results.
The latest export was created by a newer Kibana version than the local
8.15.3 stack and currently fails import with HTTP 422; this does not
affect ingestion or access to the indexed data in Kibana.

The corpus has 146,726 rows in 93 event/rollup files, targeting 91 indices.
Of those rows, 3,193 are identical repeated documents, so Elasticsearch
stores 143,533 distinct corpus documents. Swarmtraces adds 189,579
documents in one more index: 336,305 source rows in total, corresponding
to 333,112 indexed documents. Loading the same sources again is intended
to keep those counts unchanged. Raw captures and PDFs remain on disk.

The previous local Elasticsearch container may still use an older Docker
named volume. `make up` recreates it with the current `./elk/data` bind
mount; it does not delete the older volume. Confirm the mount with
`docker inspect silent-locus-es` before ingestion. Never use `make reset`
or `docker compose down -v` to migrate data.
