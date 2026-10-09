# Factum data contract reference

This file is a navigation aid, not a duplicate schema specification.

## Where the contract lives

- **Accepted record shapes:** the host corpus's installed JSON Schemas under
  `data/schema-packs/`.
- **Active pack versions and file hashes:** `data/schema-lock.json`.
- **Storage, identity, references, integrity, and recovery:**
  [ARCHITECTURE.md](../ARCHITECTURE.md).
- **Agent workflow:** [SKILL.md](../SKILL.md).
- **Installing and extending schemas:** [INSTALL.md](../INSTALL.md).

The installed skill's `scripts/factum_lib/assets/packs/` contains seeds. After initialization,
the corpus's locked copies govern validation.

Do not edit installed packs or portable records to make validation pass.

## Inspect the current contract

Resolve the script relative to the installed skill and pass the host repository:

```bash
uv run <skill-directory>/scripts/factum.py \
  --repo <host-repository> schema list
```

Inspect a type assignment:

```bash
uv run <skill-directory>/scripts/factum.py \
  --repo <host-repository> \
  schema assigned observable domain
```

Inspect a schema:

```bash
uv run <skill-directory>/scripts/factum.py \
  --repo <host-repository> \
  schema describe urn:factum:core:observable:1
```

Use these commands rather than assuming that an example in documentation
describes every installed type.

## Submission versus stored record

An agent submits a bundle entry:

```json
{
  "ref": "domain",
  "kind": "observable",
  "body": {
    "type": "domain",
    "value": "Example.COM"
  },
  "tags": {}
}
```

This entry belongs inside a complete bundle with `"bundle": 2`, an actor,
and an idempotency key.

Factum assigns:

- the record ID;
- the acceptance timestamp;
- the core body schema;
- the registered value schema;
- the record fingerprint.

For the seeded `domain` type, the stored body includes:

```json
{
  "type": "domain",
  "value_schema": "urn:factum:core:raw-string:1",
  "value": "Example.COM"
}
```

The evidence value remains unchanged.

## Essential distinctions

- SQLite is rebuildable; pending submissions and local-only bytes may not
  exist anywhere else.
- A record ID, artifact hash, request key, and schema ID identify different
  things.
- `@timestamp` is acceptance time, not necessarily acquisition or event time.
- `tags` is miscellaneous metadata, not an implicit reference container.
- Bundle-local references resolve only in schema-declared reference fields.
- A schema-valid assertion is not necessarily factually true.
- A no-match result is scoped retrieval, not proof of originality.
- Retraction preserves the original record.
- A source link is not proof of preserved bytes.

For complete semantics, extension constraints, and required tests, read
[ARCHITECTURE.md](../ARCHITECTURE.md).