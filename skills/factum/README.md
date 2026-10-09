# Factum

**Schema-driven evidence storage for research agents, inside the repository they already use.**

Factum is a repository skill and a small Python toolkit. Agents collect and
review information. Factum stores their submitted evidence, validates its
shape, connects its provenance, indexes it in SQLite, and exports portable
JSONL records for Git synchronization.

Factum is not a crawler, agent runtime, or backend service.

## Start here

- **Installing or upgrading:** [INSTALL.md](INSTALL.md)
- **Using Factum as an agent:** [SKILL.md](SKILL.md)
- **Developing Factum:** [AGENTS.md](AGENTS.md)
- **Data contracts, schema packs, and testing:** [ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Quick installation

From the root of the repository that will hold the evidence:

```bash
git clone https://github.com/christopherwoodall/factum.git \
  .agents/skills/factum

uv run .agents/skills/factum/scripts/factum.py init

uv run .agents/skills/factum/scripts/factum.py doctor
```

Use your agent platform's skills directory if it differs.

A plain clone creates a nested Git repository. Before staging host-repository
changes, choose whether the skill should remain a local installation or be
tracked as a submodule. See [INSTALL.md](INSTALL.md).

## Repository layout

```text
your-repository/
├── .agents/
│   └── skills/
│       └── factum/
│           ├── SKILL.md
│           ├── INSTALL.md
│           ├── docs/ARCHITECTURE.md
│           ├── scripts/
│           └── scripts/factum_lib/assets/packs/
│
└── data/
    ├── corpus.json
    ├── schema-lock.json
    ├── schema-packs/
    ├── records/
    ├── lanes/
    ├── blobs/
    └── .local/
```

The installed skill holds code and seed packs.

The host repository owns the corpus:

- `data/schema-packs/`: installed, pinned schema packs
- `data/records/`: exported immutable JSONL batches
- `data/lanes/`: editable work contexts and Markdown documents
- `data/blobs/`: explicitly Git-retained evidence bytes
- `data/.local/`: SQLite, pending submissions, and local-only bytes

`data/.local/` is ignored by Git.

**Not everything under `.local/` is disposable.** SQLite is rebuildable.
Unexported pending records and local-only evidence may be the only copies.

## The workflow

```text
Agent acquires and reviews information
                 |
                 v
       capture / add / extract / note
                 |
                 +--> preserved bytes or external references
                 +--> durable pending records
                 +--> SQLite index
                 |
                 v
               export
                 |
                 v
        sealed portable JSONL batches
                 |
                 v
      agent reviews and performs Git operations
                 |
                 v
          verify + rebuild at another checkout
```

Factum does not fetch URLs, query external trackers, commit, push, pull,
merge, or choose branch policy.

## Evidence remains unchanged

Factum preserves exact submitted strings and file bytes.

- `Example.COM` remains `Example.COM`.
- Malformed URLs can still be evidence.
- A copied artifact is not reformatted or redacted.
- Sensitivity can be annotated in `tags`.
- Derived matching keys never replace raw values.

An exact source file should be stored as an artifact when its byte-level
serialization matters. Parsing JSON and storing its fields does not preserve
the original file's whitespace or key order.

## Capture already-collected evidence

First, acquire the data with your own tools.

Then record the saved file:

```bash
uv run .agents/skills/factum/scripts/factum.py \
  capture \
  --url 'https://Example.COM/report?Token=AbC' \
  --file ./captures/report.html \
  --storage git \
  --actor agent:researcher \
  --key mission-17/capture-1
```

Factum does not fetch that URL.

Use `--observed-at` when the actual acquisition time is known. Otherwise
Factum records its receive time with an explicit time basis.

### Storage choices

| Choice | Meaning |
|---|---|
| `--storage git` | Preserve submitted bytes under `data/blobs/` |
| `--storage local` | Preserve submitted bytes under `data/.local/blobs/` |
| Reference artifact | Store a locator and optional revision without claiming preservation |

Example dataset reference:

```bash
uv run .agents/skills/factum/scripts/factum.py \
  capture \
  --dataset 'https://huggingface.co/datasets/example/corpus' \
  --revision '<pinned-revision>' \
  --coverage metadata_only \
  --actor agent:researcher \
  --key mission-17/dataset-reference-1
```

A reference is not proof that the dataset bytes remain available.

## Search

```bash
uv run .agents/skills/factum/scripts/factum.py \
  match --value 'Example.COM' --type domain
```

Derived-key matching:

```bash
uv run .agents/skills/factum/scripts/factum.py \
  match --value 'Example.COM' --type domain --mode key
```

Fuzzy retrieval:

```bash
uv run .agents/skills/factum/scripts/factum.py \
  match --text 'example infrastructure' --mode fuzzy
```

Results are:

- `found`, with a list of matches
- `not_found`, with the searched scope
- `ok: false`, when the operation fails

A failed search is not `not_found`.

A no-match result means no match under the stated query, policy, and indexed
scope. It does not establish global novelty or originality.

Fuzzy results are candidates, not identity decisions.

## Record shapes

| Kind | Purpose |
|---|---|
| `source` | Origin or source locator |
| `artifact` | Preserved bytes or an external reference |
| `observation` | What was encountered or submitted |
| `observable` | Exact typed value |
| `sighting` | Where a value appeared |
| `event` | Proposed event anchor |
| `claim` | Assertion with basis and citations |
| `edge` | Registered relationship |
| `assessment` | Scoped comparison or interpretation |
| `run` | Collection, extraction, or analytical context |
| `retraction` | Withdrawal without deleting the original record |

Every record has a `tags` object for miscellaneous JSON metadata.

Lanes are editable contexts with their own `tags`, stable IDs, and ordinary
Markdown documents.

## Structured submissions

Use bundles for related records:

```json
{
  "bundle": 2,
  "idempotency_key": "mission-17/value-1",
  "actor": "agent:researcher",
  "tags": {},
  "records": [
    {
      "ref": "domain",
      "kind": "observable",
      "body": {
        "type": "domain",
        "value": "Example.COM"
      },
      "tags": {
        "review_status": "unreviewed"
      }
    }
  ]
}
```

```bash
uv run .agents/skills/factum/scripts/factum.py \
  add --input bundle.json
```

The script assigns record IDs, fingerprints, acceptance timestamps, and
registered schema assignments.

A standalone observable records a submitted value. Use an observation and
sighting when you need to record exactly where that value appeared.

Local bundle references use `@name` only in declared reference fields.
Factum does not rewrite matching strings inside evidence values or `tags`.

## Schema packs

Schemas are individual JSON files grouped into versioned packs.

A pack can define:

- observation payload schemas
- observable types
- event payload schemas
- predicates and endpoint constraints

Inspect the installed definitions:

```bash
uv run .agents/skills/factum/scripts/factum.py schema list

uv run .agents/skills/factum/scripts/factum.py \
  schema assigned observation web.capture

uv run .agents/skills/factum/scripts/factum.py \
  schema describe urn:factum:web:web-capture:1
```

Preview a local pack installation:

```bash
uv run .agents/skills/factum/scripts/factum.py \
  schema install ./schema-proposals/research-webhooks/1.0.0
```

Install when authorized:

```bash
uv run .agents/skills/factum/scripts/factum.py \
  schema install ./schema-proposals/research-webhooks/1.0.0 --approve
```

Updating the skill does not update installed corpus schemas.

The current installer is additive. It rejects replacement schema IDs and
type assignments. See [INSTALL.md](INSTALL.md) before updating a pack.

## Lanes and writeups

```bash
uv run .agents/skills/factum/scripts/factum.py \
  lane new "Infrastructure follow-up"
```

Factum creates a lane document and initial Markdown files. Agents can maintain
README, provenance notes, findings, methodology, and other writeups normally.

Lane membership is recorded through `in_lane` edges rather than a shared
mutable membership list.

## Git synchronization

Before Git operations that publish or change the corpus:

```bash
uv run .agents/skills/factum/scripts/factum.py export
uv run .agents/skills/factum/scripts/factum.py verify --blobs
```

Review the results and intended files. Commit and synchronize them yourself.

After a pull, merge, or checkout:

```bash
uv run .agents/skills/factum/scripts/factum.py verify
uv run .agents/skills/factum/scripts/factum.py rebuild
```

Do not run Git changes concurrently with Factum commands in the same worktree.
Use separate worktrees for concurrent workers.

`verify --blobs` reports missing bytes separately. Missing local-only artifacts
may be expected at another site; they must not be mistaken for verified
preservation at that site.

## Historical views

Build a separate index from a commit without checking it out:

```bash
uv run .agents/skills/factum/scripts/factum.py \
  --at <commit> rebuild
```

Search it:

```bash
uv run .agents/skills/factum/scripts/factum.py \
  --at <commit> match --value 'Example.COM' --type domain
```

Historical views use that commit's packs, lock, records, and lanes. They exclude
current pending submissions.

## Current boundaries

- Portable corpus format: `2`
- No automatic migration from format `1`
- Full corpus validation and SQLite rebuilds
- Bounded, heuristic fuzzy retrieval
- UTF-8 regex extraction
- No arbitrary code execution from schema packs
- No automatic resolution of factual disagreements
- No automatic Git operations or source acquisition

The synthetic external-host workflow is validated, including packaged CLI
installation and two-site Git synchronization. See
[validation results](docs/VALIDATION.md) and the
[installation handoff](docs/HANDOFF.md) for the exact tested version.

Run the reproducible checks from this toolkit checkout:

```bash
uv run --group dev pytest -q
uv run --no-project tools/smoke_test.py
```

The smoke test uses disposable hosts and a local bare remote, never a real
corpus. Representative-scale benchmarking remains necessary before
high-volume use.