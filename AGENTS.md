# AGENTS.md — silent-locus repo STANDARDS

Standards for agents that hunt in this repo. This is the standards
document. Keep it tight.

## 1. One-home rule

Docs with docs, data with data, code with code. Every artifact has
exactly one canonical home. New top-level directories need operator
approval.

## 2. Canonical layout

- `AGENTS.md` — this file, repo standards.
- `README.md` — 30-second grok.
- `LICENSE`
- `animation/` — render artifacts (archival, not hunt data).
- `collections/` — ongoing collectors. Each has `collect.py` +
  `state.json` + `data/` (its working data, separate from `data/`).
- `data/` — ALL hunt data.
  - `data/<YYYY-MM-DD-slug>/` — one directory per hunt event or lane.
    Holds `events.jsonl` (observations), `PROVENANCE.md`,
    `SHA256SUMS(.txt)`, `raw/` (captured evidence), plus lane notes.
    Event name starts with the event date, not the analysis date.
  - `data/aggregates/`, `data/raw/`, `data/processed/`,
    `data/site-captures/` — cross-event aggregates, raw captures,
    processed outputs, site captures.
  - `data/transluce-api/` — Transluce Findings tracker integration.
    `LEDGER.md` (daily ingest runs), `submissions/` (numbered filing
    drafts `NNN-slug.md` + `LEDGER.md` with Prepared / ON HOLD /
    Submitted / Withdrawn), `raw/` (pulls). Read its `README.md` and
    `SCHEMA.md` before touching it.
  - `data/hf-trajectories/` — HuggingFace trajectory audits.
    `url-farm/` holds farm runs (per-group JSONs, `merged.json`,
    `lead-candidates.json`, deep-dives, `TARGET.md`); `raw/` is the
    cached HF data.
  - `data/2026-10-03-openai-agent-traces/raw/traces.jsonl` — the raw
    corpus (gitignored).
- `docs/` — standing reference: `onboarding.md`, `methodology.md`,
  `glossary.md`, `toolchain.md`, `evidence-rules.md`, `repo-map.md`.
  Ops docs: `OPERATIONS.md`, `TASKS.md`, `TODO.md`, `DATA-AUDIT.md`.
- `docs/notes/` — analyst writeups, one per investigation thread
  (`analyst-note-<topic>-<YYYY-MM-DD>.md`).
- `hidden_files/` — old lane runtime state. Stale. Do not add new.
- `lists/` — canonical hunt lists. `lists/words/` (IOC search terms),
  `lists/urls/` (URL inventory). See `lists/README.md`.
- `scripts/` — shared multi-event tooling. Single-event scripts live in
  the event dir.

## 3. Where new work goes (decision tree)

- Dated evidence or a new hunt event → `data/<YYYY-MM-DD-slug>/`.
- Ongoing collector (recurring pull) → `collections/<name>/`.
- New search term → `lists/words/`.
- New URL → `lists/urls/urls.jsonl`.
- Analysis writeup → `docs/notes/analyst-note-<topic>-<YYYY-MM-DD>.md`.
- Standing reference doc → `docs/`.
- Shared script → `scripts/`; single-event script → the event dir.
- Transluce filing draft → `data/transluce-api/submissions/NNN-slug.md`.

## 4. Naming conventions

- Event dirs: `data/<YYYY-MM-DD-slug>/` — event date, not analysis date.
- Analyst notes: `analyst-note-<topic>-<YYYY-MM-DD>.md`.
- Submission drafts: `NNN-slug.md` (`001-`, `002-`, `003-`, ...).
- Branches: `<date>-<lane>`. One-and-done: branch, work, PR, retire.

## 5. Schema docs live alongside their data

`lists/README.md` documents the wordlist and URL inventory.
`data/transluce-api/SCHEMA.md` documents the common schema. The schema
section in this file is the index. No separate `schemas/` directory.

Schema per data type:

- **events.jsonl** (per-event observations): one JSON object per line;
  the common envelope is `@timestamp`, `event{}`, `record_kind`,
  `fingerprint` (SHA-256 hex of the dataset's documented identity
  string, per PROVENANCE.md), `labels{}`. Write findings in lane docs,
  not in the event JSONL.
