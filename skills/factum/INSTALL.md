# Install and update Factum

This document is for agents or operators setting up Factum in a host repository.

It covers:

1. Installing the agent skill or Python CLI.
2. Initializing or checking a corpus.
3. Updating installed code.
4. Installing additive schema packs.
5. Safely handling schema changes.
6. Registering Factum in the host repository's agent instructions.

For everyday evidence work, read [SKILL.md](SKILL.md).

For pack design, architecture, and testing, read
[ARCHITECTURE.md](ARCHITECTURE.md).

## Scope and authorization

Factum stores data. It does not acquire sources or perform Git operations.

Do not interpret installation as permission to:

- start crawling;
- submit findings externally;
- publish evidence;
- change repository branch policy;
- migrate an existing corpus;
- replace installed schemas;
- delete pending work.

Follow the user's authorization and the host repository's rules.

## Requirements

- Git
- Python 3.11 or later
- Python's SQLite build with FTS5 and its trigram tokenizer
- A host Git repository
- uv for the documented installation and script workflows

The public script declares its Python dependencies through inline uv metadata.
A manually managed virtual environment is not required for that workflow.

uv may need network access to obtain Python or dependencies, depending on the
local environment. Use the environment's approved installation procedure.

## Installation modes

Factum supports two entry points.

### Agent skill installation

Clone Factum into the agent platform's skills directory.

This provides:

- `SKILL.md`;
- installation and architecture documentation;
- the uv script;
- implementation code;
- bundled seed schema packs.

Run:

```bash
uv run <skill-directory>/scripts/factum.py \
  --repo <host-repository> \
  <command>
```

Use this mode when installing Factum as an agent skill.

### Python CLI installation

Installing the Python distribution provides:

- the `factum` console command;
- implementation code;
- bundled seed schema packs.

Run:

```bash
factum --repo <host-repository> <command>
```

A Python package installation does not register `SKILL.md` with the agent
platform. It is a CLI installation, not automatic skill discovery.

Both entry points use the same implementation and corpus format.

Avoid accidentally running different toolkit versions against the same corpus.
If both modes are installed, choose one entry point for normal use and record
which installation is active.

## 1. Choose the host repository

The host repository is where evidence belongs.

```text
host-repository/
├── .agents/skills/factum/
└── data/
```

The installed Factum clone is not the corpus.

The skill examples below use `.agents/skills/factum/`. Use the skills directory
recognized by the agent platform if it differs.

Factum stores corpus data under the host repository's root `data/`, not inside
the installed skill directory.

## 2. Install Factum

### Option A: local nested skill clone

From the host repository root:

```bash
git clone https://github.com/christopherwoodall/factum.git \
  .agents/skills/factum
```

Keep this nested clone out of accidental host commits.

For a local-only installation, add this line to the host repository's local
Git exclude file:

```text
/.agents/skills/factum/
```

Locate that file from the host repository:

```bash
git rev-parse --git-path info/exclude
```

Append the line without overwriting existing contents. Adjust the path if the
skill is installed elsewhere.

Do not blindly stage the nested repository.

### Option B: shared, pinned skill submodule

Use this instead of the plain-clone command:

```bash
git submodule add https://github.com/christopherwoodall/factum.git \
  .agents/skills/factum
```

This lets the host repository track an approved Factum revision.

Other checkouts will need the submodule initialized through their approved Git
workflow.

Choose either the plain-clone or submodule approach. Do not create a nested
clone and accidentally stage it as an unmanaged embedded repository.

### Option C: Python console command

To install the CLI from an approved local Factum source directory:

```bash
uv tool install /absolute/path/to/factum
```

To install a prepared wheel:

```bash
uv tool install /absolute/path/to/factum_skill-0.2.0-py3-none-any.whl
```

Use the actual wheel filename produced for the approved release.

Make sure uv's tool executable directory is on PATH using the environment's
normal setup procedure.

Then:

```bash
factum --help
```

This option does not create an agent skill directory or install `SKILL.md`
into the agent host.

For an agent that needs skill discovery, use Option A or B. The console
installation is optional.

### Where seed assets live

In the source checkout, bundled packs live under:

```text
scripts/factum_lib/assets/packs/
```

