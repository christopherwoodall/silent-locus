# Factum architecture

This document describes the current repository-skill implementation and its
extension and testing contracts.

It is not a claim that the implementation has passed the tests listed here.

## 1. System boundary

Factum receives data from external agents and tools.

```text
External acquisition and review
              |
              v
      Factum CLI / uv script
              |
              v
  Schema validation and bundle compilation
              |
              +--> preserved artifact bytes
              +--> durable pending records
              |
              v
        SQLite projection
              |
              v
       Portable batch export
              |
              v
   Agent-controlled Git synchronization
```

Factum does not perform acquisition, remote novelty searches, Git publication,
or agent orchestration.

## 2. Installation versus corpus

The toolkit lives inside the agent's skills directory.

The host repository owns the corpus.

```text
installed-toolkit/
├── SKILL.md
├── scripts/
└── scripts/factum_lib/assets/packs/  # Packaged seeds only

host-repository/
└── data/
    ├── corpus.json
    ├── schema-lock.json
    ├── schema-packs/   # Authoritative installed copies
    ├── records/
    ├── lanes/
    ├── blobs/
    └── .local/
```

The toolkit may be updated independently of the corpus.

A code update must not silently reseed corpus schemas.

## 3. Authoritative data

### Committed portable state

The selected Git tree contains:

- corpus identity;
- installed schema packs and lock;
- exported record batches and receipts;
- editable lane definitions;
- intended Git-retained artifact bytes.

Rebuild does not need to replay every historical commit.

### Unexported accepted state

Pending files under `data/.local/pending/` preserve accepted submissions.

SQLite is not their only copy.

### Local artifact state

Local-only bytes may exist only under `data/.local/blobs/`.

Consequently, ignoring `.local/` in Git does not make the entire directory
safe to delete.

### SQLite

SQLite is a projection over portable records, lanes, and current pending work.

The implementation builds a replacement database, checks it, and replaces the
active index.

It currently uses a generic record table, graph references, supporting search
tables, and core-kind views. It is not the earlier PostgreSQL typed-anchor
backend.

## 4. Identity and integrity

These identities have different purposes:

| Identity | Purpose |
|---|---|
| Corpus ID | Distinguish datasets |
| Record UUID | Distinguish submitted records |
| Artifact SHA-256 | Address and verify bytes |
| Record fingerprint | Detect changed record content |
| Idempotency key | Identify a retried request |
| Request digest | Detect incompatible reuse of a request key |
| Schema `$id` | Identify a schema contract |
| Pack name/version | Identify an immutable installed pack |
| State digest | Identify the validated logical corpus state |

Do not substitute one for another.

Record fingerprints use Factum's canonical JSON serialization. This is not
a claim of RFC 8785 compliance.

Every record carries the system-assigned tag `factum.author`, set at
creation from the bundle's actor. A submitter-provided value is overwritten,
not trusted. The key is immutable: record updates must reject changes to it
with `EVIDENCE_EDIT`. It is part of the signed envelope, so the fingerprint
covers it.

Hashes detect inconsistency. Without an independently trusted signature or
reference, they do not prove who collected evidence or whether a source was
truthful.

## 5. Schema layers

### Core contracts

Core schemas define:

- record envelopes;
- bundle shape;
- identities and references;
- core record bodies;
- locators;
- lanes.

Changing core contracts is development work, potentially requiring migration.

### Type definitions

Definitions map logical types to payload/value schemas.

Example:

```json
{
  "category": "observation",
  "name": "research.webhook_capture",
  "schema": "urn:research:webhooks:capture:1",
  "tags": {}
}
```

Supported categories:

- `observation`
- `observable`
- `event`
- `predicate`

### Assigned schemas

Stored observations and events identify `data_schema`.

Stored observables identify `value_schema`.

The compiler fills omitted assignments from the registry. A supplied
assignment must agree with the registered type.

Assignments are not inferred from whichever installed schema happens to
validate the payload.

## 6. Pack structure

A pack contains a manifest, declared schema files, and definition files.

```text
research-webhooks/1.0.0/
├── pack.json
├── definitions.json
└── schemas/
    └── webhook-capture.schema.json
```

Example manifest:

```json
{
  "pack_format": 1,
  "name": "research-webhooks",
  "version": "1.0.0",
  "requires": {
    "factum-core": "1.0.0"
  },
  "schemas": [
    "schemas/webhook-capture.schema.json"
  ],
  "definitions": [
    "definitions.json"
  ],
  "tags": {}
}
```

Dependencies currently use exact versions.

