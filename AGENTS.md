# AGENTS.md — silent-locus agent reference

Working guide for agents that hunt in this repo. Keep it tight; when in
doubt, read `lists/README.md` and the nearest PROVENANCE.md.

## Directory layout

- `data/<YYYY-MM-DD-slug>/` — one directory per hunt event or lane.
  Each holds `events.jsonl` (observations), `PROVENANCE.md`,
  `SHA256SUMS(.txt)`, `raw/` (captured evidence), plus lane-specific
  scripts and notes. Event names start with the event date, not the
  analysis date.
- `data/transluce-api/` — Transluce Findings tracker integration. Read
  `README.md` (definitions, findings so far), `SCHEMA.md` (common schema
  for Transluce findings x our observation corpus), `LEDGER.md` (daily
  ingest runs). `raw/` holds pulls; `submissions/` holds filing drafts.
- `data/hf-trajectories/` — HuggingFace trajectory audits. Farm-level
  writeups live here (`URL-KEYWORD-FARM.md`, `ADVERSARIAL.md`,
  `CROSSREF.md`, `RANKED-HITS.md`, `candidates.md`). `url-farm/` holds
  farm runs: per-group JSONs, `merged.json`, `lead-candidates.json`,
  deep-dives, and `TARGET.md` (agent targeting profile). `raw/` is the
  cached HF data; specific large subdirs are gitignored.
- `lists/` — canonical hunt lists, one home for everything.
  `lists/words/` holds the IOC search-term wordlist; `lists/urls/`
  holds the URL inventory. See "Schema" below and `lists/README.md`.
- `data/transluce-api/submissions/` — Transluce filing ledger +
  numbered drafts (`001-*.md`, `002-*.md`, `003-*.md`). Its own
  `LEDGER.md` tracks Prepared / ON HOLD / Submitted / Withdrawn.
- `collections/` — cross-event indexes and curated collections
  (e.g. `collections/README.md`, `linkage-evidence/`, `eval-questions/`).
- `scripts/`, `schema/`, `workers/` — shared tooling and the common
  event schema. Put single-event scripts in the event dir; put
  multi-event parsers in `scripts/`.

## Schema per data type

- **events.jsonl** (per-event observations): one JSON object per line;
  see `schema/` for the common envelope (`@timestamp`, `event{}`,
  `record_kind`, `fingerprint` = SHA-256 hex of the dataset's documented identity string (per PROVENANCE.md), `labels{}`).
  Write findings in lane docs, not in the event JSONL.
- **url-inventory.jsonl**: one object per line: `url`, `canonical`,
  `finding_id`, `submitter`, `source_field`, `status`, `corpus_path`
  (farm rows may add `tier`, `occurrences`). Canonical home is
  `lists/urls/urls.jsonl`; the copy at `data/transluce-api/url-inventory.jsonl`
  is LEGACY — read-only, because active code still points at it. New URLs
  go in `lists/urls/` only.
- **lists/words/wordlist.txt**: one IOC term per line, `#` = comment or
  section header. Exact-match dedupe (case-sensitive); noisy/FP terms do
  not belong here.
- **lists/words/wordlist.json**: metadata superset of the txt. Fields:
  `term`, `category`, `provenance`, `added_utc` (UTC ISO-8601), `status`
  (`active` | noisy/retired), `note`. Noisy terms live here only
  (`status != active`).
- **Submission drafts**: markdown files with the full filed form content:
  Status, Transluce ID, Evidence pack, Short description, Detailed
  description, form sections as filed. Keep the numbering `NNN-slug.md`.
- **Farm reports**: one writeup per farm run (`URL-KEYWORD-FARM.md`):
  coverage table, tiered URL inventory, keyword counts, ranked leads, with
  exact OBSERVED counts and no sampling silently hidden. Keep the raw
  per-group JSONs beside the writeup.
- **PROVENANCE.md + SHA256SUMS(.txt)**: every cached artifact needs a
  provenance record — source URL, retrieval time, retrieval method, and
  sha256 for every file. Record what changed between pulls and what failed.
  A capture without provenance is not evidence.
- **TARGET.md**: the agent targeting profile for a farm/corpus — what the
  agents were pointed at, how they accessed it, how they exfiltrated.
  Grade every claim OBSERVED / INFERENCE.

## Conventions

- **NEVER redact evidence.** Keep full observed values in every artifact.
  If a value is sensitive, annotate its sensitivity beside it — do not
  remove it.
- **Provenance on everything cached.** Source URL, retrieval time/method,
  sha256. No provenance = not evidence.
- **Grade every claim**: OBSERVED (saw it in the bytes), INFERENCE
  (concluded from facts, not seen directly), UPSTREAM (another source
  said it, not checked). Mark each one; never present INFERENCE as
  OBSERVED.
- **Keep-all, annotate.** Keep all entries; note external overlap in
  metadata, never dedupe away records. External overlap goes in a
  per-report annotation sidecar, not in the data.
- **raw/ is local-only.** Big captures stay gitignored; only curated
  evidence logs are tracked (see the `raw` exceptions in `.gitignore`).
- **Dedupe lists programmatically** after any bulk add; zero duplicates
  is the rule (dedupe keys: exact term, exact URL). The check commands
  are in `lists/README.md`.
- **Branches, not main.** One-and-done feature branches + PRs; never push
  to `main` directly without Christopher's word. Commit messages in the
  imperative mood. He pushes from his side when the branch is ready.
- **Lane docs in ASD-STE100**: short sentences, simple words, define a
  term on first use.
- **Scope**: agents and agent infrastructure only. Never pursue
  human/operator identity, registrant details, or social profiles.

## Key files

- `data/transluce-api/README.md` — findings pulled so far, definitions
  (finding, observation, dead-drop, beacon, epoch, fingerprint).
- `data/transluce-api/SCHEMA.md` — the common two-layer schema: Transluce
  findings (analyst conclusions) x our observation corpus (records).
- `data/transluce-api/LEDGER.md` — running record of daily ingest runs
  into the corpus.
- `data/transluce-api/submissions/LEDGER.md` — what we filed on the
  Transluce tracker and its status. Submission drafts live beside it.
- `data/hf-trajectories/URL-KEYWORD-FARM.md` — canonical farm report
  template; `url-farm/TARGET.md` — agent targeting profile.
- `lists/README.md` — canonical-location notes, add-entry procedures,
  dedupe verification commands.

## Quick start for a new lane

1. Make a dated branch: `git checkout -b <date>-<lane>`.
2. Create `data/<YYYY-MM-DD-slug>/`; collect evidence into `raw/`;
   write `PROVENANCE.md` and `SHA256SUMS` as you go.
3. Put observations in `events.jsonl` (common envelope); put analysis in
   `README.md` / `NOTES.md` with graded claims.
4. New search terms → `lists/words/`; new URLs → `lists/urls/urls.jsonl`;
   dedupe-check before pushing.
5. Open a PR when done. One and done — retire the branch.