They are included in the Python distribution and accessed as package resources.

Initialization does not require a source clone when using the console command.

Once initialized, the host corpus's installed packs are authoritative:

```text
data/schema-packs/
data/schema-lock.json
```

## 3. Check whether a corpus already exists

From the host repository root, using the skill:

```bash
uv run .agents/skills/factum/scripts/factum.py status
```

For explicit path resolution:

```bash
uv run /path/to/factum/scripts/factum.py \
  --repo /path/to/host-repository \
  status
```

Using the installed CLI:

```bash
factum --repo /path/to/host-repository status
```

`FACTUM_REPO` can also identify the host repository.

Place global options such as `--repo` and `--at` before the command.

### Repository detection

Without `--repo` or `FACTUM_REPO`:

- The console command uses the current Git repository.
- The clone-based script uses the current Git repository.
- If the script is invoked inside its own nested skill checkout, it attempts
  to find the containing host repository.

The clone-based script refuses to initialize its own toolkit checkout as the
corpus.

When running from an unrelated directory or a standalone toolkit checkout,
pass `--repo` explicitly.

## 4. Initialize or rebuild

The remaining examples use the clone-based skill entry point.

For the Python installation, replace:

```text
uv run .agents/skills/factum/scripts/factum.py
```

with:

```text
factum
```

Use `--repo` explicitly when not running from the host root.

### New corpus

When authorized:

```bash
uv run .agents/skills/factum/scripts/factum.py init
```

Initialization:

- creates the corpus identity;
- loads bundled seed packs through Python package resources;
- copies those packs into the host repository;
- verifies the copied pack inventory;
- writes the schema lock;
- creates local site metadata;
- adds scoped ignore and artifact-preservation attributes;
- builds SQLite;
- leaves unrelated files and legacy directories alone.

It does not:

- commit or push;
- fetch evidence;
- configure remotes;
- install hooks;
- import legacy datasets;
- edit the host `AGENTS.md`.

### Existing compatible corpus

Initialization does not replace its schemas with the latest bundled seeds.

When preparing a newly cloned corpus on a new machine, `init` can create missing
local site metadata and rebuild the existing compatible corpus:

```bash
uv run .agents/skills/factum/scripts/factum.py init
```

For normal verification and index refresh:

```bash
uv run .agents/skills/factum/scripts/factum.py verify
uv run .agents/skills/factum/scripts/factum.py rebuild
uv run .agents/skills/factum/scripts/factum.py doctor
```

Existing pending submissions are included during the current-state rebuild.

### Existing incompatible corpus

The current implementation uses portable format `2`.

Format `1` is not automatically migrated. Stop and report the incompatibility.

Do not edit `corpus.json` merely to change its version number.

A reviewed migration is separate development work.

### Partial initialization

If managed schema or record paths exist without `corpus.json`, initialization
stops rather than guessing whether it should overwrite them.

Inspect the partial state before recovery. Do not delete existing evidence or
pending submissions to make initialization succeed.

## 5. Review initial setup

Normally, initial host changes include:

```text
.gitignore
.gitattributes
data/corpus.json
data/schema-lock.json
data/schema-packs/
```

Do not commit `data/.local/`.

Inspect `doctor` output:

- repository path;
- format and toolkit versions;
- record and lane counts;
- pending count;
- index staleness;
- database location.

SQLite capability is exercised during rebuild. If FTS5 or trigram support is
missing, use a compatible Python/SQLite distribution.

Initialization and rebuild must succeed before treating the installation as
ready.

Installed pack files are hash-pinned bytes. Initialization appends
`data/schema-packs/** -text` to prevent Git newline normalization. Existing
host Git configuration-file content is preserved.

## 6. Onboard the working agent

Read [SKILL.md](SKILL.md).

The agent should then:

1. Run `status`.
2. Rebuild if stale.
3. Select or create a lane.
4. Inspect the applicable schema assignment.
5. Collect evidence using its own tools.
6. Submit files or bundles.
7. Search the actual Factum corpus before making novelty claims.
8. Keep interpretations separate from observations.
9. Export and verify before Git synchronization.
10. Register Factum in the host instructions using the section below.

Raw files do not need to be opened simply because Factum has been installed.

