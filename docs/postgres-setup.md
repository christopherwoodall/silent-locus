# PostgreSQL Setup for Hunt Database

Target: Mac running Docker and Docker Compose.
Scope: PostgreSQL setup, schema, blackboard channels, and data model.
No data ingestion — that's a separate script.

Design influences: Elastic's AlertZero (task-oriented agent watches with
documented decisions). Records are mutable — agents correct mistakes by
updating, not by appending retractions. Status is kanban-based throughout.

---

## 1. Docker Compose

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

```bash
docker compose up -d
docker exec hunt-db pg_isready -U hunt -d hunt
curl http://localhost:3000/
```

---

## 2. Database Roles

```sql
CREATE ROLE hunt_anon NOLOGIN;
GRANT USAGE ON SCHEMA api TO hunt_anon;
GRANT SELECT ON ALL TABLES IN SCHEMA api TO hunt_anon;
ALTER DEFAULT PRIVILEGES IN SCHEMA api GRANT SELECT ON TABLES TO hunt_anon;

CREATE ROLE hunt_agent NOLOGIN;
GRANT USAGE ON SCHEMA api TO hunt_agent;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA api TO hunt_agent;
ALTER DEFAULT PRIVILEGES IN SCHEMA api GRANT SELECT, INSERT, UPDATE ON TABLES TO hunt_agent;
```

Note: agents get UPDATE. Records are mutable by design.

---

## 3. Core Schema

```sql
CREATE SCHEMA IF NOT EXISTS api;

-- Observations: the core record type. MUTABLE.
-- document holds the full original JSON as JSONB.
-- status is kanban: backlog → triaging → analyzing → review → done/dismissed.
CREATE TABLE api.observations (
    id          TEXT PRIMARY KEY,
    kind        TEXT NOT NULL,
    accepted_at TIMESTAMPTZ NOT NULL,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fingerprint TEXT NOT NULL,
    schema_urn  TEXT,
    status      TEXT NOT NULL DEFAULT 'backlog'
                CHECK (status IN ('backlog', 'triaging', 'analyzing',
                                  'review', 'done', 'dismissed')),
    grade       TEXT NOT NULL DEFAULT 'ungraded'
                CHECK (grade IN ('ungraded', 'observed', 'inference', 'upstream')),
    assigned_to TEXT,
    document    JSONB NOT NULL
);

CREATE TABLE api.observation_tags (
    observation_id TEXT NOT NULL REFERENCES api.observations(id) ON DELETE CASCADE,
    key            TEXT NOT NULL,
    value          TEXT NOT NULL,
    PRIMARY KEY (observation_id, key)
);

-- Edges: graph relationships for recursive CTE traversals.
CREATE TABLE api.edges (
    id          TEXT PRIMARY KEY,
    subject     TEXT NOT NULL,
    predicate   TEXT NOT NULL,
    object      TEXT NOT NULL,
    accepted_at TIMESTAMPTZ NOT NULL,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    document    JSONB NOT NULL
);

-- Artifacts: metadata in DB, bytes on disk. sha256 is the content key.
CREATE TABLE api.artifacts (
    id          TEXT PRIMARY KEY,
    sha256      TEXT NOT NULL UNIQUE,
    path        TEXT NOT NULL,
    size_bytes  BIGINT,
    mime_type   TEXT,
    accepted_at TIMESTAMPTZ NOT NULL,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata    JSONB NOT NULL
);

-- Claims: assertions with epistemic grade and kanban status.
CREATE TABLE api.claims (
    id          TEXT PRIMARY KEY,
    confidence  TEXT,
    epistemic   TEXT NOT NULL DEFAULT 'inference'
                CHECK (epistemic IN ('observed', 'inference', 'upstream')),
    status      TEXT NOT NULL DEFAULT 'backlog'
                CHECK (status IN ('backlog', 'triaging', 'analyzing',
                                  'review', 'done', 'dismissed')),
    accepted_at TIMESTAMPTZ NOT NULL,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    document    JSONB NOT NULL
);

-- Sources: provenance for every observation.
CREATE TABLE api.sources (
    id          TEXT PRIMARY KEY,
    accepted_at TIMESTAMPTZ NOT NULL,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    document    JSONB NOT NULL
);
```

---

## 4. Agent Coordination Schema (AlertZero-influenced)

