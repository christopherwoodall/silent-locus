# Repo map: annotated tree

Paths are relative to the repo root. `docs/`-relative links use `../`.

## Top level

- [`README.md`](../README.md) — dataset card: what the corpus is, the 71
  collections, schema summary, provenance methodology, loading examples.
- [`schema/`](../schema/) — `record.schema.json` (JSON Schema draft
  2020-12), `collections.md` + `collections.json` (naming taxonomy and
  registry), `README.md` (human-readable rules: timestamps, labels,
  fingerprints, `record_kind` registry).
- [`evidence/`](../evidence/) — one directory per collection,
  `YYYY-MM-DD-<subject>[-<activity>]`, each with `events.jsonl`,
  `PROVENANCE.md`, `SHA256SUMS`, `raw/`. Plus `evidence/aggregates/`
  (multi-source conglomerates).
- [`scripts/`](../scripts/) — loaders and validators at root,
  cross-collection transforms in `builders/`, reusable tools in
  `maintenance/`, preserved one-off collectors in `archive/`. Read
  `scripts/README.md` before running historical code.
- [`collections/`](../collections/) — derived corpora that are not event
  collections: `eval-questions/` (below), `deepsearchqa/`,
  `hunt-missed-surfaces/`, `urlscan-cc-feeds/`, etc.
- [`ioc-wordlist/`](../ioc-wordlist/) — the shared IOC word list (v3+,
  thousands of terms): benchmark names, marker grammars, dead-drop
  domains, eval-infrastructure markers. Watch terms, not evidence.
- [`notes/`](../notes/) — methodology notes and verification reports.
- [`docs/`](../docs/) — this directory (onboarding for people and agents).
- `elk/`, `kibana-exports/` — local Elasticsearch + Kibana dev stack
  (`make ingest`).
- `openai-agent-traces/` — incident-trace corpus (separate branch
  history; see its README).

## The hunt workspace

`evidence/2026-09-28-chinese-amap-fleet/` — the active hunt. Key files:

- [`METHODOLOGY.md`](../evidence/2026-09-28-chinese-amap-fleet/METHODOLOGY.md) —
  the hunt manual (principles, collection, detection, verification,
  OPSEC, anti-patterns). Living file.
- [`LESSONS.md`](../evidence/2026-09-28-chinese-amap-fleet/LESSONS.md) — the
  findings log: agent shapes, null results, fingerprint bank, open
  threads. Living file.
- [`PERSONA_MANIFEST.md`](../evidence/2026-09-28-chinese-amap-fleet/PERSONA_MANIFEST.md) —
  the lane registry.
- [`IP_LOG.md`](../evidence/2026-09-28-chinese-amap-fleet/IP_LOG.md) —
  infrastructure observations log.
- [`SSLIP-REPORT.md`](../evidence/2026-09-28-chinese-amap-fleet/SSLIP-REPORT.md) —
  the sslip.io dead-drop investigation (OBSERVED vs INFERENCE labeled).

Key directories:

- [`personas/`](../evidence/2026-09-28-chinese-amap-fleet/personas/) — 69
  analyst lanes, each with `FINDINGS.md`/`CHASE.md` + `raw/`.
- [`raw/lanes/`](../evidence/2026-09-28-chinese-amap-fleet/raw/lanes/) — 9
  sweep lanes with `FINDINGS.md`.
- [`studies/`](../evidence/2026-09-28-chinese-amap-fleet/studies/) — deep
  studies:
  - `skill-egress-top500/` — the original egress study (EGRESS_MAP.md,
    SKILLS.md).
  - `skill-egress-top1000/` — the extension: `EGRESS_MAP.md`,
    `SKILLS.md`, `SCAN-LOG.md`, `INVESTIGATION-REPORT.md` (the integrated
    2026-10-05 report — start here), `HYGIENE-AUDIT.md`,
    `why-these-sites/` (thesis test: WHY-SITES.md,
    TRADECRAFT-RESURGENCE.md, CORRECTIONS-LOG.md,
    `linkhunt-deep/LINKHUNT-DEEP.md`).
  - `eu-hunt/`, `wiki-hunt-2/`, `msgboard-hunt-2/`,
    `shodan-chat-transcripts/` — other completed studies.
- [`german-french-swarm-hunt/`](../evidence/2026-09-28-chinese-amap-fleet/german-french-swarm-hunt/) —
  EUROSWARM assessment (verdict: not found) + `clipboard-followup/`
  (CLIPBOARD-REPORT.md).
- [`village-join/`](../evidence/2026-09-28-chinese-amap-fleet/village-join/) —
  AI Village cross-dataset join: VILLAGE-JOIN-2.md (results),
  matches-2025.jsonl, WORKLOG.md.
- [`live-monitor/`](../evidence/2026-09-28-chinese-amap-fleet/live-monitor/) —
  monitor logs (LOG.md).
- [`infra-watchlist/`](../evidence/2026-09-28-chinese-amap-fleet/infra-watchlist/) —
  INFRASTRUCTURE-WATCHLIST.md, the living infrastructure list.
- [`counsel/`](../evidence/2026-09-28-chinese-amap-fleet/counsel/) — red-team
  review rounds and grades.
- `slug-hunt.py` — cross-archive slug presence sweep (urlquery + urlscan
  + Wayback CDX). See [`toolchain.md`](toolchain.md).

## Eval-questions corpus

`collections/eval-questions/`:

- [`EVAL_QUESTIONS.md`](../collections/eval-questions/EVAL_QUESTIONS.md) —
  index: per-eval counts, licenses, topic/source distributions.
- [`HUNT-QUERIES.md`](../collections/eval-questions/HUNT-QUERIES.md) —
  50 ranked fingerprint queries with per-surface search strings.
- [`all-questions.jsonl`](../collections/eval-questions/all-questions.jsonl) —
  10,201 records: eval, question, topic, expected sources, fingerprint
  phrases, license.
- Per-eval dirs: `raw/` (byte-identical downloads) + `questions.jsonl` +
  `NOTES.md` (source URL, license, retrieval date).
- `_tools/` — stdlib-only parquet reader + normalizer.

## Where things live by task

| I want to… | Go to |
|---|---|
| Understand the hunt | `docs/onboarding.md`, `docs/methodology.md` |
| Cite the evidence contract | `docs/evidence-rules.md` |
| Look up jargon | `docs/glossary.md` |
| Run a hunt lane | `evidence/2026-09-28-chinese-amap-fleet/personas/<lane>/` |
| Read current findings | `…/LESSONS.md`, `…/studies/skill-egress-top1000/INVESTIGATION-REPORT.md` |
| Hunt eval fingerprints | `collections/eval-questions/HUNT-QUERIES.md` |
| Check a slug across archives | `…/slug-hunt.py` (see `docs/toolchain.md`) |
| Add a collection | `schema/collections.md`, `scripts/validate_collections.py` |
| Check IOC coverage | `ioc-wordlist/` |