## Updating installed code

Toolkit code and corpus schemas have separate lifecycles.

### Before updating

- Identify the active installation mode and revision or package version.
- Check for local modifications to an installed source clone.
- Check corpus status.
- Export pending records when practical.
- Preserve pending work and local-only evidence.
- Review release notes or the proposed code diff.

Do not overwrite a modified skill checkout.

### Apply the approved update

For a plain clone, update the installed Factum Git repository using the
approved revision and normal Git workflow.

For a submodule, update its pinned revision through the host repository's
approved workflow.

For a Python CLI installation, reinstall the approved source or wheel using
the environment's tool-management procedure. For example:

```bash
uv tool install --force /absolute/path/to/approved-factum.whl
```

Use the actual approved artifact path.

There is no `factum update` command.

### After updating

```bash
uv run .agents/skills/factum/scripts/factum.py verify
uv run .agents/skills/factum/scripts/factum.py rebuild
uv run .agents/skills/factum/scripts/factum.py doctor
```

For a console installation:

```bash
factum --repo /path/to/host-repository verify
factum --repo /path/to/host-repository rebuild
factum --repo /path/to/host-repository doctor
```

A toolkit update must not silently replace:

```text
data/schema-packs/
data/schema-lock.json
```

Stop on incompatibility instead of copying new bundled assets over old schemas.

## Installing a new schema pack

### What an agent may extend

Schema packs may add:

- observable types;
- observation payload schemas;
- event payload schemas;
- predicates.

They cannot add arbitrary Python execution, storage providers, or new core
record kinds.

Use `tags` for one-off metadata. Do not create a schema pack for every temporary
annotation.

### Step 1: inspect existing assignments

```bash
uv run .agents/skills/factum/scripts/factum.py schema list
```

For a specific type:

```bash
uv run .agents/skills/factum/scripts/factum.py \
  schema assigned observation web.capture
```

Inspect the returned schema ID:

```bash
uv run .agents/skills/factum/scripts/factum.py \
  schema describe urn:factum:web:web-capture:1
```

Prefer an existing suitable type over a duplicate.

### Step 2: obtain or author a candidate pack

Develop the candidate outside installed pack directories:

```text
schema-proposals/
└── research-webhooks/
    └── 1.0.0/
        ├── pack.json
        ├── definitions.json
        └── schemas/
            └── webhook-capture.schema.json
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for manifest and definition contracts.

The agent handles obtaining the pack. Factum does not download packs.

Review unfamiliar packs before activation. Data-only packs still influence
validation, matching, and reference interpretation.

Do not put proposal changes directly into `data/schema-packs/`.

### Step 3: preview installation

```bash
uv run .agents/skills/factum/scripts/factum.py \
  schema install ./schema-proposals/research-webhooks/1.0.0
```

Without `--approve`, the command validates the proposed combined catalog but
does not activate it.

It checks:

- pack structure and file inventory;
- exact dependency versions;
- JSON Schema validity;
- local reference resolution;
- duplicate schema IDs;
- duplicate type assignments;
- supported Factum reference annotations.

This is not a substitute for testing real example bundles.

### Step 4: test in a disposable repository

Before installing a nontrivial pack into an important corpus:

1. Initialize a disposable host Git repository.
2. Initialize its Factum corpus.
3. Install required dependency packs.
4. Install the candidate.
5. Submit positive example bundles.
6. Confirm malformed bundles fail.
7. Export, verify, and rebuild.
8. Retrieve records and check schema assignments and references.

Use the installed script with explicit `--repo`, or the console command.

Do not initialize the Factum source checkout as the test corpus.

Never use the production corpus as the only pack test environment.

### Step 5: activate when authorized

```bash
uv run .agents/skills/factum/scripts/factum.py \
  schema install ./schema-proposals/research-webhooks/1.0.0 --approve
```

Activation copies the pack, updates the lock, and rebuilds the index.

### Step 6: verify and review

```bash
uv run .agents/skills/factum/scripts/factum.py verify

uv run .agents/skills/factum/scripts/factum.py \
  schema assigned observation research.webhook_capture