- **url-inventory.jsonl**: one object per line: `url`, `canonical`,
  `finding_id`, `submitter`, `source_field`, `status`, `corpus_path`
  (farm rows may add `tier`, `occurrences`). Canonical home is
  `lists/urls/urls.jsonl`. The copy at
  `data/transluce-api/url-inventory.jsonl` is LEGACY — read-only,
  because active code still points at it. New URLs go in `lists/urls/`
  only.
- **lists/words/wordlist.txt**: one IOC term per line, `#` = comment or
  section header. Exact-match dedupe (case-sensitive). Noisy/FP terms
  do not belong here.
- **lists/words/wordlist.json**: metadata superset of the txt. Fields:
  `term`, `category`, `provenance`, `added_utc` (UTC ISO-8601), `status`
  (`active` | noisy/retired), `note`. Noisy terms live here only
  (`status != active`).
- **Submission drafts**: markdown files with the full filed form
  content: Status, Transluce ID, Evidence pack, Short description,
  Detailed description, form sections as filed. Keep the numbering
  `NNN-slug.md`.
- **Farm reports**: one writeup per farm run. Coverage table, tiered URL
  inventory, keyword counts, ranked leads, with exact OBSERVED counts
  and no sampling silently hidden. Keep the raw per-group JSONs beside
  the writeup.
- **PROVENANCE.md + SHA256SUMS(.txt)**: every cached artifact needs a
  provenance record — source URL, retrieval time, retrieval method, and
  sha256 for every file. Record what changed between pulls and what
  failed. A capture without provenance is not evidence.
- **TARGET.md**: the agent targeting profile for a farm/corpus — what
  the agents were pointed at, how they accessed it, how they
  exfiltrated. Grade every claim OBSERVED / INFERENCE.

## 6. Conventions

- **NEVER redact evidence.** Keep full observed values in every
  artifact. If a value is sensitive, annotate its sensitivity beside it
  — do not remove it.
- **Provenance on everything cached.** Source URL, retrieval
  time/method, sha256. No provenance = not evidence.
- **Grade every claim**: OBSERVED (saw it in the bytes), INFERENCE
  (concluded from facts, not seen directly), UPSTREAM (another source
  said it, not checked). Mark each one. Never present INFERENCE as
  OBSERVED.
- **Keep-all, annotate.** Keep all entries; note external overlap in
  metadata, never dedupe away records. External overlap goes in a
  per-report annotation sidecar, not in the data.
- **raw/ is local-only.** Big captures stay gitignored; only curated
  evidence logs are tracked (see the `raw` exceptions in `.gitignore`).
- **Dedupe lists programmatically** after any bulk add; zero duplicates
  is the rule (dedupe keys: exact term, exact URL). The check commands
  are in `lists/README.md`.
- **Branches, not main.** One-and-done feature branches + PRs; never
  push to `main` directly without Christopher's word. Commit messages in
  the imperative mood. He pushes from his side when the branch is
  ready.
- **Lane docs in ASD-STE100**: short sentences, simple words, define a
  term on first use.
- **Scope**: agents and agent infrastructure only. Never pursue
  human/operator identity, registrant details, or social profiles.
- **Novelty rule**: before claiming any find is NEW, dedupe against (a)
  the 2026-09-28 corpus (`data/2026-09-28-chinese-amap-fleet/`,
  `data/2026-09-28-*`), (b) the Transluce findings DB via `tl.py`
  (`~/workspace/skills/transluce/bin/tl.py`), (c) `lists/` and
  `data/transluce-api/url-inventory.jsonl`. Diff against the internal
  corpus, not just the excluded list. Assume REPORTED until proven
  novel.

## 7. Quick start for a new lane

1. Make a dated branch: `git checkout -b <date>-<lane>`.
2. Create `data/<YYYY-MM-DD-slug>/`; collect evidence into `raw/`;
   write `PROVENANCE.md` and `SHA256SUMS` as you go.
3. Put observations in `events.jsonl` (common envelope); put analysis in
   `README.md` / `NOTES.md` with graded claims.
4. New search terms → `lists/words/`; new URLs →
   `lists/urls/urls.jsonl`; dedupe-check before pushing.
5. Open a PR when done. One and done — retire the branch.
