# Lane checklist — swarmtraces-hf-corpus ingest lanes (binding)

Run through this list before any dataset lands in a primary Elastic index.
A lane is not done until every box is checked against the live environment.

## Evidence
- [ ] Raw evidence is captured first (capture-first): raw bytes on disk with
      SHA-256 in the dataset dir's SHA256SUMS before any parse or ingest.
- [ ] PROVENANCE.md records sources, method, retrieval dates, and caveats;
      no absolute home-directory paths in logs or docs (project-relative only).

## Granularity (standing rule, 2026-09-28)
- [ ] **PRIMARY INDEXES HOLD EXPLICIT EVENTS ONLY (one doc per observable
      event); rollups/summaries go in `<index>-rollup` support indexes.
      Verify doc granularity against raw evidence before ingest: if one doc
      would summarize N raw rows, explode the rows into the primary and put
      the summary doc in the `<index>-rollup` index instead.**
- [ ] Doc IDs are deterministic (re-runs overwrite, never duplicate).
- [ ] `event.dataset` is set on every doc; `event.dataset.keyword` verified.

## Elastic write pause (standing rule from Christopher, 2026-09-28)
- [ ] **No cloud-cluster writes until Christopher says resume** — no _bulk
      ingests, no index creates, no deletes, no delete-by-queries, no
      forcemerges. `_count`, `_mapping`, `_search`, `_cat` are fine.
- [ ] Stage ingest payloads on disk instead: exploded explicit-event JSONLs,
      rollup JSONLs, deterministic IDs, ready-to-run scripts (which must
      refuse `--execute` while `notes/ELASTIC_WRITE_PAUSE` exists).

## Verification bar
- [ ] `_count` matches the raw evidence row count exactly after ingest.
- [ ] Zero top-level fields outside the canonical mapping
      (`notes/gems-es-mapping.json`); no field drift.
- [ ] Committed + pushed with explicit pathspecs (never `git add -A`);
      check `git status` first to avoid colliding with running lanes.

## Scope
- [ ] Agents/infrastructure only — never operator identity, registrant
      details, or person-focused attribution. Patterns, not phrases.
- [ ] Read-only research posture: no submissions, uploads, accounts, logins,
      posts, counter-increments, payload execution, or mass fetching.
- [ ] Never reproduce credentials — use the project's existing ES credential
      pattern (vault-backed skill helper).
