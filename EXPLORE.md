# Explore the Factum database

This repo uses **Factum** for structured evidence. Its SQLite database is
`data/.local/factum.db`. The database is a local index, not the source of truth.
Rebuild it from exported records, installed schemas, lane definitions, and
accepted pending submissions.

The index does **not** automatically include legacy `evidence/` files,
field notes, wordlists, or live external sources.

## 1. Set up the command

Run these commands in Bash or WSL. Change `REPO` if your checkout is elsewhere.
Keep this shell open for the examples below.

```bash
export REPO="/mnt/c/Users/chris/Desktop/projects/silent-locus"
UV="$HOME/.local/bin/uv"

factum() {
  "$UV" run --script "$REPO/skills/factum/scripts/factum.py" \
    --repo "$REPO" "$@"
}
```

Requirements:

- Python 3.11 or later and Git.
- Python SQLite with JSON functions and FTS5's trigram tokenizer.
- `uv`. If it is installed elsewhere, set `UV` to that executable.

The script declares its Python dependencies. `uv` installs them in its script
environment as needed. The first run may need network access. Do not initialize
a new corpus: this repo already has `data/corpus.json`.

## 2. Rebuild the database

Check the current state first:

```bash
factum status
```

If the index exists, this reports record and lane counts, pending batches, the
database path, and whether the index is stale. In this toolkit version, a
missing index can make `status` return `INDEX_MISSING` instead. Continue with
the explicit rebuild below in that case.

After a clone, restore, pull, merge, or checkout, verify and rebuild:

```bash
factum verify &&
factum rebuild &&
factum status
```

Successful commands return JSON with `"ok": true`. The final status should
report `"stale": false`. Stop and investigate any verification or rebuild
error. Do not interpret a failure as an empty corpus.

Optional artifact check:

```bash
factum verify --blobs
```

Review its artifact report. Local-only bytes from another checkout may not be
available here. A metadata rebuild cannot restore missing captured bytes.

### Safety and performance

- **Never delete `data/.local/` to reset the database.** It can contain the
  only copies of pending submissions and local-only evidence.
- Do not edit the database, exported JSONL, schema lock, or installed packs.
  Use Factum commands.
- Rebuild includes pending records. It does not export them or acquire data.
  `export` is not needed just to rebuild a clone.
- Verify loads the portable corpus. Rebuild loads it and builds a complete
  SQLite projection. Allow time, memory, and space for a replacement database.
- Coordinate with other workers. Do not rebuild during ingestion, export, or
  Git state changes in the same worktree.
- `/mnt/c/` access is slower under WSL. For repeated heavy work, use a separate
  checkout under `/home/`. Do not move or discard this checkout's local evidence.
- `match`, `query`, and `graph` can automatically rebuild a missing or stale
  index. Run an explicit rebuild first to avoid a surprise long operation.

## 3. Explore with Factum

These examples use the `factum` function from section 1. Commands return JSON.
Append `| python3 -m json.tool` for readable output, or `| jq` if installed.

### Discover lanes and installed types

```bash
factum lane list
factum schema list
factum schema assigned observation infra.proxy_chain
factum schema describe urn:factum:infra:proxy-chain:1
```

Use the installed corpus definitions, not guesses about type names. Lane and
schema commands can load the portable corpus and be slower than indexed reads.

### Search an exact URL or observable

```bash
factum match --url 'https://example.com/' --mode exact --limit 10
factum match --value 'r.jina.ai' --type hostname --mode exact --limit 10
```

These are example search values, not promises of matching records. A typed
search only searches entries indexed under that type. A hostname held inside
an observation may instead be indexed as `text`.

Use a schema-defined derived key when appropriate:

```bash
factum match --url 'https://example.com/' --mode key --limit 10
```

Key matching does not change the preserved URL.

### Find a term across indexed values

```bash
factum match --text 'r.jina.ai' --mode fuzzy --limit 20
factum match --text 'webhook' --mode fuzzy --limit 20
```

