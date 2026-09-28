# Local ELK runtime state (git-ignored).

`elk/data/` is the Elasticsearch data directory, bind-mounted by
`docker-compose.yml` (`./elk/data:/usr/share/elasticsearch/data`).

- Created automatically by `make up`.
- Survives `make down` and `make restart`.
- Wiped only by `make reset` (asks for confirmation).
- Never committed: cluster data stays on your machine.