```sql
-- Watches: agent groups with distinct responsibilities.
-- Seed with: triage, hunt, detection, forensics.
CREATE TABLE api.watches (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO api.watches (id, name, description) VALUES
    ('triage',    'Triage Watch',    'Enrich incoming findings, filter false positives with documented reasons'),
    ('hunt',      'Hunt Watch',      'Continuous threat hunting based on threat intelligence'),
    ('detection', 'Detection Watch', 'Analyze detections, suggest new rules and coverage improvements'),
    ('forensics', 'Forensics Watch', 'Deep analysis: malware, exploit paths, complex investigations')
ON CONFLICT (id) DO NOTHING;

-- Agents: registered workers. Each belongs to a watch.
CREATE TABLE api.agents (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    watch_id    TEXT NOT NULL REFERENCES api.watches(id),
    status      TEXT NOT NULL DEFAULT 'idle'
                CHECK (status IN ('idle', 'working', 'offline')),
    last_seen   TIMESTAMPTZ,
    metadata    JSONB NOT NULL DEFAULT '{}',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tasks: kanban work items. The unit of agent collaboration.
-- A task links to an observation, moves through kanban states,
-- and gets assigned to a watch or a specific agent.
CREATE TABLE api.tasks (
    id             TEXT PRIMARY KEY,
    title          TEXT NOT NULL,
    description    TEXT,
    status         TEXT NOT NULL DEFAULT 'backlog'
                   CHECK (status IN ('backlog', 'todo', 'in_progress',
                                     'review', 'done', 'blocked')),
    priority       TEXT NOT NULL DEFAULT 'medium'
                   CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    watch_id       TEXT REFERENCES api.watches(id),
    assigned_to    TEXT REFERENCES api.agents(id),
    observation_id TEXT REFERENCES api.observations(id),
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at   TIMESTAMPTZ,
    metadata       JSONB NOT NULL DEFAULT '{}'
);

-- Decisions: every verdict carries a documented reason.
-- This is the AlertZero pattern: no silent dismissals.
CREATE TABLE api.decisions (
    id          TEXT PRIMARY KEY,
    target_id   TEXT NOT NULL,
    target_kind TEXT NOT NULL
                CHECK (target_kind IN ('observation', 'claim', 'task')),
    verdict     TEXT NOT NULL,
    reason      TEXT NOT NULL,
    decided_by  TEXT NOT NULL REFERENCES api.agents(id),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata    JSONB NOT NULL DEFAULT '{}'
);

-- Findings: consolidated results promoted from observations.
-- When triage confirms something is real, it becomes a finding.
CREATE TABLE api.findings (
    id            TEXT PRIMARY KEY,
    title         TEXT NOT NULL,
    summary       TEXT NOT NULL,
    severity      TEXT NOT NULL
                  CHECK (severity IN ('info', 'low', 'medium', 'high', 'critical')),
    status        TEXT NOT NULL DEFAULT 'open'
                  CHECK (status IN ('open', 'investigating', 'confirmed',
                                    'false_positive', 'closed')),
    observation_ids TEXT[] NOT NULL DEFAULT '{}',
    created_by    TEXT REFERENCES api.agents(id),
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata      JSONB NOT NULL DEFAULT '{}'
);
```

---

## 5. Indexes

```sql
CREATE INDEX idx_obs_kind       ON api.observations(kind);
CREATE INDEX idx_obs_accepted   ON api.observations(accepted_at);
CREATE INDEX idx_obs_doc        ON api.observations USING GIN (document);
CREATE INDEX idx_obs_schema     ON api.observations(schema_urn);
CREATE INDEX idx_obs_status     ON api.observations(status);
CREATE INDEX idx_obs_grade      ON api.observations(grade);
CREATE INDEX idx_obs_assigned   ON api.observations(assigned_to);

CREATE INDEX idx_tags_key_value ON api.observation_tags(key, value);
CREATE INDEX idx_tags_obs       ON api.observation_tags(observation_id);

CREATE INDEX idx_edges_subject   ON api.edges(subject);
CREATE INDEX idx_edges_object   ON api.edges(object);
CREATE INDEX idx_edges_predicate ON api.edges(predicate);
CREATE INDEX idx_edges_doc      ON api.edges USING GIN (document);

CREATE INDEX idx_artifacts_sha  ON api.artifacts(sha256);

CREATE INDEX idx_claims_epistemic ON api.claims(epistemic);
CREATE INDEX idx_claims_status   ON api.claims(status);

CREATE INDEX idx_tasks_status   ON api.tasks(status);
CREATE INDEX idx_tasks_watch    ON api.tasks(watch_id);
CREATE INDEX idx_tasks_assigned ON api.tasks(assigned_to);
CREATE INDEX idx_tasks_obs      ON api.tasks(observation_id);

CREATE INDEX idx_decisions_target ON api.decisions(target_id);
CREATE INDEX idx_decisions_agent  ON api.decisions(decided_by);

CREATE INDEX idx_findings_status   ON api.findings(status);
CREATE INDEX idx_findings_severity ON api.findings(severity);
CREATE INDEX idx_agents_watch  ON api.agents(watch_id);
CREATE INDEX idx_agents_status ON api.agents(status);
```

