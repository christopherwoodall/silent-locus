# Developing Factum

This file is for agents changing the Factum project itself.

For agents using Factum to conduct research, follow [SKILL.md](SKILL.md).
For installation, follow [INSTALL.md](INSTALL.md).
For technical contracts and test requirements, read
[ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Product boundary

Factum is a repository skill and local script toolkit.

It stores and indexes submitted evidence. It does not acquire sources or
manage agents.

Do not add the following without an explicit request:

- crawling or browser automation;
- source-fetching orchestration;
- REST or MCP services;
- automatic Git operations;
- background daemons;
- arbitrary Python execution from schema packs;
- a general plugin framework;
- GUI code.

## Current architecture

- Root `SKILL.md` makes the cloned project installable as a skill.
- `scripts/factum.py` is the uv-compatible public entry point.
- `scripts/factum_lib/` contains implementation.
- `scripts/factum_lib/assets/packs/` contains packaged seed schema packs.
- The host repository owns `data/`.
- Installed corpus packs and `schema-lock.json` govern validation.
- SQLite is a rebuildable projection.
- Pending files contain durable accepted-but-unexported records.
- Exported JSONL batches and manifests synchronize through Git.
- Lane documents are editable working material.

Keep toolkit paths separate from host-repository paths.

## Non-negotiable invariants

### Evidence

- Preserve exact strings and file bytes.
- Never normalize or redact raw evidence in place.
- Derived match keys are not evidence identity.
- Preserve distinct acquisitions and sightings.
- Never execute captured payloads.

### Records

- Every record has `tags`.
- Fingerprints cover the complete envelope except the fingerprint field.
- Same immutable ID with different content is an error.
- Retractions preserve their targets.
- Claims require assertion basis and citations.

### Schemas

- JSON files, not Python dictionaries, define portable shapes.
- Installed pack versions are immutable.
- Validation uses the corpus's locked packs.
- Normal validation never fetches schemas from the network.
- Type assignments are explicit and preserved on records.
- Arbitrary values and tags are not implicitly resolved as references.
- New types can be declarative; new core record kinds require development.
- Schema packs cannot install executable code.

### Persistence

- Accepted pending files must be durable before acknowledgement.
- Rebuild must include or explicitly protect pending work.
- Export must be retryable after interruption.
- The current portable tree must suffice for rebuild.
- Historical reads must use the selected commit's pack lock and records.
- SQLite replacement occurs only after successful projection checks.

### Search

- Failures never become `not_found`.
- Search scope and state identity are reported.
- Fuzzy scores are retrieval signals, not semantic classifications.
- Unknown constraints must not be silently ignored.
- Graph traversal has cycle prevention and explicit budgets.

## Development workflow

1. Inspect the affected implementation and contracts.
2. State whether the change affects:
   - portable format;
   - schema packs;
   - SQLite projection;
   - CLI behavior;
   - skill documentation.
3. Implement the smallest coherent change.
4. Add positive, negative, and recovery tests.
5. Update all affected documentation.
6. Report actual test results and untested assumptions.

Do not claim a command or test was executed unless it was.

Respect user instructions prohibiting execution.

Use conventional `tests/test_*.py` files and the single
`tools/smoke_test.py` entry point. Keep test helpers small; do not add a custom
test framework. Run `uv run --group dev pytest -q`, then
`uv run --no-project tools/smoke_test.py` for release acceptance.

The smoke test must snapshot current files, including relevant uncommitted
changes, rather than clone a stale project commit. Keep environments and
workspaces on Linux paths when developing through WSL.

## Schema-pack work

Before adding a pack:

- check whether an installed type already covers the need;
- distinguish reusable structure from miscellaneous `tags`;
- preserve raw observable strings even when malformed;
- assign unique schema IDs and logical type names;
- declare exact dependencies;
- keep examples with the proposed change;
- test bundle-local references in custom fields.

The current installer rejects duplicate schema IDs and type names across
installed packs. New pack versions coexist; they do not replace older ones.

Do not add migration behavior implicitly while fixing pack installation.

For breaking changes, specify the old and new identities and how both remain
available to rebuild historical records.

## Code practices

- Keep the public script runnable with `uv run`.
- Keep CLI parsing separate from validation and persistence.
- Use parameterized SQL.
- Treat schema packs, bundles, and captured files as untrusted inputs.
- Validate paths and reject traversal or unintended symlink escapes.
- Do not overwrite unrelated files or existing user documents.
- Do not shell-interpolate record values.
- Keep generated output machine-readable.
- Do not leak raw sensitive evidence through unnecessary diagnostics.
- Keep validation errors to schema paths and failed rules, not evidence values.
- Use process locks for coordinated local toolkit writes.
- Do not assume that toolkit locks coordinate external Git operations.

## Required tests

The detailed matrix is in docs/ARCHITECTURE.md.

At minimum, changes should preserve:

1. Nested-skill installation and explicit host path resolution.
2. Schema-pack hashing, dependency checks, and local `$ref` resolution.
3. Additive type assignment without Python edits.
4. Rejection of duplicate IDs, unknown types, and incompatible assignments.
5. Exact evidence preservation.
6. Bundle-local reference resolution without modifying tags or values.
7. Atomic logical bundle acceptance.
8. Idempotency across export and rebuild.
9. Pending recovery after index loss.
10. Two-site batch merging and conflict detection.
11. Historical rebuild without checkout.
12. Bounded search and graph operations.

Tests must use disposable repositories. Do not run development tests against
a real research corpus.

## Known implementation limits

The current implementation:

- loads the portable record set into memory;
- performs full SQLite rebuilds;
- uses a generic local record projection with supporting indexes;
- supports a constrained schema-reference annotation profile;
- does not implement pack replacement or uninstall;
- does not migrate portable format 1;
- does not prove source authenticity with content hashes;
- does not automatically resolve claim disagreements.

Document changes to these limits rather than silently promising stronger
guarantees.

## Documentation ownership

- README.md: overview and normal user workflow.
- INSTALL.md: setup, upgrades, and schema-pack installation.
- SKILL.md: concise operating rules for research agents.
- AGENTS.md: development rules.
- docs/ARCHITECTURE.md: technical contracts, tests, and limitations.

Avoid copying extensive implementation detail into every document.