Schema IDs must be absolute and unique across the installed catalog.

Pack files are pinned by hashes in `data/schema-lock.json`.

Only listed files participate in the pack contract.

Git must preserve installed pack bytes. Initialization appends
`data/schema-packs/** -text`; newline conversion would invalidate locked hashes.
Existing `.gitignore` and `.gitattributes` bytes are preserved when rules are
appended. Updating toolkit code does not update these host rules until `init`
is run again.

## 7. Schema resolution

Use JSON Schema Draft 2020-12.

References resolve through the locally installed catalog. Normal validation
does not retrieve network resources.

The current implementation supports:

- absolute `$ref` targets;
- local JSON Pointer fragments;
- references to installed schema documents.

It deliberately does not support:

- nested `$id` declarations;
- `$dynamicRef`;
- `$dynamicAnchor`;
- arbitrary remote retrieval.

An absolute schema ID identifies a document. It is not permission to fetch it.

## 8. Declared graph references

Factum's annotation marks fields containing node references:

```json
{
  "$ref": "urn:factum:core:common:1#/$defs/id",
  "x-factum-target-kinds": ["artifact"]
}
```

This is a Factum extension annotation, not a standard JSON Schema keyword.

Factum uses it to:

1. Resolve bundle-local references.
2. Check that targets exist.
3. Check target kinds.
4. Populate the reference index.

The current annotation walker supports references through:

- direct properties;
- array items and prefix items;
- `allOf`;
- `$ref`.

Reference annotations beneath conditional/alternative branches or dynamic
property matching are rejected where unsupported.

Only JSON Schema subschema locations are inspected. Property names and
`examples`, `default`, `const`, and `enum` data are not schema keywords.
Annotations under `dependentSchemas`, `propertyNames`, `unevaluatedItems`,
and `contentSchema` are also rejected because the reference compiler does
not implement those traversals.

Do not assume that any JSON Schema construction accepted by the standard
validator is also supported by the reference compiler.

Keep reference fields structurally explicit.

## 9. Key, tags, or artifact?

| Information | Representation |
|---|---|
| Identity, provenance link, typed reusable field | Declared schema key |
| New reusable observation shape | Observation type and payload schema |
| New exact-string observable category | Observable definition |
| Reusable event profile | Event definition and payload schema |
| Graph relationship | Registered predicate and edge |
| Miscellaneous annotation | `tags` |
| Original source content | Artifact |

`tags` accepts arbitrary JSON metadata.

It is not an implicit graph-reference container. Strings such as `"@source"`
inside tags remain strings.

A raw observable string should not be rejected merely because it is a malformed
URL, IP address, or hash. Parsing and normalization belong in derived behavior,
not evidence destruction.

## 10. Pack installation and evolution

### Installation sequence

1. Read and hash the candidate's declared files.
2. Build the proposed combined catalog.
3. Check dependencies and uniqueness.
4. Resolve schemas locally.
5. Validate definitions and supported annotations.
6. Copy the immutable pack directory.
7. Activate it through an atomic lock-file replacement.
8. Rebuild the SQLite projection.

The lock is the activation point.

An unreferenced copied directory is inactive.

### Evolution policy

Installed pack versions are immutable.

The current implementation is additive:

- old packs remain installed;
- existing schema IDs cannot be redeclared;
- existing logical type names cannot be reassigned;
- new records can adopt new explicitly named types;
- old records retain their original contracts.

A newer pack version is not automatically a replacement.

A successor containing the same old definitions will fail uniqueness checks.
Use a delta pack containing only additions, with dependencies on the earlier
pack where necessary.

### Breaking example

```text
Old type:   research.webhook_capture
Old schema: urn:research:webhooks:capture:1

New type:   research.webhook_capture.v2
New schema: urn:research:webhooks:capture:2
```

The new type does not rewrite old observations.

### Not implemented

- automatic pack replacement;
- pack uninstall;
- core schema migration;
- implicit upcasting;
- executable corpus plugins.

## 11. Bundle compilation

Bundles are submission requests, not already-complete portable records.

Compilation:

1. Validate the bundle envelope.
2. Copy and hash submitted files.
3. Compute the request digest.
4. Check idempotency.
5. Allocate record IDs.
6. Apply explicit defaults.
7. Assign registered payload/value schemas.
8. Resolve declared local references.
9. Validate complete records.
10. Validate graph references and semantic constraints.
11. Write the durable pending file.
12. Rebuild the projection.

Some unreferenced artifact bytes may remain after failed validation.

This is acceptable and preferable to acknowledging a record before its bytes
have been preserved. Artifact garbage collection is not implemented here.