---

## 6. Updated-At Trigger

Every mutable table auto-updates `updated_at`:

```sql
CREATE OR REPLACE FUNCTION api.touch_updated_at()
RETURNS trigger AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_obs_touch BEFORE UPDATE ON api.observations
    FOR EACH ROW EXECUTE FUNCTION api.touch_updated_at();
CREATE TRIGGER trg_edges_touch BEFORE UPDATE ON api.edges
    FOR EACH ROW EXECUTE FUNCTION api.touch_updated_at();
CREATE TRIGGER trg_artifacts_touch BEFORE UPDATE ON api.artifacts
    FOR EACH ROW EXECUTE FUNCTION api.touch_updated_at();
CREATE TRIGGER trg_claims_touch BEFORE UPDATE ON api.claims
    FOR EACH ROW EXECUTE FUNCTION api.touch_updated_at();
CREATE TRIGGER trg_sources_touch BEFORE UPDATE ON api.sources
    FOR EACH ROW EXECUTE FUNCTION api.touch_updated_at();
CREATE TRIGGER trg_tasks_touch BEFORE UPDATE ON api.tasks
    FOR EACH ROW EXECUTE FUNCTION api.touch_updated_at();
CREATE TRIGGER trg_findings_touch BEFORE UPDATE ON api.findings
    FOR EACH ROW EXECUTE FUNCTION api.touch_updated_at();
```

---

## 7. Blackboard Channels (LISTEN/NOTIFY)

```sql
CREATE OR REPLACE FUNCTION api.notify_new_observation()
RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('new_observation',
        json_build_object('id', NEW.id, 'kind', NEW.kind,
                          'schema', NEW.schema_urn, 'status', NEW.status)::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_new_observation ON api.observations;
CREATE TRIGGER trg_new_observation
    AFTER INSERT ON api.observations
    FOR EACH ROW EXECUTE FUNCTION api.notify_new_observation();

CREATE OR REPLACE FUNCTION api.notify_status_change()
RETURNS trigger AS $$
BEGIN
    IF OLD.status IS DISTINCT FROM NEW.status THEN
        PERFORM pg_notify('status_change',
            json_build_object('id', NEW.id, 'kind', TG_TABLE_NAME,
                              'old', OLD.status, 'new', NEW.status)::text);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_obs_status ON api.observations;
CREATE TRIGGER trg_obs_status
    AFTER UPDATE ON api.observations
    FOR EACH ROW EXECUTE FUNCTION api.notify_status_change();

DROP TRIGGER IF EXISTS trg_task_status ON api.tasks;
CREATE TRIGGER trg_task_status
    AFTER UPDATE ON api.tasks
    FOR EACH ROW EXECUTE FUNCTION api.notify_status_change();

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

CREATE OR REPLACE FUNCTION api.notify_new_task()
RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('new_task',
        json_build_object('id', NEW.id, 'title', NEW.title,
                          'watch_id', NEW.watch_id, 'priority', NEW.priority)::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_new_task ON api.tasks;
CREATE TRIGGER trg_new_task
    AFTER INSERT ON api.tasks
    FOR EACH ROW EXECUTE FUNCTION api.notify_new_task();

CREATE OR REPLACE FUNCTION api.notify_new_decision()
RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('new_decision',
        json_build_object('id', NEW.id, 'target_id', NEW.target_id,
                          'verdict', NEW.verdict, 'by', NEW.decided_by)::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_new_decision ON api.decisions;
CREATE TRIGGER trg_new_decision
    AFTER INSERT ON api.decisions
    FOR EACH ROW EXECUTE FUNCTION api.notify_new_decision();
```

### Channels Summary

| Channel | Fires on | Agents subscribe to |
|---|---|---|
| `new_observation` | INSERT on observations | Triage Watch |
| `new_edge` | INSERT on edges | Hunt Watch (graph mining) |
| `new_task` | INSERT on tasks | All watches |
| `new_decision` | INSERT on decisions | Review agents |
| `status_change` | UPDATE changing status | Kanban board UI, coordinators |

