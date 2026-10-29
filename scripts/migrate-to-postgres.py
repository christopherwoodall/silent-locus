#!/usr/bin/env python3
"""
migrate-to-postgres.py — Migrate Factum SQLite to PostgreSQL. Does everything.

Creates the schema, migrates all records, sets up indexes, triggers,
and LISTEN/NOTIFY channels for the blackboard pattern.

Usage:
    python3 migrate-to-postgres.py --dsn "postgresql://user:pass@localhost:5432/hunt"
    python3 migrate-to-postgres.py --dsn "$DATABASE_URL" --dry-run

Idempotent: safe to re-run. Uses ON CONFLICT DO NOTHING.

Requirements:
    pip install psycopg2-binary
    PostgreSQL 14+ running (Postgres.app on Mac works fine)
"""

import argparse
import json
import sqlite3
import sys

FACTUM_DB = "data/.local/factum.db"
BATCH_SIZE = 5000

SCHEMA_SQL = """
-- Core tables. document holds the full Factum JSON as JSONB.
-- Tags are extracted to a separate table for fast filtering.

CREATE TABLE IF NOT EXISTS observations (
    id          TEXT PRIMARY KEY,
    kind        TEXT NOT NULL,
    accepted_at TIMESTAMPTZ NOT NULL,
    fingerprint TEXT NOT NULL,
    schema_urn  TEXT,
    document    JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS observation_tags (
    observation_id TEXT NOT NULL REFERENCES observations(id) ON DELETE CASCADE,
    key            TEXT NOT NULL,
    value          TEXT NOT NULL,
    PRIMARY KEY (observation_id, key)
);

-- Edges as a proper graph table for recursive CTE traversals.
CREATE TABLE IF NOT EXISTS edges (
    id          TEXT PRIMARY KEY,
    subject     TEXT NOT NULL,
    predicate   TEXT NOT NULL,
    object      TEXT NOT NULL,
    accepted_at TIMESTAMPTZ NOT NULL,
    document    JSONB NOT NULL
);

-- Artifacts: metadata in DB, bytes on disk (or MinIO).
-- sha256 is the content key.
CREATE TABLE IF NOT EXISTS artifacts (
    id          TEXT PRIMARY KEY,
    sha256      TEXT NOT NULL UNIQUE,
    path        TEXT NOT NULL,
    size_bytes  BIGINT,
    mime_type   TEXT,
    accepted_at TIMESTAMPTZ NOT NULL,
    metadata    JSONB NOT NULL
);

-- Claims with confidence for Counsel/Red team verdicts.
CREATE TABLE IF NOT EXISTS claims (
    id          TEXT PRIMARY KEY,
    confidence  TEXT,
    accepted_at TIMESTAMPTZ NOT NULL,
    document    JSONB NOT NULL
);

-- Sources for provenance.
CREATE TABLE IF NOT EXISTS sources (
    id          TEXT PRIMARY KEY,
    accepted_at TIMESTAMPTZ NOT NULL,
    document    JSONB NOT NULL
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_obs_kind ON observations(kind);
CREATE INDEX IF NOT EXISTS idx_obs_accepted ON observations(accepted_at);
CREATE INDEX IF NOT EXISTS idx_obs_doc ON observations USING GIN (document);
CREATE INDEX IF NOT EXISTS idx_obs_schema ON observations(schema_urn);
CREATE INDEX IF NOT EXISTS idx_tags_key_value ON observation_tags(key, value);
CREATE INDEX IF NOT EXISTS idx_tags_obs ON observation_tags(observation_id);
CREATE INDEX IF NOT EXISTS idx_edges_subject ON edges(subject);
CREATE INDEX IF NOT EXISTS idx_edges_object ON edges(object);
CREATE INDEX IF NOT EXISTS idx_edges_predicate ON edges(predicate);
CREATE INDEX IF NOT EXISTS idx_edges_doc ON edges USING GIN (document);
CREATE INDEX IF NOT EXISTS idx_artifacts_sha ON artifacts(sha256);

-- Blackboard: notify on new observations.
-- Agents LISTEN on these channels.
CREATE OR REPLACE FUNCTION notify_new_observation() RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('new_observation',
        json_build_object(
            'id', NEW.id,
            'kind', NEW.kind,
            'schema', NEW.schema_urn
        )::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_new_observation ON observations;
CREATE TRIGGER trg_new_observation
    AFTER INSERT ON observations
    FOR EACH ROW EXECUTE FUNCTION notify_new_observation();

CREATE OR REPLACE FUNCTION notify_new_edge() RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('new_edge',
        json_build_object(
            'id', NEW.id,
            'subject', NEW.subject,
            'predicate', NEW.predicate,
            'object', NEW.object
        )::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_new_edge ON edges;
CREATE TRIGGER trg_new_edge
    AFTER INSERT ON edges
    FOR EACH ROW EXECUTE FUNCTION notify_new_edge();

-- Counsel verdicts channel
CREATE OR REPLACE FUNCTION notify_new_claim() RETURNS trigger AS $$
BEGIN
    PERFORM pg_notify('new_claim',
        json_build_object('id', NEW.id, 'confidence', NEW.confidence)::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_new_claim ON claims;
CREATE TRIGGER trg_new_claim
    AFTER INSERT ON claims
    FOR EACH ROW EXECUTE FUNCTION notify_new_claim();
"""


