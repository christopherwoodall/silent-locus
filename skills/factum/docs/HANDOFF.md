# Factum deployment handoff

## Obtain the tested code

This handoff includes local, uncommitted changes based on
`08183d4da30958cc056fffe649fe80aaff7f4643`. The public clone URL alone does
not deliver these fixes.

The operator must either commit and publish the reviewed changes separately,
or transfer the prepared `factum-source.tar.gz` and its `SHA256SUMS` sidecar.
Check the checksum before extraction. The release sidecar records the tested
runtime digest and full source inventory. No project commit or external push
was performed for this task.

The archive excludes Git internals, environments, caches, test corpora, and
local evidence. It includes scripts, packaged seed schemas, documentation,
tests, and synthetic examples.

## Prerequisites

- Git, uv, and Python 3.11+.
- SQLite with FTS5 and the trigram tokenizer.
- A separate host Git repository.
- Permission to preserve/publish the selected evidence bytes.
- Network access or cached dependencies for uv.

Tests and smoke tooling also require an existing Git identity for disposable
fixture commits. They do not configure it.

## Install the skill

If the operator publishes the validated revision, clone that approved revision:

```bash
cd "$HOST"
git clone <approved-factum-repository> .agents/skills/factum
git -C .agents/skills/factum checkout <approved-revision>
```

For an archive transfer, extract it into a separate source directory and copy
the extracted `factum/` directory to `$HOST/.agents/skills/factum`. The archive
is a complete skill; it does not need a Python package installation or Git
internals. The validated principal test uses actual nested Git clones.

For a plain nested clone, append `/.agents/skills/factum/` once to the host's
local exclude file, preserving existing lines:

```bash
cd "$HOST"
EXCLUDE=$(git rev-parse --git-path info/exclude)
grep -qxF '/.agents/skills/factum/' "$EXCLUDE" ||
  printf '\n/.agents/skills/factum/\n' >> "$EXCLUDE"
```

Do not accidentally commit an unmanaged nested repository. The documented
pinned-submodule alternative is also tested; see [INSTALL.md](../INSTALL.md).

Resolve paths, then check and initialize:

```bash
HOST=$(cd "$HOST" && pwd)
SKILL="$HOST/.agents/skills/factum"
uv run "$SKILL/scripts/factum.py" --repo "$HOST" status
uv run "$SKILL/scripts/factum.py" --repo "$HOST" init
uv run "$SKILL/scripts/factum.py" --repo "$HOST" doctor
uv run "$SKILL/scripts/factum.py" --repo "$HOST" verify
```

Repeated `init` preserves corpus identity and installed packs. Format 1 requires
a separately reviewed migration, not a version-number edit.

## Host agent instructions

Read the host's existing `AGENTS.md` and any more-specific instructions.
Insert or update the marked integration block from
[INSTALL.md](../INSTALL.md#register-factum-in-the-host-repositorys-agent-instructions)
once. Preserve unrelated instructions and reconcile conflicts explicitly.

The block directs agents to read the installed `SKILL.md`, use explicit
`--repo`, preserve exact evidence, and export/verify around authorized Git
operations. `init` does not edit `AGENTS.md`. The smoke fixture demonstrates
this integration in a disposable host only.

## Complete synthetic walkthrough

The example is synthetic and contains no credential. Run it in a disposable
host first. Commands use the uv entry point, not Python internals.

Preview and activate the example schema pack:

```bash
uv run "$SKILL/scripts/factum.py" --repo "$HOST" \
  schema install "$SKILL/examples/pack/1.0.0"
uv run "$SKILL/scripts/factum.py" --repo "$HOST" \
  schema install "$SKILL/examples/pack/1.0.0" --approve
uv run "$SKILL/scripts/factum.py" --repo "$HOST" \
  schema assigned observation example.capture
```

Capture an already-collected file:

```bash
uv run "$SKILL/scripts/factum.py" --repo "$HOST" capture \
  --url 'https://Example.COM/CasePath?Token=AbC#MiXeD' \
  --file "$SKILL/examples/capture.txt" --storage git \
  --actor agent:synthetic --key example/web-capture
```

Submit the complete custom bundle. Its file path is relative to the current
directory, so run this command from the skill directory:

```bash
(
  cd "$SKILL"
  uv run scripts/factum.py --repo "$HOST" add --input examples/bundle.json
)
```

The returned `ids` map contains the observation, artifact, value, event, edge,
and claim IDs. Copy the observation ID from that JSON if you need `get`:

```bash
uv run "$SKILL/scripts/factum.py" --repo "$HOST" get <observation-id>
uv run "$SKILL/scripts/factum.py" --repo "$HOST" match \
  --value '  Example.COM/Case?Token=AbC#MiXeD  ' --type example.exact
uv run "$SKILL/scripts/factum.py" --repo "$HOST" export
uv run "$SKILL/scripts/factum.py" --repo "$HOST" verify --blobs
uv run "$SKILL/scripts/factum.py" --repo "$HOST" rebuild
```

Review and perform Git synchronization yourself, only as authorized. Include
the required packs, lock, corpus metadata, exported records, and selected
`data/blobs/` bytes. Never commit `data/.local/`.

At another checkout, install the same approved skill independently and run:

```bash
uv run "$SKILL/scripts/factum.py" --repo "$HOST" init
uv run "$SKILL/scripts/factum.py" --repo "$HOST" verify --blobs
uv run "$SKILL/scripts/factum.py" --repo "$HOST" rebuild
uv run "$SKILL/scripts/factum.py" --repo "$HOST" match \
  --value '  Example.COM/Case?Token=AbC#MiXeD  ' --type example.exact
```

No IDs, hashes, SQL, or portable ledger files need to be hand-written.
Installing new schemas is additive. Preview first; activate only when approved.
Breaking shapes require new schema IDs and logical type names.

## Recovery and boundaries

- Missing/stale SQLite: `rebuild`. Never delete pending work.
- Index failure after acceptance: retry the same unchanged request key to
  recover original IDs, then rebuild.
- Interrupted export: retry `export`; identical published batches are reused.
- Copied-but-unlocked pack: inactive; retry the same unchanged proposal.
- Activated pack with failed indexing: pack remains active; retry `rebuild`.
- Schema drift: restore approved exact bytes and lock; do not recompute hashes
  to conceal an unexplained change.
- Partial initialization: inspect managed paths before deciding recovery.
- Missing local-only bytes: disclose absence. Do not fetch a replacement and
  call it the original capture.
- Git changes: serialize them against Factum commands in each checkout.
- Historical view: put globals first, `--at <commit> rebuild`. It creates a
  separate database and excludes current pending work without checkout.
- General locators receive structural validation, not full selector/quote
  verification. `get --context` verifies supported text-position quotes.
- Fuzzy scores are retrieval signals. Retractions do not silently hide originals.
- Full rebuilds and in-memory validation are not benchmarked at research scale.

For repeatable acceptance, run `uv run --group dev pytest -q` and
`uv run --no-project tools/smoke_test.py` from the toolkit source directory.
See [VALIDATION.md](VALIDATION.md) for results and untested environments.
