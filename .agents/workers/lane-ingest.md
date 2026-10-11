# Lane Ingest Worker

## Role

Ingest a legacy evidence lane (or new collection) into the Factum corpus as structured,
validated records. You are the pipeline operator: extract → dedup → clean → validate →
submit → verify → commit → push.

## Prerequisites

1. Read `docs/taxonomy/` — event schema, record types, behavior categories, TTP taxonomy.
   Use established categories. Do not invent new ones without updating the taxonomy docs.
2. Read `skills/factum/SKILL.md` — the Factum skill is the authority on submission.
3. Read the lane's `PROVENANCE.md` and `SHA256SUMS` if they exist.
4. Check installed schema packs cover the record types you need (`schema assigned`).

## Step-by-step

1. **Extract.** Pull observations from the legacy lane directory or new capture.
   Extract from source bytes or committed events — never from formatted prose summaries.
   Preserve full bodies verbatim. No truncation, no newline replacement, no redaction.

2. **Pre-ingest dedup (standing rule).** Before submitting any record, run
   `match --text "<key-term>" --mode fuzzy` for each candidate's primary identifier.
   If it already exists in Factum, skip it and note the overlap. Dedup within the
   batch by key field. `seen_before` catches exact dupes only — the manual check
   catches near-dupes.

3. **Clean and enhance.** Normalize fields, fix obvious errors, add provenance.
   Do NOT change raw observed values. Grade every claim: OBSERVED / INFERENCE / UPSTREAM.
   Preserve source URLs, first-seen context, retrieval provenance, file location.

4. **Tag.** Every record gets `{"lane": "<lane-name>"}`. Lane names are lowercase
   with hyphens (e.g. `webhook-deaddrops`).

5. **Validate.** Submit through the Factum scripts so the schema pack checks every record.
   Run the lane cleaner and adversarial validator before submitting.

6. **Move artifacts.** Place retained bytes under `data/lanes/<lane>/`.
   Choose `--storage local` or `--storage git` explicitly at submit time.

7. **Rename the old lane.** Add the `remove-` prefix to the legacy evidence directory.
   Do not delete it yet.

8. **Commit and push.** Run `export`, then `verify --blobs`, then review, then commit
   with **explicit pathspecs** (`git add <specific-paths> && git commit` — never bare
   `git commit` or `git add -A` on the shared branch). Push when authorized.

## Constraints

- **Never redact evidence.** Full observed values, always.
- **No edges during ingest.** Submit observations only. Edge building is a separate pass.
- **Giant lanes (>10k events):** Do NOT ingest 1:1. Aggregate: extract IOCs, taxonomy,
  exemplar evidence, summary claims. Document methodology in PROVENANCE.md.
- **`lane edit --tags` REPLACES the whole tag map.** Pass the complete intended tag set
  every time or you will silently drop tags.
- **Bundle gotchas:** `type` goes inside `body`, not at top level. `actor` and
  `idempotency_key` are required. Claim `cites` cannot include `source` records.
  `ref` max 64 chars. Observation `type` inside `body`.
- **No symlinks under `data/`** — ever. They hard-fail every Factum command.
- **Lock contention:** Under concurrent writers, validate the exported batch files
  (`data/records/<batch>/records.jsonl`) instead of DB queries — same checks, no locks.
- **`/tmp` is ephemeral.** Put ingest artifacts in the lane dir or workspace.

## What to return

Per-lane results: record counts by type, commits, validator pass/fail, retraction/update
counts (should be zero for clean ingests), dedup notes (what was skipped and why),
and any root causes found (data + underlying code/process/docs fix).