```

Review and commit together:

```text
data/schema-packs/<pack-name>/<version>/
data/schema-lock.json
```

Commit dependent records with their required packs. Other sites need both.

## Updating schemas and packs

### Uninstalled draft

Edit freely while it remains a proposal. Revalidate and retest.

### Installed pack version

Do not edit it in place.

The lock pins its file contents. Modification produces schema drift.

### Additive extension

Create a pack containing only new schema IDs and new type names.

The current installer does not replace installed packs. Multiple versions can
remain installed, but duplicate definitions are rejected even when their
contents are identical.

Therefore, copying an entire installed pack, changing its version, and
reinstalling it usually fails because it repeats existing schema IDs and type
names.

A supported pattern is a new extension pack:

```text
research-webhooks-extra/1.0.0/
```

It can declare this manifest dependency:

```json
{
  "requires": {
    "research-webhooks": "1.0.0"
  }
}
```

This is a manifest fragment, not a complete manifest.

The extension must declare only its additions.

### Breaking change to a type

Use a new schema ID and logical type name, for example:

```text
Schema ID: urn:research:webhooks:capture:2
Type name: research.webhook_capture.v2
```

New records use the new type. Old records retain their original assignment.

There is no in-place type reassignment command.

### Core schema or record migration

Stop and request explicit development authorization.

Do not:

- edit locked core schemas;
- rewrite old records to make them validate;
- recompute hashes to conceal changed history;
- remove old packs still needed by records;
- relabel a corpus format without migrating its actual records.

## Register Factum in the host repository's agent instructions

After successful setup, make Factum discoverable to future agents by adding a
short integration block to the host repository's root `AGENTS.md`.

This is an agent-managed documentation step. The current `init` command does
not modify `AGENTS.md`.

### Scope

Update the host repository's instructions, not the development `AGENTS.md`
inside the installed Factum clone.

Use the instruction filename recognized by the host platform. Prefer
`AGENTS.md` when that is the repository convention.

If the repository uses `AGENT.md` instead, confirm that the platform reads it.
Do not create competing instruction files without a reason.

### Procedure

1. Read the existing host instructions.
2. Check for an existing `FACTUM INTEGRATION` marker block.
3. Add the block once, or update that existing block.
4. Substitute the actual repository-relative skill path.
5. Preserve all unrelated instructions.
6. Identify conflicting storage instructions.
7. Update those conflicts when authorized, or report them before using Factum
   as the required storage path.
8. Review the diff.
9. Do not commit or push automatically.

A bottom-of-file block does not safely resolve contradictory earlier
instructions.

For example, if an earlier section directs agents to hand-write every new
observation into legacy `events.jsonl`, clarify that:

- historical files retain their existing schemas;
- new structured records go through Factum;
- compatibility exports require an explicit adapter;
- agents must not manually maintain two authoritative copies.

Preserve existing acquisition, publication, retention, and branch policies.

### Suggested integration block

Adjust `.agents/skills/factum/` if the skill is installed elsewhere.

```markdown
<!-- BEGIN FACTUM INTEGRATION -->
## Factum evidence storage

Use Factum for new structured evidence, provenance, claims, and relationships.

- Read `.agents/skills/factum/SKILL.md` before evidence-storage work.
- Follow `.agents/skills/factum/INSTALL.md` for setup and schema-pack changes.
- The host repository owns the corpus under `data/`.
- Run:
  `uv run .agents/skills/factum/scripts/factum.py --repo <host-repository> <command>`

Start with `status`. Use Factum scripts rather than editing managed JSONL,
manifests, SQLite, or installed schema packs directly.

Preserve exact evidence. Use `tags` for miscellaneous metadata. Install new
schema packs only through the documented, authorized workflow.

Export and verify before Git synchronization. Verify and rebuild after corpus
changes from Git. Never discard pending submissions.

Existing evidence and reports remain in place. Factum does not automatically
import or search legacy files. A Factum no-match result is not global novelty.