def migrate(dsn, dry_run=False):
    # Connect to SQLite
    sq = sqlite3.connect(FACTUM_DB)
    sq.row_factory = sqlite3.Row

    if dry_run:
        counts = {}
        for row in sq.execute("SELECT kind, COUNT(*) as c FROM records GROUP BY kind"):
            counts[row["kind"]] = row["c"]
        print("DRY RUN — would migrate:")
        for kind, count in sorted(counts.items()):
            print(f"  {kind}: {count:,}")
        print(f"  Total: {sum(counts.values()):,}")
        sq.close()
        return

    try:
        import psycopg2
        import psycopg2.extras
    except ImportError:
        print("ERROR: pip install psycopg2-binary", file=sys.stderr)
        sys.exit(1)

    # Connect to Postgres
    pg = psycopg2.connect(dsn)
    pg.autocommit = False
    cur = pg.cursor()

    print("Creating schema...")
    cur.execute(SCHEMA_SQL)
    pg.commit()

    # Migrate records
    total = sq.execute("SELECT COUNT(*) as c FROM records").fetchone()["c"]
    print(f"Migrating {total:,} records...")

    migrated = {"observations": 0, "edges": 0, "artifacts": 0,
                "claims": 0, "sources": 0, "other": 0}

    batch_obs = []
    batch_tags = []
    batch_edges = []
    batch_artifacts = []
    batch_claims = []
    batch_sources = []

    def flush():
        if batch_obs:
            psycopg2.extras.execute_values(cur,
                """INSERT INTO observations (id, kind, accepted_at, fingerprint, schema_urn, document)
                   VALUES %s ON CONFLICT (id) DO NOTHING""",
                batch_obs, template="(%s,%s,%s,%s,%s,%s::jsonb)")
        if batch_tags:
            psycopg2.extras.execute_values(cur,
                """INSERT INTO observation_tags (observation_id, key, value)
                   VALUES %s ON CONFLICT DO NOTHING""",
                batch_tags)
        if batch_edges:
            psycopg2.extras.execute_values(cur,
                """INSERT INTO edges (id, subject, predicate, object, accepted_at, document)
                   VALUES %s ON CONFLICT (id) DO NOTHING""",
                batch_edges, template="(%s,%s,%s,%s,%s,%s::jsonb)")
        if batch_artifacts:
            psycopg2.extras.execute_values(cur,
                """INSERT INTO artifacts (id, sha256, path, size_bytes, mime_type, accepted_at, metadata)
                   VALUES %s ON CONFLICT (id) DO NOTHING""",
                batch_artifacts, template="(%s,%s,%s,%s,%s,%s,%s::jsonb)")
        if batch_claims:
            psycopg2.extras.execute_values(cur,
                """INSERT INTO claims (id, confidence, accepted_at, document)
                   VALUES %s ON CONFLICT (id) DO NOTHING""",
                batch_claims, template="(%s,%s,%s,%s::jsonb)")
        if batch_sources:
            psycopg2.extras.execute_values(cur,
                """INSERT INTO sources (id, accepted_at, document)
                   VALUES %s ON CONFLICT (id) DO NOTHING""",
                batch_sources, template="(%s,%s,%s::jsonb)")
        pg.commit()
        batch_obs.clear(); batch_tags.clear(); batch_edges.clear()
        batch_artifacts.clear(); batch_claims.clear(); batch_sources.clear()

    done = 0
    for row in sq.execute("SELECT id, kind, accepted_at, fingerprint, document FROM records"):
        try:
            doc = json.loads(row["document"])
        except (json.JSONDecodeError, TypeError):
            continue

        doc_json = json.dumps(doc)
        schema_urn = doc.get("schema", "")
        tags = doc.get("tags", {})

        if row["kind"] == "edge":
            body = doc.get("body", {})
            batch_edges.append((
                row["id"],
                body.get("subject", ""),
                body.get("predicate", ""),
                body.get("object", ""),
                row["accepted_at"],
                doc_json,
            ))
            migrated["edges"] += 1
        elif row["kind"] == "artifact":
            body = doc.get("body", {})
            batch_artifacts.append((
                row["id"],
                body.get("sha256", ""),
                body.get("path", body.get("locator", "")),
                body.get("size_bytes"),
                body.get("mime_type", ""),
                row["accepted_at"],
                doc_json,
            ))
            migrated["artifacts"] += 1
        elif row["kind"] == "claim":
            batch_claims.append((
                row["id"],
                doc.get("body", {}).get("confidence", ""),
                row["accepted_at"],
                doc_json,
            ))
            migrated["claims"] += 1
        elif row["kind"] == "source":
            batch_sources.append((
                row["id"],
                row["accepted_at"],
                doc_json,
            ))
            migrated["sources"] += 1
        else:
            # observation, event, observable, run, retraction → observations table
            batch_obs.append((
                row["id"],
                row["kind"],
                row["accepted_at"],
                row["fingerprint"],
                schema_urn,
                doc_json,
            ))
            for k, v in tags.items():
                if isinstance(v, str):
                    batch_tags.append((row["id"], k, v))
            migrated["observations"] += 1

        done += 1
        if done % BATCH_SIZE == 0:
            flush()
            print(f"  {done:,}/{total:,} ({done/total*100:.1f}%)")

    flush()
    pg.commit()

    print("\nDone. Migrated:")
    for kind, count in sorted(migrated.items()):
        print(f"  {kind}: {count:,}")
    print(f"  Total: {sum(migrated.values()):,}")

    # Verify
    cur.execute("SELECT COUNT(*) FROM observations")
    obs_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM edges")
    edge_count = cur.fetchone()[0]
    print(f"\nPostgres now holds: {obs_count:,} observations, {edge_count:,} edges")

    cur.close()
    pg.close()
    sq.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate Factum to PostgreSQL")
    parser.add_argument("--dsn", required=True, help="Postgres connection string")
    parser.add_argument("--dry-run", action="store_true", help="Show counts only")
    args = parser.parse_args()
    migrate(args.dsn, args.dry_run)
