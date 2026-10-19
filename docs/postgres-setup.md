# PostgreSQL Setup for Hunt Database

Target: Mac running Docker and Docker Compose.
Scope: PostgreSQL setup, schema, blackboard channels, and data model constraints.
No data ingestion — that's a separate script.

This document is the single source of truth for getting the initial database
running correctly. It incorporates the record taxonomy, evidence rules, and
hunt doctrine from the existing docs.

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

Create the `init/` directory. Numbered `.sql` files there run in order on first boot.

```bash
docker compose up -d
docker exec hunt-db pg_isready -U hunt -d hunt
curl http://localhost:3000/
```

---

## 2. Database Roles

```sql
-- Read-only role for the PostgREST API
CREATE ROLE hunt_anon NOLOGIN;
GRANT USAGE ON SCHEMA api TO hunt_anon;
GRANT SELECT ON ALL TABLES IN SCHEMA api TO hunt_anon;
ALTER DEFAULT PRIVILEGES IN SCHEMA api GRANT SELECT ON TABLES TO hunt_anon;

-- Read-write role for agents that ingest findings
CREATE ROLE hunt_agent NOLOGIN;
GRANT USAGE ON SCHEMA api TO hunt_agent;
GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA api TO hunt_agent;
ALTER DEFAULT PRIVILEGES IN SCHEMA api GRANT SELECT, INSERT ON TABLES TO hunt_agent;
```

Read-only agents use PostgREST (port 3000, anonymous).
Writing agents connect to Postgres directly (port 5432) with `hunt_agent`.

---

## 3. Schema

All tables in the `api` schema so PostgREST exposes them.

```sql
CREATE SCHEMA IF NOT EXISTS api;

-- Observations: the core record type.
-- document holds the full original JSON as JSONB. Schemas are preserved as-is.
-- See Section 8 for the registered observation types this must support.
CREATE TABLE api.observations (
    id          TEXT PRIMARY KEY,
    kind        TEXT NOT NULL,
    accepted_at TIMESTAMPTZ NOT NULL,
    fingerprint TEXT NOT NULL,
    schema_urn  TEXT,
    grade       TEXT NOT NULL DEFAULT 'ungraded'
                CHECK (grade IN ('ungraded', 'observed', 'inference', 'upstream')),
    document    JSONB NOT NULL
);

-- Tags extracted for fast filtering.
CREATE TABLE api.observation_tags (
    observation_id TEXT NOT NULL REFERENCES api.observations(id) ON DELETE CASCADE,
    key            TEXT NOT NULL,
    value          TEXT NOT NULL,
    PRIMARY KEY (observation_id, key)
);

-- Edges as a proper graph table for recursive CTE traversals.
CREATE TABLE api.edges (
    id          TEXT PRIMARY KEY,
    subject     TEXT NOT NULL,
    predicate   TEXT NOT NULL,
    object      TEXT NOT NULL,
    accepted_at TIMESTAMPTZ NOT NULL,
    document    JSONB NOT NULL
);

-- Artifacts: metadata in DB, bytes on disk.
-- sha256 is the content key. Never store redacted values — see Section 9.
CREATE TABLE api.artifacts (
    id          TEXT PRIMARY KEY,
    sha256      TEXT NOT NULL UNIQUE,
    path        TEXT NOT NULL,
    size_bytes  BIGINT,
    mime_type   TEXT,
    accepted_at TIMESTAMPTZ NOT NULL,
    metadata    JSONB NOT NULL
);

-- Claims with confidence and epistemic grade.
-- See Section 9 for the OBSERVED / INFERENCE / UPSTREAM distinction.
CREATE TABLE api.claims (
    id          TEXT PRIMARY KEY,
    confidence  TEXT,
    epistemic   TEXT NOT NULL DEFAULT 'inference'
                CHECK (epistemic IN ('observed', 'inference', 'upstream')),
    accepted_at TIMESTAMPTZ NOT NULL,
    document    JSONB NOT NULL
);

-- Sources for provenance. Every observation should link to one.
CREATE TABLE api.sources (
    id          TEXT PRIMARY KEY,
    accepted_at TIMESTAMPTZ NOT NULL,
    document    JSONB NOT NULL
);

-- Retractions: corrections are logged, never erased.
-- The original record stays. This table explains what changed.
CREATE TABLE api.retractions (
    id          TEXT PRIMARY KEY,
    target_id   TEXT NOT NULL REFERENCES api.observations(id),
    reason      TEXT NOT NULL,
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
CREATE INDEX idx_obs_grade      ON api.observations(grade);

CREATE INDEX idx_tags_key_value ON api.observation_tags(key, value);
CREATE INDEX idx_tags_obs       ON api.observation_tags(observation_id);

CREATE INDEX idx_edges_subject   ON api.edges(subject);
CREATE INDEX idx_edges_object   ON api.edges(object);
CREATE INDEX idx_edges_predicate ON api.edges(predicate);
CREATE INDEX idx_edges_doc      ON api.edges USING GIN (document);

CREATE INDEX idx_artifacts_sha  ON api.artifacts(sha256);
CREATE INDEX idx_claims_epistemic ON api.claims(epistemic);
CREATE INDEX idx_retractions_target ON api.retractions(target_id);
```

---

## 5. Blackboard Channels (LISTEN/NOTIFY)

Agents subscribe instead of polling.