Repository rules for acquisition, review, retention, publication, and Git
operations remain authoritative.
<!-- END FACTUM INTEGRATION -->
```

For a CLI-only installation, do not insert nonexistent skill paths. Document
the actual `factum --repo ...` command and an accessible, approved copy of the
operating instructions instead.

A CLI-only installation still does not register an agent skill automatically.

### Existing or nested instructions

Check whether more-specific agent instructions apply in the directories where
the agent will work.

Do not silently overwrite those files. Report or reconcile conflicting storage
guidance when authorized.

### Completion report

Report:

- installation mode;
- installed revision or package version;
- host repository and corpus location;
- which host instruction file was updated;
- the installed skill path or CLI entry point;
- whether an existing integration block was updated or a new one was added;
- any conflicting instructions that remain;
- whether legacy material remains outside Factum's indexed scope.

## Recovery

### `INDEX_STALE` or `INDEX_MISSING`

Run `rebuild`.

Do not delete pending submissions.

### Schema drift

Restore the intended pack bytes and corresponding lock from an approved Git
state.

Do not regenerate hashes just to accept an unexplained change.

If an earlier installation used `data/schema-packs/** text eol=lf`, run `init`
on a currently valid corpus to append the preservation rule. If normalization
has already changed pack bytes, first restore the exact locked bytes from an
approved copy. Do not silently rewrite the lock to accept drift.

### Interrupted pack installation

The lock is the activation point.

A copied but unlocked pack directory is inactive. Retry installation from the
same unchanged candidate.

If the directory differs, stop and inspect it.

### Pack activated but rebuild failed

Inspect the error and retry `rebuild` after correcting the underlying problem.

Do not assume that an error means the pack was not activated.

### Partial initial setup

Initialization can fail after some managed files have been created.

If `corpus.json` is absent but managed pack or record paths exist, the next
initialization stops for inspection.

Do not remove those paths automatically. Determine whether they are failed
initialization output or pre-existing data before recovery.

### Missing bundled schema packs

A correctly built distribution contains its seed packs.

If initialization reports missing bundled resources:

1. Confirm which script or console installation is being executed.
2. Confirm that the installation is the intended release.
3. Reinstall a corrected, tested source checkout or distribution.
4. Do not work around the defect by copying unknown schemas into the corpus.

For developers, run the packaging acceptance checks below.

### Missing artifact bytes

A metadata-only clone may not contain another site's local-only bytes.

Report the limitation. Do not silently fetch a live replacement and present it
as the original capture.

### Removing or reinstalling Factum

Preserve the host `data/` directory.

In particular, preserve pending submissions and local-only bytes. They may not
exist in Git.

SQLite can be rebuilt. Local-only evidence and pending records cannot
necessarily be recovered from the repository.

## Packaging acceptance checks for maintainers

This section applies to agents preparing a release, not ordinary research
agents installing an approved version.

Do not validate packaging with an editable installation alone.

Run the automated acceptance workflow from the toolkit checkout:

```bash
uv run --group dev pytest -q
uv run --no-project tools/smoke_test.py
```

It snapshots current source, installs real nested clones, tests a pinned
submodule, builds wheel/sdist artifacts, installs a rebuilt wheel into a clean
environment, and exercises `uv tool install` in isolated tool directories.
All Git synchronization stays inside its disposable local workspace.
The environment must already have a configured Git identity for fixture
commits. The test tooling does not change identity configuration.

See [docs/HANDOFF.md](docs/HANDOFF.md) for a complete synthetic example and
[docs/VALIDATION.md](docs/VALIDATION.md) for executed results.

Before declaring a release ready:

1. Build a wheel and source distribution.
2. Inspect the wheel for every manifest-declared seed file.
3. Build a second wheel from the source distribution.
4. Install that wheel into a clean tool or virtual environment.
5. Run `factum --repo <temporary-host> init` from outside the source checkout.
6. Confirm copied packs, schema assignments, and the lock validate.
7. Run capture, export, verification, and rebuild through the console command.
8. Run the equivalent workflow through a nested clone's uv script.
9. Confirm both entry points initialize equivalent schema catalogs.
10. Record the exact tested code revision and distribution artifact.

The console-command test must not depend on access to the development
checkout's assets.

The source layout for bundled resources is:

```text
scripts/
└── factum_lib/
    ├── resources.py
    └── assets/
        └── packs/
```

Changing the seed-pack layout requires updating package-data configuration and
packaging tests together.

Do not claim that wheel installation or initialization passed unless the
commands were actually executed.