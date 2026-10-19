# PostgreSQL Setup for Hunt Database

Target: Mac running Docker and Docker Compose.
Scope: PostgreSQL setup, schema, and blackboard channels only. No data ingestion.

---

## 1. Docker Compose

Create `docker-compose.yml`:

```yaml
services:
  postgres:
    image: postgres:16
    container_name: hunt-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: hunt
      POSTGRES_PASSWORD: hunt-secret-change-me
      POSTGRES_DB: hunt
    ports:
      - "5432:5432"
    volumes:
      - hunt-data:/var/lib/postgresql/data
      - ./init:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U hunt -d hunt"]
      interval: 10s
      timeout: 5s
      retries: 5

  postgrest:
    image: postgrest/postgrest:v12
    container_name: hunt-api
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      PGRST_DB_URI: postgres://hunt:hunt-secret-change-me@postgres:5432/hunt
      PGRST_DB_SCHEMAS: api
      PGRST_DB_ANON_ROLE: hunt_anon
      PGRST_SERVER_PORT: 3000
    ports:
      - "3000:3000"

volumes:
  hunt-data:
```

Create the `init/` directory. Any `.sql` file placed here runs once on first boot.

Start it:

```bash
docker compose up -d
```

Verify:

```bash
docker exec hunt-db pg_isready -U hunt -d hunt
curl http://localhost:3000/
```

---

## 2. Database Roles

PostgREST needs an anonymous role. Run once via `psql`:

```bash
docker exec -it hunt-db psql -U hunt -d hunt
```

```sql
-- Read-only role for the API
CREATE ROLE hunt_anon NOLOGIN;
GRANT USAGE ON SCHEMA api TO hunt_anon;
GRANT SELECT ON ALL TABLES IN SCHEMA api TO hunt_anon;
ALTER DEFAULT PRIVILEGES IN SCHEMA api GRANT SELECT ON TABLES TO hunt_anon;

-- Read-write role for agents that ingest
CREATE ROLE hunt_agent NOLOGIN;
GRANT USAGE ON SCHEMA api TO hunt_agent;
GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA api TO hunt_agent;
ALTER DEFAULT PRIVILEGES IN SCHEMA api GRANT SELECT, INSERT ON TABLES TO hunt_agent;
```

Agents that only read use the PostgREST endpoint (port 3000, anonymous).
Agents that write connect directly to Postgres (port 5432) with `hunt_agent` credentials.

---

## 3. Schema

All tables live in the `api` schema so PostgREST exposes them automatically.

```sql
CREATE SCHEMA IF NOT EXISTS api;

-- Observations: the core record type.
-- document holds the full original JSON as JSONB (schemas preserved as-is).
CREATE TABLE api.observations (
    id          TEXT PRIMARY KEY,
    kind        TEXT NOT NULL,
    accepted_at TIMESTAMPTZ NOT NULL,
    fingerprint TEXT NOT NULL,
    schema_urn  TEXT,
    document    JSONB NOT NULL
);

-- Tags extracted for fast filtering.
-- Query: all observations in a lane, all PRIMARY findings, etc.
CREATE TABLE api.observation_tags (
    observation_id TEXT NOT NULL REFERENCES api.observations(id) ON DELETE CASCADE,
    key            TEXT NOT NULL,
    value          TEXT NOT NULL,
    PRIMARY KEY (observation_id, key)
);

-- Edges as a proper graph table.
-- subject/predicate/object as columns enable recursive CTE traversals.
CREATE TABLE api.edges (
    id          TEXT PRIMARY KEY,
    subject     TEXT NOT NULL,
    predicate   TEXT NOT NULL,
    object      TEXT NOT NULL,
    accepted_at TIMESTAMPTZ NOT NULL,
    document    JSONB NOT NULL
);

-- Artifacts: metadata in the DB, bytes on disk.
-- sha256 is the content key. Path points to the file.
CREATE TABLE api.artifacts (
    id          TEXT PRIMARY KEY,
    sha256      TEXT NOT NULL UNIQUE,
    path        TEXT NOT NULL,
    size_bytes  BIGINT,
    mime_type   TEXT,
    accepted_at TIMESTAMPTZ NOT NULL,
    metadata    JSONB NOT NULL
);

-- Claims with confidence (Counsel/Red team verdicts).
CREATE TABLE api.claims (
    id          TEXT PRIMARY KEY,
    confidence  TEXT,
    accepted_at TIMESTAMPTZ NOT NULL,
    document    JSONB NOT NULL
);

-- Sources for provenance.
CREATE TABLE api.sources (
    id          TEXT PRIMARY KEY,
    accepted_at TIMESTAMPTZ NOT NULL,
    document    JSONB NOT NULL
);
```

---

## 4. Indexes