```sql
CREATE OR REPLACE FUNCTION api.notify_new_observation()
RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('new_observation',
        json_build_object('id', NEW.id, 'kind', NEW.kind,
                          'schema', NEW.schema_urn, 'grade', NEW.grade)::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_new_observation ON api.observations;
CREATE TRIGGER trg_new_observation
    AFTER INSERT ON api.observations
    FOR EACH ROW EXECUTE FUNCTION api.notify_new_observation();

CREATE OR REPLACE FUNCTION api.notify_new_edge()
RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('new_edge',
        json_build_object('id', NEW.id, 'subject', NEW.subject,
                          'predicate', NEW.predicate, 'object', NEW.object)::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_new_edge ON api.edges;
CREATE TRIGGER trg_new_edge
    AFTER INSERT ON api.edges
    FOR EACH ROW EXECUTE FUNCTION api.notify_new_edge();

CREATE OR REPLACE FUNCTION api.notify_new_claim()
RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('new_claim',
        json_build_object('id', NEW.id, 'confidence', NEW.confidence,
                          'epistemic', NEW.epistemic)::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_new_claim ON api.claims;
CREATE TRIGGER trg_new_claim
    AFTER INSERT ON api.claims
    FOR EACH ROW EXECUTE FUNCTION api.notify_new_claim();
```

### Python Subscribe Example

```python
import psycopg2, select, json

conn = psycopg2.connect("postgresql://hunt:hunt-secret-change-me@localhost:5432/hunt")
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
cur.execute("LISTEN new_observation;")
cur.execute("LISTEN new_edge;")
cur.execute("LISTEN new_claim;")

while True:
    if select.select([conn], [], [], 5) == ([], [], []):
        continue
    conn.poll()
    while conn.notifies:
        n = conn.notifies.pop(0)
        print(f"{n.channel}: {json.loads(n.payload)}")
```

---

## 6. Graph Traversal

```sql
WITH RECURSIVE connected AS (
    SELECT subject, predicate, object, 1 AS depth
    FROM api.edges
    WHERE subject = 'observation_abc123'
    UNION
    SELECT e.subject, e.predicate, e.object, c.depth + 1
    FROM api.edges e
    JOIN connected c ON e.subject = c.object
    WHERE c.depth < 5
)
SELECT DISTINCT subject, predicate, object FROM connected;
```

---

## 7. Verification

```bash
docker exec hunt-db pg_isready -U hunt -d hunt
docker exec hunt-db psql -U hunt -d hunt -c "\dt api.*"
curl -s http://localhost:3000/observations?limit=1
```

---

## 8. Registered Observation Types

The `document` JSONB column must support these schemas without modification.
The `schema_urn` column holds the URN for each.

**Infrastructure** (`factum-infra`):
- `infra.ioc` — indicator term with category and status
- `infra.dead_drop` — exfiltration endpoint
- `infra.message` — intercepted message
- `infra.package` — package registry finding
- `infra.proxy_chain` — observed proxy usage
- `infra.proxy_instance` — deployed proxy infrastructure
- `infra.shortcut` — short URL with destination
- `infra.tunnel` — reverse tunnel

**Behavior** (`factum-behavior`):
- `behavior.profile` — per-model behavioral profile
- `behavior.tool_sequence` — ordered tool-call steps from a trajectory

**Hunt** (`factum-hunt`):
- `intel.ioc`, `proxy.chain`, `exfil.dead_drop`

**Intel** (`factum-intel`):
- `intel.report`, `intel.behavior`, `intel.ttp`

**Malware** (`factum-malware`):
- `malware.family` — AI-assisted malware family

**Web** (`factum-web`):
- `web.capture`, `reachability.check`

**Datasets** (`factum-datasets`):
- `dataset.snapshot`, `dataset.record`

**Core predicates** (for edges):
- `in_lane`, `part_of`, `derived_from`, `related_to`
- `supports`, `contradicts`, `copied_from`, `updates`
- `exhibits`, `uses`

---

## 9. Evidence Rules (DB Constraints)

These rules from the project docs are load-bearing for the schema design.

### Never redact
Evidence keeps full observed values. No `[REDACTED]` placeholders in
`document` JSONB. If a value is sensitive, annotate it in metadata —
do not remove it. A redacted value is unverifiable and unmatchable.

### Epistemic grades
Every claim carries one of three labels, enforced by the `epistemic` column:
- **observed** — bytes are present in the cited artifact, verifiable by re-reading
- **inference** — reasoned linkage from observed facts, states its premises
- **upstream** — someone else's claim, cited, not independently verified

Never present an INFERENCE with OBSERVED language.

### Strength grades
Findings carry a strength grade in `document`:
`confirmed`, `agent-shaped-unconfirmed`, `lead`, `watchlist-grade`,
`evidence-grade`, `clean-negative`, `could-not-check`.

### Immutability
Records are never edited in place. Corrections go in `api.retractions`,
which reference the original `target_id` and explain the reason.
The original stays.

### Provenance
Every observation should link to a source. The `document` must include:
source locator, acquisition time, and method. A bare URL is a reference,
not proof of preserved content.

### Scope
Agents and agent infrastructure only. No operator identity, registrant
details, or social profiles — not in observations, not in notes.

---

## 10. File Layout

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

---

## Notes

- Change `hunt-secret-change-me` before anything touches a network.
- The `api` schema is what PostgREST exposes. Internal tables go elsewhere.
- Artifacts (raw bytes) stay on disk. DB holds path + sha256 + metadata.
- Back up: `docker exec hunt-db pg_dump -U hunt hunt > backup.sql`
- Full record type definitions: `docs/taxonomy/record-types.md`
- Full evidence contract: `docs/evidence-rules.md`
- Hunt honesty rules: `docs/hunt-doctrine.md`
