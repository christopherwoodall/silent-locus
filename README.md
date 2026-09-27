# swarmtraces-hf-corpus

Phase-two corpus for the agent-activity research: the public SwarmTraces
80,000-payload Hugging Face incident dataset.

## Relationship to the wrapped hunt

`../urlquery-api-hunt/` is **wrapped and frozen** (commit 22d65bb, 2026-09-26).
This project does NOT extend it. It ingests the SwarmTraces data in its native
schema and correlates the two corpora via shared fingerprints. The hunt repo is
a read-only reference here — never write into it.

## RubyGems go-import campaign collection (SEPARATE — pending relocation)

`data/gem-*`, `data/raw/gems/`, `scripts/*gem*.py`, `notes/gem-*`,
`notes/rubygems-rescan-2026-09-27.md`, and `data/gem-pins-diffend.txt`
belong to an **independent Diffend-sourced collection** — our own pull of
the May 11–12, 2026 RubyGems go-import meta-tag injection campaign
(Christopher's screenshots, harvested from my.diffend.io). It is **NOT**
part of the SwarmTraces dataset and NOT part of this project's corpus.
It is temporarily co-located here and will move to its own project home
(`../rubygems-goimport-campaign/`) with its own provenance record; its
Elastic index is `rubygems-goimport-campaign`.

## Standing rules (inherited)

- Agents and infrastructure only — no human/operator attribution work.
- Keep-all + annotate: nothing deleted, overlap noted in metadata.
- Provenance record for every external source (source URL, retrieval date,
  SHA-256) before it enters the corpus.
- Read-only research posture: no submissions, no accounts, no logins.
- Never execute decoded payloads.
- Every finding carries direct evidence (URL or file path + offset).

## Layout

- `data/raw/` — dataset as published, untouched. MANIFEST.json lands here.
- `data/processed/` — parsed/normalized working copies.
- `scripts/` — ingestion, fingerprint extraction, overlap joins.
- `notes/` — working notes, verification reports, the overlap plan.