```sql
CREATE INDEX idx_obs_kind       ON api.observations(kind);
CREATE INDEX idx_obs_accepted   ON api.observations(accepted_at);
CREATE INDEX idx_obs_doc        ON api.observations USING GIN (document);
CREATE INDEX idx_obs_schema     ON api.observations(schema_urn);

CREATE INDEX idx_tags_key_value ON api.observation_tags(key, value);
CREATE INDEX idx_tags_obs       ON api.observation_tags(observation_id);

CREATE INDEX idx_edges_subject   ON api.edges(subject);
CREATE INDEX idx_edges_object   ON api.edges(object);
CREATE INDEX idx_edges_predicate ON api.edges(predicate);
CREATE INDEX idx_edges_doc      ON api.edges USING GIN (document);

CREATE INDEX idx_artifacts_sha  ON api.artifacts(sha256);
```

---

## 5. Blackboard Channels (LISTEN/NOTIFY)

Agents subscribe to these channels instead of polling.

```sql
-- New observation inserted
CREATE OR REPLACE FUNCTION api.notify_new_observation()
RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('new_observation',
        json_build_object(
            'id',     NEW.id,
            'kind',   NEW.kind,
            'schema', NEW.schema_urn
        )::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_new_observation ON api.observations;
CREATE TRIGGER trg_new_observation
    AFTER INSERT ON api.observations
    FOR EACH ROW EXECUTE FUNCTION api.notify_new_observation();

-- New edge inserted
CREATE OR REPLACE FUNCTION api.notify_new_edge()
RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('new_edge',
        json_build_object(
            'id',        NEW.id,
            'subject',   NEW.subject,
            'predicate', NEW.predicate,
            'object',    NEW.object
        )::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_new_edge ON api.edges;
CREATE TRIGGER trg_new_edge
    AFTER INSERT ON api.edges
    FOR EACH ROW EXECUTE FUNCTION api.notify_new_edge();

-- New claim/verdict inserted
CREATE OR REPLACE FUNCTION api.notify_new_claim()
RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('new_claim',
        json_build_object(
            'id',         NEW.id,
            'confidence', NEW.confidence
        )::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_new_claim ON api.claims;
CREATE TRIGGER trg_new_claim
    AFTER INSERT ON api.claims
    FOR EACH ROW EXECUTE FUNCTION api.notify_new_claim();
```

### Subscribing (Python example)

```python
import psycopg2
import select
import json

conn = psycopg2.connect("postgresql://hunt:hunt-secret-change-me@localhost:5432/hunt")
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
cur.execute("LISTEN new_observation;")
cur.execute("LISTEN new_edge;")
cur.execute("LISTEN new_claim;")

print("Subscribed. Waiting for events...")
while True:
    if select.select([conn], [], [], 5) == ([], [], []):
        continue
    conn.poll()
    while conn.notifies:
        notify = conn.notifies.pop(0)
        print(f"Channel: {notify.channel}")
        print(f"Payload: {json.loads(notify.payload)}")
```

---

## 6. Graph Traversal Example

Find all records connected to a term across lanes (recursive CTE):

```sql
WITH RECURSIVE connected AS (
    -- Start: edges where subject matches
    SELECT subject, predicate, object, 1 AS depth
    FROM api.edges
    WHERE subject = 'observation_abc123'
    UNION
    -- Recurse: follow edges from each found object
    SELECT e.subject, e.predicate, e.object, c.depth + 1
    FROM api.edges e
    JOIN connected c ON e.subject = c.object
    WHERE c.depth < 5
)
SELECT DISTINCT subject, predicate, object FROM connected;
```

---

## 7. Verification Checklist

Run these to confirm the setup is correct:

```bash
# Postgres is up
docker exec hunt-db pg_isready -U hunt -d hunt

# Tables exist
docker exec hunt-db psql -U hunt -d hunt -c "\dt api.*"

# PostgREST is serving
curl -s http://localhost:3000/observations?limit=1

# LISTEN/NOTIFY works (in psql, two sessions)
# Session 1: LISTEN new_observation;
# Session 2: INSERT a test row, confirm Session 1 receives the notification
```

---

## 8. File Layout

```
hunt-db/
├── docker-compose.yml
├── init/
│   ├── 01-roles.sql      # Section 2
│   ├── 02-schema.sql      # Section 3
│   ├── 03-indexes.sql     # Section 4
│   └── 04-triggers.sql    # Section 5
└── README.md              # This file
```

Place sections 2–5 as numbered `.sql` files in `init/`. They run in order on first `docker compose up`.

---

## Notes

- Change `hunt-secret-change-me` before anything touches a network.
- The `api` schema is what PostgREST exposes. Internal tables go in a separate schema if needed.
- Artifacts (raw bytes) stay on disk. The DB holds path + sha256 + metadata.
- Back up with `docker exec hunt-db pg_dump -U hunt hunt > backup.sql`.