A failure after the pending file is durable may mean the submission was accepted
even if indexing failed. Recovery must inspect pending state and retry with the
same idempotency key.

An idempotent retry returns the original IDs; it does not guarantee that a
previously failed index rebuild has completed. Run `rebuild` if the index is
missing or stale. Receipt validation checks both named IDs and all returned
record IDs.

Atomic writers sync files, publication directories, and newly created parent
directory entries. The tests inject failures around these operations; they
do not simulate physical power loss or prove every filesystem's durability.

Failure recovery:

| Interruption | State and retry |
|---|---|
| Before pending publication | No accepted submission; retry the same request |
| After pending publication, before indexing | Accepted pending records survive; retry key and rebuild |
| After batch publication, before pending cleanup | Batch and pending coexist; export retry checks equality and removes only the exported pending file |
| Database replacement failure | Previous database remains; pending stays; retry rebuild |
| Pack copied, before lock activation | Pack is inactive; retry unchanged candidate |
| Lock activated, before rebuild | Pack is active; retry rebuild |
| Partial first initialization | Stop for inspection; do not delete managed paths automatically |

## 12. Idempotency and offline replicas

A key identifies a request within a corpus.

The request digest includes the submitted bundle and imported file hashes.

- Same key and same request: return the original result.
- Same key and different request: conflict.

Receipts travel with exported batches.

Offline sites do not have a global coordinator. If they independently accept
incompatible outcomes under the same key, merge validation reports a conflict.

Prefer actor/run-scoped keys.

File-based retries currently require the submitted files to remain available
to recompute their hashes.

## 13. Evidence and locators

Artifact identity is separate from acquisition metadata.

An artifact can identify:

- hashed preserved bytes;
- an external reference without preserved bytes.

Observation file bindings describe roles, filenames, and reported media types.

Locators can identify:

- whole artifacts;
- exact quotes;
- text or byte ranges;
- JSON Pointers;
- dataset rows;
- pages.

Text offsets count Unicode code points in a specific UTF-8 representation.
Range ends are exclusive.

General ingestion checks structure and references. It does not prove every
submitted quote or selector resolves correctly.

`get --context` checks supported text-position selectors against available
bytes.

Derived text or OCR must be represented as separate preserved artifacts, with
derivation provenance, rather than substituted for original bytes.

## 14. Search and interpretations

Search has separate concerns:

- exact raw-value lookup;
- registered derived-key lookup;
- bounded fuzzy candidate retrieval;
- source and sighting retrieval;
- graph traversal.

Fuzzy matching uses heuristic candidate generation. It is not exhaustive.

`not_found` is scoped to the query, indexed data, and matching policy.

Unknown search types and unsupported constraints fail. Exact/key retrieval
caps candidates at 5,000; fuzzy retrieval adds at most 2,000 FTS candidates
from at most 32 query trigrams. Result limits are 1–200. Graph traversal limits
depth to 0–10 and edges to 1–2,000, reporting omitted edges at either budget.

Similarity does not decide:

- originality;
- independent corroboration;
- event identity;
- updates;
- contradictions.

Agents record those interpretations through cited claims and assessments.

Retractions preserve records and are not automatically applied as a hidden
search filter.

## 15. Git coordination

Factum has a per-checkout process lock for its own commands.

That lock does not coordinate external agents running Git.

Use separate worktrees for concurrent workers, and serialize Git state changes
against Factum commands in each worktree.

Before synchronization:

```text
export
verify --blobs
review
agent-controlled Git operations
```

After synchronization:

```text
verify
rebuild
```

A clean textual merge does not prove semantic validity. Validate the merged
catalog, IDs, receipts, and graph references before treating the index as current.

Branches are not read-access security boundaries. Repository and artifact
publication policies remain the operator's responsibility.

## 16. Required test matrix

Use disposable repositories and small, explicit fixtures.

### Installation and paths

- Plain nested-clone installation.
- Explicit `--repo`.
- `FACTUM_REPO`.
- Invocation from the host root and skill directory.
- Refusal to initialize the toolkit itself.
- Existing unrelated `data/` content.
- Existing incompatible corpus.
- Missing SQLite capabilities.

### Schema packs

- Valid pack and exact dependency installation.
- Missing dependency.
- Missing file or invalid hash.
- Path traversal and symlink attempts.
- Duplicate schema ID.
- Duplicate type assignment.
- Unsupported schema dialect.
- Uninstalled `$ref` target.
- Local JSON Pointer resolution.
- Unknown reference target kind.
- Unsupported conditional reference annotations.
- Dry run leaves active lock unchanged.
- Interrupted installation before and after activation.
- Identical installation retry.
- Modified installed version rejection.