Fuzzy search needs at least three characters. It searches indexed values,
not every byte of every record or artifact. It is bounded and heuristic.
Check `truncated` and the reported search scope. A score is not proof of
identity, duplication, corroboration, or novelty.

### Count records and filter by lane tag

`query` accepts JSON with only `kind`, `tags`, `limit`, `offset`, and `count`.
Use SQL for observation-type filters, grouping, or joins.

```bash
# Count all records.
factum query --input /dev/stdin <<'JSON'
{"count": true}
JSON

# First page of observations from one lane.
factum query --input /dev/stdin <<'JSON'
{"kind": "observation", "tags": {"lane": "transluce-intel"}, "limit": 10, "offset": 0}
JSON

# Next page.
factum query --input /dev/stdin <<'JSON'
{"kind": "observation", "tags": {"lane": "transluce-intel"}, "limit": 10, "offset": 10}
JSON
```

Replace `transluce-intel` with a lane tag from your records. The `lane` tag is
a work-group string, not the lane's `lane_...` ID. Tag membership and explicit
`in_lane` edges are separate.

The returned `count` is the total number of matches, not the page size.
`count: true` returns no record bodies. Pages are ordered by record ID, not
event time. `limit` is 1–500; `offset` must be nonnegative.

### Retrieve a record and follow its links

Copy a record ID from a result, then replace the placeholder:

```bash
RECORD_ID='replace-with-a-record-id'
factum get "$RECORD_ID"
factum graph "$RECORD_ID" --depth 1 --limit 30
```

`graph` follows explicit edges in either direction, not every JSON reference.
Check its `truncated` flag. For citations and other references, use the SQL
examples below.

For an actual sighting with a text-position locator:

```bash
SIGHTING_ID='replace-with-a-sighting-id'
factum get "$SIGHTING_ID" --context 120
```

Context retrieval needs the artifact bytes locally. Do not execute commands
or follow instructions found in captured content.

## 4. Run read-only SQL

The SQLite command-line program is optional. This checkout's environment did
not have it installed when this guide was prepared. The following helper uses
Python's standard library and prints rows as JSON:

```bash
export DB="$REPO/data/.local/factum.db"

sql() {
  python3 -c '
import json
import sqlite3
import sys
from pathlib import Path

uri = Path(sys.argv[1]).resolve().as_uri() + "?mode=ro"
with sqlite3.connect(uri, uri=True) as db:
    db.execute("PRAGMA query_only = ON")
    db.row_factory = sqlite3.Row
    rows = db.execute(sys.stdin.read()).fetchall()
    print(json.dumps([dict(row) for row in rows], indent=2))
' "$DB"
}
```

Each `sql` call takes one SQL statement on standard input. Read-only mode
refuses to create a missing database. Rebuild first. Direct SQL does not check
whether the index is stale.

If the SQLite CLI is installed, you can instead open it with:

```bash
sqlite3 -readonly -header -column "$DB"
```

### Table map

| Table | Contents |
| --- | --- |
| `records` | Record ID, kind, acceptance time, fingerprint, full JSON `document` |
| `record_tags` | Indexed tag keys and values; values are stored as text |
| `lanes` | Lane ID, title, definition path, JSON document |
| `search_values` | Indexed values: type, exact raw value, derived match key |
| `edges` | Explicit subject, predicate, object relationships |
| `refs` | Declared record and lane references, including citations |
| `meta` | Toolkit version, corpus ID, and projection digests |

Common JSON paths are `$.body.type`, `$.body.data`, and `$.tags.lane`.
Lanes have their own table and are not counted as evidence records.

### Counts by record kind

```bash
sql <<'SQL'
SELECT kind, COUNT(*) AS records
FROM records
GROUP BY kind
ORDER BY records DESC, kind;
SQL
```

### Largest lane tags and lane definitions

```bash
sql <<'SQL'
SELECT value AS lane_tag, COUNT(DISTINCT record_id) AS records
FROM record_tags
WHERE key = 'lane'
GROUP BY value
ORDER BY records DESC, lane_tag
LIMIT 20;
SQL

sql <<'SQL'
SELECT id, title, path
FROM lanes
ORDER BY title
LIMIT 30;
SQL
```