### Python Subscribe Example

```python
import psycopg2, select, json

conn = psycopg2.connect("postgresql://hunt:hunt-secret-change-me@localhost:5432/hunt")
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
for ch in ['new_observation', 'new_edge', 'new_task', 'new_decision', 'status_change']:
    cur.execute(f"LISTEN {ch};")

while True:
    if select.select([conn], [], [], 5) == ([], [], []):
        continue
    conn.poll()
    while conn.notifies:
        n = conn.notifies.pop(0)
        print(f"{n.channel}: {json.loads(n.payload)}")
```

---

## 8. Graph Traversal

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

## 9. Kanban Queries

```sql
-- Board view: all tasks grouped by status
SELECT status, COUNT(*), array_agg(title) AS titles
FROM api.tasks GROUP BY status ORDER BY
    CASE status WHEN 'backlog' THEN 1 WHEN 'todo' THEN 2
         WHEN 'in_progress' THEN 3 WHEN 'review' THEN 4
         WHEN 'done' THEN 5 WHEN 'blocked' THEN 6 END;

-- My queue: tasks assigned to an agent, not done
SELECT id, title, priority, status FROM api.tasks
WHERE assigned_to = 'agent-123' AND status NOT IN ('done')
ORDER BY priority DESC, created_at;

-- Stuck: in progress for more than 24h
SELECT id, title, assigned_to, updated_at FROM api.tasks
WHERE status = 'in_progress' AND updated_at < NOW() - INTERVAL '24 hours';

-- Findings pipeline
SELECT status, COUNT(*) FROM api.findings GROUP BY status;
```

---

## 10. Registered Observation Types

The `document` JSONB must support these schemas without modification:

**Infrastructure:** `infra.ioc`, `infra.dead_drop`, `infra.message`,
`infra.package`, `infra.proxy_chain`, `infra.proxy_instance`,
`infra.shortcut`, `infra.tunnel`

**Behavior:** `behavior.profile`, `behavior.tool_sequence`

**Hunt:** `intel.ioc`, `proxy.chain`, `exfil.dead_drop`

**Intel:** `intel.report`, `intel.behavior`, `intel.ttp`

**Malware:** `malware.family`

**Web:** `web.capture`, `reachability.check`

**Datasets:** `dataset.snapshot`, `dataset.record`

**Core predicates** (edges): `in_lane`, `part_of`, `derived_from`,
`related_to`, `supports`, `contradicts`, `copied_from`, `updates`,
`exhibits`, `uses`

---

## 11. Design Principles

### Mutable by default
Agents UPDATE records to fix mistakes. No retractions table, no
immutability enforcement. The `updated_at` trigger tracks when things
change. If audit history matters later, add a history table — don't
block corrections now.

### Kanban everywhere
`observations.status`: backlog → triaging → analyzing → review → done/dismissed
`tasks.status`: backlog → todo → in_progress → review → done/blocked
`findings.status`: open → investigating → confirmed → false_positive/closed

### Documented decisions
Every verdict in `api.decisions` requires a `reason`. No silent dismissals.
This is the AlertZero pattern: Triage Watch closes false positives only
with a written reason.

### Watches, not free-for-all
Agents register in `api.agents` under a watch. Tasks are assigned to
watches or specific agents. The four default watches mirror AlertZero:
triage (filter), hunt (proactive), detection (improve coverage),
forensics (deep dive).

### Never redact
Evidence keeps full observed values. Annotate sensitivity in metadata,
don't remove values.

---

## 12. Verification

```bash
docker exec hunt-db pg_isready -U hunt -d hunt
docker exec hunt-db psql -U hunt -d hunt -c "\dt api.*"
docker exec hunt-db psql -U hunt -d hunt -c "SELECT * FROM api.watches;"
curl -s http://localhost:3000/tasks?limit=1
```

---

## 13. File Layout

```
hunt-db/
├── docker-compose.yml
├── init/
│   ├── 01-roles.sql       # Section 2
│   ├── 02-schema.sql      # Section 3
│   ├── 03-coordination.sql # Section 4
│   ├── 04-indexes.sql     # Section 5
│   └── 05-triggers.sql    # Sections 6-7
└── README.md              # This file
```

---

## Notes

- Change `hunt-secret-change-me` before anything touches a network.
- The `api` schema is what PostgREST exposes.
- Artifacts (raw bytes) stay on disk. DB holds path + sha256 + metadata.
- Back up: `docker exec hunt-db pg_dump -U hunt hunt > backup.sql`