### Assignment and bundles

- Omitted schema assignment is filled correctly.
- Explicit matching assignment is accepted.
- Explicit conflicting assignment is rejected.
- New observation type works without a Python change.
- Custom annotated field resolves `@local-ref`.
- Unknown local reference fails.
- Wrong target kind fails.
- Literal `@text` inside tags and claim values remains unchanged.
- Unknown structural keys fail.
- Arbitrary valid JSON tags survive round trips.
- Mixed-case and malformed observable strings remain exact.

### Evidence storage

- Byte-exact Git-retained and local-only captures.
- Same bytes share physical CAS storage.
- Separate acquisitions remain separate records.
- Corrupt existing CAS file is detected.
- Reference-only artifacts do not claim preserved bytes.
- Missing local bytes are reported.
- Extraction preserves substrings and code-point offsets.
- Invalid UTF-8 extraction fails without invented replacement text.

### Persistence and recovery

- Invalid bundle creates no accepted record set.
- Crash before pending publication.
- Crash after pending publication but before projection.
- SQLite deletion followed by rebuild.
- Export retry after batch creation but before pending cleanup.
- Same key/same request.
- Same key/different request.
- Receipt restoration after rebuild.
- Corrupt manifest, count, fingerprint, or JSONL.
- Same immutable ID with different content.
- Failed rebuild leaves the prior database available.
- Disk-full and permission failures.

### Distributed and historical behavior

- Two sites write different batches offline and merge.
- Duplicate identical records project once.
- Conflicting receipts fail validation.
- Divergent lane edits remain explicit Git conflicts.
- Historical rebuild reads the selected commit's schemas and lock.
- Historical reads exclude current pending work.
- Branch changes cannot silently use a stale index.

### Search and graph

- Exact versus derived-key match reasons.
- Fuzzy candidate and result limits.
- Empty and invalid queries.
- Stale or missing index fails, not `not_found`.
- Search scope disclosure.
- Cyclic graph termination.
- High-degree graph budgets.
- Context verification against exact artifact bytes.

## 17. Pack acceptance procedure

Before approving a new pack:

1. Review its manifest, dependencies, definitions, and schemas.
2. Confirm that the proposed shape is reusable.
3. Confirm that fields holding evidence are not destructively constrained.
4. Confirm reference fields are annotated explicitly.
5. Include representative valid examples.
6. Include invalid examples for unknown keys, wrong references, and missing fields.
7. Test installation in a disposable host repository.
8. Submit complete bundles using local references.
9. Export, verify, remove only the test SQLite index, and rebuild.
10. Confirm the same evidence, schema assignments, references, and tags are retrieved.
11. Commit the pack, lock, and dependent records consistently.

A pack that validates JSON but loses provenance or changes raw evidence is not
acceptable.

## 18. Performance and release limits

The current implementation prioritizes simplicity:

- full portable validation;
- in-memory record loading;
- full SQLite rebuilds;
- bounded fuzzy search;
- no background processing.

Measure before claiming suitability for the complete production corpus.

Recommended benchmarks:

- record count and peak validation memory;
- add and rebuild duration;
- export and verification duration;
- artifact hashing throughput;
- exact/key/fuzzy query latency;
- fuzzy retrieval recall on a labeled fixture set;
- graph traversal behavior at high degree;
- Git file count and history growth.

Do not claim tests, recovery guarantees, or performance measurements that have
not actually been executed.

## 19. Running deployment checks

The test suite is ordinary pytest, split into six `tests/test_*.py` files.
All corpora and Git conflict fixtures are disposable and synthetic.

```bash
uv run --group dev pytest -q
uv run --no-project tools/smoke_test.py
```

The smoke test stages current source files, including relevant uncommitted
changes, and installs actual nested clones. It uses a local bare Git remote,
independent replicas, a pinned submodule, and clean packaged installations.
It leaves a JSON report and disposable workspace under `~/factum-validation/`.
`--workspace <new-directory>` selects another new location.

`FACTUM_TEST_PYTHON` selects the uv test interpreter (default `3.12`).
`--skip-packaging` is for focused reruns, not release acceptance.
Git fixture commits use the environment's existing identity; missing identity
is an environment blocker. The tooling never configures identities or publishes
to external remotes.

See [docs/VALIDATION.md](docs/VALIDATION.md) for executed results and
[docs/HANDOFF.md](docs/HANDOFF.md) for installation.