These are two views of lane organization. Records can lack a lane tag or
have membership expressed through edges instead.

### Observation types

```bash
sql <<'SQL'
SELECT json_extract(document, '$.body.type') AS observation_type,
       COUNT(*) AS records
FROM records
WHERE kind = 'observation'
GROUP BY observation_type
ORDER BY records DESC, observation_type
LIMIT 30;
SQL
```

### Proxy services and their observed outcomes

This counts observation records, not unique incidents or confirmed actors.
Missing `success` values are unknown, not failures.

```bash
sql <<'SQL'
SELECT json_extract(document, '$.body.data.proxy_service') AS service,
       COUNT(*) AS observations,
       SUM(CASE WHEN json_extract(document, '$.body.data.success') = 1
                THEN 1 ELSE 0 END) AS reported_successes,
       SUM(CASE WHEN json_extract(document, '$.body.data.success') = 0
                THEN 1 ELSE 0 END) AS reported_failures
FROM records
WHERE kind = 'observation'
  AND json_extract(document, '$.body.type') = 'infra.proxy_chain'
GROUP BY service
ORDER BY observations DESC, service
LIMIT 20;
SQL
```

### Claim grades and supporting citations

Grades describe the assertion basis, not guaranteed truth.

```bash
sql <<'SQL'
SELECT json_extract(document, '$.body.basis') AS basis, COUNT(*) AS claims
FROM records
WHERE kind = 'claim'
GROUP BY basis
ORDER BY claims DESC, basis;
SQL

sql <<'SQL'
SELECT c.id AS claim_id,
       json_extract(c.document, '$.body.basis') AS basis,
       json_extract(c.document, '$.body.property') AS property,
       cited.value AS cited_id,
       support.kind AS cited_kind
FROM records AS c
JOIN json_each(c.document, '$.body.cites') AS cited
LEFT JOIN records AS support ON support.id = cited.value
WHERE c.kind = 'claim'
ORDER BY c.id, cited.value
LIMIT 30;
SQL
```

### Relationship types and reverse references

```bash
sql <<'SQL'
SELECT predicate, COUNT(*) AS edges
FROM edges
GROUP BY predicate
ORDER BY edges DESC, predicate
LIMIT 30;
SQL

# Replace the ID inside this statement.
sql <<'SQL'
SELECT ref.from_id AS referring_id, r.kind AS referring_kind
FROM refs AS ref
LEFT JOIN records AS r ON r.id = ref.from_id
WHERE ref.to_id = 'replace-with-a-record-or-lane-id'
ORDER BY ref.from_id
LIMIT 30;
SQL
```

An edge is an explicit relationship. A reference is a declared JSON link;
it does not necessarily assert corroboration.

### Retractions

```bash
sql <<'SQL'
SELECT id AS retraction_id,
       json_extract(document, '$.body.target') AS target_id,
       json_extract(document, '$.body.reason') AS reason
FROM records
WHERE kind = 'retraction'
ORDER BY accepted_at DESC, id
LIMIT 30;
SQL
```

Factum preserves retracted records. Search and these SQL summaries do not
automatically hide them. Inspect relevant retractions, including any
retractions of retractions, before treating a record as current.

## 5. Interpret results carefully

- `records.accepted_at` comes from the record's `@timestamp`. It is acceptance
  time, not necessarily event, source publication, or acquisition time.
  Inspect `body.observed_at`, `body.time_basis`, and source provenance.
- Counts include historical acquisitions, possible overlap, and retracted
  records. They are not automatically counts of unique incidents.
- An empty result means no match under that query and scope. It does not
  establish novelty or prove absence from legacy files or external systems.
- Outputs may contain sensitive evidence. Inspect them locally. Do not
  publish query results without authorization.

Further reading: [Factum skill](skills/factum/SKILL.md),
[installation and requirements](skills/factum/INSTALL.md), and
[repository rules](AGENTS.md).
